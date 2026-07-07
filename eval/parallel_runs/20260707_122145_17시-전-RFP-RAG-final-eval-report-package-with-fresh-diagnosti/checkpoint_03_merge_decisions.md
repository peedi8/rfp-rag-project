# Checkpoint 03 - Merge Decisions

## Accepted

- L97 fixture expansion: keep. No-API guard suite reached `33/33` after correcting one expectation.
- qv8 diagnostic set: keep as `diagnostic_only`, not strict validation. Mixed field-level candidate q20260707_a04 was excluded.
- L98 qv8 raw result: keep as raw saved run. EDD `95.81`, latency `17.645s`, observed cost `$0.126294`.
- L99 measurement correction: keep as recompute. EDD `97.81`, abstention accuracy `1.0`, fixtures `34/34`.
- Final report caveat: strict scoreboard remains L37 EDD `86.25`; L95 remains best source-exposed diagnostic row EDD `98.54`.

## Rejected Or Not Promoted

- Do not promote qv8 to held-out validation. It was generated after prior loop insights and includes diagnostic/source-exposed risk modes.
- Do not call L99 a model improvement. It is an evaluator correction over saved answers.
- Do not use the excluded official-contact/personal-contact candidate in aggregate scoring until field-level grading exists.

## Cause Result Insight

Cause: The high-score v7 loop was saturated, so the useful work shifted to boundary fixtures, semi-fresh diagnostic questions, and red-team caveats.

Result: qv8 confirmed strong retrieval and answer grounding, while exposing tail latency and one abstention-measurement blind spot.

Insight: The next gain is likely from latency decomposition and better evaluation granularity, not from more tuning on the same exposed v7 cohort.
