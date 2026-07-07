"""임베딩 생성 + Chroma Vector DB 구축/로드.

임베딩: OpenAI text-embedding-3-small (가이드 허용 모델)
Vector DB: Chroma (로컬 영속, 메타데이터 필터링 지원)
"""
from __future__ import annotations
from openai import OpenAI
import chromadb
from tqdm import tqdm
import config
from src.costing import traced_call

_client = OpenAI(api_key=config.OPENAI_API_KEY)


def _sanitize(t: str) -> str:
    """UTF-8로 인코딩 불가한 문자(외톨이 서로게이트 등) 제거. 빈 문자열 방지."""
    t = (t or "").encode("utf-8", "ignore").decode("utf-8", "ignore")
    return t if t.strip() else " "


def embed_texts(
    texts: list[str],
    batch_size: int = 100,
    trace: list[dict] | None = None,
    operation: str = "embedding",
) -> list[list[float]]:
    """텍스트 리스트를 임베딩 벡터로 변환 (배치 처리로 API 호출 최소화)."""
    vectors = []
    for i in tqdm(range(0, len(texts), batch_size), desc="임베딩"):
        batch = [_sanitize(t) for t in texts[i:i + batch_size]]
        resp = _client.embeddings.create(model=config.EMBEDDING_MODEL, input=batch)
        if trace is not None:
            trace.append(traced_call(
                operation=operation,
                model=config.EMBEDDING_MODEL,
                resp=resp,
                meta={"batch_size": len(batch), "batch_start": i},
            ))
        vectors.extend([d.embedding for d in resp.data])
    return vectors


def _get_collection():
    db = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    return db.get_or_create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def build_index(chunks: list[dict]):
    """청크들을 임베딩하여 Chroma에 저장한다. (기존 컬렉션은 초기화)"""
    db = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    try:
        db.delete_collection(config.COLLECTION_NAME)
    except Exception:
        pass
    col = db.get_or_create_collection(
        name=config.COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )
    texts = [c["text"] for c in chunks]
    ids = [c["id"] for c in chunks]
    metas = [c["metadata"] for c in chunks]
    vectors = embed_texts(texts)

    # Chroma는 add 한 번에 max_batch_size(약 5461) 제한이 있어 나눠서 저장
    ADD_BATCH = 5000
    for i in range(0, len(chunks), ADD_BATCH):
        col.add(
            ids=ids[i:i + ADD_BATCH],
            documents=texts[i:i + ADD_BATCH],
            embeddings=vectors[i:i + ADD_BATCH],
            metadatas=metas[i:i + ADD_BATCH],
        )
    print(f"저장 완료: {col.count()}개 청크")
    return col


def load_index():
    return _get_collection()
