# L41-L44 Quality And Cost Gate Report

## Summary

- L41 claim audit: L40 is a partial recovery for qv6_007, not a full metamorphic pass.
- L41 ambiguity review: qv6_010 needs a post-refusal over-answer quality gate.
- L42 dry-run: cost-trace artifacts write without API calls and are excluded from scoreboard.
- L43 live no-judge probe: usage/cost trace works for query embedding plus answer generation.
- L44 live judge-included probe: usage/cost trace works for query embedding, answer generation, and judge.

## L41 Claim Pair Audit

The qv6_006/qv6_007 pair tests whether the same Goyang project keeps the same facts when wording is shuffled.

- L37: retrieved the Goyang project at rank 2 but mixed other organizations, then said unmanned operation and access control could not be confirmed.
- L40: fixed retrieval binding and recovered unmanned operation plus H/W linkage.
- Remaining issue: L40 still says physical access control is not confirmed, even though the source data includes access-control-system purchase/installation.

Decision: keep the alias fix, but label L40 as `partial_recovery_only`.

## L41 Ambiguity Review

qv6_010 improved from unsafe project selection to an ambiguity refusal. However, after saying the title fragment is insufficient, the answer gives a long candidate requirements summary.

New issue label:

`ambiguous_identifier_refusal_with_excessive_candidate_summary`

Recommended rule: if a title fragment is insufficient, answer briefly with the missing identifiers and optional candidate identity anchors only. Do not summarize requirements, budgets, schedules, or security details until the user selects a candidate.

## L42-L44 Cost Trace

Code changes added:

- `src/costing.py`
- generation usage/cost trace in `src/generator.py`
- query embedding trace in `src/vectorstore.py` and `src/retriever.py`
- retrieval/generation cost fields in `src/rag.py` and `scripts/evaluate.py`
- judge usage/cost trace in `scripts/evaluate.py`
- `cost_summary.json` and `budget_ledger.jsonl` in `scripts/run_experiment_worker.py`
- dry-run and diagnostic question-set exclusion in `scripts/aggregate_parallel_eval.py`

L43 live no-judge probe:

- observed calls: 2
- observed local-table cost: `$0.008312`
- query embedding: `$0.000002`
- answer generation: `$0.008310`
- latency: `21.46s`
- answer quality: still underanswers physical access control.

L44 live judge-included probe:

- observed calls: 3
- observed local-table cost: `$0.013187`
- query embedding: `$0.000002`
- answer generation: `$0.007432`
- judge: `$0.005753`
- latency: `19.27s`
- judge score: groundedness `5`, relevance `5`
- answer quality: still underanswers physical access control.

## Gate Decision

- Scoreboard currently contains only L37 EDD `86.25`.
- L38-L44 are diagnostic, dry-run, no-judge, or exposed-case evidence.
- L44 is an important report example: high judge score but human-visible metamorphic incompleteness.
- Follow-up L45 implemented hard-stop budget enforcement and the over-answer gate.
- Next broad paid loop should still wait for the qv6_007 claim-preservation gate.
