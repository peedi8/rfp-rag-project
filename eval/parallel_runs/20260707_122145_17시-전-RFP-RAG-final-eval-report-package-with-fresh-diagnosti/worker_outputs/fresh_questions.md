# Worker A Fresh/Semi-Fresh Question Proposal

- Contract: `fresh_questions.contract.json`
- Count: 12 proposed cases
- Model calls: none
- Write scope: this `worker_outputs` folder only

## Labeling Caveat

The exposure registry says prior v2-v7 files are already exposed, spent holdout, source-exposed, or diagnostic. This set should be reported as semi-fresh plus diagnostic candidates, not strict held-out validation, unless the orchestrator freezes it before any answers are inspected and confirms project exposure.

## Proposed Coverage

| id | label | focus |
|---|---|---|
| q20260707_a01_generic_integrated_system_preempt_false_positive | diagnostic | preempt false positive on generic title fragment |
| q20260707_a02_hanyoung_plain_language_track_system | semi-fresh | plain-language hint |
| q20260707_a03_kogas_erp_final_contract_vs_budget | semi-fresh | final contract vs estimated amount |
| q20260707_a04_kesco_official_vs_personal_contact | semi-fresh | official vs personal contact |
| q20260707_a05_nmc_patient_example_fabrication | source-exposed | patient/example fabrication |
| q20260707_a06_gist_same_issuer_rcms_vs_academic | semi-fresh | same issuer project mixing |
| q20260707_a07_livestock_honey_vs_traceability_compare | source-exposed | comparison and domain contamination |
| q20260707_a08_hanyoung_numeric_precision | semi-fresh | numeric precision |
| q20260707_a09_kaeri_dose_ai_overclaim | semi-fresh | adversarial buzzword overclaim |
| q20260707_a10_kitech_procurement_vs_gas_safety | source-exposed | same issuer comparison regression |
| q20260707_a11_dbrain_award_score_and_vendor | source-exposed | unsupported award score/vendor |
| q20260707_a12_seoul_digital_sex_crime_sensitive_story | semi-fresh | sensitive case fabrication |

## Freeze Recommendation

Use 10-12 cases if time is tight. The strongest compact 10 are a01, a02, a03, a04, a05, a06, a08, a09, a11, and a12. Add a07/a10 when the report needs comparison and same-issuer regression continuity.
