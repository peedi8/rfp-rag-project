# L119 Question Bank 64 Runnable Manifest

This is an execution-readiness manifest, not a full answer run.

## Score Policy
- ordinary_edd_rule: Only cases with ordinary_edd_included=true may be aggregated into an ordinary EDD subtotal.
- sidecar_rule: metadata_corpus_sidecar and system_trace_audit cases must be reported as separate gates/subtotals.
- contamination_rule: If a failure is inspected and then fixed, the same inspected set becomes contaminated and must be labeled as targeted-recheck, not fresh holdout.
- judge_rule: Judge changes must be labeled separately from system changes; compare strict vs balanced on a calibration subset before claiming improvement.
- keyword_sidecar_rule: Keyword discovery sidecars are candidate lists for preflight and recall prompts; exact scoring must use row-level metadata/body evidence review, not keyword match alone.
- selected_project_seed_rule: Selected-project rows must bind to one explicit seed per run; cross-seed synthesis is contamination unless the question explicitly asks for comparison.
- trace_wrapper_rule: Q090-Q091 are blocked from execution until retrieval_trace and chunk_source_map export is wired.

## Counts
- total cases: 64
- ordinary EDD subtotal candidates: 49
- sidecar/trace-only cases: 15
- runnable_status blocked_until_trace_wrapper: 2
- runnable_status ready: 62
- concrete_single_document_rag: 3
- conversation_seeded_domain_expansion: 1
- conversation_seeded_followup_rag: 4
- conversation_seeded_numeric_comparison: 1
- corpus_discovery_rag_with_sidecar: 2
- metadata_corpus_sidecar: 13
- missing_metadata_abstention_boundary: 1
- multi_document_comparison_or_business_recommendation: 5
- near_duplicate_comparison: 1
- negative_requirement_check: 1
- persona_or_business_usefulness_seeded_rag: 8
- selected_project_seeded_contract_rag: 8
- selected_project_seeded_technical_rag: 8
- system_trace_audit: 2
- unsupported_claim_boundary: 5
- wrong_org_correction_boundary: 1

## Review Decisions
- Q001-Q012 and Q065 remain sidecar-only metadata/corpus rows; keyword lists are candidate preflight aids, not strict gold answers.
- Q033-Q035 remain physically in shard A but score under a quarantined comparison subtotal.
- Q038-Q045 must use one selected-project seed per run and must not blend evidence across seeds.
- Q046-Q050 must use a preferred seed/fallback policy and return not-found rather than padding sparse fields.
- Q090-Q091 are blocked until a retrieval-trace export wrapper exists.

## Shards
### A_metadata_corpus
- count: 16
- ordinary EDD subtotal candidates: 3
- sidecar/trace-only: 13
- blocked_until_trace_wrapper: 0
- modes: {"metadata_corpus_sidecar": 13, "multi_document_comparison_or_business_recommendation": 3}
- gates: {"G_METADATA_AGGREGATION": 13, "G_MULTI_DOC_COMPARISON": 3, "G_QUARANTINED_COMPARISON_SUBTOTAL": 3}
### B_contract_technical_extract
- count: 16
- ordinary EDD subtotal candidates: 16
- sidecar/trace-only: 0
- blocked_until_trace_wrapper: 0
- modes: {"concrete_single_document_rag": 3, "selected_project_seeded_contract_rag": 8, "selected_project_seeded_technical_rag": 5}
- gates: {"G_SINGLE_DOC_TARGET": 3, "G_SELECTED_PROJECT_MEMORY": 13, "G_CONTRACT_FIELDS": 8, "G_TECHNICAL_REQUIREMENT_FIELDS": 5}
### C_technical_followup_boundary
- count: 16
- ordinary EDD subtotal candidates: 16
- sidecar/trace-only: 0
- blocked_until_trace_wrapper: 0
- modes: {"selected_project_seeded_technical_rag": 3, "corpus_discovery_rag_with_sidecar": 2, "negative_requirement_check": 1, "near_duplicate_comparison": 1, "wrong_org_correction_boundary": 1, "conversation_seeded_followup_rag": 4, "conversation_seeded_numeric_comparison": 1, "conversation_seeded_domain_expansion": 1, "unsupported_claim_boundary": 1, "missing_metadata_abstention_boundary": 1}
- gates: {"G_SELECTED_PROJECT_MEMORY": 3, "G_TECHNICAL_REQUIREMENT_FIELDS": 3, "G_CORPUS_DISCOVERY": 2, "G_NEGATIVE_REQUIREMENT": 1, "G_DUPLICATE_TITLE_DISAMBIGUATION": 1, "G_ENTITY_CORRECTION": 1, "G_FOLLOWUP_CONTEXT_MEMORY": 4, "G_NUMERIC_COMPARISON": 1, "G_FOLLOWUP_DOMAIN_EXPANSION": 1, "G_UNSUPPORTED_CLAIM_BOUNDARY": 1, "G_NO_EXACT_BUDGET_GUESS": 1}
### D_persona_business_citation
- count: 16
- ordinary EDD subtotal candidates: 14
- sidecar/trace-only: 2
- blocked_until_trace_wrapper: 2
- modes: {"unsupported_claim_boundary": 4, "persona_or_business_usefulness_seeded_rag": 8, "system_trace_audit": 2, "multi_document_comparison_or_business_recommendation": 2}
- gates: {"G_UNSUPPORTED_CLAIM_BOUNDARY": 4, "G_CONTEXTUAL_USEFULNESS": 8, "G_TRACE_TRANSPARENCY": 2, "G_MULTI_DOC_COMPARISON": 2, "G_BUSINESS_RECOMMENDATION_CRITERIA": 2}

