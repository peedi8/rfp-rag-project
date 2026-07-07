# Checkpoint 01 - Inputs

- objective: RFP RAG parallel EDD full run after abstention fix
- workspace: I:\0706\rfp-rag-project
- run_dir: I:\0706\rfp-rag-project\eval\parallel_runs\20260706_134254_RFP-RAG-parallel-EDD-full-run-after-abstention-fix
- cpu_percent_at_start: 9.0
- recommended_workers: 4

## Protected Paths
- I:\0706\rfp-rag-project\업무일지.md
- I:\0706\rfp-rag-project\eval\experiment_log.md
- I:\0706\rfp-rag-project\CLAUDE.md
- I:\0706\rfp-rag-project\config.py
- I:\0706\rfp-rag-project\src\**
- I:\0706\rfp-rag-project\chroma_db\**

## Tasks
- topk_sweep: Run top_k 5/8/12 against frozen raw index
- mmr_lambda_sweep: Run mmr_lambda 0.3/0.5/0.7 against frozen raw index
- fetchk_sweep: Run fetch_k 20/40 against frozen raw index
- filter_rewrite_ablation: Run auto_filter on/off x rewrite_query on/off ablation
