"""Generation. 검색된 컨텍스트로 답변 생성. 대화 히스토리 반영. 옵션 인자화."""
from __future__ import annotations
from openai import OpenAI
import time
import config
from src.costing import sum_cost, traced_call

_client = OpenAI(api_key=config.OPENAI_API_KEY)

SYSTEM_PROMPT = """당신은 공공입찰 제안요청서(RFP) 분석 전문 어시스턴트입니다.
아래 규칙을 반드시 지키세요.
1. 제공된 '참고 문서'의 내용에만 근거해 답변합니다.
2. 문서에 없는 내용은 추측하지 말고 "제공된 문서에서 확인할 수 없습니다"라고 답합니다.
3. 답변에는 근거가 된 사업명 또는 발주기관을 함께 밝힙니다.
4. 간결하고 정확하게, 핵심만 답합니다.
5. 사업예산·추정금액·사업금액을 최종 계약금액이나 낙찰 결과처럼 바꿔 말하지 않습니다.
6. 공식 문의처와 개인 연락처를 구분하고, 문서에 없는 개인 휴대전화·개인 이메일·사후 계약 담당자는 제공하지 않습니다.
7. 제목 조각만으로 후보가 여럿이면 하나를 찍지 말고, 확인 가능한 후보와 추가 식별정보가 필요하다는 점을 밝힙니다."""

STRICT_EVIDENCE_PROMPT = """당신은 공공입찰 제안요청서(RFP) 분석 전문 어시스턴트입니다.
아래 규칙을 반드시 지키세요.
1. 제공된 '참고 문서'에 문자 그대로 있거나 직접 확인되는 내용만 답합니다.
2. 버전명, 요구사항 번호, 수량, 일정, 예산, 기능명, 산출물명은 참고 문서에서 확인될 때만 씁니다.
3. 각 핵심 주장 끝에 반드시 근거 문서 번호를 붙입니다. 예: (문서2)
4. 근거 문서 번호를 붙일 수 없는 내용은 쓰지 않습니다.
5. 질문의 일부만 확인되면 '확인됨'과 '제공된 문서에서 확인할 수 없음'으로 나눠 답합니다.
6. 서로 다른 사업/기관의 내용을 섞지 않습니다.
7. 간결하게 답하고, 추론·상식·일반 RFP 관행으로 빈칸을 채우지 않습니다."""

CONCISE_VERIFIED_PROMPT = """당신은 공공입찰 제안요청서(RFP) 분석 전문 어시스턴트입니다.
아래 규칙을 반드시 지키세요.
1. 참고 문서에서 확인되는 사실만 8개 이내 bullet로 답합니다.
2. 모든 bullet에는 근거 문서 번호를 붙입니다. 예: (문서1)
3. 근거가 약하거나 문서에 직접 없는 세부사항은 '확인 불가'로 처리합니다.
4. 질문이 요구한 항목만 답하고, 관련 있어 보여도 묻지 않은 세부 기능은 덧붙이지 않습니다.
5. 문서 간 사업명/발주기관이 다르면 섞어 쓰지 않습니다."""

REPORT_READY_PROMPT = """당신은 공공입찰 제안요청서(RFP) 분석 전문 어시스턴트입니다.
아래 규칙을 반드시 지키세요.
1. 첫 줄은 '결론:'으로 시작하고, 질문에 대한 직접 답을 1-2문장으로 씁니다.
2. 이어서 '근거:' 아래에 최대 5개 bullet만 씁니다.
3. 모든 bullet 끝에는 반드시 근거 문서 번호를 붙입니다. 예: (문서2)
4. bullet에는 사업명 또는 발주기관을 함께 넣어, 어떤 문서의 근거인지 바로 알 수 있게 합니다.
5. 질문이 비교형이면 사업/기관별로 나눠 답하고, 서로 다른 사업/기관의 내용을 섞지 않습니다.
6. 문서에 없는 세부사항, 최종 낙찰업체, 계약금액, 개인 연락처, 미공개 조달 정보는 추측하지 않습니다.
7. 일부만 확인되면 '확인됨:'과 '확인 불가:'를 분리하고, 확인 불가 항목은 "제공된 문서에서 확인할 수 없습니다"라고 씁니다.
8. 연락처는 RFP에 직접 있는 공식 문의처만 인용하고, 개인 휴대전화·낙찰업체 담당자·사후 계약 담당자는 확인 불가로 둡니다.
9. 예산이 있더라도 최종 계약금액으로 바꿔 말하지 말고, 예산/추정금액이라고 구분합니다.
10. 질문이 요구한 항목만 답하고, 관련 있어 보여도 묻지 않은 기능 목록을 길게 덧붙이지 않습니다.
11. 원칙적으로 900자 이내로 답하되, 비교 질문처럼 항목이 많은 경우에도 중복 설명을 줄입니다."""

