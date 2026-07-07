"""실험 비교 러너.  실행: python -m scripts.run_experiments

여러 검색/생성 설정을 같은 평가셋으로 돌려 지표를 비교표로 출력·저장한다.
이 표가 보고서의 핵심 근거가 된다. (인덱스는 한 번만 구축돼 있으면 됨)

주의: 청크 크기/임베딩 모델 변경 실험은 재임베딩이 필요하므로 별도로
      config.py 를 바꾼 뒤 build_index 를 다시 돌려 비교하세요.
"""
import sys, os, json, csv
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from scripts.evaluate import run_eval

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "eval", "results")

# --- 비교할 설정들 (검색 시점 옵션이라 재임베딩 불필요) ---
EXPERIMENTS = {
    "1_baseline_유사도top5":      {"use_mmr": False, "top_k": 5},
    "2_MMR_top5":                 {"use_mmr": True,  "top_k": 5, "mmr_lambda": 0.5},
    "3_MMR_top8":                 {"use_mmr": True,  "top_k": 8, "mmr_lambda": 0.5},
    "4_MMR_top5_자동필터":         {"use_mmr": True,  "top_k": 5, "auto_filter": True},
    "5_MMR_top5_LLM리랭크":        {"use_mmr": True,  "top_k": 5, "rerank": True},
    "6_자동필터_top8":             {"use_mmr": True,  "top_k": 8, "auto_filter": True},
    "7_최종_자동필터top8_쿼리재작성": {"use_mmr": True,  "top_k": 8, "auto_filter": True, "rewrite_query": True},
}

METRIC_COLS = [
    "retrieval_coverage_avg", "hit_all_targets_rate", "mrr",
    "groundedness_avg", "relevance_avg", "abstention_accuracy", "latency_avg_sec",
]


def main():
    if not config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY 없음. .env 를 먼저 설정하세요.")
        return
    from src.vectorstore import load_index
    cnt = load_index().count()
    if cnt == 0:
        print("❌ 인덱스가 비어 있습니다! (검색할 문서가 0개)")
        print("   → 먼저 `python -m scripts.build_index` (또는 raw) 를 '성공적으로' 실행하세요.")
        print("   → build 마지막에 '저장 완료: N개 청크' 문구가 떠야 정상입니다.")
        return
    print(f"✅ 인덱스 청크 수: {cnt}개 — 실험 시작\n")

    rows = []
    details_all = {}
    for name, params in EXPERIMENTS.items():
        print(f"\n{'='*50}\n▶ 실험: {name}  {params}\n{'='*50}")
        out = run_eval(params=params, verbose=True)
        row = {"experiment": name, **out["metrics"]}
        rows.append(row)
        # 질문별 상세(어느 질문이 왜 실패했는지) 보관 → 원인 분석용
        details_all[name] = {"params": params, "metrics": out["metrics"], "details": out["details"]}

    # --- 비교표 출력 ---
    print("\n\n================ 실험 비교표 ================")
    header = ["experiment"] + METRIC_COLS
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join(["---"] * len(header)) + "|")
    for r in rows:
        print("| " + " | ".join(str(r.get(c, "")) for c in header) + " |")

    # --- 저장 (CSV + JSON) ---
    os.makedirs(OUT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(OUT_DIR, f"experiments_{stamp}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)
    # 질문별 상세도 저장 (원인 분석·일지 작성용)
    import json
    detail_path = os.path.join(OUT_DIR, f"experiments_{stamp}_detail.json")
    with open(detail_path, "w", encoding="utf-8") as f:
        json.dump(details_all, f, ensure_ascii=False, indent=2)
    print(f"\n비교표 저장: {csv_path}")
    print(f"질문별 상세 저장: {detail_path}")


if __name__ == "__main__":
    main()
