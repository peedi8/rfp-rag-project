# L65 Same-Project Guard Red Review

## Bottom Line

The qv6_001 failure should be treated as same-issuer, different-project source mixing. A guard is worth pursuing, but not as "same issuer is enough" and not as a hard global single-project filter.

Patch retrieval/context scoping first, then add a deterministic evaluation/report gate. A generation prompt-only fix is not enough because the current generator instructions already ask for evidence discipline, yet L64 still blended same-issuer material.

## Failure Shape

- Case: `qv6_001_uicc_fragment_scope`
- L64 metrics: coverage `1.0`, first hit rank `1`, no abstention
- Judge: groundedness `4`, relevance `5`
- Key issue: all retrieved orgs are the target issuer, but the answer drifted into unrelated same-issuer Basic Academic Data Center style operation/reporting/project-management material.

This is invisible to org-only retrieval coverage in `scripts/evaluate.py`.

## Main Risks

- Same-project false positive: one real project can have overview, SFR, operation support, attachment, and CSV-summary chunks.
- Alias/encoding split: mojibake, spaces, punctuation, and partial titles can make one project look like several.
- Wrong dominant project: a generic fragment must not pick the largest same-issuer group by frequency.
- Lost recall: qv6_001 needs title-fragment recovery, so exact-title filtering too early can drop the target.
- Clause leakage: generic management/reporting clauses should not be imported from another same-issuer project.
- Mislabeling: if target evidence was not retrieved, call it retrieval scope failure, not generation source mixing.

## Recommended Patch Point

1. Retrieval/context assembly:
   Group chunks by normalized project identity: issuer plus business title, with announcement/file metadata as tie-breakers where available. For issuer+fragment queries, select a dominant project only when query/title evidence supports it. Exclude off-project chunks before generation or mark the run as `mixed_project_same_issuer`.

2. Evaluation/reporting:
   Add no-API diagnostics: `project_scope_status`, `project_groups_seen`, `selected_project_identity`, `off_project_chunk_count`, and `answer_scope_status`. Keep this out of EDD until fixture-proven.

3. Generation:
   Optional secondary prompt line only after scoping exists: do not combine documents with different business names under the same issuer.

## No-API Fixtures To Prove

- `same_org_same_project_multidoc_pass`: same issuer and same UICC project across several document types should pass.
- `same_org_other_project_distractor_flagged`: target UICC chunks plus same-issuer distractor project chunks should flag or prune.
- `fragment_with_issuer_dominant_project_pass`: qv6_001-like partial title plus issuer should choose UICC only when evidence is strong.
- `generic_fragment_no_dominant_abstain`: qv6_010-like generic fragment should stay ambiguous.
- `alias_title_same_project_pass`: title variants should group as one project.
- `off_project_answer_citation_flagged`: answer using off-project doc numbers/topics should fail the diagnostic.
- `retrieval_missing_not_generation_fail`: missing target retrieval should be labeled retrieval scope failure.

## Red Lines

- Do not call this fixed based on judge score alone.
- Do not use global source-file search to justify the runtime answer.
- Do not put the diagnostic into EDD until the fixture pack passes.
- Do not make same issuer the trusted boundary.

No API/model calls were made. No protected paths were edited.
