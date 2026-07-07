# L46 Red Review Budget Gate Correction

## Summary

L45 added useful gates, but the red review found that its budget proof was too weak:

- dry-run should not be skipped by a budget cap, because dry-run has no model cost;
- all-skipped budget runs should be explicitly labeled;
- budget events should be written immediately, not only at the end;
- compact harmful post-refusal summaries should be caught by keyword/detail signals, not only length.

## Fixes

- Dry-run bypasses the preflight budget skip and still writes a zero-cost diagnostic row.
- Non-dry preflight skip writes `status=blocked`, `budget_gate_all_skipped=true`, and `skipped_preflight_budget`.
- Budget events are appended to `budget_ledger.jsonl` as they happen.
- Ledger records now include run id, worker id, question file, dry-run/no-judge flags, spent before/after, remaining budget, skip reason, status, record type, cost basis, and usage-missing flags.
- `answer_quality_diagnostics` now records post-refusal tail characters, bullet count, and detail keyword hits.
- Saved-eval recompute scripts now propagate `answer_quality_issues`.

## Verification

Hard-stop skip path:

- command: `python scripts\run_experiment_worker.py --run-dir eval\parallel_runs\20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight --suite baseline_default --worker-id l46_hardstop_skip --questions eval\questions_v6_l38_safety_retry.json --case-limit 1 --max-experiments 1 --no-judge --hard-stop-usd 0.001 --starting-spent-usd 0.001 --preflight-case-estimate-usd 0.02`
- result: `status=blocked`, `wrote_rows=0`, `budget_gate_all_skipped=true`, `observed_cost_usd=0`

Dry-run path:

- command: `python scripts\run_experiment_worker.py --run-dir eval\parallel_runs\20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight --suite baseline_default --worker-id l46_dryrun_not_skipped --questions eval\questions_v6_l38_safety_retry.json --case-limit 1 --max-experiments 1 --dry-run --no-judge --hard-stop-usd 0 --starting-spent-usd 0`
- result: `wrote_rows=1`, `skipped_preflight_budget=0`, `observed_cost_usd=0`

Aggregate and smoke:

- aggregate: rows `11`, scoreboard rows `1`, diagnostic-only rows `10`
- smoke: pass, worker output contracts `18`, issues `[]`

## Decision

L46 supersedes the L45 dry-run skip as budget proof. The corrected proof is the non-dry preflight skip that stops before any model call.

Broad paid v7/v8/v9 should still wait for the qv6_007 claim-preservation gate.
