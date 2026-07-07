from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from scripts.run_sparse_field_guard import GLOBAL_NOT_FOUND_MARKERS, NOT_FOUND_MARKERS


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_questions(path: Path) -> dict[str, dict]:
    data = read_json(path)
    cases = data if isinstance(data, list) else data.get("cases", [])
    return {case["id"]: case for case in cases}


def has_any(text: str, markers: list[str] | tuple[str, ...]) -> bool:
    return any(marker and marker in text for marker in markers)


def has_not_found_near(text: str, label: str) -> bool:
    if not label:
        return False
    for idx in find_all(text, label):
        window = text[max(0, idx - 140) : idx + len(label) + 180]
        if has_any(window, NOT_FOUND_MARKERS):
            return True
    return False


def find_all(text: str, needle: str) -> list[int]:
    indexes: list[int] = []
    start = 0
    while needle:
        idx = text.find(needle, start)
        if idx < 0:
            break
        indexes.append(idx)
        start = idx + len(needle)
    return indexes


def audit_detail(case: dict, detail: dict) -> dict:
    answer = detail.get("answer") or ""
    present = [x for x in case.get("expected_present_field_labels", []) if x]
    absent = [x for x in case.get("expected_absent_field_labels", []) if x]
    global_not_found = has_any(answer, GLOBAL_NOT_FOUND_MARKERS) and has_any(answer, NOT_FOUND_MARKERS)
    absent_mentions = [label for label in absent if label in answer]
    absent_caveated = [
        label for label in absent
        if label in answer and (global_not_found or has_not_found_near(answer, label))
    ]
    absent_uncaveated = [
        label for label in absent
        if label in answer and not (global_not_found or has_not_found_near(answer, label))
    ]
    present_mentions = [label for label in present if label in answer]
    absent_pass = len(absent_uncaveated) == 0 and (global_not_found or len(absent_caveated) == len(absent_mentions))
    present_coverage = round(len(present_mentions) / len(present), 3) if present else None
    partial_answer_shape = bool(present_mentions) and (global_not_found or bool(absent_caveated))
    detector_conflict = bool(detail.get("abstention")) and partial_answer_shape
    padding_risk = bool(absent_uncaveated)
    case_passed = (
        not padding_risk
        and (present_coverage is None or present_coverage >= 0.5)
        and partial_answer_shape
    )
    return {
        "case_id": detail.get("id", ""),
        "mode": "padding_trap" if "padding_trap" in detail.get("id", "") else "mixed",
        "abstention_detector": bool(detail.get("abstention")),
        "present_expected": len(present),
        "present_mentions": len(present_mentions),
        "present_coverage": present_coverage,
        "absent_expected": len(absent),
        "absent_mentions": len(absent_mentions),
        "absent_caveated": len(absent_caveated),
        "absent_uncaveated": len(absent_uncaveated),
        "global_not_found": global_not_found,
        "partial_answer_shape": partial_answer_shape,
        "detector_conflict": detector_conflict,
        "padding_risk": padding_risk,
        "case_passed": case_passed,
        "latency_sec": detail.get("latency_sec"),
        "judge_groundedness": (detail.get("judge") or {}).get("groundedness"),
        "judge_relevance": (detail.get("judge") or {}).get("relevance"),
        "uncaveated_labels": ";".join(absent_uncaveated),
    }


def summarize_rows(rows: list[dict]) -> dict:
    if not rows:
        return {
            "cases": 0,
            "case_pass_rate": None,
            "padding_risk_count": 0,
            "detector_conflict_count": 0,
            "avg_present_coverage": None,
            "avg_latency_sec": None,
        }
    pass_count = sum(1 for row in rows if row["case_passed"])
    covs = [row["present_coverage"] for row in rows if row["present_coverage"] is not None]
    lats = [float(row["latency_sec"]) for row in rows if row.get("latency_sec") is not None]
    return {
        "cases": len(rows),
        "case_pass_rate": round(pass_count / len(rows), 3),
        "padding_risk_count": sum(1 for row in rows if row["padding_risk"]),
        "detector_conflict_count": sum(1 for row in rows if row["detector_conflict"]),
        "avg_present_coverage": round(sum(covs) / len(covs), 3) if covs else None,
        "avg_latency_sec": round(sum(lats) / len(lats), 3) if lats else None,
    }


