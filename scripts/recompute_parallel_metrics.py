"""Recompute worker metrics from saved details without re-calling APIs."""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.edd_score import add_edd_columns
from scripts.evaluate import aggregate, answer_quality_diagnostics, is_abstention
from scripts.run_experiment_worker import METRIC_COLS


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
    return {
        "coverage_fail": coverage_fail,
        "false_abstain": false_abstain,
        "empty_answer": empty_answer,
        "judge_low": judge_low,
        "answer_quality_issues": answer_quality_issues,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()
    run_dir = Path(args.run_dir)
    worker_dirs = sorted(p for p in (run_dir / "worker_outputs").iterdir() if p.is_dir())
    for worker_dir in worker_dirs:
        detail_path = worker_dir / "details.json"
        if not detail_path.exists():
            continue
        data = json.loads(detail_path.read_text(encoding="utf-8"))
        csv_path = worker_dir / "results.csv"
        suite = worker_dir.name
        if csv_path.exists():
            with csv_path.open(encoding="utf-8-sig", newline="") as f:
                old_rows = list(csv.DictReader(f))
            if old_rows and old_rows[0].get("suite"):
                suite = old_rows[0]["suite"]
        rows = []
        for exp_name, exp in data.items():
            for detail in exp.get("details", []):
                detail["abstention"] = is_abstention(detail.get("answer", ""))
                quality = answer_quality_diagnostics(detail, detail.get("answer", ""), detail["abstention"])
                detail["answer_quality_issues"] = quality["issues"]
                detail["answer_quality_diagnostics"] = quality
            metrics = aggregate(exp.get("details", []))
            exp["metrics"] = metrics
            exp["issues"] = _issue_summary(exp.get("details", []))
            row = add_edd_columns({"suite": suite, "experiment": exp_name, **metrics})
            exp["edd_score"] = row["edd_score"]
            rows.append(row)
        _write_json(detail_path, data)
        fieldnames = METRIC_COLS + [
            "edd_retrieval_coverage_avg",
            "edd_hit_all_targets_rate",
            "edd_mrr",
            "edd_groundedness_avg",
            "edd_relevance_avg",
            "edd_abstention_accuracy",
            "edd_latency_score",
        ]
        with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        best = max(rows, key=lambda r: float(r.get("edd_score") or 0), default=None)
        for contract_path in [worker_dir / "worker_output.json", run_dir / "worker_outputs" / f"{worker_dir.name}.json"]:
            if not contract_path.exists():
                continue
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            if best:
                contract["summary"] = f"{suite} recomputed; best={best['experiment']} EDD={best['edd_score']}"
                contract.setdefault("proposal", {})["accepted_fields_or_changes"] = [best]
            observed = contract.setdefault("validation", {}).setdefault("observed_results", [])
            observed.append("metrics_recomputed_from_saved_details")
            _write_json(contract_path, contract)
        print(f"recomputed {worker_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
