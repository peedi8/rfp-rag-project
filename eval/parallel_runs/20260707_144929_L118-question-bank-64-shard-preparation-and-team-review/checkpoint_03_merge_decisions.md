# Checkpoint 03 - Merge Decisions

## Decision

Keep the 64-case physical split as written. Do not swap cases after worker review.

## Accepted Worker Findings

- Shard A: keep Q001-Q012 as metadata/corpus core, keep Q065 as acronym/corpus bridge, and keep Q033-Q035 physically in A only as a quarantined `ordinary_rag_text_cluster_comparison` sublane. Do not fold Q033-Q035 into the metadata analytics subtotal.
- Shard B: keep all 16. Execute as two lanes: Q024/Q026/Q027 ordinary single-document controls, and Q038-Q050 selected-project contract/technical extraction after fixed project seeds are written.
- Shard C: keep all 16. Execute with buckets for selected-project technical extraction, corpus-wide technical discovery, ambiguity correction, follow-up memory, and unsupported boundary.
- Shard D: keep all 16. Execute with sublanes for unsupported guarantee boundary, persona usefulness, system citation transparency, and business recommendation boundary.

## Rejected Changes

- Do not physically move Q033-Q035 out of A for this 64 split, because replacing them with D cases would only move the lane impurity elsewhere.
- Do not run Q090-Q091 as ordinary answer rows unless retrieval/citation trace artifacts are available.
- Do not execute selected-project rows before seed projects and seed turns are recorded.

## Next Execution Gate

Before any answer run, write lane-specific runnable manifests with seed contexts and sidecar metrics. Preserve raw first execution separately from later repair or measurement correction.
