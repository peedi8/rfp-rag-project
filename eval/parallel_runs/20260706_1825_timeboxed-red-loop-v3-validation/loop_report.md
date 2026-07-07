# Timeboxed Loop Report: v3 Validation

- start: 2026-07-06 18:25 KST
- target boundary: 2026-07-06 20:00 KST
- questioner: local Codex reasoning from project files, no question-generation API call
- run directory: `eval\parallel_runs\20260706_1825_timeboxed-red-loop-v3-validation`

## Loop Points

| point | label | score type | EDD | coverage | groundedness | relevance | abstention | latency | decision |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| L0 | v3_first_validation_top8_raw | first validation raw | 89.69 | 1.000 | 5.000 | 5.000 | 0.333 | 24.021 | keep as first evidence |
| L1 | v3_top8_same_answers_recomputed | measurement correction | 96.36 | 1.000 | 5.000 | 5.000 | 1.000 | 24.021 | current best quality point |
| L2 | v3_top5_speed_probe_raw | targeted speed probe raw | 91.41 | 1.000 | 4.667 | 4.778 | 0.667 | 21.372 | reject global default |
| L3 | v3_top5_same_answers_recomputed | measurement correction | 94.74 | 1.000 | 4.667 | 4.778 | 1.000 | 21.372 | reject global default |
| L4 | qv3_010_admin_alias_filter_fix | local retrieval diagnostic | N/A | N/A | N/A | N/A | N/A | N/A | keep for next probe |
| L5 | short_alias_false_positive_guard | local retrieval diagnostic | N/A | N/A | N/A | N/A | N/A | N/A | keep patch |
| L6 | qv3_010_filtered_source_evidence_probe | local source evidence diagnostic | N/A | N/A | N/A | N/A | N/A | N/A | keep for targeted rerun |
| L7 | blind_judge_calibration_pack | local judge validation preparation | N/A | N/A | N/A | N/A | N/A | N/A | keep for future judge run |
| L8 | blind_judge_calibration_runner_no_api | local runner validation | N/A | N/A | N/A | N/A | N/A | N/A | ready for optional judge run |
| L9 | qv3_010_top5_targeted_answer_probe | no-judge targeted answer probe | N/A | 1.000 | N/A | N/A | N/A | 18.660 | reject top5 for PG detail |
| L10 | qv3_010_top8_targeted_answer_probe | no-judge targeted answer probe | N/A | 1.000 | N/A | N/A | N/A | 18.160 | prefer top8 for qv3_010 |
| L11 | adaptive_top_k_facility_payment_guard | local code guard validation | N/A | N/A | N/A | N/A | N/A | N/A | keep for future adaptive eval |
| L12 | representative_answer_quality_review_matrix | qualitative review no-api | N/A | N/A | N/A | N/A | N/A | N/A | keep for report and next prompt loop |
| L13 | report_ready_prompt_candidate | local prompt candidate no-api | N/A | N/A | N/A | N/A | N/A | N/A | keep for future scored prompt sweep |
| L14 | headless_red_overfit_gate_audit | headless gate audit no-api | N/A | N/A | N/A | N/A | N/A | N/A | keep as headless gate |
| L15 | headless_runner_no_api_self_check | headless runner no-api | N/A | N/A | N/A | N/A | N/A | N/A | keep runner pending cost gate |
| L16 | fresh_v4_validation_draft_noapi | fresh question draft no-api | N/A | N/A | N/A | N/A | N/A | N/A | keep as unscored validation candidate |
| L17 | question_exposure_registry_noapi | overfit registry no-api | N/A | N/A | N/A | N/A | N/A | N/A | keep for overfit gate |
| L18 | registry_connected_gate_classifier_fix | headless gate classifier fix no-api | N/A | N/A | N/A | N/A | N/A | N/A | keep gate fix |
| L19 | v4_frozen_first_run_manifest | v4 freeze no-api | N/A | N/A | N/A | N/A | N/A | N/A | keep for first scored run |
| L20 | blind_judge_calibration_budgeted_original_pack | judge calibration paid | N/A | N/A | N/A | N/A | N/A | N/A | partial fail; hold scored gate |
| L21 | blind_judge_scale_guard_noapi | local judge guard no-api | N/A | N/A | N/A | N/A | N/A | N/A | keep for retest |
| L22 | blind_judge_calibration_scale_guard_original_pack | judge calibration paid | N/A | N/A | N/A | N/A | N/A | N/A | reject until pack clean |
| L23 | strict_calibration_pack_cleaning_noapi | calibration pack fix no-api | N/A | N/A | N/A | N/A | N/A | N/A | keep strict pack |
| L24 | blind_judge_calibration_strict_pack | judge calibration paid | N/A | N/A | N/A | N/A | N/A | N/A | open v4 scored gate |
| L25 | v4_first_baseline_top8 | first validation score | 97.41 | 1.000 | 5.000 | 5.000 | 1.000 | 19.377 | best v4 first evidence |
| L26 | v4_top5_speed_probe | targeted speed probe | 97.12 | 1.000 | 5.000 | 4.889 | 1.000 | 18.725 | reject global top5 |
| L27 | v4_report_ready_prompt | prompt probe | 95.00 | 1.000 | 5.000 | 5.000 | 1.000 | 30.681 | reject prompt default |
| L28 | v4_concise_verified_prompt_raw | prompt probe raw | 86.42 | 1.000 | 5.000 | 5.000 | 0.000 | 23.754 | measurement issue found |
| L29 | v4_concise_verified_same_answers_recomputed | measurement correction | 96.42 | 1.000 | 5.000 | 5.000 | 1.000 | 23.754 | reject after recompute |

