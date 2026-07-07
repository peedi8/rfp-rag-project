# Claim Preservation Check

- created_at: `2026-07-07T00:13:59`
- details: `eval\parallel_runs\20260706_230033_EDD-loop-under-10-USD-with-recorded-cause-result-insight\worker_outputs\l40_v6_goyang_alias_retry_baseline_default\details.json`
- expectations: `eval\claim_preservation_expectations.json`
- cases_checked: `1`
- claims_total: `2`
- claims_failed: `1`
- preservation_rate: `0.5`

| case | status | passed | failed | warned | rate |
|---|---|---:|---:|---:|---:|
| qv6_007_goyang_facility_order_permutation | fail | 1 | 1 | 0 | 0.5 |

## Claim Details

### qv6_007_goyang_facility_order_permutation

| claim | status | issue | source | answer | underanswered |
|---|---|---|---:|---:|---:|
| unmanned_operation_program | pass |  | True | True | False |
| physical_access_control_system | fail | source_supported_but_answer_underanswered;false_friend_substitution | True | False | True |
