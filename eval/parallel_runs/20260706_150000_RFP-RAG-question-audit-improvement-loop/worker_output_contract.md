# Worker Output Contract

Workers are proposal-only. They must not edit source files, final config, the work diary, or the experiment log.

## question_generator

Path: `worker_outputs/question_generator/questions_v2_proposals.json`

Required schema:

```json
{
  "schema": "rfp_rag_question_proposals.v1",
  "created_at": "ISO-8601",
  "model_or_worker": "string",
  "strategy": "string",
  "questions": [
    {
      "id": "string",
      "type": "single_extract | followup | compare | precise_check | ambiguous_org | abstention | score_trap",
      "turns": ["string"],
      "target_orgs": ["string"],
      "target_biz": "string",
      "expect_abstention": false,
      "why_this_tests_the_system": "string",
      "expected_failure_mode": "string"
    }
  ]
}
```

## rag_answer_runner

Path: `worker_outputs/rag_answer_runner/results.json`

Required schema:

```json
{
  "schema": "rfp_rag_answer_run.v1",
  "created_at": "ISO-8601",
  "question_set": "path",
  "experiments": [
    {
      "experiment": "string",
      "params": {},
      "metrics": {},
      "edd_score": 0.0,
      "cases": [
        {
          "question_id": "string",
          "turns": ["string"],
          "answer": "string",
          "retrieved_orgs": ["string"],
          "coverage": 1.0,
          "first_hit_rank": 1,
          "abstention": false,
          "expect_abstention": false,
          "latency_sec": 0.0,
          "automatic_flags": ["string"]
        }
      ]
    }
  ]
}
```

## quality_audit_55

Path: `worker_outputs/quality_audit_55/audit_results.json`

Required schema:

```json
{
  "schema": "rfp_rag_quality_audit_results.v1",
  "created_at": "ISO-8601",
  "audit_input": "path",
  "auditor_model_or_worker": "string",
  "results": [
    {
      "case_id": "string",
      "contextual_quality": 1,
      "evidence_fit": 1,
      "usefulness": 1,
      "decision": "pass | pass_with_caveat | fail",
      "risk_flags": ["string"],
      "reason": "string",
      "recommended_next_action": "keep | revise_prompt | revise_retrieval | add_question | manual_review"
    }
  ]
}
```

## report_evidence_pack

Path: `worker_outputs/report_evidence_pack/report_evidence.json`

Required contents:

- question id, question turns, target orgs, and expected abstention
- answer and answer excerpt
- retrieved organizations
- EDD and secondary metrics
- automatic flags
- quality audit decision when available
- cause analysis
- next action
