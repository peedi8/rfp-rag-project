# CLAUDE.md — 프로젝트 컨텍스트 & 인수인계

> 이 파일은 이 프로젝트를 이어받는 에이전트(Claude Code 등)가 맥락을 잃지 않도록
> 요구사항·결정·현재상태·함정·남은일을 정리한 문서다. **작업 전 반드시 통독할 것.**

---

## 0. 한 줄 요약
코드잇 AI 스프린트 **중급 프로젝트(개인)** — 공공입찰 제안요청서(RFP) 100건을 대상으로
질의응답이 가능한 **RAG 시스템**을 로컬 + OpenAI API로 구축한다. GCP 미사용.

## 1. 과제 요구사항 (개인 가이드 기준)
- **미션**: RFP 문서 내용을 추출·요약해 Q&A 하는 사내 RAG 시스템 구축.
- **데이터**: 실제 RFP 100건(hwp 96 + pdf 4) + `data_list.csv` 메타데이터. **NDA — 원본 데이터 외부 공유/커밋 금지.**
- **개인 프로젝트 특이사항**:
  - 클라우드 서버(GCP) 미제공 → **로컬 PC + LLM API(시나리오 B)** 로 진행.
  - RAG 시스템의 **일부 또는 전체** 구현 허용(범위 축소 가능). 단 보고서 필수.
  - 발표 없음. 팀 평가·과정평가 대상 아님. 주강사 개인 결과평가만.
- **허용 모델**: `gpt-5-mini`, `gpt-5-nano`, `text-embedding-3-small` (+ 테스트용 `gpt-5` 제한적).
- **필수 요구**: hwp/pdf 두 포맷 대응, 청킹, 임베딩, retrieval(메타데이터 필터링 포함), generation(대화맥락 유지), **성능 평가(지표 직접 선정)**, 결론/분석 보고서.
- **핵심 취지**: "돌아가느냐"가 아니라 **성능을 어떻게 측정하고 실험으로 개선했는지, 그 의사결정을 보고서에 드러내는 것**.

## 2. 제출물 & 마감 (개인)
- **GitHub 레포 링크 + 보고서 PDF** → 프로젝트 종료 D-1 **7/7(화) 19:00** (주말 제외).
- **업무일지** → 종료일 **7/8(수) 23:50**. (Readme에 링크/첨부)
- 보고서는 레포 README에서 다운로드 가능하게 첨부.
- ⚠️ 개인 전환은 페널티 대상이나 **결과물 제출 시 즉시 구제**. 일정은 강사님과 1:1로 확인 권장.

## 3. 실행 환경 & 방법
- Python 3.14, Windows. 작업 경로: `I:\0706\rfp-rag-project`.
- **API 키**: 본인 OpenAI 키 사용. 키는 `.env/gpt.txt`(폴더 안)에 원시 문자열로 있음.
  `config._load_api_key()`가 환경변수 → `.env.local` → `.env/gpt.txt` 순으로 자동 로드.
  ⚠️ `.env`가 **폴더**로 존재하는 특수 상황이라 일반 `.env` 파일 방식은 안 됨. 키는 절대 커밋 금지(`.gitignore` 처리됨).
- 설치: `pip install -r requirements.txt`
- 실행:
  ```
  python -m scripts.build_index            # CSV 추출본으로 인덱스 구축 (기본)
  python -m scripts.build_index raw        # 원본 hwp/pdf 전체 파싱본으로 구축
  python -m scripts.ask                    # 대화형 질의
  python -m scripts.smoke_test             # 질문 1개 빠른 확인
  python -m scripts.evaluate               # 단일 평가
  python -m scripts.run_experiments        # 7개 설정 비교표 (→ eval/results/*.csv)
  ```
- **주의**: OpenAI 호출은 사용자 PC(로컬)에서만 가능. (Cowork 샌드박스는 OpenAI 접속 차단)

