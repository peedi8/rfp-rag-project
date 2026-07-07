"""문서 청킹. 글자 수 기반 + 중첩(overlap) 방식의 단순/견고한 베이스라인.

심화: 제안서 목차(Ⅰ, Ⅱ, 1., 2. 등) 단위로 나누는 의미 기반 청킹을 시도해볼 것.
"""
from __future__ import annotations
import re
import config


def _clean(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, size: int = None, overlap: int = None) -> list[str]:
    """글자 수 기준으로 문단 경계를 최대한 존중하며 청킹한다."""
    size = size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP
    text = _clean(text)
    if len(text) <= size:
        return [text] if text else []

    chunks, start = [], 0
    while start < len(text):
        end = start + size
        if end < len(text):
            # 근처의 문단/문장 경계에서 자르도록 시도
            window = text[start:end]
            cut = max(window.rfind("\n"), window.rfind(". "), window.rfind("。"))
            if cut > size * 0.5:
                end = start + cut + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    return chunks


def chunk_documents(docs: list[dict]) -> list[dict]:
    """문서 리스트를 청크 리스트로 변환. 각 청크는 원본 메타데이터를 상속한다."""
    out = []
    for doc in docs:
        pieces = chunk_text(doc["text"])
        for idx, piece in enumerate(pieces):
            meta = dict(doc["metadata"])
            meta["doc_id"] = doc["doc_id"]
            meta["chunk_index"] = idx
            out.append({
                "id": f'{doc["doc_id"]}::{idx}',
                "text": piece,
                "metadata": meta,
            })
    return out
