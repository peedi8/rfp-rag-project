"""대화형 질문 CLI.  실행: python -m scripts.ask

연속 질문 시 대화 맥락(히스토리)이 유지된다.
  - 'reset' 입력 시 대화 초기화
  - 'exit' / 'quit' 입력 시 종료
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.rag import RAGPipeline


def main():
    if not config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY 가 없습니다. .env 파일을 먼저 설정하세요.")
        return
    rag = RAGPipeline()
    print("입찰메이트 RAG 챗봇 (종료: exit / 대화초기화: reset)\n")
    while True:
        try:
            q = input("질문> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            continue
        if q.lower() in ("exit", "quit"):
            break
        if q.lower() == "reset":
            rag.reset()
            print("(대화 초기화됨)\n")
            continue
        result = rag.ask(q)
        print(f"\n답변> {result['answer']}")
        print(f"\n(근거 사업: {', '.join(s for s in result['sources'] if s)[:120]})")
        print(f"(응답시간: {result['latency_sec']}초)\n")


if __name__ == "__main__":
    main()
