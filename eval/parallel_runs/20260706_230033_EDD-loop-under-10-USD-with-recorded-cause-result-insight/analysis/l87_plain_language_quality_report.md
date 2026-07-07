# L87 Plain-Language Quality Report

## Purpose

L87 checks whether high-scoring answers can still fail the user's requested answer style. The trigger case is qv7_009, where the user asked for a plain-language explanation but the system returned long RFP-style bullet lists.

## Change

- Added `plain_language_answer_over_structured` to `scripts/evaluate.py`.
- Expanded no-API fixtures to `22/22`.
- Recomputed saved worker outputs without new paid calls.

## Finding

| row | chars | lines | bullet/list lines | judge groundedness/relevance | issue |
|---|---:|---:|---:|---|---|
| L81 baseline | `1142` | `25` | `20` | `5/5` | `plain_language_answer_over_structured` |
| L85 topk5 | `1160` | `29` | `15` | `5/5` | `plain_language_answer_over_structured` |
| L85 topk8 control | `1294` | `42` | `16` | `5/5` | `plain_language_answer_over_structured` |
| L85 topk12 | `1448` | `29` | `11` | `5/5` | `plain_language_answer_over_structured` |

## Interpretation

This is not an EDD improvement. It is a measurement improvement.

The judge was not wrong that the answers were grounded. The missing dimension was whether the answer matched the user's requested level and format. Plain-language requests should not be answered as exhaustive RFP requirement inventories unless the user asks for that level of detail.

## Decision

- Keep the measurement gate.
- Do not promote or reject any retrieval setting based on this alone.
- Use qv7_009 in the report as a second example, alongside qv7_006, showing why high automatic metrics do not fully prove answer quality.
- If repaired, use a one-case format probe first and reject it if groundedness, relevance, abstention, or ambiguity handling regresses.
