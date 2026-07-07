"""Check deterministic claim preservation for exposed metamorphic cases.

This is a no-API diagnostic gate. It does not create a fresh validation score.
It separates source-supported claims from answer-preserved claims so a high
judge score cannot hide a missing claim.
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPECTATIONS = ROOT / "eval" / "claim_preservation_expectations.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize(text: str) -> str:
    return " ".join((text or "").split()).lower()


def contains_any(text: str, markers: list[str]) -> bool:
    haystack = normalize(text)
    return any(normalize(marker) in haystack for marker in markers)


def matching_markers(text: str, markers: list[str]) -> list[str]:
    haystack = normalize(text)
    return [marker for marker in markers if normalize(marker) in haystack]


def has_underanswer_near(text: str, anchors: list[str], markers: list[str]) -> bool:
    lines = [normalize(line) for line in (text or "").splitlines() if line.strip()]
    marker_hits = [normalize(marker) for marker in markers]
    anchor_hits = [normalize(anchor) for anchor in anchors]
    for line in lines:
        if any(anchor in line for anchor in anchor_hits) and any(marker in line for marker in marker_hits):
            return True
    haystack = normalize(text)
    for anchor in anchors:
        needle = normalize(anchor)
        for match in re.finditer(re.escape(needle), haystack):
            start = max(0, match.start() - 80)
            end = min(len(haystack), match.end() + 80)
            snippet = haystack[start:end]
            if any(marker in snippet for marker in marker_hits):
                return True
    return False


def _source_rows_from_csv(path: Path, expectation: dict) -> list[str]:
    search = expectation.get("source_search") or {}
    required_any = search.get("required_any") or []
    target_orgs = expectation.get("target_org_any") or []
    rows = []
    try:
        with path.open("r", encoding="utf-8-sig", errors="ignore", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                row_text = "\n".join(row)
                if target_orgs and not contains_any(row_text, target_orgs):
                    continue
                if required_any and not contains_any(row_text, required_any):
                    continue
                rows.append(row_text)
    except (OSError, csv.Error):
        return []
    return rows


def source_text_for(expectation: dict, source_root: Path) -> str:
    search = expectation.get("source_search") or {}
    file_glob = search.get("file_glob", "")
    paths = [Path(p) for p in glob.glob(str(source_root / file_glob))]
    texts = []
    required_any = search.get("required_any") or []
    target_orgs = expectation.get("target_org_any") or []
    for path in paths:
        if path.suffix.lower() == ".csv":
            texts.extend(_source_rows_from_csv(path, expectation))
            continue
        try:
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
        except OSError:
            continue
        if target_orgs and not contains_any(text, target_orgs):
            continue
        if required_any and not contains_any(text, required_any):
            continue
        texts.append(text)
    return "\n".join(texts)


def iter_details(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if "details" in payload and isinstance(payload["details"], list):
            return payload["details"]
        rows = []
        for value in payload.values():
            if isinstance(value, dict) and isinstance(value.get("details"), list):
                rows.extend(value["details"])
        return rows
    return []


def evaluate_case(expectation: dict, detail: dict, source_text: str) -> dict:
    answer = detail.get("answer") or ""
    retrieved_orgs = detail.get("retrieved_orgs") or []
    target_orgs = expectation.get("target_org_any") or []
    target_retrieved = [
        org for org in retrieved_orgs
        if any(normalize(target) in normalize(org) for target in target_orgs)
    ]
    off_target_retrieved = [
        org for org in retrieved_orgs
        if target_orgs and not any(normalize(target) in normalize(org) for target in target_orgs)
    ]
    claim_rows = []
    for claim in expectation.get("claims", []):
        source_hits = matching_markers(source_text, claim.get("source_any") or [])
        answer_hits = matching_markers(answer, claim.get("answer_any") or [])
        false_friend_hits = matching_markers(answer, claim.get("false_friend_any") or [])
        underanswered = has_underanswer_near(
            answer,
            claim.get("underanswer_near") or [],
            claim.get("underanswer_any") or [],
        )
        source_supported = bool(source_hits)
        answer_supported = bool(answer_hits)
        status = "pass"
        issue = ""
        if source_supported and underanswered:
            status = "fail"
            issue = "source_supported_but_answer_underanswered"
        elif source_supported and not answer_supported:
            status = "fail"
            issue = "source_supported_but_answer_missing_claim"
        elif not source_supported and answer_supported:
            status = "warn"
            issue = "answer_claim_without_source_marker"
        if false_friend_hits and not answer_supported:
            issue = f"{issue};false_friend_substitution" if issue else "false_friend_substitution"
            if status == "pass":
                status = "fail"
        claim_rows.append(
            {
                "claim_key": claim.get("claim_key", ""),
                "description": claim.get("description", ""),
                "status": status,
                "issue": issue,
                "source_supported": source_supported,
                "answer_supported": answer_supported,
                "underanswered": underanswered,
                "source_hits": source_hits,
                "answer_hits": answer_hits,
                "false_friend_hits": false_friend_hits,
            }
        )
    failed = [row for row in claim_rows if row["status"] == "fail"]
    warned = [row for row in claim_rows if row["status"] == "warn"]
    passed = [row for row in claim_rows if row["status"] == "pass"]
    return {
        "id": expectation.get("id"),
        "canonical_id": expectation.get("canonical_id"),
        "metamorphic_group": expectation.get("metamorphic_group"),
        "claim_scope": expectation.get("claim_scope"),
        "answer_found": bool(answer),
        "retrieval_scope": {
            "target_org_any": target_orgs,
            "retrieved_orgs": retrieved_orgs,
            "target_retrieved_count": len(target_retrieved),
            "off_target_retrieved_count": len(off_target_retrieved),
            "retrieval_scope_status": (
                "mixed_orgs" if off_target_retrieved else ("target_only" if target_retrieved else "target_missing")
            ) if retrieved_orgs else "not_recorded",
        },
        "case_status": "fail" if failed else ("warn" if warned else "pass"),
        "claims_total": len(claim_rows),
        "claims_passed": len(passed),
        "claims_failed": len(failed),
        "claims_warned": len(warned),
        "claim_preservation_rate": round(len(passed) / len(claim_rows), 3) if claim_rows else None,
        "claims": claim_rows,
    }


def render_markdown(result: dict) -> str:
    lines = [
        "# Claim Preservation Check",
        "",
        f"- created_at: `{result['created_at']}`",
        f"- details: `{result['details_path']}`",
        f"- expectations: `{result['expectations_path']}`",
        f"- cases_checked: `{result['summary']['cases_checked']}`",
        f"- claims_total: `{result['summary']['claims_total']}`",
        f"- claims_failed: `{result['summary']['claims_failed']}`",
        f"- preservation_rate: `{result['summary']['claim_preservation_rate']}`",
        "",
        "| case | status | passed | failed | warned | rate |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for case in result["cases"]:
        lines.append(
            f"| {case['id']} | {case['case_status']} | {case['claims_passed']} | "
            f"{case['claims_failed']} | {case['claims_warned']} | {case['claim_preservation_rate']} |"
        )
    lines.extend(["", "## Claim Details", ""])
    for case in result["cases"]:
        lines.append(f"### {case['id']}")
        lines.append("")
        lines.append("| claim | status | issue | source | answer | underanswered |")
        lines.append("|---|---|---|---:|---:|---:|")
        for claim in case["claims"]:
            lines.append(
                f"| {claim['claim_key']} | {claim['status']} | {claim['issue']} | "
                f"{claim['source_supported']} | {claim['answer_supported']} | {claim['underanswered']} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_csv(path: Path, result: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "case_id",
        "claim_key",
        "status",
        "issue",
        "source_supported",
        "answer_supported",
        "underanswered",
        "source_hits",
        "answer_hits",
        "false_friend_hits",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for case in result["cases"]:
            for claim in case["claims"]:
                writer.writerow(
                    {
                        "case_id": case["id"],
                        "claim_key": claim["claim_key"],
                        "status": claim["status"],
                        "issue": claim["issue"],
                        "source_supported": claim["source_supported"],
                        "answer_supported": claim["answer_supported"],
                        "underanswered": claim["underanswered"],
                        "source_hits": "; ".join(claim["source_hits"]),
                        "answer_hits": "; ".join(claim["answer_hits"]),
                        "false_friend_hits": "; ".join(claim["false_friend_hits"]),
                    }
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--details", required=True)
    parser.add_argument("--expectations", default=str(DEFAULT_EXPECTATIONS))
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--source-root", default=str(ROOT))
    args = parser.parse_args()

    details_path = Path(args.details)
    expectations_path = Path(args.expectations)
    out_dir = Path(args.out_dir)
    payload = load_json(details_path)
    details = {row.get("id"): row for row in iter_details(payload)}
    expectations = load_json(expectations_path)

    case_results = []
    for expectation in expectations.get("cases", []):
        detail = details.get(expectation.get("id"), {})
        source_text = source_text_for(expectation, Path(args.source_root))
        case_results.append(evaluate_case(expectation, detail, source_text))

    claims_total = sum(case["claims_total"] for case in case_results)
    claims_failed = sum(case["claims_failed"] for case in case_results)
    claims_passed = sum(case["claims_passed"] for case in case_results)
    result = {
        "schema": "rfp_rag_claim_preservation_results.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "details_path": str(details_path),
        "expectations_path": str(expectations_path),
        "source_root": str(Path(args.source_root)),
        "summary": {
            "cases_checked": len(case_results),
            "claims_total": claims_total,
            "claims_passed": claims_passed,
            "claims_failed": claims_failed,
            "claim_preservation_rate": round(claims_passed / claims_total, 3) if claims_total else None,
            "gate_status": "fail" if claims_failed else "pass",
            "claim_scope": "diagnostic_only_exposed_case",
        },
        "cases": case_results,
    }
    write_json(out_dir / "claim_preservation_results.json", result)
    write_csv(out_dir / "claim_preservation_results.csv", result)
    (out_dir / "claim_preservation_results.md").write_text(render_markdown(result), encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0 if not claims_failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