Chart artifact: `analysis\loop_points_chart.svg`

## What Improved

- The new v3 validation set produced a first raw score of **89.69**, lower than the tuned/remeasured v2 scores, so it successfully reduced metric saturation.
- Retrieval stayed strong on v3: coverage, hit-all, and MRR were all **1.0**.
- The largest raw failure was not answer generation. It was the evaluator missing correct abstentions in `qv3_006` and `qv3_012`.
- A narrow abstention taxonomy correction changed the same top8 answers from **89.69** to **96.36**. This is a measurement correction, not a new RAG run.

## What Got Worse

- `top_k=5` reduced average latency from **24.021s** to **21.372s**, but this was only about **2.65s** average improvement.
- The top5 answer quality dropped: groundedness **5.000 -> 4.667**, relevance **5.000 -> 4.778**.
- The clearest regression was `qv3_010_casual_anyang_sports_reservation`: top8 answered reservation/payment/member operation correctly, while top5 incorrectly said payment/PG details were not available.

## Root Cause Notes

- `qv3_006` and `qv3_012` showed the same pattern as earlier missed abstention cases: the answer correctly said the requested information was not in the documents, but the detector required a narrower wording.
- `qv3_008` in the top5 run exposed a shorter form: "final score and selected vendor cannot be confirmed" in one sentence. The detector now handles procurement-result markers when at least two such fields are present.
- `qv3_010` shows why global top5 is risky. The saved pre-L4 retrieval org list mixed `경기도 안양시` with nearby sports-facility documents from `고양도시관리공사`, `전북특별자치도 정읍시`, and `대한장애인체육회`; fewer context chunks made that source-scope mix more damaging, so top5 omitted payment/PG details that top8 recovered.
- L4 fixed a local retrieval cause without spending answer/judge calls: the query said "안양 호계체육관" rather than "안양시", so the organization filter did not activate. Short municipality aliases now map `안양`, `평택`, `봉화`, and `정읍`-style mentions to the issuing organization when they come from an administrative org name.
- L4 diagnostic artifact: `analysis\l4_admin_alias_filter\diagnostic.md`. It verifies `안양 -> 경기도 안양시`, `평택 -> 경기도 평택시`, `봉화 -> 경상북도 봉화군`, and `정읍 -> 전북특별자치도 정읍시` without answer generation or judge calls.
- L5 stress-tested the new short aliases for false positives. Before the guard, `안양대학교`, `평택대학교`, `봉화산역`, and `안양천` over-matched to municipality issuers. The guard now blocks short aliases before university/station/river suffixes while preserving valid facility/project queries.
- L5 diagnostic artifact: `analysis\l5_alias_false_positive_stress\diagnostic.md`.
- L6 checked the actual source evidence under the fixed `경기도 안양시` filter without answer/judge calls. The filtered set contains 106 chunks from `호계체육관 배드민턴장 및 탁구장 예약시스템 구축 용역`; term hits include 예약 39, 결제 7, PG 2, 회원 8, 키오스크 13, 발권 3, 매출 4, 무인 5.
- L6 diagnostic artifact: `analysis\l6_qv3_010_source_scope_probe\diagnostic.md`.
- L7 created a blind judge calibration pack without judge calls. It contains planted pass/fail answers for grounded qv3_010, contradicted PG/payment evidence, wrong-document bleed, proper abstention, fabricated vendor/contact data, and same-issuer scope mix.
- L7 artifact: `analysis\l7_blind_judge_calibration_pack\calibration_pack.md` / `.json`.
- L8 added and validated `scripts\run_blind_judge_calibration.py` in no-api mode. The runner loaded the L7 pack and wrote expected-only outputs with 6 cases, expected pass 2, expected fail 4.
- L8 artifact: `analysis\l8_blind_judge_calibration_runner_no_api\calibration_results.md` / `.json`.
- L9 ran a single qv3_010 top5 answer without judge. The fixed filter worked: all 5 retrieved organizations were `경기도 안양시`. However, the answer still did not mention PG and said concrete payment processing details were unavailable.
- L9 artifact: `analysis\l9_qv3_010_targeted_answer_probe\diagnostic.md`.
- L10 ran the same qv3_010 question with top8 and no judge. All 8 retrieved organizations were `경기도 안양시`, and the answer recovered PG, 발권, 매출, 회원, 키오스크 details.
- L10 artifact: `analysis\l10_qv3_010_targeted_top8_answer_probe\diagnostic.md`.
- L11 added an opt-in `adaptive_top_k` guard in `src\rag.py`. When enabled, facility reservation/payment detail questions with multiple detail terms are upgraded from top5 to at least top8. A no-answer unit check verifies facility payment queries go to 8, simple BIS queries stay at 5, and disabled adaptive mode stays at 5.
- L12 reviewed 8 representative saved/planted answer cases without new model/API calls. The review separated automated score from human answer quality and produced `human_quality_avg=3.62`, `evidence_safety_score_avg=3.47`. A/B/C became high-score readability cautions, E/F/G became the clearest before/after retrieval story, and D/H became the safety contrast pair.
- L12 artifact: `eval\parallel_runs\20260706_193521_Representative-answer-quality-review-matrix-for-RFP-RAG-repo\summary\answer_quality_review_matrix.md` / `.json` / `.csv` / `.svg`.
- L13 converted the L12 answer-quality insight into a candidate prompt only. `src\generator.py` now has `report_ready`, and `scripts\run_experiment_worker.py` includes `prompt_report_ready` in `prompt_sweep`. Static and fake-client no-API checks passed.
- L13 artifact: `eval\parallel_runs\20260706_1946_answer-format-safety-loop\summary\answer_format_safety_loop.md` / `.json`.
- L14 added a headless red/overfit gate audit without model/API calls. It labels L0 as the best promotable first-validation evidence, L1 as a measurement correction only, L12 as qualitative evidence, and L13 as candidate-only.
- L14 artifact: `eval\parallel_runs\20260706_200022_headless-improvement-loop-with-red-and-overfit-gates\summary\headless_gate_report.md` and `summary\headless_loop_operating_rules.md`.
- L15 added and ran `scripts\run_headless_loop.py` in `no_api_gate_only` mode. The manifest runner regenerated gate state and chose `pending_cost_gate` because the next useful scored gate is blind judge calibration, which needs judge/API cost.
- L15 artifact: `eval\parallel_runs\20260706_200022_headless-improvement-loop-with-red-and-overfit-gates\summary\headless_runner\headless_runner_state.md` / `.json`.
- L16 created a fresh v4 draft question set without model/API calls. The draft uses organizations not present in the existing target-org registry at creation time and mixes single extraction, comparison, follow-up, sensitive scope guard, ISP-vs-build guard, and final-vendor/contact abstention.
- L16 artifact: `eval\questions_v4_draft_noapi.json` and `eval\questions_v4_draft_notes.md`.
- L17 added `scripts\build_exposure_registry.py` and generated `eval\question_exposure_registry.json` / `.md`. The registry marks v2 holdout as spent, v3 as exposed first-validation/regression evidence, and v4 draft as an unscored candidate until first run.
- L18 connected `eval\question_exposure_registry.json` to `scripts\headless_gate.py` and `scripts\run_headless_loop.py`. The first connected run exposed a classifier false positive: L14/L17 were briefly labeled candidate-only because the classifier searched explanatory text. The fix now uses row identity fields for candidate/measurement checks, and L14/L17 are diagnostic-only while L16 remains candidate-only.
- L19 added `scripts\freeze_question_set.py`, froze `eval\questions_v4_draft_noapi.json` to `eval\questions_v4_frozen_first_run.json`, and wrote `eval\questions_v4_frozen_first_run.manifest.json` with SHA256 `29441fe8e64c89086b2bac4ea98d0058b5121dc6dfa9b556301eedd0f6f2ee80`. The exposure registry and gate report were regenerated.

