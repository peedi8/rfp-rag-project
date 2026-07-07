# Overfit Gate Proposal

## Purpose

Prevent the improvement loop from converting reused validation evidence into final generalization claims. The gate should label each result by question-set exposure, judge status, and whether failures from that same set influenced later code, prompt, retrieval, or metric changes.

## Evidence Read

- `eval/parallel_runs/20260706_1825_timeboxed-red-loop-v3-validation/loop_points.csv`
- `eval/parallel_runs/20260706_1825_timeboxed-red-loop-v3-validation/loop_report.md`
- `eval/questions_v2*.json`
- `eval/questions_v3_validation.json`
- `eval/experiment_log.md`
- `eval/next_improvement_tasks.md`

## Proposed Labels

- `strict_first_validation`: first full judged run on an untouched set after the candidate configuration is frozen.
- `measurement_correction_same_answers`: same saved answers re-scored after a narrow evaluator/taxonomy correction; useful, but not a new RAG run.
- `targeted_retry_same_set`: rerun after inspecting failures from the same set or patching behavior for those failures.
- `diagnostic_only`: local retrieval/source probes, no-judge answer probes, dry-runs, calibration-pack generation, fake-client checks, or rows missing groundedness/relevance.
- `overfit_risk`: same validation/holdout set influenced fixes, prompt changes, retrieval rules, top-k routing, alias/backfill rules, or evaluator taxonomy before a later score on that same set.
- `needs_new_validation`: any final/generalization claim after a set has been used for tuning, targeted failure analysis, retry selection, metric correction, or judge calibration design.

## Set Reuse Rules

1. `questions_v2_tune.json` is tuning evidence only. Scores such as 95.55 can be called tuned-set champion scores, not final validated scores.
2. `questions_v2_holdout.json` is no longer strict held-out evidence after its failures were inspected and used for targeted fixes. Its first strict result, 81.55, remains the generalization warning signal; later 96.80 must be labeled as same-holdout targeted-fix remeasurement.
3. v2 probe files such as groundedness, compare, and holdout-failure probes are diagnostic subsets. They cannot support final performance claims.
4. `questions_v3_validation.json` was a fresh validation set for L0, but it has now been used for top5/top8 comparisons, alias/filter diagnostics, qv3_010 targeted probes, adaptive top-k guard design, and prompt candidate preparation. L0 89.69 is first raw evidence; L1 96.36 is measurement correction; further claims on v3 require `overfit_risk` unless a new untouched split is created.
5. If `questions_v3_tune.json` / `questions_v3_holdout.json` are created from the existing v3 file after seeing v3 results, they should not be described as fully untouched. They may be useful for regression coverage, but final generalization needs a separately authored or time-separated validation set.

## Contamination Checks

- Compare each run's question_set against a registry of exposed sets and case IDs.
- Mark a set as exposed once any case-level answer, failure reason, retrieved chunk list, judge reason, or manual quality review is inspected.
- Mark a run contaminated if the candidate includes changes motivated by failures from the same set.
- Mark judge contamination if scoring rules, abstention taxonomy, judge context formatting, or rubric sensitivity were changed after viewing answers from the same set.
- Mark retrieval contamination if aliases, org filters, source-scope guards, backfill, pruning, or adaptive top-k routing were changed based on cases in the evaluated set.
- Mark prompt contamination if prompt variants are created from representative answers or quality-review matrices drawn from the same set.
- Mark leaderboard contamination if no-judge/missing-judge rows enter ranked graphs or if recomputed rows replace first-run logged evidence.

## Final Claim Evidence Rules

Allowed for final performance claims:

- First full judged run on an untouched validation set, with question set fixed before candidate changes.
- Judge-calibrated scoring, where planted wrong-document/hallucinated answers are caught before the judged run is trusted.
- Complete metrics only: retrieval coverage, hit-all/MRR where applicable, groundedness, relevance, abstention, latency, run id, question-set id, and exact config.
- Clear claim label: tuned score, first validation score, measurement correction, same-set retry, diagnostic-only, or final validation.

Not allowed for final performance claims:

- No-judge probes, dry runs, fake-client checks, local retrieval diagnostics, source evidence probes, calibration-pack generation, or rows with incomplete judge fields.
- Same-set retries after case-level failure inspection.
- Recomputed metrics that replace the original first-run score without preserving the original.
- v2 holdout post-fix 96.80 as strict held-out performance.
- v3 post-L0/L1 targeted qv3_010/top-k/prompt results as new generalization evidence.

## Recommended Gate Decision

For the current headless loop, require:

- `overfit_risk` on any proposal claiming improvement from reused v2 holdout or reused v3 validation.
- `needs_new_validation` before any final report says the system generalizes at 96+ EDD.
- A new untouched validation set plus blind judge calibration before promoting a performance claim.
- A summary table that preserves first-run raw scores beside corrections/retries instead of overwriting them.
