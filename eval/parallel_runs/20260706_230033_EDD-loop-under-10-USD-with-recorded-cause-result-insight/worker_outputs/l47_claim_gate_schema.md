# L47 Claim Gate Schema Proposal: qv6_007

- schema: `parallel_team_worker_output.v1`
- worker: `worker_a_l47_claim_gate_schema`
- API use: none
- protected files edited: none

## Bottom Line

Add a deterministic no-API gate for `qv6_007_goyang_facility_order_permutation`.

The gate should fail the current L40 pattern: it correctly binds to `고양도시관리공사` and recovers `무인화 운영`, but still says physical `출입통제` cannot be confirmed while the Goyang source summary says `출입통제시스템 구매 및 설치`.

## Hard Expected Claim Keys

| Claim key | Required behavior |
|---|---|
| `project_identity.goyang_gwansan_integrated_operation` | Answer binds to `고양도시관리공사` + `관산근린공원`/`다목적구장`. |
| `unmanned_operation.program_technical_support` | Answer confirms `무인화 운영 프로그램 제공` or equivalent program/technical support. |
| `unmanned_operation.operating_system_hw_linkage` | Answer confirms `운영시스템과의 하드웨어 연동` or `H/W 연동 프로그램`. |
| `physical_access_control.purchase_install` | Answer confirms physical `출입통제시스템 구매 및 설치` or equivalent inclusion. |
| `physical_access_control.not_system_account_access_only` | Answer must not substitute `접근권한`/`접속기록`/network access control for physical facility access control. |
| `source_scope.no_cross_org_leak` | Answer must not use Jeongeup or other non-Goyang facility evidence for Goyang claims. |

Guard claim:

| Claim key | Behavior |
|---|---|
| `unknown_detail_boundary.method_specs_not_overclaimed` | Do not fail merely because the answer omits this boundary. Fail only if it asserts unsupported method/spec/vendor/interface details, or turns narrow unknowns into broad inclusion denial. |

## Positive Markers

Minimal pass markers:

- `고양도시관리공사` with `관산근린공원` or `다목적구장`
- `무인화 운영 프로그램 제공` or `무인화 운영을 위한 프로그램 및 기술 지원`
- `운영시스템과의 하드웨어 연동`, `운영시스템과의 H/W 연동`, or `H/W 연동 프로그램`
- `출입통제시스템 구매 및 설치`, `출입통제시스템 구매`, or `출입통제시스템 설치`
- Narrow unknowns only for `상세 규격`, `출입통제 방식`, `RFID`, `지문`, `카드`, `제품명`, or interface details

Optional preservation/detail markers:

- `무인발권기`
- `안내데스크`
- `부가장비`
- `2SET`
- `중계서버`
- `출입통제시스템과 운영시스템 연계`

## Negative / Underanswer Markers

Fail when these appear near `무인 운영`, `무인화`, or `무인 운영 프로그램`:

- `제공된 문서에서 확인할 수 없습니다`
- `확인할 수 없습니다`
- `확인 불가`
- `명확히 확인되지 않음`

Fail when these appear near `출입통제`, `출입통제시스템`, or `물리적 시설 출입통제`:

- `제공된 문서에서 확인할 수 없습니다`
- `확인할 수 없습니다`
- `확인 불가`
- `명시적 언급은 없습니다`
- `명확히 확인되지 않음`
- `직접적으로 명시되어 있지 않`

Fail the false-friend pattern when the answer only gives:

- `시스템 차원의 접근통제`
- `접근권한`
- `접속기록`
- `네트워크 접근통제`
- `서버 접근통제`
- `보안제품 목록`

and does not also confirm physical `출입통제시스템 구매/설치`.

## Source Notes

- Goyang support: `data\원본 데이터\data_list.csv:2035-2039` confirms project identity, H/W linkage, unmanned operation program, and `안내데스크 및 출입통제시스템 구매 및 설치`.
- Goyang support: `data\원본 데이터\data_list.csv:2086-2100` confirms exact project name, budget, period, and automatic-system/goods-purchase purpose.
- Distractor scope: `data\원본 데이터\data_list.csv:6708`, `6727`, `6751-6755` mention `무인발권`, `출입통제`, `중계서버`, etc., but are non-Goyang/Jeongeup lines. Use them as leakage guards, not as Goyang support.

## Suggested Outputs

- `claim_gate_results.jsonl`: per-case/per-claim result rows with detected markers and failed claim keys.
- `claim_gate_summary.json`: aggregate pass/fail counts and fail labels.
- `claim_gate_report.md`: compact human-readable claim table.
- `hard_stop_flags.json`: optional orchestrator flag keeping broad paid loops closed when qv6_007 fails.
