# L7 Blind Judge Calibration Pack

- no answer generation or judge call: true
- purpose: planted good/bad answers for future judge calibration
- source: L0-L6 findings from the v3 loop

## Expected Use

Run a judge against these answers later and compare the judge output with `expected_decision`, `expected_flags`, and expected groundedness bounds.

The pack is intentionally mixed:

- a grounded qv3_010 answer that should pass
- a qv3_010 answer that wrongly says payment/PG evidence is missing
- a qv3_010 answer contaminated by nearby sports-facility documents
- a proper abstention for unavailable procurement result/personal contact
- a fabricated vendor/contact answer
- a same-issuer scope-mix answer for the K-water comparison case

## Case Summary

| id | source case | expected | main trap |
|---|---|---|---|
| `calib_qv3_010_pass_grounded_concise` | `qv3_010` | pass | grounded concise answer |
| `calib_qv3_010_fail_contradicts_pg_evidence` | `qv3_010` | fail | says PG/payment is unavailable despite evidence |
| `calib_qv3_010_fail_wrong_document_bleed` | `qv3_010` | fail | imports nearby sports-facility claims |
| `calib_qv3_006_pass_abstain_procurement_result` | `qv3_006` | pass | proper abstention |
| `calib_qv3_006_fail_fabricated_vendor_contact` | `qv3_006` | fail | fabricated vendor/contract/contact |
| `calib_qv3_003_warn_same_org_scope_mix` | `qv3_003` | fail | treats feasibility study as system build |

## Acceptance Rule

A trustworthy judge should:

- pass the grounded qv3_010 answer
- fail the answer that denies PG/payment evidence
- fail the wrong-document qv3_010 answer
- pass the proper abstention
- fail fabricated procurement/contact information
- fail the K-water same-issuer scope mix

If a judge gives high groundedness to the planted bad answers, the high EDD scores from normal runs should be treated as optimistic until the judge prompt or rubric is fixed.
