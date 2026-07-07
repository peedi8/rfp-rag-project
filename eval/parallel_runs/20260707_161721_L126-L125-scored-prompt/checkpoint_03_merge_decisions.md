# Checkpoint 03 - Merge Decisions

- accepted: `baseline_default_baseline_default` as diagnostic-only evidence.
- accepted: `prompt_sweep_prompt_sweep` as diagnostic-only evidence.
- rejected for promotion: all L126 rows as ordinary EDD/champion rows because the question file is explicitly diagnostic-only and source-exposed.
- accepted code fix: `scripts/aggregate_parallel_eval.py` now reads worker contracts with `utf-8-sig` and detects diagnostic-only question files from question content.
- accepted analysis add-on: `scripts/audit_sparse_answer_runs.py` created sparse-field answer-shape diagnostics under `analysis/sparse_answer_audit/`.

## Result Notes

- Best ordinary-looking L126 row was `prompt_concise_verified` with EDD `76.64`, but this is diagnostic-only.
- `prompt_concise_verified` reduced binary false-abstain to `0/6`, but sparse answer audit pass rate was only `0.5`.
- Interpretation: the prompt stopped obvious global refusals and padding risk, but still did not consistently recover enough source-visible fields.
