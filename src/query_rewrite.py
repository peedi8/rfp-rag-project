"""후속질문 쿼리 재작성(condense question).

멀티턴 대화에서 후속 질문은 대명사/생략이 많아("그럼 그건?", "더 자세히") 그 자체로는
검색이 안 된다. 이전 대화를 반영해 '혼자서도 검색 가능한' 독립 질문으로 바꾼다.
예) 히스토리(국민연금 이러닝) + "콘텐츠 개발 관리 더 알려줘"
    → "국민연금공단 이러닝시스템 사업의 콘텐츠 개발·관리 요구사항"
"""
from __future__ import annotations
from openai import OpenAI
import config

_client = OpenAI(api_key=config.OPENAI_API_KEY)


def rewrite_query(history: list[dict], query: str) -> str:
    """history가 있으면 독립 질문으로 재작성해 반환. 없거나 실패 시 원본 그대로."""
    if not history:
        return query
    # 최근 몇 턴만 사용
    convo = "\n".join(
        f"{'사용자' if m['role']=='user' else '어시스턴트'}: {m['content'][:300]}"
        for m in history[-4:]
    )
    prompt = (
        "다음 대화 맥락을 참고하여, 마지막 후속 질문을 '문맥 없이도 검색 가능한' "
        "완전한 독립 질문으로 다시 써 주세요. 발주기관·사업명 등 핵심 대상을 명시적으로 포함하세요. "
        "재작성한 질문 문장만 출력하세요.\n\n"
        f"[대화]\n{convo}\n\n[후속 질문] {query}\n\n[독립 질문]"
    )
    try:
        resp = _client.chat.completions.create(
            model=config.CHAT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=600,   # gpt-5 계열 추론 토큰 여유 (짧은 출력이라도 넉넉히)
        )
        out = (resp.choices[0].message.content or "").strip()
        return out if out else query
    except Exception:
        return query
