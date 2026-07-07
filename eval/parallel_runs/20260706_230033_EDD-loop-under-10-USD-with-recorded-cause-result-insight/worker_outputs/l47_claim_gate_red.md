# L47 Claim Gate Red Review

- worker: Worker B
- status: proposal only
- API use: none
- protected files edited: none
- contract: `parallel_team_worker_output.v1`

## Bottom Line

The L47 claim-preservation outputs are useful, but only as exposed-case diagnostics. They show that L40 improved qv6_007 from L37, not that qv6_007 is fixed and not that the system generalizes.

Current evidence:

| run | claim gate | failed claims | preservation | label |
|---|---|---:|---:|---|
| L37 qv6_007 first v6 run | fail | 2 / 2 | 0.0 | first-run evidence plus exposed diagnostic |
| L40 qv6_007 alias retry | fail | 1 / 2 | 0.5 | partial recovery only |

The important red-team point is L44: the judged qv6_007 row got 5/5 groundedness and relevance while the physical access-control claim still failed the claim gate. That makes L44 a judge-blindness example, not a success case.

## Edge Cases To Red-Team

- Source scope false positive: `check_claim_preservation.py` can load a whole `data_list.csv`, so source markers may come from the wrong row or project unless source hits are tied to the qv6_007 project span or retrieved chunks.
- Answer polarity false positive: a marker should not count as preserved when the answer says the claim is not confirmed.
- False friend access control: account permissions, access logs, or network access control should not satisfy physical entry/exit access-control systems.
- Fixed window miss: a 220-character underanswer window can miss longer answers where the anchor and denial are far apart.
- Encoding fragility: the expectation markers are mojibake-sensitive, so normalized text or spacing changes can cause false failures.
- Missing source markers: for required diagnostic claims, missing source evidence should block or mark expectation/source-gap, not silently pass.
- Old detail schema: older details may lack `answer_quality_issues`; verification should state whether recompute/backfill ran.

## Verification Commands For Orchestrator

Do not interpret exit code `1` from the claim checker as infrastructure failure if the JSON is written and `gate_status=fail`; that is the expected diagnostic result for qv6_007 right now.

```powershell
python -X utf8 scripts/check_claim_preservation.py --details eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs/l37_v6_metamorphic_first_baseline_baseline_default/details.json --expectations eval/claim_preservation_expectations.json --out-dir eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/analysis/l47_claim_gate_l37_first_run --source-root .
```

Expected: `gate_status=fail`, `claims_failed=2`, `claim_preservation_rate=0.0`.

```powershell
python -X utf8 scripts/check_claim_preservation.py --details eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/worker_outputs/l40_v6_goyang_alias_retry_baseline_default/details.json --expectations eval/claim_preservation_expectations.json --out-dir eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight/analysis/l47_claim_gate_l40_alias_retry --source-root .
```

Expected: `gate_status=fail`, `claims_failed=1`, `claim_preservation_rate=0.5`; unmanned operation passes, physical access control fails.

```powershell
python scripts/aggregate_parallel_eval.py --run-dir eval/parallel_runs/20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight
```

Expected: scoreboard remains L37 only; claim-gate evidence remains diagnostic/report-gate evidence, not an EDD row.

## Labeling Rules

Use:

- `diagnostic_only_exposed_case`
- `targeted_failure_probe_exposed`
- `partial_recovery_only`
- `source_supported_but_answer_underanswered`
- `judge_blindness_example`
- `not_generalization_evidence`

Avoid:

- "qv6_007 is fixed"
- "L40 proves generalization"
- "claim preservation is 50% system-wide"
- "judge 5/5 confirms completeness"
- "L47 improves EDD"

Recommended report language:

> L47 confirms a no-API diagnostic gate can catch the exposed qv6_007 residual underanswer. L40 is a partial recovery over L37, but the qv6_007 claim gate still fails and should not be used as generalization evidence.
