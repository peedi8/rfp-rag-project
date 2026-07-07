# L88-L90 Plain-Language Format Probe Report

## Purpose

L87 found that qv7_009 was grounded but over-structured for a plain-language request. L88-L90 tested whether the answer could be shortened without losing evidence quality.

## Runs

| loop | candidate | chars | lines | bullets | judge | latency | issue | decision |
|---|---|---:|---:|---:|---|---:|---|---|
| L88 | default | `1228` | `47` | `29` | `5/5` | `18.8s` | `plain_language_answer_over_structured` | reject |
| L88 | report_ready | `644` | `8` | `5` | `5/5` | `50.94s` | none | reject as broad setting due latency |
| L89 | query-specific plain-language hint | `605` | `9` | `5` | `5/5` | `16.7s` | none | candidate only |

## Measurement Correction

The first L89 interpretation marked the answer as a false abstention because the final sentence said that final vendor/contract result was not available in the documents. That was a measurement error: the answer had already provided substantive, grounded bullets.

L90 corrected `is_abstention` for substantive plain-language answers with a final unsupported-result caveat. Fixtures pass `23/23`.

## Decision

- Keep the query-specific hint as a candidate improvement.
- Do not claim generalization because this is one source-exposed qv7_009 probe.
- Reject `report_ready` as a broad setting despite clean format, because latency was much worse.
- Next useful check: rerun the full v7 source-exposed diagnostic under the hint to look for regressions in compare, sensitive refusal, and ambiguity cases.
