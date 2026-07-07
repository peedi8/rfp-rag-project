from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA = "rfp_rag_report_evidence_pack.v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    # Some generated detail files can contain raw control characters in long answers.
    return json.loads(path.read_text(encoding="utf-8"), strict=False)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_text(value: Any, limit: int | None = None) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if limit is not None and len(text) > limit:
        return text[:limit].rstrip() + "\n...(truncated; full text is in report_evidence.json)"
    return text


def md_escape(value: Any) -> str:
    return normalize_text(value).replace("|", "\\|").replace("\n", "<br>")


def load_questions(path: Path) -> dict[str, dict[str, Any]]:
    questions = load_json(path)
    return {q["id"]: q for q in questions}


def load_summary(run_dir: Path) -> list[dict[str, Any]]:
    summary_json = run_dir / "summary" / "summary.json"
    if not summary_json.exists():
        return []
    data = load_json(summary_json)
    return list(data.get("rows", []))


def load_experiments(run_dir: Path) -> list[dict[str, Any]]:
    summary_by_experiment = {row.get("experiment"): row for row in load_summary(run_dir)}
    experiments: list[dict[str, Any]] = []
    for detail_path in sorted((run_dir / "worker_outputs").glob("*/details.json")):
        worker_name = detail_path.parent.name
        details = load_json(detail_path)
        for experiment, payload in details.items():
            summary_row = summary_by_experiment.get(experiment, {})
            experiments.append(
                {
                    "suite": summary_row.get("suite") or worker_name,
                    "experiment": experiment,
                    "worker_name": worker_name,
                    "detail_path": str(detail_path),
                    "summary": summary_row,
                    "params": payload.get("params", {}),
                    "metrics": payload.get("metrics", {}),
                    "edd_score": payload.get("edd_score", summary_row.get("edd_score")),
                    "issues": payload.get("issues", {}),
                    "details": payload.get("details", []),
                }
            )
    return experiments


