# L5 Short Alias False Positive Stress

- no answer generation or judge call: true
- purpose: verify that L4 short municipality aliases do not over-match universities, stations, or rivers

## false_positive_expected_none
- anyang_university: `안양대학교 학사관리 시스템 고도화 요구사항` -> `null`
- pyeongtaek_university: `평택대학교 학사행정 시스템 구축 요구` -> `null`
- bonghwasan_station: `봉화산역 교통 안내 시스템 요구` -> `null`
- anyangcheon_water: `안양천 수질관리 플랫폼 구축 요구` -> `null`

## valid_expected_filter
- valid_anyang_facility: `안양 호계체육관 예약결제 요구` -> `{"발주 기관": "경기도 안양시"}`
- valid_pyeongtaek_bis: `평택 버스정보시스템 정류장 안내기 요구` -> `{"발주 기관": "경기도 평택시"}`
- valid_bonghwa_smartfarm: `봉화 스마트팜 작물관리 장비연계 요구` -> `{"발주 기관": "경상북도 봉화군"}`
- valid_jeongeup_center: `정읍체육트레이닝센터 통합예약 결제 PG 연동 요구` -> `{"발주 기관": "전북특별자치도 정읍시"}`