## Red Review

- L1 is the best current point for quality, but it must be labeled as `measurement_correction_same_answers`.
- L0 remains the honest first-seen raw validation score.
- L3 does not beat L1. The speed gain is not worth the quality loss, so global top5 should not be adopted.
- L5 is accepted because it reduces a known overfit/false-positive risk introduced by L4 without changing answer generation behavior.
- L6 supports a targeted rerun hypothesis: qv3_010 should not need broader context if the fixed filter is applied, because payment/PG/member evidence exists inside the correct issuer scope.
- L7 should be run before trusting another near-ceiling judge score. If the judge passes planted bad answers, the judge/rubric must be fixed before reporting final quality.
- L8 makes the L7 check repeatable and checkpointed, so a future paid judge call can be bounded to the planted 6-case pack instead of rerunning broad experiments.
- L9/L10 isolate the remaining top5 problem: after source-scope cleanup, top5 is still too narrow for qv3_010's payment/PG detail. Top8 is the safer setting for this question type.
- L11 encodes that lesson without changing the current default top8 behavior. It prepares a future adaptive latency experiment without forcing a risky global top5 default.
- L12 confirms that the remaining quality gap is not only retrieval. Even high-scoring answers can be too long or hard to cite, so human-readable answer structure deserves its own loop.
- L13 is accepted as a prompt candidate because it does not mutate defaults and does not claim a score improvement before a judge-enabled run.
- L14 is accepted because it prevents the headless loop from mistaking the highest number for the best evidence. It explicitly keeps same-answer recomputation, no-judge probes, diagnostics, and prompt candidates out of performance promotion.
- L15 is accepted because it proves the gate can be rerun from a manifest without API cost. It also correctly refuses to launch the next scored gate while the manifest disallows API spending.
- L16 is accepted as preparation for future validation, not as validation itself. Once answers/retrieval/failures are inspected, this set must be treated as exposed and cannot be used as untouched evidence without labeling.
- L17 is accepted because it turns overfit/contamination status into a machine-readable artifact instead of relying on memory. Future automation should consult this registry before promoting a score.
- L18 is accepted because it treats the gate itself as testable software. The gate produced an incorrect label, the root cause was identified, and the rerun produced the intended classification.
- L19 is accepted because it makes the next first scored v4 run reproducible. Any later change to the frozen file can be detected by the manifest hash.
- The v3 questions were generated locally from file names and project context, not by a separate external questioner. They are still new to the RAG answer path, but not an independent external benchmark.
- The judge may still be lenient because it is automated. Blind calibration with planted wrong answers remains required before claiming final quality.

