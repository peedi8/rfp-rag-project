"""Re-judge saved answers under multiple evidence-context views.

This is a validation tool for judge-bias checks. It keeps the saved answer
fixed and changes only what evidence context the judge sees:

- old_slice: first 4000 chars of concatenated retrieved chunks
- balanced: per-chunk metadata + excerpt
- strict_unsupported: asks specifically for unsupported concrete claims
"""
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
from scripts.edd_score import add_edd_columns
from scripts.evaluate import _chat_json, _format_judge_context
from src.retriever import retrieve


ROOT = Path(__file__).resolve().parents[1]
CONTROL = {
    "use_mmr": True,
    "top_k": 8,
    "mmr_lambda": 0.5,
    "fetch_k": 20,
    "auto_filter": True,
    "rerank": False,
}


def load_details(path: Path, experiment: str | None) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if experiment:
        return data[experiment]["details"]
    if len(data) != 1:
        raise SystemExit(f"--experiment is required; details has keys: {', '.join(data)}")
    return next(iter(data.values()))["details"]


def load_questions(path: Path) -> dict[str, dict[str, Any]]:
    return {q["id"]: q for q in json.loads(path.read_text(encoding="utf-8"))}


def context_for_question(case: dict[str, Any], top_k: int) -> tuple[str, str, list[str]]:
    query = case["turns"][-1]
    chunks = retrieve(
        query,
        top_k=top_k,
        use_mmr=CONTROL["use_mmr"],
        mmr_lambda=CONTROL["mmr_lambda"],
        fetch_k=CONTROL["fetch_k"],
        auto_filter=True,
        rerank=False,
    )
    old_context = "\n".join(c["text"] for c in chunks)[:4000]
    balanced_context = _format_judge_context(chunks)
    orgs = [c["metadata"].get("발주 기관", "") for c in chunks]
    return old_context, balanced_context, orgs


def judge_groundedness(query: str, context: str, answer: str) -> dict[str, Any]:
    from openai import OpenAI

    prompt = f"""다음은 RAG 시스템의 (질문 / 검색된 근거 / 답변)입니다.
아래 두 항목을 각각 0~5 정수로 채점하세요.
- groundedness: 답변이 '검색된 근거'에 의해 뒷받침되는 정도 (근거에 없는 내용을 지어내면 낮음)
- relevance: 답변이 '질문'에 실제로 답하는 정도
반드시 JSON 객체로만 답하세요: {{"groundedness": 0, "relevance": 0, "reason": "..."}}

[질문] {query}
[검색된 근거] {context[:config.JUDGE_CONTEXT_CHARS]}
[답변] {answer}"""
    data = _chat_json(OpenAI(api_key=config.OPENAI_API_KEY), prompt, max_tokens=config.JUDGE_MAX_TOKENS, model=config.JUDGE_MODEL)
    return {
        "groundedness": data.get("groundedness"),
        "relevance": data.get("relevance"),
        "reason": data.get("reason", ""),
        "judge_model": config.JUDGE_MODEL,
    }


def judge_unsupported(query: str, context: str, answer: str) -> dict[str, Any]:
    from openai import OpenAI

    prompt = f"""다음 답변에서 '검색된 근거'로 확인되지 않는 구체 주장만 엄격하게 찾으세요.
숫자, 날짜, 버전, 기관명, 사업명, 요구사항 번호, 기능명, 산출물명, 동일/차수 판단을 특히 엄격히 봅니다.
근거가 충분하면 unsupported_claims는 빈 배열로 두세요.
반드시 JSON 객체로만 답하세요:
{{
  "unsupported_claims": ["..."],
  "severity": 0,
  "groundedness_skeptical": 0,
  "reason": "..."
}}

[질문] {query}
[검색된 근거] {context[:config.JUDGE_CONTEXT_CHARS]}
[답변] {answer}"""
    data = _chat_json(OpenAI(api_key=config.OPENAI_API_KEY), prompt, max_tokens=config.JUDGE_MAX_TOKENS, model=config.JUDGE_MODEL)
    return {
        "unsupported_claims": data.get("unsupported_claims", []),
        "severity": data.get("severity"),
        "groundedness_skeptical": data.get("groundedness_skeptical"),
        "reason": data.get("reason", ""),
        "judge_model": config.JUDGE_MODEL,
    }


