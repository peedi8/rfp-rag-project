# L37-L40 V6 Metamorphic Loop Report

## Scope

- Budget policy: continue under the 10 USD cap.
- Evidence rule: first-run, targeted retry, measurement correction, and diagnostic-only results are kept separate.
- Freshness rule: L37 is the first v6 evidence. L38-L40 are exposed-case diagnostics because the failures were inspected before retry.

## Loop Points

| loop | purpose | EDD | comparable? | result |
|---|---|---:|---|---|
| L37 | frozen v6 first run | 86.25 | yes, first-run evidence | found abstention and metamorphic failures |
| L38 | qv6_004/qv6_010 safety retry | 56.04 | no, missing judged quality | abstention fixed on both targeted cases |
| L39 | qv6_007 top_k depth probe | 80.95 best row | no, one exposed case | top_k alone failed to recover stable answer |
| L40 | qv6_007 alias retry | 85.00 | no, one exposed case | retrieval contamination fixed, but latency and answer completeness remain weak |

## Cause, Result, Insight

### L37

- Cause: v6 introduced harder properties: unsupported final procurement, generic title ambiguity, and metamorphic paraphrase/order invariance.
- Result: EDD fell to 86.25. Coverage and judge scores looked high, but abstention accuracy was 0.0.
- Insight: the old high scores were not enough. The system still answered when it should have refused or asked for more identifying information.

### L38

- Cause: qv6_004 treated a budget/business amount as if it answered actual contract amount, and qv6_010 picked a plausible project from a generic title fragment.
- Change: strengthened the system prompt to separate budget from final contract results, official contacts from personal contacts, and ambiguous titles from identified projects.
- Result: both targeted cases were detected as abstentions. qv6_004 became much safer.
- Insight: qv6_010 still says the fragment is ambiguous but then gives a long candidate summary. The next answer-quality gate should penalize over-answering after ambiguity.

### L39

- Cause: qv6_007 used `고양 공사`, which did not bind to `고양도시관리공사`. The context included unrelated organizations.
- Result: top5/top8 still said 무인 운영 and 출입통제 were not confirmed. top12 recovered part of 무인화 but groundedness fell to 1.0.
- Insight: increasing top_k is not a real fix when the organization binding is wrong. It can add noise faster than it adds evidence.

### L40

- Cause: the retriever needed an alias rule for `도시관리공사` organizations.
- Change: added `city + 공사` and `city + 도시공사` aliases for `*도시관리공사`.
- Result: qv6_007 retrieved only `고양도시관리공사` chunks at rank 1. However latency rose to 40.69s and the answer still said physical 출입통제 was not confirmed.
- Insight: source inspection shows 출입통제/무인발권/중계서버 evidence exists in `data/원본 데이터/data_list.csv`. The remaining failure is answer evidence-use/completeness, not source absence.

## Budget Note

- Existing blind judge calibration has recorded actual cost `$0.063527` across its budgeted checks.
- L37-L40 worker outputs record latency and metrics but do not persist token usage or observed USD cost for general answer/judge calls.
- This means the run followed a low-volume under-10-USD policy, but exact total spend for L37-L40 cannot be audited from artifacts yet.
- Next broad paid loop is gated on v9-style usage/cost tracing or a smaller run that records usage per call.

## Promotion Decision

- Keep v6 first-run evidence as L37 EDD 86.25.
- Keep safety prompt guard and `도시관리공사` alias patch.
- Do not promote L38-L40 as generalization scores.
- Next best work: claim-level/metamorphic answer audit on qv6_006/qv6_007 and implement cost tracing before any broad v7/v8/v9 paid execution.
