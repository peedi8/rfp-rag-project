"""성능 평가 하네스.  실행: python -m scripts.evaluate

eval/questions.json 의 케이스(단일/멀티턴)를 실행하고 아래 지표를 계산한다.
- Retrieval: 정답 기관 커버리지, Hit@k, 첫 정답 순위(MRR)
- 답변 품질: Groundedness(충실도), Relevance(관련성)  ← LLM-as-judge (참조 없이)
- 환각 방지: abstention 정확도 (없는 정보엔 '모른다')
- 효율: 평균 지연시간

결과는 eval/results/ 에 JSON 으로 저장.
"""
import sys, os, json, re, time, glob
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.rag import RAGPipeline
from src.costing import sum_cost, traced_call
from scripts.field_level_contact_scorer import score_answer_fields

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTIONS_PATH = os.path.join(ROOT, "eval", "questions.json")
RESULTS_DIR = os.path.join(ROOT, "eval", "results")

ABSTAIN_PATTERNS = [
    r"^(제공된|검색된|참고) 문서.{0,80}(확인할 수 없|찾을 수 없|없습니다|존재하지 않)",
    r"^요청하신 .{0,120}(확인할 수 없|확인되지 않|찾을 수 없|없습니다|존재하지 않)",
    r"^관련 문서(가|는)? .{0,40}(없|확인되지 않)",
    r"^해당 .{0,80}(사업|문서|내용).{0,40}(없|확인되지 않|찾을 수 없)",
    r"^문서에서 .{0,80}(확인할 수 없|찾을 수 없)",
]


# ---------------------------------------------------------------------------
# 순수 함수 (OpenAI 불필요, 단위테스트 가능)
# ---------------------------------------------------------------------------
def retrieval_coverage(retrieved_orgs: list[str], target_orgs: list[str]) -> float:
    """검색된 기관들 안에 정답 기관이 몇 %나 포함됐는지 (0~1)."""
    if not target_orgs:
        return None
    found = sum(any(t in (o or "") or (o or "") in t for o in retrieved_orgs) for t in target_orgs)
    return found / len(target_orgs)


def first_hit_rank(retrieved_orgs: list[str], target_orgs: list[str]) -> int | None:
    """정답 기관이 처음 등장하는 순위(1-based). 없으면 None."""
    if not target_orgs:
        return None
    for rank, o in enumerate(retrieved_orgs, 1):
        if any(t in (o or "") or (o or "") in t for t in target_orgs):
            return rank
    return None


