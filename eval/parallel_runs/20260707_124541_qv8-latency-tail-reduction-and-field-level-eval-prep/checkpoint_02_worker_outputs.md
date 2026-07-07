# checkpoint_02_worker_outputs.md

All four proposal workers completed and wrote valid `parallel_team_worker_output.v1` contracts.

| task | output | accepted signal |
|---|---|---|
| latency_trace_audit | `worker_outputs/latency_trace_audit.contract.json` | Tail latency is mostly generation-heavy; a01 also has retrieval outlier behavior. |
| candidate_latency_fixes | `worker_outputs/candidate_latency_fixes.contract.json` | Adaptive/top5 context reduction is a plausible speed lever; prompt-wide concision is risky. |
| field_level_eval_design | `worker_outputs/field_level_eval_design.contract.json` | Mixed public official-contact and private/personal-info questions need field-level scoring, not aggregate EDD. |
| report_update_plan | `worker_outputs/report_update_plan.contract.json` | Keep L37 strict, L95 source-exposed diagnostic, qv8 raw/recomputed diagnostic-only. |

Worker outputs were proposal-only. Protected final files were merged only by the main orchestrator.
