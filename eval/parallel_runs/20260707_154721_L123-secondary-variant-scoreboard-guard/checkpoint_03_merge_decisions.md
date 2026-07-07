# checkpoint_03_merge_decisions.md

Pending.
# Checkpoint 03 - Merge Decisions

## Accepted

- Added a secondary-variant guard to `scripts/aggregate_parallel_eval.py`.
- The guard detects secondary variant question files by filename markers and by payload markers such as `variant_claim`, secondary `diagnostic_label`, or `promotion_blocker`.
- The guard sets `quality_status=diagnostic_secondary_variant` and `rank_scope=diagnostic_only` before normal scoreboard eligibility rules.

## Verification

- Synthetic row had complete quality metrics and `edd_score=99.99`.
- Synthetic row pointed at `questions_l121_selected_project_secondary_variants.json`.
- Aggregate output:
  - rows: `1`
  - scoreboard_rows: `0`
  - diagnostic_only_rows: `1`

## Decision

This is an aggregation hygiene fix, not an answer-quality or EDD improvement point.
