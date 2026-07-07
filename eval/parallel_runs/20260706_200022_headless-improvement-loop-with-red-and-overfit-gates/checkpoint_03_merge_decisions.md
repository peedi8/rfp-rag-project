# Checkpoint 03 - Merge Decisions

## Accepted

- Adopt the promotion states: `promote`, `hold`, `diagnostic_only`, `candidate_only`, `overfit_risk`, `reject`, `needs_new_validation`.
- Treat same-answer recomputation as measurement correction, not model improvement.
- Treat no-judge, local diagnostic, qualitative review, and prompt/code guard rows as non-performance evidence.
- Preserve first validation scores separately from targeted retries and same-set reruns.
- Make blind judge calibration the next scored gate before trusting another near-ceiling EDD claim.

## Rejected Or Deferred

- Do not automatically promote the row with the highest EDD.
- Do not treat the v2 post-fix same-holdout score as strict generalization.
- Do not run broad top-k/fetch sweeps before judge/overfit gates are trusted.
- Do not claim `report_ready` improvement until a scored prompt sweep is run.

## Current Gate Decision

- L0 remains the best promotable first-validation evidence: EDD 89.69.
- L1 remains the best corrected/measurement point: EDD 96.36, but not a model improvement by itself.
- L14 is a gate/audit result and carries no EDD.

