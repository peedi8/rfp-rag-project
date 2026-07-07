# Worker B Guard False-Positive Fixture Proposals

- Contract: `guard_false_positive.contract.json`
- Proposed fixtures: `20`
- Sensitive preempt positives: `4`
- Sensitive preempt false-positive boundaries: `8`
- Plain-language hint positives: `4`
- Plain-language hint negatives: `4`

The proposals are no-API cases intended for direct calls to:

- `src.generator._preempt_sensitive_abstention_answer`
- `src.generator._apply_query_prompt_hint`

Main risks covered:

- Adversarial unsupported final award, contract amount, patient data, and personal contact requests should preempt.
- Normal procurement terms such as `추정금액`, `추정가격`, `사업예산`, and official contact extraction should not preempt.
- User instructions like `문서에 없으면 말하지 마`, `추정하지 말고`, and partial-answer requests should not become full abstentions.
- Plain-language hint should trigger for `쉽게 말`, `비전문가`, `잘 모르겠`, and `간단히 말`, while negations such as `쉽게 말하지`, `요약하지`, and `짧게 말하지` should suppress it.
