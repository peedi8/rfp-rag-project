# L48-L76 Backfill, Guard, and Regression Report

Created: 2026-07-07 01:12 KST

## Executive Summary

- Honest v6 first-run evidence remains L37: EDD `86.25`.
- L76 is not fresh validation. It is an exposed-regression result after inspecting and fixing failures.
- L76 exposed-regression metrics: EDD `97.13`, coverage `1.0`, MRR `1.0`, groundedness `5.0`, relevance `5.0`, abstention accuracy `1.0`, latency `20.642s`.
- qv6_007 claim preservation at L76: `2/2` pass.
- Scoreboard isolation held: aggregate after L76 shows `scoreboard_rows=1`, `diagnostic_only_rows=31`.
- Observed spend from available cost summaries in this run directory: `$0.943855`.
- Smoke after contract repair: pass, worker output contracts `45`, issues `[]`.

## What Changed

| area | files | purpose |
|---|---|---|
| CSV summary backfill | `src/rag.py` | Add target-bound `사업 요약` evidence only when query/source terms require it and retrieved chunks are single-org/title matched. |
| Project focus filter | `src/rag.py` | Drop same-issuer but different-project chunks when the query clearly points to one project. |
| Answer guards | `src/generator.py` | Repair source-supported physical access-control underanswers, shorten ambiguous-title refusals, and remove contradictory/duplicate access-control lines. |
| Eval details | `scripts/evaluate.py` | Record `context_backfill_count` and `project_focus_filter_count`. |
| Fixtures | `scripts/check_evidence_guard_fixtures.py` | Cover source backfill, access-control repair, ambiguity concision, project focus, contradiction cleanup, and duplicate-line cleanup. |
| Aggregation safety | `scripts/aggregate_parallel_eval.py` | Keep unregistered temporary probe files diagnostic-only. |

## Loop Results

| loop | purpose | result | decision |
|---|---|---|---|
| L48 | First answer-only evidence guard | claim gate still failed | reject generation-only fix; evidence was missing from context |
| L49-L59 | CSV backfill + access-control guard | qv6_007 claim gate `2/2`, judge `5/5` | keep as targeted diagnostic |
| L60 | Full v6 exposed regression | EDD `97.59`; qv6_010 over-answer remained | do not promote; fix answer-quality issue |
| L62-L64 | Ambiguous-title concision | qv6_010 issue cleared; qv6_001 groundedness fell | keep concision guard; investigate project mixing |
| L65-L68 | Same-issuer project focus | qv6_001 fixed; qv6_007 contradiction remained | keep project focus; clean answer consistency |
| L69-L75 | qv6_007 contradiction/duplicate cleanup | one-case qv6_007 judge `5/5`, claim `2/2` | keep cleanup fixtures |
| L76 | Full v6 exposed regression | EDD `97.13`, no automated issues, qv6_007 claim `2/2` | keep as exposed-regression stability evidence only |

## Key Findings

1. Org coverage is not source purity.
   qv6_001 retrieved only `한국연구재단`, but mixed UICC with another same-issuer project. Project-title focus was required.

2. Judge 5/5 is not enough.
   qv6_007 could pass judge and claim preservation while still containing contradictory or duplicate lines. Human-readable consistency needed its own cleanup.

3. Correct abstention can still be too verbose.
   qv6_010 did the right refusal but then gave a long candidate requirements summary. The concise ambiguity guard fixed this.

4. L76 should be reported honestly.
   It is useful regression evidence after fixes, but not a held-out or fresh validation score.

## Remaining Work

- Build a fresh untouched validation split before making generalization claims.
- Run a latency/cost loop. L76 latency is still `20.642s`, with qv6_006 and qv6_010 slow.
- Validate CSV summary backfill against fresh false-positive cases.
- Consider adding project-scope diagnostics directly to reports, not only as filter counts.

## L77 Addendum: Rejected Latency Prompt

L77 tested `prompt_concise_verified_only` on the exposed v6 set. It lowered average latency only from `20.642s` to `20.112s`, while EDD dropped to `92.25` because abstention accuracy fell to `0.5`.

The concrete failure was qv6_010: the answer no longer treated the generic title fragment as ambiguous, selected `국가과학기술지식정보서비스`, and summarized requirements. This confirms that prompt-level concision is an unsafe speed path unless ambiguity refusal is preserved.

Decision: reject L77 as an optimization. The next speed test should vary context/top-k under the current guards and require qv6_007 claim preservation, qv6_010 refusal, `5/5` groundedness/relevance, and a material latency improvement before adoption.