## Seed Catalog
- S_PORTAL_KOREA_UNIV: DOC008 | 고려대학교 | 차세대 포털·학사 정보시스템 구축사업 | amount=11270000000.0 | why=large PDF education/portal project; useful for procurement, evaluation, schedule, budget, and persona rewrite tests
- S_ADD_LARGE_TRANSFER: DOC010 | 국방과학연구소 | 대용량 자료전송시스템 고도화 | amount=316800000.0 | why=technical upgrade project; useful for interface, operations, performance, and failure-response checks
- S_KOGAS_ERP: DOC048 | 한국가스공사 | [재공고]차세대 통합정보시스템(ERP) 구축 | amount=14107009000.0 | why=large ERP/backoffice build; useful for contract and integration/migration checks
- S_BONGHWA_DISASTER: DOC005 | 경상북도 봉화군 | 봉화군 재난통합관리시스템 고도화 사업(협상)(긴급) | amount=900000000.0 | why=disaster integrated management project; useful for security, control, and operational risk checks
- S_HEAVY_ION: DOC051 | 기초과학연구원 | 2025년도 중이온가속기용 극저온시스템 운전 용역 | amount=743070000.0 | why=explicit cryogenic operation service case for negative AI prediction question
- S_MEDICAL_DEVICE_A: DOC022 | 한국보건산업진흥원 | 의료기기산업 종합정보시스템(정보관리기관) 기능개선 사업 | amount=50000000.0 | why=medical device information system first issuer variant
- S_MEDICAL_DEVICE_B: DOC047 | BioIN | 의료기기산업 종합정보시스템(정보관리기관) 기능개선 사업(2차) | amount=50000000.0 | why=same/near-same medical device information system title with BioIN issuer variant
- S_NUCLEAR_DOSE: DOC082 | 한국원자력연구원 | 한국원자력연구원 선량평가시스템 고도화 | amount=46600000.0 | why=correct organization is institute, useful for wrong-org correction
- S_MISSING_AMOUNT_RENEWABLE: DOC060 | 대한상공회의소 | 기업 재생에너지 지원센터 홈페이지 개편 및 시스템 고도화 사업 | amount=None | why=only corpus row with missing budget value
- S_LMS_SPORTS_ETHICS: DOC009 | 재단법인스포츠윤리센터 | 스포츠윤리센터 LMS(학습지원시스템) 기능개선 | amount=46445000.0 | why=compact LMS case for education follow-up expansion
- S_BUS_UIS_ULSAN: DOC034 | 울산광역시 | 2024년 버스정보시스템 확대 구축 및 기능개선 용역 | amount=986945000.0 | why=large bus information system case for transport comparison
- S_BIFF: DOC058 | (사)부산국제영화제 | 2024년 BIFF & ACFM 온라인서비스 재개발 및 행사지원시스템 공급 용역 입찰 공고의 건 | amount=243000000.0 | why=BIFF/ACFM cultural online-service target
- S_E_NARADOOM: DOC036 | 한국재정정보원 | e나라도움 업무시스템 웹 접근성 컨설팅 | amount=70000000.0 | why=e-Naradoum web accessibility consulting target
- S_REDCROSS_DR: DOC096 | 대한적십자사 의료원 | 적십자병원 병원정보 재해복구시스템 구축 용역 재공고입찰 | amount=500000000.0 | why=hospital information disaster recovery target

