# L4 Admin Alias Filter Diagnostic

- no answer generation or judge call: true
- purpose: verify short administrative aliases after the L4 source-scope guard patch

- qv3_010_anyang_from_set: `안양 호계체육관 배드민턴/탁구 예약시스템, 회원통합운영이랑 예약/결제 쪽 요구 뭐야? 좀 짧게.` -> `{"발주 기관": "경기도 안양시"}`
- pyeongtaek_short: `평택 버스정보시스템 정류장 안내기랑 센터 통신 요구만 알려줘` -> `{"발주 기관": "경기도 평택시"}`
- bonghwa_short: `봉화 스마트팜 사업에서 작물관리랑 장비연계 요구 정리해줘` -> `{"발주 기관": "경상북도 봉화군"}`
- jeongeup_short: `정읍체육트레이닝센터 통합예약 결제 PG 연동 요구 말해줘` -> `{"발주 기관": "전북특별자치도 정읍시"}`