## L79 Addendum: Guarded Top-K Latency Probe

L79 ran `topk_sweep` on the exposed v6 set after the L76 guards.

| candidate | EDD | latency | groundedness | relevance | abstention | qv6_007 claim | decision |
|---|---:|---:|---:|---:|---:|---|---|
| topk5 | `98.13` | `16.209s` | `5.0` | `5.0` | `1.0` | `2/2` | cost-saving candidate only; tail latency risk |
| topk8 control | `98.15` | `16.130s` | `5.0` | `5.0` | `1.0` | `2/2` | best exposed diagnostic row; not fresh validation |
| topk12 | `95.62` | `16.263s` | `4.5` | `4.875` | `1.0` | `2/2` | reject |

The topk8 row is the current control setting, so the apparent speed gain versus L76 should not be treated as a parameter improvement. topk5 reduced observed cost but had worse tail latency on qv6_006/qv6_010. topk12 shows a useful failure pattern: coarse claim preservation can pass while groundedness drops.

Decision: keep current topk8 as the safest exposed-regression setting, reject topk12, and require a repeatability or fresh-validation check before claiming speed/generalization improvement.

## L80 Addendum: Exposure Registry Correction

The registry still marked v5 as unscored, but prior artifacts showed L30 had already run v5 as first validation. This was corrected in `scripts/build_exposure_registry.py`, and the registry was regenerated.

Two v6 targeted probe files were also explicitly labeled diagnostic-only. `scripts/aggregate_parallel_eval.py` now treats `unknown_needs_review` and `do_not_promote_until_reviewed` as diagnostic-only, so unknown files cannot silently enter the scoreboard.

Verification: aggregate returned to `scoreboard_rows=1`, `diagnostic_only_rows=35`.

## L81-L83 Addendum: High Score, Human-Quality Failure, Small Repair

L81 ran a 12-case v7 source-exposed prompt diagnostic because no completely unused source projects remained. It reached EDD `97.41`, with coverage/MRR `1.0`, groundedness/relevance `5.0/5.0`, abstention accuracy `1.0`, and latency `19.407s`. This is useful diagnostic evidence but not held-out validation.

Manual review found qv7_006 as a high-score but questionable answer. The system correctly refused final vendor and actual contract amount, but then gave a claim-flow example and official contact details. That is too much tail detail for a prompt asking for unsupported final results, real patient/claim examples, and private contact information.

L82 added the deterministic issue key `sensitive_or_forbidden_refusal_with_detail_tail`. Recomputing the saved L81 answer kept EDD at `97.41` but flagged qv7_006. L82 also expanded the no-API fixture pack to `16/16` passing cases.

L83 reran only qv7_006 without judge after adding `_apply_sensitive_abstention_guard`. The answer became a concise refusal, abstention stayed correct, and `answer_quality_issues=[]`. L83 EDD `57.16` is not comparable because judge scores were omitted.

Decision: keep L81-L83 as diagnostic and repair evidence. The report should show the qv7_006 before/after pair to explain why high automatic metrics do not prove answer quality.

## L84-L86 Addendum: Sharded Latency Probe and Measurement Repair

L84 attempted a single `topk_sweep` over the 12-case v7 source-exposed diagnostic set. It timed out before writing result and cost artifacts. Treat this as a run-design failure. It also means the local observed cost total may undercount calls made during the timed-out attempt.

The runner now has single-setting suites: `topk5_only`, `topk8_only`, and `topk12_only`. L85 used those shards so each setting wrote its own artifacts.

L85 initially exposed an abstention-measurement issue: partial answers such as “confirmed DR scope, unknown EMR full replacement” were counted as full refusals, while patient-example refusals with a project-name prefix could be missed. L86 corrected `is_abstention` and expanded no-API fixtures to `21/21` passing cases.

After L86 recompute:

| candidate | EDD | avg latency | max latency | quality | decision |
|---|---:|---:|---:|---|---|
| topk5 | `97.99` | `16.865s` | `25.85s` | clean | not adopted |
| topk8 control | `98.00` | `16.794s` | `23.46s` | clean | keep as current diagnostic control |
| topk12 | `95.51` | `19.922s` | `36.95s` | groundedness/relevance `4.667/4.889` | reject |

Decision: do not claim a new top-k optimization. topk8 is already the current control setting, and the v7 set is source-exposed. The useful improvement is the sharded execution pattern and the abstention-measurement repair.

## L87 Addendum: Plain-Language Fit Is Separate From Groundedness

