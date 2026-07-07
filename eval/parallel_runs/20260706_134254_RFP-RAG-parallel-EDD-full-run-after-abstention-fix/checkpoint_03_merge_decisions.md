# Checkpoint 03 - Merge Decisions

- status: accepted_as_evidence
- final candidate: 	op_k=8, mmr_lambda=0.5, etch_k=20, uto_filter=true, ewrite_query=true
- basis: summary/summary.md, EDD top row lambda05_top8_filter_rewrite_control = 96.57
- note: 	opk5_filter_rewrite was near tie (96.53), but top8 keeps more context and matches prior raw-mode hypothesis.

## Accepted Worker Evidence
- topk_sweep: accepted for top_k comparison.
- mmr_lambda_sweep: accepted; lambda 0.5 selected.
- fetchk_sweep: accepted; fetch_k 20 selected over 40.
- filter_rewrite_ablation: accepted; both auto_filter and rewrite_query are needed for complementary failure modes.
