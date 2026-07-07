# L48 Evidence-Use Guard Red Review

## Bottom Line

Proceed only with a narrow no-API diagnostic/reporting guard. Do not add a broad generator-time rule that says any retrieved access-control term must be confirmed.

The qv6_007 failure is specific: target-only Goyang retrieval and source support exist, but the answer says physical access control cannot be confirmed. The guard should catch that exact evidence-use failure while staying out of EDD scoring and broad generalization claims.

## Accepted Risks

| risk | accept only if |
|---|---|
| qv6_007-specific guard overfits an exposed case | It is labeled `diagnostic_only_exposed_case`, `not_generalization_evidence`, and `not_edd_scoreboard`. |
| Literal marker checks are brittle | Markers are reported as evidence, and no-API false-positive fixtures cover negation, false friends, source leakage, and missing retrieval. |
| Claim gate can block report-ready promotion despite judge 5/5 | This is desired for L44-style judge blindness: judge score must not override a critical missing/underanswered claim. |

## Rejected Risks

| risk | why rejected |
|---|---|
| Broad access-control keyword rule | System/account/network access control is a false friend for physical entry/exit access-control purchase/install. |
| Whole-file source support | Source hits must be bound to retrieved chunk IDs or project-scoped rows/spans, not any matching text in a CSV file. |
| Retrieval-agnostic blame | If target evidence was not retrieved, label retrieval scope failure instead of generation evidence-use failure. |
| Positive marker beats negation | An answer that repeats the marker while saying it cannot be confirmed must fail by polarity. |
| Claim gate as scoreboard metric | The qv6_007 two-claim gate is diagnostic only and must not become EDD or system-wide preservation evidence. |

## False-Positive Cases To Prove

| case | expected label |
|---|---|
| Answer/source only mention account permissions, access logs, server/network access control, or security products | `no_guard_fire_false_friend_only` |
| Answer confirms physical access-control inclusion but says RFID/card/biometric/vendor/interface details are unknown | `pass_narrow_unknown_boundary` |
| Physical access-control marker exists only in another org/project | `blocked_source_scope_not_generation` |
| Retrieved orgs lack the target Goyang org | `retrieval_scope_fail_not_evidence_use_fail` |
| Retrieved context mixes target and non-target facility records | `mixed_org_warning_or_fail_by_strict_mode` |
| Answer echoes the access-control marker in a cannot-confirm sentence | `source_supported_but_answer_underanswered` |
| Source supports purchase/install but answer says it is absent | `source_supported_but_answer_contradicted` |
| Source supports the claim and answer omits it entirely | `source_supported_but_answer_missing_claim` |

## Reporting Labels

Use:

- `source_supported_but_answer_underanswered`
- `source_supported_but_answer_missing_claim`
- `source_supported_but_answer_contradicted`
- `false_friend_substitution_system_access_for_physical_access`
- `retrieval_scope_target_missing`
- `retrieval_scope_mixed_orgs`
- `source_scope_unbound_or_leaked`
- `blocked_expectation_or_source_gap`
- `diagnostic_only_exposed_case`
- `not_generalization_evidence`
- `not_edd_scoreboard`
- `report_ready_blocker`
- `judge_blindness_example`
- `partial_recovery_only`

Avoid:

- `qv6_007 is fixed`
- `physical access-control guard improves EDD`
- `claim preservation is generally solved`
- `judge 5/5 validates the answer`
- `any access-control evidence should always be confirmed`

## Proof Before Broad Paid Loops

Broad paid v7/v8/v9 loops should stay closed until all of this exists:

1. A no-API fixture pack covering the false-positive cases above.
2. A same-cohort qv6_007 replay/rerun with target-only retrieval, target-bound source support, and an answer that confirms physical access-control inclusion while keeping method/vendor/spec details narrow.
3. A parsed guard report with zero critical failures, no unbound source leakage, and explicit `diagnostic_only_exposed_case` / `not_edd_scoreboard` labels.
4. A regression check proving false-friend system/account/network access language does not satisfy physical access-control support.
5. An aggregation/reporting check proving claim-gate artifacts do not enter EDD scoreboard rows and judge 5/5 cannot override a critical guard failure.
6. A budget dry run proving the next loop would run the intended frozen cohort and would not expand paid scope merely because this exposed diagnostic passes.

## Commands Run

- `Get-Content -LiteralPath 'C:/Users/peedi/.codex/skills/eval-loop-orchestrator/SKILL.md'`
- `Get-Location; git status --short`
- `Get-Content -LiteralPath 'src/generator.py'`
- `Get-Content -LiteralPath 'src/retriever.py'`
- `Get-Content -LiteralPath 'scripts/check_claim_preservation.py'`
- `Get-Content -LiteralPath 'eval/claim_preservation_expectations.json'`
- `Get-Content -LiteralPath 'eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/summary/l47_claim_preservation_gate_report.md'`
- `Get-Content -LiteralPath 'eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/analysis/l47_claim_gate_l44_judge_blindness/claim_preservation_results.json'`
- `Get-ChildItem -LiteralPath 'eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs' -Force | Select-Object Name,Length,LastWriteTime`
- `Get-Content -LiteralPath 'eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs/l47_claim_gate_red.contract.json'`
- `Get-Content -LiteralPath 'eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs/l47_claim_gate_schema.contract.json'`
- `Get-Content -LiteralPath 'eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs/l44_cost_trace_onecase_withjudge_baseline_default/details.json'`
- `Get-Content -LiteralPath 'eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs/l40_v6_goyang_alias_retry_baseline_default/details.json'`
- `$p='eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs/l48_guard_red_review.contract.json'; $j=Get-Content -Raw -LiteralPath $p | ConvertFrom-Json; $j.schema; $j.task_id; $j.validation.commands_run.Count`
- `Get-Item -LiteralPath 'eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs/l48_guard_red_review.contract.json','eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs/l48_guard_red_review.md' | Select-Object Name,Length,LastWriteTime`
- `Select-String -LiteralPath 'eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs/l48_guard_red_review.md' -Pattern 'Proof Before Broad Paid Loops','No API/model calls were made'`

## Verification Notes

No API/model calls were made. No protected files were edited. `git status --short` could not be used because `I:\0706\rfp-rag-project` is not a git repository. The inspected L44 result shows target-only retrieval and a remaining `source_supported_but_answer_underanswered` physical access-control failure despite judge 5/5, so the proposed guard is justified only as a diagnostic/report-ready blocker.