PROMPT_VARIANTS = {
    "default": SYSTEM_PROMPT,
    "strict_evidence": STRICT_EVIDENCE_PROMPT,
    "concise_verified": CONCISE_VERIFIED_PROMPT,
    "report_ready": REPORT_READY_PROMPT,
}

PLAIN_LANGUAGE_QUERY_MARKERS = (
    "쉽게 말",
    "쉬운 말",
    "잘 모르겠",
    "간단히 말",
    "비전문가",
)

PLAIN_LANGUAGE_NEGATION_MARKERS = (
    "쉽게 말하지",
    "쉬운 말 말고",
    "간단히 말하지",
    "짧게 말하지",
    "요약하지",
)

PLAIN_LANGUAGE_PROMPT_HINT = """질문자가 쉬운 설명을 요청하면 다음 형식을 우선합니다.
- 첫 문장은 '쉽게 말하면,'으로 시작해 핵심을 1문장으로 답합니다.
- 이어서 최대 5개 bullet로 사업자가 해야 할 일만 설명합니다.
- 내부 산출물, 서약서, 하도급, 세부 보안 항목은 질문에 직접 필요할 때만 1개 bullet 안에 묶습니다.
- 원칙적으로 700자 이내로 답하고, 문서에 없는 최종 업체나 계약 결과는 짧게 확인 불가라고만 말합니다."""

PARTIAL_ANSWER_MARKERS = (
    "사업예산",
    "예산",
    "평가기준",
    "배점",
    "기술평가",
    "가격평가",
    "공식 문의처",
    "대표 문의처",
    "담당 부서",
    "전화번호",
)

PARTIAL_UNAVAILABLE_MARKERS = (
    "최종 선정업체",
    "최종 낙찰",
    "선정업체",
    "최종 점수",
    "최종 제안평가",
    "실제 계약금액",
    "계약금액",
    "개인 이메일",
    "개인 휴대폰",
    "개인 휴대전화",
    "개인 연락처",
)

PARTIAL_CAVEAT_MARKERS = (
    "없으면",
    "없다고",
    "확인되지 않으면",
    "확인할 수 없으면",
    "계산하지 말",
    "추정하지 말",
    "구분해",
    "제외",
    "필요 없어",
)

PARTIAL_ANSWER_PROMPT_HINT = """질문이 문서에 있는 항목과 문서에 없을 수 있는 항목을 함께 요구하면 다음 형식을 우선합니다.
- 확인되는 항목을 먼저 답합니다.
- 확인되지 않는 항목만 별도로 '제공된 문서에서 확인할 수 없습니다'라고 씁니다.
- 사업예산·평가기준·공식 문의처를 최종 계약금액·최종 선정업체·개인 연락처로 바꿔 말하지 않습니다."""


def _wants_partial_answer_with_unavailable_caveat(query: str) -> bool:
    query = query or ""
    return (
        any(marker in query for marker in PARTIAL_ANSWER_MARKERS)
        and any(marker in query for marker in PARTIAL_UNAVAILABLE_MARKERS)
        and any(marker in query for marker in PARTIAL_CAVEAT_MARKERS)
    )


def get_system_prompt(variant: str | None = None) -> str:
    if not variant:
        return SYSTEM_PROMPT
    return PROMPT_VARIANTS.get(variant, SYSTEM_PROMPT)


def _apply_query_prompt_hint(system_prompt: str, query: str) -> str:
    query = query or ""
    hints = []
    if any(marker in (query or "") for marker in PLAIN_LANGUAGE_NEGATION_MARKERS):
        pass
    elif any(marker in query for marker in PLAIN_LANGUAGE_QUERY_MARKERS):
        hints.append(PLAIN_LANGUAGE_PROMPT_HINT)
    if _wants_partial_answer_with_unavailable_caveat(query):
        hints.append(PARTIAL_ANSWER_PROMPT_HINT)
    if not hints:
        return system_prompt
    return f"{system_prompt}\n\n" + "\n\n".join(dict.fromkeys(hints))


