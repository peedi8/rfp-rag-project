from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


VALID_TYPES = {
    "single_extract",
    "followup",
    "compare",
    "precise_check",
    "ambiguous_org",
    "abstention",
    "score_trap",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"), strict=False)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalized(value: str) -> str:
    value = value.replace("(용역)", "").replace("(주)", "").replace("주식회사", "")
    return re.sub(r"\s+", "", value)


def source_names(root: Path) -> list[str]:
    if not root.exists():
        return []
    return [p.name for p in root.rglob("*") if p.is_file()]


def org_exists(org: str, names: list[str]) -> bool:
    if not org:
        return True
    needle = normalized(org)
    return any(needle in normalized(name) for name in names)


def validate_question(q: dict[str, Any], names: list[str]) -> list[str]:
    issues: list[str] = []
    if not q.get("id"):
        issues.append("missing_id")
    if q.get("type") not in VALID_TYPES:
        issues.append(f"invalid_type:{q.get('type')}")
    if not isinstance(q.get("turns"), list) or not q.get("turns"):
        issues.append("missing_turns")
    else:
        for turn in q["turns"]:
            if not isinstance(turn, str) or not turn.strip():
                issues.append("blank_turn")
                break
    if q.get("type") != "abstention":
        missing_orgs = [org for org in q.get("target_orgs", []) if not org_exists(str(org), names)]
        if missing_orgs:
            issues.append("missing_source_org:" + ",".join(missing_orgs))
    return issues


def convert_question(q: dict[str, Any]) -> dict[str, Any]:
    converted = {
        "id": q["id"],
        "type": q["type"],
        "turns": q["turns"],
        "target_orgs": q.get("target_orgs", []),
        "target_biz": q.get("target_biz", ""),
    }
    if q.get("expect_abstention"):
        converted["expect_abstention"] = True
    note_parts = []
    if q.get("why_this_tests_the_system"):
        note_parts.append("test: " + str(q["why_this_tests_the_system"]))
    if q.get("expected_failure_mode"):
        note_parts.append("expected_failure: " + str(q["expected_failure_mode"]))
    if note_parts:
        converted["note"] = " | ".join(note_parts)
    return converted


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Question Proposal Curation Report",
        "",
        f"- created_at: {report['created_at']}",
        f"- proposals: `{report['proposals_path']}`",
        f"- output: `{report['output_path']}`",
        f"- accepted: {report['accepted_count']}",
        f"- rejected: {report['rejected_count']}",
        f"- bom_input_detected: {report['bom_input_detected']}",
        "",
        "## Type Counts",
        "",
    ]
    for key, value in report["type_counts"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Accepted Questions", ""])
    for q in report["accepted"]:
        turns = " / ".join(q["turns"])
        lines.append(f"- `{q['id']}` ({q['type']}): {turns}")
    if report["rejected"]:
        lines.extend(["", "## Rejected Questions", ""])
        for item in report["rejected"]:
            lines.append(f"- `{item['id']}`: {', '.join(item['issues'])}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposals", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report-dir", required=True)
    parser.add_argument("--source-files-root", default="data/원본 데이터/files")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    proposals_path = Path(args.proposals).resolve()
    output_path = Path(args.output).resolve()
    report_dir = Path(args.report_dir).resolve()
    source_root = Path(args.source_files_root).resolve()

    raw_bytes = proposals_path.read_bytes()
    bom_input_detected = raw_bytes.startswith(b"\xef\xbb\xbf")
    data = load_json(proposals_path)
    questions = list(data.get("questions", []))
    names = source_names(source_root)

    seen_ids: set[str] = set()
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for q in questions:
        issues = validate_question(q, names)
        if q.get("id") in seen_ids:
            issues.append("duplicate_id")
        seen_ids.add(q.get("id", ""))
        if issues:
            rejected.append({"id": q.get("id", ""), "issues": issues, "question": q})
            continue
        accepted.append(convert_question(q))

    if args.limit > 0:
        accepted = accepted[: args.limit]

    type_counts: dict[str, int] = {}
    for q in accepted:
        type_counts[q["type"]] = type_counts.get(q["type"], 0) + 1

    write_json(output_path, accepted)
    report = {
        "schema": "rfp_rag_question_curation_report.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "proposals_path": str(proposals_path),
        "output_path": str(output_path),
        "source_files_root": str(source_root),
        "bom_input_detected": bom_input_detected,
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "type_counts": type_counts,
        "accepted": accepted,
        "rejected": rejected,
    }
    write_json(report_dir / "questions_v2_curation.json", report)
    (report_dir / "questions_v2_curation.md").write_text(markdown_report(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output_path),
                "accepted": len(accepted),
                "rejected": len(rejected),
                "bom_input_detected": bom_input_detected,
                "report_dir": str(report_dir),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
