# Representative Answer Review Pack

- cases: 8

| id | kind | question_id | selection reason |
|---|---|---|---|
| `A_long_high_score_biff` | saved_rag_answer | `qv3_001_typo_biff_online_services` | High automated score, but answer may be long/list-like; useful for conciseness review. |
| `B_high_latency_mozambique` | saved_rag_answer | `qv3_007_followup_mozambique_its` | High score but very slow/long answer; useful for usefulness-vs-verbosity review. |
| `C_same_org_scope_kwater` | saved_rag_answer | `qv3_003_compare_kwater_three_projects` | Same issuer with three projects; checks whether answer keeps feasibility study separate from system builds. |
| `D_abstain_procurement_contact` | saved_rag_answer | `qv3_006_abstain_seogmin_final_vendor_contacts` | Proper unavailable-info/personal-contact abstention candidate. |
| `E_top5_bad_anyang_original` | saved_rag_answer | `qv3_010_casual_anyang_sports_reservation` | Original top5 failure: mixed nearby sports facility context and missed payment/PG. |
| `F_top5_after_filter_still_misses_pg` | saved_rag_answer | `qv3_010_casual_anyang_sports_reservation` | After source-scope fix, top5 is clean but still misses PG detail. |
| `G_top8_after_filter_recovers_pg` | saved_rag_answer | `qv3_010_casual_anyang_sports_reservation` | After source-scope fix, top8 recovers PG/??/?? details. |
| `H_planted_fabricated_vendor_contact` | planted_calibration_answer | `qv3_006_abstain_seogmin_final_vendor_contacts` | Planted bad answer; should be caught by any trustworthy quality review. |
