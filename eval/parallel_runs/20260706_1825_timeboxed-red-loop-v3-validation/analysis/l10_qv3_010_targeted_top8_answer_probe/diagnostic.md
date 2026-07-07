# L10 qv3_010 Targeted Top8 Answer Probe

- judge call: false
- scope: one qv3_010 top_k=8 answer after L4-L9
- coverage: 1.0
- first_hit_rank: 1
- latency_sec: 18.16
- retrieved_orgs: ['경기도 안양시', '경기도 안양시', '경기도 안양시', '경기도 안양시', '경기도 안양시', '경기도 안양시', '경기도 안양시', '경기도 안양시']
- all_retrieved_orgs_target: True
- manual_read_flags: source_scope_clean, payment_present, pg_recovered, top8_better_for_pg_detail

## Term Presence
- 예약: True
- 결제: True
- PG: True
- 회원: True
- 키오스크: True
- 발권: True
- 매출: True

## Manual Read Decision

Top8 keeps the fixed issuer scope and recovers PG/payment details in the answer. For qv3_010, top8 is the safer setting than top5; top5 was source-clean after L4-L8 but still missed PG detail.

## Answer

근거: 사업명 "호계체육관 배드민턴장 및 탁구장 예약 시스템 구축" / 발주기관: 경기도 안양시 (제공 문서 기준)

요약 — 회원통합운영(회원관리)
- 회원 등록·수정·삭제·상태변경 기능 제공. (문서3)
- 2년간 이용 이력 없는 회원은 이메일 통보 후 DB에서 완전 삭제. (문서3)
- 주기적 개인정보 활용 동의 프로세스 구현 필요. (문서3)
- 중복회원 방지 및 운영자가 확인·관리할 수 있도록 구현. (문서3)
- 운영자가 성명·전화번호 뒷자리 등으로 다양한 화면에서 신속히 검색 가능해야 함. (문서3)
- 개인정보 보호·시큐어 코딩 적용 요구(시민 개인정보 안전 관리). (문서1·문서6)

요약 — 예약/결제
- 배드민턴장·탁구장 예약을 구분 구축, 관리자가 예약기간·시간대 설정 가능. (문서8)
- 홈페이지에서는 당일예약 불가, 현장 키오스크에서는 당일예약 가능하도록 분리. (문서8)
- 관리자가 휴무일 지정 시 해당일은 예약 차단. (문서8)
- 키오스크는 회원·비회원 입장에 대한 매출등록·결제 기능 제공, 외부 오프라인 PG 모듈 연동 요구. (문서8)
- 키오스크 장비 제어 인터페이스·발권기 설정·출력물 변경 기능 및 제어 통신 로그 기록 필요. (문서8)
- 키오스크·홈페이지의 매표·회원이용·매출 정보 완전 연동 및 중앙서버 방식 지원. (문서8)
- 매출(회계)관리: 당일·당월 매출관리, 직원별 마감·담당자별 매출현황 확인, 발주기관 요구 통계양식 반영 및 대사(검증)정보 제공. (문서3)
