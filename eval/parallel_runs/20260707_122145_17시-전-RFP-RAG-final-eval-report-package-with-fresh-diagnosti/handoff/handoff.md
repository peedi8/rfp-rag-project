# Handoff - Pre-17:00 RFP-RAG Final Eval Package

## Objective

Prepare final eval/report evidence before the 19:00 deadline, with work complete by 17:00 when possible.

## Current State

- Final report draft: `I:\0706\rfp-rag-project\eval\parallel_runs\20260707_122145_17시-전-RFP-RAG-final-eval-report-package-with-fresh-diagnosti\summary\final_report_draft.md`
- Strict scoreboard: L37 EDD `86.25` only.
- Best source-exposed diagnostic: L95 EDD `98.54`, latency `14.44s`, quality issue rows `0/12`.
- qv8 raw diagnostic: L98 EDD `95.81`, latency `17.645s`, observed cost `$0.126294`.
- qv8 measurement-corrected diagnostic: L99 EDD `97.81`, abstention `1.0`.
- Fixture pack: `34/34` pass.
- Smoke: pass.

## Must Preserve

- Do not call L95 or qv8 strict held-out validation.
- Do not call L99 a model improvement; it is evaluator repair over saved answers.
- Keep L98 raw and L99 recompute side by side.
- Next work should target qv8 latency tail and field-level scoring.

## Next Actions

1. If preparing a student-facing final document, summarize L37/L95/qv8 with the caveats above.
2. Add qv8 latency-tail loop only if time remains.
3. Do not tune against qv8 and then call the same set held-out.
