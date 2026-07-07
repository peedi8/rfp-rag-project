# Checkpoint 01 - Inputs

- objective: RFP RAG question generation answer audit evidence improvement loop
- workspace: I:\0706\rfp-rag-project
- run_dir: I:\0706\rfp-rag-project\eval\parallel_runs\20260706_150000_RFP-RAG-question-audit-improvement-loop
- cpu_percent_at_start: 5.0
- recommended_workers: 4

## Protected Paths
- config.py
- src
- eval\questions.json
- 업무일지.md
- eval\experiment_log.md

## Tasks
- question_generator: Generate diverse high-reasoning adversarial and realistic RFP RAG questions only; no answers; output JSON proposals
- rag_answer_runner: Run current RAG defaults on frozen and newly selected question cohort; output answers metrics and raw evidence
- quality_audit_55: Audit answer quality with a high-reasoning judge for contextual fit evidence fit usefulness and suspicious high-score cases
- report_evidence_pack: Build report evidence packet linking every selected question answer retrieval metrics EDD and human-readable insight
