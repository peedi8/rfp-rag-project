# Checkpoint 03 - Merge Decisions

## Accepted Changes

- Keep `scripts\build_adversarial_v5.py`.
- Keep `scripts\analyze_adversarial_run.py`.
- Keep exposure-registry updates for v5 files.
- Keep `src\retriever.py` title-fragment issuer filtering.
- Keep `scripts\evaluate.py` narrow sensitive-example refusal detection and narrowed procurement marker counting.
- Keep updated loop table, chart, experiment log, next-task list, and L30-L36 report.

## Rejected Or Not Promoted

- Do not call L33/L34 fresh validation. They are same-answer measurement corrections after v5 exposure.
- Do not promote global top5. v5 looks fast after correction, but v4 regression did not confirm a better default.
- Do not replace L25 as the current promotable v4 evidence. L25 EDD `97.41` remains the best first-run v4 validation row.

## Evidence Labels

- L30: first v5 evidence.
- L31: local retrieval/code diagnostic.
- L32: targeted fix raw score with measurement issue.
- L33/L34: same-answer measurement corrections.
- L35/L36: v4 regression evidence.

## Next Gate

- A new v6 set is required before claiming generalization from the title-fragment filter.
- Add false-positive title-fragment probes before further tightening the filter.
