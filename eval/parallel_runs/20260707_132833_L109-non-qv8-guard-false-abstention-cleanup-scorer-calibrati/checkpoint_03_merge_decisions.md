# Checkpoint 03 - Merge Decisions

## Accepted

- Add partial-answer prompt/guard behavior for explicit caveat questions.
- Keep the guard exception narrow: it only applies when the query asks for an answerable field plus an unavailable-field caveat and the answer contains supported answerable-field evidence.
- Add `evaluation_criteria_partial_answer_not_trimmed`; final guard fixture pack passes `51/51`.
- Add `required_all_markers` and `refusal_evidence_markers` to field scoring.
- Treat q004 private-contact side as `withhold`, not strict wording repetition.
- Remove generic `개인 연락처:` from concrete leak markers while retaining phone/email leak patterns.
- Record L112 as best current diagnostic row for this loop.

## Partially Accepted

- The rerun-analysis worker initially classified q002 as a measurement artifact. Main review rejected that part after reading the answer: q002 was a true over-refusal/post-trim risk until L110.

## Rejected Or Guarded

- Do not relax all official-contact or evaluation-criteria questions out of sensitive guards.
- Do not compare L112 no-judge EDD `60.0` to judged EDD rows.
- Do not promote L108-L112 to strict validation.

## Best Diagnostic Result

- L112: coverage/MRR `1.0/1.0`, abstention accuracy `1.0`, false abstention `0.0`, field_score issues `{}`, empty answer `0.0`, latency `7.184s`, observed cost `$0.040586`, spend after run `$3.511722`.
