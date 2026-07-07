# Checkpoint 01 - Inputs

- objective: L126 scored prompt diagnostic on frozen L125 sparse-field cases
- workspace: `I:\0706\rfp-rag-project`
- run_dir: `I:\0706\rfp-rag-project\eval\parallel_runs\20260707_161721_L126-L125-scored-prompt`
- source question file: `questions/questions_l125_sparse_field_diagnostic_frozen.json`
- source basis: L124 raw-source sparse seed scan
- claim use: diagnostic-only sparse-field not-found probe

## Suites

- `baseline_default`
- `prompt_sweep`

## Safety Boundary

This run may be used for sparse-field diagnosis, prompt comparison, latency/cost evidence, and next-task selection. It must not be promoted into ordinary EDD champion ranking.
