# Sparse Answer Audit

This diagnostic checks sparse-field answer shape separately from ordinary EDD.

## Experiment Summary

| run | suite output | experiment | pass rate | padding risks | detector conflicts | present coverage | latency |
|---|---|---|---:|---:|---:|---:|---:|
| 20260707_161718_L127-L125-scored-topk-mm | topk_sweep_topk_sweep | topk8_filter_rewrite_control | 0.5 | 0 | 1 | 0.5 | 23.997 |
| 20260707_161718_L127-L125-scored-topk-mm | mmr_lambda_sweep_mmr_lambda_sweep | lambda05_top8_filter_rewrite_control | 0.5 | 0 | 1 | 0.5 | 25.792 |
| 20260707_161718_L127-L125-scored-topk-mm | topk_sweep_topk_sweep | topk5_filter_rewrite | 0.5 | 0 | 2 | 0.458 | 21.132 |
| 20260707_161718_L127-L125-scored-topk-mm | mmr_lambda_sweep_mmr_lambda_sweep | lambda07_top8_filter_rewrite | 0.5 | 0 | 3 | 0.5 | 20.693 |
| 20260707_161718_L127-L125-scored-topk-mm | topk_sweep_topk_sweep | topk12_filter_rewrite | 0.5 | 0 | 3 | 0.5 | 37.135 |
| 20260707_161718_L127-L125-scored-topk-mm | mmr_lambda_sweep_mmr_lambda_sweep | lambda03_top8_filter_rewrite | 0.5 | 0 | 3 | 0.5 | 41.73 |

## Notes
- `padding_risk` means an absent field label appeared without a nearby or global not-found caveat.
- `detector_conflict` means the binary abstention detector called the answer an abstention even though the answer had a partial answer + absence-caveat shape.
- These rows are diagnostic-only and must not be promoted to ordinary EDD ranking.
