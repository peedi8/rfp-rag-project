# L100-L101 qv8 Latency Loop Report

## Scope

This loop is diagnostic-only. It uses qv8 and a qv8 tail slice after L98/L99 inspection, so it must not be promoted to strict validation.

Strict scoreboard remains L37 EDD 86.25. L95 remains the strongest source-exposed diagnostic row at EDD 98.54. L99 qv8 recompute remains measurement repair at EDD 97.81.

## Cause

L98/L99 showed qv8 retrieval and judge quality were saturated, but latency tails remained high. Stored traces showed the slow cases were mostly generation-heavy:

- Five selected tail cases averaged 25.026s in the prior qv8 trace.
- Generation accounted for about 94.9% of those tail latencies.
- a01 was the only notable retrieval outlier; most other slow cases were long refusal or comparison answers.

## Changes Tested

Three small candidates were tested on a five-case qv8 latency-tail probe:

| config | EDD | abstention | avg latency | decision |
|---|---:|---:|---:|---|
| baseline top8 | 97.11 | 1.000 | 20.736s | control |
| top5 | 98.00 | 1.000 | 16.798s | promising on tail slice |
| concise_verified prompt | 86.53 | 0.000 | 23.280s | rejected |

Then top5 was tested on the full qv8 diagnostic set:

| config | EDD | coverage | MRR | groundedness | relevance | abstention | avg latency | decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| qv8 raw baseline top8 | 95.81 | 1.000 | 1.000 | 5.000 | 5.000 | 0.800 | 17.645s | prior raw diagnostic |
| qv8 recomputed top8 | 97.81 | 1.000 | 1.000 | 5.000 | 5.000 | 1.000 | 17.645s | measurement repair |
| qv8 full top5 | 96.57 | 1.000 | 1.000 | 5.000 | 5.000 | 0.800 | 14.284s | speed candidate, not adopted |

## Result

Top5 did reduce full-qv8 average latency from 17.645s to 14.284s, a reduction of 3.361s per question. It also kept coverage, MRR, groundedness, and relevance at ceiling.

However, top5 did not preserve the recomputed qv8 abstention profile. The failure moved to `q20260707_a11_dbrain_award_score_and_vendor`: the answer said the final evaluation score and selected vendor could not be confirmed, but then continued with a long evaluation-formula explanation. The current abstention detector does not count that as a full refusal.

Prompt concision was rejected because it reduced abstention accuracy to 0.0 on the five-case slice and did not improve latency.

## Insight

Context reduction is a real latency lever, but it is not yet a safe default. It appears helpful on generation-heavy tails, yet it can shift refusal boundary behavior on unsupported award-result questions.

The better next step is not to promote top5 globally. The next useful loop is to isolate unsupported-result refusal shape, add a narrow guard or evaluator distinction if justified, and then rerun the qv8 full top5 comparison.

## Next

1. Keep qv8 and L100/L101 as diagnostic-only evidence.
2. Do not adopt global top5 yet.
3. Add a focused unsupported-award-result refusal-shape probe around a11.
4. Keep field-level contact/privacy scoring as a separate diagnostic panel before reintroducing the excluded mixed-contact qv8 candidate.
5. Report top5 as "latency improved but safety/abstention boundary still unresolved."
