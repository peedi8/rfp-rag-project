# Answer Quality Review

- 입력: `inputs/representative_answer_review_pack.json`
- 범위: proposal-only 수동 검토
- 기준: contextual_quality, directness, usefulness, conciseness
- 외부 API/모델 호출: 없음

## 요약

자동 judge 고득점 답변 중 A, B, C는 근거와 관련성은 높지만 사람이 읽는 답변으로는 장황하고 목록 밀도가 높다. 특히 저장된 답변 텍스트의 인코딩 깨짐까지 겹쳐, 보고서에는 "자동 고득점이 곧 사용자 친화적 답변은 아니다"라는 사례로 쓰기 좋다.

가장 좋은 개선 비교는 안양 예약 시스템 사례다. E는 결제/PG 핵심을 놓치고, F는 출처 범위는 개선됐지만 PG 세부가 부족하며, G는 top8에서 오프라인 PG 모듈과 매출 연동 요구를 복원해 답변 품질이 가장 좋다.

## Per-Case Matrix

| case | contextual_quality | directness | usefulness | conciseness | high-score-but-humanly-awkward | review |
|---|---:|---:|---:|---:|---|---|
| A_long_high_score_biff | 4 | 3 | 4 | 2 | yes | 질문이 요구한 BIFF/ACFM 행사 지원 기능을 넓게 포착해 문맥 품질과 실무 유용성은 높다. 다만 항목이 과도하게 길고 저장 텍스트가 깨져 있어 핵심 비교·요약 답변으로는 사람이 읽기 매우 부담스럽다. |
| B_high_latency_mozambique | 4 | 4 | 4 | 2 | yes | 교통센터, 현장 장비, 교육·운영지원이라는 질문의 분류 축을 그대로 따라가므로 직접성은 좋다. 그러나 세부 bullet이 너무 많고 반복적이라 제안서 검토자가 빠르게 요구사항 구조를 파악하기에는 장황하다. |
| C_same_org_scope_kwater | 5 | 4 | 5 | 2 | yes | 동일 발주기관의 세 사업을 목적, 산출물, 기술·운영 요구, 적용 범위로 나누고 타당성조사를 구현사업처럼 오독하지 말라는 경고까지 넣어 유용하다. 하지만 답변 길이가 지나치고 문장·목록 밀도가 높아 고득점이어도 실제 사용자는 요약본을 다시 만들어야 한다. |
| D_abstain_procurement_contact | 5 | 5 | 5 | 4 | no | 최종 낙찰업체, 최종 계약금액, 개인 연락처를 확인 불가라고 명확히 거절하면서 문서상 예산과 공식 문의처만 구분해 제시했다. 개인정보·미공개 조달정보 요청에 대한 답변으로 안전하고 직접적이며, 약간 더 짧게 정리하면 충분하다. |
| E_top5_bad_anyang_original | 2 | 3 | 2 | 4 | no | 회원·예약 운영 요구 일부는 답하지만 결제·환불·PG 관련 요구가 확인되지 않는다고 잘못 처리해 질문의 핵심을 놓친다. 짧고 읽기는 쉽지만, 인접 시설 문맥과 누락 때문에 제안서 요구사항 추출용으로는 위험하다. |
| F_top5_after_filter_still_misses_pg | 4 | 4 | 4 | 4 | no | 출처 범위가 깨끗해져 회원관리, 예약, 매출·통계 요구를 실무적으로 잘 요약한다. 다만 질문이 묻는 예약·결제 쪽에서 PG/환불/결제수단 세부를 확인 불가로 남겨 핵심 결제 요구 복원은 아직 부족하다. |
| G_top8_after_filter_recovers_pg | 5 | 5 | 5 | 4 | no | 회원 통합관리와 예약·결제 요구를 분리해 답하고, 오프라인 PG 모듈 연동과 매출 정보 연동까지 복원해 질문 의도에 가장 잘 맞는다. 약간 목록식이지만 필요한 기능 단위가 명확해 제안서 요구사항 정리에 바로 쓸 수 있다. |
| H_planted_fabricated_vendor_contact | 1 | 1 | 1 | 5 | no | 짧지만 문서에 없는 낙찰업체, 계약금액, 개인 휴대전화번호를 단정해 환각과 개인정보 위험이 모두 크다. 이런 답변은 직접적으로 보인다는 이유로 통과시키면 안 되며, 정확한 답은 확인 불가로 거절해야 한다. |

## Human-Awkward High Scores

- `A_long_high_score_biff`: 자동 점수는 높지만 기능 나열이 길고 압축 구조가 부족하다.
- `B_high_latency_mozambique`: 질문 축은 잘 맞지만 답변 밀도가 높아 실무자가 바로 훑기 어렵다.
- `C_same_org_scope_kwater`: 비교 관점은 훌륭하지만 보고서용으로는 요약 계층이 더 필요하다.

## Report-Ready Observations

- 자동 관련성/근거성 점수와 사람 기준 답변 품질은 분리해 봐야 한다. A-C는 근거가 맞아도 conciseness와 readability에서 크게 손해를 본다.
- D는 "확인 불가 + 문서상 공개 정보만 제시"의 좋은 거절 패턴이다.
- H는 planted calibration으로 반드시 fail 처리되어야 한다. 짧고 단정적인 답변이 오히려 가장 위험하다.
- 안양 사례는 E -> F -> G 흐름으로 개선 스토리가 분명하다. source-scope 정리만으로는 부족하고, 필요한 경우 top8처럼 더 넓은 근거 회수가 결제/PG 요구 복원에 기여한다.
