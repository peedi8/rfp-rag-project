"""Retrieval. 실험을 위해 모든 옵션을 인자로 받는다.

지원 기법:
- 단순 유사도 검색 (baseline)
- MMR (다양성 고려)
- 메타데이터 자동 필터링 (질의 속 기관명을 퍼지 매칭 → 발주기관 필터)
- LLM 리스트와이즈 리랭킹 (후보를 LLM이 재정렬)
"""
from __future__ import annotations
import difflib
import json
import math
import re
from collections import Counter
import numpy as np
from openai import OpenAI
import config
from src.vectorstore import embed_texts, load_index

_client = OpenAI(api_key=config.OPENAI_API_KEY)

# 알려진 발주기관 목록 (자동 필터용). 최초 1회 로드.
_KNOWN_ORGS: list[str] | None = None
_KNOWN_PROJECTS: list[dict] | None = None

_ORG_PREFIXES = (
    "재단법인",
    "사단법인",
    "학교법인",
    "경상북도",
    "경상남도",
    "전라북도",
    "전라남도",
    "전북특별자치도",
    "충청북도",
    "충청남도",
    "강원특별자치도",
    "제주특별자치도",
    "서울특별시",
    "부산광역시",
    "대구광역시",
    "인천광역시",
    "광주광역시",
    "대전광역시",
    "울산광역시",
    "세종특별자치시",
    "경기도",
)

_SHORT_ADMIN_ALIAS_BLOCK_SUFFIXES = (
    "대학교",
    "대학원",
    "대학",
    "산역",
    "역",
    "천",
)


