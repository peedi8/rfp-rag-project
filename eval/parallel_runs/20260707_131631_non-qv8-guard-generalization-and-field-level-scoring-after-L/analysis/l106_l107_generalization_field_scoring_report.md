# L106-L107 Generalization and Field Scoring Report

After L105, qv8 reached EDD 99.13 and became saturated diagnostic evidence. The next useful work was not another qv8 score push, but overfit control: check whether refusal guards overblock normal questions and add a field-level lens for mixed official/private contact answers.

| point | artifact | result | decision |
|---|---|---|---|
| L106 guard false-positive fixtures | `scripts/check_evidence_guard_fixtures.py` | `49/49` pass | keep narrowed preempt boundary |
| L106 field contact scorer | `scripts/field_level_contact_scorer.py` | expectation match `4/4` | keep as diagnostic-only scorer |
| L107 non-qv8 draft set | `questions_l106_nonqv8_guard_generalization_diagnostic_draft.json` | 7 draft cases registered diagnostic-only | do not run as strict validation yet |
| L107 eval integration | `scripts/evaluate.py`, `scripts/run_experiment_worker.py` | field_score attaches only when field expectations exist | keep out of EDD |

Cause: red review showed the preempt guard could become too broad if one unsupported-result marker plus a generic guessing/fabrication word triggered full refusal. It also showed aggregate EDD cannot represent mixed questions where an official contact should be answered but a private contact must be refused.

Change: removed broad guessing words from the sensitive-query marker family, added positive and boundary no-API fixtures, added a deterministic field-level contact/privacy scorer, wired optional `field_score` into eval details, and registered a non-qv8 diagnostic draft set for the next grounded mini-set.

Result: guard fixtures expanded from `41/41` to `49/49` and now protect budget-vs-final-contract, evaluation-criteria-with-caveat, support-center workflow, official contact, private-contact fabrication, patient-story fabrication, award-score fabrication, and plain-language scope boundaries. Field scoring correctly matched all expected pass/fail cases while distinguishing over-refusal from unsafe exposure.

Insight: L105 remains a real qv8 diagnostic improvement, but the next score claim must come from a non-qv8 grounded mini-set. Field-level scoring is now available as a diagnostic axis, so mixed official/private contact rows no longer need to be forced into a single abstention/EDD label.

Next: assign real corpus-backed target projects to the L107 draft cases, freeze that mini-set before reading answers, then run a small scored or no-judge probe under the budget gate. Keep strict scoreboard, diagnostic-only, measurement repair, and field-level diagnostics separate.
