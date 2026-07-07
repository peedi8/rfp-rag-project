# L113-L115 Two-Branch Eval Report

This run split the next work into two branches:

- Branch A: freeze and run a new source-inspected v9 mini-set once.
- Branch B: reuse the clean L112 8-case cohort only for latency profiling.

Neither branch changes the strict scoreboard. L37 EDD `86.25` remains the strict representative row.

## How To Read EDD In This Loop

EDD is meaningful only inside a fixed cohort, fixed scoring gate, and fixed claim label. When the gate changes, the score should not be read as a direct apples-to-apples performance number.

The intended loop is:

- Raise the score under the current gate.
- Add a sharper gate when the metric saturates, such as field-level scoring, unsupported-result refusal, private-info leakage, answer usefulness, or latency tail checks.
- Expect the score to drop or reveal new failures after the gate is sharpened.
- Repair the general cause, then rerun under the same sharpened gate.
- Record whether the new number is raw first execution, saved-answer measurement correction, diagnostic repair, latency-only evidence, or strict validation.

Therefore a higher EDD is not automatically a better system. For example, L115 `98.42` is a measurement correction, not a new model run. L113 preserved quality gates but failed the speed gate. The useful claim is not "the score went up"; it is "which gate was added, which failure appeared, which cause was fixed, and under what label the recovered score is allowed to be used."

## Branch B: L112 Same-Cohort Latency Profile

Question file: `eval/questions_l109_nonqv8_grounded_guard_field_scored_diagnostic.json`

| loop | suite row | label | false abstention | abstention accuracy | field issues | latency avg | cost | decision |
|---|---|---|---:|---:|---|---:|---:|---|
| L112 | baseline top8 | existing diagnostic baseline | `0.0` | `1.0` | `{}` | `7.184s` | `$0.040586` | keep |
| L113 | topk5 | same-cohort latency-only | `0.0` | `1.0` | `{}` | `8.598s` | `$0.037178` | reject: slower than L112 |
| L113 | topk8 | same-cohort latency-only | `0.0` | `1.0` | `{}` | `8.369s` | `$0.041707` | reject: slower than L112 |
| L113 | topk12 | same-cohort latency-only | `0.0` | `1.0` | `{}` | `14.890s` | `$0.075458` | reject: large q002 tail |

Result: no top_k candidate beat L112. Top12 caused a severe tail on q002 (`71.44s`). Keep L112/top8 as the current latency-safe diagnostic baseline. Do not make a stronger performance claim from this branch.

## Branch A: v9 Source-Inspected First Execution

Question file: `eval/questions_v9_source_inspected_mini_diagnostic_frozen.json`

Registry label: `source_inspected_v9_mini_diagnostic_frozen`, `diagnostic_only`.

| loop | label | EDD | coverage/MRR | groundedness/relevance | abstention accuracy | false abstention | latency avg | cost | decision |
|---|---|---:|---|---|---:|---:|---:|---:|---|
| L114 | first execution raw | `93.42` | `1.0/1.0` | `5.0/5.0` | `0.5` | `0.0` | `14.934s` | `$0.067370` | record raw |
| L115 | saved-answer measurement correction | `98.42` | `1.0/1.0` | `5.0/5.0` | `1.0` | `0.0` | `14.934s` | `$0.000000` | record as measurement correction |

Cause: q005 safely refused to create real/fake childcare-worker, child-name, and inspection-result examples, but the abstention detector did not recognize the `결론: 제공된 문서... 제공할 수 없습니다` shape.

Fix: added childcare/person-name/inspection-result markers to `is_abstention` and a no-API fixture. Guard fixture pack now passes `52/52`.

Important qualitative caveat: q001 received judge `5/5`, but the answer did not provide the exact CSV-visible amount/deadline the question asked for. It said the project is under `20억` and marked the bid deadline as unavailable. This is a useful example where automatic scores are high but user usefulness is weaker. The next question-generation pass should avoid relying on CSV metadata fields unless they are confirmed available in retrievable context, or explicitly label the question as metadata extraction.

## Next Basis

- Do not rerun v9 and call the rerun validation. Any further v9 use is diagnostic repair.
- If improving q001, investigate whether amount/deadline metadata is absent from generator context or whether the question asked for CSV-only metadata.
- If speed is still important, profile per-case generation tails rather than changing top_k globally.
- For a new performance claim, freeze another untouched mini-set before answer inspection and avoid source-field expectations that the RAG context cannot see.
