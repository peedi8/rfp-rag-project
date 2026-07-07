# Checkpoint 02 - Worker Outputs

- `guard_boundary`: completed. Proposed keeping sensitive guard boundaries narrow, adding exact boundary regression coverage, and avoiding broad relaxation.
- `field_scorer`: completed. Proposed field-specific refusal evidence and mixed-answer handling so supported fields are not swallowed by global abstention.
- `rerun_analysis`: completed. Proposed L108/L109 comparison lens. Main review accepted the metric lens but tightened q002 classification from "measurement artifact" to "real over-refusal plus scorer blind spot."
- `report_gate`: completed. Proposed diagnostic-only labeling, strict-scoreboard separation, and red-team gates.

Additional orchestrator outputs:

- L109, L110, L111, and L112 worker output contracts under `worker_outputs/`.
- Analysis report: `analysis/l108_l112_nonqv8_guard_field_report.md`.
- Loop data: `analysis/l108_l112_loop_points.csv`.
- Trend graphic: `analysis/l108_l112_loop_points.svg`.
