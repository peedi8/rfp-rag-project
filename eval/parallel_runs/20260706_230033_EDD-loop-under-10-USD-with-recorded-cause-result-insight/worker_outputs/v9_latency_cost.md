# v9 Latency/Cost Evidence Note

Proposal-only worker. No paid APIs were called and no protected paths were modified.

## Observed Baseline

- Current `evaluate.py` records per-case `latency_sec` from `RAGPipeline.ask`.
- Current `run_experiment_worker.py` writes aggregate `latency_avg_sec` in result rows.
- No reviewed script persists token usage, observed cost, preflight cost reservation, or stage-level timing.
- L25 v4 first baseline: EDD `97.41`, latency average `19.377s`.
- L30-L36 adversarial report shows latency changed promotion decisions: L35 at `22.035s` and L36 at `23.683s` were not suitable speed wins even though correctness was saturated.

## Proposed Captures

Add per-case timers for pipeline init, rewrite, filter inference, retrieval, MMR/rerank, context formatting, answer generation, judge generation, metric aggregation, artifact writes, and unattributed time.

Add cost ledger fields for estimated/observed tokens, estimated/observed USD, model, provider, operation, paid-call flag, cache state, spend before/after, remaining budget, and stop reason.

## Budget Rule

Use a hard cap of `$10.00`, but stop launching scored paid work at `$9.00` projected/observed spend. Keep `$1.00` as error/retry reserve. Default all loops to no-api-first diagnostics, saved recomputation, retrieval checks, and no-judge slices before judged scored runs.

## Promotion Blockers

Block promotion if candidate latency average is more than 10 percent slower than baseline without at least 1.0 EDD improvement, p90 is more than 15 percent slower, max is more than 25 percent slower, or two shared cases regress by at least 5 seconds. Also block any latency-saving candidate that degrades retrieval coverage, abstention accuracy, groundedness, relevance, false abstention, empty answers, or red-gate safety/source-scope checks.
