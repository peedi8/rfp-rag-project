# checkpoint_03_merge_decisions.md

## Merge Decisions

- Accepted with modification: `fresh_question_design`.
  - The v9 question set was created and frozen before answer execution.
  - The red-gate caveat was applied, so the set is `diagnostic_only`, not strict held-out validation.
- Accepted: `fresh_red_gate`.
  - Registry label: `source_inspected_v9_mini_diagnostic_frozen`.
  - Claim use: `diagnostic_only`.
- Accepted: `latency_profile`.
  - L113 was executed as same-cohort latency-only profiling.
  - No top_k candidate beat L112 latency `7.184s`, so no speed candidate was promoted.
- Accepted: `report_update`.
  - L113-L115 were added to `eval/experiment_log.md`, `eval/next_improvement_tasks.md`, and `업무일지.md`.

## Final Decisions

- Keep L112 top8 as the current latency-safe diagnostic baseline for the L109/L112 8-case cohort.
- Record L114 raw separately: EDD `93.42`, abstention accuracy `0.5`, latency `14.934s`.
- Record L115 as measurement correction only: EDD `98.42`, abstention accuracy `1.0`.
- Do not promote v9 to strict validation.
- Do not call any future same-v9 targeted rerun validation.
- Investigate q001 as a high-judge-score but weak-user-usefulness case caused by possible CSV-only metadata expectation.
