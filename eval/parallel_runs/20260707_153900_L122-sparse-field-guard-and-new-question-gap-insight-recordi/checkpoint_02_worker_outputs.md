# checkpoint_02_worker_outputs.md

Pending.
# Checkpoint 02 - Worker Outputs

## Collected

- `worker_outputs/sparse_guard_design.contract.json`
  - accepted with correction: the design was right about field-level scoring, but the actual source basis must be raw HWP/PDF text rather than CSV-only text.
- `worker_outputs/secondary_variant_red_review.contract.json`
  - accepted: secondary variants must be diagnostic-only and excluded from ordinary EDD/champion rows.
- `worker_outputs/report_log_review.local_contract.json`
  - accepted local fallback: the report/log review worker could not be spawned because the agent thread limit was reached.

## Important Findings

- `questions_l121_selected_project_secondary_variants.json` currently marks all secondary rows as `ordinary_edd_candidate=true` and includes `EDD` in `metric_routes`, so downstream aggregation needs an explicit exclusion or override.
- The first CSV-only sparse-field view found `4` visible groups and `27` not-found groups, but raw-file inspection found `31` visible groups and `0` not-found groups.
- Therefore the ADD secondary technical seed is not a strong sparse-field seed when raw source text is available. It is better evidence for source-basis mismatch and scoreboard contamination risk.