## Decision

- Current best loop point: **L1 top8 after measurement correction, EDD 96.36**.
- Do not promote top5 globally.
- Stop additional paid/API-heavy experimentation for this timebox unless a small no-answer rerun or local analysis is needed.
- L4-L8 are local diagnostics/preparations, not new performance scores. L9-L10 are no-judge targeted answer probes and their EDD-like no-judge rows must not be used as performance scores.
- L11 is a local code guard, not a performance score. Next meaningful loop should be a small adaptive-top-k eval on mixed easy/detail-heavy questions, or executing the L7/L8 judge calibration path if judge spending becomes acceptable.
- L12-L13 are quality-review and prompt-candidate steps, not performance scores. The next scored prompt step should compare `prompt_report_ready` in `prompt_sweep` without changing retrieval settings.
- L14 defines the continuing headless rule: loops may continue, but only fresh scored validation rows with complete judge metrics and no red/overfit flags can be promoted.
- L15 defines the safe no-api runner state: until cost is allowed, continue with gate maintenance, manifests, logs, and fresh question drafts without scored claims.
- L16 gives the next no-api validation candidate. It should be frozen before any scored run, and first-run scores must be preserved separately from later fixes.
- L17 provides the exposure registry that future gates should use to block spent holdout or diagnostic-only sets from being promoted as fresh validation.
- L18 proves the gate report should be treated like any other implementation: it needs regression checks because bad labels can create false confidence.
- L19 prepares the next strict first-run candidate. Do not inspect answers/failures from this frozen set before recording the first scored result.

## Budgeted Extension L20-L29

### What changed

- L20 used the original planted judge calibration pack under a cost cap. It was directionally useful but not sufficient: pass/fail matched 6/6, but groundedness bounds matched only 5/6 and the old runner did not yet validate score range.
- L21 added explicit 0-5 score-scale instructions and score-range validation to the calibration runner.
- L22 showed that the runner fix alone was not enough. Score range became stable, but one planted pass case failed because its answer included an ambiguous `web/kiosk` phrase not present in the evidence snippets.
- L23 preserved the original pack and created a stricter calibration pack by removing that ambiguous phrase.
- L24 passed strict calibration: decision match 6/6, decision value 6/6, score range 6/6, groundedness bounds 6/6. Actual recorded calibration cost through the ledger is $0.063527.
- L25 ran the frozen v4 question set for the first time after calibration and produced EDD 97.41 with complete quality metrics.
- L26 tested global top5 on the same v4 set. It reduced average latency by only 0.652s and lowered relevance to 4.889, so it is rejected as a default.
- L27 tested `report_ready`. It kept quality metrics but raised average latency to 30.681s, so it is rejected as a default.
- L28 tested `concise_verified`. The raw run looked like EDD 86.42 because the abstention detector missed `문서상 확인 불가`.
- L29 recomputed the same L28 answers after a narrow detector correction. EDD recovered to 96.42, but it still stays below L25 because latency is worse.

