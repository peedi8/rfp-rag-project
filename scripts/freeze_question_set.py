"""Freeze a question JSON file and write a hash manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--dest", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument(
        "--allowed-use",
        default="first_scored_run_only_until_answers_or_failures_are_inspected",
    )
    parser.add_argument(
        "--rule",
        default="If the frozen file is edited or failures are inspected before rerun, do not use later scores as strict untouched validation.",
    )
    args = parser.parse_args()

    args.dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.source, args.dest)
    questions = json.loads(args.dest.read_text(encoding="utf-8"))
    data = {
        "schema": "rfp_rag_frozen_question_set_manifest.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "label": args.label,
        "source": str(args.source),
        "dest": str(args.dest),
        "sha256": sha256(args.dest),
        "case_count": len(questions) if isinstance(questions, list) else None,
        "allowed_use": args.allowed_use,
        "rule": args.rule,
    }
    args.manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"dest": str(args.dest), "manifest": str(args.manifest), "sha256": data["sha256"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
