# L45 Budget And Over-Answer Gate Report

L46 correction note: the L45 dry-run skip showed that the new branch could write a budget event, but it was not the right proof for hard-stop behavior because dry-run has no model cost. L46 supersedes the budget proof by verifying a non-dry preflight skip and a separate dry-run-not-skipped path.

## Summary

- Added preflight hard-stop budget checks to `scripts/run_experiment_worker.py`.
- Added deterministic post-refusal answer quality flags to `scripts/evaluate.py`.
- Verified both gates without launching paid model calls.
- Kept the scoreboard unchanged: L37 remains the only strict v6 score row.

## Budget Gate

New worker arguments:

- `--budget-cap-usd`
- `--hard-stop-usd`
- `--starting-spent-usd`
- `--preflight-case-estimate-usd`

Dry-run verification used a deliberately tiny hard stop:

`--hard-stop-usd 0.001 --preflight-case-estimate-usd 0.01`

L45 result:

- `wrote_rows=0`
- `budget_events=1`
- `skipped_preflight_budget=1`
- no API calls launched
- no scoreboard pollution after aggregation

L46 superseding result:

- non-dry preflight skip: `status=blocked`, `budget_gate_all_skipped=true`, `observed_cost_usd=0`
- dry-run with `hard_stop=0`: `wrote_rows=1`, `skipped_preflight_budget=0`, `observed_cost_usd=0`

## Over-Answer Gate

Saved L38 answers were checked with the new deterministic quality rule.

- `qv6_004_unavailable_procurement_result_university_finance`: no new quality issue
- `qv6_010_generic_fragment_unidentifiable_abstain`: `ambiguous_identifier_refusal_with_excessive_candidate_summary`

This keeps the binary abstention metric honest: an answer can refuse correctly and still be too verbose or too suggestive afterward.

## Gate Decision

L45 is not a new performance score. It is an execution safety and quality-filter step.

Next broad paid v7/v8/v9 runs should remain closed until qv6_007 has a claim-preservation gate for the physical access-control under-answer.
