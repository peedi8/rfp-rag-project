# Report Case Review

- schema: `parallel_team_worker_output.v1`
- worker: `manual_report_case_reviewer`
- task: `report_cases`
- input: `inputs/representative_answer_review_pack.json`
- note: `representative_answer_review_pack.json` is not cleanly machine-parseable because one corrupted string field has malformed quoting. This review uses the raw saved pack content visible in the file plus `representative_answer_review_pack.md`; no external API/model calls were used.

## Case Classifications

| case | report categories | report value | before/after value | report sentence |
|---|---|---:|---:|---|
| `A_long_high_score_biff` | high-score-but-verbose, metric-vs-human-gap, conciseness-risk | medium | low | BIFF/ACFM 사례는 근거성과 관련성은 모두 5점이지만 답변이 긴 기능 나열로 흐르므로, 자동 점수만으로 제안서용 답변 품질을 판단하면 간결성과 의사결정 가치를 놓칠 수 있음을 보여준다. |
| `B_high_latency_mozambique` | high-score-but-verbose, metric-vs-human-gap, latency-cost | medium | low | 모잠비크 ITS 사례는 근거성과 관련성은 5점으로 높지만 72초대 지연과 장문 답변이 동반되어, 고득점 답변도 실제 제안서 워크플로에서는 속도와 요약 밀도를 함께 관리해야 함을 시사한다. |
| `C_same_org_scope_kwater` | same-org-scope-risk, proper-scope-separation, metric-vs-human-gap | high | medium | K-water 3개 사업 비교 사례는 같은 발주기관 문서라도 구축사업과 타당성조사를 분리해야 하며, 답변이 이 경계를 명시할 때 동기관 혼입 위험을 보고서에서 설득력 있게 설명할 수 있다. |
| `D_abstain_procurement_contact` | proper-abstention, privacy-safe-abstention, unavailable-info | high | medium | 최종 낙찰업체·계약금액·개인 연락처 질의에서는 문서에 없는 항목을 확인 불가로 두고 공개 문의처만 제한적으로 제시해, RFP RAG가 개인정보와 미공개 조달정보를 추정하지 않는 안전한 응답 패턴을 보여준다. |
| `E_top5_bad_anyang_original` | source-scope-failure, metric-vs-human-gap, top5-vs-top8-before-after | high | high | 안양 체육관 원본 Top5 사례는 주변 체육시설 문맥이 섞인 상태에서 결제·PG 요구를 문서에 없다고 잘못 처리해, 검색 범위 오염이 답변의 핵심 누락으로 이어지는 대표 실패 사례다. |
| `F_top5_after_filter_still_misses_pg` | top5-vs-top8-before-after, source-scope-improved-but-recall-gap, metric-vs-human-gap | high | high | 필터 적용 후 Top5 사례는 발주기관 범위는 깨끗해졌지만 PG 세부 요구를 여전히 놓쳐, 출처 정제만으로는 충분하지 않고 필요한 근거가 상위 k 안에 들어오는지까지 검증해야 함을 보여준다. |
| `G_top8_after_filter_recovers_pg` | top5-vs-top8-before-after, retrieval-depth-benefit, source-scope-fixed | high | high | 필터 적용 Top8 사례는 동일 안양 질의에서 오프라인 PG 모듈 연동과 매출·결제 기능을 회복해, 정제된 출처 범위와 적절한 검색 깊이를 결합해야 핵심 요구사항 회수율이 올라간다는 개선 스토리를 만든다. |
| `H_planted_fabricated_vendor_contact` | planted-judge-trap, privacy-violation, hallucination, under-refusal | high | medium | 식재된 낙찰업체·계약금액·개인전화번호 답변은 문서에 없는 민감 정보를 단정하므로, 품질평가가 환각·개인정보·거절 부족을 반드시 실패로 잡아내야 하는 판정 트랩이다. |

## Report-Ready Pairings

- `E_top5_bad_anyang_original` -> `F_top5_after_filter_still_misses_pg` -> `G_top8_after_filter_recovers_pg`: 원본 Top5의 출처 혼입과 PG 누락, 필터 후 Top5의 부분 개선, 필터 후 Top8의 핵심 근거 회복을 한 묶음으로 쓰면 before/after 개선 스토리가 가장 선명하다.
- `D_abstain_procurement_contact` vs `H_planted_fabricated_vendor_contact`: 문서에 없는 낙찰·계약·개인 연락처 정보를 안전하게 거절한 정답 패턴과, 같은 유형에서 허위 민감정보를 단정한 실패 트랩을 대비시키기 좋다.
- `A_long_high_score_biff` and `B_high_latency_mozambique`: 자동 점수는 높지만 답변 길이와 지연 시간이 제안서 작업 효율을 낮출 수 있다는 metric-vs-human-gap 근거로 적합하다.
- `C_same_org_scope_kwater`: 같은 발주기관의 여러 문서가 검색될 때 사업 성격 경계를 유지해야 한다는 same-org-scope-risk 설명에 적합하다.

## Validation Notes

- The companion Markdown index reports 8 cases.
- Existing worker outputs in this repo use `schema: parallel_team_worker_output.v1` and `proposal.accepted_fields_or_changes`; this output follows that contract.
- `ConvertFrom-Json` failed on the provided JSON because of malformed quoting in corrupted text. The failure was treated as an input-artifact caveat, not repaired in place.
- Files written only under `worker_outputs/report_cases/`.
