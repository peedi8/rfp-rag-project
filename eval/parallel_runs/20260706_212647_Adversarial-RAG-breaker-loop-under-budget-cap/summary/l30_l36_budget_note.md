# L30-L36 Budget Note

- user cap: below `$14.00`
- hard preference: avoid unnecessary paid question-generation calls
- actual token billing captured by current eval scripts: not available for L30-L36 answer/judge runs
- actual calibration ledger from earlier budgeted gate: `$0.063527`

## What Was Run

- L30: 14-case v5 baseline
- L31: no-answer retrieval/code diagnostic
- L32: 42-case v5 top-k sweep
- L33/L34: same-answer recomputations without answer/judge calls
- L35: 10-case v4 regression baseline
- L36: 30-case v4 top-k regression

## Conservative Interpretation

The L30-L36 loop stayed within the intended budget posture because:

- question generation used local project context rather than paid generation calls;
- recomputation steps reused saved answers and did not call answer/judge models;
- the paid portions were bounded case sets, not open-ended runs;
- no additional high-cost external audit was launched.

Exact cost accounting should be added before future long runs. The next runner improvement should capture token usage per answer and judge call, then write a cumulative cost ledger before starting each next case.