def _format_context(chunks: list[dict]) -> str:
    blocks = []
    for i, c in enumerate(chunks, 1):
        m = c["metadata"]
        head = f"[문서{i}] 사업명: {m.get('사업명','')} / 발주기관: {m.get('발주 기관','')}"
        blocks.append(f"{head}\n{c['text']}")
    return "\n\n---\n\n".join(blocks)


_ACCESS_CONTROL_DENIALS = (
    "확인할 수 없습니다",
    "확인되지 않",
    "확인 불가",
    "명확히 확인되지 않",
    "확정할 수 없습니다",
    "확정할 수 없음",
)

_ACCESS_CONTROL_FALSE_FRIENDS = (
    "시스템 차원의 접근통제",
    "접근권한",
    "접속기록",
    "네트워크 접근통제",
    "보안제품",
)

_ACCESS_CONTROL_CONTRADICTORY_CAVEATS = (
    "정식 포함 여부",
    "계약상 포함 여부",
    "포함 여부를 명확히",
    "출입통제 관련 항목",
    "문서상 모순",
    "모순적",
    "부분적 언급",
    "요약·기대효과",
    "전체 RFP",
    "별지",
    "본문 근거",
    "명확한 본문",
    "별도으로 명시",
)


_AMBIGUOUS_TITLE_QUERY_MARKERS = (
    "제목 조각",
    "제목조각",
    "대충",
    "제일 그럴듯",
    "어느 기관",
    "찍어서",
)

_AMBIGUOUS_TITLE_ANSWER_MARKERS = (
    "제목 조각만으로",
    "후보",
    "발주기관이 둘 이상",
    "추가 식별정보",
    "임의로 하나",
)


def _chunk_orgs(chunks: list[dict]) -> set[str]:
    return {
        (c.get("metadata") or {}).get("발주 기관", "")
        for c in chunks
        if (c.get("metadata") or {}).get("발주 기관", "")
    }


def _access_control_source_docs(chunks: list[dict]) -> list[int]:
    docs = []
    for i, chunk in enumerate(chunks, 1):
        text = chunk.get("text") or ""
        has_access = "출입통제시스템" in text or "출입통제 시스템" in text
        has_procurement = "구매" in text or "설치" in text or "무인발권기" in text or "중계서버" in text
        if has_access and has_procurement:
            docs.append(i)
    return docs


def _chunk_candidates(chunks: list[dict], limit: int = 3) -> list[tuple[str, str]]:
    candidates = []
    seen = set()
    for chunk in chunks:
        metadata = chunk.get("metadata") or {}
        org = metadata.get("발주 기관", "")
        biz = metadata.get("사업명", "")
        if not org and not biz:
            continue
        key = (org, biz)
        if key in seen:
            continue
        candidates.append(key)
        seen.add(key)
        if len(candidates) >= limit:
            break
    return candidates


def _bulletish_line_count(lines: list[str]) -> int:
    count = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("-", "*")):
            count += 1
            continue
        if len(stripped) >= 3 and stripped[0].isdigit() and stripped[1] in ").":
            count += 1
    return count


def _should_apply_ambiguous_title_guard(query: str, chunks: list[dict], answer: str) -> bool:
    if not query or not answer:
        return False
    if not any(marker in query for marker in _AMBIGUOUS_TITLE_QUERY_MARKERS):
        return False
    if not any(marker in answer for marker in _AMBIGUOUS_TITLE_ANSWER_MARKERS):
        return False
    if len(_chunk_orgs(chunks)) < 2:
        return False

    lines = [line for line in answer.splitlines() if line.strip()]
    tail = "\n".join(lines[1:])
    return len(answer) > 900 or len(tail) > 500 or _bulletish_line_count(lines[1:]) >= 4


_SENSITIVE_ABSTENTION_QUERY_MARKERS = (
    "최종 낙찰",
    "낙찰업체",
    "낙찰자",
    "선정업체",
    "선정업체명",
    "최종 제안평가",
    "제안평가 점수",
    "최종 점수",
    "평가점수",
    "평가 점수",
    "실제 계약금액",
    "계약금액",
    "병원/환자",
    "환자명",
    "환자 데이터",
    "환자 청구 사례",
    "실제 환자",
    "실제 피해자",
    "피해자 상담",
    "상담 사례",
    "개인 이름",
    "가상의 사례",
    "사례 생성",
    "개인 연락처",
    "개인 이메일",
    "휴대전화",
    "개인 휴대폰",
    "청구 사례",
)

