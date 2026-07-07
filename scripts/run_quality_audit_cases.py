from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


SCHEMA = "rfp_rag_scripted_quality_audit_results.v1"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"), strict=False)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def trim(value: Any, limit: int) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if len(text) > limit:
        return text[:limit].rstrip() + "\n...(truncated)"
    return text


def chat_json(model: str, prompt: str, max_tokens: int, timeout_sec: float) -> dict[str, Any]:
    from openai import OpenAI

    client = OpenAI(api_key=config.OPENAI_API_KEY, timeout=timeout_sec)
    kwargs = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_completion_tokens": max_tokens,
    }
    try:
        resp = client.chat.completions.create(response_format={"type": "json_object"}, **kwargs)
    except Exception:
        resp = client.chat.completions.create(**kwargs)
    content = (resp.choices[0].message.content or "").strip()
    try:
        return json.loads(content)
    except Exception:
        start, end = content.find("{"), content.rfind("}")
        if start >= 0 and end > start:
            return json.loads(content[start : end + 1])
        return {"parse_error": True, "raw": content}


def build_prompt(case: dict[str, Any]) -> str:
    metrics = case.get("metrics_snapshot", {})
    question = " / ".join(case.get("turns") or [])
    return f"""다음 RFP RAG 답변을 독립적인 품질 감리자 관점에서 평가하세요.
자동 점수나 EDD를 그대로 믿지 말고, 실제 질문 맥락에 맞는 답인지 판단하세요.

반드시 JSON 객체로만 답하세요.
스키마:
{{
  "case_id": "{case.get('case_id', '')}",
  "contextual_quality": 1,
  "evidence_fit": 1,
  "usefulness": 1,
  "conciseness": 1,
  "decision": "pass | pass_with_caveat | fail",
  "risk_flags": ["hallucination | over_refusal | under_refusal | wrong_document | verbosity | missing_citation | unclear_source | context_mismatch"],
  "reason": "구체적인 한국어 근거",
  "recommended_next_action": "keep | revise_prompt | revise_retrieval | add_question | manual_review"
}}

[case_id]
{case.get('case_id', '')}

[질문]
{question}

[목표 기관]
{case.get('target_orgs', [])}

[자동 플래그]
{case.get('automatic_flags', [])}

[자동 지표]
coverage={metrics.get('coverage')}, first_hit_rank={metrics.get('first_hit_rank')}, abstention={metrics.get('abstention')}, latency={metrics.get('latency_sec')}, EDD={case.get('edd_score')}

[검색된 기관]
{case.get('retrieved_orgs', [])}

[답변]
{trim(case.get('answer'), 6000)}
"""


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = Counter(r.get("decision", "unknown") for r in results)
    risks = Counter(flag for r in results for flag in (r.get("risk_flags") or []))
    return {
        "pass": decisions.get("pass", 0),
        "pass_with_caveat": decisions.get("pass_with_caveat", 0),
        "fail": decisions.get("fail", 0),
        "unknown": decisions.get("unknown", 0),
        "most_common_risks": [flag for flag, _ in risks.most_common(8)],
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Scripted Quality Audit Results",
        "",
        f"- created_at: {result['created_at']}",
        f"- model: {result['model']}",
        f"- input: `{result['input']}`",
        f"- cases_requested: {result['cases_requested']}",
        f"- cases_completed: {result['cases_completed']}",
        "",
        "## Summary",
        "",
    ]
    for key, value in result["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Cases", ""])
    for row in result["results"]:
        lines.extend(
            [
                f"### {row.get('case_id')}",
                "",
                f"- decision: {row.get('decision')}",
                f"- contextual_quality: {row.get('contextual_quality')}",
                f"- evidence_fit: {row.get('evidence_fit')}",
                f"- usefulness: {row.get('usefulness')}",
                f"- conciseness: {row.get('conciseness')}",
                f"- risk_flags: {', '.join(row.get('risk_flags') or [])}",
                f"- recommended_next_action: {row.get('recommended_next_action')}",
                f"- reason: {row.get('reason')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="audit_input.json/audit_input_top8.json")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--model", default=config.JUDGE_MODEL)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--timeout-sec", type=float, default=120)
    parser.add_argument("--max-tokens", type=int, default=1200)
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = out_dir / "audit_results.jsonl"
    result_json = out_dir / "audit_results.json"
    result_md = out_dir / "audit_results.md"

    data = load_json(input_path)
    cases = list(data.get("cases", []))
    if args.case_id:
        wanted = set(args.case_id)
        cases = [case for case in cases if case.get("case_id") in wanted or case.get("question_id") in wanted]
    if args.limit > 0:
        cases = cases[: args.limit]

    completed: list[dict[str, Any]] = []
    for index, case in enumerate(cases, start=1):
        row_base = {
            "case_id": case.get("case_id"),
            "question_id": case.get("question_id"),
            "model": args.model,
            "audited_at": datetime.now().isoformat(timespec="seconds"),
            "source_flags": case.get("automatic_flags", []),
        }
        try:
            audit = chat_json(args.model, build_prompt(case), args.max_tokens, args.timeout_sec)
            row = {**row_base, **audit, "status": "ok"}
        except Exception as exc:
            row = {
                **row_base,
                "status": "failed",
                "decision": "unknown",
                "risk_flags": ["audit_call_failed"],
                "reason": f"{type(exc).__name__}: {exc}",
                "recommended_next_action": "manual_review",
            }
        completed.append(row)
        append_jsonl(checkpoint_path, row)
        print(json.dumps({"done": index, "total": len(cases), "case_id": row.get("case_id"), "status": row["status"]}, ensure_ascii=False))

    result = {
        "schema": SCHEMA,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "input": str(input_path),
        "model": args.model,
        "cases_requested": len(cases),
        "cases_completed": len(completed),
        "checkpoint_jsonl": str(checkpoint_path),
        "summary": summarize(completed),
        "results": completed,
    }
    write_json(result_json, result)
    result_md.write_text(render_markdown(result), encoding="utf-8")
    print(json.dumps({"out_dir": str(out_dir), "cases_completed": len(completed), "summary": result["summary"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
