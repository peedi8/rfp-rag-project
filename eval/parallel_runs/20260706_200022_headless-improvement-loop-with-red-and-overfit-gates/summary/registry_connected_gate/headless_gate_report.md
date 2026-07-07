# Headless Red/Overfit Gate Report

- created_at: `2026-07-06T20:16:01`
- loop rows checked: `19`
- promotable_count: `1`
- measurement_correction_count: `2`
- diagnostic_or_qualitative_count: `13`
- candidate_only_count: `2`
- human_quality_avg: `3.62`
- evidence_safety_score_avg: `3.47`
- exposure_registry_entries: `12`

## Current Gate Decision

- best promotable evidence: `L0` `v3_first_validation_top8_raw` EDD `89.69`
- best corrected/measurement point: `L1` `v3_top8_same_answers_recomputed` EDD `96.36`; do not call this model improvement by itself.
- active red flags: `latency_risk, metric_saturation_risk, near_ceiling_score, needs_scored_validation, no_judge_not_performance, not_model_improvement, targeted_or_reused_case, human_quality_gap, evidence_safety_gap`

## Row Labels

| loop | state | EDD | promotion | flags |
|---|---|---:|---|---|
| `L0` | first_validation_evidence | 89.69 | True | metric_saturation_risk, latency_risk |
| `L1` | measurement_correction | 96.36 | False | not_model_improvement, near_ceiling_score, metric_saturation_risk, latency_risk |
| `L2` | scored_evidence | 91.41 | False | targeted_or_reused_case, latency_risk |
| `L3` | measurement_correction | 94.74 | False | not_model_improvement, latency_risk |
| `L4` | diagnostic_only |  | False |  |
| `L5` | diagnostic_only |  | False |  |
| `L6` | diagnostic_only |  | False | targeted_or_reused_case |
| `L7` | diagnostic_only |  | False |  |
| `L8` | diagnostic_only |  | False |  |
| `L9` | diagnostic_only |  | False | targeted_or_reused_case, no_judge_not_performance |
| `L10` | diagnostic_only |  | False | targeted_or_reused_case, no_judge_not_performance |
| `L11` | diagnostic_only |  | False |  |
| `L12` | qualitative_evidence |  | False |  |
| `L13` | candidate_only |  | False | needs_scored_validation |
| `L14` | diagnostic_only |  | False |  |
| `L15` | diagnostic_only |  | False |  |
| `L16` | candidate_only |  | False | needs_scored_validation |
| `L17` | diagnostic_only |  | False |  |
| `L18` | diagnostic_only |  | False |  |

## Exposure Registry

- strict candidate files: `questions_v4_draft_noapi.json, questions_v4_frozen_first_run.json`
- spent/diagnostic files: `questions_qv3_010_targeted.json, questions_v2.json, questions_v2_compare_probe.json, questions_v2_groundedness_probe.json, questions_v2_holdout.json, questions_v2_holdout_failure_probe.json`

## Next Recommendations

1. Run blind judge calibration before trusting another near-ceiling judge score. `optional_paid_judge`
   - reason: Existing loop points include near-ceiling automated scores plus planted pass/fail calibration artifacts.
2. Run a small scored prompt_sweep comparing prompt_report_ready against existing prompt variants. `paid_judge_small`
   - reason: report_ready is candidate-only and must not be promoted from static checks.
3. Create a fresh validation cohort before claiming generalization beyond v3. `no_api_question_generation_then_paid_eval`
   - reason: Existing v2 holdout/v3 sets have already informed targeted fixes and diagnostics.