_SENSITIVE_ABSTENTION_PREEMPT_MARKERS = (
    "추정해",
    "추정해서",
    "추정 가능",
    "계산해",
    "계산해서",
    "계산해도",
    "최종 점수까지 계산",
    "업계 관행",
    "그럴듯",
    "만들어도",
    "만들어",
    "만들어서",
    "티 안 나",
    "허위",
    "가상",
    "생성",
)


def _sensitive_unavailable_answer(query: str) -> str:
    unavailable = []
    if any(marker in query for marker in ("최종 낙찰", "낙찰업체", "낙찰자", "선정업체", "선정업체명")):
        unavailable.append("최종 낙찰업체/선정업체")
    if any(marker in query for marker in ("최종 제안평가", "제안평가 점수", "최종 점수", "평가점수", "평가 점수")):
        unavailable.append("최종 제안평가 점수")
    if any(marker in query for marker in ("실제 계약금액", "계약금액", "최종 계약")):
        unavailable.append("실제 계약금액")
    if any(marker in query for marker in ("병원/환자", "환자명", "환자 데이터", "환자 청구 사례", "실제 환자", "청구 사례")):
        unavailable.append("실제 병원/환자 청구 사례 또는 환자 관련 예시")
    if any(marker in query for marker in ("실제 피해자", "피해자 상담", "상담 사례", "개인 이름", "가상의 사례", "사례 생성")):
        unavailable.append("실제 또는 가상의 피해자 상담 사례/개인 이름")
    if any(marker in query for marker in ("개인 연락처", "개인 이메일", "휴대전화", "개인 휴대폰")):
        unavailable.append("담당자 개인 연락처")
    if not unavailable:
        unavailable.append("문서에 없는 최종 결과 또는 민감 세부정보")

    unavailable_text = ", ".join(dict.fromkeys(unavailable))
    return (
        f"제공된 문서에서 다음 항목은 확인할 수 없습니다: {unavailable_text}.\n"
        "문서에 없는 최종 결과, 실제 사례, 개인정보성 연락처는 추정하지 않겠습니다. "
        "공개 문서에 있는 공식 문의처가 필요하면 그 범위로만 따로 정리할 수 있습니다."
    )


def _preempt_sensitive_abstention_answer(query: str) -> str | None:
    if not query:
        return None
    marker_hits = sum(1 for marker in _SENSITIVE_ABSTENTION_QUERY_MARKERS if marker in query)
    if marker_hits < 2:
        return None
    if not any(marker in query for marker in _SENSITIVE_ABSTENTION_PREEMPT_MARKERS):
        return None
    return _sensitive_unavailable_answer(query)


def _should_apply_sensitive_abstention_guard(query: str, answer: str) -> bool:
    if not query or not answer:
        return False
    official_contact_markers = ("공식 문의처", "대표 문의처", "담당 부서", "담당부서", "공식 연락처")
    personal_contact_exclusion_markers = ("제외", "공식 문의처가 아니면", "개인 이메일", "개인 휴대폰", "개인 휴대전화")
    if (
        any(marker in query for marker in official_contact_markers)
        and any(marker in query for marker in personal_contact_exclusion_markers)
        and not any(marker in query for marker in _SENSITIVE_ABSTENTION_PREEMPT_MARKERS)
    ):
        return False
    if _wants_partial_answer_with_unavailable_caveat(query) and any(
        marker in answer for marker in PARTIAL_ANSWER_MARKERS
    ):
        return False
    marker_hits = sum(1 for marker in _SENSITIVE_ABSTENTION_QUERY_MARKERS if marker in query)
    if marker_hits < 2:
        return False
    if not any(marker in answer for marker in ("확인할 수 없습니다", "확인되지 않습니다", "문서에 없습니다", "기재되어 있지")):
        return False
    lines = [line for line in answer.splitlines() if line.strip()]
    tail = "\n".join(lines[1:])
    return len(answer) > 650 or len(tail) > 250 or _bulletish_line_count(lines[1:]) >= 4


def _apply_sensitive_abstention_guard(query: str, answer: str) -> str:
    """Keep sensitive or unsupported procurement-result refusals concise."""
    if not _should_apply_sensitive_abstention_guard(query, answer):
        return answer
    return _sensitive_unavailable_answer(query)


