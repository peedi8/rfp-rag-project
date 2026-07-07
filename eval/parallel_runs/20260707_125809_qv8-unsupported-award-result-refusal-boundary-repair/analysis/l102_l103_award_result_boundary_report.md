# L102-L103 Award Result Boundary Repair

Diagnostic-only repair for qv8_a11 after L101 top5 shifted the unsupported-result refusal boundary.

| row | EDD | abstention | latency | note |
|---|---:|---:|---:|---|
| L98 qv8 raw top8 | 95.81 | 0.800 | 17.645s | raw diagnostic |
| L99 qv8 recomputed top8 | 97.81 | 1.000 | 17.645s | measurement repair |
| L101 qv8 full top5 before guard | 96.57 | 0.800 | 14.284s | faster but a11 failed |
| l102_a11_topk5_guard_topk5_only | 60.00 | 1.000 | 2.440s | diagnostic-only |
| l103_qv8_full_topk5_guard_topk5_only | 98.71 | 1.000 | 13.656s | diagnostic-only |

Cause: top5 reduced latency but let qv8_a11 drift into evaluation-rule exposition instead of a clean refusal.
Result: no-API fixtures pass 39/39; single a11 probe latency is 2.44s with abstention true; full qv8 top5 after guard reaches EDD 98.71, abstention 1.0, latency 13.656s.
Insight: the improvement is real within qv8 diagnostics because it fixes both the a11 boundary and speed, but it is still exposed diagnostic evidence.
Next: keep top5+guard as a candidate, then test on a non-qv8 unsupported-result mini-set before any default promotion.
