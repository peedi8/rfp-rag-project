from __future__ import annotations

import argparse
import csv
import html
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_MANIFEST = Path("eval/question_bank64_runnable_manifest_20260707.json")

STRICTNESS_BY_QID = {
    "Q001": "taxonomy_candidate",
    "Q002": "exact_repeated_org_set",
    "Q003": "exact_top_amount_order",
    "Q004": "exact_amount_threshold_set",
    "Q005": "exact_amount_threshold_set_with_domain_note",
    "Q006": "candidate_keyword_discovery",
    "Q007": "candidate_keyword_discovery",
    "Q008": "candidate_keyword_discovery",
    "Q009": "candidate_keyword_discovery",
    "Q010": "candidate_keyword_discovery",
    "Q011": "candidate_keyword_discovery",
    "Q012": "exact_format_count",
    "Q054": "candidate_keyword_discovery",
    "Q055": "candidate_keyword_discovery",
    "Q065": "candidate_keyword_discovery",
    "Q070": "candidate_followup_domain_expansion",
    "Q076": "boundary_missing_metadata",
}

EXACT_STRICTNESS = {
    "exact_repeated_org_set",
    "exact_top_amount_order",
    "exact_amount_threshold_set",
    "exact_amount_threshold_set_with_domain_note",
    "exact_format_count",
    "boundary_missing_metadata",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def doc_label(doc: dict[str, Any]) -> str:
    amount = doc.get("amount_krw")
    amount_text = "amount=missing" if amount is None else f"amount={int(amount):,}"
    return f"{doc.get('doc_id')} | {doc.get('org')} | {doc.get('title')} | {amount_text}"


def unique_docs(docs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for doc in docs:
        doc_id = str(doc.get("doc_id", ""))
        if doc_id and doc_id not in seen:
            seen.add(doc_id)
            out.append(doc)
    return out


def docs_from_key(key: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(key.get("docs"), list):
        return unique_docs(key["docs"])
    if isinstance(key.get("top10"), list):
        return unique_docs(key["top10"])
    if isinstance(key.get("orgs"), dict):
        docs: list[dict[str, Any]] = []
        for org_docs in key["orgs"].values():
            docs.extend(org_docs)
        return unique_docs(docs)
    if isinstance(key.get("buckets"), dict):
        docs = []
        for bucket_docs in key["buckets"].values():
            docs.extend(bucket_docs)
        return unique_docs(docs)
    return []


def render_answer(case: dict[str, Any], key: dict[str, Any], strictness: str) -> str:
    qid = case["id"]
    lines = [f"Question {qid}: {case.get('question', '')}", ""]
    lines.append(f"Sidecar key type: {key.get('check_type', 'unknown')}")
    lines.append(f"Strictness label: {strictness}")
    lines.append("")
    if qid == "Q012":
        counts = key.get("format_counts", {})
        total = key.get("total_docs")
        lines.append(f"Total documents: {total}")
        for fmt, count in sorted(counts.items()):
            lines.append(f"- {fmt}: {count}")
    elif qid == "Q076":
        docs = docs_from_key(key)
        lines.append(key.get("expected_behavior", "Do not infer missing exact values."))
        for doc in docs:
            lines.append(f"- {doc_label(doc)}")
    elif qid == "Q002":
        orgs = key.get("orgs", {})
        lines.append(f"Repeated issuers: {len(orgs)}")
        for org, docs in orgs.items():
            lines.append(f"- {org}: {len(docs)}")
            for doc in docs[:8]:
                lines.append(f"  - {doc_label(doc)}")
    elif qid == "Q003":
        lines.append("Top 10 by amount:")
        for i, doc in enumerate(key.get("top10", []), 1):
            lines.append(f"{i}. {doc_label(doc)}")
    elif qid == "Q001":
        buckets = key.get("buckets", {})
        lines.append(f"Candidate taxonomy buckets: {len(buckets)}")
        for bucket, docs in buckets.items():
            lines.append(f"- {bucket}: {len(docs)} candidate docs")
            for doc in docs[:5]:
                lines.append(f"  - {doc_label(doc)}")
    else:
        docs = docs_from_key(key)
        count = key.get("count", len(docs))
        lines.append(f"Candidate/expected document count: {count}")
        for doc in docs[:30]:
            lines.append(f"- {doc_label(doc)}")
        if len(docs) > 30:
            lines.append(f"- ... {len(docs) - 30} more docs omitted in markdown preview")
    if "candidate" in strictness:
        lines.append("")
        lines.append("Caveat: this is a candidate sidecar list, not a strict gold answer. Row-level evidence review is required before claiming semantic accuracy.")
    return "\n".join(lines).strip() + "\n"


def make_svg(path: Path, strictness_counts: Counter[str], status_counts: Counter[str]) -> None:
    labels = list(strictness_counts)
    values = [strictness_counts[label] for label in labels]
    width = 920
    height = 320
    left = 220
    top = 40
    bar_h = 24
    gap = 12
    max_v = max(values + [1])
    rows = []
    for i, (label, value) in enumerate(zip(labels, values)):
        y = top + i * (bar_h + gap)
        bar_w = int((width - left - 120) * value / max_v)
        color = "#2f6f73" if "exact" in label or "boundary" in label else "#b07b2c"
        if "taxonomy" in label:
            color = "#6b5ca5"
        rows.append(f'<text x="16" y="{y + 17}" font-size="13" font-family="Arial">{html.escape(label)}</text>')
        rows.append(f'<rect x="{left}" y="{y}" width="{bar_w}" height="{bar_h}" fill="{color}" rx="3" />')
        rows.append(f'<text x="{left + bar_w + 8}" y="{y + 17}" font-size="13" font-family="Arial">{value}</text>')
    status_text = ", ".join(f"{k}: {v}" for k, v in status_counts.items())
    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="#f7f7f4" />',
            '<text x="16" y="24" font-size="18" font-family="Arial" font-weight="700">L120 Metadata Sidecar Strictness</text>',
            *rows,
            f'<text x="16" y="{height - 22}" font-size="13" font-family="Arial">Runner status: {html.escape(status_text)}</text>',
            "</svg>",
        ]
    )
    path.write_text(svg + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run no-API metadata sidecar readiness cases.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    answer_dir = out_dir / "answers"
    answer_dir.mkdir(exist_ok=True)

    keys = manifest.get("metadata_expected_outputs", {})
    cases = [
        c
        for c in manifest.get("cases", [])
        if str(c.get("preflight_answer_key_ref") or "").startswith("metadata_expected_outputs.")
    ]
    results: list[dict[str, Any]] = []
    strictness_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()

    for case in cases:
        qid = case["id"]
        strictness = STRICTNESS_BY_QID.get(qid, "unclassified")
        key_ref = str(case.get("preflight_answer_key_ref") or "")
        key_id = key_ref.split(".")[-1] if "." in key_ref else qid
        key = keys.get(key_id)
        status = "ready" if key else "missing_key"
        docs = docs_from_key(key or {})
        answer = render_answer(case, key or {}, strictness) if key else ""
        answer_path = answer_dir / f"{qid}_sidecar_answer.md"
        if answer:
            answer_path.write_text(answer, encoding="utf-8")
        strict_accuracy_claim_allowed = strictness in EXACT_STRICTNESS
        result = {
            "id": qid,
            "question": case.get("question", ""),
            "execution_mode": case.get("execution_mode"),
            "ordinary_edd_included": case.get("ordinary_edd_included"),
            "strictness": strictness,
            "status": status,
            "check_type": (key or {}).get("check_type"),
            "sidecar_key_id": key_id,
            "doc_count": len(docs),
            "expected_count": (key or {}).get("count", len(docs)),
            "answer_path": str(answer_path) if answer else "",
            "strict_accuracy_claim_allowed": strict_accuracy_claim_allowed,
            "sidecar_readiness_score": 1.0 if status == "ready" else 0.0,
            "semantic_accuracy_score": 1.0 if strict_accuracy_claim_allowed and status == "ready" else None,
            "claim_note": "no-api sidecar readiness; not a model answer and not an EDD row",
        }
        if qid != key_id:
            result["alias_note"] = (
                f"Intentional sidecar alias: this case uses metadata key {key_id} "
                "because the manifest points to a shared corpus-discovery preflight set."
            )
            result["claim_note"] += f"; intentional sidecar alias to {key_id}"
        if "candidate" in strictness or "taxonomy" in strictness:
            result["claim_note"] += "; candidate list requires row-level evidence review"
        results.append(result)
        strictness_counts[strictness] += 1
        status_counts[status] += 1

    exact_scores = [r["semantic_accuracy_score"] for r in results if r["semantic_accuracy_score"] is not None]
    summary = {
        "schema": "metadata_sidecar_run.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "manifest": str(args.manifest),
        "out_dir": str(out_dir),
        "claim": "No-API metadata sidecar readiness run; not an ordinary EDD leaderboard row.",
        "case_count": len(results),
        "status_counts": dict(status_counts),
        "strictness_counts": dict(strictness_counts),
        "ready_count": status_counts.get("ready", 0),
        "sidecar_readiness_score": status_counts.get("ready", 0) / len(results) if results else 0.0,
        "exact_semantic_accuracy_mean": sum(exact_scores) / len(exact_scores) if exact_scores else None,
        "exact_semantic_accuracy_n": len(exact_scores),
        "candidate_or_taxonomy_n": sum(1 for r in results if r["semantic_accuracy_score"] is None),
        "results": results,
    }

    write_json(out_dir / "metadata_sidecar_results.json", summary)
    with (out_dir / "metadata_sidecar_results.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fieldnames = [
            "id",
            "execution_mode",
            "ordinary_edd_included",
            "strictness",
            "status",
            "check_type",
            "sidecar_key_id",
            "doc_count",
            "expected_count",
            "strict_accuracy_claim_allowed",
            "sidecar_readiness_score",
            "semantic_accuracy_score",
            "answer_path",
            "claim_note",
            "alias_note",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

    md = [
        "# L120 Metadata Sidecar Results",
        "",
        summary["claim"],
        "",
        "## Summary",
        f"- case_count: {summary['case_count']}",
        f"- ready_count: {summary['ready_count']}",
        f"- sidecar_readiness_score: {summary['sidecar_readiness_score']:.3f}",
        f"- exact_semantic_accuracy_mean: {summary['exact_semantic_accuracy_mean']}",
        f"- exact_semantic_accuracy_n: {summary['exact_semantic_accuracy_n']}",
        f"- candidate_or_taxonomy_n: {summary['candidate_or_taxonomy_n']}",
        "",
        "## Strictness Counts",
    ]
    for label, count in strictness_counts.items():
        md.append(f"- {label}: {count}")
    md.extend(["", "## Cases", "| id | key | mode | strictness | status | docs | claim |", "|---|---|---|---|---|---:|---|"])
    for row in results:
        md.append(
            f"| {row['id']} | {row['sidecar_key_id']} | {row['execution_mode']} | {row['strictness']} | {row['status']} | {row['doc_count']} | {row['claim_note']} |"
        )
    aliases = [row for row in results if row.get("alias_note")]
    if aliases:
        md.extend(["", "## Intentional Sidecar Aliases"])
        for row in aliases:
            md.append(f"- {row['id']} -> {row['sidecar_key_id']}: {row['alias_note']}")
    (out_dir / "metadata_sidecar_results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    make_svg(out_dir / "metadata_sidecar_strictness.svg", strictness_counts, status_counts)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if status_counts.get("missing_key", 0) == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
