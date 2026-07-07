from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST = Path("eval/question_bank64_runnable_manifest_20260707.json")

TARGET_MODES = {
    "selected_project_seeded_contract_rag",
    "selected_project_seeded_technical_rag",
    "conversation_seeded_followup_rag",
    "conversation_seeded_numeric_comparison",
    "conversation_seeded_domain_expansion",
    "unsupported_claim_boundary",
    "persona_or_business_usefulness_seeded_rag",
}

PRIMARY_SEEDS = {
    "Q038": ["S_PORTAL_KOREA_UNIV"],
    "Q039": ["S_PORTAL_KOREA_UNIV"],
    "Q040": ["S_PORTAL_KOREA_UNIV"],
    "Q041": ["S_PORTAL_KOREA_UNIV"],
    "Q042": ["S_PORTAL_KOREA_UNIV"],
    "Q043": ["S_PORTAL_KOREA_UNIV"],
    "Q044": ["S_PORTAL_KOREA_UNIV"],
    "Q045": ["S_PORTAL_KOREA_UNIV"],
    "Q046": ["S_KOGAS_ERP"],
    "Q047": ["S_KOGAS_ERP"],
    "Q048": ["S_KOGAS_ERP"],
    "Q049": ["S_BONGHWA_DISASTER"],
    "Q050": ["S_BONGHWA_DISASTER"],
    "Q051": ["S_BONGHWA_DISASTER"],
    "Q052": ["S_BONGHWA_DISASTER"],
    "Q053": ["S_KOGAS_ERP"],
    "Q067": ["S_PORTAL_KOREA_UNIV"],
    "Q069": ["S_PORTAL_KOREA_UNIV", "S_LMS_SPORTS_ETHICS"],
    "Q070": ["S_LMS_SPORTS_ETHICS"],
    "Q071": ["S_PORTAL_KOREA_UNIV"],
    "Q072": ["S_PORTAL_KOREA_UNIV"],
    "Q073": ["S_INCHEON_JOB_ISP"],
    "Q075": ["S_PORTAL_KOREA_UNIV"],
    "Q077": ["S_PORTAL_KOREA_UNIV"],
    "Q079": ["S_PORTAL_KOREA_UNIV"],
    "Q080": [],
    "Q081": ["S_PORTAL_KOREA_UNIV"],
    "Q082": ["S_PORTAL_KOREA_UNIV"],
    "Q083": ["S_PORTAL_KOREA_UNIV"],
    "Q084": ["S_PORTAL_KOREA_UNIV"],
    "Q085": ["S_PORTAL_KOREA_UNIV"],
    "Q086": ["S_PORTAL_KOREA_UNIV"],
    "Q087": ["S_PORTAL_KOREA_UNIV"],
    "Q088": ["S_PORTAL_KOREA_UNIV"],
    "Q089": ["S_PORTAL_KOREA_UNIV"],
}

SECONDARY_VARIANTS = {
    "persona_add_transfer": {
        "case_ids": ["Q082", "Q083", "Q084", "Q085", "Q086", "Q087", "Q088", "Q089"],
        "seed_refs": ["S_ADD_LARGE_TRANSFER"],
        "claim": "secondary persona/usefulness variant on a technical-upgrade seed",
    },
    "technical_add_transfer": {
        "case_ids": ["Q046", "Q047", "Q048", "Q049", "Q050", "Q051", "Q052", "Q053"],
        "seed_refs": ["S_ADD_LARGE_TRANSFER"],
        "claim": "secondary sparse-technical seed to test not-found behavior",
    },
}

EXPECT_ABSTENTION = {"Q075", "Q077", "Q079", "Q080", "Q081"}


def load_json(path: Path) -> dict[str, Any]:
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


