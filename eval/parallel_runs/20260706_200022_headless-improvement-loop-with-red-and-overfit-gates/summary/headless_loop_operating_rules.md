# Headless Loop Operating Rules

- run_dir: `eval\parallel_runs\20260706_200022_headless-improvement-loop-with-red-and-overfit-gates`
- mode used in this loop: no-api gate audit
- current loop point: L14
- EDD: N/A

## Accepted Rules

1. Keep running improvement loops, but do not promote the highest EDD automatically.
2. Separate every result into one of these states:
   - `promote`
   - `hold`
   - `diagnostic_only`
   - `candidate_only`
   - `overfit_risk`
   - `reject`
   - `needs_new_validation`
3. A row can be promoted only when it is a fresh scored validation or comparable scored run with complete judge metrics.
4. Same-answer recomputation, no-judge probes, local diagnostics, qualitative review, and prompt/code guards are useful evidence but not performance scores.
5. If a failure case is inspected and then the same set is rerun, the later score is a targeted/reused-set result, not strict generalization.
6. Near-ceiling automated scores must pass blind judge calibration or equivalent safety checks before being trusted for final claims.
7. Human-quality and evidence-safety gaps remain active risks even when EDD is high.

## Current Gate Audit

- rows checked: 14
- promotable rows: 1
- best promotable evidence: L0 `v3_first_validation_top8_raw`, EDD 89.69
- best corrected/measurement point: L1 `v3_top8_same_answers_recomputed`, EDD 96.36
- active flags:
  - latency risk
  - metric saturation risk
  - near-ceiling score risk
  - no-judge rows are not performance scores
  - measurement correction is not model improvement
  - targeted/reused case risk
  - human quality gap
  - evidence safety gap

## Next Priority

1. Judge calibration gate on the existing planted 6-case pack. This is optional paid judge-only work; if cost is locked, keep it as pending and do no-api checks only.
2. Small scored `prompt_report_ready` sweep against existing prompt variants, only after the judge gate is trusted.
3. Small adaptive top-k validation, only after the quality gate is trusted.
4. Fresh untouched validation set before any final generalization claim.

## Decision

L14 is accepted as a gate/audit loop point, not a performance improvement. It makes the automated loop safer: future loops may continue, but only results passing the red/overfit gates can be promoted.

