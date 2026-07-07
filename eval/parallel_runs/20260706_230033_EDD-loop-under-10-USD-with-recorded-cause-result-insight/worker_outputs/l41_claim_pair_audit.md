# l41 Claim Pair Audit: qv6_006 vs qv6_007

- schema: `parallel_team_worker_output.v1`
- task: `l41_claim_pair_audit`
- API use: none
- protected files edited: none

## Bottom Line

L37 preserved the Goyang project identity but underanswered the shuffled qv6_007 question: it said both `무인 운영 프로그램` and `출입통제` could not be confirmed.

L40 is a meaningful partial fix. It retrieves only Goyang documents, confirms `무인 운영 프로그램` and H/W linkage, and separates system-level access permissions from physical access control. However, it still fails to preserve qv6_006's physical `출입통제시스템` purchase/linkage claims.

Merge recommendation: merge/use L40 as the better qv6_007 result, but mark the metamorphic pair as `partial recovery`, not full pass.

## Evidence Used

- `data\원본 데이터\data_list.csv:2035-2039`
  - Confirms the Goyang project and high-level scope.
  - Scope includes system upgrade, operating-system H/W linkage, unmanned-operation program, and purchase/installation of information desk and access-control systems.
- `data\원본 데이터\data_list.csv:2086-2100`
  - Confirms project name, 90-day period, 90,000,000 KRW budget, and purpose: efficient member integrated operation management and automatic-system build.
- L37 `details.json`
  - qv6_006 canonical answer lists homepage, member management, unmanned operation, and access control claims.
  - qv6_007 answer says unmanned operation and access control cannot be confirmed.
- L40 `details.json`
  - qv6_007 answer confirms unmanned operation program and H/W linkage, but still says physical access control cannot be confirmed.

## Claim Preservation Counts

| Run | Preserved | Partial | Underanswered / Not Preserved | Contradicted / False Not-Found | Unsupported Added Claims |
|---|---:|---:|---:|---:|---:|
| L37 qv6_007 | 1 | 1 | 14 | 3 | 0 |
| L40 qv6_007 | 3 | 4 | 9 | 2 | 0 |

## Key Atomic Claims

| Claim | qv6_006 Expected | L37 qv6_007 | L40 qv6_007 |
|---|---|---|---|
| C01 | Same Goyang project binding | Preserved | Preserved |
| C11 | Unmanned-operation program / technical support included | Not preserved: says cannot confirm | Preserved |
| C13 | H/W linkage program with operating system | Not preserved | Preserved |
| C14 | Physical entry/exit access-control system purchase/install, 2SET, relay/equipment | Contradicted/underanswered | Contradicted/underanswered |
| C15 | Access-control system linked with operating system | Contradicted/underanswered | Contradicted/underanswered |
| C16 | Narrow unknowns: detailed H/W specs, RFID/fingerprint/card method, PG vendor, interface specs | Partially preserved as broad not-found | Partially preserved as broad physical-access not-found |

## Audit Interpretation

L37's issue is not hallucination; it is over-refusal caused by weak retrieval depth. It found the Goyang project at rank 2 but retrieved mixed organizations, then used the limited Goyang excerpt to say the requested features were unavailable.

L40 fixes most of that retrieval problem: first hit is Goyang and all retrieved orgs are Goyang. It correctly recovers the unmanned-operation claim. The remaining failure is narrower: it treats physical `출입통제` as unconfirmed, even though qv6_006 asserted it and the CSV project summary directly mentions `출입통제시스템 구매 및 설치`.

## Recommendation

Use L40 over L37 for qv6_007. In reports, phrase the result as:

> Alias retry recovered the Goyang project binding and unmanned-operation claim, but a claim-level audit still finds a residual false-not-found/underanswer on physical access-control scope.

Next proposal-only improvement: add a no-API qv6_007 regression assertion requiring the answer to preserve unmanned operation and not wholly deny physical access-control evidence when the source summary contains `출입통제시스템 구매 및 설치`.
