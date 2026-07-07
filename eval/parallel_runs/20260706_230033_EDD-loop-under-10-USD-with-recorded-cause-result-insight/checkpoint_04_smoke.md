# Checkpoint 04 - Smoke

- status: pass
- worker_output_count: 60
- report: eval\parallel_runs\20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight\smoke\parallel_smoke_report.json

## Issues

## Verification Notes

- final aggregate: `rows=49`, `scoreboard_rows=1`, `diagnostic_only_rows=48`.
- final smoke: pass, worker output contracts `60`, issues `[]`.
- latest no-API fixture pack: `28/28` pass.
- diary forbidden-term check for `병렬|병행`: no matches.
- ledger / exposure registry / L94 question file / L95 worker JSON parse: pass.
- observed run-folder spend: `$2.687161`.
- cost caveat: L84 monolithic timeout may have made calls before writing a local `cost_summary.json`.

## Current Best Diagnostic Position

- strict scoreboard still preserves L37 only: EDD `86.25`.
- best source-exposed v7 candidate after answer-format and sensitive-preempt guards is L95: EDD `98.54`, latency `14.44s`, qv7_009 clean, qv7_006/qv7_012 preempted, all `answer_quality_issues=[]`.
- L95 is not fresh validation. It is the strongest source-exposed diagnostic row.

## L87-L96 Verification Notes

- L87 added `plain_language_answer_over_structured`; fixtures reached `22/22`.
- L88 found `prompt_report_ready` cleaned qv7_009 but was too slow at `50.94s`.
- L89 query-specific hint cleaned qv7_009 at `16.7s`.
- L90 corrected abstention measurement for substantive plain-language answers with final-result caveats; fixtures reached `23/23`.
- L91 full v7 source-exposed diagnostic completed with EDD `97.82`, abstention `1.0`, quality issue rows `0/12`.
- L92 added plain-language trigger negation fixtures; fixture pack reached `25/25`.
- L93 added sensitive preempt fixtures; fixture pack reached `27/27`.
- L94 two-case preempt probe had generation cost `$0.0` and average latency `2.065s`; EDD is not comparable.
- L95 full v7 source-exposed diagnostic reached EDD `98.54`, latency `14.44s`, quality issue rows `0/12`.
- L96 narrowed the `추정` preempt marker to avoid `추정금액` false positives; fixture pack reached `28/28`.