def add_dynamic_seeds(seed_catalog: dict[str, Any], corpus_csv: Path | None) -> dict[str, Any]:
    if not corpus_csv or not corpus_csv.exists():
        return seed_catalog
    with corpus_csv.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return seed_catalog
    keys = list(rows[0].keys())
    title_key, amount_key, org_key, pub_key, start_key, end_key, fmt_key, filename_key, text_key = (
        keys[2],
        keys[3],
        keys[4],
        keys[5],
        keys[6],
        keys[7],
        keys[9],
        keys[10],
        keys[11],
    )

    def amount(raw: str) -> float | None:
        raw = (raw or "").strip()
        if not raw:
            return None
        try:
            return float(raw.replace(",", ""))
        except ValueError:
            return None

    dynamic_rows = {
        "S_INCHEON_JOB_ISP": 30,
    }
    for seed_id, one_based in dynamic_rows.items():
        if seed_id in seed_catalog or one_based > len(rows):
            continue
        row = rows[one_based - 1]
        seed_catalog[seed_id] = {
            "doc_id": f"DOC{one_based:03d}",
            "row_index": one_based,
            "title": row[title_key].strip(),
            "org": row[org_key].strip(),
            "amount_krw": amount(row[amount_key]),
            "format": row[fmt_key].strip(),
            "text_length": len(row[text_key] or ""),
            "published_at": row[pub_key],
            "bid_start_at": row[start_key],
            "bid_end_at": row[end_key],
            "filename": row[filename_key].strip(),
            "why": "dynamic L121 seed for ISP/ISMP follow-up terminology context",
        }
    return seed_catalog


def seed_phrase(seed: dict[str, Any]) -> str:
    return f"{seed['org']}의 '{seed['title']}'"


def seed_selection_turn(seeds: list[dict[str, Any]]) -> str:
    if not seeds:
        return ""
    if len(seeds) == 1:
        seed = seeds[0]
        amount = seed.get("amount_krw")
        amount_text = "금액 미기재" if amount is None else f"{int(amount):,}원"
        return (
            f"이 대화에서는 {seed_phrase(seed)} 공고를 선택한 사업으로 볼게. "
            f"먼저 이 공고의 발주기관, 사업명, 사업금액({amount_text}), 입찰 마감일을 문서 기준으로 확인해줘."
        )
    joined = "과 ".join(seed_phrase(seed) for seed in seeds)
    return f"이 대화에서는 {joined} 두 공고를 비교 대상으로 볼게. 먼저 두 공고의 기관, 사업명, 사업금액을 문서 기준으로 확인해줘."


def prior_turns_for(case_id: str, seeds: list[dict[str, Any]]) -> list[str]:
    if case_id == "Q072":
        return ["선택한 사업의 핵심 범위, 일정/예산, 주요 위험을 문서 근거로 먼저 요약해줘."]
    if case_id == "Q073":
        return ["선택한 ISP/ISMP 관련 공고에서 ISP와 ISMP라는 용어가 어떤 맥락으로 나오는지 먼저 설명해줘."]
    return []


def resolve_question(question: str, seeds: list[dict[str, Any]], case_id: str) -> str:
    if not seeds:
        return question
    if case_id == "Q069" and len(seeds) >= 2:
        return f"{seed_phrase(seeds[0])}과 {seed_phrase(seeds[1])} 중 예산 규모가 더 큰 사업은 어느 쪽이고 몇 배 차이나?"
    if case_id == "Q070":
        return f"{seed_phrase(seeds[0])}과 비슷한 교육 또는 학습 관련 사업을 다른 기관에서도 찾아줘."
    if case_id == "Q072":
        return f"{seed_phrase(seeds[0])}의 핵심 내용을 임원 보고용으로 5줄만 요약해줘."
    if case_id == "Q073":
        return f"{seed_phrase(seeds[0])} 문서 맥락을 기준으로 ISMP와 ISP가 무슨 차이인지 쉽게 설명해줘."
    if len(seeds) == 1:
        return f"{seed_phrase(seeds[0])} 기준으로, {question}"
    joined = "과 ".join(seed_phrase(seed) for seed in seeds)
    return f"{joined} 기준으로, {question}"


