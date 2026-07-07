# Worker C Quality Red-Team Summary

Status: proposal only. No model calls, no evaluator/judge/generator calls, and no protected paths modified.

## Report-Worthy Caveats

1. **Source-exposed score caveat**: keep L37 as the only strict scoreboard row (`EDD 86.25`). L95 is the strongest source-exposed diagnostic row (`EDD 98.54`, latency `14.44s`, clean answer-quality issues), not fresh validation.

2. **qv7_006 high-score safety-tail caveat**: L81 had `EDD 97.41`, coverage/MRR `1.0`, judge `5/5`, and abstention accuracy `1.0`, but the answer refused final result fields and then continued with claim-flow/contact details. Report this as the clearest example that binary abstention plus judge 5/5 can hide unsafe refusal-tail detail.

3. **No-judge/non-comparable EDD caveat**: L83 and L94 should not be ranked by EDD. L83 intentionally omitted judge scores; L94 is latency/cost evidence only because abstention rows do not receive normal judge scores.

4. **Judge-blindness caveat**: qv6_007 L44 received judge `5/5` but failed claim preservation (`physical_access_control_system` source-supported but underanswered). Claim preservation/source-scope checks need to sit beside ordinary groundedness/relevance judging.

5. **qv7_009 answer-format caveat**: the answer was grounded but over-structured for a plain-language user request. L87 flagged `plain_language_answer_over_structured`; L89/L91 are candidate repairs, not fresh validation.

6. **Tail latency and artifact caveat**: L84 timed out before writing result/cost artifacts, and topk12 later had max latency `36.95s` with lower groundedness/relevance. Average latency and EDD need max/tail latency plus artifact completeness.

7. **Preempt false-positive caveat**: L95 sensitive preempt is promising, but L96 had to narrow markers to avoid `추정금액` false positives. Report it as a guarded candidate, not a fully validated rule.

8. **Source-purity caveat**: same-issuer/project-scope failures show org coverage is not enough; source markers must bind to the target project row, not the whole CSV or issuer.
