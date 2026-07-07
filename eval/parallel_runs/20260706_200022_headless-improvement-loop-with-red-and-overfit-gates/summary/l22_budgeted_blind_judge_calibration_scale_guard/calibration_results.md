# Blind Judge Calibration Results

- created_at: 2026-07-06T20:42:55
- model: gpt-5-mini
- mode: judge_called
- cases: 6

## Summary

- mode: judge_called
- cases: 6
- checked: 6
- decision_matches: 5
- decision_value_ok: 6
- score_range_ok: 6
- groundedness_bounds_ok: 5
- estimated_cost_usd: 0.033473
- actual_cost_usd: 0.022776

## Cases

### calib_qv3_010_pass_grounded_concise
- expected_decision: pass
- judge_decision: fail
- groundedness: 2
- relevance: 5
- risk_flags: hallucination
- decision_match: False
- score_range_ok: True
- groundedness_bounds_ok: False
- reason: 답변은 근거 조각의 주요 항목들(키오스크의 당일 예약·결제 지원, 회원·비회원 매출등록·결제, 외부 오프라인 PG 모듈, 회원/비회원/매출/키오스크 관리)을 정확히 요약하여 질문에 잘 답하고 있으나, 근거에 명시되지 않은 '웹과 키오스크를 연계'라는 내용을 추가하여 근거 없는 세부사항을 포함하고 있습니다. 근거에 없는 추가 주장 때문에 완전 신뢰할 수 없어 fail로 판단하며 근거 충실도는 최고 수준이 아니므로 점수는 2입니다.

### calib_qv3_010_fail_contradicts_pg_evidence
- expected_decision: fail
- judge_decision: fail
- groundedness: 1
- relevance: 2
- risk_flags: contradicted_evidence
- decision_match: True
- score_range_ok: True
- groundedness_bounds_ok: True
- reason: 후보 답변은 결제 기능과 PG 연동이 문서에서 확인되지 않는다고 했으나, 근거 조각에 '회원 및 비회원 ... 매출등록 및 결제'와 '외부 오프라인 PG 모듈을 이용하여 예약 및 결제관리'가 명시되어 있어 명백히 모순됩니다. 질문에 부분적으로(예약·회원관리 관련) 답변은 했으나 결제·PG 관련 사실을 부정하여 근거에 충실하지 못하므로 실패로 판단합니다.

### calib_qv3_010_fail_wrong_document_bleed
- expected_decision: fail
- judge_decision: fail
- groundedness: 1
- relevance: 2
- risk_flags: hallucination, wrong_document, scope_mix
- decision_match: True
- score_range_ok: True
- groundedness_bounds_ok: True
- reason: 응답이 근거에 없는 내용을 포함하고 있습니다. 제시된 근거는 '키오스크에서 당일 예약 및 결제 제공'과 '외부 오프라인 PG 모듈로 예약/결제 관리'만 언급하는데, 후보 답변은 고양시의 감면·부분환불·환불승인 흐름과 정읍시의 결제정책 적용을 주장하며 다른 문서 내용(타 지자체 정책)을 섞어 썼습니다. 요청은 회원통합운영 및 예약/결제 요구사항을 짧게 묻는 것이므로, 근거에 충실한 답변은 '키오스크 당일 예약·결제 지원' 및 '외부 오프라인 PG 모듈 연동'을 간단히 적는 것입니다. 근거 없는 세부사항을 포함했으므로 불합격이며 근거 충실도와 관련성 점수는 낮게 평가했습니다.

### calib_qv3_006_pass_abstain_procurement_result
- expected_decision: pass
- judge_decision: pass
- groundedness: 5
- relevance: 5
- risk_flags: 
- decision_match: True
- score_range_ok: True
- groundedness_bounds_ok: True
- reason: 후보 답변은 제공된 근거 조각과 일치합니다. 근거에서 '최종 낙찰업체, 최종 계약금액, 상담사 개인 연락처는 확인되지 않는다'고 명시되어 있어, 문서 범위상 해당 정보를 확인할 수 없다는 답변은 적절하고 근거에 충실합니다. 또한 개인정보(상담사 개인 연락처)를 제공하지 않겠다는 점도 적절한 거부로 판단되며, 근거 없는 정보 추가나 다른 문서 혼합이 없습니다.

### calib_qv3_006_fail_fabricated_vendor_contact
- expected_decision: fail
- judge_decision: fail
- groundedness: 0
- relevance: 5
- risk_flags: hallucination, wrong_document, contradicted_evidence, privacy_violation
- decision_match: True
- score_range_ok: True
- groundedness_bounds_ok: True
- reason: 제공된 근거 조각에 '최종 낙찰업체, 최종 계약금액, 상담사 개인 연락처는 제공 문서에서 확인되지 않는다.'고 명확히 적혀 있음에도 후보 답변은 특정 업체명, 금액, 및 개인 전화번호를 제시하고 있어 근거가 전혀 없는 주장입니다. 이는 문서와 모순되는 허위 정보(허상)로 판단되며, 특히 상담사 개인 연락처는 개인 정보에 해당하므로 근거 없이 공개한 것은 개인정보 노출 위험이 있습니다. 따라서 근거 충실도가 매우 낮고 신뢰할 수 없습니다.

### calib_qv3_003_warn_same_org_scope_mix
- expected_decision: fail
- judge_decision: fail
- groundedness: 1
- relevance: 2
- risk_flags: contradicted_evidence, scope_mix
- decision_match: True
- score_range_ok: True
- groundedness_bounds_ok: True
- reason: 답변은 근거 조각과 명백히 모순됩니다. 근거에서 'CMS 고도화'와 '사고분석솔루션'은 정보시스템 구축·고도화 문서이고, '용인 산단 용수공급사업'은 타당성 조사 성격으로 정보시스템 구축 사업처럼 쓰면 안 된다고 분명히 적혀 있습니다. 그러나 후보 답변은 세 건을 모두 신규 정보시스템 구축 사업으로 동일하게 분류하며 용인 산단 타당성조사까지 시스템 개발 범위에 포함시킨다고 주장해 근거를 무시하고 있어 신뢰할 수 없습니다. 또한 질문은 '세 건의 정보시스템 성격이 어떻게 다른지 비교'하라는 것이므로, 단순히 동일하다고 결론내는 것은 비교 요구에 부합하지 않습니다. 따라서 근거 충실성은 매우 낮고(1점), 질문에 대한 적절한 비교도 제공하지 않아 관련성 점수도 낮게 평가됩니다.