def is_abstention(answer: str) -> bool:
    """Whether the answer refused because relevant evidence was not found.

    Do not treat every sentence containing "없습니다" as abstention. Negative
    findings such as "AI 기반 예측 요구사항은 확인되지 않음" are valid answers.
    """
    normalized = " ".join((answer or "").strip().split())
    if not normalized:
        return True
    prefix = normalized[:900]
    evidence_leadins = (
        "제공된 문서 기준으로 답변",
        "제공된 문서에서 확인되는",
        "제공된 문서 내(",
        "문서에서 확인되는 평가 기준",
        "문서에서 확인되는 평가기준",
        "문서에서 확인되는 평가 방식",
        "문서에서 확인되는 평가방법",
    )
    if normalized.startswith(evidence_leadins):
        return False
    if normalized.startswith(("제공된 문서", "검색된 문서", "참고 문서")):
        hard_markers = ["확인할 수 없습니다", "확인되지 않습니다", "찾을 수 없습니다", "없습니다", "존재하지 않습니다"]
        if any(marker in prefix for marker in hard_markers):
            return True
    requested_missing_fields = ("최종 낙찰", "최종 계약", "평가점수")
    if all(field in normalized for field in requested_missing_fields):
        if normalized.count("확인할 수 없습니다") >= 3 or "기재되어 있지 않아" in normalized[:1400]:
            return True
    procurement_markers = (
        "최종 낙찰",
        "낙찰업체",
        "낙찰자",
        "선정업체",
        "최종 구축업체",
        "구축업체",
        "계약금액",
        "최종 계약",
        "개인 연락처",
    )
    if normalized.startswith("쉽게 말하면") and _bulletish_line_count(answer.splitlines()) >= 3:
        if (
            any(marker in normalized for marker in ("최종 낙찰", "낙찰업체", "계약 결과", "계약결과"))
            and "확인할 수 없습니다" in normalized
        ):
            return False
    procurement_hits = sum(1 for marker in procurement_markers if marker in normalized)
    if procurement_hits >= 2 and normalized.count("제공된 문서에서 확인할 수 없습니다") >= 2:
        return True
    if procurement_hits >= 2 and (
        normalized.count("문서상 확인 불가") >= 2
        or normalized.count("확인 불가") >= 2
    ):
        return True
    if procurement_hits >= 2 and (
        "확인할 수 없습니다" in prefix
        or "확인되지 않습니다" in prefix
        or "확인되지 않" in prefix
    ):
        return True
    unsupported_result_markers = (
        "최종 제안평가",
        "제안평가 점수",
        "최종 점수",
        "평가점수",
        "평가 점수",
        "선정업체명",
        "선정업체",
    )
    unsupported_result_hits = sum(1 for marker in unsupported_result_markers if marker in normalized)
    if unsupported_result_hits >= 2 and any(
        marker in prefix
        for marker in ("확인할 수 없습니다", "확인되지 않습니다", "포함되어 있지 않습니다", "최종계산 불가능")
    ):
        return True
    personal_missing_fields = ("투입 개발자 실명", "개인 휴대전화", "개인 이메일")
    if all(field in normalized for field in personal_missing_fields):
        if normalized.count("확인할 수 없습니다") >= 3 or normalized.count("확인되지 않습니다") >= 3:
            return True
    if "투입 개발자" in normalized and "실명" in normalized and "개인" in normalized:
        if ("이메일" in normalized or "휴대전화" in normalized or "연락처" in normalized):
            if "제공된 문서에서 확인할 수 없습니다" in prefix or "확인되지 않습니다" in prefix:
                return True
    partial_scope_markers = (
        "문서에서 확인되는 범위",
        "문서상 실제 사업 범위",
        "확인되는 범위",
        "확인 가능한 범위",
        "확인된 사항",
        "확실한 항목",
        "문서에서 명시된",
        "문서상 실제",
    )
    if any(marker in normalized[:1800] for marker in partial_scope_markers):
        if any(marker in normalized for marker in ("확인할 수 없습니다", "확인되지 않습니다", "확인되지 않")):
            return False
    if "개인 연락처" in prefix and "제공된 문서에서 확인할 수 없습니다" in prefix:
        return True
    sensitive_example_markers = (
        "실제 환자",
        "환자 이름",
        "환자명",
        "실제 피해자",
        "피해자 상담",
        "상담 사례",
        "개인 이름",
        "실제 인명",
        "아동 이름",
        "아이돌봄 인력 이름",
        "검사 결과 사례",
        "병원 연락처",
        "그럴듯한 예시",
        "가상 예시",
        "가상의 사례",
        "사례 생성",
        "허위 사례",
        "추측",
    )
    sensitive_hits = sum(1 for marker in sensitive_example_markers if marker in normalized)
    if sensitive_hits >= 2 and (
        "확인할 수 없습니다" in prefix
        or "포함되어 있지 않습니다" in prefix
        or "포함되어 있지 않" in prefix
    ):
        return True
    if sensitive_hits >= 2 and (
        "제공할 수 없습니다" in prefix
        or "생성할 수 없습니다" in prefix
        or "응할 수 없습니다" in prefix
        or "예시 생성" in prefix
        or "사례 생성" in prefix
        or "문서에 근거한 예시는 제공할 수 없습니다" in prefix
        or "허위 사례" in prefix
        or "추측" in prefix
    ):
        if "확인할 수 없습니다" in prefix or "포함되어 있지 않습니다" in prefix:
            return True
    if normalized.count("제공된 문서에서 확인할 수 없습니다") >= 5:
        return True
    return any(re.search(pattern, prefix) for pattern in ABSTAIN_PATTERNS)


def _bulletish_line_count(lines: list[str]) -> int:
    return sum(1 for line in lines if re.match(r"^\s*(?:[-*]|\d+[.)])\s+", line))


