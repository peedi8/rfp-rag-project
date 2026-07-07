from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"), strict=False)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--tune-out", required=True)
    parser.add_argument("--holdout-out", required=True)
    parser.add_argument("--holdout-per-type", type=int, default=1)
    args = parser.parse_args()

    questions = load_json(Path(args.input))
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for question in questions:
        by_type[question.get("type", "unknown")].append(question)

    holdout_ids: set[str] = set()
    for _, items in sorted(by_type.items()):
        for question in items[-args.holdout_per_type :]:
            holdout_ids.add(question["id"])

    tune = [q for q in questions if q["id"] not in holdout_ids]
    holdout = [q for q in questions if q["id"] in holdout_ids]
    write_json(Path(args.tune_out), tune)
    write_json(Path(args.holdout_out), holdout)
    print(json.dumps({"input": args.input, "tune": len(tune), "holdout": len(holdout), "holdout_ids": sorted(holdout_ids)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
