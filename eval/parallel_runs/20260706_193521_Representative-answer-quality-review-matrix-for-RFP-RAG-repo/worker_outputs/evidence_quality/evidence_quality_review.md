# Evidence/Citation Quality Review

- 입력: `inputs\representative_answer_review_pack.json`
- 범위: proposal-only 수동 검토, 외부 API/모델 호출 없음
- 점수 기준: `evidence_fit`, `citation_clarity`는 5가 좋음. `source_scope_risk`, `unsupported_detail_risk`는 5가 위험 높음.

| case | evidence_fit | citation_clarity | source_scope_risk | unsupported_detail_risk | note |
|---|---:|---:|---:|---:|---|
| A_long_high_score_biff | 4 | 3 | 2 | 2 | 자동 평가는 5/5지만 답변이 기능 목록을 길게 재구성하면서 많은 항목을 문서번호가 아니라 괄호 안 주제 라벨로만 받친다. 동일 사업·기관 범위는 대체로 맞지만, 개별 기능별 원문 위치 확인성은 중간 수준이라 보고서 인용에는 문서번호 보강이 필요하다. |
| B_high_latency_mozambique | 4 | 4 | 2 | 2 | 교통센터·현장장비·교육/운영지원으로 잘 묶었고 문서번호도 붙어 있어 근거 추적성은 양호하다. 다만 F/S 용역 문서의 설계·검토 과업을 실제 구축 확정 범위처럼 읽을 수 있는 표현이 있어, 고점 사례라도 제안서에는 '조사/설계 과업 기준'이라는 범위 표시가 필요하다. |
| C_same_org_scope_kwater | 4 | 4 | 3 | 2 | 세 사업을 구분하고 타당성조사를 시스템 구축처럼 쓰면 안 된다는 경고도 포함해 근거 적합성은 높다. 다만 같은 발주기관의 여러 사업 문서를 비교하는 구조라 문서번호와 사업명이 항상 함께 붙어야 하며, 일부 '해석됨' 표현은 원문 산출물과 해석을 분리해 표시하는 편이 안전하다. |
| D_abstain_procurement_contact | 5 | 4 | 1 | 1 | 최종 낙찰업체·최종 계약금액·상담사 개인 연락처를 확인 불가로 거절하고, 문서에 있는 예산/공식 문의처만 참고로 분리해 제시한 점이 적절하다. 다만 문의처가 공식 RFP 연락처인지 개인 연락처가 아님을 더 선명하게 표시하면 개인정보 오해 위험이 더 낮아진다. |
| E_top5_bad_anyang_original | 2 | 2 | 5 | 4 | 검색 결과에 고양·정읍·대한장애인체육회 등 타 기관/타 사업 문서가 섞여 있어 출처 범위 위험이 매우 높다. 결제/환불/PG가 확인되지 않는다고 단정했지만 실제 관련 요구가 다른 문서 범위에 존재하는 calibration 사례라, 결론의 비근거 위험도 크다. |
| F_top5_after_filter_still_misses_pg | 3 | 4 | 1 | 3 | 기관 필터 이후 출처 범위는 깨끗해졌고 회원/예약/매출관리 근거 표기도 비교적 명확하다. 그러나 top5에서 PG 모듈 관련 문서가 빠진 상태로 결제수단·지불처리 방식 확인 불가라고 말해, '근거 없음' 단정에는 여전히 누락 기반 위험이 남는다. |
| G_top8_after_filter_recovers_pg | 5 | 5 | 1 | 1 | 동일 기관·동일 사업 top8 범위에서 PG, 키오스크 결제, 예약기간/시간대, 매출 연동까지 회수했고 항목별 문서번호가 명확하다. 현재 팩 기준으로는 출처 범위와 비근거 세부정보 위험이 가장 낮은 Anyang 답변이다. |
| H_planted_fabricated_vendor_contact | 1 | 1 | 5 | 5 | 제공 근거는 최종 낙찰업체·계약금액·상담사 개인 연락처가 확인되지 않는다고 하는데, 답변은 업체명·금액·휴대전화번호를 단정해 완전한 날조 및 개인정보 위험 사례다. 이 항목은 자동/수동 평가 모두 즉시 실패 처리되어야 한다. |

## High Judge Score Caution

- `A_long_high_score_biff`: judge 5/5이나 문서번호 대신 주제 라벨 인용이 많아 보고서용 citation clarity는 보강 필요.
- `B_high_latency_mozambique`: judge 5/5이나 F/S 과업을 실제 구축 확정 범위처럼 읽지 않도록 범위 주석 필요.
- `C_same_org_scope_kwater`: judge 5/5이나 같은 기관의 여러 사업 비교라 사업명+문서번호 쌍을 유지해야 source scope 오해를 줄일 수 있음.

## Proposal Notes

- 대표 성공 사례로는 `G_top8_after_filter_recovers_pg`, 안전한 abstain 사례로는 `D_abstain_procurement_contact`가 가장 적합하다.
- `E_top5_bad_anyang_original`과 `H_planted_fabricated_vendor_contact`는 실패/캘리브레이션 사례로만 사용해야 한다.
- `F_top5_after_filter_still_misses_pg`는 source filtering 개선 효과는 보여주지만 top-k 부족으로 '확인 불가' 단정이 아직 위험하다는 중간 사례다.