### Red Review

- L25 is the best current first-run validation row, but it is now exposed. Do not tune against v4 and then call the same set fresh validation again.
- L26-L29 are useful negative evidence. They show that shorter context or stricter prompt form can look appealing but still lose either relevance, latency, or both.
- L28/L29 are a measurement lesson, not model improvement. The answer already refused; the detector failed to recognize one valid refusal phrase.
- The score is again near saturation. Further runs on this same v4 set need a clear new failure hypothesis, otherwise they are likely to chase noise.

### Decision

- Current promotable v4 evidence: **L25, EDD 97.41**.
- Current rejected candidates: **L26 top5**, **L27 report_ready**, **L29 concise_verified after correction**.
- Next useful work should not be another same-set prompt tweak. Better next steps are either a fresh unseen validation set, a human readability audit of L25 answers, or a targeted latency investigation for `qv4_002`, `qv4_004`, and `qv4_008`.

## Adversarial Extension L30-L36

### What changed

- L30 ran a frozen v5 adversarial set for the first time. It deliberately included title-fragment questions, pushy unsupported requests, privacy traps, similar project contamination, paraphrase stability, and comparison cases.
- L30 result: EDD `92.40`, coverage `0.929`, MRR `0.929`, groundedness/relevance `5.0/5.0`, abstention accuracy `1.0`, latency `20.776s`.
- L30 exposed a real retrieval weakness: `qv5_010c` asked about `EIP3.0 고압가스 안전관리 시스템` without naming `한국생산기술연구원`, so auto filtering did not fire and unrelated documents were retrieved.
- L31 added strict project-title-fragment issuer filtering in `src\retriever.py`. If organization alias matching fails, the retriever now checks long project-title overlap and maps a unique title fragment to its issuing organization.
- L32 reran v5 after the title filter. Raw EDD rose to `95.87`; coverage/MRR reached `1.0`; average latency fell to `15.151s`. The remaining defect was measurement: the detector missed a valid refusal on a sensitive patient-example request.
- L33 recomputed the same L32 answers after a narrow sensitive-example abstention detector correction. EDD became `98.37`.
- L34 recomputed the v5 top5 answers after the same detector correction. EDD became `98.70`, but this remains exposed-set and same-answer evidence, not fresh validation.
- L35 checked v4 regression with the title filter. EDD was `96.81` with saturated correctness metrics, but latency was worse than L25.
- L36 checked v4 top5 regression. EDD was `96.44`; top5 did not beat L25 and did not provide a latency advantage.

### Red Review

- L30 is the honest first v5 evidence.
- L33/L34 are useful targeted evidence, but they are not fresh generalization scores because L30 exposed the failure before the fix.
- The project-title filter is accepted because it is a general source-scope rule, not a single hardcoded fix.
- The abstention detector corrections are measurement corrections only. They should not be described as model improvement.
- Do not promote global top5. It looks strong on v5 after correction, but v4 does not confirm a better default.
- Current promotable v4 evidence remains L25 EDD `97.41`.

### Artifacts

- Full L30-L36 report: `eval\parallel_runs\20260706_212647_Adversarial-RAG-breaker-loop-under-budget-cap\summary\l30_l36_adversarial_loop_report.md`
- v5 analysis: `summary\l30_adversarial_analysis`, `summary\l31_adversarial_analysis`, `summary\l32_adversarial_analysis`
- measurement corrections: `analysis\l34_l31_sensitive_abstention_recompute`, `analysis\l34_l32_top5_sensitive_abstention_recompute`, `analysis\l36_l35_top8_procurement_marker_recompute`
- updated chart: `analysis\loop_points_chart.svg`

### Decision

- Keep the title-fragment issuer filter.
- Keep L30 as first v5 evidence.
- Keep L33/L34 as targeted exposed-set evidence only.
- Keep L35/L36 as regression evidence.
- Next useful loop should create a small v6 set from unseen project-title fragments and generic-title traps, then test whether the title-fragment filter generalizes without false issuer narrowing.
