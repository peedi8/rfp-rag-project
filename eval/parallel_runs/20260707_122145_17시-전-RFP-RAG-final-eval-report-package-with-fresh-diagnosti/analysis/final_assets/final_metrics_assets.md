# Final Metrics Assets

- generated_from: `I:\0706\rfp-rag-project\eval\parallel_runs\20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight`

## Selected Diagnostic Trend

| loop | EDD | latency | decision | caveat |
|---|---:|---:|---|---|
| L81 | 97.41 | 19.407 | keep_as_quality_probe_not_validation | diagnostic_prompt_fresh_source_exposed |
| L85b | 98.00 | 16.794 | keep_control_not_new_optimization | diagnostic_latency_probe |
| L91 | 97.82 | 17.613 | keep_hint_candidate_not_fresh_validation | source_exposed_regression |
| L95 | 98.54 | 14.44 | keep_as_source_exposed_candidate_not_validation | source_exposed_regression |

## qv7_009 Answer Shape

| loop | chars | lines | bullets | issues | latency |
|---|---:|---:|---:|---:|---:|
| L81 | 1142 | 25 | 20 | 1 | 25.21 |
| L85b | 1294 | 42 | 27 | 1 | 18.08 |
| L91 | 718 | 9 | 5 | 0 | 17.66 |
| L95 | 651 | 9 | 5 | 0 | 16.09 |

## qv7_006 Latency Breakdown

| loop | latency | retrieval | generation | answer chars | issues |
|---|---:|---:|---:|---:|---:|
| L81 | 20.25 | 0.34 | 19.9 | 528 | 1 |
| L85b | 17.83 | 0.36 | 17.46 | 179 | 0 |
| L91 | 28.81 | 0.32 | 28.49 | 179 | 0 |
| L95 | 0.35 | 0.35 | 0 | 179 | 0 |

## Chart Files

- `edd_trend.svg`
- `latency_trend.svg`
- `qv7_009_answer_shape.svg`
- `qv7_006_latency_breakdown.svg`
