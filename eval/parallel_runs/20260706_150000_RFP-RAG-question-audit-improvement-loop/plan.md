# RFP RAG Parallel Improvement Loop Plan

- created_at: 2026-07-06 15:00 KST
- baseline_run: `eval/parallel_runs/20260706_134254_RFP-RAG-parallel-EDD-full-run-after-abstention-fix`
- baseline_best: `mmr_lambda_sweep/lambda05_top8_filter_rewrite_control`
- baseline_best_edd: 96.57
- default_candidate: `top_k=8`, `mmr_lambda=0.5`, `fetch_k=20`, `auto_filter=True`, `rewrite_query=True`, `rerank=False`

## Objective

Run the next improvement loop as a measured RAG research loop, not a blind retry loop.

The loop must answer four questions every round:

1. Did EDD improve or regress against the frozen baseline?
2. Did human/5.5-level qualitative audit agree with the score?
3. Which question types failed or looked suspicious despite high metrics?
4. What exact code/config/prompt change should be kept, reverted, or tested next?

## Parallel Work Streams

| stream | owner role | output only | purpose |
|---|---|---|---|
| question_generator | high-reasoning question designer | `worker_outputs/question_generator/questions_v2_proposals.json` | Create diverse realistic and adversarial RFP-RAG questions. Must not answer them. |
| rag_answer_runner | RAG experiment worker | `worker_outputs/rag_answer_runner/results.*` | Run frozen and candidate configs on the same selected question cohort. |
| quality_audit_55 | high-reasoning quality judge/red team | `worker_outputs/quality_audit_55/audit_results.json` | Judge contextual fit, evidence fit, usefulness, and high-score-but-unconvincing cases. |
| report_evidence_pack | evidence/report worker | `worker_outputs/report_evidence_pack/report_evidence.*` | Keep question, answer, retrieval, scores, flags, cause analysis, and insight together. |

Workers do not edit final config, source files, `업무일지.md`, or `eval/experiment_log.md`. Main Codex merges decisions only after verification.

## Metrics

Primary metric:

- EDD score: retrieval coverage, hit-all, MRR, groundedness, relevance, abstention accuracy, latency score, false-abstention penalty, empty-answer penalty.

Required secondary metrics:

- `retrieval_coverage_avg`
- `hit_all_targets_rate`
- `mrr`
- `groundedness_avg`
- `relevance_avg`
- `abstention_accuracy`
- `false_abstention_rate`
- `empty_answer_rate`
- `latency_avg_sec`
- qualitative `contextual_quality`
- qualitative `evidence_fit`
- qualitative `usefulness`
- qualitative `decision`: `pass`, `pass_with_caveat`, `fail`
- `risk_flags`: hallucination, over-refusal, under-refusal, wrong-document, verbosity, missing-citation, unclear-source

## Loop Procedure

1. Freeze baseline: use the existing `20260706_134254...` run and its generated evidence/audit packs.
2. Generate candidate questions: high-reasoning model proposes new questions by type, including multi-turn, ambiguous org, comparison, absence/abstention, and "score trap" cases.
3. Curate cohort: main Codex accepts a bounded question set into a new versioned JSON file; old questions remain unchanged.
4. Run parallel answer experiments: sweep only one variable group per worker so cause analysis stays readable.
5. Aggregate EDD and graphs: produce CSV/JSON/Markdown/SVG for every run.
6. Build evidence pack: record every selected question, answer, retrieved organizations, metrics, automatic flags, and interpretation.
7. Run 5.5-quality audit: judge whether the answer is actually convincing in context.
8. Decide: keep a change only if EDD improves or holds while qualitative audit does not reveal a worse answer pattern.
9. Record diary: append exact process, cause, result, insight, and next action to `업무일지.md`.

## Adoption Gate

A candidate can become default only when all are true:

- EDD is higher than baseline, or EDD is within 1.0 point while qualitative audit clearly improves.
- `false_abstention_rate == 0` on the frozen cohort.
- `empty_answer_rate == 0`.
- No new high-severity quality audit failure appears on comparison, follow-up, or abstention questions.
- Cause analysis explains why the change helped.

If a candidate regresses, it is still recorded as useful negative evidence. The diary must include what dropped, why we think it dropped, and what the next controlled test should be.

## Current Round Artifacts

- baseline summary: `eval/parallel_runs/20260706_134254_RFP-RAG-parallel-EDD-full-run-after-abstention-fix/summary/summary.md`
- baseline graphs: `summary/edd_score.svg`, `summary/metric_heatmap.svg`, `summary/quality_vs_retrieval.svg`, `summary/latency_vs_edd.svg`
- report evidence pack: `report_evidence/report_evidence.md` and `.json`
- quality audit input: `audits/audit_input.md` and `.json`

## Immediate Next Experiments

1. Run high-reasoning question generation for `questions_v2_proposals.json`.
2. Curate 15-25 accepted questions into a frozen `questions_v2.json`.
3. Run candidate suites:
   - baseline default on v2 cohort
   - low-verbosity prompt variant
   - stricter citation/no-evidence prompt variant
   - focused retrieval filter fallback for ambiguous organization questions
4. Run quality audit on all failures and on a sample of high EDD answers.
5. Merge only after EDD and quality audit both support the change.
