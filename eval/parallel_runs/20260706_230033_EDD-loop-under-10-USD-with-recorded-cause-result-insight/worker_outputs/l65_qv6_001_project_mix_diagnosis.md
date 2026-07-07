# L65 qv6_001 Project-Mixing Diagnosis

No API/model calls were made. This is a proposal-only diagnosis from saved artifacts and local code reads.

## Finding

L64 qv6_001 is not an org-level retrieval failure. The row retrieved eight `한국연구재단` chunks, with coverage `1.0`, first hit rank `1`, abstention `false`, and `context_backfill_count=0`.

The groundedness drop to `4` comes from same-issuer project mixing. The target question asks for the UICC project:

`2024년 대학산학협력활동 실태조사 시스템(UICC) 기능개선`

The answer correctly summarizes UICC 기능개선 and 대학정보공시 연계, but the 운영지원 section also cites generic 운영/관리 material:

- `문서5·문서7(운영·관리 관련 제시사항 일부)`
- `사업 단계별 착수·중간·완료보고회, 품질보증·프로젝트 관리 방안 제출 등 운영·관리 요구(문서3·문서7...)`

The saved judge reason says those generic 운영/관리 claims appear to come from 기초학문자료센터-related documents, which is a project-scope bleed under the same `한국연구재단` issuer.

## Root Cause

`src/rag.py` passes all retrieved chunks to generation after retrieval/backfill. The evaluation harness records org coverage but not retrieved 사업명 precision. `src/generator.py` default prompt says to answer from provided documents, but it does not require same-issuer multi-project separation. The ambiguous-title guard only triggers when there are explicit ambiguous-title markers and at least two retrieved orgs, so it does not catch this all-한국연구재단 multi-project case.

## Proposed Narrow Fix

Add a deterministic same-issuer project-scope guard before generation:

1. Detect multiple distinct `metadata["사업명"]` values under one `발주 기관`.
2. If the query contains a unique discriminative title fragment matching exactly one retrieved project, keep/rank that project's chunks for generation.
3. Treat acronyms like `UICC`, quoted/full title fragments, years, and rare long Hangul fragments as discriminative.
4. Ignore generic words such as `기능개선`, `운영지원`, `고도화`, and `시스템`.
5. If zero or multiple projects match, do not choose; preserve ambiguity behavior.

As defense in depth, add one default-prompt line: when 참고 문서 contains different 사업명 values under the same 발주기관, do not combine their requirements.

## No-API Fixtures

- Synthetic same-org chunks for UICC plus 기초학문자료센터; query includes `UICC`; assert only UICC chunks are selected.
- Same chunks with only generic fragments; assert no project is selected.
- Two candidates with the same generic title fragment; assert ambiguity is preserved.
- Saved qv6_001 answer plus doc-to-project mapping; assert 문서3/5/7 are flagged as source-project mixing.
- Evaluation fixture with all orgs matching but multiple 사업명 values; assert details record retrieved_projects/project_mix_candidate_count.

## Risks

Main risk is over-filtering legitimate comparison questions or ambiguous fragments. Mitigate by requiring a unique discriminative title match and skipping the guard for comparison/multi-candidate wording.