def iter_experiment_details(run_dir: Path):
    for path in sorted((run_dir / "worker_outputs").glob("*/*details.json")):
        payload = read_json(path)
        for experiment, data in payload.items():
            yield path.parent.name, experiment, data.get("details", [])


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def render_markdown(result: dict) -> str:
    lines = [
        "# Sparse Answer Audit",
        "",
        "This diagnostic checks sparse-field answer shape separately from ordinary EDD.",
        "",
        "## Experiment Summary",
        "",
        "| run | suite output | experiment | pass rate | padding risks | detector conflicts | present coverage | latency |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in result["summary_rows"]:
        lines.append(
            "| {run} | {worker_output} | {experiment} | {case_pass_rate} | {padding_risk_count} | {detector_conflict_count} | {avg_present_coverage} | {avg_latency_sec} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Notes",
            "- `padding_risk` means an absent field label appeared without a nearby or global not-found caveat.",
            "- `detector_conflict` means the binary abstention detector called the answer an abstention even though the answer had a partial answer + absence-caveat shape.",
            "- These rows are diagnostic-only and must not be promoted to ordinary EDD ranking.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_svg(path: Path, summary_rows: list[dict]) -> None:
    width = 1040
    row_h = 34
    height = 76 + row_h * max(1, len(summary_rows))
    rows = []
    for i, row in enumerate(summary_rows):
        y = 58 + i * row_h
        pass_rate = row.get("case_pass_rate") or 0
        conflict = row.get("detector_conflict_count") or 0
        bar_w = int(430 * pass_rate)
        rows.extend(
            [
                f'<text x="20" y="{y + 17}" font-size="12" font-family="Arial">{row["experiment"]}</text>',
                f'<rect x="300" y="{y}" width="{bar_w}" height="18" rx="3" fill="#2f7d62" />',
                f'<text x="742" y="{y + 15}" font-size="12" font-family="Arial">pass {pass_rate:.3f} / detector conflicts {conflict}</text>',
            ]
        )
    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="#ffffff" />',
            '<text x="20" y="30" font-size="18" font-family="Arial" font-weight="700">Sparse Answer Audit Pass Rate</text>',
            *rows,
            "</svg>",
        ]
    )
    path.write_text(svg + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--questions", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()

    run_dir = args.run_dir
    questions = load_questions(args.questions)
    out_dir = args.out_dir or run_dir / "analysis" / "sparse_answer_audit"

    case_rows: list[dict] = []
    summary_rows: list[dict] = []
    for worker_output, experiment, details in iter_experiment_details(run_dir):
        rows = []
        for detail in details:
            case = questions.get(detail.get("id", ""), {})
            if not case:
                continue
            row = {
                "run": run_dir.name,
                "worker_output": worker_output,
                "experiment": experiment,
                **audit_detail(case, detail),
            }
            rows.append(row)
            case_rows.append(row)
        summary_rows.append(
            {
                "run": run_dir.name,
                "worker_output": worker_output,
                "experiment": experiment,
                **summarize_rows(rows),
            }
        )

    summary_rows.sort(
        key=lambda row: (
            -(row.get("case_pass_rate") or 0),
            row.get("padding_risk_count") or 0,
            row.get("detector_conflict_count") or 0,
            row.get("avg_latency_sec") or 999,
        )
    )
    result = {
        "schema": "rfp_rag_sparse_answer_audit.v1",
        "run_dir": str(run_dir),
        "questions": str(args.questions),
        "diagnostic_only": True,
        "summary_rows": summary_rows,
        "case_rows": case_rows,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "sparse_answer_audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_csv(out_dir / "sparse_answer_audit_cases.csv", case_rows)
    write_csv(out_dir / "sparse_answer_audit_summary.csv", summary_rows)
    (out_dir / "sparse_answer_audit.md").write_text(render_markdown(result), encoding="utf-8")
    write_svg(out_dir / "sparse_answer_audit.svg", summary_rows)
    print(json.dumps({"summary_rows": summary_rows}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
