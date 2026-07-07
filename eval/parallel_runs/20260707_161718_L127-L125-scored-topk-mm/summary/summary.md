# Parallel Eval Summary

EDD score definition: 20% coverage, 10% hit-all-targets, 15% MRR, 20% groundedness, 20% relevance, 10% abstention accuracy, 5% latency score, minus penalties for false abstention and empty answers.

Rows missing groundedness/relevance are marked `diagnostic_only` and excluded from rankings and graphs because their EDD score is not comparable with fully judged runs.

- Scoreboard rows: 0
- Diagnostic-only rows: 6

## Best By Suite

| suite | run label | experiment | EDD | coverage | MRR | groundedness | relevance | false abstain | empty | latency |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

## Top Experiments

| rank | suite | run label | experiment | EDD | coverage | MRR | groundedness | relevance | false abstain | empty | latency |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

## Diagnostic-Only Rows

| suite | run label | experiment | EDD | coverage | MRR | abstention | latency | reason |
|---|---|---|---:|---:|---:|---:|---:|---|
| mmr_lambda_sweep | mmr_lambda_sweep_mmr_lambda_sweep | lambda05_top8_filter_rewrite_control | 71.12 | 1.000 | 1.000 | 0.000 | 25.792 | diagnostic_question_file_content |
| mmr_lambda_sweep | mmr_lambda_sweep_mmr_lambda_sweep | lambda07_top8_filter_rewrite | 69.77 | 1.000 | 1.000 | 0.000 | 20.693 | diagnostic_question_file_content |
| topk_sweep | topk_sweep_topk_sweep | topk8_filter_rewrite_control | 69.02 | 1.000 | 1.000 | 0.000 | 23.997 | diagnostic_question_file_content |
| topk_sweep | topk_sweep_topk_sweep | topk5_filter_rewrite | 66.52 | 1.000 | 1.000 | 0.000 | 21.132 | diagnostic_question_file_content |
| mmr_lambda_sweep | mmr_lambda_sweep_mmr_lambda_sweep | lambda03_top8_filter_rewrite | 65.84 | 1.000 | 1.000 | 0.000 | 41.730 | diagnostic_question_file_content |
| topk_sweep | topk_sweep_topk_sweep | topk12_filter_rewrite | 64.50 | 1.000 | 1.000 | 0.000 | 37.135 | diagnostic_question_file_content |

## Visuals

![EDD score graph](edd_score.svg)

![Metric heatmap](metric_heatmap.svg)

![Retrieval quality scatter](quality_vs_retrieval.svg)

![Latency vs EDD](latency_vs_edd.svg)
