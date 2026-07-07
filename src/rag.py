"""RAG 파이프라인 통합. Retrieval → Generation + 대화 히스토리 관리.

params(dict)로 실험 설정을 넘길 수 있다. 예:
    {"top_k":5, "use_mmr":True, "mmr_lambda":0.5, "rerank":False, "auto_filter":False}
"""
from __future__ import annotations
import csv
import difflib
import re
import time
import config
from src.retriever import retrieve
from src.generator import generate_answer_with_trace
from src.query_rewrite import rewrite_query
from src.costing import sum_cost

DEFAULT_PARAMS = {
    "top_k": config.TOP_K,
    "use_mmr": config.USE_MMR,
    "mmr_lambda": config.MMR_LAMBDA,
    "fetch_k": config.FETCH_K,
    "auto_filter": config.AUTO_FILTER,
    "rerank": config.RERANK,
    "rewrite_query": config.REWRITE_QUERY,
    "adaptive_top_k": False,
    "prompt_variant": "default",
}


_DETAIL_HEAVY_TERMS = ("예약", "결제", "PG", "회원", "키오스크", "발권", "매출", "환불")
_FACILITY_TERMS = ("체육관", "센터", "시설", "배드민턴", "탁구", "예약시스템", "통합예약")
_CSV_BACKFILL_QUERY_TERMS = ("출입통제", "무인발권", "중계서버", "안내데스크")
_CSV_BACKFILL_SOURCE_TERMS = ("출입통제시스템", "무인발권기", "중계서버", "안내데스크")
_TITLE_STOPWORDS = {
    "2024",
    "2024년",
    "2025",
    "2025년",
    "시스템",
    "정보시스템",
    "통합정보시스템",
    "사업",
    "용역",
    "구축",
    "고도화",
    "기능개선",
    "운영",
    "관리",
    "운영관리",
}


def _effective_top_k(search_query: str, original_query: str, params: dict) -> int:
    """Optionally keep detail-heavy facility questions at top8.

    L9/L10 showed that qv3_010 is source-clean at top5 but still misses PG
    detail, while top8 recovers PG/발권/매출. This opt-in guard lets speed
    experiments use top5 for simple questions without shrinking complex
    reservation/payment facility questions.
    """
    top_k = int(params.get("top_k", config.TOP_K))
    if not params.get("adaptive_top_k"):
        return top_k
    q = f"{search_query} {original_query}"
    detail_hits = sum(1 for term in _DETAIL_HEAVY_TERMS if term in q)
    facility_hit = any(term in q for term in _FACILITY_TERMS)
    if facility_hit and detail_hits >= 2:
        return max(top_k, 8)
    return top_k


def _compact(text: str) -> str:
    return "".join(str(text or "").split()).lower()


def _single_retrieved_org(chunks: list[dict]) -> str:
    orgs = {
        (chunk.get("metadata") or {}).get("발주 기관", "")
        for chunk in chunks
        if (chunk.get("metadata") or {}).get("발주 기관", "")
    }
    return next(iter(orgs)) if len(orgs) == 1 else ""


def _retrieved_titles(chunks: list[dict]) -> list[str]:
    titles = []
    for chunk in chunks:
        title = (chunk.get("metadata") or {}).get("사업명", "")
        if title and title not in titles:
            titles.append(title)
    return titles


def _title_tokens(title: str) -> list[str]:
    tokens = []
    for token in re.findall(r"[A-Za-z0-9가-힣]+", title or ""):
        token = token.strip()
        if len(token) < 2:
            continue
        if token in _TITLE_STOPWORDS:
            continue
        if token.isdigit():
            continue
        tokens.append(token)
    return tokens


def _title_query_score(title: str, query: str) -> float:
    compact_query = _compact(query)
    compact_title = _compact(title)
    if not compact_title or not compact_query:
        return 0.0

    score = 0.0
    for token in _title_tokens(title):
        compact_token = _compact(token)
        if compact_token and compact_token in compact_query:
            score += 2.0 if re.fullmatch(r"[A-Za-z0-9]+", token) else 1.0

    match = difflib.SequenceMatcher(None, compact_title, compact_query).find_longest_match(
        0, len(compact_title), 0, len(compact_query)
    )
    if match.size >= 8:
        score += min(2.0, match.size / 8)
    return score


def _single_project_focus_filter(query: str, chunks: list[dict]) -> list[dict]:
    """Drop same-issuer but different-project chunks when one title is clearly intended."""
    if not chunks or not _single_retrieved_org(chunks):
        return chunks

    titles = _retrieved_titles(chunks)
    if len(titles) < 2:
        return chunks

    scored = sorted(
        ((title, _title_query_score(title, query)) for title in titles),
        key=lambda item: item[1],
        reverse=True,
    )
    best_title, best_score = scored[0]
    second_score = scored[1][1] if len(scored) > 1 else 0.0
    if best_score < 2.0 or best_score - second_score < 1.5:
        return chunks

    focused = [
        chunk
        for chunk in chunks
        if (chunk.get("metadata") or {}).get("사업명", "") == best_title
    ]
    return focused or chunks


