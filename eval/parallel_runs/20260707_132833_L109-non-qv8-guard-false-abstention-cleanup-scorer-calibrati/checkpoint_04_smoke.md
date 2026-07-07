# Checkpoint 04 - Smoke

- status: pass
- worker_output_count: 8
- report: eval\parallel_runs\20260707_132833_L109-non-qv8-guard-false-abstention-cleanup-scorer-calibrati\smoke\parallel_smoke_report.json

## Issues

None.

## Final Observed Results

- Python compile: pass.
- Evidence guard fixtures: `51/51`, pass.
- Field scorer calibration: expectation matches `5/5`; expected diagnostic failures remain visible as `over_refusal` and `unsafe_exposure`.
- Exposure registry: generated successfully with `32` entries.
- JSON parse: pass for registry, L109 question file, field fixtures, ledger, and handoff.
- Team output smoke: pass, `worker_output_count=8`, `issues=[]`.
- Diary forbidden-term check: no matches.
- Experiment process check: no matching `run_experiment_worker.py` process running.

Best diagnostic loop for this run: L112.
