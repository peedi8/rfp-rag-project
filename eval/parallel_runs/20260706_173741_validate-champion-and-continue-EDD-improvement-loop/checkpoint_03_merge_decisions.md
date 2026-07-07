# Checkpoint 03 - Merge Decisions

- holdout_validation: accepted with follow-up. Initial holdout EDD 81.55 exposed generalization failures; after targeted backfill/abstention fixes, holdout recomputed EDD 96.80.
- judge_bias_check: accepted as measurement evidence. Balanced context is mostly fair correction, not pure leniency, but qv2_003 remains a real source-scope risk.
- latency_candidate_review: accepted as next-experiment proposal. Keep top8 champion; test adaptive top5 fast path with top8 fallback.
- quality_audit: accepted. Reject global top5 as champion because of qualitative regressions.

Remaining follow-ups:
- qv2_003 and qv2_008 source-scope/citation guard.
- adaptive top_k experiment with holdout revalidation.
