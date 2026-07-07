"""Headless red/overfit gate for RFP-RAG loop points.

This script does not run RAG, judge answers, or mutate final logs. It reads
existing loop artifacts and writes a gate report that separates:

- scored evidence
- measurement corrections
- diagnostics/no-judge probes
- candidate-only changes
- overfit or validation-contamination risks
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


NUMERIC_FIELDS = {
    "edd",
    "coverage",
    "hit_all",
    "mrr",
    "groundedness",
    "relevance",
    "abstention",
    "latency_sec",
}


def _read_json(path: Path | None) -> dict[str, Any]:
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _num(value: Any) -> float | None:
    if value in (None, "", "NA", "N/A"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _load_loop_points(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            converted = dict(row)
            for key in NUMERIC_FIELDS:
                converted[key] = _num(converted.get(key))
            rows.append(converted)
    return rows


def _contains(row: dict[str, Any], *needles: str) -> bool:
    haystack = " ".join(str(row.get(k, "")) for k in ("label", "score_type", "decision", "main_reason")).lower()
    return any(n.lower() in haystack for n in needles)


def _contains_identity(row: dict[str, Any], *needles: str) -> bool:
    haystack = " ".join(str(row.get(k, "")) for k in ("label", "score_type", "decision")).lower()
    return any(n.lower() in haystack for n in needles)


def classify_row(row: dict[str, Any]) -> dict[str, Any]:
    score_type = str(row.get("score_type") or "")
    decision = str(row.get("decision") or "").lower()
    edd = row.get("edd")
    flags: list[str] = []

    if edd is None:
        state = "diagnostic_only"
    else:
        state = "scored_evidence"

    if "first_validation" in score_type:
        state = "first_validation_evidence"
    if _contains_identity(row, "measurement", "same_answers", "recomputed"):
        state = "measurement_correction"
        flags.append("not_model_improvement")
    if _contains_identity(row, "targeted", "same-holdout", "same_holdout"):
        flags.append("targeted_or_reused_case")
    if _contains_identity(row, "no_judge", "no-judge"):
        state = "diagnostic_only"
        flags.append("no_judge_not_performance")
    if _contains_identity(row, "local", "diagnostic", "guard", "preparation"):
        state = "diagnostic_only"
    if _contains_identity(row, "qualitative", "review"):
        state = "qualitative_evidence"
    if _contains_identity(row, "candidate", "future_scored", "future scored", "draft"):
        state = "candidate_only"
        flags.append("needs_scored_validation")
    if _contains_identity(row, "gate", "registry", "runner"):
        state = "diagnostic_only"
        flags = [flag for flag in flags if flag != "needs_scored_validation"]

    if edd is not None and edd >= 95:
        flags.append("near_ceiling_score")
    if row.get("coverage") == 1 and row.get("mrr") == 1 and row.get("groundedness") == 5 and row.get("relevance") == 5:
        flags.append("metric_saturation_risk")
    if row.get("latency_sec") is not None and row["latency_sec"] >= 20:
        flags.append("latency_risk")
    if any(marker in decision for marker in ("reject", "partial_fail", "do_not_open", "hold")):
        flags.append("rejected_by_decision")

    promotion_allowed = state in {"first_validation_evidence", "scored_evidence"} and not {
        "targeted_or_reused_case",
        "no_judge_not_performance",
        "needs_scored_validation",
        "rejected_by_decision",
    }.intersection(flags)
    if state == "measurement_correction":
        promotion_allowed = False

    return {
        "loop_point": row.get("loop_point"),
        "label": row.get("label"),
        "state": state,
        "edd": edd,
        "promotion_allowed": promotion_allowed,
        "flags": flags,
        "decision": row.get("decision"),
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    rows = _load_loop_points(args.loop_points)
    classifications = [classify_row(row) for row in rows]
    quality = _read_json(args.quality_matrix)
    exposure = _read_json(args.exposure_registry)

    promotable = [c for c in classifications if c["promotion_allowed"] and c["edd"] is not None]
    corrected = [c for c in classifications if c["state"] == "measurement_correction" and c["edd"] is not None]
    candidate_only = [c for c in classifications if c["state"] == "candidate_only"]
    diagnostic = [c for c in classifications if c["state"] in {"diagnostic_only", "qualitative_evidence"}]

    human_quality_avg = None
    evidence_safety_avg = None
    if quality:
        aggregate = quality.get("aggregate") or {}
        human_quality_avg = aggregate.get("human_quality_avg")
        evidence_safety_avg = aggregate.get("evidence_safety_score_avg")

    red_flags = sorted({flag for c in classifications for flag in c["flags"]})
    if human_quality_avg is not None and human_quality_avg < 4:
        red_flags.append("human_quality_gap")
    if evidence_safety_avg is not None and evidence_safety_avg < 4:
        red_flags.append("evidence_safety_gap")

    has_strict_calibration_pass = any(
        row.get("label") == "blind_judge_calibration_strict_pack"
        and "open" in str(row.get("decision") or "").lower()
        for row in rows
    )
    has_v4_first_score = any(row.get("label") == "v4_first_baseline_top8" for row in rows)
    has_report_ready_score = any(row.get("label") == "v4_report_ready_prompt" for row in rows)

    recommendations = []
    if not has_strict_calibration_pass:
        recommendations.append({
            "priority": len(recommendations) + 1,
            "action": "Run blind judge calibration before trusting another near-ceiling judge score.",
            "reason": "Existing loop points include near-ceiling automated scores plus planted pass/fail calibration artifacts.",
            "cost_mode": "optional_paid_judge",
        })
    if not has_report_ready_score:
        recommendations.append({
            "priority": len(recommendations) + 1,
            "action": "Run a small scored prompt_sweep comparing prompt_report_ready against existing prompt variants.",
            "reason": "report_ready is candidate-only and must not be promoted from static checks.",
            "cost_mode": "paid_judge_small",
        })
    recommendations.append({
        "priority": len(recommendations) + 1,
        "action": "Create a fresh validation cohort before claiming generalization beyond the current exposed sets.",
        "reason": "The current v2/v3/v4 sets have now informed diagnostics, scoring, or candidate rejection.",
        "cost_mode": "no_api_question_generation_then_paid_eval",
    })
    if has_v4_first_score:
        recommendations.append({
            "priority": len(recommendations) + 1,
            "action": "Review L25 answers for human readability and investigate the slow v4 cases.",
            "reason": "L25 is the current best evidence, while later same-set probes did not beat it.",
            "cost_mode": "mostly_no_api_review",
        })

    best_promotable = max(promotable, key=lambda c: c["edd"], default=None)
    best_corrected = max(corrected, key=lambda c: c["edd"], default=None)
    exposure_summary = {}
    if exposure:
        entries = exposure.get("entries") or []
        exposure_summary = {
            "entry_count": len(entries),
            "strict_candidate_files": [
                e.get("name") for e in entries
                if e.get("claim_use") in {"candidate_until_first_run"}
            ],
            "spent_or_diagnostic_files": [
                e.get("name") for e in entries
                if e.get("claim_use") in {"first_holdout_only", "diagnostic_only", "development_and_regression_only"}
            ],
        }

    return {
        "schema": "rfp_rag_headless_gate_report.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "loop_points_path": str(args.loop_points),
        "row_count": len(rows),
        "classifications": classifications,
        "summary": {
            "promotable_count": len(promotable),
            "diagnostic_or_qualitative_count": len(diagnostic),
            "candidate_only_count": len(candidate_only),
            "measurement_correction_count": len(corrected),
            "best_promotable": best_promotable,
            "best_corrected_or_measurement": best_corrected,
            "human_quality_avg": human_quality_avg,
            "evidence_safety_score_avg": evidence_safety_avg,
            "red_flags": red_flags,
            "exposure_summary": exposure_summary,
        },
        "gate_rules": {
            "promote": "Only first-run or scored validation rows with judge results and no targeted/reuse flags.",
            "hold": "Near-ceiling or measurement-corrected rows that need calibration/new validation.",
            "diagnostic_only": "Local checks, no-judge answer probes, source probes, static checks, and qualitative reviews.",
            "candidate_only": "Code/prompt/routing candidates that passed local checks but lack scored eval evidence.",
            "overfit_risk": "Rows produced after inspecting failures on the same cohort, same-answer recomputations, or targeted retries.",
            "needs_new_validation": "Any final/generalization claim after using the current cohort to guide fixes.",
        },
        "recommendations": recommendations,
    }


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    s = report["summary"]
    lines = [
        "# Headless Red/Overfit Gate Report",
        "",
        f"- created_at: `{report['created_at']}`",
        f"- loop rows checked: `{report['row_count']}`",
        f"- promotable_count: `{s['promotable_count']}`",
        f"- measurement_correction_count: `{s['measurement_correction_count']}`",
        f"- diagnostic_or_qualitative_count: `{s['diagnostic_or_qualitative_count']}`",
        f"- candidate_only_count: `{s['candidate_only_count']}`",
        f"- human_quality_avg: `{s['human_quality_avg']}`",
        f"- evidence_safety_score_avg: `{s['evidence_safety_score_avg']}`",
        f"- exposure_registry_entries: `{(s.get('exposure_summary') or {}).get('entry_count')}`",
        "",
        "## Current Gate Decision",
        "",
    ]
    best = s.get("best_promotable")
    corrected = s.get("best_corrected_or_measurement")
    if best:
        lines.append(f"- best promotable evidence: `{best['loop_point']}` `{best['label']}` EDD `{best['edd']}`")
    if corrected:
        lines.append(
            f"- best corrected/measurement point: `{corrected['loop_point']}` `{corrected['label']}` "
            f"EDD `{corrected['edd']}`; do not call this model improvement by itself."
        )
    lines.extend([
        f"- active red flags: `{', '.join(s['red_flags'])}`",
        "",
        "## Row Labels",
        "",
        "| loop | state | EDD | promotion | flags |",
        "|---|---|---:|---|---|",
    ])
    for c in report["classifications"]:
        edd = "" if c["edd"] is None else f"{c['edd']:.2f}"
        flags = ", ".join(c["flags"])
        lines.append(f"| `{c['loop_point']}` | {c['state']} | {edd} | {c['promotion_allowed']} | {flags} |")

    exposure = s.get("exposure_summary") or {}
    if exposure:
        lines.extend(["", "## Exposure Registry", ""])
        lines.append(f"- strict candidate files: `{', '.join(exposure.get('strict_candidate_files') or [])}`")
        lines.append(f"- spent/diagnostic files: `{', '.join(exposure.get('spent_or_diagnostic_files') or [])}`")

    lines.extend(["", "## Next Recommendations", ""])
    for rec in report["recommendations"]:
        lines.append(f"{rec['priority']}. {rec['action']} `{rec['cost_mode']}`")
        lines.append(f"   - reason: {rec['reason']}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop-points", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--quality-matrix", type=Path)
    parser.add_argument("--exposure-registry", type=Path)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    report = build_report(args)
    json_path = args.out_dir / "headless_gate_report.json"
    md_path = args.out_dir / "headless_gate_report.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(md_path, report)
    print(json.dumps({"json": str(json_path), "md": str(md_path), "row_count": report["row_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
