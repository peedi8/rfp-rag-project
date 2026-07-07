# Checkpoint 04 - Verification

## Commands

- source compile check for:
  - `src\retriever.py`
  - `scripts\evaluate.py`
  - `scripts\build_adversarial_v5.py`
  - `scripts\analyze_adversarial_run.py`
  - `scripts\build_exposure_registry.py`
- JSON parse check for v5 question, manifest, registry, ledger, and adversarial analysis files.
- output smoke check:
  - `python C:\Users\peedi\.codex\skills\parallel-team-orchestrator\scripts\smoke_parallel_outputs.py --run-dir eval\parallel_runs\20260706_212647_Adversarial-RAG-breaker-loop-under-budget-cap`
- `업무일지.md` forbidden-term check.

## Results

- compile: pass (`5` files)
- JSON parse: pass (`7` files)
- output smoke: pass
  - worker_output_count: `5`
  - issues: `[]`
- `업무일지.md` forbidden-term hits: `[]`
