# Prompt Format Review

## Scope

Proposal-only review for the RFP RAG answer format. No external API/model calls were made. Source files were read only; no `src` files were edited.

Allowed inputs reviewed:

- `src/generator.py`
- `src/rag.py`
- `eval/parallel_runs/20260706_193521_Representative-answer-quality-review-matrix-for-RFP-RAG-repo/summary/answer_quality_review_matrix.json`
- `eval/parallel_runs/20260706_193521_Representative-answer-quality-review-matrix-for-RFP-RAG-repo/summary/answer_quality_review_matrix.md`
- `eval/next_improvement_tasks.md`

## Recommendation

Add a new prompt variant named `compact_evidence_brief`.

The current prompt set already has a concise/evidence-oriented variant, but the review matrix shows a more specific failure mode: A/B/C are high-groundedness, high-relevance answers that become too long, too list-like, or too report-unfriendly. The fix should therefore be an answer-shape contract, not a relaxation of evidence rules.

The proposed variant should:

- keep source-only answering,
- keep per-claim document citations,
- keep explicit abstention for missing details,
- reduce normal answers to a short decision-ready brief,
- prevent same-agency or same-client source bleed in comparisons.

## Proposed Prompt Contract

Suggested Korean system-prompt content, to be adapted after confirming repository encoding:

```text
당신은 공공입찰 제안요청서(RFP) 분석 전문 어시스턴트입니다.
아래 규칙을 반드시 지키세요.

1. 제공된 참고 문서에서 직접 확인되는 내용만 답합니다.
2. 질문이 묻는 범위에만 답하고, 문서에 있는 주변 기능을 장황하게 나열하지 않습니다.
3. 일반 답변은 먼저 1문장으로 결론을 말한 뒤 최대 5개 bullet로 요약합니다.
4. 여러 사업/항목 비교처럼 질문 자체가 넓은 경우에만 최대 7개 bullet까지 허용합니다.
5. 각 bullet은 하나의 핵심 주장만 담고, 끝에 근거 문서 번호를 붙입니다. 예: (문서1), (문서1, 문서3)
6. 같은 발주기관의 여러 사업을 비교할 때는 bullet 안에 사업/문서 범위를 먼저 밝히고, 다른 사업의 근거를 섞지 않습니다.
7. 요청한 세부정보가 참고 문서에서 직접 확인되지 않으면 "확인 불가: 제공된 문서에서 직접 확인되지 않습니다"라고 답하고 추정하지 않습니다.
8. 낙찰업체, 계약금액, 개인 연락처, 전화번호, 미공개 조달정보는 문서에 정확히 있을 때만 말합니다. 없으면 반드시 확인 불가로 처리합니다.
9. 일반적인 RFP 조언, 구현 제안, 배경 설명은 사용자가 명시적으로 요청하지 않으면 추가하지 않습니다.
10. 단일 사업 답변은 대략 700자 이내, 다중 비교 답변은 대략 1000자 이내로 유지합니다.
```

## Why This Variant

A/B/C share the same pattern: evidence is mostly valid, but the answer is too verbose for a proposal workflow. The review matrix repeatedly points to long feature inventories, repeated category expansions, and answer text that a human would need to summarize again.

The variant should not punish useful citations. Instead, it should reduce the number of claims and make each cited claim more purposeful.

## Case-Specific Fit

`A_long_high_score_biff`

The answer should preserve the BIFF/ACFM support-function evidence, but avoid a long feature inventory. A 1-sentence direct answer plus 3-5 grouped bullets should be enough.

`B_high_latency_mozambique`

The answer should group traffic center, field equipment, and training/operation support. It should avoid repeating the question's category structure as a long list.

`C_same_org_scope_kwater`

The answer needs compact comparison plus strict scope labeling. Each bullet should identify which K-water project/document the claim belongs to before making the comparison.

`D_abstain_procurement_contact` and `H_planted_fabricated_vendor_contact`

The compact format must not make unsafe answers easier. Short fabricated answers are still failures. The variant must preserve hard abstention for final vendor, contract amount, private contact, phone number, and unpublished procurement details.

`E/F/G_top5_top8_anyang`

Prompt formatting cannot solve missing retrieval evidence. The key safety rule is to avoid global absence claims when the provided context may be incomplete. If payment/PG evidence is not in context, say it is not confirmed in the provided documents.

## Acceptance Checks

- Normal answers contain no more than 5 bullets.
- Explicit multi-project/multi-dimension comparisons contain no more than 7 bullets.
- Every substantive bullet ends with document citation(s).
- No bullet contains multiple unrelated claims.
- Missing facts are marked as 확인 불가 rather than inferred.
- Same-agency comparisons identify project/document scope before the claim.
- No generic RFP advice or implementation recommendations appear unless requested.
- A/B/C become shorter and more report-ready without losing citation discipline.
- D/H safety behavior is preserved.
- E/F/G absence wording stays context-limited rather than absolute.

## Risks

- A hard cap can under-answer broad comparison questions; the 7-bullet exception is needed.
- Character limits should begin as qualitative prompt guidance, not strict runtime truncation.
- Over-compression can create multi-claim bullets; the one-main-claim rule is important.
- This proposal does not replace adaptive retrieval/top_k work.
- The source files displayed with mojibake in this environment, so implementation should confirm the intended file encoding before inserting Korean prompt text.
