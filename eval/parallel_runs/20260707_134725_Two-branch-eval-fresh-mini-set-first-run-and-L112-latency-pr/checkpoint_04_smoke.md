# Checkpoint 04 - Smoke

- status: pass
- worker_output_count: 6
- report: eval\parallel_runs\20260707_134725_Two-branch-eval-fresh-mini-set-first-run-and-L112-latency-pr\smoke\parallel_smoke_report.json

## Issues

- none

## Final Checks

- Python compile: pass for `scripts/evaluate.py`, `scripts/check_evidence_guard_fixtures.py`, `scripts/build_exposure_registry.py`, `scripts/run_experiment_worker.py`, and `scripts/recompute_saved_eval.py`.
- Guard fixtures: `52/52`, failed `0`.
- Exposure registry rebuild: `33` entries.
- Worker contract smoke: pass, `worker_output_count=6`, `issues=[]`.
- JSON parse: pass for `ledger.json` and `handoff/handoff.json`.
- Diary forbidden-word check: pass, no matches.
- Active process check: no `run_experiment_worker.py` process remained for this run.

## Residual Risk

- L115 is a measurement correction, not a new model run.
- v9 remains source-inspected diagnostic evidence, not strict held-out validation.
- q001 needs follow-up because automatic judge score was high while exact metadata usefulness was weak.
