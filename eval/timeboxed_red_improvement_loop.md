# Timeboxed Red-Review Improvement Loop

## Purpose

Run measured RAG improvement loops within a time budget, without pretending that every higher score is a true generalization gain.

## Operating Rule

- The user may set a target stop time, for example "run until 20:00".
- The target time is a planning boundary, not a hard interrupt.
- Do not start a large new run near the target time.
- If a run is already in progress near the target time, finish the current safe unit, collect artifacts, and then close the loop.
- If the active unit may run far beyond the target, stop at the nearest checkpoint and record it as unfinished.

## Loop Shape

1. Select one improvement hypothesis.
2. Freeze the question cohort and run label.
3. Run the RAG answer path.
4. Score retrieval, answer quality, abstention behavior, and latency.
5. Inspect low-quality or suspicious high-score answers.
6. Apply a narrow fix only when the cause is clear.
7. Rerun the same cohort only as targeted retry evidence.
8. Run red review:
   - Was the validation set already exposed?
   - Did the judge change?
   - Did missing judge rows enter the average?
   - Did a speed gain hide answer-quality loss?
   - Did org backfill inject wrong documents?
   - Is the sample too small for a precise claim?
9. Label the result:
   - first-seen validation evidence
   - targeted retry evidence
   - diagnostic-only evidence
   - judge-calibration evidence
10. Record the result in `eval/experiment_log.md`, `eval/next_improvement_tasks.md`, and `업무일지.md`.

## Time Budget Defaults

- More than 90 minutes left: create or run one new measured cohort.
- 45-90 minutes left: run a focused failure-mode probe or judge-calibration check.
- 15-45 minutes left: finish active run, aggregate, graph, inspect answers, and write logs.
- Less than 15 minutes left: no new experiment; summarize, label scores, and list next tasks.

## Required Score Labels

- `tuned_score`: score on a set used for iteration.
- `first_validation_score`: first score on a not-yet-inspected validation set.
- `targeted_retry_score`: score after inspecting failures and fixing them.
- `diagnostic_only`: partial/no-judge/source-check result, not comparable with full EDD.
- `judge_calibration`: result testing whether the judge catches planted mistakes.

## Next Loop Priority

1. Create a new untouched validation set.
2. Run blind judge calibration with intentionally wrong or unsupported answers.
3. Stress-test org backfill false positives.
4. Reduce source-scope bleed in `qv2_003` and `qv2_008`.
5. Revisit adaptive `top_k` for latency only after the validity checks are clean.

