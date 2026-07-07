# Worker D Report Graphs Summary

Recommended final report exhibits:

1. EDD trend for L81, L85 topk8, L91, L95 as source-exposed diagnostic evidence. Keep L85 topk5/topk8/topk12 as an inset or adjacent table.
2. Latency trend with L94 clearly marked as latency/cost-only and non-comparable on EDD.
3. Quality issue count trend: L81 has 2 issue rows, L85 has 1, L91 and L95 have 0.
4. qv7_009 case panel: answer length/list count drops from L81 1142 chars / 20 derived list items to L89 605 chars / 5 items and stays clean in L91/L95.
5. qv7_006 latency breakdown: generation drops from L81 19.90s and $0.009889 to L94/L95 zero generation and zero generation cost.
6. Scoreboard-vs-diagnostic separation: prior summary has 1 scoreboard row and 48 diagnostic-only rows; do not promote L81/L85/L91/L95 as fresh validation.
7. Observed cost trend: show marginal observed cost and cumulative spent where available; include L84 timeout as an unledgered-cost caveat.

All specs are in `report_graphs.contract.json` under `proposal.accepted_fields_or_changes`.
