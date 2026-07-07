# Checkpoint 02 - Worker Outputs

Created: 2026-07-06 23:20 KST
Updated: 2026-07-07 00:20 KST

## Proposal Contracts

| task | contract | status | merge posture |
|---|---|---|---|
| v6_metamorphic | `worker_outputs/v6_metamorphic.contract.json` | proposal complete | accepted partially; materialized as frozen v6 first-run cohort |
| v7_perturbation | `worker_outputs/v7_perturbation.contract.json` | proposal complete | accepted as next-loop design, not yet run broadly |
| v8_claim_audit | `worker_outputs/v8_claim_audit.contract.json` | proposal complete | accepted as answer-quality and unsupported-claim audit direction |
| v9_latency_cost | `worker_outputs/v9_latency_cost.contract.json` | proposal complete | accepted as required before broader paid runs |
| l41_claim_pair_audit | `worker_outputs/l41_claim_pair_audit.contract.json` | proposal complete | accepted as no-API claim-level audit evidence |
| l41_qv6_010_ambiguity_review | `worker_outputs/l41_qv6_010_ambiguity_review.contract.json` | proposal complete | accepted as no-API over-answer gate evidence |
| l41_cost_trace_design_review | `worker_outputs/l41_cost_trace_design_review.contract.json` | proposal complete | accepted; implementation patch followed actual `src/rag.py` path |
| l47_claim_gate_schema | `worker_outputs/l47_claim_gate_schema.contract.json` | proposal complete | accepted partially; materialized as deterministic qv6_007 claim-preservation expectation |
| l47_claim_gate_red | `worker_outputs/l47_claim_gate_red.contract.json` | proposal complete | accepted; row-scoped source matching and false-friend access-control guard added |

All proposal workers reported `directly_modified_protected_paths: []`.

## Executed Loop Points

| loop | file | result | note |
|---|---|---:|---|
| L37 | `worker_outputs/l37_v6_metamorphic_first_baseline_baseline_default/worker_output.json` | EDD 86.25 | first v6 run; valid first-run evidence |
| L38 | `worker_outputs/l38_v6_safety_prompt_retry_baseline_default/worker_output.json` | diagnostic | targeted abstention retry only |
| L39 | `worker_outputs/l39_v6_goyang_order_depth_probe_topk_sweep/worker_output.json` | diagnostic | top_k depth probe for one exposed case |
| L40 | `worker_outputs/l40_v6_goyang_alias_retry_baseline_default/worker_output.json` | diagnostic | alias retry for one exposed case |
| L41 | `worker_outputs/l41_claim_pair_audit.contract.json` | no-API diagnostic | qv6_006/qv6_007 claim-level comparison |
| L41 | `worker_outputs/l41_qv6_010_ambiguity_review.contract.json` | no-API diagnostic | generic-title ambiguity over-answer review |
| L42 | `worker_outputs/l42_cost_trace_dryrun_embedding_baseline_default/worker_output.json` | dry-run diagnostic | cost trace artifact schema smoke |
| L43 | `worker_outputs/l43_cost_trace_onecase_nojudge_baseline_default/worker_output.json` | diagnostic | one actual no-judge cost trace probe |
| L44 | `worker_outputs/l44_cost_trace_onecase_withjudge_baseline_default/worker_output.json` | diagnostic | one actual judge-included cost trace probe |
| L47 | `analysis/l47_claim_gate_l37_first_run/claim_preservation_results.json` | no-API diagnostic | L37 qv6_007 claim preservation 0/2 |
| L47 | `analysis/l47_claim_gate_l40_alias_retry/claim_preservation_results.json` | no-API diagnostic | L40 qv6_007 claim preservation 1/2 |
| L47 | `analysis/l47_claim_gate_l44_judge_blindness/claim_preservation_results.json` | no-API diagnostic | L44 qv6_007 claim preservation 1/2 despite judge 5/5 |

## Key Observations

- L37 dropped to EDD 86.25 because abstention accuracy was 0.0 on unsupported final-procurement and generic-title traps.
- L38 fixed the two targeted abstentions, but qv6_010 still over-answers after saying the title fragment is ambiguous.
- L39 showed top_k alone does not fix the qv6_007 metamorphic failure.
- L40 fixed the Goyang alias binding and moved the target to rank 1, but latency regressed and physical access-control evidence remained underused.
- L41 claim audit confirms L40 is partial recovery only: unmanned/HW linkage recovered; physical access-control remains underanswered.
- L41 ambiguity review defines `ambiguous_identifier_refusal_with_excessive_candidate_summary`.
- L43 verified cost tracing with one actual no-judge call: `query_embedding` plus `answer_generation`, observed local-table cost `$0.008312`.
- L44 verified judge-included tracing with one actual call: `query_embedding`, `answer_generation`, and `judge`, observed local-table cost `$0.013187`.
- L44 also shows judge blindness: groundedness/relevance were 5/5 while paired claim audit still flags access-control under-answer.
- L47 turns that paired claim audit into a deterministic no-API gate. It keeps L40 as partial recovery only and labels L44 as a judge-blindness example.

