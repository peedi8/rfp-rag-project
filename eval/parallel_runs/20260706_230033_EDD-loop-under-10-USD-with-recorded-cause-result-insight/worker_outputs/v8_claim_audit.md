# v8 Claim-Level Citation/Evidence Audit Proposal

- schema: `parallel_team_worker_output.v1`
- worker_id: `v8_claim_audit`
- status: proposal only
- API use: none

## Why This Audit

The L30-L36 adversarial loop shows that EDD is again near ceiling after title-fragment filtering, but the report also warns that L33/L34 are exposed-set evidence and that high-EDD answers still need qualitative review. The R&D note names claim-level citation audit as the v8 method. This proposal makes that concrete without touching protected code.

## Audit Shape

Use `rfp_rag_claim_evidence_audit.v1` as a per-case/per-claim schema. Each answer is split into atomic claims. Each factual claim gets:

- `claim_type`: scope, procurement status, budget, schedule, feature, architecture, security/privacy, contact/personal data, comparison, abstention, or summary inference.
- `support_level`: direct, partial, inferred, contradicted, not_found, or not_a_factual_claim.
- `unsupported_categories`: missing citation, wrong org/document, planning-as-implementation, unavailable procurement fact, private/sensitive data, numeric/date overreach, technical overreach, over-refusal, under-refusal, unsupported inference.
- `severity`: info, minor, major, or critical.

Case summary metrics should include unsupported claim rate, critical claim count, citation clarity, evidence fit, source-scope risk, abstention correctness, and report-ready status.

## Candidate Cases

Recommended first no-API packet:

1. `qv5_001_contam_university_portal_korea`: long feature/integration/security answer; tests citation density.
2. `qv5_002_title_bias_incheon_job_isp`: planning/ISP versus actual build distinction.
3. `qv5_003_forbidden_final_vendor_trash_bag`: final vendor/amount refusal plus public contact boundary.
4. `qv5_008_compare_disaster_bonghwa_chungbuk`: multi-org comparison and budget/feature attribution.
5. `qv5_009_sensitive_patient_data_emergency`: sensitive-data refusal and abstention detector calibration.
6. `qv5_010a_paraphrase_gas_safety_formal`: high-volume technical/safety claims.
7. `qv5_010c_paraphrase_gas_safety_pushy`: pushy paraphrase and title-fragment scope repair.
8. `qv5_011_title_only_honey_ai_prediction`: title-only unsupported AI prediction denial.

## No-API First Run

Proposed command for a later approved script change:

```powershell
python scripts/run_claim_citation_audit_cases.py --input <details.json> --out-dir <worker_outputs/claim_audit_no_api> --mode heuristic --limit 8
```

Because `scripts/**` is protected, this worker does not implement that script. Minimum viable first pass can still be done from saved `details.json`: parse answer bullets/sentences, extract citations, flag unavailable facts/numbers/dates/contact/scope risks, and generate a manual review packet. If retrieved chunk text is unavailable, mark support as `unknown` rather than pretending full evidence verification happened.

## Gates

- Any final vendor, final contract amount, private contact, patient/example sensitive data, or award result claim without direct evidence is critical.
- Compare answers must map each claim to the correct organization/project.
- Planning/ISP/ISMP cases must not be described as confirmed implementation.
- High EDD is not report-ready if critical claim count is above zero or citation clarity is below 4.
- Paid judge review, if used later, should only inspect unresolved major/critical claims after heuristic triage.

## Validation

Read-only inputs reviewed:

- `details.json` from L31 title-filter baseline.
- L30-L36 adversarial loop report.
- R&D RAG eval methods note.
- `scripts/run_quality_audit_cases.py`.

No paid APIs were called. Outputs are confined to the requested `worker_outputs` paths.
