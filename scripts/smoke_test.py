"""비대화형 스모크 테스트. 질문 1개를 던져 파이프라인이 도는지 빠르게 확인.
실행: python -m scripts.smoke_test
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.rag import RAGPipeline


def main():
    if not config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY 가 없습니다. .env 를 먼저 설정하세요.")
        return
    rag = RAGPipeline()
    q = "국민연금공단이 발주한 이러닝시스템 관련 사업 요구사항을 정리해 줘."
    print(f"[테스트 질문] {q}\n")
    r = rag.ask(q)
    print(f"[답변]\n{r['answer']}\n")
    print(f"[근거 사업] {', '.join(s for s in r['sources'] if s)[:150]}")
    print(f"[응답시간] {r['latency_sec']}초")
    print("\n✅ 파이프라인 정상 동작!")


if __name__ == "__main__":
    main()
