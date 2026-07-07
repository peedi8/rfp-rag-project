"""Analyze adversarial RAG eval outputs beyond aggregate EDD."""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"), strict=False)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def qmap(path: Path) -> dict[str, dict[str, Any]]:
    return {q["id"]: q for q in load_json(path)}


def is_target_org(org: str, targets: list[str]) -> bool:
    return any(target in (org or "") or (org or "") in target for target in targets)


def citation_count(answer: str) -> int:
    return answer.count("문서")


def row_issues(row: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if row["non_target_org_rate"] >= 0.375:
        issues.append("high_context_contamination")
    if row["latency_sec"] >= 30:
        issues.append("slow_case")
    if row["answer_chars"] >= 1400:
        issues.append("long_answer")
    if row["expect_abstention"] and not row["abstention"]:
        issues.append("missed_abstention")
    if (not row["expect_abstention"]) and row["abstention"]:
        issues.append("false_abstention")
    if row["citation_mentions"] == 0 and not row["expect_abstention"]:
        issues.append("no_visible_citation_marker")
    if row["groundedness"] is not None and row["groundedness"] < 4:
        issues.append("low_groundedness")
    if row["relevance"] is not None and row["relevance"] < 4:
        issues.append("low_relevance")
    return issues


def analyze(details_path: Path, questions_path: Path) -> dict[str, Any]:
    questions = qmap(questions_path)
    payload = load_json(details_path)
    rows: list[dict[str, Any]] = []
    stability_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for experiment, exp in payload.items():
        for detail in exp.get("details", []):
            q = questions.get(detail.get("id"), {})
            targets = q.get("target_orgs") or []
            retrieved = detail.get("retrieved_orgs") or []
            non_target = [org for org in retrieved if targets and not is_target_org(org, targets)]
            answer = detail.get("answer") or ""
            judge = detail.get("judge") or {}
            row = {
                "experiment": experiment,
                "id": detail.get("id"),
                "type": q.get("type", detail.get("type")),
                "questioner_profile": q.get("questioner_profile", ""),
                "failure_mode": q.get("failure_mode", ""),
                "stability_group": q.get("stability_group", ""),
                "target_orgs": targets,
                "retrieved_orgs": retrieved,
                "retrieved_count": len(retrieved),
                "non_target_org_count": len(non_target),
                "non_target_org_rate": round(len(non_target) / len(retrieved), 3) if retrieved else 0.0,
                "coverage": detail.get("coverage"),
                "first_hit_rank": detail.get("first_hit_rank"),
                "abstention": detail.get("abstention"),
                "expect_abstention": detail.get("expect_abstention", q.get("expect_abstention", False)),
                "latency_sec": detail.get("latency_sec"),
                "answer_chars": len(answer),
                "citation_mentions": citation_count(answer),
                "groundedness": judge.get("groundedness"),
                "relevance": judge.get("relevance"),
            }
            row["issues"] = row_issues(row)
            rows.append(row)
            if row["stability_group"]:
                stability_groups[row["stability_group"]].append(row)

    issue_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        for issue in row["issues"]:
            issue_counts[issue] += 1

    stability = []
    for group, group_rows in stability_groups.items():
        if len(group_rows) < 2:
            continue
        stability.append({
            "group": group,
            "cases": [r["id"] for r in group_rows],
            "latency_range": [
                min(float(r["latency_sec"] or 0) for r in group_rows),
                max(float(r["latency_sec"] or 0) for r in group_rows),
            ],
            "answer_chars_range": [
                min(r["answer_chars"] for r in group_rows),
                max(r["answer_chars"] for r in group_rows),
            ],
            "groundedness_values": [r["groundedness"] for r in group_rows],
            "relevance_values": [r["relevance"] for r in group_rows],
            "abstention_values": [r["abstention"] for r in group_rows],
            "issue_union": sorted({issue for r in group_rows for issue in r["issues"]}),
        })

    return {
        "schema": "rfp_rag_adversarial_analysis.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "details_path": str(details_path),
        "questions_path": str(questions_path),
        "summary": {
            "cases": len(rows),
            "issue_counts": dict(sorted(issue_counts.items())),
            "avg_non_target_org_rate": round(sum(r["non_target_org_rate"] for r in rows) / len(rows), 3) if rows else None,
            "avg_answer_chars": round(sum(r["answer_chars"] for r in rows) / len(rows), 1) if rows else None,
            "avg_latency_sec": round(sum(float(r["latency_sec"] or 0) for r in rows) / len(rows), 3) if rows else None,
            "stability_groups": len(stability),
        },
        "rows": rows,
        "stability": stability,
    }


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# Adversarial Run Analysis",
        "",
        f"- created_at: {result['created_at']}",
        f"- cases: {summary['cases']}",
        f"- avg_non_target_org_rate: {summary['avg_non_target_org_rate']}",
        f"- avg_answer_chars: {summary['avg_answer_chars']}",
        f"- avg_latency_sec: {summary['avg_latency_sec']}",
        "",
        "## Issue Counts",
        "",
    ]
    for key, value in summary["issue_counts"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Cases", ""])
    for row in result["rows"]:
        lines.extend([
            f"### {row['id']}",
            "",
            f"- profile: {row['questioner_profile']}",
            f"- failure_mode: {row['failure_mode']}",
            f"- non_target_org_rate: {row['non_target_org_rate']}",
            f"- latency_sec: {row['latency_sec']}",
            f"- answer_chars: {row['answer_chars']}",
            f"- groundedness/relevance: {row['groundedness']} / {row['relevance']}",
            f"- abstention: {row['abstention']} expected={row['expect_abstention']}",
            f"- issues: {', '.join(row['issues']) if row['issues'] else 'none'}",
            "",
        ])
    if result["stability"]:
        lines.extend(["## Stability Groups", ""])
        for row in result["stability"]:
            lines.extend([
                f"### {row['group']}",
                "",
                f"- cases: {', '.join(row['cases'])}",
                f"- latency_range: {row['latency_range']}",
                f"- answer_chars_range: {row['answer_chars_range']}",
                f"- groundedness_values: {row['groundedness_values']}",
                f"- relevance_values: {row['relevance_values']}",
                f"- issues: {', '.join(row['issue_union']) if row['issue_union'] else 'none'}",
                "",
            ])
    return "\n".join(lines).rstrip() + "\n"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "id",
        "type",
        "questioner_profile",
        "failure_mode",
        "non_target_org_rate",
        "latency_sec",
        "answer_chars",
        "citation_mentions",
        "coverage",
        "first_hit_rank",
        "abstention",
        "expect_abstention",
        "groundedness",
        "relevance",
        "issues",
    ]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["issues"] = ",".join(row.get("issues") or [])
            writer.writerow(out)


