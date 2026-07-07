# 자율 EDD 최적화 루프 (코덱스 사전 지시문)

> 목적: 사람이 매번 지시하지 않아도, **실패 진단에 따라 스스로 분기**하며 holdout EDD를
> 최대화한다. 단 **과적합·지표 게이밍 없이** 진짜 성능을 올린다.
> 이 파일은 사전 지시서다. 코덱스는 각 회차마다 이 규칙을 그대로 따른다.

## 0. 대원칙 (어기면 전체가 무의미)
1. **튜닝은 `questions_v2_tune.json`(18)로만.** 채택 판정은 **`questions_v2_holdout.json`(7)** 로 한다.
2. **holdout에서 regression 나면 무조건 기각.** tune만 오르는 건 과적합이므로 버린다.
3. **챔피언(현재 최고 config)은 항상 보존.** 도전자가 holdout에서 이겨야만 교체.
4. 채점자는 **답변 모델과 다른 강한 모델(gpt-5/gpt-5.5, `JUDGE_MODEL`)** 로 고정. 답변=gpt-5-mini.
5. 모든 회차는 **성공/실패 상관없이** 질문·답변·근거·지표·판단을 로그로 남긴다.

## 1. 상태(state) — `eval/auto_loop/state.json`
```
{
  "champion": { "params": {...}, "prompt_variant": "...", "holdout_edd": <float> },
  "iteration": <int>,
  "history": [ {회차별 후보·tune지표·holdout지표·채택여부·근거} ],
  "no_improve_streak": <int>,
  "budget_calls_left": <int>
}
```

## 2. 루프 (매 회차 이 순서)
1. **진단**: 직전 챔피언의 tune 실패분석(`failure_analysis.json`)에서 **지배적 실패모드**를 센다.
   `low_groundedness / coverage_fail / missed_abstention / false_abstention / high_latency` 중 최다.
2. **개입 선택(분기)**: 아래 §3 표에서 그 실패모드에 매핑된 후보 **1개**를 고른다.
   (이미 시도해 기각된 후보는 건너뛴다. 동률이면 groundedness > coverage > abstention > latency 우선.)
3. **tune 실행**: 그 후보 config로 `questions_v2_tune.json` 전체를 judge 포함 실행 → tune EDD·분해지표.
4. **게이트 A (tune)**: tune EDD가 챔피언 tune EDD 대비 **-1.0 미만으로 떨어지면 즉시 기각**(회차 종료, 로그).
5. **holdout 실행**: 통과 시 `questions_v2_holdout.json`으로 실행 → holdout EDD.
6. **게이트 B (채택 조건, 모두 충족해야 채택)**:
   - holdout EDD ≥ 챔피언 holdout EDD (동률 허용)
   - 정성 감리(스크립트, per-case) 4개 지표(contextual_quality/evidence_fit/usefulness/conciseness) 중 **최소 1개 개선, 나머지 regression 없음**
   - **무결성 가드(§4) 전부 통과**
7. **채택/기각**:
   - 채택 → 챔피언 교체, `no_improve_streak=0`, config를 `config.py`/RAGPipeline 기본값 후보로 승격.
   - 기각 → 챔피언 유지, `no_improve_streak+=1`, 실패 원인·다음 가설 로그.
8. **정지 조건 확인(§5)** → 계속이면 1로.

## 3. 진단 → 개입 매핑 (분기표)
| 지배적 실패모드 | 개입 후보(우선순위순) |
|---|---|
| **low_groundedness** | ① 프롬프트 `strict_evidence` → ② `concise_verified` → ③ temperature 0.2→0.0 → ④ 근거 문서번호 강제 인용 + 미근거 문장 자기검열 후처리 |
| **coverage_fail** (compare/ambiguous) | ① 비교질문 multi-org fallback(각 기관 개별 검색 후 병합) → ② fetch_k 20→40 → ③ 청킹 의미단위(목차 기반) 재색인 |
| **missed_abstention** (없는 정보 우김) | ① 프롬프트에 "낙찰자·가격·미공개값은 문서에 없으면 반드시 '확인 불가'" 명시 → ② 검색 최고 유사도 임계 미만이면 abstain 게이트 |
| **false_abstention / precise value missing** | ① abstention taxonomy 보정("문서에 값 없음"은 정상, 거절 아님) → ② 부분확인 답변 포맷(확인됨/확인불가 분리) |
| **high_latency** (>18s) | ① top_k 8→5 → ② 청크 컨텍스트 상한 축소·중복 제거 → ③ 답변 max_tokens 하향 |

> 개입은 **한 번에 하나만** 바꾼다(어블레이션 유지). 두 개 동시에 바꾸면 원인 귀속이 깨진다.

## 4. 무결성 가드 (게이밍 방지 — 하나라도 걸리면 기각)
- `empty_answer_rate > 0` → 기각.
- `false_abstention_rate`가 챔피언보다 상승 → 기각(모른다 도배 방지).
- 답변이 전부 abstention이 아닌데 `relevance_avg`가 챔피언 대비 -0.3 이상 하락 → 기각(회피로 groundedness만 올리는 것 차단).
- holdout에서 특정 유형(single/compare/abstention 등) 하나라도 **0점 붕괴** → 기각.
- 주기적(3회차마다) judge 재검증: 동일 답변 2개에 같은 점수 주는지 sanity check.

## 5. 정지 조건 (하나라도 만족하면 종료)
- `no_improve_streak >= 4` (더 개선 안 됨 = 수렴).
- holdout EDD ≥ 목표(예: 88) **그리고** 정성 감리 4지표 평균 ≥ 4.0.
- `budget_calls_left <= 0` (API 예산/시간 한도).
- tune·holdout이 다시 포화(둘 다 상한 근처) → 루프 멈추고 **평가셋 강화(v3)** 로 전환.

## 6. 종료 시 산출물
- `eval/auto_loop/state.json` (최종 챔피언 + 전체 이력)
- `eval/auto_loop/leaderboard.md` (회차별 후보·tune·holdout·채택여부·근거)
- 챔피언 config를 `config.py` 기본값 + `RAGPipeline` 기본 params로 확정.
- 업무일지에 "무엇을·왜 채택/기각했나" 서술(일지_작성가이드 형식).

## 7. 사람 개입이 필요한 순간(그때만 멈추고 물어봄)
- 무결성 가드가 **반복해서** 걸림(설계상 지표 정의를 손봐야 할 수 있음).
- 정지 조건 "평가셋 포화"에 도달(v3 생성 방향은 사람이 승인).
- 예산 한도 도달.