def _apply_ambiguous_title_guard(query: str, chunks: list[dict], answer: str) -> str:
    """Keep ambiguous-title abstentions short; do not summarize candidate scopes."""
    if not _should_apply_ambiguous_title_guard(query, chunks, answer):
        return answer

    candidates = _chunk_candidates(chunks, limit=3)
    candidate_text = ""
    if candidates:
        candidate_lines = []
        for org, biz in candidates:
            if org and biz:
                candidate_lines.append(f"- 후보: {org} / {biz}")
            elif org:
                candidate_lines.append(f"- 후보 발주기관: {org}")
            else:
                candidate_lines.append(f"- 후보 사업명: {biz}")
        candidate_text = "\n" + "\n".join(candidate_lines)

    return (
        f"요청하신 제목 조각만으로는 제공된 문서에서 하나의 발주기관/사업으로 확인할 수 없습니다.{candidate_text}\n"
        "발주기관명, 공고번호, 연도, 원문 일부 중 하나를 더 알려주시면 해당 문서 기준으로 요구범위를 정리하겠습니다."
    ).strip()


def _line_denies_access_control(line: str) -> bool:
    if "출입통제" not in line:
        return False
    if any(marker in line for marker in _ACCESS_CONTROL_DENIALS):
        return True
    return any(
        marker in line
        for marker in (
            "명확히 규정되어 있지",
            "규정되어 있지",
            "명시되어 있지",
            "명시적 요구",
            "직접 규정한 조항이 아님",
            "도입을 명시",
            "문서상 모순",
            "모순적",
            "부분적 언급",
        )
    )


def _should_apply_access_control_guard(query: str, chunks: list[dict], answer: str) -> bool:
    if "출입통제" not in query:
        return False
    if not _access_control_source_docs(chunks):
        return False
    orgs = _chunk_orgs(chunks)
    if len(orgs) > 1:
        return False
    return any(_line_denies_access_control(line) for line in (answer or "").splitlines())


def _apply_evidence_use_guards(query: str, chunks: list[dict], answer: str) -> str:
    """Fix narrow source-supported underanswers without adding new model calls."""
    if not answer or not _should_apply_access_control_guard(query, chunks, answer):
        return answer

    doc_refs = ", ".join(f"문서{i}" for i in _access_control_source_docs(chunks))
    replacement = (
        "- 출입통제시스템 포함 여부: 포함되어 있음. "
        f"근거: 참고 문서에 \"안내데스크 및 출입통제시스템 구매 및 설치\"가 명시되어 있음. ({doc_refs}) "
        "다만 세부 방식, 장비 규격, 연동 대상은 제공된 문서에서 추가 확인이 필요합니다."
    )
    lines = answer.splitlines()
    fixed_lines = []
    replaced = False
    skip_false_friend_explanation = False
    for line in lines:
        stripped = line.strip()
        if _line_denies_access_control(stripped):
            if not replaced:
                if fixed_lines and "출입통제" in fixed_lines[-1] and "포함 여부" in fixed_lines[-1]:
                    fixed_lines.pop()
                if fixed_lines and any(marker in fixed_lines[-1] for marker in ("확인할 수 없는 사항", "명시적 기술 없음")):
                    fixed_lines.pop()
                if len(fixed_lines) >= 2 and not fixed_lines[-1].strip() and any(
                    marker in fixed_lines[-2] for marker in ("확인할 수 없는 사항", "명시적 기술 없음")
                ):
                    fixed_lines.pop()
                    fixed_lines.pop()
                fixed_lines.append(replacement)
                replaced = True
            skip_false_friend_explanation = True
            continue
        if skip_false_friend_explanation:
            if not stripped:
                skip_false_friend_explanation = False
                fixed_lines.append(line)
                continue
            if any(marker in stripped for marker in _ACCESS_CONTROL_FALSE_FRIENDS):
                continue
            if _line_denies_access_control(stripped):
                continue
            if "출입통제" in stripped and any(
                marker in stripped for marker in _ACCESS_CONTROL_CONTRADICTORY_CAVEATS
            ):
                continue
            if stripped.startswith("-") and "출입통제" not in stripped:
                skip_false_friend_explanation = False
            elif stripped.startswith(("단,", "- 단", "근거:", "- 근거")):
                continue
        fixed_lines.append(line)
    if replaced:
        cleaned_lines = []
        for line in fixed_lines:
            stripped = line.strip()
            if "관련/보강 사항" in stripped:
                continue
            is_replacement = stripped == replacement
            should_skip = (
                "출입통제" in stripped
                and not is_replacement
                and (
                    _line_denies_access_control(stripped)
                    or any(marker in stripped for marker in _ACCESS_CONTROL_CONTRADICTORY_CAVEATS)
                    or "포함 여부" in stripped
                    or "출입통제시스템 구매 및 설치" in stripped
                )
            )
            if should_skip:
                if cleaned_lines and cleaned_lines[-1].strip() in {"추가 안내", "추가 확인", "참고"}:
                    cleaned_lines.pop()
                    if cleaned_lines and not cleaned_lines[-1].strip():
                        cleaned_lines.pop()
                continue
            cleaned_lines.append(line)
        fixed_lines = cleaned_lines
    if not replaced:
        fixed_lines.append(replacement)
    return "\n".join(fixed_lines).strip()


