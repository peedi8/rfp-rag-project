# checkpoint_02_worker_outputs.md

## Worker Proposal Outputs

- `fresh_question_design`: proposed a 5-question v9 source-inspected mini-set with supported extraction, comparison, unsupported final-result, and sensitive fabrication cases.
- `fresh_red_gate`: required diagnostic-only labeling unless a truly untouched source pool and pre-run freeze are documented.
- `latency_profile`: proposed same-cohort L112 top_k profiling as latency-only evidence, with L112 top8 latency `7.184s` as the baseline.
- `report_update`: proposed the cause/result/insight/next-basis recording structure.

## Executed Outputs

- `l113_l112_same_cohort_latency_topk_sweep_nojudge_topk_sweep.json`
  - top5 latency `8.598s`, false abstention `0.0`, field issues `{}`.
  - top8 same-run control latency `8.369s`, false abstention `0.0`, field issues `{}`.
  - top12 latency `14.890s`, false abstention `0.0`, field issues `{}`, with q002 tail `71.44s`.
- `l114_v9_source_inspected_first_execution_judged_baseline_default.json`
  - raw EDD `93.42`, abstention accuracy `0.5`, latency `14.934s`, cost `$0.067370`.
- `analysis/l115_v9_saved_recompute_after_childcare_detector`
  - saved-answer recompute EDD `98.42`, abstention accuracy `1.0`.
  - Changed only q005 abstention detection from `false` to `true`.

All worker files are proposal/evidence outputs. Final merges and labels were decided by the orchestrator.