def avg(values: list[float]) -> float | None:
    vals = [v for v in values if isinstance(v, (int, float))]
    return round(sum(vals) / len(vals), 3) if vals else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--details", required=True)
    ap.add_argument("--experiment", default=None)
    ap.add_argument("--questions", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--case-ids", default="")
    ap.add_argument("--top-k", type=int, default=8)
    args = ap.parse_args()

    details = load_details(Path(args.details), args.experiment)
    questions = load_questions(Path(args.questions))
    wanted = {x.strip() for x in args.case_ids.split(",") if x.strip()}
    if wanted:
        details = [d for d in details if d["id"] in wanted]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for detail in details:
        case = questions.get(detail["id"])
        if not case or case.get("expect_abstention"):
            continue
        query = case["turns"][-1]
        answer = detail.get("answer", "")
        old_context, balanced_context, orgs = context_for_question(case, args.top_k)
        old_judge = judge_groundedness(query, old_context, answer)
        balanced_judge = judge_groundedness(query, balanced_context, answer)
        strict_audit = judge_unsupported(query, balanced_context, answer)
        rows.append({
            "id": detail["id"],
            "type": detail.get("type"),
            "query": query,
            "retrieved_orgs_rebuilt": orgs,
            "saved_judge": detail.get("judge"),
            "old_slice_judge": old_judge,
            "balanced_judge": balanced_judge,
            "strict_unsupported_audit": strict_audit,
            "delta_groundedness": (
                balanced_judge.get("groundedness") - old_judge.get("groundedness")
                if isinstance(balanced_judge.get("groundedness"), (int, float))
                and isinstance(old_judge.get("groundedness"), (int, float))
                else None
            ),
        })
        (out_dir / "rejudge_results.jsonl").open("a", encoding="utf-8").write(json.dumps(rows[-1], ensure_ascii=False) + "\n")

    summary_metrics = {
        "old_groundedness_avg": avg([r["old_slice_judge"].get("groundedness") for r in rows]),
        "balanced_groundedness_avg": avg([r["balanced_judge"].get("groundedness") for r in rows]),
        "old_relevance_avg": avg([r["old_slice_judge"].get("relevance") for r in rows]),
        "balanced_relevance_avg": avg([r["balanced_judge"].get("relevance") for r in rows]),
        "unsupported_severity_avg": avg([r["strict_unsupported_audit"].get("severity") for r in rows]),
        "checked_cases": len(rows),
    }
    summary = {
        "schema": "judge_bias_recheck.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_details": args.details,
        "questions": args.questions,
        "case_ids": [r["id"] for r in rows],
        "metrics": summary_metrics,
        "rows": rows,
    }
    (out_dir / "rejudge_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Judge Bias Recheck",
        "",
        f"- checked_cases: {summary_metrics['checked_cases']}",
        f"- old_groundedness_avg: **{summary_metrics['old_groundedness_avg']}**",
        f"- balanced_groundedness_avg: **{summary_metrics['balanced_groundedness_avg']}**",
        f"- old_relevance_avg: **{summary_metrics['old_relevance_avg']}**",
        f"- balanced_relevance_avg: **{summary_metrics['balanced_relevance_avg']}**",
        f"- unsupported_severity_avg: **{summary_metrics['unsupported_severity_avg']}**",
        "",
        "## Cases",
    ]
    for row in rows:
        lines.extend([
            f"### {row['id']}",
            f"- old: g={row['old_slice_judge'].get('groundedness')}, r={row['old_slice_judge'].get('relevance')}",
            f"- balanced: g={row['balanced_judge'].get('groundedness')}, r={row['balanced_judge'].get('relevance')}",
            f"- delta_groundedness: {row['delta_groundedness']}",
            f"- unsupported severity: {row['strict_unsupported_audit'].get('severity')}",
            f"- unsupported claims: {row['strict_unsupported_audit'].get('unsupported_claims')}",
            "",
        ])
    (out_dir / "rejudge_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    contract = {
        "schema": "parallel_team_worker_output.v1",
        "worker_id": "main_rejudge_saved_answers",
        "task_id": "judge_bias_check",
        "status": "proposal",
        "summary": (
            f"rejudged {summary_metrics['checked_cases']} saved answers; "
            f"old_g={summary_metrics['old_groundedness_avg']} balanced_g={summary_metrics['balanced_groundedness_avg']}"
        ),
        "inputs": [args.details, args.questions],
        "protected_paths_seen": ["업무일지.md", "eval/experiment_log.md", "eval/next_improvement_tasks.md", "config.py", "src/**", "scripts/**"],
        "directly_modified_protected_paths": [],
        "outputs": [
            {"path": str(out_dir / "rejudge_summary.json"), "kind": "json", "description": "same-answer judge comparison"},
            {"path": str(out_dir / "rejudge_summary.md"), "kind": "md", "description": "human-readable judge comparison"},
            {"path": str(out_dir / "rejudge_results.jsonl"), "kind": "data", "description": "per-case checkpointed rejudge rows"},
        ],
        "proposal": {
            "accepted_fields_or_changes": [summary_metrics],
            "rejected_or_risky_items": [],
            "needs_orchestrator_review": [
                "If balanced scores rise but strict unsupported audit flags concrete claims, treat the gain as suspect.",
                "Do not claim model improvement from judge-context-only changes.",
            ],
        },
        "merge_risk": "low",
        "blocking_reason": "",
        "validation": {
            "commands_run": [" ".join(sys.argv)],
            "observed_results": [f"checked_cases={summary_metrics['checked_cases']}"],
        },
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    (out_dir / "worker_output.json").write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(contract, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
