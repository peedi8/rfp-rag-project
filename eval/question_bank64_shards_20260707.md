# Question Bank 64-Case Shard Plan - 2026-07-07

## Rule

Start from the 68 kept diagnostic candidates, remove four rows that are mostly experiment-harness/meta work, then split the remaining 64 into four 16-case shards. This is still candidate preparation, not an answer run.

## Excluded From This 64

| id | reason | later lane |
|---|---|---|
| `Q092` | metadata filter on/off comparison is an experiment harness task, not a user-facing RFP answer case. | RAG ops harness |
| `Q093` | latency measurement is an instrumentation metric, not a normal RAG answer question. | RAG ops harness |
| `Q094` | failure diagnosis requires a known wrong answer/run trace first; use after a failed run, not in the first 64. | RAG ops harness |
| `Q095` | question-set classification is eval design meta-work and duplicates the current orchestration task. | RAG ops harness |

## Shards

### A_metadata_corpus

- count: `16`
- ids: `Q001`, `Q002`, `Q003`, `Q004`, `Q005`, `Q006`, `Q007`, `Q008`, `Q009`, `Q010`, `Q011`, `Q012`, `Q065`, `Q033`, `Q034`, `Q035`
- lanes: `metadata_corpus_analytics` 13, `ordinary_rag_text` 3

| id | segment | intent | lane | seed required |
|---|---|---|---|---|
| `Q001` | 전체탐색 | 코퍼스 개요 | `metadata_corpus_analytics` | `false` |
| `Q002` | 전체탐색 | 기관/사업 탐색 | `metadata_corpus_analytics` | `false` |
| `Q003` | 전체탐색 | 예산 탐색 | `metadata_corpus_analytics` | `false` |
| `Q004` | 전체탐색 | 예산 필터 | `metadata_corpus_analytics` | `false` |
| `Q005` | 전체탐색 | 예산 필터 | `metadata_corpus_analytics` | `false` |
| `Q006` | 전체탐색 | 도메인 탐색 | `metadata_corpus_analytics` | `false` |
| `Q007` | 전체탐색 | 도메인 탐색 | `metadata_corpus_analytics` | `false` |
| `Q008` | 전체탐색 | 도메인 탐색 | `metadata_corpus_analytics` | `false` |
| `Q009` | 전체탐색 | 도메인 탐색 | `metadata_corpus_analytics` | `false` |
| `Q010` | 전체탐색 | 도메인 탐색 | `metadata_corpus_analytics` | `false` |
| `Q011` | 전체탐색 | 국제사업 탐색 | `metadata_corpus_analytics` | `false` |
| `Q012` | 전체탐색 | 형식 탐색 | `metadata_corpus_analytics` | `false` |
| `Q065` | 모호질문 | 약어 | `metadata_corpus_analytics` | `false` |
| `Q033` | 비교/종합 | 유사사업 탐색 | `ordinary_rag_text` | `false` |
| `Q034` | 비교/종합 | 국제사업 비교 | `ordinary_rag_text` | `false` |
| `Q035` | 비교/종합 | 행사/문화 비교 | `ordinary_rag_text` | `false` |

### B_contract_technical_extract

- count: `16`
- ids: `Q024`, `Q026`, `Q027`, `Q038`, `Q039`, `Q040`, `Q041`, `Q042`, `Q043`, `Q044`, `Q045`, `Q046`, `Q047`, `Q048`, `Q049`, `Q050`
- lanes: `ordinary_rag_text` 3, `conversation_or_selected_project_rag` 13

| id | segment | intent | lane | seed required |
|---|---|---|---|---|
| `Q024` | 단일문서 | 제출/계약 조건 | `ordinary_rag_text` | `false` |
| `Q026` | 단일문서 | 접근성 요구 | `ordinary_rag_text` | `false` |
| `Q027` | 단일문서 | 재해복구 요구 | `ordinary_rag_text` | `false` |
| `Q038` | 계약/입찰 | 제출 조건 | `conversation_or_selected_project_rag` | `true` |
| `Q039` | 계약/입찰 | 평가기준 | `conversation_or_selected_project_rag` | `true` |
| `Q040` | 계약/입찰 | 계약 방식 | `conversation_or_selected_project_rag` | `true` |
| `Q041` | 계약/입찰 | 참가자격 | `conversation_or_selected_project_rag` | `true` |
| `Q042` | 계약/입찰 | 예산/금액 | `conversation_or_selected_project_rag` | `true` |
| `Q043` | 계약/입찰 | 기간/일정 | `conversation_or_selected_project_rag` | `true` |
| `Q044` | 계약/입찰 | 검수/산출물 | `conversation_or_selected_project_rag` | `true` |
| `Q045` | 계약/입찰 | 유지보수 | `conversation_or_selected_project_rag` | `true` |
| `Q046` | 기술검토 | 연계/API | `conversation_or_selected_project_rag` | `true` |
| `Q047` | 기술검토 | 시스템 구성 | `conversation_or_selected_project_rag` | `true` |
| `Q048` | 기술검토 | 데이터 요구 | `conversation_or_selected_project_rag` | `true` |
| `Q049` | 기술검토 | UI/UX 요구 | `conversation_or_selected_project_rag` | `true` |
| `Q050` | 기술검토 | 개인정보/보안 | `conversation_or_selected_project_rag` | `true` |

### C_technical_followup_boundary

