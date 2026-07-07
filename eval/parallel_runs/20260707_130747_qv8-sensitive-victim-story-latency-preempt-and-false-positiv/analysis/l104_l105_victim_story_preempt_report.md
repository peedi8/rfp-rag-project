# L104-L105 Victim Story Preempt Report

Diagnostic-only repair for qv8_a12 after L103 showed the sensitive victim-story refusal still spent most time in answer generation.

| row | EDD | abstention | latency | note |
|---|---:|---:|---:|---|
| L98 qv8 raw top8 | 95.81 | 0.800 | 17.645s | raw diagnostic |
| L99 qv8 recomputed top8 | 97.81 | 1.000 | 17.645s | measurement repair only |
| L103 qv8 top5 award guard | 98.71 | 1.000 | 13.656s | a11 fixed, a12 still slow |
| L104 qv8_a12 top5 victim preempt | 60.00 | 1.000 | 2.120s | no-judge single-case diagnostic |
| L105 qv8 top5 award+victim guards | 99.13 | 1.000 | 11.813s | diagnostic-only full qv8 rerun |

Cause: L99 fixed the evaluator's missed abstention label for qv8_a12, but it reused saved answers and therefore could not reduce generation time. L103 fixed qv8_a11 yet still left qv8_a12 at 22.06s because the model wrote a long refusal before the post-generation guard could trim it.

Change: add a narrow pre-generation boundary for requests that ask to invent or fabricate victim consultation stories or personal names, while preserving normal support-center scope questions. The no-API fixture pack now includes both a positive fabrication case and a support-center boundary case.

Result: L104 proved the targeted qv8_a12 path now returns before generation with latency 2.12s and negligible observed cost. L105 then reran the full qv8 diagnostic set with top5 plus the award-result and victim-story guards: EDD 99.13, coverage/MRR 1.0/1.0, groundedness/relevance 5.0/5.0, abstention accuracy 1.0, average latency 11.813s, and no answer-quality issues.

Insight: pre-generation refusal is the right tool only for requests that are impossible or unsafe to satisfy from the documents. It improved both speed and refusal shape for qv8_a11/a12, but the qv8 set is already exposed diagnostic evidence, so the 99.13 row must not be presented as strict validation.

Next: stop tuning qv8 for score. The next useful loop should test generalization on non-qv8 unsupported-result and sensitive-story prompts, and should add a field-level scorer for mixed official/private contact questions before those cases influence aggregate EDD.
