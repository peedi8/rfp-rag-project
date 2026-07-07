# L120 Metadata Sidecar Results

No-API metadata sidecar readiness run; not an ordinary EDD leaderboard row.

## Summary
- case_count: 17
- ready_count: 17
- sidecar_readiness_score: 1.000
- exact_semantic_accuracy_mean: 1.0
- exact_semantic_accuracy_n: 6
- candidate_or_taxonomy_n: 11

## Strictness Counts
- taxonomy_candidate: 1
- exact_repeated_org_set: 1
- exact_top_amount_order: 1
- exact_amount_threshold_set: 1
- exact_amount_threshold_set_with_domain_note: 1
- candidate_keyword_discovery: 9
- exact_format_count: 1
- candidate_followup_domain_expansion: 1
- boundary_missing_metadata: 1

## Cases
| id | key | mode | strictness | status | docs | claim |
|---|---|---|---|---|---:|---|
| Q001 | Q001 | metadata_corpus_sidecar | taxonomy_candidate | ready | 54 | no-api sidecar readiness; not a model answer and not an EDD row; candidate list requires row-level evidence review |
| Q002 | Q002 | metadata_corpus_sidecar | exact_repeated_org_set | ready | 24 | no-api sidecar readiness; not a model answer and not an EDD row |
| Q003 | Q003 | metadata_corpus_sidecar | exact_top_amount_order | ready | 10 | no-api sidecar readiness; not a model answer and not an EDD row |
| Q004 | Q004 | metadata_corpus_sidecar | exact_amount_threshold_set | ready | 37 | no-api sidecar readiness; not a model answer and not an EDD row |
| Q005 | Q005 | metadata_corpus_sidecar | exact_amount_threshold_set_with_domain_note | ready | 22 | no-api sidecar readiness; not a model answer and not an EDD row |
| Q006 | Q006 | metadata_corpus_sidecar | candidate_keyword_discovery | ready | 29 | no-api sidecar readiness; not a model answer and not an EDD row; candidate list requires row-level evidence review |
| Q007 | Q007 | metadata_corpus_sidecar | candidate_keyword_discovery | ready | 7 | no-api sidecar readiness; not a model answer and not an EDD row; candidate list requires row-level evidence review |
| Q008 | Q008 | metadata_corpus_sidecar | candidate_keyword_discovery | ready | 37 | no-api sidecar readiness; not a model answer and not an EDD row; candidate list requires row-level evidence review |
| Q009 | Q009 | metadata_corpus_sidecar | candidate_keyword_discovery | ready | 7 | no-api sidecar readiness; not a model answer and not an EDD row; candidate list requires row-level evidence review |
| Q010 | Q010 | metadata_corpus_sidecar | candidate_keyword_discovery | ready | 13 | no-api sidecar readiness; not a model answer and not an EDD row; candidate list requires row-level evidence review |
| Q011 | Q011 | metadata_corpus_sidecar | candidate_keyword_discovery | ready | 8 | no-api sidecar readiness; not a model answer and not an EDD row; candidate list requires row-level evidence review |
| Q012 | Q012 | metadata_corpus_sidecar | exact_format_count | ready | 0 | no-api sidecar readiness; not a model answer and not an EDD row |
| Q065 | Q065 | metadata_corpus_sidecar | candidate_keyword_discovery | ready | 5 | no-api sidecar readiness; not a model answer and not an EDD row; candidate list requires row-level evidence review |
| Q054 | Q054 | corpus_discovery_rag_with_sidecar | candidate_keyword_discovery | ready | 29 | no-api sidecar readiness; not a model answer and not an EDD row; candidate list requires row-level evidence review |
| Q055 | Q055 | corpus_discovery_rag_with_sidecar | candidate_keyword_discovery | ready | 26 | no-api sidecar readiness; not a model answer and not an EDD row; candidate list requires row-level evidence review |
| Q070 | Q006 | conversation_seeded_domain_expansion | candidate_followup_domain_expansion | ready | 29 | no-api sidecar readiness; not a model answer and not an EDD row; intentional sidecar alias to Q006; candidate list requires row-level evidence review |
| Q076 | Q076 | missing_metadata_abstention_boundary | boundary_missing_metadata | ready | 1 | no-api sidecar readiness; not a model answer and not an EDD row |

## Intentional Sidecar Aliases
- Q070 -> Q006: Intentional sidecar alias: this case uses metadata key Q006 because the manifest points to a shared corpus-discovery preflight set.
