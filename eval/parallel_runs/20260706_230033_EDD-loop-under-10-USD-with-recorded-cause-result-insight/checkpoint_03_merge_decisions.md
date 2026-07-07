# Checkpoint 03 - Merge Decisions

Created: 2026-07-06 23:25 KST
Updated: 2026-07-07 00:20 KST

## Accepted

- Freeze and run v6 metamorphic/property cohort. L37 is the first-run evidence and must be preserved separately from later retries.
- Keep the safety prompt guard in `src/generator.py`:
  - do not turn budget/estimated/business amount into final contract result;
  - separate official contact from personal contact;
  - do not pick a single project from an ambiguous title fragment.
- Keep the Goyang urban-management alias expansion in `src/retriever.py`; it recovers the qv6_007 project binding and removes cross-organization contamination.
- Accept L41 claim-pair audit conclusion: L40 is partial recovery, not full metamorphic pass.
- Accept L41 qv6_010 ambiguity rule: a correct ambiguity refusal can still be penalized if it adds a long candidate requirements summary.
- Accept L41-L44 cost-trace implementation:
  - `src/costing.py` local usage/cost helper;
  - answer, judge, and query-embedding usage trace fields;
  - `cost_summary.json` and `budget_ledger.jsonl` under worker output folders;
  - aggregate exclusion of dry-run and diagnostic question-set rows from the scoreboard.
- Accept L44 judge-included cost-trace smoke as verification of the judge usage/cost path.
- Accept L47 claim-preservation gate as a diagnostic-only guard for the exposed qv6_007 metamorphic failure.
- Accept Worker B's source-scope warning: source markers must be tied to the target Goyang row, not the whole `data_list.csv`.

## Rejected Or Not Promoted

- Do not promote L38 EDD 56.04 as a performance score. It lacks judged groundedness/relevance and is diagnostic-only.
- Do not promote L39 top_k results. top_k changes did not recover stable answer quality and top12 lowered groundedness.
- Do not promote L40 as a champion. It is a one-case targeted retry, has high latency, and still underanswers source-supported physical access-control evidence.
- Do not treat L43 EDD 46.94 as a quality score; it was intentionally run `--no-judge` on a diagnostic question set to verify cost tracing.
- Do not treat L44 EDD 87.44 as a general performance score; it is a judged diagnostic question-set row and remains excluded from the scoreboard.
- Do not promote L47 as an EDD improvement. It is a measurement gate that currently fails qv6_007.

## Red-Team Notes

- L37 is the honest v6 first-run number: EDD 86.25.
- L38-L44 are useful engineering evidence but are not held-out/generalization evidence.
- L44 confirms the judge can give 5/5 to an answer that fails a paired metamorphic comparison. Future gates must compare paired answers and claim preservation, not only each answer against retrieved chunks.
- Source check found access-control, unmanned ticketing, relay-server, and `2SET` evidence in the data source. The remaining qv6_007 failure is evidence-use/completeness, not source absence.
- L47 confirms the sharper gate result: L37 is 0/2, L40 is 1/2, and L44 is 1/2. L40 recovers unmanned-operation/HW linkage but still misses physical access-control.

## Next Gate

Before any broad paid loop under the 10 USD cap, fix or explicitly carry the qv6_007 physical access-control underanswer. The hard-stop budget runner, over-answer gate, and claim-preservation gate are now smoke-tested.

## L48-L76 Decisions

## Accepted

- Accept target-bound CSV summary backfill in `src/rag.py` for qv6_007-style evidence gaps.
  - It only fires on specific query/source terms, single retrieved org, and matching project title.
  - `context_backfill_count` is recorded for audit.
- Accept narrow physical access-control evidence-use guard in `src/generator.py`.
  - It repairs source-supported underanswers but preserves unknown boundaries for method, specification, vendor, and integration details.
- Accept concise ambiguous-title refusal guard.
  - qv6_010 should ask for an identifier instead of summarizing candidate requirements after refusal.
- Accept conservative same-issuer project focus filter.
  - qv6_001 showed org coverage is not enough; same issuer can still mix different projects.
  - `project_focus_filter_count` is recorded for audit.
- Accept aggregate protection for unregistered temporary probe files.
  - L67 was correctly removed from scoreboard after this patch.

## Not Promoted

- Do not promote L60/L64/L68/L73/L76 as fresh validation. They are exposed-regression rows on the already inspected v6 set.
- Do not promote one-case probes L49/L59/L62/L67/L70/L72/L75. They explain causes and verify repairs only.
- Do not treat CSV summary backfill as generally safe until fresh false-positive tests are run.

## Final L76 Position

- L76 full v6 exposed regression: EDD `97.13`, groundedness `5.0`, relevance `5.0`, abstention accuracy `1.0`, latency `20.642s`.
- qv6_007 claim-preservation gate: `2/2` pass.
- Aggregate after L76: `scoreboard_rows=1`, `diagnostic_only_rows=31`.
- Smoke after contract repair: pass, worker output contracts `45`, issues `[]`.

## Next Gate

The next meaningful improvement should be either:

- a fresh untouched validation split, or
- a latency/cost loop that does not claim quality improvement from the exposed v6 set.

## L77 Decision

