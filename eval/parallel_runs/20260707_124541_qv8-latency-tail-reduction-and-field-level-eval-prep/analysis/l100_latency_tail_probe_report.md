# L100 qv8 Latency-Tail Probe

Diagnostic-only five-case probe selected from qv8 high-latency cases after L98/L99 inspection. It is not fresh validation.

| config | EDD | coverage | MRR | groundedness | relevance | abstention | avg latency | decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| topk5_only / topk5_filter_rewrite | 98.00 | 1.000 | 1.000 | 5.000 | 5.000 | 1.000 | 16.798s | candidate for full-qv8 confirmation |
| baseline_default / baseline_default | 97.11 | 1.000 | 1.000 | 5.000 | 5.000 | 1.000 | 20.736s | control baseline |
| prompt_concise_verified_only / prompt_concise_verified | 86.53 | 1.000 | 1.000 | 5.000 | 5.000 | 0.000 | 23.280s | reject: abstention collapsed |

Cause: L98/L99 left qv8 tail latency around 20-31s, mostly generation-heavy rather than retrieval-heavy.
Result: top5 reduced the five-case average latency from 20.736s to 16.798s while keeping abstention, coverage, MRR, groundedness, and relevance at ceiling. concise_verified dropped abstention accuracy to 0.0 and is rejected.
Insight: context reduction appears safer than changing the answer style prompt; prompt variants can accidentally remove refusal behavior.
Next basis: run top5 over the full qv8 diagnostic set before considering any broader config or adaptive-top-k change.