def write_svg(path: Path, rows: list[dict[str, Any]]) -> None:
    width, height = 900, 360
    ml, mr, mt, mb = 56, 24, 28, 72
    plot_w, plot_h = width - ml - mr, height - mt - mb
    max_latency = max([float(r["latency_sec"] or 0) for r in rows] + [1])
    max_chars = max([int(r["answer_chars"] or 0) for r in rows] + [1])
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<style>text{font-family:Arial,sans-serif;font-size:12px;fill:#27313d}.axis{stroke:#9aa4b2}.grid{stroke:#e8edf3}.dot{fill:#2f6f73;opacity:.85}.bad{fill:#b85c38;opacity:.9}</style>',
        f'<line class="axis" x1="{ml}" y1="{height-mb}" x2="{width-mr}" y2="{height-mb}"/>',
        f'<line class="axis" x1="{ml}" y1="{mt}" x2="{ml}" y2="{height-mb}"/>',
        f'<text x="{ml}" y="18" font-weight="700">Latency vs Answer Length</text>',
        f'<text x="{width-mr}" y="{height-20}" text-anchor="end">answer chars</text>',
        '<text x="12" y="28" transform="rotate(-90 12,28)">latency sec</text>',
    ]
    for i in range(1, 5):
        x = ml + plot_w * i / 4
        y = mt + plot_h * i / 4
        lines.append(f'<line class="grid" x1="{x:.1f}" y1="{mt}" x2="{x:.1f}" y2="{height-mb}"/>')
        lines.append(f'<line class="grid" x1="{ml}" y1="{y:.1f}" x2="{width-mr}" y2="{y:.1f}"/>')
    for row in rows:
        x = ml + (row["answer_chars"] / max_chars) * plot_w
        y = height - mb - (float(row["latency_sec"] or 0) / max_latency) * plot_h
        cls = "bad" if row.get("issues") else "dot"
        lines.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="5"><title>{row["id"]}: {row["issues"]}</title></circle>')
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--details", type=Path, required=True)
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    result = analyze(args.details, args.questions)
    write_json(args.out_dir / "adversarial_analysis.json", result)
    (args.out_dir / "adversarial_analysis.md").write_text(render_markdown(result), encoding="utf-8")
    write_csv(args.out_dir / "adversarial_analysis.csv", result["rows"])
    write_svg(args.out_dir / "latency_vs_answer_length.svg", result["rows"])
    print(json.dumps({"out_dir": str(args.out_dir), "summary": result["summary"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
