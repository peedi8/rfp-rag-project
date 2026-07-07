"""인덱스 구축 스크립트.
실행:
    python -m scripts.build_index          # config.DATA_SOURCE 사용 (기본 csv)
    python -m scripts.build_index raw      # 원본 hwp/pdf 전체 파싱본으로 구축
    python -m scripts.build_index csv      # CSV 추출본으로 구축

문서를 로드 → 청킹 → 임베딩 → Chroma에 저장한다. (설정 바꾸면 다시 실행)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.data_loader import load_documents
from src.chunking import chunk_documents
from src.vectorstore import build_index


def main():
    if not config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY 가 없습니다. .env 파일을 먼저 설정하세요.")
        return
    source = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"1) 문서 로딩... (source={source or config.DATA_SOURCE})")
    docs = load_documents(source=source)
    print(f"   문서 {len(docs)}개")
    print("2) 청킹...")
    chunks = chunk_documents(docs)
    print(f"   청크 {len(chunks)}개 (문서당 평균 {len(chunks)/max(len(docs),1):.1f}개)")
    print("3) 임베딩 + Chroma 저장...")
    try:
        build_index(chunks)
    except Exception as e:
        print("\n❌❌❌ 인덱스 구축 실패! 인덱스가 비어있을 수 있으니 문제 해결 후 다시 실행하세요.")
        print(f"   에러: {type(e).__name__}: {e}")
        raise
    print("✅ 완료. 이제 `python -m scripts.ask` 로 질문하거나 평가를 돌려보세요.")


if __name__ == "__main__":
    main()
