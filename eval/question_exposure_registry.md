# Question Exposure Registry

- created_at: `2026-07-07T14:02:25`

| file | questions | orgs | status | claim use |
|---|---:|---:|---|---|
| `questions.example.json` | 9 | 0 | example_only | do_not_use_for_performance |
| `questions.json` | 10 | 5 | legacy_exposed | baseline_development_only |
| `questions_l106_nonqv8_guard_generalization_diagnostic_draft.json` | 7 | 0 | draft_nonqv8_guard_generalization_after_l105 | diagnostic_only |
| `questions_l108_nonqv8_grounded_guard_field_diagnostic_frozen.json` | 8 | 4 | grounded_nonqv8_guard_field_diagnostic_after_l105 | diagnostic_only |
| `questions_l109_nonqv8_grounded_guard_field_scored_diagnostic.json` | 8 | 4 | scored_copy_nonqv8_guard_field_diagnostic_after_l108 | diagnostic_only |
| `questions_qv3_010_targeted.json` | 1 | 1 | targeted_single_case_exposed | diagnostic_only |
| `questions_v2.json` | 25 | 27 | full_v2_exposed | development_and_regression_only |
| `questions_v2_compare_probe.json` | 3 | 11 | diagnostic_exposed | diagnostic_only |
| `questions_v2_groundedness_probe.json` | 3 | 4 | diagnostic_exposed | diagnostic_only |
| `questions_v2_holdout.json` | 7 | 9 | holdout_spent | first_holdout_only |
| `questions_v2_holdout_failure_probe.json` | 3 | 6 | targeted_failure_probe_exposed | diagnostic_only |
| `questions_v2_tune.json` | 18 | 22 | tune_exposed | tuning_score_only |
| `questions_v3_validation.json` | 12 | 12 | first_validation_exposed | first_run_and_regression_only |
| `questions_v4_draft_noapi.json` | 10 | 10 | draft_exposed_by_v4_first_run | development_and_regression_only |
| `questions_v4_frozen_first_run.json` | 10 | 10 | first_validation_exposed | first_run_and_regression_only |
| `questions_v5_adversarial_draft.json` | 14 | 13 | draft_exposed_by_v5_first_run | development_and_regression_only |
| `questions_v5_adversarial_frozen_first_run.json` | 14 | 13 | first_validation_exposed | first_run_and_regression_only |
| `questions_v6_l38_safety_retry.json` | 2 | 1 | targeted_failure_probe_exposed | diagnostic_only |
| `questions_v6_l39_goyang_order_depth_probe.json` | 1 | 1 | targeted_failure_probe_exposed | diagnostic_only |
| `questions_v6_l61_ambiguous_title_abstention_probe.json` | 1 | 0 | targeted_failure_probe_exposed | diagnostic_only |
| `questions_v6_l65_uicc_project_focus_probe.json` | 1 | 1 | targeted_failure_probe_exposed | diagnostic_only |
| `questions_v6_metamorphic_draft.json` | 10 | 7 | draft_exposed_by_v6_first_run | development_and_regression_only |
| `questions_v6_metamorphic_frozen_first_run.json` | 10 | 7 | first_validation_exposed | first_run_and_regression_only |
| `questions_v7_l83_sensitive_guard_probe.json` | 1 | 1 | targeted_failure_probe_exposed | diagnostic_only |
| `questions_v7_l88_plain_language_probe.json` | 1 | 1 | targeted_failure_probe_exposed | diagnostic_only |
| `questions_v7_l94_sensitive_preempt_probe.json` | 2 | 2 | targeted_failure_probe_exposed | diagnostic_only |
| `questions_v7_source_exposed_prompt_diagnostic_draft.json` | 12 | 10 | source_exposed_prompt_diagnostic_draft | diagnostic_only |
| `questions_v7_source_exposed_prompt_diagnostic_frozen.json` | 12 | 10 | source_exposed_prompt_diagnostic_frozen | diagnostic_only |
| `questions_v8_deadline_semi_fresh_diagnostic_frozen.json` | 10 | 8 | semi_fresh_deadline_diagnostic | diagnostic_only |
| `questions_v8_l100_latency_tail_probe.json` | 5 | 4 | targeted_latency_tail_probe_exposed | diagnostic_only |
| `questions_v8_l102_award_result_probe.json` | 1 | 1 | targeted_award_result_probe_exposed | diagnostic_only |
| `questions_v8_l104_victim_story_probe.json` | 1 | 1 | targeted_sensitive_story_probe_exposed | diagnostic_only |
| `questions_v9_source_inspected_mini_diagnostic_frozen.json` | 5 | 6 | source_inspected_v9_mini_diagnostic_frozen | diagnostic_only |

## Notes

