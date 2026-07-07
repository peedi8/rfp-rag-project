# RFP Question Bank Gap Review - 2026-07-07

## Decision

Do not run the 95-row bank as one full evaluation. Use it as a gap source. The rule here is not a 12-16 cap: cut pattern-known rows, keep every row that adds a new or undercovered signal, and split non-ordinary-RAG work into its own lane.

## Counts

- total bank rows: 95
- kept candidates: 68
- cut as pattern-known for now: 27

| decision | count |
|---|---:|
| `keep_new_lane` | 47 |
| `cut_pattern_known` | 27 |
| `keep_new_or_undercovered` | 18 |
| `keep_as_concrete_seed` | 3 |

## Kept Candidate Lanes

| lane | count | why separate |
|---|---:|---|
| `conversation_or_selected_project_rag` | 24 | the question is underspecified until a project/context seed is fixed |
| `metadata_corpus_analytics` | 13 | whole-corpus ranking/filtering/counting needs metadata or corpus tools, not only retrieved RFP chunks |
| `ordinary_rag_text` | 9 | can be tested as normal RAG text if body-visible support is confirmed |
| `ordinary_rag_text_or_mixed` | 8 | persona/usefulness output can be grounded, but recommendation wording needs sidecar checks |
| `unsupported_absent_or_mixed` | 6 | must refuse or caveat unavailable guarantees while still giving useful check items |
| `system_instrumentation` | 6 | requires retrieval trace, citation, filter, latency, or failure-diagnosis instrumentation |
| `mixed` | 2 | combines answerable document fields with business judgment or unsupported limits |

## Kept IDs By Segment

- `RAG평가` (6): Q090, Q091, Q092, Q093, Q094, Q095
- `계약/입찰` (8): Q038, Q039, Q040, Q041, Q042, Q043, Q044, Q045
- `기술검토` (10): Q046, Q047, Q048, Q049, Q050, Q051, Q052, Q053, Q054, Q055
- `단일문서` (3): Q024, Q026, Q027
- `모호질문` (4): Q062, Q063, Q064, Q065
- `부정질문` (6): Q075, Q076, Q077, Q079, Q080, Q081
- `비교/종합` (5): Q033, Q034, Q035, Q036, Q037
- `사용자수준` (8): Q082, Q083, Q084, Q085, Q086, Q087, Q088, Q089
- `전체탐색` (12): Q001, Q002, Q003, Q004, Q005, Q006, Q007, Q008, Q009, Q010, Q011, Q012
- `후속질문` (6): Q067, Q069, Q070, Q071, Q072, Q073

## Cut IDs For Now

- `단일문서` (12): Q013, Q014, Q015, Q016, Q017, Q018, Q019, Q020, Q021, Q022, Q023, Q025
- `모호질문` (6): Q056, Q057, Q058, Q059, Q060, Q061
- `부정질문` (2): Q074, Q078
- `비교/종합` (5): Q028, Q029, Q030, Q031, Q032
- `후속질문` (2): Q066, Q068

## Execution Rule

- Freeze a lane before answer inspection; do not silently swap rows after a first run.
- Do not compare EDD across different lanes/gates as if it were one number.
- Metadata/corpus analytics and RAG ops rows need tool/harness evaluation, not the normal answer generator alone.
- Conversation rows need a fixed seed turn, otherwise the answer target is undefined.
- Keep every run labeled `diagnostic_candidate_only` until a manifest and exposure entry are written before answer execution.

## Next Work Queue

1. Build lane-specific frozen files from the kept candidates, starting with one metadata/corpus analytics file, one contract/technical selected-project file, and one persona/usefulness file.
2. For selected-project rows, choose seed projects before running answers and record why each seed was chosen.
3. Add sidecar blockers before scoring: exact-value availability, project/context loss, unsupported guarantee, over-refusal, overlong persona answer, and instrumentation missing.
4. Only then run answers lane by lane and record cause, result, insight, and next-basis per loop point.

