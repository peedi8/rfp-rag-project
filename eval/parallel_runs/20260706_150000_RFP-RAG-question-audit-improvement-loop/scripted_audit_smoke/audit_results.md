# Scripted Quality Audit Results

- created_at: 2026-07-06T15:50:16
- model: gpt-5-mini
- input: `I:\0706\rfp-rag-project\eval\parallel_runs\20260706_150000_RFP-RAG-question-audit-improvement-loop\audits\audit_input_top8.json`
- cases_requested: 1
- cases_completed: 1

## Summary

- pass: 0
- pass_with_caveat: 1
- fail: 0
- unknown: 0
- most_common_risks: ['coverage_below_target', 'context_mismatch']

## Cases

### filter_off_rewrite_on::q1_single_extract

- decision: pass_with_caveat
- contextual_quality: 4
- evidence_fit: 5
- usefulness: 4
- conciseness: 5
- risk_flags: coverage_below_target, context_mismatch
- recommended_next_action: revise_retrieval
- reason: 제출된 검색 결과와 첨부 문서 목록(수협중앙회, 서민금융진흥원 등)에 '국민연금공단'이나 해당 이러닝 사업의 RFP/요구사항 문서가 전혀 포함되어 있지 않음이 명확하므로, 요청한 요구사항을 추출할 근거가 없어 추출을 거부한 응답은 문맥상 적절함. 다만 사용자에게 단순히 문서를 제출해 달라고만 요청하고, 대안(예: 공개 RFP 검색, 예상되는 요구사항 항목 템플릿 제시 등)을 제안하지 않아 실무적 도움 면에서 개선여지가 있음. 또한 자동 플래그(coverage=0.0, abstention=True)에 맞게 '근거 없음'을 명확히 했으나, 검색/재조회 권고 또는 최소한의 일반적 요구사항 예시를 제시하면 유용성이 더 높아졌을 것임.
