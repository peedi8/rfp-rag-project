# Next Experiments Proposal

## Priority 1: L14 blind_judge_calibration_scored

Run the existing six-case blind judge calibration pack before trusting any new scored improvement. This is the cheapest useful red gate because L7/L8 already prepared the planted pass/fail cases and no-api runner.

- Expected signal: judge passes 2 grounded/proper-abstention cases and fails 4 planted bad cases.
- Cost mode: low judge-only, no answer generation.
- Success label: `judge_calibration_gate_pass`.
- Failure label: `judge_calibration_gate_fail_rubric_or_context_fix_required`.
- Loop point type: `red_gate_judge_calibration`.

## Priority 2: L15 prompt_report_ready_small_scored_sweep

Score `report_ready` against existing prompt variants on a tiny mixed fixed-retrieval set. This converts L13 from a no-api prompt candidate into a real, bounded signal.

- Expected signal: tied or better EDD plus improved directness, conciseness, citation clarity, or safety on A/B/C/D/H-style cases.
- Cost mode: low 6-8 case scored prompt sweep, same retrieval controls.
- Success label: `prompt_report_ready_passes_mixed_quality_safety_gate`.
- Failure label: `prompt_report_ready_regresses_grounding_safety_or_false_abstention`.
- Loop point type: `small_scored_prompt_candidate`.

## Priority 3: L16 adaptive_top_k_small_validation

Validate the opt-in adaptive top-k guard only after the red gates pass. Global top5 is already rejected; the useful question is whether the L11 guard preserves top8 depth for facility/payment cases while letting simple cases stay faster.

- Expected signal: qv3_010-style payment/facility questions route to effective top8 and preserve PG/payment details; simple cases stay top5 with real latency benefit.
- Cost mode: low small answer-plus-judge run after calibration.
- Success label: `adaptive_top_k_passes_quality_latency_gate`.
- Failure label: `adaptive_top_k_quality_regression_or_no_latency_value`.
- Loop point type: `small_scored_latency_candidate`.

Do not run broad top-k/fetch sweeps next. Keep first validation, measurement correction, no-judge diagnostics, and targeted retries labeled separately.
