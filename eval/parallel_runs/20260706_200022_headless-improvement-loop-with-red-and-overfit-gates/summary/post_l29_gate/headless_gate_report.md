# Headless Red/Overfit Gate Report

- created_at: `2026-07-06T21:18:10`
- loop rows checked: `30`
- promotable_count: `2`
- measurement_correction_count: `4`
- diagnostic_or_qualitative_count: `19`
- candidate_only_count: `2`
- human_quality_avg: `None`
- evidence_safety_score_avg: `None`
- exposure_registry_entries: `12`

## Current Gate Decision

- best promotable evidence: `L25` `v4_first_baseline_top8` EDD `97.41`
- best corrected/measurement point: `L29` `v4_concise_verified_same_answers_recomputed` EDD `96.42`; do not call this model improvement by itself.
- active red flags: `latency_risk, metric_saturation_risk, near_ceiling_score, needs_scored_validation, no_judge_not_performance, not_model_improvement, rejected_by_decision, targeted_or_reused_case`

## Row Labels

| loop | state | EDD | promotion | flags |
|---|---|---:|---|---|
| `L0` | first_validation_evidence | 89.69 | True | metric_saturation_risk, latency_risk |
| `L1` | measurement_correction | 96.36 | False | not_model_improvement, near_ceiling_score, metric_saturation_risk, latency_risk |
| `L2` | scored_evidence | 91.41 | False | targeted_or_reused_case, latency_risk, rejected_by_decision |
| `L3` | measurement_correction | 94.74 | False | not_model_improvement, latency_risk, rejected_by_decision |
| `L4` | diagnostic_only |  | False |  |
| `L5` | diagnostic_only |  | False |  |
| `L6` | diagnostic_only |  | False | targeted_or_reused_case |
| `L7` | diagnostic_only |  | False |  |
| `L8` | diagnostic_only |  | False |  |
| `L9` | diagnostic_only |  | False | targeted_or_reused_case, no_judge_not_performance, rejected_by_decision |
| `L10` | diagnostic_only |  | False | targeted_or_reused_case, no_judge_not_performance |
| `L11` | diagnostic_only |  | False |  |
| `L12` | qualitative_evidence |  | False |  |
| `L13` | candidate_only |  | False | needs_scored_validation |
| `L14` | diagnostic_only |  | False |  |
| `L15` | diagnostic_only |  | False |  |
| `L16` | candidate_only |  | False | needs_scored_validation |
| `L17` | diagnostic_only |  | False |  |
| `L18` | diagnostic_only |  | False |  |
| `L19` | diagnostic_only |  | False |  |
| `L20` | diagnostic_only |  | False | rejected_by_decision |
| `L21` | diagnostic_only |  | False |  |
| `L22` | diagnostic_only |  | False | rejected_by_decision |
| `L23` | diagnostic_only |  | False |  |
| `L24` | diagnostic_only |  | False |  |
| `L25` | first_validation_evidence | 97.41 | True | near_ceiling_score, metric_saturation_risk |
| `L26` | scored_evidence | 97.12 | False | targeted_or_reused_case, near_ceiling_score, rejected_by_decision |
| `L27` | scored_evidence | 95.00 | False | near_ceiling_score, metric_saturation_risk, latency_risk, rejected_by_decision |
| `L28` | measurement_correction | 86.42 | False | not_model_improvement, metric_saturation_risk, latency_risk |
| `L29` | measurement_correction | 96.42 | False | not_model_improvement, near_ceiling_score, metric_saturation_risk, latency_risk, rejected_by_decision |

## Exposure Registry

- strict candidate files: `questions_v4_draft_noapi.json, questions_v4_frozen_first_run.json`
- spent/diagnostic files: `questions_qv3_010_targeted.json, questions_v2.json, questions_v2_compare_probe.json, questions_v2_groundedness_probe.json, questions_v2_holdout.json, questions_v2_holdout_failure_probe.json`

## Next Recommendations

1. Create a fresh validation cohort before claiming generalization beyond the current exposed sets. `no_api_question_generation_then_paid_eval`
   - reason: The current v2/v3/v4 sets have now informed diagnostics, scoring, or candidate rejection.
2. Review L25 answers for human readability and investigate the slow v4 cases. `mostly_no_api_review`
   - reason: L25 is the current best evidence, while later same-set probes did not beat it.
