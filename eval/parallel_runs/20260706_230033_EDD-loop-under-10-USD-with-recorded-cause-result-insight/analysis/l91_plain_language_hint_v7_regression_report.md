# L91 Plain-Language Hint V7 Regression Report

## Purpose

L89 improved qv7_009, but it was a one-case source-exposed probe. L91 reran the full v7 source-exposed diagnostic set to check whether the query-specific plain-language hint caused obvious regressions elsewhere.

## Result

| metric | value |
|---|---:|
| EDD | `97.82` |
| coverage | `1.0` |
| MRR | `1.0` |
| groundedness | `5.0` |
| relevance | `5.0` |
| abstention accuracy | `1.0` |
| avg latency | `17.613s` |
| answer quality issue rows | `0/12` |
| observed cost | `$0.171454` |

qv7_009 after the hint:

- `718` chars
- `9` lines
- `5` bullets
- judge `5/5`
- `answer_quality_issues=[]`

## Decision

Keep the hint as a guarded candidate repair. Do not call it fresh validation because the set is source-exposed. Do not claim a speed win because L91 is slightly slower than L85 topk8 control and qv7_006 had a `28.81s` tail.

## Next Gate

Either test false positives for the plain-language trigger or investigate qv7_006 tail latency.
