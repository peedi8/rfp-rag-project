# checkpoint_03_merge_decisions.md

## Merge Decisions

- Accepted: `intent_taxonomy`.
  - Final taxonomy keeps 12 realistic user-intent families.
- Accepted: `gate_design`.
  - Adopted `rfp_rag_user_intent_gate_v10.0.0`.
  - EDD remains gate-versioned; sidecar blockers decide usability.
- Accepted: `corpus_feasibility`.
  - Every future v10 candidate must declare `answerability_source`.
  - Exact value/deadline cases require body-visible support unless labeled metadata diagnostic.
- Accepted: `red_report`.
  - V10 is taxonomy/gate design only, not a new EDD result.
  - Source-inspected or prior-failure-derived question sets stay diagnostic-only unless a true untouched source pool is frozen before answers.

## Created Orchestrator Artifacts

- `analysis/v10_realistic_intent_taxonomy_gate_report.md`
- `analysis/v10_realistic_intent_taxonomy.json`

## Final Decision

Do not run answers yet. Next step is to create a 12-16 case v10 question file only after exposure, metadata/body-visibility, and retrieval-preview checks.
