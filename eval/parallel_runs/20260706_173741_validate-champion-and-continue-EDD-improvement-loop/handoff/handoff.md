# Handoff

Objective: validate champion and continue EDD improvement loop.

Accepted evidence:
- Initial holdout rejected naive final claim: EDD 81.55.
- Targeted retrieval backfill and abstention taxonomy fix recovered holdout to EDD 96.80 after recomputation.
- Judge-bias recheck: old first-slice groundedness 2.0 vs balanced 4.714; balanced is not purely lenient because qv2_003 remains low.
- Global top5 rejected; adaptive top_k is the next experiment.

Next actions:
- Fix qv2_003/qv2_008 source-scope bleed.
- Test adaptive top_k on tune and holdout.
- Keep recording user review/red-team feedback in ????.md and eval/experiment_log.md.
