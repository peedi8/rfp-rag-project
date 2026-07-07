# Parallel Eval Summary

EDD score definition: 20% coverage, 10% hit-all-targets, 15% MRR, 20% groundedness, 20% relevance, 10% abstention accuracy, 5% latency score, minus penalties for false abstention and empty answers.

Rows missing groundedness/relevance are marked `diagnostic_only` and excluded from rankings and graphs because their EDD score is not comparable with fully judged runs.

- Scoreboard rows: 0
- Diagnostic-only rows: 5

## Best By Suite

| suite | run label | experiment | EDD | coverage | MRR | groundedness | relevance | false abstain | empty | latency |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

## Top Experiments

| rank | suite | run label | experiment | EDD | coverage | MRR | groundedness | relevance | false abstain | empty | latency |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

## Diagnostic-Only Rows

| suite | run label | experiment | EDD | coverage | MRR | abstention | latency | reason |
|---|---|---|---:|---:|---:|---:|---:|---|
| prompt_sweep | prompt_sweep_prompt_sweep | prompt_concise_verified | 76.64 | 1.000 | 1.000 | 0.000 | 28.648 | diagnostic_question_file_content |
| prompt_sweep | prompt_sweep_prompt_sweep | prompt_report_ready | 76.00 | 1.000 | 1.000 | 0.000 | 38.708 | diagnostic_question_file_content |
| prompt_sweep | prompt_sweep_prompt_sweep | prompt_strict_evidence | 70.16 | 1.000 | 1.000 | 0.000 | 37.863 | diagnostic_question_file_content |
| baseline_default | baseline_default_baseline_default | baseline_default | 64.76 | 1.000 | 1.000 | 0.000 | 28.870 | diagnostic_question_file_content |
| prompt_sweep | prompt_sweep_prompt_sweep | prompt_default | 64.00 | 1.000 | 1.000 | 0.000 | 30.873 | diagnostic_question_file_content |

## Visuals

![EDD score graph](edd_score.svg)

![Metric heatmap](metric_heatmap.svg)

![Retrieval quality scatter](quality_vs_retrieval.svg)

![Latency vs EDD](latency_vs_edd.svg)
