"""프로젝트 전역 설정. 경로와 하이퍼파라미터를 한 곳에서 관리한다."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Windows cp949 콘솔에서 ✅ 등 이모지 print 가 UnicodeEncodeError 로 죽는 것 방지
# (한글 출력 인코딩은 그대로 두고, 표현 불가 문자만 ? 로 대체)
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

# --- 경로 ---
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "원본 데이터"
CSV_PATH = DATA_DIR / "data_list.csv"
FILES_DIR = DATA_DIR / "files"
CHROMA_DIR = ROOT / "chroma_db"
COLLECTION_NAME = "rfp"


def _load_api_key():
    """API 키를 여러 위치에서 순서대로 찾아 반환한다.
    1) 환경변수  2) .env.local / .env 파일(KEY=VALUE)  3) 원시 키 파일(sk-... 한 줄)
    (이 프로젝트는 .env 가 폴더로 존재할 수 있어 아래 3번 폴백을 둔다.)
    """
    if os.getenv("OPENAI_API_KEY"):
        return os.getenv("OPENAI_API_KEY")
    for fname in [".env.local", ".env"]:
        p = ROOT / fname
        if p.is_file():
            load_dotenv(p)
            if os.getenv("OPENAI_API_KEY"):
                return os.getenv("OPENAI_API_KEY")
    for p in [ROOT / "key.txt", ROOT / ".env.local", ROOT / ".env" / "gpt.txt"]:
        if p.is_file():
            val = p.read_text(encoding="utf-8").strip()
            if val.startswith("sk-"):
                return val
    return None


# --- 모델 (가이드에서 허용된 모델만 사용) ---
OPENAI_API_KEY = _load_api_key()
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-5-mini")
JUDGE_MODEL = os.getenv("JUDGE_MODEL", CHAT_MODEL)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# --- 데이터 소스 ---
DATA_SOURCE = "csv"       # "csv"(추출본, 빠름) 또는 "raw"(원본 hwp/pdf 전체 파싱)

# --- 청킹 하이퍼파라미터 (실험하며 조정) ---
CHUNK_SIZE = 800          # 청크당 글자 수
CHUNK_OVERLAP = 150       # 청크 간 중첩 글자 수

# --- Retrieval 하이퍼파라미터 ---
TOP_K = 8                 # 최종적으로 LLM에 넣을 청크 수
FETCH_K = 20              # MMR 후보로 먼저 뽑을 청크 수
USE_MMR = True            # True면 MMR, False면 단순 유사도
MMR_LAMBDA = 0.5          # 1=관련성 위주, 0=다양성 위주
AUTO_FILTER = True        # 질의 내 기관명 기반 메타데이터 필터
RERANK = False            # LLM 리랭크는 지연 대비 이득이 낮아 기본 비활성화
REWRITE_QUERY = True      # 멀티턴 후속질문 검색용 독립질문 재작성

# --- Generation 하이퍼파라미터 ---
# gpt-5-mini는 긴 RFP 근거를 읽을 때 추론 토큰을 많이 쓰므로 1024면 빈 답변이 날 수 있다.
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "3072"))
JUDGE_MAX_TOKENS = int(os.getenv("JUDGE_MAX_TOKENS", "2400"))
JUDGE_CONTEXT_CHARS = int(os.getenv("JUDGE_CONTEXT_CHARS", "7200"))
JUDGE_CONTEXT_PER_CHUNK_CHARS = int(os.getenv("JUDGE_CONTEXT_PER_CHUNK_CHARS", "800"))
TEMPERATURE = 0.2         # 사실 기반 답변이라 낮게. (gpt-5 계열은 미지원일 수 있음)
