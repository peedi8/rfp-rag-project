# L48 Evidence-Use Guard Design

## Bottom Line

Proposal only. Add a narrow no-API post-generation guard for qv6_007-style failures:

1. The retrieved/context chunks contain physical access-control evidence, especially `출입통제시스템 구매 및 설치`.
2. The answer says physical access control cannot be confirmed.
3. The answer substitutes account/admin permission, access logs, server/network access control, or security-product evidence for physical facility access control.

The guard should start as flag-only/report-ready-blocking. If a product answer must be repaired, use a deterministic append-only correction, not another model call.

## Observed Failure

The L47 claim-preservation result for L40 shows `gate_status=fail`, `claims_failed=1`, and `claim_preservation_rate=0.5`.

The failed claim is `physical_access_control_system`:

- `source_supported=true`
- `answer_supported=false`
- `underanswered=true`
- issue: `source_supported_but_answer_underanswered;false_friend_substitution`

The L40 details show this is not a retrieval miss: all 8 retrieved orgs are the target Goyang org, and the model judge gave groundedness/relevance 5/5. The remaining problem is evidence use in the generated answer.

## Proposed Guard

Guard id: `physical_access_control_evidence_use_guard.v1`

Inputs:

- `query`
- `chunks`
- `answer`
- optional target-org or expectation metadata

Trigger only when all are true:

- Retrieved chunks are target-bound or target-only.
- Retrieved chunk text contains a physical access-control source marker such as `출입통제시스템 구매 및 설치` or `출입통제시스템`.
- The question/expectation is asking about access-control inclusion or qv6_007-style facility feature division.

Fail or flag when any is true:

- The answer has cannot-confirm wording near access-control anchors and does not positively confirm physical purchase/install.
- The answer says physical/facility access control cannot be confirmed while citing only account/admin permission, connection logs, server/network access control, or security products.
- The answer mentions the physical marker only inside a negated/not-confirmed sentence.

Allowed unknown boundary:

- RFID/card/biometric method may remain unknown.
- Vendor, model, detailed interface, and exact device specs may remain unknown.
- Operating-system linkage detail may remain unknown if purchase/install inclusion is first confirmed.

## Proposed Change Shape

Do not use global source-file search at runtime. Use only retrieved chunks passed through `RAGPipeline.ask()` and `generate_answer_with_trace()`.

Recommended first implementation is flag-only:

- Add guard diagnostics to the ask result/details output.
- Block report-ready promotion for this exposed diagnostic case.
- Keep the generated answer text unchanged.

Optional deterministic repair:

> However, the retrieved evidence does confirm physical access-control-system purchase/install; detailed method/spec/vendor remains unconfirmed.

This should be append-only and traceable with before/after hashes. No second model/API call.

## Risks

- Marker brittleness: current artifacts include mojibake and spacing variants.
- Source leakage: using whole-file source search could borrow non-target evidence.
- Overcorrection: broad inclusion denial should be caught, but narrow unknown details should remain allowed.
- Overclaiming: qv6_007 is an exposed diagnostic case, not fresh generalization evidence.
- Metric interaction: changing answer text can affect judge/relevance metrics, so start flag-only.

## Exact Before/After Verification Plan

Before implementation:

1. Parse `analysis/l47_claim_gate_l40_alias_retry/claim_preservation_results.json`.
   Expected: `gate_status=fail`, `claims_failed=1`, `claim_preservation_rate=0.5`.
2. Inspect the `physical_access_control_system` claim.
   Expected: `source_supported=true`, `answer_supported=false`, `underanswered=true`, issue includes `false_friend_substitution`.
3. Parse `worker_outputs/l40_v6_goyang_alias_retry_baseline_default/details.json`.
   Expected: 8 target-org retrievals, no off-target retrieval, judge groundedness/relevance 5/5.

After flag-only implementation:

1. Run a no-API fixture test using the L40 answer and retrieved chunk text.
   Expected: guard returns `action=flag`, `guard_id=physical_access_control_evidence_use_guard.v1`, and issues include source-supported underanswer plus false-friend substitution.
2. Rerun `scripts/check_claim_preservation.py` on unchanged L40 details.
   Expected: exit code 1 with JSON written, confirming the original before-state failure.
3. Run a synthetic corrected-answer fixture.
   Expected: no guard issue when the answer confirms purchase/install and limits unknowns to method/spec/vendor.

After optional repair implementation:

1. Apply deterministic append-only repair to the L40 fixture.
   Expected: repaired answer confirms physical access-control purchase/install and does not claim RFID/vendor/spec details.
2. Run claim preservation against a temporary repaired details fixture.
   Expected: exposed qv6_007 diagnostic passes with `claims_failed=0`, while still labeled `diagnostic_only_exposed_case`.

Regression fixtures:

- Source lacks physical access-control marker: no flag, no repair.
- Answer confirms purchase/install but leaves RFID/vendor/spec unknown: pass.
- Retrieved chunks are mixed/off-target: no repair; emit source-scope block or warning.
- Answer repeats the physical marker inside a negated sentence: fail by polarity.

## Commands Run

- `Get-Content -Raw` on `src/generator.py`
- `Get-Content -Raw` on `src/rag.py`
- `Get-Content -Raw` on `scripts/check_claim_preservation.py`
- `Get-Content -Raw` on `eval/claim_preservation_expectations.json`
- `Get-Content -Raw` on L47 L40 `claim_preservation_results.json`
- `Get-Content -Raw` on L40 `details.json`
- `Get-ChildItem` on the run `worker_outputs` directory
- `git -C I:\0706\rfp-rag-project status --short` failed because this checkout is not a git repository
- `Get-Content -Raw` on nearby L47 worker contracts to match `parallel_team_worker_output.v1`

No API/model calls were made. No protected paths were edited.
