# Checkpoint 01 - Inputs

- objective: validate champion and continue EDD improvement loop
- workspace: I:\0706\rfp-rag-project
- run_dir: I:\0706\rfp-rag-project\eval\parallel_runs\20260706_173741_validate-champion-and-continue-EDD-improvement-loop
- cpu_percent_at_start: 5.0
- recommended_workers: 4

## Protected Paths
- final target index.html
- renderer source files
- prepared payload JSON
- option consumer payload JSON
- stage slot pack candidate files

## Tasks
- holdout_validation: run champion top8 on held-out v2 questions
- judge_bias_check: rescore saved champion answers with old versus balanced judge contexts
- latency_candidate_review: analyze top5/adaptive top_k risk and speed tradeoff
- quality_audit: audit high-risk answers for unsupported claims
