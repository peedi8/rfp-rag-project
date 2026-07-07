# Parallel Eval Summary

EDD score definition: 20% coverage, 10% hit-all-targets, 15% MRR, 20% groundedness, 20% relevance, 10% abstention accuracy, 5% latency score, minus penalties for false abstention and empty answers.

Rows missing groundedness/relevance are marked `diagnostic_only` and excluded from rankings and graphs because their EDD score is not comparable with fully judged runs.

- Scoreboard rows: 0
- Diagnostic-only rows: 4

## Best By Suite

| suite | run label | experiment | EDD | coverage | MRR | groundedness | relevance | false abstain | empty | latency |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

## Top Experiments

| rank | suite | run label | experiment | EDD | coverage | MRR | groundedness | relevance | false abstain | empty | latency |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

## Diagnostic-Only Rows

| suite | run label | experiment | EDD | coverage | MRR | abstention | latency | reason |
|---|---|---|---:|---:|---:|---:|---:|---|
| topk5_only | l100_topk5_only_topk5_only | topk5_filter_rewrite | 98.00 | 1.000 | 1.000 | 1.000 | 16.798 | diagnostic_question_set |
| baseline_default | l100_baseline_default_baseline_default | baseline_default | 97.11 | 1.000 | 1.000 | 1.000 | 20.736 | diagnostic_question_set |
| topk5_only | l101_qv8_full_topk5_topk5_only | topk5_filter_rewrite | 96.57 | 1.000 | 1.000 | 0.800 | 14.284 | diagnostic_question_set |
| prompt_concise_verified_only | l100_prompt_concise_verified_only_prompt_concise_verified_only | prompt_concise_verified | 86.53 | 1.000 | 1.000 | 0.000 | 23.280 | diagnostic_question_set |

## Visuals

![EDD score graph](edd_score.svg)

![Metric heatmap](metric_heatmap.svg)

![Retrieval quality scatter](quality_vs_retrieval.svg)

![Latency vs EDD](latency_vs_edd.svg)
