"""실험 결과 자동 누적 로거.  실행: python -m scripts.log_run [csv경로]

가장 최근(또는 지정) experiments_*.csv 를 읽어:
- 비교표를 마크다운으로 정리
- 지표별 최고/최저 설정을 자동 관찰(observation)로 뽑음
- eval/experiment_log.md 에 '누적' 기록 (append)
OpenAI 호출 없음 — 순수 파일 처리.
"""
import sys, os, csv, glob
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "eval", "results")
LOG = os.path.join(ROOT, "eval", "experiment_log.md")

METRICS = [
    ("retrieval_coverage_avg", True), ("hit_all_targets_rate", True), ("mrr", True),
    ("groundedness_avg", True), ("relevance_avg", True),
    ("abstention_accuracy", True), ("latency_avg_sec", False),
]


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _latest_csv():
    files = sorted(glob.glob(os.path.join(RESULTS, "experiments_*.csv")))
    return files[-1] if files else None


def _best(rows, col, maximize=True):
    vals = [(r["experiment"], _num(r.get(col))) for r in rows if _num(r.get(col)) is not None]
    if not vals:
        return None
    return (max if maximize else min)(vals, key=lambda t: t[1])


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else _latest_csv()
    if not path or not os.path.exists(path):
        print("❌ 읽을 실험 CSV가 없습니다. 먼저 run_experiments 를 실행하세요.")
        return
    with open(path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("❌ CSV가 비어 있습니다.")
        return

    cols = [c for c, _ in METRICS]
    header = ["experiment"] + cols
    lines = []
    lines.append(f"\n## {datetime.now():%Y-%m-%d %H:%M} · {os.path.basename(path)}\n")
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "|".join(["---"] * len(header)) + "|")
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(c, "")) for c in header) + " |")

    lines.append("\n**자동 관찰:**")
    labels = {
        "retrieval_coverage_avg": "검색 커버리지 최고",
        "mrr": "MRR 최고",
        "groundedness_avg": "충실도 최고",
        "relevance_avg": "관련성 최고",
        "latency_avg_sec": "지연 최저",
    }
    for col, label in labels.items():
        maximize = col != "latency_avg_sec"
        b = _best(rows, col, maximize)
        if b:
            lines.append(f"- {label}: **{b[0]}** ({b[1]})")

    # 검증 경고: 커버리지 0이면 빈 인덱스 착시 가능성
    covs = [_num(r.get("retrieval_coverage_avg")) for r in rows]
    if all((c == 0 for c in covs if c is not None)):
        lines.append("- ⚠️ 모든 커버리지가 0 → 빈 인덱스 착시 의심. build_index 성공 여부 확인 필요.")

    block = "\n".join(lines) + "\n"
    header_note = "# 실험 누적 로그 (자동 생성)\n\n> `scripts/log_run.py`가 실험마다 append. 사람이 쓰는 서술 일지는 `업무일지.md` 참조.\n"
    if not os.path.exists(LOG):
        with open(LOG, "w", encoding="utf-8") as f:
            f.write(header_note)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(block)
    print(f"✅ 누적 기록 완료 → {LOG}")
    print(block)


if __name__ == "__main__":
    main()
