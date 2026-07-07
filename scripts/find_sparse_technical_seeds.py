from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.run_sparse_field_guard import FIELD_GROUPS, raw_text_for, token_hits


DEFAULT_CORPUS = Path("data/원본 데이터/data_list.csv")

TECHNICAL_TITLE_TOKENS = (
    "시스템",
    "정보",
    "전산",
    "ERP",
    "홈페이지",
    "플랫폼",
    "DB",
    "데이터",
    "고도화",
    "구축",
    "운영",
    "기능개선",
    "재구축",
)

EXCLUDE_TITLES = {
    "대용량 자료전송시스템 고도화",
    "[재공고]차세대 통합정보시스템(ERP) 구축",
    "봉화군 재난통합관리시스템 고도화 사업(협상)(긴급)",
}


def read_corpus(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def all_field_specs() -> list[dict[str, Any]]:
    specs = []
    seen = set()
    for case_id, groups in FIELD_GROUPS.items():
        for group in groups:
            key = (case_id, group["id"])
            if key in seen:
                continue
            seen.add(key)
            specs.append({"case_id": case_id, **group})
    return specs


def is_technical_candidate(row: dict[str, str]) -> bool:
    title = row.get("사업명", "")
    summary = row.get("사업 요약", "")
    joined = f"{title} {summary}"
    return any(token in joined for token in TECHNICAL_TITLE_TOKENS)


def amount_value(raw: str) -> float | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return float(raw.replace(",", ""))
    except ValueError:
        return None


def analyze_row(row: dict[str, str], row_index: int, corpus_csv: Path, specs: list[dict[str, Any]]) -> dict[str, Any]:
    raw_text, basis = raw_text_for(row, corpus_csv)
    csv_text = row.get("텍스트", "")
    visible = []
    csv_visible = []
    for spec in specs:
        hits = token_hits(raw_text, spec["tokens"])
        csv_hits = token_hits(csv_text, spec["tokens"])
        if hits:
            visible.append(
                {
                    "case_id": spec["case_id"],
                    "field_group": spec["id"],
                    "label": spec["label"],
                    "hit_tokens": hits,
                }
            )
        if csv_hits:
            csv_visible.append(
                {
                    "case_id": spec["case_id"],
                    "field_group": spec["id"],
                    "label": spec["label"],
                    "hit_tokens": csv_hits,
                }
            )
    total = len(specs)
    visible_count = len(visible)
    csv_visible_count = len(csv_visible)
    absent_count = total - visible_count
    if len(raw_text or "") < 500 or visible_count == 0:
        recommended_use = "too_empty_for_sparse_seed"
    elif absent_count >= 10:
        recommended_use = "candidate_sparse_seed_high_absence"
    else:
        recommended_use = "too_rich_for_sparse_seed"
    return {
        "row_index": row_index,
        "doc_id": f"DOC{row_index:03d}",
        "title": row.get("사업명", ""),
        "org": row.get("발주 기관", ""),
        "amount_krw": amount_value(row.get("사업 금액", "")),
        "format": row.get("파일형식", ""),
        "filename": row.get("파일명", ""),
        "source_basis": basis,
        "raw_text_length": len(raw_text or ""),
        "csv_text_length": len(csv_text or ""),
        "total_field_groups": total,
        "raw_visible_groups": visible_count,
        "raw_absent_groups": absent_count,
        "csv_visible_groups": csv_visible_count,
        "csv_absent_groups": total - csv_visible_count,
        "raw_sparse_ratio": round((total - visible_count) / total, 4) if total else 0.0,
        "csv_sparse_ratio": round((total - csv_visible_count) / total, 4) if total else 0.0,
        "visible_groups": visible,
        "csv_visible_groups_detail": csv_visible,
        "recommended_use": recommended_use,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "doc_id",
        "row_index",
        "org",
        "title",
        "amount_krw",
        "format",
        "source_basis",
        "raw_text_length",
        "raw_visible_groups",
        "raw_absent_groups",
        "raw_sparse_ratio",
        "csv_visible_groups",
        "csv_absent_groups",
        "csv_sparse_ratio",
        "recommended_use",
        "filename",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rank, row in enumerate(rows, 1):
            writer.writerow({key: row.get(key, "") for key in fieldnames} | {"rank": rank})


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# L124 Raw-Source Sparse Technical Seed Scan",
        "",
        result["claim"],
        "",
        "## Summary",
    ]
    for key, value in result["summary"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Top Candidates",
            "| rank | doc | org | title | raw visible | raw absent | sparse ratio | use |",
            "|---:|---|---|---|---:|---:|---:|---|",
        ]
    )
    for rank, row in enumerate(result["top_candidates"], 1):
        lines.append(
            "| {rank} | {doc} | {org} | {title} | {visible} | {absent} | {ratio:.3f} | {use} |".format(
                rank=rank,
                doc=row["doc_id"],
                org=row["org"],
                title=row["title"],
                visible=row["raw_visible_groups"],
                absent=row["raw_absent_groups"],
                ratio=row["raw_sparse_ratio"],
                use=row["recommended_use"],
            )
        )
    lines.extend(
        [
            "",
            "## Decision Note",
            "",
            "Candidates are not answer runs and not EDD evidence. They are source-selection inputs for a future sparse-field diagnostic.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_svg(path: Path, rows: list[dict[str, Any]]) -> None:
    top = rows[:20]
    width = 1120
    height = 70 + max(1, len(top)) * 34
    max_absent = max((row["raw_absent_groups"] for row in top), default=1)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8f8f5" />',
        '<text x="18" y="30" font-size="18" font-family="Arial" font-weight="700">L124 Raw Sparse Technical Seed Candidates</text>',
    ]
    for i, row in enumerate(top):
        y = 54 + i * 34
        bar_w = int(460 * row["raw_absent_groups"] / max_absent)
        label = html.escape(f"{row['doc_id']} {row['org']} / {row['title'][:42]}")
        lines.append(f'<text x="18" y="{y + 18}" font-size="12" font-family="Arial">{label}</text>')
        lines.append(f'<rect x="430" y="{y}" width="{bar_w}" height="20" fill="#bf6b3d" rx="3" />')
        lines.append(
            f'<text x="{440 + bar_w}" y="{y + 15}" font-size="12" font-family="Arial">absent {row["raw_absent_groups"]} / visible {row["raw_visible_groups"]}</text>'
        )
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Find raw-source sparse technical seed candidates.")
    parser.add_argument("--corpus-csv", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    rows = read_corpus(args.corpus_csv)
    specs = all_field_specs()
    analyzed = []
    for idx, row in enumerate(rows, 1):
        if row.get("사업명", "") in EXCLUDE_TITLES:
            continue
        if not is_technical_candidate(row):
            continue
        analyzed.append(analyze_row(row, idx, args.corpus_csv, specs))
    ranked = sorted(
        analyzed,
        key=lambda row: (
            not row["recommended_use"].startswith("candidate_sparse_seed"),
            -row["raw_sparse_ratio"],
            row["raw_visible_groups"],
            -row["raw_text_length"],
        ),
    )
    top = ranked[: args.limit]
    recommended = [row for row in ranked if row["recommended_use"].startswith("candidate_sparse_seed")]
    result = {
        "schema": "rfp_rag_raw_sparse_seed_scan.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "claim": "No-API raw-source sparse technical seed scan; not an answer run and not an EDD point.",
        "source_corpus_csv": str(args.corpus_csv),
        "summary": {
            "technical_candidate_docs_scanned": len(analyzed),
            "field_group_count": len(specs),
            "recommended_sparse_seed_count": len(recommended),
            "excluded_known_seed_titles": len(EXCLUDE_TITLES),
            "source_basis_counts": dict(Counter(row["source_basis"] for row in analyzed)),
        },
        "top_candidates": top,
        "all_candidates": ranked,
    }

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "raw_sparse_seed_scan.json", result)
    write_csv(out_dir / "raw_sparse_seed_scan.csv", ranked)
    (out_dir / "raw_sparse_seed_scan.md").write_text(render_markdown(result), encoding="utf-8")
    write_svg(out_dir / "raw_sparse_seed_scan.svg", ranked)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
