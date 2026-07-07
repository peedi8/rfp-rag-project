# v7 Perturbation Proposal Evidence

This worker was proposal-only. It inspected the frozen v5 adversarial questions, the local R&D eval-methods note, the adversarial analyzer, the experiment worker contract shape, and the run ledger. It did not call paid APIs and did not modify protected paths.

## Main Design

- Use a run-local shadow corpus and shadow vector index only.
- Add decoy near-duplicates that are semantically tempting but wrong on organization, scope, final procurement facts, or title-derived assumptions.
- Add gold-ablation runs where target evidence is removed and the correct behavior is abstention.
- Add generic-title controls where title fragments are retrievable but insufficient for factual claims.
- Optionally add rank-shuffle replays to distinguish retriever errors from generator top-rank susceptibility.

## Metrics To Add

- `decoy_hit_rate_at_8`
- `decoy_first_hit_rank`
- `gold_retained_rank_delta`
- `false_positive_title_rate`
- `gold_ablation_non_abstention_rate`
- `unsupported_claim_rate_under_ablation`
- `cited_decoy_count`
- `answer_flip_rate_under_rank_shuffle`
- `non_target_org_rate_delta`

## Corpus Safety

All perturbation documents should live under the run directory, carry explicit synthetic metadata, and be excluded from production ingestion. The future runner should fail closed if its output path resolves outside the current parallel run's `worker_outputs` directory.
