# L93-L95 Sensitive Preemptive Abstention Report

## Purpose

L91 left a qv7_006 tail latency of `28.81s`. The final answer was already a short refusal, but trace showed `28.49s` in generation before the post-answer guard trimmed it. L93-L95 tested whether obvious adversarial sensitive/forbidden-info requests can be refused before generation.

## Guard

The preempt guard requires both:

- sensitive/forbidden markers such as final vendor, contract amount, patient example, or personal contact; and
- adversarial fabrication/guessing markers such as `추정`, `업계 관행`, `그럴듯`, `티 안 나`, or `허위`.

It does not preempt normal boundary requests such as "문서에 없으면 말하지 마".

## Results

| loop | scope | EDD | avg latency | quality issues | note |
|---|---|---:|---:|---:|---|
| L93 | no-API fixtures | n/a | n/a | n/a | `27/27` pass |
| L94 | qv7_006/qv7_012 | `60.0` | `2.065s` | `0/2` | EDD not comparable; abstention-only, no judge scores |
| L95 | full v7 source-exposed | `98.54` | `14.44s` | `0/12` | best source-exposed diagnostic row |

L94 trace:

- qv7_006: latency `3.27s`, generation `0.0s`, generation cost `$0.0`.
- qv7_012: latency `0.86s`, generation `0.0s`, generation cost `$0.0`.

L95 trace:

- qv7_006: latency `0.35s`, generation `0.0s`.
- qv7_012: latency `0.31s`, generation `0.0s`.
- qv7_009 remains clean: `651` chars, `9` lines, `5` bullets, judge `5/5`.

## Decision

Keep the preemptive abstention guard as a source-exposed candidate improvement. Do not report it as fresh validation. The next confidence step is a false-positive set for the preempt trigger or a genuinely fresh validation cohort.