## 4. 아키텍처 / 파일 맵
```
config.py                 # 경로·하이퍼파라미터·키로더·DATA_SOURCE
src/
  data_loader.py          # CSV/raw 로딩, HWP·PDF 파서(서로게이트·컨트롤문자 처리), doc_id 유일화
  chunking.py             # 글자수 800/중첩 150 청킹
  vectorstore.py          # 임베딩(text-embedding-3-small)+Chroma, 배치저장(5000), sanitize
  retriever.py            # 유사도/MMR/자동필터(LCS+$in)/LLM리랭크
  generator.py            # 근거기반 답변 생성(환각억제), 대화히스토리
  query_rewrite.py        # 후속질문 → 독립질문 재작성(condense)
  rag.py                  # RAGPipeline: params dict로 실험설정 주입
scripts/
  build_index.py          # 인덱스 구축 (인자 raw/csv)
  ask.py / smoke_test.py  # 질의
  evaluate.py             # 지표 계산 + LLM-judge + 빈인덱스 가드
  run_experiments.py      # 설정 스윕 비교표
eval/
  questions.json          # 10케이스 평가셋(정답기관 라벨 포함)
  results/                # 실험 결과 CSV/JSON 저장
업무일지.md               # Day 1~7 작성됨 (Day 8 예정)
```

## 5. 데이터 핵심
- `data_list.csv`의 `텍스트` 컬럼에 본문 일부가 이미 추출돼 있음(문서당 ~3.8천자 = 원문 일부).
- **원본 파싱(raw)** 시 문서당 평균 **7.3만 자**(19배). 청크 616개(csv) → **11,842개(raw)**.
- CSV 파일명 ↔ 실제 파일 100/100 정확 매칭. 발주기관 87종.

## 6. 핵심 결정 & 근거
- **GCP 미사용, 시나리오 B**: 개인이라 GPU 서빙 오버킬. API로 완성도 우선. A는 선택사항(보고서에 비교분석만).
- **Vector DB = Chroma**: 로컬 영속 + 메타데이터 필터링.
- **자동 기관필터 채택**: 실험서 MRR 0.54→0.75, 최저 지연. 기관명 LCS 매칭 + 비교질문은 `$in`.
- **LLM 리랭크 폐기**: 검색개선 0 + 지연 2배. (안 되는 것도 근거로 보고서에 남김)
- **원본 파싱 도입**: CSV 텍스트가 얕아 답변품질 낮음(groundedness 1.4~2.25/5) → 원본으로 전환.
- **쿼리 재작성 도입**: 후속질문(기관명 생략)이 검색 실패 → 히스토리 반영 독립질문화.
- **최종 기본 검색 설정**: 병렬 EDD 실험(2026-07-06)에서 `MMR top8 + mmr_lambda 0.5 + fetch_k 20 + 자동필터 + 쿼리재작성`이 EDD 96.57, coverage/MRR 1.0, groundedness 4.667, relevance 5.0으로 최상위. top5도 근접했지만 문맥 여유와 기존 가설 일관성을 위해 top8을 기본값으로 고정.
- **5.5급 품질 감리 추가 필요**: EDD는 정량 비교용이고, 실제 사용자 맥락에 맞는 답변인지 보증하려면 강한 LLM 감리 레이어가 필요. 최종 후보는 contextual_quality/evidence_fit/answer_usefulness 기준으로 별도 판정하고, 충돌 시 일지에 원인과 판단 변화를 남길 것.
- **보고서 근거 패킷 필요**: 최종 보고서는 단순 지표표가 아니라 q1~q10 질문/답변/근거/점수/납득 여부/다음 실험 결정의 연결을 보여줘야 함. 고득점이지만 납득 안 되는 답변, 저득점이지만 평가식 문제였던 답변도 숨기지 말고 기록.
- **출제자/응답자/채점자 분리**: 질문은 가능하면 강한 추론 모델이 다양하게 생성하고, 답변은 반드시 평가 대상 RAG 파이프라인이 생성하며, 답변 품질은 다시 강한 모델이 감리한다. 질문 생성 메타데이터(target_orgs/target_biz)는 평가용으로만 쓰고 답변 모델에 직접 힌트로 주지 말 것.