- `prompt_concise_verified_only` on exposed v6 is rejected.
- It reduced latency only from `20.642s` to `20.112s`, while abstention accuracy fell from `1.0` to `0.5`.
- The failure was qv6_010: a generic title fragment received a concrete candidate answer instead of a refusal/request for identifiers.
- This row remains diagnostic-only and must not be used as a champion.
- Red review accepts only a tightly gated top-k/context latency diagnostic next: quality must hold at L76 levels and latency must improve materially, not by noise.

## L79 Decision

- Keep topk8 control as the safest exposed-regression diagnostic row, but do not call it a fresh validation result or a new optimization.
- Keep topk5 as a cost-saving candidate only. It preserved quality and qv6_007 claim `2/2`, but tail latency worsened on qv6_006/qv6_010.
- Reject topk12. It preserved qv6_007 claim `2/2` but lowered groundedness/relevance, showing that claim preservation alone is insufficient.
- All L79 rows remain diagnostic-only; scoreboard isolation still preserves L37 as the only first-run row.

## L80 Decision

- Do not use v5 as a new first-run candidate in this run. Prior L30 already spent that first validation status.
- Keep the registry correction: v5 draft/frozen are exposed, qv6_l61/qv6_l65 probes are diagnostic-only.
- Keep the aggregator guard that prevents `unknown_needs_review` and `do_not_promote_until_reviewed` rows from entering the scoreboard.
- Next strict validation must come from a genuinely new v7/v8 cohort.

## L81-L83 Decision

- Keep L81 as `diagnostic_only`; it is prompt-fresh but source-exposed, so EDD `97.41` is not held-out validation.
- Accept the L82 measurement correction: sensitive/forbidden-info abstentions need a separate refusal-tail quality flag because binary abstention can be correct while the answer remains too detailed.
- Accept `_apply_sensitive_abstention_guard` because no-API fixtures pass 16/16 and the targeted L83 probe clears qv7_006 over-detail.
- Do not rank or promote L83 EDD `57.16`; the run intentionally omitted judge scores.
- Carry the L81-before/L83-after qv7_006 pair into the report as qualitative evidence that high automatic metrics can hide answer-quality issues.

## L84-L86 Decision

- Reject the monolithic L84 sweep design. It timed out before writing result/cost artifacts.
- Accept sharded top-k suites in `scripts/run_experiment_worker.py` so future long runs checkpoint each setting independently.
- Accept the L86 abstention measurement correction because fixtures pass `21/21`.
- Reject topk12 for v7 source-exposed diagnostics: EDD `95.51`, latency `19.922s`, max `36.95s`, groundedness/relevance `4.667/4.889`.
- Do not adopt topk5 because topk8 control is slightly better on average latency, tail latency, and EDD.
- Keep topk8 as the current best diagnostic/control row: EDD `98.00`, latency `16.794s`, max `23.46s`, no quality issues. Do not describe it as fresh validation or a new optimization.
- Record possible unledgered cost risk from L84 timeout; local observed total `$2.230893` excludes any calls made before that failed run wrote summaries.

## L87 Decision

- Accept the `plain_language_answer_over_structured` measurement gate.
- Treat L87 as a diagnostic lens, not an EDD-improving model change.
- Do not change the current control setting based on L87 alone.
- Carry qv7_009 into the report as a high-score answer that is grounded but too structured for the user's plain-language intent.
- If a repair is attempted next, restrict it to a one-case qv7_009 format probe and reject it if groundedness, relevance, abstention, or ambiguity handling regresses.

## L88-L90 Decision

- Accept `questions_v7_l88_plain_language_probe.json` and registry labeling as diagnostic-only.
- Reject L88 default because it remains over-structured despite judge `5/5`.
- Reject L88 `prompt_report_ready` as a broad setting because it clears the quality issue but latency is `50.94s`.
- Accept the query-specific plain-language hint as a candidate repair: L89 clears the quality issue, keeps judge `5/5`, and improves latency to `16.7s`.
- Do not promote L89 as generally validated. It is a single source-exposed qv7_009 probe.
- Accept the L90 abstention measurement correction because fixtures pass `23/23`.
- Next gate: full v7 source-exposed regression under the hint before considering adoption.

## L91 Decision

- Accept L91 as source-exposed regression evidence that the plain-language hint did not create automated quality regressions on v7.
- Keep the hint as a guarded candidate repair.
- Do not call L91 fresh validation or a speed win.
- Next gate is either a false-positive trigger test for plain-language markers or a qv7_006 tail-latency analysis.

## L92 Decision

- Accept plain-language hint negation markers.
- Keep the no-API trigger fixtures as a guard against user-intent reversal.
- Do not attach a performance score to L92.

## L93-L95 Decision

- Accept the preemptive sensitive abstention guard as a source-exposed candidate improvement.
- Use L94 for latency/cost evidence only; its EDD is not comparable because abstention rows do not receive judge scores.
- Treat L95 as the strongest source-exposed diagnostic row so far: EDD `98.54`, latency `14.44s`, quality issue rows `0/12`.
- Do not call L95 fresh validation.
- Next gate is a false-positive set for preempt triggers or a genuinely fresh validation cohort.

## L96 Decision

- Accept the narrower preempt marker set.
- Keep `추정금액` false-positive fixture.
- No paid rerun required because this is a no-API trigger safety correction.
