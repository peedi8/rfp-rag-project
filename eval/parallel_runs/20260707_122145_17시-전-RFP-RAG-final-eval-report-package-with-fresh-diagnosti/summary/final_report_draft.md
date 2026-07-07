# Final RFP-RAG Eval Package Draft

- generated_at: `2026-07-07 12:37:27`
- run_dir: `I:\0706\rfp-rag-project\eval\parallel_runs\20260707_122145_17시-전-RFP-RAG-final-eval-report-package-with-fresh-diagnosti`
- strict scoreboard rule: keep true validation separate from source-exposed or diagnostic evidence.

## Executive Summary

The strict scoreboard number is still L37 EDD `86.25`. That is the honest first-run validation reference.

The strongest source-exposed diagnostic row remains L95: EDD `98.54`, average latency `14.44s`, coverage/MRR `1.0/1.0`, groundedness/relevance `5.0/5.0`, abstention accuracy `1.0`, and answer-quality issue rows `0/12`. This is useful evidence that the plain-language hint and sensitive preempt guard improved exposed failure modes, but it is not fresh validation.

For the deadline run, qv8 was created by the Codex questioner as a semi-fresh/source-exposed mixed diagnostic set, not a held-out set. Raw L98 scored EDD `95.81` with abstention accuracy `0.8` and latency `17.645s`. L99 recomputed the saved answers after a narrow abstention measurement correction: EDD `97.81`, abstention accuracy `1.0`, same latency `17.645s`.

## What Actually Improved

| loop | evidence | result | caveat |
|---|---|---|---|
| L91 | full v7 source-exposed after plain-language hint | qv7_009 stayed concise, answer issues `0/12`, EDD `97.82` | not fresh validation |
| L95 | full v7 source-exposed after sensitive preempt | EDD `98.54`, latency `14.44s`, qv7_006/qv7_012 zero-generation refusals | strongest diagnostic, not scoreboard |
| L97 | no-API guard fixtures | fixture pack expanded from `28` to `33`, all passed | safety guard, not EDD |
| L98 | qv8 diagnostic first run | raw EDD `95.81`, cost `$0.126294` | diagnostic-only; raw abstention metric had one false negative |
| L99 | saved-answer recompute | qv8 EDD `97.81`, abstention `1.0`, issues none | measurement correction, not model improvement |

## Red-Team Caveats

- Do not present L95 or qv8 as strict held-out validation. The report should say `diagnostic_only` clearly.
- qv8_a12 exposed an evaluator blind spot: the answer refused a fabricated victim story, but the old abstention heuristic marked it as non-abstention.
- High judge scores still need answer-shape review. qv7_009 had judge `5/5` while being too structured before the plain-language hint.
- Average latency hides tail latency. qv8 had cases at `31.17s`, `27.25s`, and `25.60s` even though some cases were under `10s`.
- Mixed field-level questions such as official contact plus personal contact need manual or field-level scoring before they are used in an aggregate.

## qv8 First Diagnostic Run

| metric | raw L98 | recomputed L99 |
|---|---:|---:|
| EDD | `95.81` | `97.81` |
| coverage | `1.0` | `1.0` |
| MRR | `1.0` | `1.0` |
| groundedness | `5.0` | `5.0` |
| relevance | `5.0` | `5.0` |
| abstention accuracy | `0.8` | `1.0` |
| average latency | `17.645s` | `17.645s` |
| observed qv8 cost | `$0.126294` | same saved answers |

Changed abstention case: `q20260707_a12_seoul_digital_sex_crime_sensitive_story` changed from `False` to `True` after adding a narrow sensitive-victim-story refusal pattern.

## Visual Assets

- `analysis/final_assets/final_edd_comparison.svg`
- `analysis/final_assets/edd_trend.svg`
- `analysis/final_assets/latency_trend.svg`
- `analysis/final_assets/qv7_009_answer_shape.svg`
- `analysis/final_assets/qv7_006_latency_breakdown.svg`
- `analysis/final_assets/qv8_case_latency.svg`

## Next Best Work

1. Freeze a genuinely unused validation set only if there are uninspected source projects left. If not, report this honestly and use diagnostic labels.
2. Run a latency-tail loop on qv8 high-latency cases, especially generic ambiguity and plain-language cases.
3. Add field-level evaluation for mixed questions: answer official public facts, refuse private/personal fabricated details.
4. Keep the no-API guard fixture pack as the cheap preflight gate before any paid run.
5. Preserve the scoreboard/diagnostic split in every table and figure.
