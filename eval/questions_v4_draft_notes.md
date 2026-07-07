# v4 Draft Questions - No API

- created_at: 2026-07-06
- source: local `data_list.csv` metadata scan
- status: draft only, not yet scored
- purpose: prepare a fresher validation candidate after v2/v3 became partially exposed through diagnostics and targeted fixes.

## Design Notes

- Uses organizations not present in the existing question target-org registry when drafted.
- Mixes single extraction, within-project comparison, follow-up context, sensitive-domain scope control, ISP-vs-build guard, and final-vendor/contact abstention.
- This file must not be treated as untouched validation after anyone inspects answers, retrieval chunks, or failure causes from these questions.

## Gate Rule

Before this set can support a final generalization claim:

1. Freeze the question file.
2. Record first-run score separately.
3. Do not target-fix failures and then reuse the same score as strict validation.
4. Keep any later rerun labeled as targeted retry, regression, or measurement correction.

