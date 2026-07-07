# Sparse Answer Audit

This diagnostic checks sparse-field answer shape separately from ordinary EDD.

## Experiment Summary

| run | suite output | experiment | pass rate | padding risks | detector conflicts | present coverage | latency |
|---|---|---|---:|---:|---:|---:|---:|
| 20260707_161721_L126-L125-scored-prompt | prompt_sweep_prompt_sweep | prompt_concise_verified | 0.5 | 0 | 0 | 0.542 | 28.648 |
| 20260707_161721_L126-L125-scored-prompt | prompt_sweep_prompt_sweep | prompt_report_ready | 0.5 | 0 | 0 | 0.458 | 38.708 |
| 20260707_161721_L126-L125-scored-prompt | baseline_default_baseline_default | baseline_default | 0.5 | 0 | 2 | 0.5 | 28.87 |
| 20260707_161721_L126-L125-scored-prompt | prompt_sweep_prompt_sweep | prompt_default | 0.5 | 0 | 3 | 0.5 | 30.873 |
| 20260707_161721_L126-L125-scored-prompt | prompt_sweep_prompt_sweep | prompt_strict_evidence | 0.167 | 3 | 0 | 0.5 | 37.863 |

## Notes
- `padding_risk` means an absent field label appeared without a nearby or global not-found caveat.
- `detector_conflict` means the binary abstention detector called the answer an abstention even though the answer had a partial answer + absence-caveat shape.
- These rows are diagnostic-only and must not be promoted to ordinary EDD ranking.
