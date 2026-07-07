# v6 Metamorphic Proposal Evidence

Worker: `v6_metamorphic`

Scope: proposal-only design for an unseen v6 RAG eval cohort focused on title-fragment generalization plus metamorphic/property tests.

Files read:

- `eval/questions_v5_adversarial_frozen_first_run.json`
- `eval/questions_v4_frozen_first_run.json`
- `eval/question_exposure_registry.json`
- `eval/rnd_rag_eval_methods_20260706.md`
- `eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/ledger.json`

Main observations:

- v4/v5 already exercise several exposed patterns: ISP-versus-build, feasibility-versus-implementation, forbidden final vendor/contact details, budget-versus-contract, similar-project contamination, and one paraphrase-stability group.
- The exposure registry says frozen first runs are the only strict validation basis, and inspected sets become regression or diagnostic material.
- The R&D note explicitly recommends metamorphic/property tests: paraphrase invariance, irrelevant-context injection, and evidence-removal checks.

Design choice:

The JSON proposal intentionally avoids concrete reused v4/v5 titles and organizations. It recommends deterministic unseen corpus selection and freeze-before-run so the merge owner can instantiate concrete Korean prompts without leaking answers or converting v6 into an exposed hand-tuned set.

Cost/API note:

No paid APIs were called. This worker only read local files and wrote the proposal/evidence files under `worker_outputs`.
