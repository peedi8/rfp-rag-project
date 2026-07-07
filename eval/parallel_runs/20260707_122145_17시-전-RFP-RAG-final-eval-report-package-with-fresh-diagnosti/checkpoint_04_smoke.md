# Checkpoint 04 - Smoke

- status: pass
- worker_output_count: 5
- report: I:\0706\rfp-rag-project\eval\parallel_runs\20260707_122145_17시-전-RFP-RAG-final-eval-report-package-with-fresh-diagnosti\smoke\parallel_smoke_report.json

## Issues

- none

## Verification Notes

- py_compile: pass for generator/evaluator/registry/worker/aggregate scripts.
- no-API fixture pack: `34/34` pass.
- qv8 aggregate: raw diagnostic row EDD `95.81`, diagnostic-only, not scoreboard.
- qv8 recompute: EDD `97.81`, abstention accuracy `1.0`, changed case `q20260707_a12_seoul_digital_sex_crime_sensitive_story`.
- qv8 observed cost: `$0.126294`; observed spent after qv8 `$2.813455` under hard stop `$5.00`.
- final report: `I:\0706\rfp-rag-project\eval\parallel_runs\20260707_122145_17시-전-RFP-RAG-final-eval-report-package-with-fresh-diagnosti\summary\final_report_draft.md`.
- visual assets: `I:\0706\rfp-rag-project\eval\parallel_runs\20260707_122145_17시-전-RFP-RAG-final-eval-report-package-with-fresh-diagnosti\analysis\final_assets`.
- diary forbidden-term check: no forbidden Korean coordination terms found.

## Current Position

- strict scoreboard remains L37 EDD `86.25`.
- strongest source-exposed diagnostic remains L95 EDD `98.54`, latency `14.44s`, quality issue rows `0/12`.
- qv8 L99 recomputed diagnostic EDD is `97.81`; it is diagnostic evidence and a measurement correction, not strict validation.
