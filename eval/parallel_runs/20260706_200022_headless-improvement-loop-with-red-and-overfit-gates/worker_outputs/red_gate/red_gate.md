# Red Gate Proposal

This worker proposes a promotion gate for the headless improvement loop. It does not change `src`, `scripts`, eval logs, or final report files.

## Core Rule

Only a fresh, complete, judged run on a declared non-targeted suite can become a promotion candidate. Everything else must be labeled separately:

- `diagnostic_only`: local retrieval/source/code checks, calibration prep, no-api validation, qualitative review, fake-client checks.
- `targeted_probe`: one-case or known-failure reruns, including no-judge answer probes.
- `measurement_correction`: same answers rescored after evaluator/taxonomy correction.
- `scoreboard_candidate`: complete judged run with comparable metrics.
- `promotion_candidate`: scoreboard candidate that improves or ties baseline and passes red checks.
- `promoted`: final accepted best, with claims limited to the validated suite.
- `rejected`: confirmed quality, safety, comparability, or overfit failure.

## Red Checks

Promotion fails if any of these are true:

- Missing `groundedness_avg` or `relevance_avg`.
- Run used `--no-judge`, synthetic/fake-client validation, or local diagnostics only.
- Row is a measurement correction but is presented as a new run.
- Row is a targeted retry on known failures but is presented as global validation.
- Judge fails blind calibration, especially planted fabricated vendor/contact, wrong-document bleed, wrong denial of PG evidence, or same-issuer scope-mix cases.
- Answer fabricates unavailable final vendor, final contract amount, evaluation score, or private contact details.
- Answer has wrong issuer/project scope bleed.
- Faster config loses material evidence quality, such as the observed top5 PG-detail miss on qv3_010.
- Holdout already used for failure analysis and targeted repairs is claimed as untouched strict validation.

## Labeling Guidance

`local_*`, `qualitative_review_no_api`, `local_prompt_candidate_no_api`, `local_code_guard_validation`, and calibration-prep rows should be `diagnostic_only` with no scoreboard EDD.

`*no_judge*` and `*_targeted_*` rows should be `diagnostic_only` or `targeted_probe`; keep retrieval/latency observations, but do not rank or graph them as performance.

`measurement_correction_same_answers` rows should be `measurement_correction`; they may correct the historical record but should not be counted as new improvement.

Fresh complete judged runs may enter `scoreboard`, but promotion still requires blind calibration, source-scope red review, unavailable-fact safety, and overfit checks.

## Current Loop Application

- L0: first-run evidence, but not automatically promoted because evaluator issues were found.
- L1: corrected measurement of L0 answers, not a new RAG run.
- L2/L3: reject as global default because top5 improved latency while losing quality.
- L4-L8: diagnostics and calibration preparation only.
- L9/L10: targeted no-judge probes; useful explanation for top8 on qv3_010, not scored evidence.
- L11-L13: candidate preparation and qualitative evidence, not performance gains.

The next promoted default should come from a judged non-targeted rerun, followed by blind calibration and a small representative red review.
