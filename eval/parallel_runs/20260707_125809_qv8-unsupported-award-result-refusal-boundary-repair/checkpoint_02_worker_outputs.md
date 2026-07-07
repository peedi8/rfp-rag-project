# checkpoint_02_worker_outputs.md

All four proposal workers completed and wrote local JSON contracts.

| task | output | useful signal |
|---|---|---|
| a11_answer_shape_audit | `worker_outputs/a11_answer_shape_audit.contract.json` | L101 a11 failure was answer shape, not retrieval. |
| evaluator_boundary_design | `worker_outputs/evaluator_boundary_design.contract.json` | Need three-way boundary: full refusal, partial supported answer with caveat, over-detailed refusal tail. |
| generator_guard_candidate | `worker_outputs/generator_guard_candidate.contract.json` | Narrow final-award-result preempt is safer than broad evaluation-term blocking. |
| probe_and_report_plan | `worker_outputs/probe_and_report_plan.contract.json` | qv8_a11 probes and report caveats should stay diagnostic-only. |

Worker outputs were proposal-only. The main orchestrator merged only the narrow fixture, evaluator, guard, registry, and probe changes.