DETAIL_KEYWORDS = {
    "budget": ["budget", "\uc608\uc0b0", "\ucd94\uc815\uac00\uaca9", "\uc0ac\uc5c5\uae08\uc561"],
    "schedule": ["schedule", "\uc77c\uc815", "\uc0ac\uc5c5\uae30\uac04", "\uacc4\uc57d \ud6c4"],
    "security": ["security", "SER-", "\ubcf4\uc548", "\ucd9c\uc785\ud1b5\uc81c"],
    "performance": ["performance", "PER-", "\uc131\ub2a5"],
    "interface": ["interface", "SIR-", "\uc778\ud130\ud398\uc774\uc2a4"],
    "data": ["data", "DAR-", "\ub370\uc774\ud130", "\uc774\uad00"],
    "requirement": ["requirement", "\uc694\uad6c\uc0ac\ud56d", "\uc694\uad6c\ubc94\uc704"],
}


def _detail_keyword_hits(text: str) -> list[str]:
    lowered = text.lower()
    hits = []
    for label, tokens in DETAIL_KEYWORDS.items():
        if any(token.lower() in lowered for token in tokens):
            hits.append(label)
    return hits


def answer_quality_diagnostics(case: dict, answer: str, abstention: bool) -> dict:
    """Deterministic quality flags that do not depend on an LLM judge.

    These are report/audit signals, not EDD score inputs. They catch cases
    where the binary abstention metric is correct but the answer still gives
    too much premature detail.
    """
    empty = {
        "issues": [],
        "post_refusal_tail_chars": 0,
        "post_refusal_bullet_count": 0,
        "detail_keyword_hits": [],
        "answer_chars": len(answer or ""),
        "answer_line_count": 0,
    }

    text = (answer or "").strip()
    if not text:
        return empty

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    tail_lines = lines[1:] if len(lines) > 1 else []
    tail_text = "\n".join(tail_lines)
    bullet_count = _bulletish_line_count(tail_lines)
    keyword_hits = _detail_keyword_hits(tail_text)
    issues: list[str] = []

    if case.get("type") == "single_extract_plain_language" and not abstention:
        if len(text) > 1000 or len(lines) > 18 or _bulletish_line_count(lines) >= 14:
            issues.append("plain_language_answer_over_structured")

    if not case.get("expect_abstention") or not abstention:
        return {
            "issues": issues,
            "post_refusal_tail_chars": 0,
            "post_refusal_bullet_count": 0,
            "detail_keyword_hits": [],
            "answer_chars": len(text),
            "answer_line_count": len(lines),
        }

    if case.get("type") == "ambiguous_fragment_negative_control":
        if (
            len(tail_text) > 700
            or bullet_count >= 4
            or len(text) > 1400
            or (len(keyword_hits) >= 2 and len(tail_text) > 250)
        ):
            issues.append("ambiguous_identifier_refusal_with_excessive_candidate_summary")

    if case.get("type") in {"forbidden_info_trap", "sensitive_info_trap"}:
        if len(tail_text) > 350 or bullet_count >= 4:
            issues.append("sensitive_or_forbidden_refusal_with_detail_tail")

    if case.get("type") == "unsupported_award_result_trap" and abstention:
        if len(tail_text) > 450 or bullet_count >= 4:
            issues.append("unsupported_result_refusal_with_excessive_detail_tail")

    if len(tail_text) > 1800 and bullet_count >= 6:
        issues.append("abstention_with_excessive_detail_after_refusal")

    return {
        "issues": issues,
        "post_refusal_tail_chars": len(tail_text),
        "post_refusal_bullet_count": bullet_count,
        "detail_keyword_hits": keyword_hits,
        "answer_chars": len(text),
        "answer_line_count": len(lines),
    }


def answer_quality_issues(case: dict, answer: str, abstention: bool) -> list[str]:
    return answer_quality_diagnostics(case, answer, abstention)["issues"]


# ---------------------------------------------------------------------------
# LLM 심판 (참조 정답 없이 충실도/관련성 평가)
# ---------------------------------------------------------------------------
def _chat_json_with_trace(client, prompt, max_tokens=900, model: str | None = None) -> tuple[dict, list[dict]]:
    """JSON 응답을 최대한 견고하게 받아온다.
    - gpt-5 계열은 추론 토큰을 소모하므로 넉넉한 토큰 필요
    - response_format(json_object) 우선, 미지원 시 폴백 + 정규식 추출
    """
    kwargs = dict(model=model or config.CHAT_MODEL,
                  messages=[{"role": "user", "content": prompt}],
                  max_completion_tokens=max_tokens)
    started = time.time()
    try:
        resp = client.chat.completions.create(response_format={"type": "json_object"}, **kwargs)
    except Exception:
        resp = client.chat.completions.create(**kwargs)
    elapsed = time.time() - started
    trace = [traced_call(
        operation="judge",
        model=model or config.CHAT_MODEL,
        resp=resp,
        elapsed_sec=elapsed,
        meta={"max_tokens": max_tokens},
    )]
    content = (resp.choices[0].message.content or "").strip()
    try:
        return json.loads(content), trace
    except Exception:
        m = re.search(r"\{.*\}", content, re.S)
        return (json.loads(m.group(0)) if m else {}), trace


