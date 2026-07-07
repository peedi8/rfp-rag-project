# V10 Realistic RFP User-Intent Taxonomy Gate Report

This run did not generate answers and did not spend model/API budget. Its purpose was to infer realistic RFP/RAG question types before making a new question file.

## Decision

V10 should be treated as a measurement-map loop first. The next useful step is not "more weird traps"; it is a balanced taxonomy of realistic RFP user intents, with a gate attached to each intent before any answer run.

The recommended gate version is `rfp_rag_user_intent_gate_v10.0.0`.

EDD under this gate must be read with labels:

- `raw_first_execution`: first saved answers on a frozen set.
- `saved_answer_measurement_correction`: same answers rescored after evaluator/scorer changes.
- `diagnostic_repair_or_source_exposed`: targeted/source-inspected/prior-failure repair evidence.
- `strict_validation_first_run`: only if the set is frozen before answer/retrieval/failure inspection and registered as promotable.
- `same_cohort_latency_only`: speed/cost evidence only.

## Final Taxonomy

| intent id | realistic user need | expected answer shape | primary risks | gate signals |
|---|---|---|---|---|
| `single_project_scope_overview` | Known project summary: "what is this RFP asking for?" | supported scope summary | generic boilerplate, wrong project bleed | coverage, groundedness, project_mixing |
| `module_level_requirement_split` | Specific modules or requirement buckets | preserve all supported subclaims | under-answering hidden by high judge score | claim preservation, missing_required_claim |
| `plain_language_usefulness` | Short explanation for non-experts | concise plain-language answer | high-score but overlong answer | answer_too_verbose_for_summary, plain_language_overstructured |
| `contextual_followup_refinement` | Follow-up without repeating project name | same target, narrowed answer | losing prior context | follow-up target retention |
| `same_issuer_or_near_topic_comparison` | Compare similar projects | separate each project, then compare | project mixing, missing comparison axis | hit_all_targets, project_mixing |
| `project_stage_scope_boundary` | Build vs ISP/ISMP/F/S/operation/maintenance | state actual stage and boundary | title-bias overclaim | unsupported_scope_transfer |
| `exact_supported_field_extraction` | Exact budget/deadline/contact/criteria | exact value if retrievable, caveat if not | CSV-only metadata mismatch | usefulness_exact_value_missing, csv_only_metadata_requested |
| `unsupported_final_result_or_calculation` | Final vendor/score/contract/result request | refuse unsupported final-result field | confusing budget/criteria with result | unsupported_final_result |
| `sensitive_private_or_fabricated_example` | Private contact or fake patient/child/victim examples | short refusal, maybe safe public scope | leakage, fabricated case, refusal tail | private_contact_leak, sensitive_case_fabricated |
| `ambiguous_title_fragment_identification` | User remembers only a title fragment | identify only when enough context, otherwise ask/abstain | picking plausible wrong project | ambiguous_query_answered_without_clarification |
| `wrong_premise_or_buzzword_correction` | User brings a plausible but unsupported tech/premise | correct the premise while answering supported core | confirming unsupported assumption | buzzword_overclaim, marker_text_misread |
| `semantic_stability_noisy_paraphrase` | Same intent phrased casually/noisily | stable grounded core | wording changes retrieval/claims | metamorphic consistency |

## Corpus Boundary

The corpus has structured listing metadata and extracted RFP text. The current generation context generally exposes project title, issuer, and retrieved text chunks, but not every CSV metadata field.

Use explicit `answerability_source` per case:

- `rag_text`: normal RFP body answerability.
- `metadata_visible_in_body`: listing metadata also appears in the RFP text.
- `csv_metadata_only`: useful diagnostic, but not ordinary strict RAG text evidence.
- `unsupported_absent`: final award/result/private data absent from RFP.
- `mixed`: answerable and unavailable/private fields are both present in the user request.

Exact budget/deadline cases need a preflight: if the value is only visible in CSV metadata and not in retrieved RFP text, the case should be metadata diagnostic or the system should intentionally add metadata to answer context.

## Gate Rules

Use EDD as the main aggregate only inside a fixed gate. Sidecar blockers decide whether a high EDD is actually usable.

Hard or near-hard sidecar blockers:

- `usefulness_exact_value_missing`
- `csv_only_metadata_requested`
- `unsupported_final_result`
- `mixed_field_over_refusal`
- `private_contact_leak`
- `sensitive_case_fabricated`
- `project_mixing`
- `ambiguous_query_answered_without_clarification`
- `answer_too_verbose_for_summary`
- `latency_tail_exceeds_gate`

Do not fold field-level diagnostics into aggregate EDD until the scorer is stable. Report field metrics beside EDD.

## Recommended V10 Cohort

For a first compact v10 question file, use 12-16 cases:

- 2 supported project summaries
- 2 exact value/body-visible metadata cases
- 2 comparison or same-issuer cases
- 2 stage-boundary cases
- 2 mixed answerable/unavailable field cases
- 1 plain-language usefulness case
- 1 ambiguity/title-fragment case
- 1 unsupported final-result case
- 1 sensitive/private fabrication case
- optional 1 noisy paraphrase/metamorphic pair

For each trap or refusal family, include a nearby normal boundary case that should not be refused.

## Before Freezing Questions

- Check exposure registry and avoid treating source-exposed projects as strict held-out evidence.
- Confirm body text length and supporting snippets for normal RAG-text cases.
- Confirm amount/deadline body visibility before exact-value strict cases.
- Run retrieval-only preview before paid judged runs.
- Freeze question JSON and manifest before answer inspection.
- Preserve raw first execution before any repair or measurement correction.

## Outcome

This run adds a gate design, not an EDD point. No strict scoreboard changes.

The useful next action is `v10A`: create a small `questions_v10_realistic_intent_diagnostic_frozen.json` or, if strict validation is desired, first select an untouched source pool and freeze it with a manifest before answer execution.
