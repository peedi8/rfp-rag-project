from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


MODEL_PRICES_PER_MTOK = {
    "gpt-5-mini": {"input": 0.75, "output": 4.50},
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"), strict=False)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _price_for_model(model: str) -> dict[str, float]:
    return MODEL_PRICES_PER_MTOK.get(model, MODEL_PRICES_PER_MTOK["gpt-5-mini"])


def _estimate_tokens(text: str) -> int:
    return max(1, int(len(text) / 4) + 1)


def _cost_usd(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    price = _price_for_model(model)
    return round((prompt_tokens / 1_000_000) * price["input"] + (completion_tokens / 1_000_000) * price["output"], 6)


def chat_json(model: str, prompt: str, max_tokens: int, timeout_sec: float) -> tuple[dict[str, Any], dict[str, Any]]:
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
    usage_obj = getattr(resp, "usage", None)
    usage = {}
    if usage_obj is not None:
        usage = {
            "prompt_tokens": getattr(usage_obj, "prompt_tokens", None),
            "completion_tokens": getattr(usage_obj, "completion_tokens", None),
            "total_tokens": getattr(usage_obj, "total_tokens", None),
        }
    try:
        return json.loads(content), usage
    except Exception:
        start, end = content.find("{"), content.rfind("}")
        if start >= 0 and end > start:
            return json.loads(content[start : end + 1]), usage
        return {"parse_error": True, "raw": content}, usage


def build_prompt(case: dict[str, Any]) -> str:
    snippets = "\n".join(f"- {s}" for s in case.get("evidence_snippets", []))
    return f"""다음은 RFP RAG 답변 채점 검증용 케이스입니다.
채점자는 expected_decision을 모르는 상태라고 가정하고, 답변이 근거와 질문에 맞는지만 보세요.

반드시 JSON 객체로만 답하세요.
스키마:
{{
  "decision": "pass | fail",
  "groundedness": 0,
  "relevance": 0,
  "risk_flags": ["hallucination | wrong_document | contradicted_evidence | under_refusal | over_refusal | privacy_violation | scope_mix | under_answer"],
  "reason": "구체적인 한국어 이유"
}}

점수는 반드시 0부터 5까지의 정수로만 쓰세요.
- groundedness: 0=근거와 맞지 않음, 5=근거에 완전히 충실함.
- relevance: 0=질문에 답하지 않음, 5=질문에 직접 답함.
- 답변에 근거 없는 세부사항, 다른 문서 내용 섞임, 근거와 모순되는 주장이 있으면 decision은 fail이고 groundedness는 최대 2입니다.
- 확신이 낮으면 높은 점수를 주지 말고 낮은 점수와 risk_flags로 표시하세요.

[질문]
{case.get("question", "")}

[근거 범위]
{json.dumps(case.get("evidence_scope", {}), ensure_ascii=False)}

[근거 조각]
{snippets}

[후보 답변]
{case.get("candidate_answer", "")}
"""


def score_match(case: dict[str, Any], judge: dict[str, Any]) -> dict[str, Any]:
    expected_decision = case.get("expected_decision")
    actual_decision = judge.get("decision")
    expected_flags = set(case.get("expected_flags") or [])
    actual_flags = set(judge.get("risk_flags") or [])
    groundedness = judge.get("groundedness")
    relevance = judge.get("relevance")
    flag_overlap = sorted(expected_flags & actual_flags)
    score_range_ok = (
        isinstance(groundedness, (int, float))
        and isinstance(relevance, (int, float))
        and 0 <= groundedness <= 5
        and 0 <= relevance <= 5
    )
    bounds_ok = True
    if isinstance(groundedness, (int, float)):
        if "expected_groundedness_min" in case:
            bounds_ok = bounds_ok and groundedness >= case["expected_groundedness_min"]
        if "expected_groundedness_max" in case:
            bounds_ok = bounds_ok and groundedness <= case["expected_groundedness_max"]
    else:
        bounds_ok = False
    return {
        "decision_match": actual_decision == expected_decision,
        "decision_value_ok": actual_decision in {"pass", "fail"},
        "score_range_ok": score_range_ok,
        "groundedness_bounds_ok": bounds_ok,
        "expected_flags": sorted(expected_flags),
        "actual_flags": sorted(actual_flags),
        "flag_overlap": flag_overlap,
        "flag_overlap_count": len(flag_overlap),
    }


def expected_row(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": case["id"],
        "status": "not_called",
        "expected_decision": case.get("expected_decision"),
        "expected_flags": case.get("expected_flags", []),
        "expected_groundedness_min": case.get("expected_groundedness_min"),
        "expected_groundedness_max": case.get("expected_groundedness_max"),
        "why": case.get("why", ""),
    }


def summarize(rows: list[dict[str, Any]], no_api: bool) -> dict[str, Any]:
    if no_api:
        return {
            "mode": "no_api",
            "cases": len(rows),
            "expected_pass": sum(1 for r in rows if r.get("expected_decision") == "pass"),
            "expected_fail": sum(1 for r in rows if r.get("expected_decision") == "fail"),
        }
    checked = [r for r in rows if r.get("status") == "ok"]
    return {
        "mode": "judge_called",
        "cases": len(rows),
        "checked": len(checked),
        "decision_matches": sum(1 for r in checked if r.get("comparison", {}).get("decision_match")),
        "decision_value_ok": sum(1 for r in checked if r.get("comparison", {}).get("decision_value_ok")),
        "score_range_ok": sum(1 for r in checked if r.get("comparison", {}).get("score_range_ok")),
        "groundedness_bounds_ok": sum(1 for r in checked if r.get("comparison", {}).get("groundedness_bounds_ok")),
        "estimated_cost_usd": round(sum(float(r.get("cost", {}).get("estimated_usd") or 0) for r in rows), 6),
        "actual_cost_usd": round(sum(float(r.get("cost", {}).get("actual_usd") or 0) for r in rows), 6),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Blind Judge Calibration Results",
        "",
        f"- created_at: {result['created_at']}",
        f"- model: {result['model']}",
        f"- mode: {result['summary']['mode']}",
        f"- cases: {result['summary']['cases']}",
        "",
        "## Summary",
        "",
    ]
    for key, value in result["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Cases", ""])
    for row in result["rows"]:
        lines.append(f"### {row.get('case_id')}")
        if row.get("status") == "ok":
            judge = row.get("judge", {})
            comparison = row.get("comparison", {})
            lines.extend([
                f"- expected_decision: {row.get('expected_decision')}",
                f"- judge_decision: {judge.get('decision')}",
                f"- groundedness: {judge.get('groundedness')}",
                f"- relevance: {judge.get('relevance')}",
                f"- risk_flags: {', '.join(judge.get('risk_flags') or [])}",
                f"- decision_match: {comparison.get('decision_match')}",
                f"- score_range_ok: {comparison.get('score_range_ok')}",
                f"- groundedness_bounds_ok: {comparison.get('groundedness_bounds_ok')}",
                f"- reason: {judge.get('reason')}",
                "",
            ])
        else:
            lines.extend([
                f"- status: {row.get('status')}",
                f"- expected_decision: {row.get('expected_decision')}",
                f"- expected_flags: {', '.join(row.get('expected_flags') or [])}",
                f"- why: {row.get('why')}",
                "",
            ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--model", default=config.JUDGE_MODEL)
    parser.add_argument("--timeout-sec", type=float, default=90)
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--no-api", action="store_true")
    parser.add_argument("--budget-cap-usd", type=float, default=None)
    parser.add_argument("--hard-stop-usd", type=float, default=None)
    parser.add_argument("--budget-ledger", default="")
    args = parser.parse_args()

    pack = load_json(Path(args.input))
    cases = list(pack.get("cases", []))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = out_dir / "calibration_results.jsonl"
    budget_ledger = Path(args.budget_ledger) if args.budget_ledger else out_dir / "budget_ledger.jsonl"

    rows: list[dict[str, Any]] = []
    spent_actual = 0.0
    spent_estimated = 0.0
    for case in cases:
        prompt = build_prompt(case)
        estimated_prompt_tokens = _estimate_tokens(prompt)
        estimated_completion_tokens = args.max_tokens
        estimated_cost = _cost_usd(args.model, estimated_prompt_tokens, estimated_completion_tokens)
        hard_stop = args.hard_stop_usd if args.hard_stop_usd is not None else args.budget_cap_usd
        if not args.no_api and hard_stop is not None and spent_actual + estimated_cost > hard_stop:
            row = {
                "case_id": case["id"],
                "status": "skipped_budget",
                "expected_decision": case.get("expected_decision"),
                "cost": {
                    "estimated_usd": estimated_cost,
                    "actual_usd": 0.0,
                    "spent_actual_before": round(spent_actual, 6),
                    "hard_stop_usd": hard_stop,
                },
            }
            rows.append(row)
            append_jsonl(checkpoint_path, row)
            append_jsonl(budget_ledger, row)
            continue
        if args.no_api:
            row = expected_row(case)
        else:
            try:
                judge, usage = chat_json(args.model, prompt, args.max_tokens, args.timeout_sec)
                actual_prompt_tokens = int(usage.get("prompt_tokens") or estimated_prompt_tokens)
                actual_completion_tokens = int(usage.get("completion_tokens") or 0)
                actual_cost = _cost_usd(args.model, actual_prompt_tokens, actual_completion_tokens)
                spent_actual += actual_cost
                spent_estimated += estimated_cost
                row = {
                    "case_id": case["id"],
                    "status": "ok",
                    "expected_decision": case.get("expected_decision"),
                    "judge": judge,
                    "comparison": score_match(case, judge),
                    "usage": usage,
                    "cost": {
                        "estimated_usd": estimated_cost,
                        "actual_usd": actual_cost,
                        "spent_actual_after": round(spent_actual, 6),
                        "spent_estimated_after": round(spent_estimated, 6),
                    },
                }
            except Exception as exc:
                row = {
                    "case_id": case["id"],
                    "status": "failed",
                    "expected_decision": case.get("expected_decision"),
                    "error": f"{type(exc).__name__}: {exc}",
                    "cost": {
                        "estimated_usd": estimated_cost,
                        "actual_usd": 0.0,
                        "spent_actual_after": round(spent_actual, 6),
                    },
                }
        rows.append(row)
        append_jsonl(checkpoint_path, row)
        append_jsonl(budget_ledger, row)

    result = {
        "schema": "rfp_rag_blind_judge_calibration_results.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "input": str(Path(args.input).resolve()),
        "model": args.model,
        "no_api": args.no_api,
        "budget": {
            "budget_cap_usd": args.budget_cap_usd,
            "hard_stop_usd": args.hard_stop_usd,
            "pricing_per_mtok": _price_for_model(args.model),
            "budget_ledger": str(budget_ledger),
        },
        "summary": summarize(rows, args.no_api),
        "rows": rows,
    }
    write_json(out_dir / "calibration_results.json", result)
    (out_dir / "calibration_results.md").write_text(render_markdown(result), encoding="utf-8")
    print(json.dumps({"out_dir": str(out_dir), "summary": result["summary"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
