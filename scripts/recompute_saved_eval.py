"""Recompute metrics from a saved details.json after evaluator changes.

This is for measurement correction only. It does not rerun retrieval or answer
generation, so the resulting score must not be labeled as a new validation run.
"""
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


METRIC_COLS = [
    "suite",
    "experiment",
    "score_label",
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


def _load_details(path: Path, experiment: str) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if experiment in data:
        return data[experiment]["details"]
    if len(data) == 1:
        return next(iter(data.values()))["details"]
    raise SystemExit(f"Experiment '{experiment}' not found in {path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--details", required=True)
    ap.add_argument("--experiment", default="baseline_default")
    ap.add_argument("--suite", default="baseline_default")
    ap.add_argument("--score-label", default="measurement_correction")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    detail_path = Path(args.details)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    details = _load_details(detail_path, args.experiment)
    changes = []
    recomputed = []
    answer_quality_issue_cases = {}
    for rec in details:
        updated = dict(rec)
        old = bool(updated.get("abstention"))
        new = is_abstention(updated.get("answer") or "")
        updated["abstention"] = new
        quality = answer_quality_diagnostics(updated, updated.get("answer") or "", new)
        updated["answer_quality_issues"] = quality["issues"]
        updated["answer_quality_diagnostics"] = quality
        for issue in quality["issues"]:
            answer_quality_issue_cases.setdefault(issue, []).append(updated.get("id"))
        recomputed.append(updated)
        if old != new:
            changes.append(
                {
                    "id": updated.get("id"),
                    "old_abstention": old,
                    "new_abstention": new,
                    "expect_abstention": updated.get("expect_abstention"),
                }
            )

    metrics = aggregate(recomputed)
    row = add_edd_columns(
        {
            "suite": args.suite,
            "experiment": args.experiment,
            "score_label": args.score_label,
            **metrics,
        }
    )

    json_out = {
        "source_details": str(detail_path),
        "score_label": args.score_label,
        "metrics": metrics,
        "edd_row": row,
        "changed_abstention_cases": changes,
        "answer_quality_issue_cases": answer_quality_issue_cases,
    }
    (out_dir / "recomputed_metrics.json").write_text(
        json.dumps(json_out, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with (out_dir / "recomputed_metrics.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=METRIC_COLS, extrasaction="ignore")
        writer.writeheader()
        writer.writerow(row)

    lines = [
        "# Recomputed Saved Eval",
        "",
        f"- source: `{detail_path}`",
        f"- score_label: `{args.score_label}`",
        f"- EDD: **{row['edd_score']}**",
        f"- coverage: **{metrics.get('retrieval_coverage_avg')}**",
        f"- groundedness/relevance: **{metrics.get('groundedness_avg')} / {metrics.get('relevance_avg')}**",
        f"- abstention_accuracy: **{metrics.get('abstention_accuracy')}**",
        f"- latency_avg_sec: **{metrics.get('latency_avg_sec')}**",
        "",
        "## Abstention Changes",
        "",
    ]
    if changes:
        lines.extend(["| id | old | new | expected |", "|---|---:|---:|---:|"])
        for item in changes:
            lines.append(
                f"| {item['id']} | {item['old_abstention']} | {item['new_abstention']} | {item['expect_abstention']} |"
            )
    else:
        lines.append("- None")
    lines.extend(["", "## Answer Quality Issues", ""])
    if answer_quality_issue_cases:
        for issue, ids in sorted(answer_quality_issue_cases.items()):
            lines.append(f"- `{issue}`: {', '.join(str(i) for i in ids)}")
    else:
        lines.append("- None")
    (out_dir / "recomputed_metrics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"edd_score": row["edd_score"], "changes": changes}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
