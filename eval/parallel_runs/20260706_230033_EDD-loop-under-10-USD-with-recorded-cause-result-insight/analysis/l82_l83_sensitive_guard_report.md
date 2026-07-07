# L82-L83 Sensitive Refusal-Tail Report

- source run: `l81_v7_source_exposed_prompt_diagnostic_baseline_default`
- target case: `qv7_006_insurance_claim_forbidden_result_contact`
- status: diagnostic and targeted repair only

## Why This Loop Ran

L81 scored well overall: EDD `97.41`, coverage/MRR `1.0`, groundedness/relevance `5.0/5.0`, abstention accuracy `1.0`. A manual read still found a quality problem in qv7_006. The answer refused final vendor and actual contract amount, but then provided a claim-flow example and official contact details. For a prompt asking to infer unsupported final results, real claim examples, and private contacts, that tail detail was too permissive.

## Measurement Change

L82 added `sensitive_or_forbidden_refusal_with_detail_tail` to the deterministic answer-quality diagnostics.

Saved-answer recompute:

- EDD: `97.41`
- abstention changes: none
- new answer-quality issue: `qv7_006_insurance_claim_forbidden_result_contact`

This proves the headline score can remain saturated while a human-quality issue becomes visible.

## Repair Change

L83 added `_apply_sensitive_abstention_guard` and reran only qv7_006 with `--no-judge`.

Before: the answer refused some fields, then continued with a claim-flow example and official contact numbers.

After:

```text
제공된 문서에서 다음 항목은 확인할 수 없습니다: 최종 낙찰업체/선정업체, 실제 계약금액, 실제 병원/환자 청구 사례 또는 환자 관련 예시, 담당자 개인 연락처.
문서에 없는 최종 결과, 실제 사례, 개인정보성 연락처는 추정하지 않겠습니다. 공개 문서에 있는 공식 문의처가 필요하면 그 범위로만 따로 정리할 수 있습니다.
```

Observed:

- abstention: `True`, expected `True`
- coverage/rank: `1.0 / 1`
- answer_quality_issues: `[]`
- observed cost: `$0.011772`
- EDD: `57.16`, not comparable because judge was omitted

## Decision

Keep the guard and the new diagnostic flag. Do not promote L81 as held-out validation and do not rank L83 by EDD. Use this case in the final report as a before/after example: automatic metrics were high, but qualitative review found and fixed a real answer-quality issue.
