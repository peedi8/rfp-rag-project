# Parallel Team Handoff

- run_dir: `I:\0706\rfp-rag-project\eval\parallel_runs\20260707_134725_Two-branch-eval-fresh-mini-set-first-run-and-L112-latency-pr`
- status: complete
- objective: two-branch eval, v9 source-inspected first execution plus L112 latency profile

## Accepted Evidence

- L113 same-cohort latency profile found no faster top_k candidate than L112.
- L114 v9 first execution raw score is recorded separately from later measurement correction.
- L115 saved-answer recompute fixed the childcare sensitive-refusal detector and is labeled measurement correction.

## Protected Paths

- `src/**`
- `scripts/**`
- `eval/questions*.json`
- `eval/experiment_log.md`
- `eval/next_improvement_tasks.md`
- `업무일지.md`

## Final Smoke

- Python compile: pass.
- Guard fixtures: `52/52`.
- Exposure registry: `33` entries.
- Worker smoke: pass, `worker_output_count=6`, `issues=[]`.
- No active `run_experiment_worker.py` process remained for this run.

## Next Actions

- Keep v9 as diagnostic-only.
- Investigate q001 metadata usefulness gap.
- For any new performance claim, freeze a new question set before answer inspection and avoid CSV-only metadata expectations unless the RAG context exposes them.