## L48-L76 Additions

| loop | file | result | note |
|---|---|---:|---|
| L48 | `worker_outputs/l48_evidence_use_guard_design.contract.json` | proposal | accepted as narrow evidence-use guard design |
| L48 | `worker_outputs/l48_guard_red_review.contract.json` | proposal | accepted; warned against broad keyword repair and global source borrowing |
| L60 | `worker_outputs/l60_v6_exposed_regression_backfill_guard_baseline_default/worker_output.json` | EDD 97.59 | exposed regression only; qv6_010 over-answer remained |
| L62 | `worker_outputs/l62_ambiguous_abstention_concision_onecase_nojudge_baseline_default/worker_output.json` | diagnostic | qv6_010 concise ambiguity refusal cleared over-answer issue |
| L64 | `worker_outputs/l64_v6_exposed_regression_ambiguous_guard_baseline_default/worker_output.json` | EDD 97.20 | exposed regression; revealed qv6_001 same-issuer project mixing |
| L65 | `worker_outputs/l65_qv6_001_project_mix_diagnosis.contract.json` | proposal | diagnosed same-issuer different-project context bleed |
| L65 | `worker_outputs/l65_same_project_guard_red_review.contract.json` | proposal | accepted; project scoping must be conservative and fixture-proven |
| L67 | `worker_outputs/l67_uicc_project_focus_onecase_withjudge_baseline_default/worker_output.json` | diagnostic | qv6_001 judge recovered to 5/5 with `project_focus_filter_count=4` |
| L68 | `worker_outputs/l68_v6_exposed_regression_project_focus_guard_baseline_default/worker_output.json` | EDD 96.42 | exposed regression; qv6_007 contradiction remained |
| L73 | `worker_outputs/l73_v6_exposed_regression_project_and_answer_guards_baseline_default/worker_output.json` | EDD 96.91 | exposed regression; qv6_007 still had a scope-denial sentence |
| L76 | `worker_outputs/l76_v6_exposed_regression_final_guard_pass_baseline_default/worker_output.json` | EDD 97.13 | exposed regression stability; qv6_007 claim gate 2/2 |

Additional no-API fixture packs:

- `analysis/l65_project_focus_fixtures/evidence_guard_fixtures.json`
- `analysis/l69_guard_fixtures_contradiction_and_project_scope/evidence_guard_fixtures.json`
- `analysis/l71_guard_fixtures_duplicate_cleanup_retry/evidence_guard_fixtures.json`
- `analysis/l74_guard_fixtures_scope_denial_cleanup/evidence_guard_fixtures.json`

Observed spend from available cost summaries in this run directory: `$0.943855`.

## L77-L78 Additions

- `worker_outputs/l77_v6_exposed_latency_prompt_concise_prompt_concise_verified_only/worker_output.json` recorded the prompt-concision latency probe.
- L77 decision after review: reject as optimization because qv6_010 abstention regressed while speed improved only marginally.
- `worker_outputs/l78_latency_red_review.contract.json` recommends a narrow top-k/context latency diagnostic only under hard quality and materiality gates.
- `worker_outputs/l78_fresh_validation_design.contract.json` proposes the next untouched validation cohort design; no question files were modified by the worker.
- `worker_outputs/l79_v6_exposed_latency_topk_after_guards_topk_sweep/worker_output.json` records the guarded top-k latency probe.
- L79 produced three diagnostic-only rows: topk5 EDD `98.13`, topk8 control EDD `98.15`, topk12 EDD `95.62`.
- Claim-preservation checks were written under `analysis/l79_claim_gate_topk5`, `analysis/l79_claim_gate_topk8`, and `analysis/l79_claim_gate_topk12`; all showed qv6_007 claim `2/2`.
- L80 did not add worker output; it corrected exposure registry metadata and aggregate safety after discovering v5 had already been spent by L30 in an earlier run.

## L81-L83 Additions

