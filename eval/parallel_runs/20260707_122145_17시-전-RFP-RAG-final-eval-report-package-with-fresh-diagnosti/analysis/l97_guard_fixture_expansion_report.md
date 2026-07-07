# L97 Guard Fixture Expansion Report

## Purpose

L95 improved source-exposed v7 diagnostics, but the red-team risk was that the new preemptive sensitive abstention guard could become too broad. L97 therefore expanded the no-API fixture pack before making any new performance claim.

## Change

- Added marker-constant fixtures for the plain-language hint trigger and negation precedence.
- Added marker-constant fixtures for sensitive preempt positive and negative boundaries.
- Preserved the L96 `추정금액` boundary that prevents normal procurement budget wording from being treated as a fabrication request.

## Result

| check | value |
|---|---:|
| fixtures before L97 | `28` |
| fixtures after L97 | `33` |
| passed | `33` |
| failed | `0` |

One provisional fixture initially expected that a single final-result marker plus an explicit fabrication marker should not preempt. Review showed that expectation was too strict: asking for a final award/result to be estimated is exactly the class the preempt guard should refuse quickly. The fixture was relabeled as a positive trigger and the suite passed.

## Decision

Keep the L97 fixture expansion as a regression guard. It is not a new EDD score; it is evidence that the L95/L96 guard is less likely to regress on trigger boundaries.

## Insight

The safest next improvement is not to keep tuning the already-exposed v7 set. It is to keep adding cheap boundary checks and then run small, clearly labeled diagnostic cohorts that can reveal new failure modes without pretending to be strict validation.
