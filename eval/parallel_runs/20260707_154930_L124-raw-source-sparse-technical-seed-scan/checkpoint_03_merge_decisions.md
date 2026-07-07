# checkpoint_03_merge_decisions.md

Pending.
# Checkpoint 03 - Merge Decisions

## Accepted

- Added `scripts/find_sparse_technical_seeds.py`.
- Scanned raw HWP/PDF text for 97 technical candidate documents.
- Reclassified the recommendation rule from "few visible groups" to "many absent groups", because sparse diagnostics need enough missing fields rather than a nearly empty document.

## Result

- technical_candidate_docs_scanned: `97`
- field_group_count: `31`
- recommended_sparse_seed_count: `5`
- source_basis_counts: `raw_file_text=97`

## Top Candidates

- DOC073 / 사단법인아시아물위원회사무국 / 우즈벡-키르기즈스탄 기후변화대응 스마트 관개시스템 구축사업: visible `15`, absent `16`.
- DOC051 / 기초과학연구원 / 2025년도 중이온가속기용 극저온시스템 운전 용역: visible `16`, absent `15`.
- DOC025 / 한국수자원공사 / 용인 첨단 시스템반도체 국가산단 용수공급사업 타당성조사 및 기본계획 수립 용역: visible `18`, absent `13`.

## Decision

L124 is source selection only. Before any paid/model answer run, freeze a small sparse diagnostic question file and preserve the raw first answers.
