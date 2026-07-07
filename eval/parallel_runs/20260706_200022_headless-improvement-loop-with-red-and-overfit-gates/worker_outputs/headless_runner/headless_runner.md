# Headless Runner Proposal

## Goal

Design a local headless improvement-loop runner that can rehearse and record loop work without API calls by default, then optionally run scored local experiments only when a manifest explicitly allows it. The runner should keep the current discipline visible in `loop_points.csv`: first validation, measurement correction, targeted retry, local diagnostic, no-judge probe, and calibration work are different things.

## Inputs

- `manifest.json`: `run_dir`, `candidate_id`, `baseline_point_id`, `hypothesis`, `mode`, `suite`, `questions_path`, `case_limit`, `max_experiments`, `no_judge`, `no_api`, `dry_run`, `budget`, `gate_config`, `append_targets`, `protected_paths`.
- Existing local scripts:
  - `scripts/run_experiment_worker.py` for bounded suite execution into worker outputs.
  - `scripts/recompute_saved_eval.py` for measurement correction only.
  - `scripts/run_blind_judge_calibration.py --no-api` for calibration pack sanity checks.
- Existing loop history: `loop_points.csv` for score labels, decisions, and non-score diagnostic rows.

## State Machine

1. `planned`: record hypothesis, parent/baseline loop point, intended question pack, and expected risk.
2. `prepared`: validate paths, render exact command strings, and confirm all outputs stay under the current run's worker output subtree.
3. `ran`: execute only commands permitted by mode and budget; record exit code, elapsed time, and artifacts.
4. `measured`: normalize results from CSV/JSON into a loop-point candidate row.
5. `gated`: run budget, red, and overfit gates.
6. Terminal state: `promoted`, `rejected`, `diagnostic_only`, `needs_red_review`, or `needs_overfit_review`.

## Budget Gates

- Stop launching scored runs at the summary cutoff, e.g. 15 minutes before loop end.
- Cap scored eval count and retries per `candidate_id`.
- Block promotion when the same holdout has been used for targeted fixes; label as `targeted_retry_score` or `diagnostic_only`.
- Treat latency improvement as insufficient if groundedness, relevance, abstention behavior, or human quality regresses.
- In `no_api_first`, block commands that would call judge/model paths and log the blocked command plus reason.

## Red And Overfit Gates

Red gate blocks promotion on empty answers, false abstentions, low judge scores, wrong-document evidence, source-scope bleed, fabricated procurement amounts, fabricated vendor/contact/private data, under-refusal, over-refusal, or blind-calibration failure.

Overfit gate blocks leaderboard/promotion claims from same-answer recomputations, same-holdout targeted retries, local diagnostics, no-judge probes, and judge calibration rows. Those rows are still valuable, but they stay labeled as evidence or preparation until verified on an untouched or explicitly fresh validation set.

## Append-Only Artifacts

Worker/headless mode should write candidate artifacts first:

- `loop_points_candidate.csv`: existing L0-L13 columns plus `candidate_id`, `parent_point`, `mode`, `gate_status`, `red_status`, `overfit_status`, `contamination_label`, `artifact_dir`, `command_hash`.
- `runner_events.jsonl`: state transitions, command previews, exits, artifact checks, and gate decisions.
- `budget_ledger.jsonl`: elapsed time, scored run count, retry count, no-api diagnostic count, and stop reasons.
- `loop_points_candidate.json`: graph source.
- `loop_points_chart_candidate.svg`: candidate graph only; never overwrite the final chart in worker mode.
- `merge_packet.md`: concise rows for the main orchestrator to accept or reject.

## Safe No-API First Mode

Allowed by default:

- Manifest validation and protected-path checks.
- `run_blind_judge_calibration.py --no-api`.
- `run_experiment_worker.py --dry-run`.
- `recompute_saved_eval.py` on existing details with measurement-correction labeling.
- Graph regeneration from saved/candidate CSVs.
- Static red/overfit checks.

Blocked by default:

- `run_experiment_worker.py` without `--dry-run` when judge/model calls could occur.
- `run_blind_judge_calibration.py` without `--no-api`.
- Any command depending on `OPENAI_API_KEY`.

## Implementation Shape

Suggested entrypoint:

```powershell
python scripts\run_headless_improvement_loop.py --manifest eval\parallel_runs\<run_id>\manifest.json
```

Suggested first smoke:

1. Validate manifest and output path guard.
2. Run calibration pack in `--no-api` mode if configured.
3. Run one dry-run worker experiment with `--max-experiments 1`.
4. Build candidate loop-points CSV and candidate SVG.
5. Assert protected paths did not change.