- `worker_outputs/l81_v7_source_exposed_prompt_diagnostic_baseline_default/worker_output.json` records the source-exposed prompt diagnostic. It reached EDD `97.41` but remains diagnostic-only.
- `analysis/l82_l81_sensitive_quality_recompute/recomputed_metrics.md` records the saved-answer measurement correction; qv7_006 is flagged as `sensitive_or_forbidden_refusal_with_detail_tail` while EDD remains `97.41`.
- `analysis/l82_guard_fixtures_sensitive_tail/evidence_guard_fixtures.json` records 16/16 no-API guard fixtures after adding the sensitive refusal-tail guard.
- `worker_outputs/l83_sensitive_guard_probe_nojudge_baseline_default/worker_output.json` records the one-case qv7_006 repair probe. Its EDD is not comparable because judge was omitted; the useful result is `answer_quality_issues=[]`.
- Observed spend from available cost summaries in this run directory after L83: `$1.690291`.

## L84-L86 Additions

- `worker_outputs/l84_v7_latency_red_review.contract.json` records the red acceptance gates for v7 source-exposed latency work.
- The original monolithic L84 `topk_sweep` timed out before writing `results.csv`, `details.json`, or `cost_summary.json`; keep it as a run-design failure, not a scored row.
- `worker_outputs/l85_v7_source_exposed_topk5_latency_shard_topk5_only/worker_output.json` records topk5 shard results.
- `worker_outputs/l85_v7_source_exposed_topk8_latency_shard_topk8_only/worker_output.json` records topk8 control shard results.
- `worker_outputs/l85_v7_source_exposed_topk12_latency_shard_topk12_only/worker_output.json` records topk12 shard results.
- `analysis/l86_abstention_classifier_fixtures_final2/evidence_guard_fixtures.json` records `21/21` no-API fixtures after the abstention measurement correction.
- After L86 recompute, topk8 control is the best v7 diagnostic row: EDD `98.00`, latency `16.794s`, max latency `23.46s`, clean quality gates.
- Observed spend from available cost summaries in this run directory after L85 shards: `$2.230893`, excluding any unledgered spend from the timed-out L84 attempt.

## L87 Additions

- `analysis/l87_plain_language_quality_fixtures/evidence_guard_fixtures.json` records `22/22` no-API fixtures after adding `plain_language_answer_over_structured`.
- Saved worker outputs were recomputed; qv7_009 is now flagged in L81 baseline and L85 topk5/topk8/topk12 diagnostic rows.
- `analysis/l87_plain_language_quality_report.md` records the qv7_009 before/after-measurement finding.
- No new paid model call was required for L87; it is a saved-answer measurement correction.

## L88-L90 Additions

- `eval/questions_v7_l88_plain_language_probe.json` records the one-case qv7_009 targeted format probe.
- `worker_outputs/l88_plain_language_format_probe_prompt_sweep/worker_output.json` records the four-prompt comparison.
- `worker_outputs/l89_plain_language_prompt_hint_probe_baseline_default/worker_output.json` records the query-specific prompt-hint rerun.
- `analysis/l90_plain_language_abstention_fixtures_final/evidence_guard_fixtures.json` records `23/23` no-API fixtures after the L90 abstention measurement correction.
- `analysis/l88_l90_plain_language_format_probe_report.md` summarizes the L88-L90 decision.
- Observed spend from available cost summaries in this run directory after L89: `$2.359344`.

## L91 Additions

- `worker_outputs/l91_plain_language_hint_v7_regression_baseline_default/worker_output.json` records the full v7 source-exposed regression after the plain-language hint.
- `analysis/l91_plain_language_hint_v7_regression_report.md` records the L91 decision.
- L91 has `answer_quality_issues=[]` for all 12 cases and qv7_009 remains concise.
- Observed spend from available cost summaries in this run directory after L91: `$2.530798`.

## L92 Additions

- `analysis/l92_plain_language_hint_trigger_fixtures/evidence_guard_fixtures.json` records `25/25` fixtures after adding plain-language trigger negation guards.
- L92 used no paid model calls.

## L93-L95 Additions

- `analysis/l93_sensitive_preempt_fixtures/evidence_guard_fixtures.json` records `27/27` fixtures after adding preemptive sensitive abstention.
- `eval/questions_v7_l94_sensitive_preempt_probe.json` records the two-case qv7_006/qv7_012 targeted latency probe.
- `worker_outputs/l94_sensitive_preempt_latency_probe_baseline_default/worker_output.json` records the two-case live path check.
- `worker_outputs/l95_sensitive_preempt_v7_regression_baseline_default/worker_output.json` records the full v7 source-exposed regression after preemptive abstention.
- `analysis/l93_l95_sensitive_preempt_report.md` records the L93-L95 decision.
- Observed spend from available cost summaries in this run directory after L95: `$2.687161`.

## L96 Additions

- `analysis/l96_preempt_estimate_price_false_positive_fixtures/evidence_guard_fixtures.json` records `28/28` fixtures after narrowing the preempt marker for `추정금액` false positives.
- L96 used no paid model calls.