def _title_matches(candidate: str, titles: list[str]) -> bool:
    cand = _compact(candidate)
    if not cand:
        return False
    for title in titles:
        got = _compact(title)
        if not got:
            continue
        if cand in got or got in cand:
            return True
        if difflib.SequenceMatcher(None, cand, got).ratio() >= 0.82:
            return True
    return False


def _has_source_term(chunks: list[dict]) -> bool:
    return any(
        any(term in (chunk.get("text") or "") for term in _CSV_BACKFILL_SOURCE_TERMS)
        for chunk in chunks
    )


def _csv_summary_backfill(query: str, chunks: list[dict]) -> list[dict]:
    """Append a target-bound CSV summary row when raw chunks miss summary evidence."""
    if not chunks or not any(term in query for term in _CSV_BACKFILL_QUERY_TERMS):
        return chunks
    if _has_source_term(chunks):
        return chunks
    org = _single_retrieved_org(chunks)
    if not org:
        return chunks
    titles = _retrieved_titles(chunks)
    if not titles:
        return chunks

    try:
        with config.CSV_PATH.open("r", encoding="utf-8-sig", errors="ignore", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row.get("발주 기관") or "") != org:
                    continue
                if not _title_matches(row.get("사업명") or "", titles):
                    continue
                summary = row.get("사업 요약") or ""
                if not any(term in summary for term in _CSV_BACKFILL_SOURCE_TERMS):
                    continue
                meta = {key: row.get(key, "") for key in ("사업명", "발주 기관", "공고 번호", "파일명")}
                meta["source_type"] = "csv_summary_backfill"
                return [
                    *chunks,
                    {
                        "text": f"[CSV 사업 요약 보강]\n{summary}",
                        "metadata": meta,
                    },
                ]
    except OSError:
        return chunks
    return chunks


class RAGPipeline:
    def __init__(self, params: dict | None = None):
        self.history: list[dict] = []
        self.params = {**DEFAULT_PARAMS, **(params or {})}

    def ask(self, query: str, where: dict | None = None, use_history: bool = True) -> dict:
        t0 = time.time()
        # 후속질문이면 대화 맥락을 반영해 검색용 독립 질문으로 재작성
        search_query = query
        if self.params.get("rewrite_query") and use_history and self.history:
            search_query = rewrite_query(self.history, query)
        effective_top_k = _effective_top_k(search_query, query, self.params)
        retrieval_trace = []
        chunks = retrieve(
            search_query, where=where,
            top_k=effective_top_k, use_mmr=self.params["use_mmr"],
            mmr_lambda=self.params["mmr_lambda"], fetch_k=self.params["fetch_k"],
            auto_filter=self.params["auto_filter"], rerank=self.params["rerank"],
            trace=retrieval_trace,
        )
        before_focus_count = len(chunks)
        chunks = _single_project_focus_filter(f"{search_query} {query}", chunks)
        project_focus_filter_count = before_focus_count - len(chunks)
        chunks = _csv_summary_backfill(f"{search_query} {query}", chunks)
        t_ret = time.time()
        hist = self.history if use_history else None
        answer_trace = generate_answer_with_trace(
            query, chunks, history=hist, prompt_variant=self.params.get("prompt_variant")
        )
        answer = answer_trace["answer"]
        t_gen = time.time()
        elapsed = time.time() - t0

        if use_history:
            self.history.append({"role": "user", "content": query})
            self.history.append({"role": "assistant", "content": answer})

        return {
            "query": query,
            "answer": answer,
            "sources": [c["metadata"].get("사업명", "") for c in chunks],
            "retrieved_orgs": [c["metadata"].get("발주 기관", "") for c in chunks],
            "chunks": chunks,
            "context_backfill_count": sum(
                1 for c in chunks
                if (c.get("metadata") or {}).get("source_type") == "csv_summary_backfill"
            ),
            "project_focus_filter_count": project_focus_filter_count,
            "effective_top_k": effective_top_k,
            "latency_sec": round(elapsed, 2),
            "retrieval_sec": round(t_ret - t0, 2),
            "retrieval_usage_trace": retrieval_trace,
            "retrieval_cost_usd": sum_cost(retrieval_trace),
            "generation_sec": round(t_gen - t_ret, 2),
            "generation_usage_trace": answer_trace.get("usage_trace", []),
            "generation_cost_usd": answer_trace.get("cost_usd"),
        }

    def reset(self):
        self.history = []
