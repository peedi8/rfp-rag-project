# L29 Abstention Recompute Note

- input run: L28 `prompt_concise_verified`
- raw EDD before recompute: 86.42
- recomputed EDD after detector correction: 96.42
- changed metric: abstention accuracy 0.0 -> 1.0
- unchanged metrics: coverage 1.0, hit-all 1.0, MRR 1.0, groundedness 5.0, relevance 5.0, latency 23.754s

## Cause

The saved L28 answer correctly refused unavailable procurement-result fields with the phrase `문서상 확인 불가`, but `scripts.evaluate.is_abstention` did not count that phrase when the question asked for final builder/vendor, actual contract amount, and personal contact information.

## Fix

The detector now treats repeated `문서상 확인 불가` or `확인 불가` as abstention only when multiple procurement-result markers are present, including `최종 구축업체`, `낙찰자`, `계약금액`, `개인 연락처`, and `담당자`.

## Decision

This is a measurement correction, not a new answer improvement. Even after correction, L28 remains below L25 because latency is worse.
