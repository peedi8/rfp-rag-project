# checkpoint_03_merge_decisions.md

## Merge Decisions

| item | decision | reason |
|---|---|---|
| Award-result no-API fixtures | accepted | They lock qv8_a11-style unsupported final-result refusals and protect criteria answers with caveats. |
| `is_abstention` evaluation-criteria lead-in exception | accepted | Prevents supported criteria answers from becoming false full abstentions merely because they mention unavailable final results. |
| Final-award/result generator markers | accepted | Narrowly targets final evaluation score / selected vendor / calculation requests. |
| `questions_v8_l102_award_result_probe.json` | accepted | Single-case diagnostic proof that qv8_a11 repair works without extra model generation. |
| L103 full qv8 top5 rerun | accepted as diagnostic evidence | Confirms the targeted repair improves qv8 top5 EDD, abstention, and latency together. |

## Decision

Keep the guard and the evaluator boundary fix. Treat L103 as the current best qv8 diagnostic row, not as strict validation. Before changing a global default, test the final-award-result guard on a non-qv8 mini-set.
