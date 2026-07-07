# L84-L86 V7 Latency and Measurement Report

- question set: `questions_v7_source_exposed_prompt_diagnostic_frozen.json`
- status: diagnostic-only, source-exposed
- strict validation: no

## L84 Failure

The first L84 run attempted the full `topk_sweep` in one process. It timed out before writing `results.csv`, `details.json`, or `cost_summary.json`.

Decision: reject this run design. Any API calls made before the timeout are not locally reconciled, so local cost totals may undercount true spend.

## L85 Shards

The runner was extended with `topk5_only`, `topk8_only`, and `topk12_only` so each setting writes artifacts independently.

After L86 measurement correction:

| shard | EDD | avg latency | max latency | quality notes | cost |
|---|---:|---:|---:|---|---:|
| topk5 | `97.99` | `16.865s` | `25.85s` | clean automated gates | `$0.154740` |
| topk8 control | `98.00` | `16.794s` | `23.46s` | clean automated gates | `$0.174094` |
| topk12 | `95.51` | `19.922s` | `36.95s` | groundedness/relevance `4.667/4.889` | `$0.211768` |

Observed shard cost: `$0.540602`.

## L86 Measurement Correction

L85 initially revealed abstention classification artifacts:

- Partial answers with confirmed scope plus an unknown subclaim were sometimes counted as full refusals.
- Sensitive patient-example refusals could be missed when the answer began with project metadata.
- A `[지문]` marker answer could be misclassified because a trailing personal-contact note interacted with an early unknown marker.

Fix:

- refined `is_abstention`
- expanded no-API fixtures to `21/21`
- recomputed saved worker metrics without new model calls

## Decision

Reject topk12. Do not adopt topk5. Keep topk8 as the current diagnostic control, not as a new optimization or validation claim. The useful durable improvements are sharded execution and the abstention measurement correction.
