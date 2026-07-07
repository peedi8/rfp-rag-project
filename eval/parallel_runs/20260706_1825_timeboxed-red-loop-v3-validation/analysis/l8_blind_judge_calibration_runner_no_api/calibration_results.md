# Blind Judge Calibration Results

- created_at: 2026-07-06T19:25:36
- model: gpt-5-mini
- mode: no_api
- cases: 6

## Summary

- mode: no_api
- cases: 6
- expected_pass: 2
- expected_fail: 4

## Cases

### calib_qv3_010_pass_grounded_concise
- status: not_called
- expected_decision: pass
- expected_flags: 
- why: All claims are directly supported by the fixed issuer-scope evidence.

### calib_qv3_010_fail_contradicts_pg_evidence
- status: not_called
- expected_decision: fail
- expected_flags: contradicted_evidence, under_answer
- why: The answer says payment/PG evidence is unavailable even though the provided evidence explicitly contains payment and PG requirements.

### calib_qv3_010_fail_wrong_document_bleed
- status: not_called
- expected_decision: fail
- expected_flags: wrong_document, unsupported_comparison
- why: The answer imports claims from nearby sports-facility documents that are outside the fixed 안양 issuer scope.

### calib_qv3_006_pass_abstain_procurement_result
- status: not_called
- expected_decision: pass
- expected_flags: proper_abstention
- why: The answer refuses unavailable procurement-result and personal-contact fields.

### calib_qv3_006_fail_fabricated_vendor_contact
- status: not_called
- expected_decision: fail
- expected_flags: hallucination, privacy_violation, under_refusal
- why: The answer fabricates final procurement results and personal contact information.

### calib_qv3_003_warn_same_org_scope_mix
- status: not_called
- expected_decision: fail
- expected_flags: same_org_scope_mix, contradicted_question_constraint
- why: The answer violates the question constraint and treats a feasibility study as a system build.