- `questions.example.json`: Example seed file, not a maintained validation suite.
- `questions.json`: Initial development/evaluation set used before later v2/v3 loops.
- `questions_l106_nonqv8_guard_generalization_diagnostic_draft.json`: Non-qv8 guard-generalization draft cases designed after L105 saturation; use for fixture/design only until grounded target projects are assigned and frozen.
- `questions_l108_nonqv8_grounded_guard_field_diagnostic_frozen.json`: Concrete corpus-backed non-qv8 guard and field-scoring diagnostic set derived after L105/L106; not strict validation because failure families were designed from prior insights.
- `questions_l109_nonqv8_grounded_guard_field_scored_diagnostic.json`: Same source-exposed L108 question intents with stricter field expectations and scorer calibration after L108 inspection; compares measurement/guard repair only, not fresh validation.
- `questions_qv3_010_targeted.json`: Single known qv3_010 targeted rerun set.
- `questions_v2.json`: Used for audit/improvement planning and partial real RAG smoke.
- `questions_v2_compare_probe.json`: Probe set for compare behavior.
- `questions_v2_groundedness_probe.json`: Probe set for groundedness/source-scope behavior.
- `questions_v2_holdout.json`: First holdout was inspected and targeted fixes followed, so later reruns are not strict held-out evidence.
- `questions_v2_holdout_failure_probe.json`: Built from known holdout failures.
- `questions_v2_tune.json`: Used for tuning champion candidates; not strict validation.
- `questions_v3_validation.json`: Used for L0-L3 scored runs and later L4-L16 diagnostics.
- `questions_v4_draft_noapi.json`: Draft source for the v4 frozen first run; v4 answers and candidate failures have now been inspected.
- `questions_v4_frozen_first_run.json`: Frozen v4 first run was executed as L25 and later probes used the same set; do not call future reruns fresh validation.
- `questions_v5_adversarial_draft.json`: Draft source for the v5 adversarial first run; L30 answers and failures have now been inspected.
- `questions_v5_adversarial_frozen_first_run.json`: Frozen v5 first run was executed as L30 in the adversarial loop; later L31-L34 repairs/recomputes are exposed regression only.
- `questions_v6_l38_safety_retry.json`: Built from known v6 abstention failures qv6_004/qv6_010 after L37 inspection.
- `questions_v6_l39_goyang_order_depth_probe.json`: Single known v6 metamorphic failure qv6_007 used for top_k and alias diagnostics.
- `questions_v6_l61_ambiguous_title_abstention_probe.json`: Single known v6 qv6_010 ambiguity/refusal case used after L60 inspection.
- `questions_v6_l65_uicc_project_focus_probe.json`: Single known v6 qv6_001 same-issuer project-focus case used after L64 inspection.
- `questions_v6_metamorphic_draft.json`: Draft source for the v6 metamorphic/property first run; L37 answers and failures have now been inspected.
- `questions_v6_metamorphic_frozen_first_run.json`: Frozen v6 first run was executed as L37; later targeted retries on L38-L40 are diagnostic, not fresh validation.
- `questions_v7_l83_sensitive_guard_probe.json`: Single qv7_006 source-exposed case rerun after L82 sensitive/refusal-tail guard; measures repair only.
- `questions_v7_l88_plain_language_probe.json`: Single qv7_009 source-exposed case rerun after L87 plain-language over-structure flag; measures format repair only.
- `questions_v7_l94_sensitive_preempt_probe.json`: Two source-exposed sensitive/forbidden-info cases rerun after preemptive abstention guard; measures latency/cost repair only.
- `questions_v7_source_exposed_prompt_diagnostic_draft.json`: Fresh prompt forms over already-exposed corpus projects; useful for diagnostics but not strict validation.
- `questions_v7_source_exposed_prompt_diagnostic_frozen.json`: Frozen diagnostic copy of v7 source-exposed prompts; run results must not be reported as fresh held-out validation.
- `questions_v8_deadline_semi_fresh_diagnostic_frozen.json`: Codex-generated semi-fresh/source-exposed mixed diagnostic set created after prior loop insights; useful for deadline stress evidence but not strict held-out validation.
- `questions_v8_l100_latency_tail_probe.json`: Five qv8 high-latency cases selected after L98/L99 inspection; measures latency repair only and must not be reported as fresh validation.
- `questions_v8_l102_award_result_probe.json`: Single qv8_a11 unsupported final evaluation score / selected vendor probe after L101 inspection; measures refusal-boundary repair only.
- `questions_v8_l104_victim_story_probe.json`: Single qv8_a12 victim-story fabrication probe after L103 latency inspection; measures sensitive-story preempt latency repair only.
- `questions_v9_source_inspected_mini_diagnostic_frozen.json`: Prompt-fresh mini-set frozen before first answer run but generated from local corpus/source inspection after prior loop insights; useful for guard, field-score, and latency evidence but not strict held-out validation.
