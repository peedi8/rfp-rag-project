"""Run one bounded parallel experiment suite into a worker output folder.

This script never edits final logs or project settings. It only writes under
the provided run directory so the main Codex orchestrator can review/merge.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.edd_score import add_edd_columns
from scripts.evaluate import run_eval

ROOT = Path(__file__).resolve().parents[1]


CONTROL = {
    "use_mmr": True,
    "top_k": 8,
    "mmr_lambda": 0.5,
    "fetch_k": 20,
    "auto_filter": True,
    "rewrite_query": True,
}


SUITES: dict[str, list[tuple[str, dict]]] = {
    "baseline_default": [
        ("baseline_default", {**CONTROL}),
    ],
    "prompt_sweep": [
        ("prompt_default", {**CONTROL, "prompt_variant": "default"}),
        ("prompt_strict_evidence", {**CONTROL, "prompt_variant": "strict_evidence"}),
        ("prompt_concise_verified", {**CONTROL, "prompt_variant": "concise_verified"}),
        ("prompt_report_ready", {**CONTROL, "prompt_variant": "report_ready"}),
    ],
    "prompt_report_ready_only": [
        ("prompt_report_ready", {**CONTROL, "prompt_variant": "report_ready"}),
    ],
    "prompt_concise_verified_only": [
        ("prompt_concise_verified", {**CONTROL, "prompt_variant": "concise_verified"}),
    ],
    "topk_sweep": [
        ("topk5_filter_rewrite", {**CONTROL, "top_k": 5}),
        ("topk8_filter_rewrite_control", {**CONTROL, "top_k": 8}),
        ("topk12_filter_rewrite", {**CONTROL, "top_k": 12}),
    ],
    "topk5_only": [
        ("topk5_filter_rewrite", {**CONTROL, "top_k": 5}),
    ],
    "topk8_only": [
        ("topk8_filter_rewrite_control", {**CONTROL, "top_k": 8}),
    ],
    "topk12_only": [
        ("topk12_filter_rewrite", {**CONTROL, "top_k": 12}),
    ],
    "mmr_lambda_sweep": [
        ("lambda03_top8_filter_rewrite", {**CONTROL, "mmr_lambda": 0.3}),
        ("lambda05_top8_filter_rewrite_control", {**CONTROL, "mmr_lambda": 0.5}),
        ("lambda07_top8_filter_rewrite", {**CONTROL, "mmr_lambda": 0.7}),
    ],
    "fetchk_sweep": [
        ("fetch20_top8_filter_rewrite_control", {**CONTROL, "fetch_k": 20}),
        ("fetch40_top8_filter_rewrite", {**CONTROL, "fetch_k": 40}),
    ],
    "filter_rewrite_ablation": [
        ("filter_off_rewrite_off", {**CONTROL, "auto_filter": False, "rewrite_query": False}),
        ("filter_on_rewrite_off", {**CONTROL, "auto_filter": True, "rewrite_query": False}),
        ("filter_off_rewrite_on", {**CONTROL, "auto_filter": False, "rewrite_query": True}),
        ("filter_on_rewrite_on_control", {**CONTROL, "auto_filter": True, "rewrite_query": True}),
    ],
}


METRIC_COLS = [
    "suite",
    "experiment",
    "run_mode",
    "edd_score",
    "retrieval_coverage_avg",
    "hit_all_targets_rate",
    "mrr",
    "groundedness_avg",
    "relevance_avg",
    "abstention_accuracy",
    "false_abstention_rate",
    "empty_answer_rate",
    "latency_avg_sec",
]


PROTECTED_DEFAULTS = [
    "업무일지.md",
    "eval/experiment_log.md",
    "CLAUDE.md",
    "config.py",
    "src/**",
    "chroma_db/**",
]


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def _issue_summary(details: list[dict]) -> dict:
    coverage_fail = [
        d["id"] for d in details
        if d.get("coverage") is not None and d.get("coverage") < 1.0
    ]
    false_abstain = [
        d["id"] for d in details
        if not d.get("expect_abstention") and d.get("abstention")
    ]
    empty_answer = [
        d["id"] for d in details
        if not (d.get("answer") or "").strip()
    ]
    judge_low = []
    for d in details:
        judge = d.get("judge") or {}
        g = judge.get("groundedness")
        r = judge.get("relevance")
        if g is not None and r is not None and (g <= 1 or r <= 1):
            judge_low.append(d["id"])
    answer_quality_issues = {}
    for d in details:
        for issue in d.get("answer_quality_issues") or []:
            answer_quality_issues.setdefault(issue, []).append(d["id"])
    field_score_issues = {}
    for d in details:
        field_score = d.get("field_score") or {}
        for issue, count in (field_score.get("issue_counts") or {}).items():
            if count:
                field_score_issues.setdefault(issue, []).append(d["id"])
    return {
        "coverage_fail": coverage_fail,
        "false_abstain": false_abstain,
        "empty_answer": empty_answer,
        "judge_low": judge_low,
        "answer_quality_issues": answer_quality_issues,
        "field_score_issues": field_score_issues,
    }


def _collect_cost_rows(details_all: dict) -> list[dict]:
    rows = []
    for experiment, payload in details_all.items():
        for detail in payload.get("details", []):
            case_id = detail.get("id", "")
            for call in detail.get("retrieval_usage_trace") or []:
                rows.append({"experiment": experiment, "case_id": case_id, **call})
            for call in detail.get("generation_usage_trace") or []:
                rows.append({"experiment": experiment, "case_id": case_id, **call})
            judge = detail.get("judge") or {}
            for call in judge.get("usage_trace") or []:
                rows.append({"experiment": experiment, "case_id": case_id, **call})
    return rows


def _cost_summary(cost_rows: list[dict]) -> dict:
    observed = [r.get("cost_usd") for r in cost_rows if r.get("cost_usd") is not None]
    return {
        "schema": "rfp_rag_cost_summary.v1",
        "calls_recorded": len(cost_rows),
        "calls_with_observed_cost": len(observed),
        "observed_cost_usd": round(sum(float(v) for v in observed), 6) if observed else 0.0,
        "cost_basis": "local_price_table",
        "missing_cost_rows": [
            {
                "experiment": r.get("experiment"),
                "case_id": r.get("case_id"),
                "operation": r.get("operation"),
                "model": r.get("model"),
            }
            for r in cost_rows
            if r.get("cost_usd") is None
        ],
    }


def _effective_case_count(questions_path: str, case_limit: int | None) -> int:
    with open(questions_path, encoding="utf-8") as f:
        cases = json.load(f)
    count = len(cases)
    if case_limit is not None:
        count = min(count, case_limit)
    return count


def _hard_stop(args: argparse.Namespace) -> float | None:
    return args.hard_stop_usd if args.hard_stop_usd is not None else args.budget_cap_usd


def _estimate_experiment_cost(args: argparse.Namespace, case_count: int) -> float:
    if case_count <= 0:
        return 0.0
    return round(case_count * max(0.0, args.preflight_case_estimate_usd), 6)


def _remaining_usd(hard_stop_usd: float | None, spent_usd: float) -> float | None:
    if hard_stop_usd is None:
        return None
    return round(hard_stop_usd - spent_usd, 6)


def run_suite(args: argparse.Namespace) -> int:
    from src.vectorstore import load_index

    if args.suite not in SUITES:
        raise SystemExit(f"Unknown suite: {args.suite}. Choices: {', '.join(SUITES)}")

    worker_dir = Path(args.run_dir) / "worker_outputs" / f"{args.worker_id}_{args.suite}"
    worker_root_contract = Path(args.run_dir) / "worker_outputs" / f"{args.worker_id}_{args.suite}.json"
    worker_dir.mkdir(parents=True, exist_ok=True)
    results_csv = worker_dir / "results.csv"
    detail_json = worker_dir / "details.json"
    cost_summary_json = worker_dir / "cost_summary.json"
    budget_ledger_jsonl = worker_dir / "budget_ledger.jsonl"
    contract_json = worker_dir / "worker_output.json"
    budget_ledger_jsonl.write_text("", encoding="utf-8")

    command = " ".join(sys.argv)
    validation = {"commands_run": [command], "observed_results": []}
    rows = []
    details_all = {}
    budget_events = []
    case_count = 0
    hard_stop_usd = _hard_stop(args)
    spent_observed = max(0.0, args.starting_spent_usd)
    status = "proposal"
    blocking_reason = ""

    try:
        index_count = load_index().count()
        validation["observed_results"].append(f"index_count={index_count}")
        if index_count == 0:
            raise RuntimeError("Chroma index is empty; run build_index raw first.")
        case_count = _effective_case_count(args.questions, args.case_limit)
        validation["observed_results"].append(f"effective_case_count={case_count}")
        if hard_stop_usd is not None:
            validation["observed_results"].append(
                f"budget_gate hard_stop_usd={hard_stop_usd} starting_spent_usd={spent_observed}"
            )

        experiments = SUITES[args.suite]
        if args.max_experiments:
            experiments = experiments[:args.max_experiments]

        for name, params in experiments:
            estimated_cost = _estimate_experiment_cost(args, case_count)
            spend_before = spent_observed
            if (
                not args.dry_run
                and hard_stop_usd is not None
                and spend_before + estimated_cost > hard_stop_usd
            ):
                event = {
                    "record_type": "budget_gate_event",
                    "event_type": "budget_gate",
                    "event": "skipped_preflight_budget",
                    "status": "skipped_budget",
                    "run_id": Path(args.run_dir).name,
                    "worker_id": args.worker_id,
                    "suite": args.suite,
                    "experiment": name,
                    "question_file": args.questions,
                    "dry_run": args.dry_run,
                    "no_judge": args.no_judge,
                    "budget_gate_enabled": True,
                    "case_count": case_count,
                    "estimated_cost_usd": estimated_cost,
                    "spent_before_usd": round(spend_before, 6),
                    "spent_after_usd": round(spend_before, 6),
                    "remaining_usd": _remaining_usd(hard_stop_usd, spend_before),
                    "hard_stop_usd": hard_stop_usd,
                    "skip_reason": "projected_experiment_cost_would_exceed_hard_stop",
                    "reason": "projected experiment cost would exceed hard stop",
                    "cost_basis": "local_price_table",
                    "usage_missing": False,
                    "unknown_price_model": False,
                    "created_at": datetime.now().isoformat(timespec="seconds"),
                }
                budget_events.append(event)
                _append_jsonl(budget_ledger_jsonl, event)
                validation["observed_results"].append(
                    f"skipped_budget {name} estimated={estimated_cost} spent_before={round(spend_before, 6)}"
                )
                continue

            print(f"\n=== {args.suite}:{name} {params} ===", flush=True)
            if args.dry_run:
                metrics = {
                    "retrieval_coverage_avg": 1.0,
                    "hit_all_targets_rate": 1.0,
                    "mrr": 1.0,
                    "groundedness_avg": 4.0,
                    "relevance_avg": 4.0,
                    "abstention_accuracy": 1.0,
                    "latency_avg_sec": 10.0,
                }
                details = []
            else:
                out = run_eval(
                    params=params,
                    use_judge=not args.no_judge,
                    verbose=True,
                    case_limit=args.case_limit,
                    questions_path=args.questions,
                )
                metrics = out["metrics"]
                details = out["details"]
            row = add_edd_columns({
                "suite": args.suite,
                "experiment": name,
                "run_mode": "dry_run" if args.dry_run else "scored",
                **metrics,
            })
            rows.append(row)
            details_all[name] = {
                "params": params,
                "metrics": metrics,
                "edd_score": row["edd_score"],
                "issues": _issue_summary(details),
                "details": details,
            }
            exp_cost_rows = _collect_cost_rows({name: details_all[name]})
            actual_cost = _cost_summary(exp_cost_rows)["observed_cost_usd"]
            spent_observed += actual_cost
            for cost_row in exp_cost_rows:
                ledger_row = {
                    "record_type": "model_call",
                    "run_id": Path(args.run_dir).name,
                    "worker_id": args.worker_id,
                    "suite": args.suite,
                    "question_file": args.questions,
                    "dry_run": args.dry_run,
                    "no_judge": args.no_judge,
                    "cost_basis": "local_price_table",
                    "usage_missing": cost_row.get("cost_usd") is None,
                    "unknown_price_model": False,
                    **cost_row,
                }
                _append_jsonl(budget_ledger_jsonl, ledger_row)
            event = {
                "record_type": "budget_gate_event",
                "event_type": "budget_gate",
                "event": "experiment_reconciled",
                "status": "ok",
                "run_id": Path(args.run_dir).name,
                "worker_id": args.worker_id,
                "suite": args.suite,
                "experiment": name,
                "question_file": args.questions,
                "dry_run": args.dry_run,
                "no_judge": args.no_judge,
                "budget_gate_enabled": hard_stop_usd is not None,
                "case_count": case_count,
                "estimated_cost_usd": estimated_cost,
                "observed_cost_usd": actual_cost,
                "spent_before_usd": round(spend_before, 6),
                "spent_after_usd": round(spent_observed, 6),
                "remaining_usd": _remaining_usd(hard_stop_usd, spent_observed),
                "hard_stop_usd": hard_stop_usd,
                "skip_reason": "",
                "cost_basis": "local_price_table",
                "usage_missing": any(r.get("cost_usd") is None for r in exp_cost_rows),
                "unknown_price_model": False,
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
            budget_events.append(event)
            _append_jsonl(budget_ledger_jsonl, event)
            if not args.dry_run and hard_stop_usd is not None and spent_observed >= hard_stop_usd:
                validation["observed_results"].append(
                    f"hard_stop_reached after {name} spent_observed={round(spent_observed, 6)}"
                )
                break

        fieldnames = METRIC_COLS + [
            "edd_retrieval_coverage_avg",
            "edd_hit_all_targets_rate",
            "edd_mrr",
            "edd_groundedness_avg",
            "edd_relevance_avg",
            "edd_abstention_accuracy",
            "edd_latency_score",
        ]
        with results_csv.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        _write_json(detail_json, details_all)
        cost_rows = _collect_cost_rows(details_all)
        cost_summary = _cost_summary(cost_rows)
        cost_summary["budget"] = {
            "budget_cap_usd": args.budget_cap_usd,
            "hard_stop_usd": hard_stop_usd,
            "starting_spent_usd": args.starting_spent_usd,
            "spent_observed_usd": round(spent_observed, 6),
            "preflight_case_estimate_usd": args.preflight_case_estimate_usd,
            "effective_case_count": case_count,
            "events": budget_events,
        }
        _write_json(cost_summary_json, cost_summary)
        validation["observed_results"].append(f"wrote_rows={len(rows)}")
        validation["observed_results"].append(f"budget_events={len(budget_events)}")
        if not rows and budget_events and all(
            event.get("event") == "skipped_preflight_budget" for event in budget_events
        ):
            status = "blocked"
            blocking_reason = "budget_gate_all_skipped"
            validation["observed_results"].append("budget_gate_all_skipped=true")

    except Exception as exc:
        status = "failed"
        blocking_reason = f"{type(exc).__name__}: {exc}"
        validation["observed_results"].append(traceback.format_exc())
        print(traceback.format_exc(), file=sys.stderr)

    best = max(rows, key=lambda r: float(r.get("edd_score") or 0), default=None)
    budget_gate_all_skipped = blocking_reason == "budget_gate_all_skipped"
    budget_summary = {
        "budget_cap_usd": args.budget_cap_usd,
        "hard_stop_usd": hard_stop_usd,
        "starting_spent_usd": args.starting_spent_usd,
        "spent_observed_usd": round(spent_observed, 6),
        "preflight_case_estimate_usd": args.preflight_case_estimate_usd,
        "effective_case_count": case_count,
        "events": len(budget_events),
        "skipped_preflight_budget": len([
            e for e in budget_events if e.get("event") == "skipped_preflight_budget"
        ]),
        "budget_gate_all_skipped": budget_gate_all_skipped,
    }
    if best:
        summary = f"{args.suite} completed; best={best['experiment']} EDD={best['edd_score']}"
    elif budget_gate_all_skipped:
        summary = f"{args.suite} skipped before launch by budget gate"
    else:
        summary = f"{args.suite} produced no successful rows"
    contract = {
        "schema": "parallel_team_worker_output.v1",
        "worker_id": args.worker_id,
        "task_id": args.suite,
        "status": status,
        "summary": summary,
        "inputs": [
            str(Path(args.questions).resolve()),
            str(ROOT / "chroma_db"),
            str(ROOT / "scripts" / "evaluate.py"),
        ],
        "models": {
            "answer_model": os.getenv("CHAT_MODEL", ""),
            "judge_model": os.getenv("JUDGE_MODEL", os.getenv("CHAT_MODEL", "")) if not args.no_judge else None,
        },
        "budget_summary": budget_summary,
        "protected_paths_seen": PROTECTED_DEFAULTS,
        "directly_modified_protected_paths": [],
        "outputs": [
            {"path": str(results_csv), "kind": "data", "description": "worker metrics with EDD score"},
            {"path": str(detail_json), "kind": "json", "description": "question-level details and issue keys"},
            {"path": str(cost_summary_json), "kind": "json", "description": "observed model usage and cost summary"},
            {"path": str(budget_ledger_jsonl), "kind": "data", "description": "append-style per-call usage/cost ledger for this worker run"},
            {"path": str(contract_json), "kind": "json", "description": "worker output contract"},
        ],
        "proposal": {
            "accepted_fields_or_changes": [best] if best else [],
            "rejected_or_risky_items": [],
            "needs_orchestrator_review": [
                "Compare EDD score with raw metrics before adopting any parameter.",
                "Do not adopt a row if empty_answer or false_abstain issue keys dominate.",
            ],
        },
        "merge_risk": "low",
        "blocking_reason": blocking_reason,
        "validation": validation,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    _write_json(contract_json, contract)
    _write_json(worker_root_contract, contract)
    print(json.dumps(contract, ensure_ascii=False, indent=2))
    return 0 if status in {"proposal", "blocked"} else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--suite", required=True, choices=sorted(SUITES))
    ap.add_argument("--worker-id", default="")
    ap.add_argument("--case-limit", type=int, default=None)
    ap.add_argument("--max-experiments", type=int, default=None)
    ap.add_argument("--questions", default=str(ROOT / "eval" / "questions.json"))
    ap.add_argument("--no-judge", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--budget-cap-usd", type=float, default=None)
    ap.add_argument("--hard-stop-usd", type=float, default=None)
    ap.add_argument("--starting-spent-usd", type=float, default=0.0)
    ap.add_argument("--preflight-case-estimate-usd", type=float, default=0.02)
    args = ap.parse_args()
    if not args.worker_id:
        args.worker_id = args.suite
    return run_suite(args)


if __name__ == "__main__":
    raise SystemExit(main())
