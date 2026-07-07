# Checkpoint 03 - Merge Decisions

- accepted: L125 frozen question artifacts as diagnostic-only sparse-field probes.
- accepted downstream execution: L126 prompt-lane scored diagnostic and L127 retrieval-lane scored diagnostic.
- rejected for promotion: L125/L126/L127 rows as ordinary EDD/champion evidence because the question file is source-exposed and explicitly diagnostic-only.
- accepted fix: `scripts/aggregate_parallel_eval.py` now detects diagnostic-only question files from file content and keeps them out of scoreboard.
- accepted analysis add-on: `scripts/audit_sparse_answer_runs.py` created sparse answer-shape audits for L126/L127.

## Decision

The useful next step is not another broad top_k sweep. The remaining gap is measurement and response shape:

- generic relevance judge penalizes safe refusal on padding-trap prompts;
- binary abstention can misread partial sparse answers as global refusal;
- present-field recovery is only about half under the sparse audit.
