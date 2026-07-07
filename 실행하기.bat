@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   입찰메이트 RFP RAG - 원클릭 실행
echo ============================================
echo.

REM --- .env 확인 ---
if not exist ".env" (
    echo [!] .env 파일이 없습니다.
    echo     .env.example 을 복사해서 .env 로 만들고, OPENAI_API_KEY 를 넣으세요.
    echo.
    pause
    exit /b
)

echo [1/3] 패키지 설치 중...
pip install -r requirements.txt
echo.

echo [2/3] 인덱스 구축 중... (문서 임베딩, 1~2분 소요)
python -m scripts.build_index
echo.

echo [3/3] 스모크 테스트 (질문 1개)...
python -m scripts.smoke_test
echo.

echo ============================================
echo   완료! 이제 아래 명령으로 대화할 수 있어요:
echo       python -m scripts.ask
echo ============================================
pause
