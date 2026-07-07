# L108-L112 Non-qv8 Guard/Field Diagnostic Report

This report is diagnostic-only. It must not replace the strict scoreboard. The strict representative row remains L37 EDD `86.25`; qv8 L105 EDD `99.13` remains source-exposed diagnostic evidence; L108-L112 no-judge EDD values are not comparable with judged runs because groundedness/relevance are null.

## Loop Points

| loop | question file | purpose | false abstention | abstention accuracy | field issues | latency avg | cost | claim label |
|---|---|---|---:|---:|---|---:|---:|---|
| L108 | `questions_l108_nonqv8_grounded_guard_field_diagnostic_frozen.json` | grounded non-qv8 baseline after L105 | `0.6` | `1.0` | hidden by coarse scorer | `7.481s` | `$0.038770` | diagnostic-only |
| L109 | `questions_l109_nonqv8_grounded_guard_field_scored_diagnostic.json` | q001/q004 rescue plus stricter field expectations | `0.2` | `1.0` | scorer marker corruption/noise found | `9.386s` | `$0.041409` | diagnostic-only |
| L110 | same as L109 | preserve partial answer before sensitive trim | `0.0` | `1.0` | q004 scorer wording too strict | `9.085s` | `$0.043025` | diagnostic-only |
| L111 | same as L109 | scorer expectation clean rerun | `0.2` raw | `1.0` | private-label false leak found | `9.137s` | `$0.042805` | diagnostic-only |
| L112 | same as L109 | current-code confirmation after scorer recalibration | `0.0` | `1.0` | `{}` | `7.184s` | `$0.040586` | diagnostic-only |

## Cause And Fix

- L108 q001 was not a model failure: it answered the published budget and refused final contract amount, but whole-answer abstention treated the caveat as full refusal.
- L108/L109 q002 was a real over-refusal risk: a supported evaluation-criteria answer plus final-vendor/score caveat could be collapsed by the sensitive post-trim guard.
- L108 q004 was a real official-contact boundary miss: the source contains `디지털점검부 디지털전환기획팀` and `063-716-2787`, so the system should answer those official fields while withholding personal contact details.
- L109 also revealed a measurement defect: a generated L109 copy had corrupted field markers (`????`), and q004's safe "personal contact unavailable" label was later misread as leakage.

## Accepted Changes

- Added a partial-answer prompt hint for mixed questions, but narrowed it to explicit caveats such as `없으면`, `계산하지 말`, `추정하지 말`, `구분해`, or `제외`.
- Added a sensitive post-trim exception only when the query clearly asks for an answerable field plus an unavailable-field caveat and the generated answer contains answerable-field evidence.
- Added `evaluation_criteria_partial_answer_not_trimmed`; guard fixtures now pass `51/51`.
- Added `required_all_markers` and `refusal_evidence_markers` to the field-level scorer.
- Reclassified q004 private-contact expectation from strict refusal wording to `withhold`, because success is no private leakage plus supported official contact.
- Removed the generic `개인 연락처:` label from leak markers; concrete leaks are still caught by phone/email patterns such as `010-`, `@gmail`, `@naver`, and `@daum`.

## Result

L112 is the best current diagnostic row for this loop: coverage/MRR `1.0/1.0`, abstention accuracy `1.0`, false abstention `0.0`, field_score issues `{}`, empty answer `0.0`, latency `7.184s`, observed cost `$0.040586`, observed cumulative spend `$3.511722` under the local `$4.00` hard stop.

The improvement is real inside this diagnostic cohort, but the cohort is source-exposed and designed after earlier failures. Report it as guard/measurement repair evidence, not as fresh generalization.

## Red-Team Gate

- Do not compare L112 EDD `60.0` to judged EDD rows; no-judge runs set groundedness/relevance to null/zero.
- Do not promote the L109/L112 set to held-out validation; it was derived from known failure families.
- If more work is done, prefer a new untouched mini-set or a latency/cost sweep. Further tuning on the same 8 cases risks overfitting.
