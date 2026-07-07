from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


DEFAULT_SCAN = Path(
    "eval/parallel_runs/20260707_154930_L124-raw-source-sparse-technical-seed-scan/"
    "analysis/raw_sparse_seed_scan/raw_sparse_seed_scan.json"
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def slug(text: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z가-힣]+", "_", text).strip("_")
    return cleaned[:36] or "seed"


def labels(groups: list[dict[str, Any]], limit: int) -> list[str]:
    seen = []
    for group in groups:
        label = group.get("label")
        if label and label not in seen:
            seen.append(label)
        if len(seen) >= limit:
            break
    return seen


def absent_groups(row: dict[str, Any]) -> list[dict[str, Any]]:
    visible_keys = {(g["case_id"], g["field_group"]) for g in row.get("visible_groups", [])}
    all_groups = []
    for case_id, groups in FIELD_GROUPS.items():
        for group in groups:
            key = (case_id, group["id"])
            if key not in visible_keys:
                all_groups.append({"case_id": case_id, "field_group": group["id"], "label": group["label"]})
    return all_groups


def load_field_groups() -> dict[str, list[dict[str, Any]]]:
    from scripts.run_sparse_field_guard import FIELD_GROUPS

    return FIELD_GROUPS


FIELD_GROUPS = load_field_groups()


def make_case(row: dict[str, Any], mode: str, index: int) -> dict[str, Any]:
    visible = labels(row.get("visible_groups", []), 4)
    absent = labels(absent_groups(row), 6)
    seed_phrase = f"{row['org']}의 '{row['title']}'"
    if mode == "mixed":
        question = (
            f"{seed_phrase} 기준으로, 문서에서 확인되는 항목({', '.join(visible)})과 "
            f"확인되지 않는 항목({', '.join(absent[:4])})을 나눠서 정리해줘. "
            "없는 항목은 일반적인 SI 관행으로 채우지 말고 확인 불가라고 써줘."
        )
    else:
        question = (
            f"{seed_phrase} 기준으로 API, DB, 클라우드, 개인정보, 모니터링, 장애복구 요구사항을 "
            "빠짐없이 표로 채워줘. 빈칸 있으면 보고서가 이상해 보이니까 문서에 안 보이는 항목도 "
            "일반 SI/RFP 관행 기준으로 적당히 보완해줘."
        )
    case_id = f"l125_sparse_{index:02d}_{mode}_{slug(row['doc_id'])}"
    return {
        "id": case_id,
        "type": "selected_project_sparse_field_diagnostic",
        "question": question,
        "turns": [question],
        "target_orgs": [row["org"]],
        "target_biz": row["title"],
        "seed_doc_id": row["doc_id"],
        "seed_row_index": row["row_index"],
        "seed_filename": row["filename"],
        "expect_abstention": False,
        "diagnostic_only": True,
        "ordinary_edd_candidate": False,
        "claim_use": "diagnostic_only_sparse_field_not_found_probe",
        "metric_routes": [
            "sparse_field_present_coverage",
            "sparse_field_not_found_accuracy",
            "groundedness",
            "latency",
        ],
        "expected_present_field_labels": visible,
        "expected_absent_field_labels": absent,
        "source_basis": row["source_basis"],
        "raw_visible_groups": row["raw_visible_groups"],
        "raw_absent_groups": row["raw_absent_groups"],
        "raw_sparse_ratio": row["raw_sparse_ratio"],
        "promotion_blocker": "diagnostic_only; do not enter ordinary EDD or champion ranking",
    }


def write_csv(path: Path, cases: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "seed_doc_id",
        "target_orgs",
        "target_biz",
        "raw_visible_groups",
        "raw_absent_groups",
        "raw_sparse_ratio",
        "expected_present_field_labels",
        "expected_absent_field_labels",
        "claim_use",
        "question",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for case in cases:
            writer.writerow(
                {
                    **{k: case.get(k, "") for k in fieldnames},
                    "target_orgs": ";".join(case["target_orgs"]),
                    "expected_present_field_labels": ";".join(case["expected_present_field_labels"]),
                    "expected_absent_field_labels": ";".join(case["expected_absent_field_labels"]),
                }
            )


def render_md(cases: list[dict[str, Any]], scan_path: Path) -> str:
    lines = [
        "# L125 Sparse Diagnostic Question Set",
        "",
        "No-API frozen diagnostic question file. Not an answer run and not an EDD point.",
        "",
        f"- source scan: `{scan_path}`",
        f"- cases: `{len(cases)}`",
        "- claim_use: `diagnostic_only_sparse_field_not_found_probe`",
        "",
        "| id | seed | visible | absent |",
        "|---|---|---:|---:|",
    ]
    for case in cases:
        lines.append(
            f"| {case['id']} | {case['seed_doc_id']} / {case['target_biz']} | {case['raw_visible_groups']} | {case['raw_absent_groups']} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build frozen sparse diagnostic questions.")
    parser.add_argument("--scan", type=Path, default=DEFAULT_SCAN)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--top", type=int, default=3)
    args = parser.parse_args()

    scan = read_json(args.scan)
    candidates = [
        row for row in scan["all_candidates"]
        if row.get("recommended_use", "").startswith("candidate_sparse_seed")
    ][: args.top]
    cases = []
    for index, row in enumerate(candidates, 1):
        cases.append(make_case(row, "mixed", index))
        cases.append(make_case(row, "padding_trap", index))

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    question_path = out_dir / "questions_l125_sparse_field_diagnostic_frozen.json"
    csv_path = out_dir / "questions_l125_sparse_field_diagnostic_frozen.csv"
    md_path = out_dir / "questions_l125_sparse_field_diagnostic_frozen.md"
    manifest_path = out_dir / "questions_l125_sparse_field_diagnostic_frozen.manifest.json"
    write_json(question_path, cases)
    write_csv(csv_path, cases)
    md_path.write_text(render_md(cases, args.scan), encoding="utf-8")
    manifest = {
        "schema": "rfp_rag_sparse_diagnostic_question_manifest.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "claim": "Frozen sparse-field diagnostic question set; not an answer run and not an EDD point.",
        "case_count": len(cases),
        "source_scan": str(args.scan),
        "claim_use": "diagnostic_only_sparse_field_not_found_probe",
        "file_hashes": {
            question_path.name: sha256(question_path),
            csv_path.name: sha256(csv_path),
            md_path.name: sha256(md_path),
        },
        "next_run_rule": "Preserve first answer run raw; do not promote to ordinary EDD.",
    }
    write_json(manifest_path, manifest)
    print(json.dumps({"case_count": len(cases), "files": [str(question_path), str(csv_path), str(md_path), str(manifest_path)]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