L87 added `plain_language_answer_over_structured` after qv7_009 showed a second high-score answer-quality problem. The user asked for a plain-language explanation, but the answer returned long RFP-style lists. The answer was grounded, so the judge still gave groundedness/relevance `5/5`; the problem was usefulness and format fit.

Saved-output recompute flagged qv7_009 in L81 baseline and all L85 v7 diagnostic shards:

| row | chars | lines | bullet/list lines | judge |
|---|---:|---:|---:|---|
| L81 baseline | `1142` | `25` | `20` | `5/5` |
| L85 topk5 | `1160` | `29` | `15` | `5/5` |
| L85 topk8 control | `1294` | `42` | `16` | `5/5` |
| L85 topk12 | `1448` | `29` | `11` | `5/5` |

Fixtures pass `22/22`, and aggregate remains `scoreboard_rows=1`. L87 does not improve EDD; it improves the ability to notice when a technically correct answer is too exhaustive for the user's intent.

## L88-L90 Addendum: Narrow Plain-Language Hint Beats Broad Prompt Swap

L88 tested qv7_009 as a one-case source-exposed format probe. Default stayed over-structured: `1228` chars, `47` lines, `29` list items, judge `5/5`, latency `18.8s`. `prompt_report_ready` cleared the issue with `644` chars and `5` bullets, but latency rose to `50.94s`, so it is not a good broad setting.

L89 added a query-specific hint only when the user asks for easy/plain-language explanation. On the same qv7_009 probe, the answer became `605` chars, `9` lines, `5` bullets, judge `5/5`, latency `16.7s`, and no quality issue. This is a candidate repair, not a validated champion, because it is one source-exposed case.

L90 corrected a measurement bug exposed by L89. The answer included a final caveat that final vendor/contract result was not available, and `is_abstention` initially counted the whole answer as a refusal. After the correction, substantive plain-language bullet answers with a final unsupported-result caveat are not full abstentions. Fixtures pass `23/23`.

Decision: keep the hint as a candidate and run a small v7 source-exposed regression before adoption. Do not report L89 as fresh validation.

## L91 Addendum: Full V7 Diagnostic After Plain-Language Hint

L91 reran the full v7 source-exposed diagnostic set after the query-specific plain-language hint. It reached EDD `97.82`, coverage/MRR `1.0/1.0`, groundedness/relevance `5.0/5.0`, abstention accuracy `1.0`, and average latency `17.613s`.

All 12 answers had `answer_quality_issues=[]`. qv7_009 stayed concise: `718` chars, `9` lines, `5` bullets, judge `5/5`. The hint therefore remains a useful candidate for the plain-language problem.

This is still not fresh validation, and it is not a speed win: L85 topk8 control was slightly faster on average, and L91 had a qv7_006 tail latency of `28.81s`. The honest claim is answer-format stability on a source-exposed diagnostic set.

## L92 Addendum: Hint Trigger False-Positive Guard

L92 added negation markers so the plain-language hint does not trigger when the user explicitly says not to simplify or not to summarize. The no-API fixture pack now passes `25/25`.

This does not change EDD. It protects the L89-L91 candidate repair from overriding explicit user intent.

## L93-L95 Addendum: Preemptive Refusal Removes Wasted Generation

L91 showed qv7_006 still had high tail latency even though the final answer was short. Trace analysis showed the model spent `28.49s` generating before the post-answer guard trimmed the result. L93 added a preemptive sensitive abstention guard for adversarial requests that combine forbidden/sensitive fields with fabrication or guessing markers.

Fixtures pass `27/27`. L94 confirmed the live path: qv7_006 and qv7_012 had generation trace length `0`, generation cost `$0.0`, and average latency `2.065s`. L94 EDD is not comparable because abstention-only rows do not receive judge scores.

L95 reran full v7 source-exposed diagnostics and reached EDD `98.54`, latency `14.44s`, abstention `1.0`, and `0/12` quality issue rows. qv7_006 and qv7_012 dropped to sub-second latency; qv7_009 stayed clean.

Decision: this is the strongest source-exposed diagnostic row, but it is still not fresh validation. The next gate should be false-positive testing for the preempt trigger or a new validation cohort.

## L96 Addendum: `추정금액` Is Not a Fabrication Request

L96 tightened the preempt trigger after noticing that the broad marker `추정` could match normal procurement terms such as `추정금액`. The marker now targets intent phrases such as `추정해`, `추정해서`, and `추정 가능`.

A no-API fixture now confirms that a question asking to distinguish final contract amount from estimated amount is not preempted. Fixture pack: `28/28`.