def _chat_json(client, prompt, max_tokens=900, model: str | None = None) -> dict:
    data, _trace = _chat_json_with_trace(client, prompt, max_tokens=max_tokens, model=model)
    return data


def _judge(query, context, answer):
    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    prompt = f"""다음은 RAG 시스템의 (질문 / 검색된 근거 / 답변)입니다.
아래 두 항목을 각각 0~5 정수로 채점하세요.
- groundedness: 답변이 '검색된 근거'에 의해 뒷받침되는 정도 (근거에 없는 내용을 지어내면 낮음)
- relevance: 답변이 '질문'에 실제로 답하는 정도
반드시 JSON 객체로만 답하세요: {{"groundedness": 0, "relevance": 0, "reason": "..."}}

[질문] {query}
[검색된 근거] {context[:config.JUDGE_CONTEXT_CHARS]}
[답변] {answer}"""
    try:
        data, usage_trace = _chat_json_with_trace(
            client,
            prompt,
            max_tokens=config.JUDGE_MAX_TOKENS,
            model=config.JUDGE_MODEL,
        )
        if not data:
            data = {"groundedness": None, "relevance": None, "reason": "judge_empty_or_unparsed"}
        return {
            "groundedness": data.get("groundedness"),
            "relevance": data.get("relevance"),
            "reason": data.get("reason", ""),
            "judge_model": config.JUDGE_MODEL,
            "usage_trace": usage_trace,
            "cost_usd": sum_cost(usage_trace),
        }
    except Exception as e:
        return {"groundedness": None, "relevance": None, "reason": f"judge실패: {e}", "judge_model": config.JUDGE_MODEL}


def _format_judge_context(chunks: list[dict]) -> str:
    """Give the judge a balanced view across retrieved chunks.

    A plain first-N-character slice can hide later retrieved organizations in
    compare/duplicate cases, making grounded answers look unsupported.
    """
    blocks = []
    per = max(200, config.JUDGE_CONTEXT_PER_CHUNK_CHARS)
    for i, chunk in enumerate(chunks, 1):
        meta = chunk.get("metadata") or {}
        text = " ".join((chunk.get("text") or "").split())
        blocks.append(
            f"[문서{i}] 사업명: {meta.get('사업명','')} / 발주기관: {meta.get('발주 기관','')}\n"
            f"{text[:per]}"
        )
    return "\n\n---\n\n".join(blocks)


