# Checkpoint 04 - Smoke

- status: pass
- worker_output_count: 4
- report: eval\parallel_runs\20260707_130747_qv8-sensitive-victim-story-latency-preempt-and-false-positiv\smoke\parallel_smoke_report.json

## Issues

None.

## Additional Verification

- Python syntax check passed for `src/generator.py`, `scripts/evaluate.py`, `scripts/check_evidence_guard_fixtures.py`, `scripts/build_exposure_registry.py`, `scripts/run_experiment_worker.py`, and `scripts/aggregate_parallel_eval.py`.
- No-API guard fixture run passed `41/41`.
- Aggregate summary kept L104/L105 as diagnostic-only: `rows=2`, `scoreboard_rows=0`, `diagnostic_only_rows=2`.
- JSON parse checks passed for the L104 probe, exposure registry, ledger, handoff, report JSON, and worker contracts.
- `업무일지.md` reserved-word check returned no matches.
- Experiment process check passed: no L104/L105 worker process remains running.

This validates artifact integrity and process cleanup. It does not promote L104 or L105 to strict validation.
