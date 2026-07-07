from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA = "rfp_rag_quality_audit_pack.v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), strict=False)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_text(value: Any, limit: int | None = None) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if limit is not None and len(text) > limit:
        return text[:limit].rstrip() + "\n...(truncated; full text is in audit_input.json)"
    return text


def number(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def load_questions(path: Path) -> dict[str, dict[str, Any]]:
    return {q["id"]: q for q in load_json(path)}


def load_summary_rows(run_dir: Path) -> list[dict[str, Any]]:
    path = run_dir / "summary" / "summary.json"
    if not path.exists():
        return []
    return list(load_json(path).get("rows", []))


def load_experiments(run_dir: Path) -> list[dict[str, Any]]:
    summary_by_experiment = {row.get("experiment"): row for row in load_summary_rows(run_dir)}
    experiments: list[dict[str, Any]] = []
    for detail_path in sorted((run_dir / "worker_outputs").glob("*/details.json")):
        worker_name = detail_path.parent.name
        payload = load_json(detail_path)
        for experiment, data in payload.items():
            summary = summary_by_experiment.get(experiment, {})
            experiments.append(
                {
                    "suite": summary.get("suite") or worker_name,
                    "experiment": experiment,
                    "worker_name": worker_name,
                    "edd_score": data.get("edd_score", summary.get("edd_score")),
                    "params": data.get("params", {}),
                    "metrics": data.get("metrics", {}),
                    "details": data.get("details", []),
                }
            )
    return experiments


def judge_value(case: dict[str, Any], key: str) -> float | None:
    judge = case.get("judge") or {}
    raw = judge.get(key)
    if raw is None or raw == "":
        return None
    return number(raw)


def automatic_flags(case: dict[str, Any], edd_score: Any) -> list[str]:
    flags: list[str] = []
    answer = normalize_text(case.get("answer"))
    groundedness = judge_value(case, "groundedness")
    relevance = judge_value(case, "relevance")
    coverage = case.get("coverage")
    edd = number(edd_score)

    if not answer:
        flags.append("empty_answer")
    if coverage is not None and number(coverage) < 1:
        flags.append("coverage_below_target")
    if case.get("abstention") and not case.get("expect_abstention"):
        flags.append("false_abstention")
    if case.get("expect_abstention") and not case.get("abstention"):
        flags.append("missed_abstention")
    if groundedness is None or relevance is None:
        flags.append("missing_numeric_judge")
    if groundedness is not None and groundedness < 4:
        flags.append("low_groundedness")
    if relevance is not None and relevance < 4:
        flags.append("low_relevance")
    if edd >= 90 and len(answer) > 3500:
        flags.append("high_score_long_answer")
    return flags


def priority(case: dict[str, Any], experiment: dict[str, Any], top_experiment_names: set[str]) -> float:
    flags = set(automatic_flags(case, experiment.get("edd_score")))
    qid = case.get("id", "")
    score = number(experiment.get("edd_score"))
    if experiment["experiment"] in top_experiment_names:
        score += 20
    if qid in {"q2_followup", "q5_followup", "q7_compare", "q8_compare_precise", "q10_abstention"}:
        score += 25
    if flags:
        score += 35
    if {"empty_answer", "false_abstention", "missed_abstention", "coverage_below_target"} & flags:
        score += 60
    if "high_score_long_answer" in flags or "missing_numeric_judge" in flags:
        score += 15
    return score


def build_pack(run_dir: Path, questions_path: Path, max_cases: int) -> dict[str, Any]:
    questions = load_questions(questions_path)
    experiments = load_experiments(run_dir)
    top_experiment_names = {
        item["experiment"]
        for item in sorted(experiments, key=lambda exp: number(exp.get("edd_score")), reverse=True)[:3]
    }

    candidates: list[dict[str, Any]] = []
    for experiment in experiments:
        for case in experiment.get("details", []):
            q = questions.get(case.get("id"), {})
            flags = automatic_flags(case, experiment.get("edd_score"))
            candidates.append(
                {
                    "priority": priority(case, experiment, top_experiment_names),
                    "case_id": f"{experiment['experiment']}::{case.get('id')}",
                    "suite": experiment["suite"],
                    "experiment": experiment["experiment"],
                    "edd_score": experiment.get("edd_score"),
                    "params": experiment.get("params", {}),
                    "experiment_metrics": experiment.get("metrics", {}),
                    "question_id": case.get("id"),
                    "question_type": q.get("type", case.get("type")),
                    "turns": q.get("turns", []),
                    "target_orgs": q.get("target_orgs", []),
                    "target_biz": q.get("target_biz", ""),
                    "expect_abstention": bool(q.get("expect_abstention", case.get("expect_abstention", False))),
                    "retrieved_orgs": case.get("retrieved_orgs", []),
                    "answer": normalize_text(case.get("answer")),
                    "metrics_snapshot": {
                        "coverage": case.get("coverage"),
                        "first_hit_rank": case.get("first_hit_rank"),
                        "abstention": case.get("abstention"),
                        "latency_sec": case.get("latency_sec"),
                        "judge": case.get("judge", {}),
                    },
                    "automatic_flags": flags,
                    "audit_questions": [
                        "Does the answer actually answer the user's question in context, not merely mention related evidence?",
                        "Are all concrete claims grounded in the retrieved evidence?",
                        "Is this a case where EDD is high but the answer is verbose, evasive, or not convincing?",
                        "Should this sample be marked pass, pass_with_caveat, or fail for report-quality use?",
                    ],
                }
            )

    selected = sorted(candidates, key=lambda item: item["priority"], reverse=True)[:max_cases]
    for item in selected:
        item.pop("priority", None)

    return {
        "schema": SCHEMA,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_run_dir": str(run_dir),
        "questions_path": str(questions_path),
        "judge_role": "High-reasoning external quality auditor. Do not trust EDD alone.",
        "rubric": {
            "contextual_quality": "1-5. Does the answer satisfy the actual question and dialogue context?",
            "evidence_fit": "1-5. Are concrete claims supported by retrieved evidence?",
            "usefulness": "1-5. Is the answer concise, actionable, and report-worthy?",
            "risk_flags": "List hallucination, over-refusal, under-refusal, wrong-document, verbosity, missing-citation, or unclear-source risks.",
            "decision": "pass | pass_with_caveat | fail",
        },
        "expected_output_schema": {
            "case_id": "string",
            "contextual_quality": "integer 1-5",
            "evidence_fit": "integer 1-5",
            "usefulness": "integer 1-5",
            "decision": "pass | pass_with_caveat | fail",
            "risk_flags": ["string"],
            "reason": "short Korean explanation with concrete evidence",
            "recommended_next_action": "keep | revise_prompt | revise_retrieval | add_question | manual_review",
        },
        "cases": selected,
    }


def render_markdown(pack: dict[str, Any], answer_chars: int) -> str:
    lines: list[str] = [
        "# RFP RAG Quality Audit Input",
        "",
        f"- created_at: {pack['created_at']}",
        f"- source_run_dir: `{pack['source_run_dir']}`",
        "",
        "## Judge Instruction",
        "",
        "Use the JSON file as the source of truth. EDD is only a signal. Find cases where the metric looks good but the answer is not convincing.",
        "",
        "## Rubric",
        "",
    ]
    for key, value in pack["rubric"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Cases", ""])

    for case in pack["cases"]:
        question = " / ".join(normalize_text(turn) for turn in case.get("turns", []))
        metrics = case.get("metrics_snapshot", {})
        lines.extend(
            [
                f"### {case['case_id']}",
                "",
                f"- question: {question}",
                f"- EDD: {case.get('edd_score')}",
                f"- metrics: coverage={metrics.get('coverage')}, first_hit_rank={metrics.get('first_hit_rank')}, abstention={metrics.get('abstention')}, latency={metrics.get('latency_sec')}",
                f"- flags: {', '.join(case.get('automatic_flags') or [])}",
                f"- retrieved_orgs: {', '.join(map(str, case.get('retrieved_orgs') or []))}",
                "",
                "Answer excerpt:",
                "",
                "```text",
                normalize_text(case.get("answer"), answer_chars),
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--questions", default=str(PROJECT_ROOT / "eval" / "questions.json"))
    parser.add_argument("--out-dir", default="")
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--md-answer-chars", type=int, default=1000)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    questions_path = Path(args.questions).resolve()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else run_dir / "audits"

    pack = build_pack(run_dir, questions_path, args.max_cases)
    write_json(out_dir / "audit_input.json", pack)
    (out_dir / "audit_input.md").write_text(render_markdown(pack, args.md_answer_chars), encoding="utf-8")
    print(json.dumps({"out_dir": str(out_dir), "cases": len(pack["cases"])}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
