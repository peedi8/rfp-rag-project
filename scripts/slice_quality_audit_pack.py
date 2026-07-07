from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"), strict=False)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def risk_score(case: dict[str, Any]) -> int:
    flags = set(case.get("automatic_flags") or [])
    qid = str(case.get("question_id") or "")
    score = 0
    score += 40 if "coverage_below_target" in flags else 0
    score += 30 if "high_score_long_answer" in flags else 0
    score += 20 if "missing_numeric_judge" in flags else 0
    score += 50 if "false_abstention" in flags or "missed_abstention" in flags else 0
    score += 15 if "q10" in qid or "abstention" in qid else 0
    score += 10 if "compare" in str(case.get("question_type", "")) else 0
    return score


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()

    src = Path(args.input).resolve()
    dst = Path(args.output).resolve()
    data = load_json(src)
    cases = sorted(data.get("cases", []), key=risk_score, reverse=True)[: args.limit]
    sliced = dict(data)
    sliced["schema"] = "rfp_rag_quality_audit_pack_slice.v1"
    sliced["created_at"] = datetime.now().isoformat(timespec="seconds")
    sliced["source_audit_input"] = str(src)
    sliced["slice_reason"] = "Reduced high-risk slice after the first full audit worker timed out."
    sliced["cases"] = cases
    write_json(dst, sliced)
    print(json.dumps({"output": str(dst), "cases": len(cases)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
