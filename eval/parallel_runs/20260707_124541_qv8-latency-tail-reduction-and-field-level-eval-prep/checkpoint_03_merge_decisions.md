# checkpoint_03_merge_decisions.md

## Merge Decisions

| item | decision | reason |
|---|---|---|
| qv8 latency-tail probe file | accepted | Needed to compare slow-case latency under controlled diagnostic-only labeling. |
| exposure registry entry for `questions_v8_l100_latency_tail_probe.json` | accepted | Prevents accidental scoreboard promotion. |
| five-case top5 candidate | accepted as diagnostic evidence | Latency improved from `20.736s` to `16.798s` with abstention retained on the tail slice. |
| prompt-wide concision | rejected | Five-case abstention accuracy collapsed to `0.0` and latency worsened. |
| full qv8 top5 | accepted as diagnostic evidence, not adopted | Latency improved to `14.284s`, but abstention stayed `0.8` and qv8_a11 failed. |
| field-level contact/privacy scoring design | accepted as future task | Existing aggregate EDD cannot fairly score mixed public/private fields. |

## Final Loop Decision

Do not change the global retrieval default yet. Top5 is now a candidate for a future adaptive setting, but only after unsupported award-result refusal shape is repaired or the evaluator granularity is explicitly changed and justified.