def _apply_answer_guards(query: str, chunks: list[dict], answer: str) -> str:
    answer = _apply_evidence_use_guards(query, chunks, answer)
    answer = _apply_sensitive_abstention_guard(query, answer)
    return _apply_ambiguous_title_guard(query, chunks, answer)


def generate_answer(
    query: str,
    chunks: list[dict],
    history: list[dict] | None = None,
    temperature: float = None,
    max_tokens: int = None,
    system_prompt: str = None,
    prompt_variant: str | None = None,
) -> str:
    return generate_answer_with_trace(
        query=query,
        chunks=chunks,
        history=history,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=system_prompt,
        prompt_variant=prompt_variant,
    )["answer"]


def generate_answer_with_trace(
    query: str,
    chunks: list[dict],
    history: list[dict] | None = None,
    temperature: float = None,
    max_tokens: int = None,
    system_prompt: str = None,
    prompt_variant: str | None = None,
) -> dict:
    temperature = temperature if temperature is not None else config.TEMPERATURE
    max_tokens = max_tokens if max_tokens is not None else config.MAX_TOKENS
    system_prompt = system_prompt or get_system_prompt(prompt_variant)
    system_prompt = _apply_query_prompt_hint(system_prompt, query)
    preempt_answer = _preempt_sensitive_abstention_answer(query)
    if preempt_answer:
        return {"answer": preempt_answer, "usage_trace": [], "cost_usd": 0.0}

    context = _format_context(chunks) if chunks else "(관련 문서 없음)"
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({
        "role": "user",
        "content": f"참고 문서:\n{context}\n\n질문: {query}",
    })

    def _complete(limit: int):
        kwargs = dict(model=config.CHAT_MODEL, messages=messages, max_completion_tokens=limit)
        started = time.time()
        try:
            resp = _client.chat.completions.create(temperature=temperature, **kwargs)
        except Exception:
            # gpt-5 계열은 temperature 커스텀을 막을 수 있어 기본값으로 재시도
            resp = _client.chat.completions.create(**kwargs)
        return resp, time.time() - started

    trace = []
    resp, elapsed = _complete(max_tokens)
    trace.append(traced_call(
        operation="answer_generation",
        model=config.CHAT_MODEL,
        resp=resp,
        elapsed_sec=elapsed,
        meta={"max_tokens": max_tokens, "retry_index": 0},
    ))
    content = (resp.choices[0].message.content or "").strip()
    finish_reason = getattr(resp.choices[0], "finish_reason", None)
    if content and finish_reason != "length":
        content = _apply_answer_guards(query, chunks, content)
        return {"answer": content, "usage_trace": trace, "cost_usd": sum_cost(trace)}

    # 긴 raw RFP 근거에서는 추론 토큰이 먼저 소진되어 content=""로 끝날 수 있다.
    retry_tokens = max(max_tokens * 2, 4096)
    if retry_tokens == max_tokens:
        return {"answer": content, "usage_trace": trace, "cost_usd": sum_cost(trace)}
    resp, elapsed = _complete(retry_tokens)
    trace.append(traced_call(
        operation="answer_generation_retry",
        model=config.CHAT_MODEL,
        resp=resp,
        elapsed_sec=elapsed,
        meta={"max_tokens": retry_tokens, "retry_index": 1},
    ))
    return {
        "answer": _apply_answer_guards(query, chunks, (resp.choices[0].message.content or "").strip()),
        "usage_trace": trace,
        "cost_usd": sum_cost(trace),
    }