def number(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def judge_score(case: dict[str, Any], key: str) -> float | None:
    judge = case.get("judge") or {}
    value = judge.get(key)
    if value is None or value == "":
        return None
    return number(value)


def case_flags(case: dict[str, Any], experiment: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    answer = normalize_text(case.get("answer"))
    coverage = case.get("coverage")
    groundedness = judge_score(case, "groundedness")
    relevance = judge_score(case, "relevance")
    edd = number(experiment.get("edd_score"))

    if not answer:
        flags.append("empty_answer")
    if coverage is not None and number(coverage) < 1:
        flags.append("coverage_below_target")
    if case.get("abstention") and not case.get("expect_abstention"):
        flags.append("false_abstention")
    if case.get("expect_abstention") and not case.get("abstention"):
        flags.append("missed_abstention")
    if groundedness is not None and groundedness < 4:
        flags.append("low_groundedness")
    if relevance is not None and relevance < 4:
        flags.append("low_relevance")
    if groundedness is None or relevance is None:
        flags.append("missing_llm_judge_score")
    if len(answer) > 3500 and edd >= 90:
        flags.append("high_score_long_answer_needs_human_read")
    if edd >= 90 and not flags:
        flags.append("clean_high_score_sample")
    return flags


def interpret_case(case: dict[str, Any], experiment: dict[str, Any]) -> str:
    flags = set(case_flags(case, experiment))
    if "empty_answer" in flags:
        return "Answer generation failed; inspect token budget, retry policy, and model finish_reason."
    if "false_abstention" in flags:
        return "The system refused despite a non-abstention case; inspect abstention prompt and evidence confidence."
    if "missed_abstention" in flags:
        return "The system answered a question expected to abstain; inspect retrieval distractors and no-evidence policy."
    if "coverage_below_target" in flags:
        return "Retrieval did not cover all target organizations; inspect filtering, rewrite, and MMR diversity."
    if "low_groundedness" in flags or "low_relevance" in flags:
        return "LLM judge found a quality issue; inspect answer-evidence alignment, not only retrieval metrics."
    if "high_score_long_answer_needs_human_read" in flags:
        return "Automatic metrics are strong, but the answer is long; human audit should check whether it is concise and context-fit."
    if "missing_llm_judge_score" in flags:
        return "Retrieval metrics are available, but qualitative judge score is missing; include this in the audit queue."
    return "Automatic metrics and judge scores agree; keep as a positive report sample."


def select_experiments(experiments: list[dict[str, Any]], top_n: int) -> list[dict[str, Any]]:
    return sorted(experiments, key=lambda item: number(item.get("edd_score")), reverse=True)[:top_n]


def build_cases(
    run_dir: Path,
    questions_path: Path,
    top_experiments: int,
    answer_chars: int,
) -> dict[str, Any]:
    questions = load_questions(questions_path)
    summary_rows = load_summary(run_dir)
    experiments = load_experiments(run_dir)
    selected = select_experiments(experiments, top_experiments)
    selected_names = {item["experiment"] for item in selected}

    evidence_cases: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    def add_case(experiment: dict[str, Any], case: dict[str, Any], reason: str) -> None:
        key = (experiment["experiment"], case.get("id", ""))
        if key in seen:
            return
        seen.add(key)
        question = questions.get(case.get("id"), {})
        flags = case_flags(case, experiment)
        evidence_cases.append(
            {
                "selection_reason": reason,
                "suite": experiment["suite"],
                "experiment": experiment["experiment"],
                "edd_score": experiment.get("edd_score"),
                "params": experiment.get("params", {}),
                "experiment_metrics": experiment.get("metrics", {}),
                "question_id": case.get("id"),
                "question_type": question.get("type", case.get("type")),
                "turns": question.get("turns", []),
                "target_orgs": question.get("target_orgs", []),
                "target_biz": question.get("target_biz", ""),
                "expect_abstention": bool(question.get("expect_abstention", case.get("expect_abstention", False))),
                "answer": normalize_text(case.get("answer")),
                "answer_excerpt": normalize_text(case.get("answer"), answer_chars),
                "retrieved_orgs": case.get("retrieved_orgs", []),
                "coverage": case.get("coverage"),
                "first_hit_rank": case.get("first_hit_rank"),
                "abstention": case.get("abstention"),
                "latency_sec": case.get("latency_sec"),
                "judge": case.get("judge", {}),
                "flags": flags,
                "interpretation": interpret_case(case, experiment),
            }
        )

    for experiment in selected:
        for case in experiment.get("details", []):
            add_case(experiment, case, "top_experiment_full_question_set")

    for experiment in experiments:
        for case in experiment.get("details", []):
            flags = set(case_flags(case, experiment))
            if flags - {"clean_high_score_sample"}:
                add_case(experiment, case, "issue_or_audit_queue")

    return {
        "schema": SCHEMA,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_run_dir": str(run_dir),
        "questions_path": str(questions_path),
        "summary_rows": summary_rows,
        "selected_experiments": [
            {
                "suite": item["suite"],
                "experiment": item["experiment"],
                "edd_score": item.get("edd_score"),
                "metrics": item.get("metrics", {}),
                "params": item.get("params", {}),
            }
            for item in selected
        ],
        "metric_notes": {
            "edd_score": "Composite score from retrieval coverage, hit-all, MRR, groundedness, relevance, abstention accuracy, latency, and penalties.",
            "human_audit_reason": "High EDD is evidence, not proof. Long answers, missing judge scores, or abstention edge cases still require qualitative reading.",
        },
        "evidence_cases": evidence_cases,
    }


def render_markdown(pack: dict[str, Any]) -> str:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in pack["evidence_cases"]:
        grouped[case["experiment"]].append(case)

    lines: list[str] = [
        "# RFP RAG Report Evidence Pack",
        "",
        f"- created_at: {pack['created_at']}",
        f"- source_run_dir: `{pack['source_run_dir']}`",
        f"- questions_path: `{pack['questions_path']}`",
        "",
        "## Top Experiments",
        "",
        "| rank | suite | experiment | EDD | coverage | MRR | groundedness | relevance | false abstain | empty | latency |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(pack["summary_rows"][:10], start=1):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    md_escape(row.get("suite")),
                    md_escape(row.get("experiment")),
                    md_escape(row.get("edd_score")),
                    md_escape(row.get("retrieval_coverage_avg")),
                    md_escape(row.get("mrr")),
                    md_escape(row.get("groundedness_avg")),
                    md_escape(row.get("relevance_avg")),
                    md_escape(row.get("false_abstention_rate")),
                    md_escape(row.get("empty_answer_rate")),
                    md_escape(row.get("latency_avg_sec")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Reading Rule",
            "",
            "- A high EDD score is not accepted as final proof by itself.",
            "- Each sample keeps the question, answer excerpt, retrieval trace, automatic metrics, flags, and interpretation together.",
            "- Full answers are stored in `report_evidence.json`; this Markdown file keeps excerpts readable.",
            "",
            "## Evidence Cases",
            "",
        ]
    )

    for experiment, cases in grouped.items():
        lines.extend([f"### {experiment}", ""])
        for case in cases:
            turns = case.get("turns") or []
            question_text = " / ".join(normalize_text(turn) for turn in turns)
            judge = case.get("judge") or {}
            lines.extend(
                [
                    f"#### {case.get('question_id')} - {case.get('selection_reason')}",
                    "",
                    f"- question: {question_text}",
                    f"- EDD: {case.get('edd_score')}; coverage: {case.get('coverage')}; first_hit_rank: {case.get('first_hit_rank')}; abstention: {case.get('abstention')}; expected_abstention: {case.get('expect_abstention')}",
                    f"- judge: groundedness={judge.get('groundedness')}, relevance={judge.get('relevance')}",
                    f"- retrieved_orgs: {', '.join(map(str, case.get('retrieved_orgs') or []))}",
                    f"- flags: {', '.join(case.get('flags') or [])}",
                    f"- interpretation: {case.get('interpretation')}",
                    "",
                    "Answer excerpt:",
                    "",
                    "```text",
                    normalize_text(case.get("answer_excerpt")),
                    "```",
                    "",
                ]
            )
            reason = normalize_text(judge.get("reason"), 800)
            if reason:
                lines.extend(["Judge reason excerpt:", "", "```text", reason, "```", ""])

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--questions", default=str(PROJECT_ROOT / "eval" / "questions.json"))
    parser.add_argument("--out-dir", default="")
    parser.add_argument("--top-experiments", type=int, default=3)
    parser.add_argument("--md-answer-chars", type=int, default=1400)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    questions_path = Path(args.questions).resolve()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else run_dir / "report_evidence"

    pack = build_cases(run_dir, questions_path, args.top_experiments, args.md_answer_chars)
    write_json(out_dir / "report_evidence.json", pack)
    (out_dir / "report_evidence.md").write_text(render_markdown(pack), encoding="utf-8")
    print(json.dumps({"out_dir": str(out_dir), "cases": len(pack["evidence_cases"])}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
