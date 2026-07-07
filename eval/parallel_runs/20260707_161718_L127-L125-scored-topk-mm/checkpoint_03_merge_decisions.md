# Checkpoint 03 - Merge Decisions

- accepted: `topk_sweep_topk_sweep` as diagnostic-only evidence.
- accepted: `mmr_lambda_sweep_mmr_lambda_sweep` as diagnostic-only evidence.
- rejected for promotion: all L127 rows as ordinary EDD/champion rows because the question file is explicitly diagnostic-only and source-exposed.
- accepted code fix: `scripts/aggregate_parallel_eval.py` prevents diagnostic-only question files from entering scoreboard.
- accepted analysis add-on: `scripts/audit_sparse_answer_runs.py` created sparse-field answer-shape diagnostics under `analysis/sparse_answer_audit/`.

## Result Notes

- Best ordinary-looking L127 row was `lambda05_top8_filter_rewrite_control` with EDD `71.12`, but this is diagnostic-only.
- Sparse audit found no padding risk in the top retrieval variants, but pass rate stayed at `0.5`.
- Interpretation: retrieval changes did not solve the sparse-field issue. The remaining gap is response/evaluation shape: present-field recovery and binary abstention classification.
