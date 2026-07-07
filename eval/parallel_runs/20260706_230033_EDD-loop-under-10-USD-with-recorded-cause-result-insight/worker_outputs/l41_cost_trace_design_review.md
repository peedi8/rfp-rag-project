# l41 Cost Trace Design Review

No paid APIs were called. No protected project files were modified. This is a proposal-only review for adding token, cost, and stage timing tracing to the general experiment runner.

## Key Finding

The requested input `src\rag_pipeline.py` is stale for this checkout. That file does not exist. The actual pipeline used by `scripts\evaluate.py` is `src\rag.py`, which defines `RAGPipeline.ask`.

## Exact Patch Points

- `scripts\run_experiment_worker.py`
  - `METRIC_COLS`: append trace summary columns such as `cost_usd_total`, `tokens_total`, `stage_retrieval_avg_sec`, `stage_answer_generation_avg_sec`, and `stage_judge_generation_avg_sec`.
  - `run_suite`: create `budget_ledger.jsonl`, `timing_ledger.jsonl`, and `cost_summary.json` under each `worker_dir`; pass trace output paths into `run_eval` after tracing is implemented.
  - `details_all[name]`: add `trace_summary` while preserving existing `params`, `metrics`, `edd_score`, `issues`, and `details`.

- `scripts\evaluate.py`
  - `_chat_json`: preserve current JSON behavior but add a companion path that returns parsed JSON plus `resp.usage`.
  - `_judge`: record judge model, usage, cost, and latency under `rec["trace"]["judge"]` or `rec["judge"]["usage"]`.
  - `run_eval`: initialize per-case trace state, pass it into `RAGPipeline.ask`, and append budget/timing rows after each case.
  - `aggregate`: keep all current formulas unchanged; append optional cost/token/stage timing aggregates.

- `src\rag.py`
  - `RAGPipeline.ask`: add optional `trace: dict | None = None`. Time query rewrite, effective top-k calculation, retrieval, answer generation, and history update. Preserve `latency_sec` and `retrieval_sec`.

- `src\generator.py`
  - `generate_answer`: do not change the default return type. Add either `return_metadata=False` or a new `generate_answer_with_trace(...) -> dict`.
  - nested `_complete`: record latency, max completion tokens, finish reason, retry count, and `resp.usage` for both first attempt and length retry.

- `src\retriever.py`
  - `retrieve`: add optional `trace` parameter and record load index, embedding, auto-filter, vector query, missing-org query, MMR/rerank, coverage repair, and final assembly timing.
  - `_llm_rerank`: if enabled, capture usage/cost/latency as operation `retrieval_rerank`.

- `scripts\run_blind_judge_calibration.py`
  - Use as the implementation reference for `_cost_usd`, observed usage extraction, `append_jsonl`, `--no-api`, `--budget-cap-usd`, and `--hard-stop-usd`.

## Minimal `budget_ledger.jsonl`

One append-only row per model-call attempt:

```json
{
  "schema": "rfp_rag_budget_ledger.v1",
  "run_id": "string",
  "worker_id": "string",
  "suite": "string",
  "experiment": "string",
  "case_id": "string",
  "turn_index": 0,
  "operation": "answer_generation | judge_generation | retrieval_rerank | query_rewrite",
  "provider": "openai | local_cli | none",
  "model": "string",
  "is_paid_api": true,
  "status": "ok | failed | skipped_budget | no_api | usage_missing",
  "latency_sec": 0.0,
  "prompt_tokens_estimated": 0,
  "completion_tokens_estimated": 0,
  "total_tokens_estimated": 0,
  "prompt_tokens_observed": 0,
  "completion_tokens_observed": 0,
  "total_tokens_observed": 0,
  "cost_usd_estimated": 0.0,
  "cost_usd_observed": 0.0,
  "cost_basis": "observed_usage | estimated_chars | no_api | missing_usage",
  "spent_before_usd": 0.0,
  "spent_after_usd": 0.0,
  "hard_cap_usd": 10.0,
  "stop_reason": ""
}
```

## Minimal `cost_summary.json`

```json
{
  "schema": "rfp_rag_cost_summary.v1",
  "created_at": "ISO-8601 string",
  "run_id": "string",
  "worker_id": "string",
  "suite": "string",
  "experiment": "string",
  "no_api": false,
  "budget": {
    "hard_cap_usd": 10.0,
    "launch_ceiling_usd": 9.0,
    "spent_observed_usd": 0.0,
    "spent_estimated_usd": 0.0,
    "remaining_observed_usd": 10.0,
    "paid_api_calls": 0,
    "skipped_budget_calls": 0
  },
  "tokens": {
    "prompt_tokens_observed": 0,
    "completion_tokens_observed": 0,
    "total_tokens_observed": 0,
    "usage_missing_calls": 0
  },
  "cost_by_operation": {
    "answer_generation": 0.0,
    "judge_generation": 0.0,
    "retrieval_rerank": 0.0,
    "query_rewrite": 0.0
  },
  "latency_by_stage_avg_sec": {
    "query_rewrite": 0.0,
    "retrieval_total": 0.0,
    "answer_generation": 0.0,
    "judge_generation": 0.0,
    "metric_aggregation": 0.0
  },
  "case_count": 0,
  "artifact_paths": {
    "budget_ledger": "budget_ledger.jsonl",
    "timing_ledger": "timing_ledger.jsonl"
  }
}
```

## Risk

Estimated risk is medium. The risky part is threading trace metadata through core `src` functions without changing behavior. The safe part is append-only artifact writing and extra CSV/JSON fields.

The highest compatibility rule: do not change `generate_answer` to always return a dict. Keep its string return by default, and expose trace through an opt-in flag or wrapper.

## Avoid Breaking Current Metrics

- Preserve current keys: `latency_sec`, `retrieval_sec`, `metrics`, `details`, `judge`, `answer`, `chunks`, `retrieved_orgs`, and `first_hit_rank`.
- Preserve existing aggregate formulas.
- Append new metrics rather than replacing old ones.
- Keep `--dry-run` and `--no-judge` charge-free.
- If usage metadata is missing, record `usage_missing=true`; do not fail ordinary evals unless strict budget mode requires observed usage.

## Verification Plan

1. Run `python -m py_compile scripts\evaluate.py scripts\run_experiment_worker.py src\rag.py src\generator.py src\retriever.py`.
2. Run a no-API dry smoke: `python scripts\run_experiment_worker.py --run-dir <temp_run_dir> --suite baseline_default --worker-id trace_smoke --dry-run --no-judge --case-limit 1`.
3. Confirm old result keys still exist in `details.json` and `worker_output.json`.
4. Parse `budget_ledger.jsonl` and `cost_summary.json` with JSON loading.
5. Run `aggregate()` on synthetic details with and without trace fields and confirm existing metric values are identical.
