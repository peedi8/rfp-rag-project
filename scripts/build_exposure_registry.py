"""Build a question-set exposure registry for RFP-RAG eval loops."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


STATUS_BY_FILE = {
    "questions.example.json": {
        "status": "example_only",
        "claim_use": "do_not_use_for_performance",
        "reason": "Example seed file, not a maintained validation suite.",
    },
    "questions.json": {
        "status": "legacy_exposed",
        "claim_use": "baseline_development_only",
        "reason": "Initial development/evaluation set used before later v2/v3 loops.",
    },
    "questions_v2.json": {
        "status": "full_v2_exposed",
        "claim_use": "development_and_regression_only",
        "reason": "Used for audit/improvement planning and partial real RAG smoke.",
    },
    "questions_v2_tune.json": {
        "status": "tune_exposed",
        "claim_use": "tuning_score_only",
        "reason": "Used for tuning champion candidates; not strict validation.",
    },
    "questions_v2_holdout.json": {
        "status": "holdout_spent",
        "claim_use": "first_holdout_only",
        "reason": "First holdout was inspected and targeted fixes followed, so later reruns are not strict held-out evidence.",
    },
    "questions_v2_compare_probe.json": {
        "status": "diagnostic_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Probe set for compare behavior.",
    },
    "questions_v2_groundedness_probe.json": {
        "status": "diagnostic_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Probe set for groundedness/source-scope behavior.",
    },
    "questions_v2_holdout_failure_probe.json": {
        "status": "targeted_failure_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Built from known holdout failures.",
    },
    "questions_v3_validation.json": {
        "status": "first_validation_exposed",
        "claim_use": "first_run_and_regression_only",
        "reason": "Used for L0-L3 scored runs and later L4-L16 diagnostics.",
    },
    "questions_qv3_010_targeted.json": {
        "status": "targeted_single_case_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Single known qv3_010 targeted rerun set.",
    },
    "questions_v4_draft_noapi.json": {
        "status": "draft_exposed_by_v4_first_run",
        "claim_use": "development_and_regression_only",
        "reason": "Draft source for the v4 frozen first run; v4 answers and candidate failures have now been inspected.",
    },
    "questions_v4_frozen_first_run.json": {
        "status": "first_validation_exposed",
        "claim_use": "first_run_and_regression_only",
        "reason": "Frozen v4 first run was executed as L25 and later probes used the same set; do not call future reruns fresh validation.",
    },
    "questions_v5_adversarial_draft.json": {
        "status": "draft_exposed_by_v5_first_run",
        "claim_use": "development_and_regression_only",
        "reason": "Draft source for the v5 adversarial first run; L30 answers and failures have now been inspected.",
    },
    "questions_v5_adversarial_frozen_first_run.json": {
        "status": "first_validation_exposed",
        "claim_use": "first_run_and_regression_only",
        "reason": "Frozen v5 first run was executed as L30 in the adversarial loop; later L31-L34 repairs/recomputes are exposed regression only.",
    },
    "questions_v6_metamorphic_draft.json": {
        "status": "draft_exposed_by_v6_first_run",
        "claim_use": "development_and_regression_only",
        "reason": "Draft source for the v6 metamorphic/property first run; L37 answers and failures have now been inspected.",
    },
    "questions_v6_metamorphic_frozen_first_run.json": {
        "status": "first_validation_exposed",
        "claim_use": "first_run_and_regression_only",
        "reason": "Frozen v6 first run was executed as L37; later targeted retries on L38-L40 are diagnostic, not fresh validation.",
    },
    "questions_v6_l38_safety_retry.json": {
        "status": "targeted_failure_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Built from known v6 abstention failures qv6_004/qv6_010 after L37 inspection.",
    },
    "questions_v6_l39_goyang_order_depth_probe.json": {
        "status": "targeted_failure_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Single known v6 metamorphic failure qv6_007 used for top_k and alias diagnostics.",
    },
    "questions_v6_l61_ambiguous_title_abstention_probe.json": {
        "status": "targeted_failure_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Single known v6 qv6_010 ambiguity/refusal case used after L60 inspection.",
    },
    "questions_v6_l65_uicc_project_focus_probe.json": {
        "status": "targeted_failure_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Single known v6 qv6_001 same-issuer project-focus case used after L64 inspection.",
    },
    "questions_v7_source_exposed_prompt_diagnostic_draft.json": {
        "status": "source_exposed_prompt_diagnostic_draft",
        "claim_use": "diagnostic_only",
        "reason": "Fresh prompt forms over already-exposed corpus projects; useful for diagnostics but not strict validation.",
    },
    "questions_v7_source_exposed_prompt_diagnostic_frozen.json": {
        "status": "source_exposed_prompt_diagnostic_frozen",
        "claim_use": "diagnostic_only",
        "reason": "Frozen diagnostic copy of v7 source-exposed prompts; run results must not be reported as fresh held-out validation.",
    },
    "questions_v7_l83_sensitive_guard_probe.json": {
        "status": "targeted_failure_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Single qv7_006 source-exposed case rerun after L82 sensitive/refusal-tail guard; measures repair only.",
    },
    "questions_v7_l88_plain_language_probe.json": {
        "status": "targeted_failure_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Single qv7_009 source-exposed case rerun after L87 plain-language over-structure flag; measures format repair only.",
    },
    "questions_v7_l94_sensitive_preempt_probe.json": {
        "status": "targeted_failure_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Two source-exposed sensitive/forbidden-info cases rerun after preemptive abstention guard; measures latency/cost repair only.",
    },
    "questions_v8_deadline_semi_fresh_diagnostic_frozen.json": {
        "status": "semi_fresh_deadline_diagnostic",
        "claim_use": "diagnostic_only",
        "reason": "Codex-generated semi-fresh/source-exposed mixed diagnostic set created after prior loop insights; useful for deadline stress evidence but not strict held-out validation.",
    },
    "questions_v8_l100_latency_tail_probe.json": {
        "status": "targeted_latency_tail_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Five qv8 high-latency cases selected after L98/L99 inspection; measures latency repair only and must not be reported as fresh validation.",
    },
    "questions_v8_l102_award_result_probe.json": {
        "status": "targeted_award_result_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Single qv8_a11 unsupported final evaluation score / selected vendor probe after L101 inspection; measures refusal-boundary repair only.",
    },
    "questions_v8_l104_victim_story_probe.json": {
        "status": "targeted_sensitive_story_probe_exposed",
        "claim_use": "diagnostic_only",
        "reason": "Single qv8_a12 victim-story fabrication probe after L103 latency inspection; measures sensitive-story preempt latency repair only.",
    },
    "questions_l106_nonqv8_guard_generalization_diagnostic_draft.json": {
        "status": "draft_nonqv8_guard_generalization_after_l105",
        "claim_use": "diagnostic_only",
        "reason": "Non-qv8 guard-generalization draft cases designed after L105 saturation; use for fixture/design only until grounded target projects are assigned and frozen.",
    },
    "questions_l108_nonqv8_grounded_guard_field_diagnostic_frozen.json": {
        "status": "grounded_nonqv8_guard_field_diagnostic_after_l105",
        "claim_use": "diagnostic_only",
        "reason": "Concrete corpus-backed non-qv8 guard and field-scoring diagnostic set derived after L105/L106; not strict validation because failure families were designed from prior insights.",
    },
    "questions_l109_nonqv8_grounded_guard_field_scored_diagnostic.json": {
        "status": "scored_copy_nonqv8_guard_field_diagnostic_after_l108",
        "claim_use": "diagnostic_only",
        "reason": "Same source-exposed L108 question intents with stricter field expectations and scorer calibration after L108 inspection; compares measurement/guard repair only, not fresh validation.",
    },
    "questions_v9_source_inspected_mini_diagnostic_frozen.json": {
        "status": "source_inspected_v9_mini_diagnostic_frozen",
        "claim_use": "diagnostic_only",
        "reason": "Prompt-fresh mini-set frozen before first answer run but generated from local corpus/source inspection after prior loop insights; useful for guard, field-score, and latency evidence but not strict held-out validation.",
    },
}


def _read_questions(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data if isinstance(data, list) else []


def build_registry(eval_dir: Path) -> dict[str, Any]:
    entries = []
    for path in sorted(eval_dir.glob("questions*.json")):
        if path.name.endswith(".manifest.json"):
            continue
        questions = _read_questions(path)
        meta = STATUS_BY_FILE.get(path.name, {
            "status": "unknown_needs_review",
            "claim_use": "do_not_promote_until_reviewed",
            "reason": "No registry rule has been assigned yet.",
        })
        qids = [str(q.get("id", "")) for q in questions if q.get("id")]
        orgs = sorted({org for q in questions for org in (q.get("target_orgs") or [])})
        entries.append({
            "file": str(path),
            "name": path.name,
            "question_count": len(questions),
            "target_org_count": len(orgs),
            "sample_ids": qids[:5],
            "status": meta["status"],
            "claim_use": meta["claim_use"],
            "reason": meta["reason"],
        })
    return {
        "schema": "rfp_rag_question_exposure_registry.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "entries": entries,
        "rules": {
            "strict_validation": "Only a frozen, uninspected first run can support strict validation.",
            "spent_holdout": "If failures are inspected and targeted fixes are made, later same-set reruns are not held-out evidence.",
            "diagnostic": "Probe, no-judge, or targeted question files can explain causes but not final performance.",
            "draft": "Draft question files become exposed once answers, retrieval chunks, or failure causes are inspected.",
        },
    }


def write_markdown(path: Path, registry: dict[str, Any]) -> None:
    lines = [
        "# Question Exposure Registry",
        "",
        f"- created_at: `{registry['created_at']}`",
        "",
        "| file | questions | orgs | status | claim use |",
        "|---|---:|---:|---|---|",
    ]
    for e in registry["entries"]:
        lines.append(
            f"| `{e['name']}` | {e['question_count']} | {e['target_org_count']} | "
            f"{e['status']} | {e['claim_use']} |"
        )
    lines.extend(["", "## Notes", ""])
    for e in registry["entries"]:
        lines.append(f"- `{e['name']}`: {e['reason']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    eval_dir = Path("eval")
    registry = build_registry(eval_dir)
    json_path = eval_dir / "question_exposure_registry.json"
    md_path = eval_dir / "question_exposure_registry.md"
    json_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(md_path, registry)
    print(json.dumps({"json": str(json_path), "md": str(md_path), "entries": len(registry["entries"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