def make_case(case: dict[str, Any], seeds: list[dict[str, Any]], seed_refs: list[str], variant: str) -> dict[str, Any]:
    seed_turn = seed_selection_turn(seeds)
    prior_turns = prior_turns_for(case["id"], seeds)
    final_turn = case["question"]
    turns = [t for t in [seed_turn, *prior_turns, final_turn] if t]
    resolved_turn = resolve_question(final_turn, seeds, case["id"])
    target_orgs = [seed["org"] for seed in seeds]
    target_biz = " / ".join(seed["title"] for seed in seeds)
    if case["id"] == "Q080":
        target_orgs = []
        target_biz = "corpus-wide profitability boundary"
    base_id = f"l121_{case['id']}_{variant}"
    return {
        "id": base_id,
        "source_case_id": case["id"],
        "type": case["execution_mode"],
        "questioner_profile": case.get("segment") or "selected_project_user",
        "turns": turns,
        "resolved_one_turn": resolved_turn,
        "target_orgs": target_orgs,
        "target_biz": target_biz,
        "expect_abstention": case["id"] in EXPECT_ABSTENTION,
        "seed_refs": seed_refs,
        "seed_titles": [seed["title"] for seed in seeds],
        "seed_policy": (
            "corpus_wide_no_seed"
            if not seeds
            else "one_fixed_seed_per_run_no_cross_seed_synthesis"
            if len(seeds) == 1
            else "explicit_comparison_seed_pair"
        ),
        "execution_status": "prepared_no_api_not_answered",
        "ordinary_edd_candidate": bool(case.get("ordinary_edd_included")),
        "gates": case.get("gates", []),
        "metric_routes": case.get("metric_routes", []),
        "note": (
            "L121 prepared batch only. Use resolved_one_turn for cheaper smoke; "
            "use turns for faithful follow-up/memory evaluation. Preserve first answer run raw."
        ),
    }


