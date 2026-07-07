"""Aggregate parallel worker outputs into summary tables and SVG graphs."""
from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path


NUMERIC_COLS = [
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

QUALITY_COLS = ("groundedness_avg", "relevance_avg")

SUITE_COLORS = {
    "topk_sweep": "#2f6fed",
    "mmr_lambda_sweep": "#24a148",
    "fetchk_sweep": "#f97316",
    "filter_rewrite_ablation": "#8b5cf6",
}

FIRST_VALIDATION_PREFIX_BY_QUESTION = {
    "questions_v4_frozen_first_run.json": ("l25_",),
    "questions_v6_metamorphic_frozen_first_run.json": ("l37_",),
}

SECONDARY_VARIANT_NAME_MARKERS = (
    "secondary_variants",
    "secondary_technical_guarded",
)


def _num(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _registry_by_name(run_dir: Path) -> dict[str, dict]:
    registry_path = run_dir.parents[1] / "question_exposure_registry.json"
    if not registry_path.exists():
        return {}
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {
        entry.get("name"): entry
        for entry in registry.get("entries", [])
        if entry.get("name")
    }


def _question_file_name(contract: dict) -> str:
    def basename(value: str) -> str:
        return str(value).strip("\"'").replace("\\", "/").split("/")[-1]

    for item in contract.get("inputs") or []:
        name = basename(str(item))
        if name.startswith("questions") and name.endswith(".json"):
            return name
    commands = " ".join((contract.get("validation") or {}).get("commands_run") or [])
    for token in commands.split():
        name = basename(token)
        if name.startswith("questions") and name.endswith(".json"):
            return name
    return ""


def _question_file_paths(run_dir: Path, contract: dict, question_file: str) -> list[Path]:
    paths: list[Path] = []
    for item in contract.get("inputs") or []:
        raw = str(item).strip("\"'")
        if not raw:
            continue
        candidate = Path(raw)
        if candidate.name != question_file:
            continue
        if candidate.is_absolute():
            paths.append(candidate)
        else:
            paths.append(run_dir.parents[1] / candidate)
            paths.append(run_dir / candidate)
    if question_file:
        eval_dir = run_dir.parents[1]
        try:
            paths.extend(eval_dir.rglob(question_file))
        except Exception:
            pass
    deduped = []
    seen = set()
    for path in paths:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(path)
    return deduped


def _question_file_has_secondary_variants(run_dir: Path, contract: dict, question_file: str) -> bool:
    if not question_file:
        return False
    lowered = question_file.lower()
    if any(marker in lowered for marker in SECONDARY_VARIANT_NAME_MARKERS):
        return True
    for path in _question_file_paths(run_dir, contract, question_file):
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        cases = data if isinstance(data, list) else data.get("cases", []) if isinstance(data, dict) else []
        if any(
            isinstance(case, dict)
            and (
                case.get("variant_claim")
                or case.get("diagnostic_label", "").startswith("secondary_")
                or "secondary" in str(case.get("promotion_blocker", ""))
            )
            for case in cases
        ):
            return True
    return False


def _question_file_is_diagnostic_only(run_dir: Path, contract: dict, question_file: str) -> bool:
    if not question_file:
        return False
    for path in _question_file_paths(run_dir, contract, question_file):
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        cases = data if isinstance(data, list) else data.get("cases", []) if isinstance(data, dict) else []
        if not cases:
            continue
        diagnostic_votes = 0
        for case in cases:
            if not isinstance(case, dict):
                continue
            claim_use = str(case.get("claim_use", ""))
            blocker = str(case.get("promotion_blocker", ""))
            if (
                case.get("diagnostic_only") is True
                or claim_use.startswith("diagnostic_only")
                or "diagnostic_only" in blocker
                or case.get("ordinary_edd_candidate") is False
            ):
                diagnostic_votes += 1
        if diagnostic_votes == len(cases):
            return True
    return False


def _read_rows(run_dir: Path) -> list[dict]:
    rows = []
    registry = _registry_by_name(run_dir)
    for path in sorted((run_dir / "worker_outputs").glob("*/*results.csv")):
        contract_path = path.parent / "worker_output.json"
        contract = {}
        if contract_path.exists():
            try:
                contract = json.loads(contract_path.read_text(encoding="utf-8-sig"))
            except Exception:
                contract = {}
        commands = " ".join((contract.get("validation") or {}).get("commands_run") or [])
        is_dry_run = "--dry-run" in commands
        question_file = _question_file_name(contract)
        is_secondary_variant_question_file = _question_file_has_secondary_variants(run_dir, contract, question_file)
        is_diagnostic_question_file_content = _question_file_is_diagnostic_only(run_dir, contract, question_file)
        exposure = registry.get(question_file, {})
        claim_use = exposure.get("claim_use", "")
        exposure_status = exposure.get("status", "")
        is_unregistered_question_file = bool(question_file) and question_file not in registry
        is_diagnostic_questions = claim_use == "diagnostic_only"
        is_do_not_promote = (
            claim_use.startswith("do_not_promote")
            or exposure_status in {"unknown_needs_review"}
        )
        with path.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                row["worker_results_path"] = str(path)
                row["run_label"] = path.parent.name
                row["is_dry_run"] = is_dry_run
                row["question_file"] = question_file
                row["question_claim_use"] = claim_use
                row["question_exposure_status"] = exposure_status
                has_quality = all(row.get(col) not in (None, "") for col in QUALITY_COLS)
                first_run_prefixes = FIRST_VALIDATION_PREFIX_BY_QUESTION.get(question_file, ())
                is_exposed_regression = (
                    claim_use == "first_run_and_regression_only"
                    and first_run_prefixes
                    and not any(row["run_label"].startswith(prefix) for prefix in first_run_prefixes)
                )
                if is_secondary_variant_question_file:
                    row["quality_status"] = "diagnostic_secondary_variant"
                    row["rank_scope"] = "diagnostic_only"
                elif is_diagnostic_question_file_content:
                    row["quality_status"] = "diagnostic_question_file_content"
                    row["rank_scope"] = "diagnostic_only"
                elif is_dry_run:
                    row["quality_status"] = "diagnostic_dry_run"
                    row["rank_scope"] = "diagnostic_only"
                elif is_unregistered_question_file:
                    row["quality_status"] = "diagnostic_unregistered_question_set"
                    row["rank_scope"] = "diagnostic_only"
                elif is_diagnostic_questions:
                    row["quality_status"] = "diagnostic_question_set"
                    row["rank_scope"] = "diagnostic_only"
                elif is_do_not_promote:
                    row["quality_status"] = exposure_status or "do_not_promote_until_reviewed"
                    row["rank_scope"] = "diagnostic_only"
                elif is_exposed_regression:
                    row["quality_status"] = "exposed_regression"
                    row["rank_scope"] = "diagnostic_only"
                else:
                    row["quality_status"] = "complete" if has_quality else "incomplete_no_judge"
                    row["rank_scope"] = "scoreboard" if has_quality else "diagnostic_only"
                for col in NUMERIC_COLS:
                    if col in row:
                        row[col] = _num(row[col])
                rows.append(row)
    return rows


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _svg_bar(path: Path, rows: list[dict]) -> None:
    top = sorted(rows, key=lambda r: _num(r.get("edd_score")), reverse=True)[:12]
    width = 1100
    row_h = 34
    height = 70 + row_h * max(1, len(top))
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="24" y="34" font-size="22" font-family="Segoe UI, Arial" font-weight="700">EDD score by experiment</text>',
    ]
    x0 = 310
    max_w = 650
    for i, row in enumerate(top):
        y = 62 + i * row_h
        label = html.escape(f"{row.get('suite')} · {row.get('run_label', row.get('experiment'))}")
        score = _num(row.get("edd_score"))
        bar_w = max(2, score / 100 * max_w)
        color = "#2f6fed" if i == 0 else "#6b8fd6"
        lines.append(f'<text x="24" y="{y + 20}" font-size="13" font-family="Segoe UI, Arial">{label}</text>')
        lines.append(f'<rect x="{x0}" y="{y + 4}" width="{bar_w:.1f}" height="20" rx="3" fill="{color}"/>')
        lines.append(f'<text x="{x0 + bar_w + 8:.1f}" y="{y + 20}" font-size="13" font-family="Segoe UI, Arial">{score:.2f}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def _metric_norm(row: dict, metric: str) -> float:
    if metric in {"groundedness_avg", "relevance_avg"}:
        return max(0.0, min(1.0, _num(row.get(metric)) / 5.0))
    if metric == "latency_avg_sec":
        latency = _num(row.get(metric), 30.0)
        if latency <= 8:
            return 1.0
        if latency >= 30:
            return 0.0
        return (30 - latency) / 22
    return max(0.0, min(1.0, _num(row.get(metric))))


def _heat_color(value: float) -> str:
    value = max(0.0, min(1.0, value))
    if value >= 0.9:
        return "#1f9d55"
    if value >= 0.75:
        return "#79b851"
    if value >= 0.55:
        return "#f2c94c"
    if value >= 0.35:
        return "#f59e0b"
    return "#dc2626"


def _svg_heatmap(path: Path, rows: list[dict]) -> None:
    metrics = [
        ("retrieval_coverage_avg", "coverage"),
        ("mrr", "MRR"),
        ("groundedness_avg", "ground"),
        ("relevance_avg", "relevance"),
        ("abstention_accuracy", "abstain"),
        ("latency_avg_sec", "latency"),
    ]
    rows = sorted(rows, key=lambda r: _num(r.get("edd_score")), reverse=True)
    width = 1220
    left = 390
    top = 70
    cell_w = 105
    row_h = 32
    height = top + row_h * max(1, len(rows)) + 40
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="24" y="34" font-size="22" font-family="Segoe UI, Arial" font-weight="700">Metric heatmap</text>',
    ]
    for j, (_, label) in enumerate(metrics):
        lines.append(f'<text x="{left + j * cell_w + 8}" y="58" font-size="12" font-family="Segoe UI, Arial" font-weight="700">{label}</text>')
    for i, row in enumerate(rows):
        y = top + i * row_h
        label = html.escape(f"{row.get('suite')} · {row.get('run_label', row.get('experiment'))}")
        lines.append(f'<text x="24" y="{y + 20}" font-size="12" font-family="Segoe UI, Arial">{label}</text>')
        lines.append(f'<text x="315" y="{y + 20}" font-size="12" font-family="Segoe UI, Arial" font-weight="700">{_num(row.get("edd_score")):.2f}</text>')
        for j, (metric, _) in enumerate(metrics):
            value = _metric_norm(row, metric)
            x = left + j * cell_w
            lines.append(f'<rect x="{x}" y="{y + 5}" width="86" height="20" rx="3" fill="{_heat_color(value)}"/>')
            lines.append(f'<text x="{x + 43}" y="{y + 20}" font-size="11" text-anchor="middle" font-family="Segoe UI, Arial" fill="#111827">{value:.2f}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def _svg_quality_scatter(path: Path, rows: list[dict]) -> None:
    width, height = 920, 620
    left, right, top, bottom = 90, 40, 60, 80
    plot_w = width - left - right
    plot_h = height - top - bottom

    def sx(cov: float) -> float:
        return left + max(0.0, min(1.0, cov)) * plot_w

    def sy(g: float) -> float:
        return top + (1 - max(0.0, min(5.0, g)) / 5.0) * plot_h

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="24" y="34" font-size="22" font-family="Segoe UI, Arial" font-weight="700">Retrieval coverage vs groundedness</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#334155"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#334155"/>',
        f'<text x="{left + plot_w / 2}" y="{height - 24}" font-size="14" text-anchor="middle" font-family="Segoe UI, Arial">retrieval coverage</text>',
        f'<text x="24" y="{top + plot_h / 2}" font-size="14" transform="rotate(-90 24 {top + plot_h / 2})" text-anchor="middle" font-family="Segoe UI, Arial">groundedness</text>',
    ]
    for tick in range(0, 6):
        y = sy(tick)
        lines.append(f'<line x1="{left - 5}" y1="{y}" x2="{left}" y2="{y}" stroke="#334155"/>')
        lines.append(f'<text x="{left - 12}" y="{y + 4}" font-size="11" text-anchor="end" font-family="Segoe UI, Arial">{tick}</text>')
    for tick in [0, 0.25, 0.5, 0.75, 1.0]:
        x = sx(tick)
        lines.append(f'<line x1="{x}" y1="{top + plot_h}" x2="{x}" y2="{top + plot_h + 5}" stroke="#334155"/>')
        lines.append(f'<text x="{x}" y="{top + plot_h + 22}" font-size="11" text-anchor="middle" font-family="Segoe UI, Arial">{tick:.2f}</text>')
    for row in rows:
        suite = row.get("suite", "")
        color = SUITE_COLORS.get(suite, "#64748b")
        x = sx(_num(row.get("retrieval_coverage_avg")))
        y = sy(_num(row.get("groundedness_avg")))
        radius = 5 + _num(row.get("edd_score")) / 20
        label = html.escape(str(row.get("run_label", row.get("experiment", "")))[:26])
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{color}" fill-opacity="0.72" stroke="#111827" stroke-width="0.5"/>')
        lines.append(f'<text x="{x + radius + 4:.1f}" y="{y + 4:.1f}" font-size="10" font-family="Segoe UI, Arial">{label}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def _svg_latency_scatter(path: Path, rows: list[dict]) -> None:
    width, height = 920, 580
    left, right, top, bottom = 90, 40, 60, 80
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_latency = max([_num(r.get("latency_avg_sec")) for r in rows] + [30.0])
    min_latency = min([_num(r.get("latency_avg_sec")) for r in rows] + [0.0])
    min_score = min([_num(r.get("edd_score")) for r in rows] + [60.0])
    max_score = max([_num(r.get("edd_score")) for r in rows] + [100.0])

    def sx(lat: float) -> float:
        denom = max(1.0, max_latency - min_latency)
        return left + (lat - min_latency) / denom * plot_w

    def sy(score: float) -> float:
        denom = max(1.0, max_score - min_score)
        return top + (1 - (score - min_score) / denom) * plot_h

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="24" y="34" font-size="22" font-family="Segoe UI, Arial" font-weight="700">Latency vs EDD score</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#334155"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#334155"/>',
        f'<text x="{left + plot_w / 2}" y="{height - 24}" font-size="14" text-anchor="middle" font-family="Segoe UI, Arial">latency avg sec</text>',
        f'<text x="24" y="{top + plot_h / 2}" font-size="14" transform="rotate(-90 24 {top + plot_h / 2})" text-anchor="middle" font-family="Segoe UI, Arial">EDD score</text>',
    ]
    for row in rows:
        suite = row.get("suite", "")
        color = SUITE_COLORS.get(suite, "#64748b")
        x = sx(_num(row.get("latency_avg_sec")))
        y = sy(_num(row.get("edd_score")))
        label = html.escape(str(row.get("run_label", row.get("experiment", "")))[:28])
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{color}" fill-opacity="0.75" stroke="#111827" stroke-width="0.5"/>')
        lines.append(f'<text x="{x + 11:.1f}" y="{y + 4:.1f}" font-size="10" font-family="Segoe UI, Arial">{label}</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def _suite_best(rows: list[dict]) -> list[dict]:
    best = {}
    for row in rows:
        suite = row.get("suite", "")
        if suite not in best or _num(row.get("edd_score")) > _num(best[suite].get("edd_score")):
            best[suite] = row
    return sorted(best.values(), key=lambda r: r.get("suite", ""))


def _write_md(path: Path, rows: list[dict], score_rows: list[dict], diagnostic_rows: list[dict], best_rows: list[dict]) -> None:
    lines = [
        "# Parallel Eval Summary",
        "",
        "EDD score definition: 20% coverage, 10% hit-all-targets, 15% MRR, 20% groundedness, 20% relevance, 10% abstention accuracy, 5% latency score, minus penalties for false abstention and empty answers.",
        "",
        "Rows missing groundedness/relevance are marked `diagnostic_only` and excluded from rankings and graphs because their EDD score is not comparable with fully judged runs.",
        "",
        f"- Scoreboard rows: {len(score_rows)}",
        f"- Diagnostic-only rows: {len(diagnostic_rows)}",
        "",
        "## Best By Suite",
        "",
        "| suite | run label | experiment | EDD | coverage | MRR | groundedness | relevance | false abstain | empty | latency |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in best_rows:
        lines.append(
            "| {suite} | {run_label} | {experiment} | {edd:.2f} | {cov:.3f} | {mrr:.3f} | {g:.3f} | {r:.3f} | {fa:.3f} | {empty:.3f} | {lat:.3f} |".format(
                suite=row.get("suite", ""),
                run_label=row.get("run_label", ""),
                experiment=row.get("experiment", ""),
                edd=_num(row.get("edd_score")),
                cov=_num(row.get("retrieval_coverage_avg")),
                mrr=_num(row.get("mrr")),
                g=_num(row.get("groundedness_avg")),
                r=_num(row.get("relevance_avg")),
                fa=_num(row.get("false_abstention_rate")),
                empty=_num(row.get("empty_answer_rate")),
                lat=_num(row.get("latency_avg_sec")),
            )
        )
    lines.extend(["", "## Top Experiments", ""])
    lines.extend([
        "| rank | suite | run label | experiment | EDD | coverage | MRR | groundedness | relevance | false abstain | empty | latency |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for idx, row in enumerate(sorted(score_rows, key=lambda r: _num(r.get("edd_score")), reverse=True)[:15], 1):
        lines.append(
            "| {idx} | {suite} | {run_label} | {experiment} | {edd:.2f} | {cov:.3f} | {mrr:.3f} | {g:.3f} | {r:.3f} | {fa:.3f} | {empty:.3f} | {lat:.3f} |".format(
                idx=idx,
                suite=row.get("suite", ""),
                run_label=row.get("run_label", ""),
                experiment=row.get("experiment", ""),
                edd=_num(row.get("edd_score")),
                cov=_num(row.get("retrieval_coverage_avg")),
                mrr=_num(row.get("mrr")),
                g=_num(row.get("groundedness_avg")),
                r=_num(row.get("relevance_avg")),
                fa=_num(row.get("false_abstention_rate")),
                empty=_num(row.get("empty_answer_rate")),
                lat=_num(row.get("latency_avg_sec")),
            )
        )
    if diagnostic_rows:
        lines.extend(["", "## Diagnostic-Only Rows", ""])
        lines.extend([
            "| suite | run label | experiment | EDD | coverage | MRR | abstention | latency | reason |",
            "|---|---|---|---:|---:|---:|---:|---:|---|",
        ])
        for row in sorted(diagnostic_rows, key=lambda r: _num(r.get("edd_score")), reverse=True):
            lines.append(
                "| {suite} | {run_label} | {experiment} | {edd:.2f} | {cov:.3f} | {mrr:.3f} | {abstain:.3f} | {lat:.3f} | {reason} |".format(
                    suite=row.get("suite", ""),
                    run_label=row.get("run_label", ""),
                    experiment=row.get("experiment", ""),
                    edd=_num(row.get("edd_score")),
                    cov=_num(row.get("retrieval_coverage_avg")),
                    mrr=_num(row.get("mrr")),
                    abstain=_num(row.get("abstention_accuracy")),
                    lat=_num(row.get("latency_avg_sec")),
                    reason=row.get("quality_status", ""),
                )
            )
    lines.extend([
        "",
        "## Visuals",
        "",
        "![EDD score graph](edd_score.svg)",
        "",
        "![Metric heatmap](metric_heatmap.svg)",
        "",
        "![Retrieval quality scatter](quality_vs_retrieval.svg)",
        "",
        "![Latency vs EDD](latency_vs_edd.svg)",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()
    run_dir = Path(args.run_dir)
    rows = _read_rows(run_dir)
    rows = sorted(rows, key=lambda r: _num(r.get("edd_score")), reverse=True)
    score_rows = [row for row in rows if row.get("quality_status") == "complete"]
    diagnostic_rows = [row for row in rows if row.get("quality_status") != "complete"]
    best_rows = _suite_best(score_rows)

    summary_dir = run_dir / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(summary_dir / "summary.csv", rows)
    (summary_dir / "summary.json").write_text(
        json.dumps(
            {
                "rows": rows,
                "scoreboard_rows": score_rows,
                "diagnostic_only_rows": diagnostic_rows,
                "best_by_suite": best_rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    _svg_bar(summary_dir / "edd_score.svg", score_rows)
    _svg_heatmap(summary_dir / "metric_heatmap.svg", score_rows)
    _svg_quality_scatter(summary_dir / "quality_vs_retrieval.svg", score_rows)
    _svg_latency_scatter(summary_dir / "latency_vs_edd.svg", score_rows)
    _write_md(summary_dir / "summary.md", rows, score_rows, diagnostic_rows, best_rows)
    print(
        json.dumps(
            {
                "rows": len(rows),
                "scoreboard_rows": len(score_rows),
                "diagnostic_only_rows": len(diagnostic_rows),
                "summary": str(summary_dir / "summary.md"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
