# checkpoint_03_merge_decisions.md

Pending.
# Checkpoint 03 - Merge Decisions

## Accepted

- Added `scripts/run_sparse_field_guard.py`.
- Ran the no-API sparse-field guard on the L121 secondary technical ADD variants.
- Preserved guard outputs under `analysis/sparse_field_guard/`.
- Accepted the red-team warning that secondary variants must not enter ordinary EDD or headline performance claims.
- Accepted the source-basis correction: sparse/not-found field decisions must use raw HWP/PDF text or retrieval traces where possible, not the truncated CSV text alone.

## Rejected Or Deferred

- Rejected promotion of L122 as an EDD improvement point.
- Rejected a full answer run from the secondary variants before aggregation labels are fixed.
- Deferred true sparse-field not-found scoring until a genuinely sparse selected-project seed is chosen or a trace-backed answer run exposes an actual padding failure.

## Next

- Add an aggregation/registry guard that forces `secondary_variant` rows to diagnostic-only even when their batch JSON still says `ordinary_edd_candidate=true`.
- If testing sparse not-found behavior next, first search for a truly sparse technical seed under raw source text.
- For a cheap execution next, prefer a small resolved-one-turn smoke with diagnostic labels, not the full 35/71-call batch.
