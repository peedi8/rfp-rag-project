# L47 Claim-Preservation Gate Report

Created: 2026-07-07

## Purpose

L47 adds a no-API diagnostic gate for the exposed qv6_007 metamorphic failure. The gate is not a new generalization score and does not improve EDD directly. It checks whether source-supported claims from the canonical Goyang facility question survive in the order-permuted variant answer.

## Inputs

- expectation file: `eval\claim_preservation_expectations.json`
- checker: `scripts\check_claim_preservation.py`
- Worker A proposal: `worker_outputs\l47_claim_gate_schema.contract.json`
- Worker B red review: `worker_outputs\l47_claim_gate_red.contract.json`
- chart: `analysis\l47_claim_preservation_rates.svg`

## Accepted Red-Team Corrections

- Source evidence is scoped to CSV rows that match the target organization and required project terms, not the whole `data_list.csv`.
- False-friend access-control language, such as account permissions or network access control, is flagged separately from physical entry/exit access-control systems.
- Underanswer polarity beats marker presence: an answer can mention the claim label and still fail if it says the source does not confirm it.
- Exit code `1` from the checker is expected when `gate_status=fail`; that is a diagnostic failure, not an infrastructure failure.

## Results

| loop | case | claims passed | claims failed | preservation rate | status | interpretation |
|---|---|---:|---:|---:|---|---|
| L37 | first v6 run | 0 | 2 | 0.0 | fail | missed both unmanned-operation and physical access-control claims |
| L40 | Goyang alias retry | 1 | 1 | 0.5 | fail | recovered unmanned-operation/HW linkage but still underanswered physical access-control |
| L44 | judge-included one-case smoke | 1 | 1 | 0.5 | fail | judge gave 5/5, but claim gate still catches the physical access-control miss |

## Decision

Keep L47 as `diagnostic_only_exposed_case`. Broad paid v7/v8/v9 runs remain closed until the qv6_007 answer-generation/evidence-use path can pass this gate or the report explicitly labels the remaining failure.

## Insight

The useful improvement here is measurement sharpness, not a higher EDD number. L44 proves that ordinary groundedness/relevance can be satisfied while a metamorphic claim is still lost. Claim preservation must sit beside EDD before spending more budget on larger scored loops.