def make_svg(path: Path, counts: Counter[str]) -> None:
    width, height = 940, 360
    left, top = 300, 42
    max_v = max(counts.values() or [1])
    rows = []
    for i, (label, value) in enumerate(counts.items()):
        y = top + i * 30
        bar_w = int((width - left - 120) * value / max_v)
        rows.append(f'<text x="16" y="{y + 17}" font-size="13" font-family="Arial">{label}</text>')
        rows.append(f'<rect x="{left}" y="{y}" width="{bar_w}" height="22" fill="#3f6c9b" rx="3" />')
        rows.append(f'<text x="{left + bar_w + 8}" y="{y + 16}" font-size="13" font-family="Arial">{value}</text>')
    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="#f7f7f4" />',
            '<text x="16" y="25" font-size="18" font-family="Arial" font-weight="700">L121 Selected-Project Batch Modes</text>',
            *rows,
            "</svg>",
        ]
    )
    path.write_text(svg + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build selected-project scripted no-API batches.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--corpus-csv", type=Path, default=None)
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    seed_catalog = add_dynamic_seeds(dict(manifest.get("seed_catalog", {})), args.corpus_csv)
    source_cases = [c for c in manifest.get("cases", []) if c.get("execution_mode") in TARGET_MODES]
    prepared: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    for case in source_cases:
        seed_refs = PRIMARY_SEEDS.get(case["id"], case.get("seed_refs", [])[:1])
        missing = [ref for ref in seed_refs if ref not in seed_catalog]
        if missing:
            issues.append({"case_id": case["id"], "issue": "missing_seed", "detail": ",".join(missing)})
            continue
        seeds = [seed_catalog[ref] for ref in seed_refs]
        prepared.append(make_case(case, seeds, seed_refs, "primary"))

    variants: list[dict[str, Any]] = []
    case_by_id = {c["id"]: c for c in source_cases}
    for variant_id, spec in SECONDARY_VARIANTS.items():
        seed_refs = spec["seed_refs"]
        if any(ref not in seed_catalog for ref in seed_refs):
            continue
        seeds = [seed_catalog[ref] for ref in seed_refs]
        for case_id in spec["case_ids"]:
            if case_id in case_by_id:
                row = make_case(case_by_id[case_id], seeds, seed_refs, variant_id)
                row["variant_claim"] = spec["claim"]
                variants.append(row)

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    primary_path = out_dir / "questions_l121_selected_project_multiturn_primary.json"
    resolved_path = out_dir / "questions_l121_selected_project_resolved_primary.json"
    variant_path = out_dir / "questions_l121_selected_project_secondary_variants.json"
    batch_path = out_dir / "selected_project_batch_l121.json"
    csv_path = out_dir / "selected_project_batch_l121.csv"
    md_path = out_dir / "selected_project_batch_l121.md"
    svg_path = out_dir / "selected_project_batch_modes.svg"

    primary_eval = [
        {k: v for k, v in row.items() if k not in {"resolved_one_turn"}}
        for row in prepared
    ]
    resolved_eval = [
        {**{k: v for k, v in row.items() if k != "turns"}, "turns": [row["resolved_one_turn"]], "runner_variant": "resolved_one_turn"}
        for row in prepared
    ]
    write_json(primary_path, primary_eval)
    write_json(resolved_path, resolved_eval)
    write_json(variant_path, variants)

    counts = Counter(row["type"] for row in prepared)
    total_turns_multiturn = sum(len(row["turns"]) for row in prepared)
    total_turns_resolved = len(prepared)
    batch = {
        "schema": "l121_selected_project_batch.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "claim": "No-API selected-project scripted batch builder; not an answer run and not an EDD point.",
        "source_manifest": str(args.manifest),
        "case_count": len(prepared),
        "secondary_variant_count": len(variants),
        "issues": issues,
        "seed_catalog_used": {ref: seed_catalog[ref] for row in prepared for ref in row["seed_refs"]},
        "mode_counts": dict(counts),
        "turn_estimate": {
            "multiturn_primary_llm_calls_if_executed": total_turns_multiturn,
            "resolved_primary_llm_calls_if_executed": total_turns_resolved,
            "cost_saving_note": "Use resolved-primary for cheap retrieval smoke; use multiturn-primary for faithful follow-up memory tests.",
        },
        "files": {
            "primary_multiturn": str(primary_path),
            "primary_resolved_one_turn": str(resolved_path),
            "secondary_variants": str(variant_path),
            "csv": str(csv_path),
            "md": str(md_path),
            "svg": str(svg_path),
        },
        "prepared_cases": prepared,
    }
    write_json(batch_path, batch)

    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        fieldnames = [
            "id",
            "source_case_id",
            "type",
            "seed_refs",
            "target_orgs",
            "target_biz",
            "turn_count",
            "expect_abstention",
            "seed_policy",
            "resolved_one_turn",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in prepared:
            writer.writerow(
                {
                    "id": row["id"],
                    "source_case_id": row["source_case_id"],
                    "type": row["type"],
                    "seed_refs": ";".join(row["seed_refs"]),
                    "target_orgs": ";".join(row["target_orgs"]),
                    "target_biz": row["target_biz"],
                    "turn_count": len(row["turns"]),
                    "expect_abstention": row["expect_abstention"],
                    "seed_policy": row["seed_policy"],
                    "resolved_one_turn": row["resolved_one_turn"],
                }
            )

    lines = [
        "# L121 Selected-Project Scripted Batch",
        "",
        batch["claim"],
        "",
        "## Summary",
        f"- primary cases: {len(prepared)}",
        f"- secondary variants: {len(variants)}",
        f"- multiturn calls if executed: {total_turns_multiturn}",
        f"- resolved calls if executed: {total_turns_resolved}",
        "",
        "## Mode Counts",
    ]
    for mode, count in counts.items():
        lines.append(f"- {mode}: {count}")
    lines.extend(["", "## Cases", "| id | source | mode | seeds | turns | expect_abstention |", "|---|---|---|---|---:|---|"])
    for row in prepared:
        lines.append(
            f"| {row['id']} | {row['source_case_id']} | {row['type']} | {', '.join(row['seed_refs'])} | {len(row['turns'])} | {row['expect_abstention']} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    make_svg(svg_path, counts)

    file_hashes = {name: sha256(Path(path)) for name, path in batch["files"].items() if Path(path).exists()}
    write_json(
        out_dir / "selected_project_batch_l121.manifest.json",
        {
            "schema": "l121_selected_project_batch_manifest.v1",
            "created_at": batch["created_at"],
            "case_count": len(prepared),
            "secondary_variant_count": len(variants),
            "file_hashes": file_hashes,
            "claim": batch["claim"],
            "allowed_use": "prepared execution batch only; preserve first answer run raw",
        },
    )
    print(json.dumps({"case_count": len(prepared), "secondary_variant_count": len(variants), "issues": issues, "files": batch["files"], "turn_estimate": batch["turn_estimate"]}, ensure_ascii=False, indent=2))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
