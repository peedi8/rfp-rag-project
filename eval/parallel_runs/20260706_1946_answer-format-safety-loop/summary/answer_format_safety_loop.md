# Answer Format Safety Loop

- started_at: `2026-07-06 19:46 KST`
- run_dir: `eval\parallel_runs\20260706_1946_answer-format-safety-loop`
- score type: `local_prompt_candidate_and_no_api_validation`
- EDD: N/A
- model/API calls: none

## Inputs

- previous quality matrix: `eval\parallel_runs\20260706_193521_Representative-answer-quality-review-matrix-for-RFP-RAG-repo\summary\answer_quality_review_matrix.json`
- prior loop points: `eval\parallel_runs\20260706_1825_timeboxed-red-loop-v3-validation\loop_points.csv`
- current prompt code: `src\generator.py`
- current experiment hook: `scripts\run_experiment_worker.py`

## Proposals Reviewed

- prompt format proposal: `worker_outputs\prompt_format\prompt_format_review.json`
- safety/abstention proposal: `worker_outputs\safety_format\safety_format_review.json`
- experiment hook proposal: `worker_outputs\experiment_hook\experiment_hook_review.json`

## Accepted Change

- Added a new prompt variant: `report_ready`.
- Added `prompt_report_ready` to `prompt_sweep`.
- Kept `DEFAULT_PARAMS["prompt_variant"]` unchanged as `default`.

## Why

- A/B/C in the representative quality matrix showed high automated scores but weaker human readability: answers were grounded, yet too verbose or weakly structured.
- D/H showed the safety boundary: a good answer should preserve supported public RFP facts while refusing final award, final contract amount, private contact, and fabricated procurement details.
- E/F/G showed that prompt formatting alone cannot recover missing evidence. Retrieval depth and source scope remain separate controls.

## No-API Checks

- `py_compile`: pass for `src\generator.py`, `src\rag.py`, `scripts\run_experiment_worker.py`.
- static prompt check: pass.
- `generate_answer` fake-client check: pass; `report_ready` is placed in the system prompt without a network call.
- `RAGPipeline` forwarding check: pass; `prompt_variant="report_ready"` reaches generation and adaptive top-k still upgrades the facility payment query to top8.
- prompt suite check: pass; `prompt_report_ready` is present in `prompt_sweep`.

## Decision

- Keep `report_ready` as a candidate only.
- Do not claim EDD improvement yet.
- Next scored step, when cost is acceptable: run `prompt_sweep` on a small mixed set and compare `prompt_report_ready` against `default`, `strict_evidence`, and `concise_verified`.

