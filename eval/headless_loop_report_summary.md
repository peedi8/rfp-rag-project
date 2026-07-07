# Headless Improvement Loop Summary

- updated_at: 2026-07-06
- scope: L0-L36 after budget-capped and adversarial runs
- status: adversarial run complete; L25 is current v4 evidence, L30 is current first v5 evidence

## Current Evidence Hierarchy

| level | evidence | how to use |
|---|---|---|
| first validation | L0 v3 first run, EDD 89.69 | honest first-seen validation evidence |
| measurement correction | L1 same answers recomputed, EDD 96.36 | corrected record, not model improvement by itself |
| rejected candidate | L2/L3 top5 | speed improved slightly but quality dropped |
| diagnostics | L4-L11 | retrieval/source/judge/adaptive causes and candidate guards |
| qualitative evidence | L12 | human quality avg 3.62, evidence safety avg 3.47 |
| prompt candidate | L13 report_ready | candidate only until scored |
| gates | L14-L19 | headless gate, runner, exposure registry, frozen v4 manifest |
| judge calibration | L20-L24 | original pack failed partially, strict pack passed |
| v4 scored evidence | L25 | frozen v4 first scored run, EDD 97.41 |
| rejected probes | L26-L29 | top5/prompt probes did not beat L25 |
| adversarial first evidence | L30 | frozen v5 first run, EDD 92.40 |
| targeted retrieval fix | L31-L34 | title-fragment issuer filter fixed exposed v5; recomputed scores are measurement-corrected |
| regression evidence | L35-L36 | v4 correctness held, but top5/default speed claims were not promoted |

## Main Lessons

1. High EDD can hide weak human readability.
2. Measurement corrections must not be reported as new model improvements.
3. Same-set targeted fixes are useful but not held-out evidence.
4. No-judge rows are diagnostics, not performance scores.
5. A gate can also be wrong; L18 fixed classifier false positives in the gate itself.
6. Future first-run evidence should use a frozen question set and preserve the first result.
7. Calibration packs need clean pass cases; ambiguous "good" answers can make a judge look worse or better than it is.
8. Same-answer recomputation must be labeled as measurement correction, not model improvement.
9. Prompt changes that shorten answers can still hurt latency or abstention detection.
10. A user may remember a project title fragment better than the issuing organization; retrieval should support that without over-narrowing generic titles.
11. A high post-fix score on a set whose failure was already inspected is targeted evidence, not fresh generalization evidence.

## Ready Artifacts

- Gate report: `eval\parallel_runs\20260706_200022_headless-improvement-loop-with-red-and-overfit-gates\summary\registry_connected_gate\headless_gate_report.md`
- Exposure registry: `eval\question_exposure_registry.md`
- Frozen v4 question set: `eval\questions_v4_frozen_first_run.json`
- Frozen v4 manifest: `eval\questions_v4_frozen_first_run.manifest.json`
- Loop chart: `eval\parallel_runs\20260706_1825_timeboxed-red-loop-v3-validation\analysis\loop_points_chart.svg`
- L30-L36 report: `eval\parallel_runs\20260706_212647_Adversarial-RAG-breaker-loop-under-budget-cap\summary\l30_l36_adversarial_loop_report.md`
- v5 frozen question set: `eval\questions_v5_adversarial_frozen_first_run.json`

## Next Budgeted Step

The budgeted L20-L29 sequence is complete. L24 passed strict blind calibration, and L25 produced the current v4 first-scored evidence.

Budget rule for L20+:

- budget cap: `$14.00`
- hard stop: `$13.00`
- model default: `gpt-5-mini`
- pricing assumption: input `$0.75 / 1M tokens`, output `$4.50 / 1M tokens`
- every case writes a checkpoint before the next case starts

## Latest Outcome

- L20 original calibration: partial fail, actual cost `$0.019861`.
- L24 strict calibration: pass, actual cost `$0.020890`.
- calibration ledger recorded actual total: `$0.063527`.
- L25 v4 first scored run: EDD `97.41`, latency `19.377s`.
- L26 global top5: EDD `97.12`, rejected.
- L27 report_ready: EDD `95.00`, rejected.
- L29 concise_verified after measurement correction: EDD `96.42`, rejected.
- L30 v5 first adversarial run: EDD `92.40`, exposed title-fragment retrieval failure.
- L33 v5 same-answer recompute after title filter and detector correction: EDD `98.37`, targeted evidence only.
- L34 v5 top5 same-answer recompute: EDD `98.70`, not promoted globally.
- L35 v4 title-filter regression baseline: EDD `96.81`.
- L36 v4 top5 regression: EDD `96.44`, rejected as global default.

## Current Next Step

Do not keep tuning on the same v4/v5 sets without a new hypothesis. The next useful work is one of:

- create and freeze a v6 unseen title-fragment validation set,
- add generic-title false-positive probes,
- run human readability review on L25 answers,
- investigate latency outliers on `qv4_002`, `qv4_004`, and `qv4_008`.
