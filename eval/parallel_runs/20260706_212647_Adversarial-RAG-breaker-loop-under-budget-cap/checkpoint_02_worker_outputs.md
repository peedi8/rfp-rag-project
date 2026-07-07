# Checkpoint 02 - Outputs

## Question And Registry Artifacts

- `eval\questions_v5_adversarial_draft.json`
- `eval\questions_v5_adversarial_notes.md`
- `eval\questions_v5_adversarial_frozen_first_run.json`
- `eval\questions_v5_adversarial_frozen_first_run.manifest.json`
- `eval\question_exposure_registry.json`
- `eval\question_exposure_registry.md`

## Scored Outputs

- L30 first v5 baseline: `worker_outputs\l30_v5_adversarial_first_baseline_baseline_default`
- L31 v5 title-filter baseline: `worker_outputs\l31_v5_title_filter_baseline_baseline_default`
- L32 v5 title-filter top-k sweep: `worker_outputs\l32_v5_title_filter_topk_topk_sweep`
- L33 v4 title-filter baseline regression: `worker_outputs\l33_v4_regression_title_filter_baseline_default`
- L35 v4 title-filter top-k regression: `worker_outputs\l35_v4_title_filter_topk_regression_topk_sweep`

## Analysis Outputs

- `summary\l30_adversarial_analysis`
- `summary\l31_adversarial_analysis`
- `summary\l32_adversarial_analysis`
- `summary\l30_l36_adversarial_loop_report.md`
- `summary\l30_l36_budget_note.md`
- `analysis\l34_l31_sensitive_abstention_recompute`
- `analysis\l34_l32_top5_sensitive_abstention_recompute`
- `analysis\l36_l35_top8_procurement_marker_recompute`
- `summary\summary.md`
- `summary\edd_score.svg`
- `summary\metric_heatmap.svg`
- `summary\quality_vs_retrieval.svg`
- `summary\latency_vs_edd.svg`

## Observed Key Results

- L30 first v5 baseline: EDD `92.40`, coverage `0.929`, latency `20.776s`.
- L32 raw title-filter baseline: EDD `95.87`, coverage `1.000`, latency `15.151s`.
- L33 same-answer recompute: EDD `98.37`.
- L34 same-answer v5 top5 recompute: EDD `98.70`.
- L35 v4 baseline regression: EDD `96.81`.
- L36 v4 top5 regression: EDD `96.44`.
