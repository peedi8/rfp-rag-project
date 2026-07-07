"""Launch several read-only eval suites in parallel and aggregate outputs."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALL_SUITES = ["baseline_default", "prompt_sweep", "topk_sweep", "mmr_lambda_sweep", "fetchk_sweep", "filter_rewrite_ablation"]


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--suites", default=",".join(ALL_SUITES))
    ap.add_argument("--max-workers", type=int, default=2)
    ap.add_argument("--case-limit", type=int, default=None)
    ap.add_argument("--max-experiments", type=int, default=None)
    ap.add_argument("--questions", default=str(ROOT / "eval" / "questions.json"))
    ap.add_argument("--no-judge", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    suites = [s.strip() for s in args.suites.split(",") if s.strip()]
    logs_dir = run_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    queue = list(suites)
    active: list[tuple[str, subprocess.Popen, object, Path]] = []
    finished = []
    started_at = time.time()
    max_workers = max(1, min(args.max_workers, 4))

    while queue or active:
        while queue and len(active) < max_workers:
            suite = queue.pop(0)
            log_path = logs_dir / f"{suite}.log"
            log_file = log_path.open("w", encoding="utf-8")
            cmd = [
                sys.executable,
                "-X",
                "utf8",
                "-m",
                "scripts.run_experiment_worker",
                "--run-dir",
                str(run_dir),
                "--suite",
                suite,
                "--worker-id",
                suite,
                "--questions",
                str(args.questions),
            ]
            if args.case_limit is not None:
                cmd += ["--case-limit", str(args.case_limit)]
            if args.max_experiments is not None:
                cmd += ["--max-experiments", str(args.max_experiments)]
            if args.no_judge:
                cmd.append("--no-judge")
            if args.dry_run:
                cmd.append("--dry-run")
            print(f"launching {suite}: {' '.join(cmd)}")
            proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=log_file, stderr=subprocess.STDOUT, text=True)
            active.append((suite, proc, log_file, log_path))

        time.sleep(1)
        still_active = []
        for suite, proc, log_file, log_path in active:
            code = proc.poll()
            if code is None:
                still_active.append((suite, proc, log_file, log_path))
            else:
                log_file.close()
                finished.append({"suite": suite, "returncode": code, "log": str(log_path)})
                print(f"finished {suite}: rc={code}")
        active = still_active

    aggregate_cmd = [
        sys.executable,
        "-X",
        "utf8",
        "-m",
        "scripts.aggregate_parallel_eval",
        "--run-dir",
        str(run_dir),
    ]
    aggregate = subprocess.run(aggregate_cmd, cwd=str(ROOT), text=True, capture_output=True)
    finished.append({
        "suite": "aggregate",
        "returncode": aggregate.returncode,
        "stdout": aggregate.stdout,
        "stderr": aggregate.stderr,
    })

    _write(
        run_dir / "checkpoint_02_worker_outputs.md",
        "# Checkpoint 02 - Worker Outputs\n\n"
        + "\n".join(f"- {x['suite']}: rc={x['returncode']} log={x.get('log', '')}" for x in finished)
        + "\n",
    )
    _write(
        run_dir / "checkpoint_04_smoke.md",
        "# Checkpoint 04 - Smoke\n\n"
        f"- launch_duration_sec: {round(time.time() - started_at, 2)}\n"
        f"- aggregate_returncode: {aggregate.returncode}\n"
        f"- aggregate_stdout: `{aggregate.stdout.strip()}`\n",
    )
    (run_dir / "processes.json").write_text(json.dumps(finished, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if all(x["returncode"] == 0 for x in finished) else 1


if __name__ == "__main__":
    raise SystemExit(main())