def _cosine(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def _mmr(query_vec, cand_vecs, k, lambda_mult):
    selected, remaining = [], list(range(len(cand_vecs)))
    sims = [_cosine(query_vec, v) for v in cand_vecs]
    while remaining and len(selected) < k:
        if not selected:
            best = max(remaining, key=lambda i: sims[i])
        else:
            def score(i):
                diversity = max(_cosine(cand_vecs[i], cand_vecs[j]) for j in selected)
                return lambda_mult * sims[i] - (1 - lambda_mult) * diversity
            best = max(remaining, key=score)
        selected.append(best)
        remaining.remove(best)
    return selected


def _load_known_orgs() -> list[str]:
    global _KNOWN_ORGS
    if _KNOWN_ORGS is None:
        col = load_index()
        got = col.get(include=["metadatas"])
        orgs = {m.get("발주 기관", "") for m in got["metadatas"] if m.get("발주 기관")}
        _KNOWN_ORGS = sorted(orgs)
    return _KNOWN_ORGS


def _load_known_projects() -> list[dict]:
    """Load unique project titles for title-fragment based filtering."""
    global _KNOWN_PROJECTS
    if _KNOWN_PROJECTS is None:
        col = load_index()
        got = col.get(include=["metadatas"])
        projects = {}
        for meta in got["metadatas"]:
            title = (meta or {}).get("사업명", "")
            org = (meta or {}).get("발주 기관", "")
            if not title or not org:
                continue
            norm = _normalize_org_text(title)
            if len(norm) < 10:
                continue
            projects[(title, org)] = {"title": title, "org": org, "norm": norm}
        _KNOWN_PROJECTS = sorted(projects.values(), key=lambda x: len(x["norm"]), reverse=True)
    return _KNOWN_PROJECTS


def _normalize_org_text(text: str) -> str:
    cleaned = (text or "").replace("(주)", "").replace("주식회사", "").lower()
    return re.sub(r"[\s()（）·ㆍ\-_/]", "", cleaned)


def _alias_occurs_in_query(alias: str, query: str) -> bool:
    start = 0
    while True:
        idx = query.find(alias, start)
        if idx < 0:
            return False
        suffix = query[idx + len(alias):]
        if len(alias) <= 4 and suffix.startswith(_SHORT_ADMIN_ALIAS_BLOCK_SUFFIXES):
            start = idx + 1
            continue
        return True


def _org_aliases(org: str) -> list[str]:
    core = _normalize_org_text(org)
    aliases = {core}
    short_admin_aliases = set()
    changed = True
    while changed:
        changed = False
        for prefix in _ORG_PREFIXES:
            if core.startswith(prefix):
                core = core[len(prefix):]
                aliases.add(core)
                changed = True
    if core.endswith("도시관리공사") and len(core) > len("도시관리공사"):
        city = core[: -len("도시관리공사")]
        aliases.add(city + "공사")
        aliases.add(city + "도시공사")
    for alias in list(aliases):
        if alias.endswith("대학교"):
            aliases.add(alias[:-3] + "대학")
        if alias.endswith("대학") and not alias.endswith("대학교"):
            aliases.add(alias + "교")
        if alias.endswith(("시", "군", "구")) and len(alias) > 2:
            stripped = alias[:-1]
            if 2 <= len(stripped) <= 4:
                short_admin_aliases.add(stripped)
    aliases.update(short_admin_aliases)
    return sorted(a for a in aliases if len(a) >= 3 or a in short_admin_aliases)


def _auto_org_filter(query: str) -> dict | None:
    """질의에서 알려진 발주기관을 찾아 메타데이터 필터를 만든다.

    - 기관명이 질의에 '충분히(60%+) 통째로' 등장할 때만 매칭 → 접미사(연구원/대학교 등)
      우연 겹침으로 인한 오필터 방지.
    - 공백 차이('한국 원자력 연구원')와 부정확 입력('원자력연구소')도 대응.
    - 여러 기관이 매칭되면(비교 질문) $in 으로 모두 포함.
    """
    orgs = _load_known_orgs()
    q = _normalize_org_text(query)
    matches = []
    for org in orgs:
        best = 0
        for alias in _org_aliases(org):
            if _alias_occurs_in_query(alias, q):
                best = max(best, 100 + len(alias))
                continue
            lcs = difflib.SequenceMatcher(None, alias, q).find_longest_match(0, len(alias), 0, len(q)).size
            if lcs >= max(4, math.ceil(0.7 * len(alias))):
                best = max(best, lcs)
        if best:
            matches.append((best, org))
    if not matches:
        return _project_title_filter(query)
    matches.sort(reverse=True)
    sel = list(dict.fromkeys(o for _, o in matches))[:6]
    return {"발주 기관": sel[0]} if len(sel) == 1 else {"발주 기관": {"$in": sel}}


def _project_title_filter(query: str) -> dict | None:
    """Infer issuer from a long project-title fragment in the question.

    This is intentionally stricter than org alias matching. It only fires on
    long contiguous overlap with a known project title, so generic terms like
    "정보시스템 구축" do not force a wrong issuer.
    """
    q = _normalize_org_text(query)
    if len(q) < 10:
        return None

    matches = []
    for project in _load_known_projects():
        title_norm = project["norm"]
        match = difflib.SequenceMatcher(None, title_norm, q).find_longest_match(
            0, len(title_norm), 0, len(q)
        )
        lcs = match.size
        if lcs < 10:
            continue
        shorter = max(1, min(len(title_norm), len(q)))
        title_ratio = lcs / max(1, len(title_norm))
        shorter_ratio = lcs / shorter
        if title_ratio < 0.45 and shorter_ratio < 0.55:
            continue
        matches.append((lcs + title_ratio, project["org"], project["title"]))

    if not matches:
        return None
    matches.sort(reverse=True)
    best = matches[0][0]
    selected = []
    for score, org, _title in matches:
        if score < best - 4:
            break
        if org not in selected:
            selected.append(org)
        if len(selected) >= 6:
            break
    if not selected:
        return None
    return {"발주 기관": selected[0]} if len(selected) == 1 else {"발주 기관": {"$in": selected}}


def _llm_rerank(query: str, docs: list[str], metas: list[dict], k: int) -> list[int]:
    """LLM이 후보 청크를 보고 질의에 가장 관련 있는 top-k 인덱스를 고른다 (1회 호출)."""
    listing = []
    for i, (d, m) in enumerate(zip(docs, metas)):
        listing.append(f"[{i}] ({m.get('사업명','')}) {d[:300]}")
    prompt = (
        f"질문: {query}\n\n"
        f"다음 후보 문서 조각들 중 질문에 답하는 데 가장 관련 있는 것을 순서대로 최대 {k}개 고르세요.\n"
        f'반드시 JSON 객체로만 답하세요. 예: {{"indices": [3, 0, 7]}}\n\n' + "\n".join(listing)
    )
    kwargs = dict(model=config.CHAT_MODEL,
                  messages=[{"role": "user", "content": prompt}],
                  max_completion_tokens=500)   # gpt-5 계열 추론 토큰 여유
    try:
        try:
            resp = _client.chat.completions.create(response_format={"type": "json_object"}, **kwargs)
        except Exception:
            resp = _client.chat.completions.create(**kwargs)
        content = (resp.choices[0].message.content or "").strip()
        try:
            data = json.loads(content)
        except Exception:
            m = re.search(r"\{.*\}", content, re.S)
            data = json.loads(m.group(0)) if m else {}
        idxs = data.get("indices", []) if isinstance(data, dict) else []
        idxs = [i for i in idxs if isinstance(i, int) and 0 <= i < len(docs)]
        return idxs[:k] if idxs else list(range(min(k, len(docs))))
    except Exception:
        return list(range(min(k, len(docs))))


def _filtered_orgs(where: dict | None) -> list[str]:
    if not isinstance(where, dict):
        return []
    value = where.get("발주 기관")
    if isinstance(value, dict) and isinstance(value.get("$in"), list):
        return [str(v) for v in value["$in"] if v]
    if isinstance(value, str):
        return [value]
    return []


def _ensure_org_coverage(
    idxs: list[int],
    metas: list[dict],
    dists: list[float],
    required_orgs: list[str],
    top_k: int,
) -> list[int]:
    """Keep at least one chunk per filtered org when enough candidates exist."""
    if len(required_orgs) <= 1:
        return idxs
    selected = list(dict.fromkeys(idxs))

    def org_of(i: int) -> str:
        return (metas[i] or {}).get("발주 기관", "")

    for org in required_orgs:
        if any(org_of(i) == org for i in selected):
            continue
        candidates = [i for i, meta in enumerate(metas) if (meta or {}).get("발주 기관", "") == org and i not in selected]
        if not candidates:
            continue
        best = min(candidates, key=lambda i: dists[i])
        if len(selected) < top_k:
            selected.append(best)
            continue

        counts = Counter(org_of(i) for i in selected)
        replaceable_positions = [
            pos for pos, i in enumerate(selected)
            if org_of(i) not in required_orgs or counts[org_of(i)] > 1
        ]
        if not replaceable_positions:
            replaceable_positions = [len(selected) - 1]
        replace_pos = max(replaceable_positions, key=lambda pos: dists[selected[pos]])
        selected[replace_pos] = best

    return selected[:top_k]


def retrieve(
    query: str,
    top_k: int = None,
    where: dict | None = None,
    use_mmr: bool = None,
    mmr_lambda: float = None,
    fetch_k: int = None,
    auto_filter: bool = False,
    rerank: bool = False,
    trace: list[dict] | None = None,
) -> list[dict]:
    """질의에 대한 관련 청크 반환. 옵션 미지정 시 config 기본값 사용."""
    top_k = top_k if top_k is not None else config.TOP_K
    use_mmr = use_mmr if use_mmr is not None else config.USE_MMR
    mmr_lambda = mmr_lambda if mmr_lambda is not None else config.MMR_LAMBDA
    fetch_k = fetch_k if fetch_k is not None else config.FETCH_K

    col = load_index()
    q_vec = embed_texts([query], trace=trace, operation="query_embedding")[0]

    if where is None and auto_filter:
        where = _auto_org_filter(query)

    n = max(fetch_k, top_k) if (use_mmr or rerank) else top_k
    res = col.query(
        query_embeddings=[q_vec],
        n_results=n,
        where=where,
        include=["documents", "metadatas", "embeddings", "distances"],
    )
    docs = list(res["documents"][0])
    metas = list(res["metadatas"][0])
    vecs = list(res["embeddings"][0])
    dists = list(res["distances"][0])
    if not docs:
        return []

    required_orgs = _filtered_orgs(where)
    if len(required_orgs) > 1:
        present_orgs = {(m or {}).get("발주 기관", "") for m in metas}
        seen_doc_keys = {
            ((m or {}).get("doc_id", ""), (m or {}).get("chunk_index", ""))
            for m in metas
        }
        for org in required_orgs:
            if org in present_orgs:
                continue
            extra = col.query(
                query_embeddings=[q_vec],
                n_results=1,
                where={"발주 기관": org},
                include=["documents", "metadatas", "embeddings", "distances"],
            )
            extra_docs = extra["documents"][0]
            if not extra_docs:
                continue
            extra_meta = extra["metadatas"][0][0]
            key = ((extra_meta or {}).get("doc_id", ""), (extra_meta or {}).get("chunk_index", ""))
            if key in seen_doc_keys:
                continue
            docs.append(extra_docs[0])
            metas.append(extra_meta)
            vecs.append(extra["embeddings"][0][0])
            dists.append(extra["distances"][0][0])
            seen_doc_keys.add(key)

    if rerank:
        idxs = _llm_rerank(query, docs, metas, top_k)
    elif use_mmr and len(docs) > top_k:
        idxs = _mmr(q_vec, vecs, top_k, mmr_lambda)
    else:
        idxs = list(range(min(top_k, len(docs))))
    idxs = _ensure_org_coverage(idxs, metas, dists, required_orgs, top_k)

    return [
        {"text": docs[i], "metadata": metas[i], "score": 1 - dists[i]}
        for i in idxs
    ]