- count: `16`
- ids: `Q051`, `Q052`, `Q053`, `Q054`, `Q055`, `Q062`, `Q063`, `Q064`, `Q067`, `Q069`, `Q070`, `Q071`, `Q072`, `Q073`, `Q075`, `Q076`
- lanes: `conversation_or_selected_project_rag` 11, `ordinary_rag_text` 3, `unsupported_absent_or_mixed` 2

| id | segment | intent | lane | seed required |
|---|---|---|---|---|
| `Q051` | 기술검토 | 테스트/품질 | `conversation_or_selected_project_rag` | `true` |
| `Q052` | 기술검토 | 운영/배포 | `conversation_or_selected_project_rag` | `true` |
| `Q053` | 기술검토 | 데이터 이관 | `conversation_or_selected_project_rag` | `true` |
| `Q054` | 기술검토 | AI 요구 확인 | `conversation_or_selected_project_rag` | `true` |
| `Q055` | 기술검토 | 인증/규정 | `conversation_or_selected_project_rag` | `true` |
| `Q062` | 모호질문 | 사업명 일부 | `ordinary_rag_text` | `false` |
| `Q063` | 모호질문 | 중복 후보 | `ordinary_rag_text` | `false` |
| `Q064` | 모호질문 | 기관명 오류 | `ordinary_rag_text` | `false` |
| `Q067` | 후속질문 | 추가조건 | `conversation_or_selected_project_rag` | `true` |
| `Q069` | 후속질문 | 예산 비교 | `conversation_or_selected_project_rag` | `true` |
| `Q070` | 후속질문 | 유사사업 확장 | `conversation_or_selected_project_rag` | `true` |
| `Q071` | 후속질문 | 기술 상세 | `conversation_or_selected_project_rag` | `true` |
| `Q072` | 후속질문 | 요약 수준 변경 | `conversation_or_selected_project_rag` | `true` |
| `Q073` | 후속질문 | 쉬운 설명 | `conversation_or_selected_project_rag` | `true` |
| `Q075` | 부정질문 | 미래/최신 정보 | `unsupported_absent_or_mixed` | `true` |
| `Q076` | 부정질문 | 없는 금액 | `unsupported_absent_or_mixed` | `true` |

### D_persona_business_citation

- count: `16`
- ids: `Q077`, `Q079`, `Q080`, `Q081`, `Q082`, `Q083`, `Q084`, `Q085`, `Q086`, `Q087`, `Q088`, `Q089`, `Q090`, `Q091`, `Q036`, `Q037`
- lanes: `unsupported_absent_or_mixed` 4, `ordinary_rag_text_or_mixed` 8, `system_instrumentation` 2, `mixed` 2

| id | segment | intent | lane | seed required |
|---|---|---|---|---|
| `Q077` | 부정질문 | 법률 판단 | `unsupported_absent_or_mixed` | `true` |
| `Q079` | 부정질문 | 과도한 단정 | `unsupported_absent_or_mixed` | `true` |
| `Q080` | 부정질문 | 근거 없는 추천 | `unsupported_absent_or_mixed` | `true` |
| `Q081` | 부정질문 | 문서 밖 규정 | `unsupported_absent_or_mixed` | `true` |
| `Q082` | 사용자수준 | 쉬운 설명 | `ordinary_rag_text_or_mixed` | `true` |
| `Q083` | 사용자수준 | 실행 체크리스트 | `ordinary_rag_text_or_mixed` | `true` |
| `Q084` | 사용자수준 | 기술 리스크 | `ordinary_rag_text_or_mixed` | `true` |
| `Q085` | 사용자수준 | 의사결정 요약 | `ordinary_rag_text_or_mixed` | `true` |
| `Q086` | 사용자수준 | 사업 적합성 | `ordinary_rag_text_or_mixed` | `true` |
| `Q087` | 사용자수준 | 용어 풀이 | `ordinary_rag_text_or_mixed` | `true` |
| `Q088` | 사용자수준 | 고객 설명문 | `ordinary_rag_text_or_mixed` | `true` |
| `Q089` | 사용자수준 | 영업 포인트 | `ordinary_rag_text_or_mixed` | `true` |
| `Q090` | RAG평가 | 검색성능 | `system_instrumentation` | `false` |
| `Q091` | RAG평가 | 근거성 | `system_instrumentation` | `false` |
| `Q036` | 비교/종합 | 우선순위 | `mixed` | `false` |
| `Q037` | 비교/종합 | 사업성 판단 | `mixed` | `false` |

## Execution Caution

- Do not report one merged EDD across all four shards without lane labels.
- Shards with selected-project rows require concrete seed projects before answer execution.
- Metadata/corpus and system-trace rows need tool or harness metrics beside ordinary answer quality.
- Freeze/register the exact runnable files again before the first answer run.


## Worker Review Merge Decision

The four shard reviews were accepted as proposal evidence. The physical 64-case split remains unchanged because moving the three ordinary comparison rows out of shard A would only move mixed-lane risk into another shard.

Accepted caveats:

- A keeps `Q033-Q035` physically, but they are a quarantined `ordinary_rag_text_cluster_comparison` subtotal and must not be folded into the metadata analytics subtotal.
- B requires fixed selected-project seeds for `Q038-Q050` before answer execution.
- C requires separate execution buckets for selected-project technical rows, corpus-wide discovery rows, ambiguity correction, follow-up memory, and unsupported-boundary rows.
- D requires sublane reporting for unsupported guarantees, persona usefulness, system citation transparency, and business recommendation boundary.
- `Q090-Q091` require retrieval/citation trace artifacts; if instrumentation is unavailable, mark them blocked or move them to a later instrumentation-only run.