# ---------------------------------------------------------------------------
# 평가 실행
# ---------------------------------------------------------------------------
def run_eval(
    params: dict | None = None,
    use_judge: bool = True,
    verbose: bool = True,
    case_ids: list[str] | None = None,
    case_limit: int | None = None,
    questions_path: str | None = None,
) -> dict:
    path = questions_path or QUESTIONS_PATH
    with open(path, encoding="utf-8") as f:
        cases = json.load(f)
    if case_ids:
        wanted = set(case_ids)
        cases = [c for c in cases if c["id"] in wanted]
    if case_limit is not None:
        cases = cases[:case_limit]

    details = []
    for case in cases:
        rag = RAGPipeline(params=params)
        result = None
        for turn in case["turns"]:          # 멀티턴은 순서대로, 마지막 턴을 평가
            result = rag.ask(turn)
        ctx = _format_judge_context(result["chunks"])

        cov = retrieval_coverage(result["retrieved_orgs"], case.get("target_orgs", []))
        rank = first_hit_rank(result["retrieved_orgs"], case.get("target_orgs", []))
        abstain = is_abstention(result["answer"])
        field_score = score_answer_fields(case, result["answer"])
        if field_score and not case.get("expect_abstention") and field_score.get("case_passed"):
            has_answer_field = any(
                row.get("expected_action") in {"answer", "answer_with_caveat", "separate_answer_and_refusal"}
                and row.get("passed")
                for row in field_score.get("field_rows", [])
            )
            if has_answer_field:
                abstain = False
        quality_diagnostics = answer_quality_diagnostics(case, result["answer"], abstain)

        rec = {
            "id": case["id"], "type": case["type"],
            "answer": result["answer"],
            "retrieved_orgs": result["retrieved_orgs"],
            "coverage": cov, "first_hit_rank": rank,
            "abstention": abstain,
            "expect_abstention": case.get("expect_abstention", False),
            "answer_quality_issues": quality_diagnostics["issues"],
            "answer_quality_diagnostics": quality_diagnostics,
            "field_score": field_score,
            "latency_sec": result["latency_sec"],
            "context_backfill_count": result.get("context_backfill_count", 0),
            "project_focus_filter_count": result.get("project_focus_filter_count", 0),
            "retrieval_sec": result.get("retrieval_sec"),
            "retrieval_usage_trace": result.get("retrieval_usage_trace", []),
            "retrieval_cost_usd": result.get("retrieval_cost_usd"),
            "generation_sec": result.get("generation_sec"),
            "generation_usage_trace": result.get("generation_usage_trace", []),
            "generation_cost_usd": result.get("generation_cost_usd"),
        }
        if use_judge and not case.get("expect_abstention"):
            rec["judge"] = _judge(case["turns"][-1], ctx, result["answer"])
        details.append(rec)
        if verbose:
            print(f"[{case['id']}] cov={cov} rank={rank} abstain={abstain} "
                  f"lat={result['latency_sec']}s")

    metrics = aggregate(details)
    return {
        "params": params or "default",
        "questions_path": path,
        "answer_model": config.CHAT_MODEL,
        "judge_model": config.JUDGE_MODEL if use_judge else None,
        "metrics": metrics,
        "details": details,
    }


def aggregate(details: list[dict]) -> dict:
    covs = [d["coverage"] for d in details if d["coverage"] is not None]
    ranks = [d["first_hit_rank"] for d in details if d["first_hit_rank"]]
    all_target = [d for d in details if d["coverage"] is not None]
    hit_all = [d for d in all_target if d["coverage"] == 1.0]
    gnd = [d["judge"]["groundedness"] for d in details if d.get("judge") and d["judge"].get("groundedness") is not None]
    rel = [d["judge"]["relevance"] for d in details if d.get("judge") and d["judge"].get("relevance") is not None]
    absten = [d for d in details if d["expect_abstention"]]
    absten_ok = [d for d in absten if d["abstention"]]
    non_absten = [d for d in details if not d["expect_abstention"]]
    false_absten = [d for d in non_absten if d["abstention"]]
    empty_answers = [d for d in details if not (d.get("answer") or "").strip()]
    lat = [d["latency_sec"] for d in details]

    def avg(x): return round(sum(x) / len(x), 3) if x else None
    return {
        "retrieval_coverage_avg": avg(covs),
        "hit_all_targets_rate": round(len(hit_all) / len(all_target), 3) if all_target else None,
        "mrr": round(sum(1 / r for r in ranks) / len(all_target), 3) if all_target else None,
        "groundedness_avg": avg(gnd),
        "relevance_avg": avg(rel),
        "abstention_accuracy": round(len(absten_ok) / len(absten), 3) if absten else None,
        "false_abstention_rate": round(len(false_absten) / len(non_absten), 3) if non_absten else None,
        "empty_answer_rate": round(len(empty_answers) / len(details), 3) if details else None,
        "latency_avg_sec": avg(lat),
    }


def main():
    if not config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY 없음. .env 를 먼저 설정하세요.")
        return
    from src.vectorstore import load_index
    cnt = load_index().count()
    if cnt == 0:
        print("❌ 인덱스가 비어 있습니다! 먼저 build_index 를 성공적으로 실행하세요.")
        return
    print(f"평가 시작 (인덱스 {cnt}개 청크)...\n")
    out = run_eval()
    print("\n=== 집계 지표 ===")
    for k, v in out["metrics"].items():
        print(f"  {k}: {v}")

    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, f"eval_{datetime.now():%Y%m%d_%H%M%S}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\n상세 저장: {path}")


if __name__ == "__main__":
    main()