## Case Table
| id | shard | mode | status | EDD | subtotal | seeds | gates |
|---|---|---|---|---:|---|---|---|
| Q001 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q002 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q003 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q004 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q005 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q006 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q007 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q008 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q009 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q010 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q011 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q012 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q065 | A_metadata_corpus | metadata_corpus_sidecar | ready | no |  |  | G_METADATA_AGGREGATION |
| Q033 | A_metadata_corpus | multi_document_comparison_or_business_recommendation | ready | yes | ordinary_comparison_quarantined_inside_A |  | G_MULTI_DOC_COMPARISON, G_QUARANTINED_COMPARISON_SUBTOTAL |
| Q034 | A_metadata_corpus | multi_document_comparison_or_business_recommendation | ready | yes | ordinary_comparison_quarantined_inside_A |  | G_MULTI_DOC_COMPARISON, G_QUARANTINED_COMPARISON_SUBTOTAL |
| Q035 | A_metadata_corpus | multi_document_comparison_or_business_recommendation | ready | yes | ordinary_comparison_quarantined_inside_A |  | G_MULTI_DOC_COMPARISON, G_QUARANTINED_COMPARISON_SUBTOTAL |
| Q024 | B_contract_technical_extract | concrete_single_document_rag | ready | yes |  | S_BIFF | G_SINGLE_DOC_TARGET |
| Q026 | B_contract_technical_extract | concrete_single_document_rag | ready | yes |  | S_E_NARADOOM | G_SINGLE_DOC_TARGET |
| Q027 | B_contract_technical_extract | concrete_single_document_rag | ready | yes |  | S_REDCROSS_DR | G_SINGLE_DOC_TARGET |
| Q038 | B_contract_technical_extract | selected_project_seeded_contract_rag | ready | yes |  | S_PORTAL_KOREA_UNIV, S_KOGAS_ERP | G_SELECTED_PROJECT_MEMORY, G_CONTRACT_FIELDS |
| Q039 | B_contract_technical_extract | selected_project_seeded_contract_rag | ready | yes |  | S_PORTAL_KOREA_UNIV, S_KOGAS_ERP | G_SELECTED_PROJECT_MEMORY, G_CONTRACT_FIELDS |
| Q040 | B_contract_technical_extract | selected_project_seeded_contract_rag | ready | yes |  | S_PORTAL_KOREA_UNIV, S_KOGAS_ERP | G_SELECTED_PROJECT_MEMORY, G_CONTRACT_FIELDS |
| Q041 | B_contract_technical_extract | selected_project_seeded_contract_rag | ready | yes |  | S_PORTAL_KOREA_UNIV, S_KOGAS_ERP | G_SELECTED_PROJECT_MEMORY, G_CONTRACT_FIELDS |
| Q042 | B_contract_technical_extract | selected_project_seeded_contract_rag | ready | yes |  | S_PORTAL_KOREA_UNIV, S_KOGAS_ERP | G_SELECTED_PROJECT_MEMORY, G_CONTRACT_FIELDS |
| Q043 | B_contract_technical_extract | selected_project_seeded_contract_rag | ready | yes |  | S_PORTAL_KOREA_UNIV, S_KOGAS_ERP | G_SELECTED_PROJECT_MEMORY, G_CONTRACT_FIELDS |
| Q044 | B_contract_technical_extract | selected_project_seeded_contract_rag | ready | yes |  | S_PORTAL_KOREA_UNIV, S_KOGAS_ERP | G_SELECTED_PROJECT_MEMORY, G_CONTRACT_FIELDS |
| Q045 | B_contract_technical_extract | selected_project_seeded_contract_rag | ready | yes |  | S_PORTAL_KOREA_UNIV, S_KOGAS_ERP | G_SELECTED_PROJECT_MEMORY, G_CONTRACT_FIELDS |
| Q046 | B_contract_technical_extract | selected_project_seeded_technical_rag | ready | yes |  | S_ADD_LARGE_TRANSFER, S_KOGAS_ERP, S_BONGHWA_DISASTER | G_SELECTED_PROJECT_MEMORY, G_TECHNICAL_REQUIREMENT_FIELDS |
| Q047 | B_contract_technical_extract | selected_project_seeded_technical_rag | ready | yes |  | S_ADD_LARGE_TRANSFER, S_KOGAS_ERP, S_BONGHWA_DISASTER | G_SELECTED_PROJECT_MEMORY, G_TECHNICAL_REQUIREMENT_FIELDS |
| Q048 | B_contract_technical_extract | selected_project_seeded_technical_rag | ready | yes |  | S_ADD_LARGE_TRANSFER, S_KOGAS_ERP, S_BONGHWA_DISASTER | G_SELECTED_PROJECT_MEMORY, G_TECHNICAL_REQUIREMENT_FIELDS |
| Q049 | B_contract_technical_extract | selected_project_seeded_technical_rag | ready | yes |  | S_ADD_LARGE_TRANSFER, S_KOGAS_ERP, S_BONGHWA_DISASTER | G_SELECTED_PROJECT_MEMORY, G_TECHNICAL_REQUIREMENT_FIELDS |
| Q050 | B_contract_technical_extract | selected_project_seeded_technical_rag | ready | yes |  | S_ADD_LARGE_TRANSFER, S_KOGAS_ERP, S_BONGHWA_DISASTER | G_SELECTED_PROJECT_MEMORY, G_TECHNICAL_REQUIREMENT_FIELDS |
| Q051 | C_technical_followup_boundary | selected_project_seeded_technical_rag | ready | yes |  | S_ADD_LARGE_TRANSFER, S_KOGAS_ERP, S_BONGHWA_DISASTER | G_SELECTED_PROJECT_MEMORY, G_TECHNICAL_REQUIREMENT_FIELDS |
| Q052 | C_technical_followup_boundary | selected_project_seeded_technical_rag | ready | yes |  | S_ADD_LARGE_TRANSFER, S_KOGAS_ERP, S_BONGHWA_DISASTER | G_SELECTED_PROJECT_MEMORY, G_TECHNICAL_REQUIREMENT_FIELDS |
| Q053 | C_technical_followup_boundary | selected_project_seeded_technical_rag | ready | yes |  | S_ADD_LARGE_TRANSFER, S_KOGAS_ERP, S_BONGHWA_DISASTER | G_SELECTED_PROJECT_MEMORY, G_TECHNICAL_REQUIREMENT_FIELDS |
| Q054 | C_technical_followup_boundary | corpus_discovery_rag_with_sidecar | ready | yes |  |  | G_CORPUS_DISCOVERY |
| Q055 | C_technical_followup_boundary | corpus_discovery_rag_with_sidecar | ready | yes |  |  | G_CORPUS_DISCOVERY |
| Q062 | C_technical_followup_boundary | negative_requirement_check | ready | yes |  | S_HEAVY_ION | G_NEGATIVE_REQUIREMENT |
| Q063 | C_technical_followup_boundary | near_duplicate_comparison | ready | yes |  | S_MEDICAL_DEVICE_A, S_MEDICAL_DEVICE_B | G_DUPLICATE_TITLE_DISAMBIGUATION |
| Q064 | C_technical_followup_boundary | wrong_org_correction_boundary | ready | yes |  | S_NUCLEAR_DOSE | G_ENTITY_CORRECTION |
| Q067 | C_technical_followup_boundary | conversation_seeded_followup_rag | ready | yes |  | S_PORTAL_KOREA_UNIV | G_FOLLOWUP_CONTEXT_MEMORY |
| Q069 | C_technical_followup_boundary | conversation_seeded_numeric_comparison | ready | yes |  | S_PORTAL_KOREA_UNIV, S_LMS_SPORTS_ETHICS | G_NUMERIC_COMPARISON |
| Q070 | C_technical_followup_boundary | conversation_seeded_domain_expansion | ready | yes |  | S_LMS_SPORTS_ETHICS | G_FOLLOWUP_DOMAIN_EXPANSION |
| Q071 | C_technical_followup_boundary | conversation_seeded_followup_rag | ready | yes |  | S_PORTAL_KOREA_UNIV | G_FOLLOWUP_CONTEXT_MEMORY |
| Q072 | C_technical_followup_boundary | conversation_seeded_followup_rag | ready | yes |  | S_PORTAL_KOREA_UNIV | G_FOLLOWUP_CONTEXT_MEMORY |
| Q073 | C_technical_followup_boundary | conversation_seeded_followup_rag | ready | yes |  | S_PORTAL_KOREA_UNIV | G_FOLLOWUP_CONTEXT_MEMORY |
| Q075 | C_technical_followup_boundary | unsupported_claim_boundary | ready | yes |  | S_PORTAL_KOREA_UNIV | G_UNSUPPORTED_CLAIM_BOUNDARY |
| Q076 | C_technical_followup_boundary | missing_metadata_abstention_boundary | ready | yes |  | S_MISSING_AMOUNT_RENEWABLE | G_NO_EXACT_BUDGET_GUESS |
| Q077 | D_persona_business_citation | unsupported_claim_boundary | ready | yes | unsupported_claim_boundary | S_PORTAL_KOREA_UNIV | G_UNSUPPORTED_CLAIM_BOUNDARY |
| Q079 | D_persona_business_citation | unsupported_claim_boundary | ready | yes | unsupported_claim_boundary | S_PORTAL_KOREA_UNIV | G_UNSUPPORTED_CLAIM_BOUNDARY |
| Q080 | D_persona_business_citation | unsupported_claim_boundary | ready | yes | unsupported_claim_boundary |  | G_UNSUPPORTED_CLAIM_BOUNDARY |
| Q081 | D_persona_business_citation | unsupported_claim_boundary | ready | yes | unsupported_claim_boundary | S_PORTAL_KOREA_UNIV | G_UNSUPPORTED_CLAIM_BOUNDARY |
| Q082 | D_persona_business_citation | persona_or_business_usefulness_seeded_rag | ready | yes | persona_contextual_usefulness | S_PORTAL_KOREA_UNIV, S_ADD_LARGE_TRANSFER | G_CONTEXTUAL_USEFULNESS |
| Q083 | D_persona_business_citation | persona_or_business_usefulness_seeded_rag | ready | yes | persona_contextual_usefulness | S_PORTAL_KOREA_UNIV, S_ADD_LARGE_TRANSFER | G_CONTEXTUAL_USEFULNESS |
| Q084 | D_persona_business_citation | persona_or_business_usefulness_seeded_rag | ready | yes | persona_contextual_usefulness | S_PORTAL_KOREA_UNIV, S_ADD_LARGE_TRANSFER | G_CONTEXTUAL_USEFULNESS |
| Q085 | D_persona_business_citation | persona_or_business_usefulness_seeded_rag | ready | yes | persona_contextual_usefulness | S_PORTAL_KOREA_UNIV, S_ADD_LARGE_TRANSFER | G_CONTEXTUAL_USEFULNESS |
| Q086 | D_persona_business_citation | persona_or_business_usefulness_seeded_rag | ready | yes | persona_contextual_usefulness | S_PORTAL_KOREA_UNIV, S_ADD_LARGE_TRANSFER | G_CONTEXTUAL_USEFULNESS |
| Q087 | D_persona_business_citation | persona_or_business_usefulness_seeded_rag | ready | yes | persona_contextual_usefulness | S_PORTAL_KOREA_UNIV, S_ADD_LARGE_TRANSFER | G_CONTEXTUAL_USEFULNESS |
| Q088 | D_persona_business_citation | persona_or_business_usefulness_seeded_rag | ready | yes | persona_contextual_usefulness | S_PORTAL_KOREA_UNIV, S_ADD_LARGE_TRANSFER | G_CONTEXTUAL_USEFULNESS |
| Q089 | D_persona_business_citation | persona_or_business_usefulness_seeded_rag | ready | yes | persona_contextual_usefulness | S_PORTAL_KOREA_UNIV, S_ADD_LARGE_TRANSFER | G_CONTEXTUAL_USEFULNESS |
| Q090 | D_persona_business_citation | system_trace_audit | blocked_until_trace_wrapper | no |  |  | G_TRACE_TRANSPARENCY |
| Q091 | D_persona_business_citation | system_trace_audit | blocked_until_trace_wrapper | no |  |  | G_TRACE_TRANSPARENCY |
| Q036 | D_persona_business_citation | multi_document_comparison_or_business_recommendation | ready | yes | business_recommendation_criteria |  | G_MULTI_DOC_COMPARISON, G_BUSINESS_RECOMMENDATION_CRITERIA |
| Q037 | D_persona_business_citation | multi_document_comparison_or_business_recommendation | ready | yes | business_recommendation_criteria |  | G_MULTI_DOC_COMPARISON, G_BUSINESS_RECOMMENDATION_CRITERIA |
