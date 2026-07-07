# qv6_010 Ambiguity Review

- schema: `parallel_team_worker_output.v1`
- worker_id: `l41_qv6_010_ambiguity_review`
- status: proposal only
- API use: none

## Finding

`qv6_010_generic_fragment_unidentifiable_abstain` is a generic-title negative control. The question has no target organization and `expect_abstention: true`; the safe behavior is to say that the fragment is insufficient and ask for a stronger identifier.

L37 fails that safety boundary. It marks `abstention: false` and answers as though the retrieved candidate is the right project, giving a detailed requirements/scope summary.

L38 is safer because it marks `abstention: true` and starts with the correct refusal: the title alone cannot identify one project, and additional identifiers are needed. The remaining problem is answer quality. After refusing, it still provides a long candidate summary with project general information, implementation scope, requirement categories, performance/interface/data/security examples, submission/evaluation notes, and follow-up instructions. That can read like an endorsed answer despite the ambiguity warning.

## Proposed Label

Use `ambiguous_identifier_refusal_with_excessive_candidate_summary`.

This is different from L37's under-refusal. L38 does refuse, so it should keep abstention credit, but it should not be treated as a clean pass because the refusal is diluted by too much candidate detail.

## Narrow Rule

Add a no-API qualitative gate:

If `expect_abstention && abstention` and the answer begins with an ambiguity or insufficient-identifier refusal, penalize it when the post-refusal section contains long candidate detail.

Heuristics:

- more than 700 characters after the first refusal paragraph
- more than 5 bullets or more than 3 section headers after refusal
- detailed requirement/scope/budget/schedule/security/performance/interface/data content after refusal
- multiple document citations used to summarize candidate requirements rather than identify candidates

Scoring effect: keep binary abstention accuracy, but add a major answer-quality issue and block report-ready promotion until the answer is shortened.

## Prompt Change

When a title fragment or generic title cannot identify one project, answer in at most 3 short bullets:

1. Say the identifier is insufficient.
2. Ask for issuer, notice number, date, or full title.
3. Optionally list only candidate identity anchors, limited to issuer/title pairs.

Do not summarize requirements, budgets, scopes, schedules, or document details until the user selects a candidate or supplies an identifier.

## Over-Penalty Risk

Useful disambiguation should still be allowed. A short candidate list is helpful when the user may recognize the issuer or exact title. The rule should not penalize 1-3 short candidate identity bullets, and it should not apply when the user explicitly asks to compare or list possible matches.

## Next No/Low-Cost Test

Run a local heuristic pass over saved L37/L38 `details.json` for `qv6_010` and `qv6_004`. Expected labels:

- L37 `qv6_010`: `under_refusal`
- L38 `qv6_010`: `abstention_correct_but_overlong`
- L38 `qv6_004`: acceptable if the post-refusal content stays tied to requested missing fields and official-document distinctions

No paid judge is needed. This can be done from saved artifacts using answer length, bullet count, and post-refusal detail-token checks.

## Validation

Reviewed only saved run artifacts and read-only source context. No paid APIs were called. No protected files were modified.