## 7. 함정 / 이미 해결한 버그 (재발 방지)
1. **doc_id 중복(nan)**: 공고번호 결측 → doc_id `nan` 충돌. 행번호+접미사로 유일화. (해결)
2. **LLM-judge None**: `gpt-5-mini`는 **추론형** → `max_completion_tokens` 부족 시 본문 빈값. 토큰 900+ / `response_format=json_object` / 정규식 폴백. 리랭크·쿼리재작성도 동일 처리. (해결)
3. **UnicodeEncodeError(surrogates)**: HWP 원문의 서로게이트 → API 전송 실패. 파서에서 서로게이트 쌍 결합 + `_clean`/`embed_texts`에서 `utf-8,ignore` sanitize. (해결)
4. **Chroma 배치 상한(5461)**: raw 11,842개 일괄 add 실패 → 5,000개씩 분할 add. (해결)
5. **자동필터 결함**: 비교질문서 한 기관만 필터(나머지 탈락) + 접미사 우연겹침 오필터 → 60%+ 통째 등장(LCS)일 때만, 다중은 `$in`. (해결)
6. **빈 인덱스 착시**: 인덱스 비면 전부 abstention인데 judge가 groundedness 높게 줌 → **coverage 0이면 실패**. evaluate/run_experiments에 빈 인덱스 가드 추가. (해결)
7. **Generator 빈 답변**: raw top8처럼 근거가 길면 `gpt-5-mini`가 `max_completion_tokens=1024`를 전부 reasoning에 써서 `finish_reason=length`, `content=""`가 발생. q1 재현 시 reasoning_tokens=1024/content 빈값 확인 → 기본 생성 토큰 3072, 빈 답변/length 시 4096+ 재시도. (해결)
8. **abstention 과대판정**: 답변 안에 "없습니다"가 한 번만 들어가도 abstention=True가 되어 q1/q2 같은 정상 답변이 거절로 오분류됨. 시작부가 "제공된 문서에서 확인할 수 없음" 류인 경우만 abstention으로 보도록 정규식 기반으로 축소하고, false_abstention_rate/empty_answer_rate를 EDD 페널티에 추가. (해결)
9. **교훈**: 지표는 교차검증. API 불필요한 로직(파싱·Chroma·필터)은 로컬 레드팀으로 선제 검증.

## 8. 현재 상태 (2026-07-06 기준)
- ✅ 베이스라인 파이프라인 완성, CSV 모드 실험 완료.
- ✅ 원본 파서/쿼리재작성/자동필터 개선 완료 + 로컬 레드팀 검증 완료(11,842청크 저장·검색·필터).
- ⏳ **원본(raw) 모드 재빌드 + 실험은 아직 실제 실행 전** (사용자 PC에서 실행 필요).
- ⏳ 보고서 미작성. 업무일지 Day 8(7/7) 미작성.

### CSV 모드 실험 결과 (참고)
| 실험 | coverage | mrr | groundedness | relevance | latency |
|---|---|---|---|---|---|
| baseline 유사도top5 | 0.562 | 0.542 | 1.43 | 1.43 | 10.9s |
| MMR top5 | 0.5 | 0.525 | 2.0 | 2.0 | 11.3s |
| MMR top8 | 0.625 | 0.543 | 2.0 | 2.25 | 9.1s |
| **MMR+자동필터** | 0.625 | **0.75** | 1.63 | 1.88 | 7.7s |
| MMR+LLM리랭크 | 0.562 | 0.542 | 1.67 | 1.67 | 19.7s |

## 9. 다음 할 일 (우선순위)
1. **원본 재빌드 + 실험**: `python -m scripts.build_index raw` → `python -m scripts.run_experiments`.
   - 확인 포인트: build 끝 "저장 완료: 11842개 청크", experiments 시작 "✅ 인덱스 청크 수: 11842".
   - 결과 CSV: `eval/results/experiments_*.csv`.
2. **CSV vs 원본 비교 분석**: groundedness/relevance 상승 여부, 실험7(쿼리재작성)로 후속질문 커버리지 회복 여부.
3. **최종 설정 픽스** (예상: 원본 + MMR top8 + 자동필터 + 쿼리재작성).
4. **보고서 PDF 작성** (배경/데이터/방법/실험/결정/결과/개선/한계). 발표자료로 대체 가능.
5. **업무일지 Day 8 작성**, README에 보고서·업무일지 링크.
6. **GitHub push** (`.gitignore`로 데이터·키 제외 확인).

## 10. 평가셋 & 지표 정의 (evaluate.py)
- 10케이스: 단일추출/멀티종합/후속맥락/비교/부정확기관입력/환각방지.
- 지표: retrieval_coverage, hit_all_targets_rate, mrr, groundedness(LLM-judge), relevance(LLM-judge), abstention_accuracy, latency.
- 정답기관 라벨로 검색 객관채점. groundedness/relevance는 참조없는 LLM 심판.

---
_원본 RFP 데이터와 API 키는 절대 커밋하지 말 것. 이 문서는 커밋 가능(민감정보 없음)._
