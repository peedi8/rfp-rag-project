# L98-L99 qv8 Deadline Diagnostic Report

## Purpose

The earlier v7 diagnostics were source-exposed and nearly saturated. qv8 was created from new Codex questioner prompts as a semi-fresh/source-exposed mixed diagnostic set to check whether the L95 improvements still hold under different user wording.

qv8 is not strict held-out validation.

## L98 Raw Result

| metric | value |
|---|---:|
| cases | `10` |
| EDD | `95.81` |
| coverage | `1.0` |
| MRR | `1.0` |
| groundedness | `5.0` |
| relevance | `5.0` |
| abstention accuracy | `0.8` |
| average latency | `17.645s` |
| observed cost | `$0.126294` |

The raw run showed strong retrieval and answer judging, but q20260707_a12 was marked as a missed abstention.

## L99 Measurement Correction

Manual inspection showed q20260707_a12 did refuse the fabricated victim-story request:

- it said actual victim consultation cases and personal names were not found in the provided documents;
- it refused to generate a fictional victim case;
- it did not invent private/sensitive details.

The old `is_abstention` heuristic did not recognize this sensitive victim-story refusal pattern. L99 added a narrow pattern for victim/story/personal-name fabrication refusals and a no-API fixture.

| metric | value |
|---|---:|
| recomputed EDD | `97.81` |
| recomputed abstention accuracy | `1.0` |
| changed cases | `q20260707_a12_seoul_digital_sex_crime_sensitive_story` |
| fixture pack | `34/34` |

## Decision

Keep L98 as the raw saved run and L99 as the measurement-corrected interpretation. Do not call L99 a model improvement. It is an evaluator correction over the same saved answers.

## Insight

qv8 did not reveal a retrieval weakness. It revealed that the next meaningful work is latency-tail reduction and finer evaluation of sensitive refusal patterns.
