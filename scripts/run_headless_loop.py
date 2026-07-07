"""Run a safe no-API headless loop step for RFP-RAG.

The first implementation is intentionally conservative:

- reads a manifest,
- reruns the red/overfit gate,
- writes a runner state and next-action file,
- never launches paid/API evaluation unless a future manifest explicitly
  implements that mode.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.headless_gate import build_report, write_markdown


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _validate_manifest(manifest: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    required = ["run_dir", "loop_points_path", "mode"]
    for key in required:
        if not manifest.get(key):
            issues.append(f"missing required manifest key: {key}")
    mode = manifest.get("mode")
    if mode not in {"no_api_gate_only"}:
        issues.append(f"unsupported mode for this runner version: {mode}")
    if manifest.get("allow_api"):
        issues.append("allow_api=true is not supported by this safe no-api runner version")
    return issues


def _choose_next_action(report: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    recommendations = report.get("recommendations") or []
    first = recommendations[0] if recommendations else {}
    cost_allowed = bool(manifest.get("allow_api"))
    if not cost_allowed:
        return {
            "state": "pending_cost_gate",
            "next_candidate": first.get("action", "Run blind judge calibration before scored promotion."),
            "reason": "The next useful scored gate needs judge/API cost, but this manifest is no-api.",
            "safe_no_api_followup": "Maintain gates, prepare manifests, update logs, or create a fresh question draft without scoring.",
        }
    return {
        "state": "ready_for_paid_gate",
        "next_candidate": first.get("action", "Run blind judge calibration before scored promotion."),
        "reason": "Manifest allows API, but this runner version still requires a separate scored command path.",
    }


def _write_runner_report(path: Path, state: dict[str, Any]) -> None:
    lines = [
        "# Headless Runner State",
        "",
        f"- created_at: `{state['created_at']}`",
        f"- mode: `{state['mode']}`",
        f"- allow_api: `{state['allow_api']}`",
        f"- gate_report: `{state['gate_report_md']}`",
        f"- next_action_state: `{state['next_action']['state']}`",
        "",
        "## Next Action",
        "",
        f"- candidate: {state['next_action']['next_candidate']}",
        f"- reason: {state['next_action']['reason']}",
    ]
    if state["next_action"].get("safe_no_api_followup"):
        lines.append(f"- no-api follow-up: {state['next_action']['safe_no_api_followup']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(manifest_path: Path) -> dict[str, Any]:
    manifest = _read_json(manifest_path)
    issues = _validate_manifest(manifest)
    run_dir = Path(manifest["run_dir"])
    out_dir = run_dir / "summary" / "headless_runner"
    out_dir.mkdir(parents=True, exist_ok=True)

    if issues:
        state = {
            "schema": "rfp_rag_headless_runner_state.v1",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "status": "blocked",
            "issues": issues,
            "manifest_path": str(manifest_path),
        }
        _write_json(out_dir / "headless_runner_state.json", state)
        return state

    gate_args = SimpleNamespace(
        loop_points=Path(manifest["loop_points_path"]),
        out_dir=out_dir,
        quality_matrix=Path(manifest["quality_matrix_path"]) if manifest.get("quality_matrix_path") else None,
        exposure_registry=Path(manifest["exposure_registry_path"]) if manifest.get("exposure_registry_path") else None,
    )
    report = build_report(gate_args)
    gate_json = out_dir / "headless_gate_report.json"
    gate_md = out_dir / "headless_gate_report.md"
    _write_json(gate_json, report)
    write_markdown(gate_md, report)
    next_action = _choose_next_action(report, manifest)
    state = {
        "schema": "rfp_rag_headless_runner_state.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "completed",
        "mode": manifest["mode"],
        "allow_api": bool(manifest.get("allow_api")),
        "manifest_path": str(manifest_path),
        "gate_report_json": str(gate_json),
        "gate_report_md": str(gate_md),
        "next_action": next_action,
    }
    _write_json(out_dir / "headless_runner_state.json", state)
    _write_json(out_dir / "next_action.json", next_action)
    _write_runner_report(out_dir / "headless_runner_state.md", state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    state = run(args.manifest)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0 if state.get("status") == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
