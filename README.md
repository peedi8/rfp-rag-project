# 입찰메이트 RFP 질의응답 RAG 시스템

공공입찰 제안요청서(RFP) 100건을 대상으로, 근거와 함께 답하는 Q&A RAG 시스템입니다.
개인 프로젝트로 GCP 없이 로컬 PC + OpenAI API(시나리오 B)로 구현했습니다.

## 📄 제출물

- **보고서(PDF)**: [보고서.pdf](./보고서.pdf) — 진행 과정, 방법, 실험, 결과, 의사결정, 한계 정리
- **업무일지**: [업무일지.md](./업무일지.md) — 일자별 수행 내용·고민·의사결정 기록

## 개요

- 문서 파싱(hwp/pdf) → 청킹 → 임베딩 → Chroma 검색(자동 기관필터 + MMR) → 근거 기반 답변 생성.
- 성능을 지표로 측정하고 실험으로 개선하는 과정을 중심으로 진행했습니다. 자세한 내용은 보고서를 참조하세요.

## 기술 스택

| 구성 | 선택 |
|------|------|
| LLM | OpenAI `gpt-5-mini` |
| 임베딩 | `text-embedding-3-small` |
| Vector DB | Chroma (로컬 영속) |
| 검색 | 코사인 유사도 + MMR + 발주기관 자동필터 + 쿼리 재작성 |

## 재현 방법

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. API 키 설정 (.env.example 복사 후 OPENAI_API_KEY 입력)
copy .env.example .env

# 3. 인덱스 구축 — 원본 hwp/pdf 전체 파싱본(약 11,842 청크)
python -m scripts.build_index raw

# 4. 대화형 질의
python -m scripts.ask

# 5. 성능 평가 / 설정 비교 실험
python -m scripts.evaluate
python -m scripts.run_experiments
```

> 원본 RFP 데이터를 `data/원본 데이터/` 에 두어야 인덱스를 만들 수 있습니다.
> 데이터는 비밀유지계약(NDA) 대상이라 이 저장소에는 포함하지 않습니다(`.gitignore` 처리).

## 프로젝트 구조

```
rfp-rag-project/
├── config.py                 # 경로·하이퍼파라미터·기본 설정
├── src/
│   ├── data_loader.py        # CSV/원본 로딩, hwp/pdf 파서
│   ├── chunking.py           # 청킹(글자수 800/중첩 150)
│   ├── vectorstore.py        # 임베딩 + Chroma(배치 저장)
│   ├── retriever.py          # 유사도/MMR/자동 기관필터
│   ├── generator.py          # 근거 기반 답변 생성
│   ├── query_rewrite.py      # 후속질문 → 독립질문 재작성
│   └── rag.py                # RAG 파이프라인 통합
├── scripts/
│   ├── build_index.py        # 인덱스 구축 (인자: raw / csv)
│   ├── ask.py                # 대화형 질의
│   ├── evaluate.py           # 성능 평가(지표 + LLM 채점)
│   └── run_experiments.py    # 설정 비교 실험
├── eval/                     # 평가셋 · 실험 결과
├── 보고서.pdf                # 제출 보고서
└── 업무일지.md               # 제출 업무일지
```

## 최종 설정

원본 파싱 데이터 기준으로 `MMR top8 + mmr_lambda 0.5 + fetch_k 20 + 자동필터 + 쿼리재작성`을 기본값으로 사용합니다.
선택 근거와 실험 비교는 보고서 5·6장에 정리돼 있습니다.

---

> ⚠️ 보안: 원본 RFP 데이터와 API 키는 절대 커밋하지 않습니다(`.gitignore` 처리됨).
