# Experiment Hook Review: Answer-Format Prompt Candidate

## Scope

This is proposal-only. I reviewed the allowed experiment hook path and did not run API/model calls or edit source files.

Allowed files reviewed:

- `scripts/run_experiment_worker.py`
- `scripts/evaluate.py`
- `src/rag.py`
- `src/generator.py`
- `eval/next_improvement_tasks.md`
- `eval/parallel_runs/20260706_1825_timeboxed-red-loop-v3-validation/loop_points.csv`

## Recommendation

Add the new answer-format candidate through the existing `prompt_variant` mechanism, not through a default behavior change.

The current wiring already supports this:

- `scripts/run_experiment_worker.py` defines `prompt_sweep` rows with `prompt_variant`.
- `src/rag.py` carries `params["prompt_variant"]` into `generate_answer`.
- `src/generator.py` maps variant names in `PROMPT_VARIANTS` and falls back safely through `get_system_prompt`.

The low-risk source change for a future implementation is:

1. Add a new prompt constant in `src/generator.py`, for example `ANSWER_FORMAT_SAFETY_PROMPT`.
2. Add `"answer_format_safety": ANSWER_FORMAT_SAFETY_PROMPT` to `PROMPT_VARIANTS`.
3. Add a prompt sweep entry in `scripts/run_experiment_worker.py`:

```python
("prompt_answer_format_safety", {**CONTROL, "prompt_variant": "answer_format_safety"})
```

Keep `SYSTEM_PROMPT`, `DEFAULT_PARAMS`, and `CONTROL` unchanged.

## Candidate Intent

The prompt should focus on answer format and safety, not retrieval or scoring:

- answer only from retrieved reference documents;
- cite each concrete claim with a document number;
- keep answers concise and directly responsive;
- separate confirmed facts from unavailable fields;
- avoid blending facts across different projects or issuing organizations;
- abstain only when the requested information is not present in the provided evidence.

This should be treated as a candidate for later scoring, not as a claimed improvement.

## No-API Validation Checks

Before any scored run, validate only local wiring:

- Compile/import `src/generator.py` and `src/rag.py`.
- Check `get_system_prompt("answer_format_safety")` returns the new prompt.
- Check unknown variants still fall back to `SYSTEM_PROMPT`.
- Monkeypatch the OpenAI client in `src.generator` and verify `generate_answer(..., prompt_variant="answer_format_safety")` sends the new prompt as the system message without a network call.
- Monkeypatch `retrieve` and `generate_answer` in `src.rag` and verify `RAGPipeline(...).ask(...)` forwards `prompt_variant`.
- Run `scripts/run_experiment_worker.py` with `--dry-run` after adding the suite row to verify CSV/JSON output shape.

These checks prove the hook works. They do not prove answer quality.

## Future Scored Eval Plan

Run `prompt_sweep` later with judge enabled and identical retrieval controls. Compare the new row against `prompt_default`, `prompt_strict_evidence`, and `prompt_concise_verified`.

Promotion should require both score evidence and case-level review. The loop history distinguishes first validation, measurement correction, no-judge diagnostics, and targeted probes; the same separation should be preserved here. No dry-run, no-api check, or targeted example should be described as a score improvement.

Recommended review focus:

- source-scope bleed;
- unsupported detail risk;
- false abstention;
- missed abstention;
- citation clarity;
- directness and concision;
- whether missing fields are made explicit instead of hidden in vague prose.

## Risks

- A more polished format can mask unsupported synthesis.
- A stricter evidence instruction can raise false abstention.
- Mutating the default prompt would make the baseline ambiguous.
- Combining this with retrieval changes would make attribution unclear.
- Judge calibration concerns remain relevant, so scored promotion should include case-level inspection rather than relying only on aggregate EDD.
