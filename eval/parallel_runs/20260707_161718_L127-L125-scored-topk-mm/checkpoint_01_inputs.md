# Checkpoint 01 - Inputs

- objective: L127 scored retrieval diagnostic on frozen L125 sparse-field cases
- workspace: `I:\0706\rfp-rag-project`
- run_dir: `I:\0706\rfp-rag-project\eval\parallel_runs\20260707_161718_L127-L125-scored-topk-mm`
- source question file: `questions/questions_l125_sparse_field_diagnostic_frozen.json`
- source basis: L124 raw-source sparse seed scan
- claim use: diagnostic-only sparse-field not-found probe

## Suites

- `topk_sweep`
- `mmr_lambda_sweep`

## Safety Boundary

This run compares retrieval parameter behavior for sparse-field diagnostics. It must not be promoted into ordinary EDD champion ranking.
