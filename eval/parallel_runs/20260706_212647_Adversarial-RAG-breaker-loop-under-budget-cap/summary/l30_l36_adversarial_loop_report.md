# L30-L36 Adversarial Loop Report

## Purpose

This loop deliberately moved away from saturated easy metrics. The goal was to find questions that look like real user behavior: partial project titles, pushy unsupported requests, privacy traps, similar project contamination, and paraphrase instability.

## Loop Points

| point | label | score type | EDD | coverage | groundedness | relevance | abstention | latency | decision |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| L30 | v5 adversarial first baseline | first validation score | 92.40 | 0.929 | 5.000 | 5.000 | 1.000 | 20.776 | keep as first v5 evidence |
| L31 | title-fragment issuer filter | local retrieval diagnostic | N/A | N/A | N/A | N/A | N/A | N/A | keep code patch |
| L32 | v5 title-filter baseline raw | targeted fix score raw | 95.87 | 1.000 | 5.000 | 5.000 | 0.750 | 15.151 | measurement issue found |
| L33 | v5 title-filter baseline recomputed | same-answer measurement correction | 98.37 | 1.000 | 5.000 | 5.000 | 1.000 | 15.151 | keep as targeted evidence only |
| L34 | v5 top5 recomputed | same-answer measurement correction | 98.70 | 1.000 | 5.000 | 5.000 | 1.000 | 13.724 | do not promote globally |
| L35 | v4 title-filter baseline regression | regression score | 96.81 | 1.000 | 5.000 | 5.000 | 1.000 | 22.035 | keep patch with latency note |
| L36 | v4 top5 regression | regression score | 96.44 | 1.000 | 5.000 | 5.000 | 1.000 | 23.683 | reject top5 default |

## What Broke

- L30 exposed the real weakness: `qv5_010c` contained the project title fragment `EIP3.0 고압가스 안전관리 시스템` but did not name the issuer. The existing issuer filter only used organization aliases, so retrieval drifted into unrelated safety/system documents.
- L30 also showed that the prior metrics were too saturated. The new set lowered EDD to `92.40` with one false abstention and five context-contamination flags.
- The issue was not answer formatting. It was source scope: the correct project was present in the index, but the filter did not know how to use long project-title fragments.

## What Changed

- `src/retriever.py` now builds a cached map of known project titles to issuing organizations.
- If no organization alias is found, auto filtering tries a stricter title-fragment match.
- The title rule requires a long contiguous overlap and ratio checks, so generic strings such as "정보시스템 구축" should not force a wrong issuer.
- Normalization now lowercases Latin text so `eip` and `EIP` behave the same.

## Results

- L31 retrieval diagnostics showed all v5 cases now get explainable filters. The comparison case keeps both target organizations with `$in`.
- L32 raw v5 baseline recovered coverage from `0.929` to `1.000` and cut average latency from `20.776s` to `15.151s`, but the evaluator missed one valid sensitive-example refusal.
- L33 recomputed the same L32 answers after the narrow refusal detector fix: EDD `98.37`.
- L34 recomputed the v5 top5 answers: EDD `98.70`, latency `13.724s`.
- L35 checked v4 regression: correctness metrics stayed saturated, but latency was `22.035s`, below the earlier L25 score because L25 was faster.
- L36 checked v4 top5: EDD `96.44`, with no useful latency advantage. This blocks promoting top5 as the global default.

## Red Review

- The v5 post-fix scores are not fresh holdout evidence. L30 exposed the failure, then L31-L34 fixed and remeasured the same set.
- The real generalizable improvement is the source-scope mechanism: title-fragment matching fixes a plausible user query pattern without relying on a single hardcoded case.
- The best honest report language is: "v5 first run found a title-fragment retrieval failure; a general title-fragment issuer filter repaired it on the exposed v5 set; v4 regression showed no correctness break, but no new global best."
- Do not promote global top5. It is attractive on v5, but v4 does not confirm a latency/quality win.
- Current v4 promotable evidence remains L25 EDD `97.41`; L33/L34 are targeted/exposed-set evidence.

## Artifacts

- v5 questions: `eval\questions_v5_adversarial_frozen_first_run.json`
- L30 analysis: `summary\l30_adversarial_analysis\adversarial_analysis.md`
- L31 analysis: `summary\l31_adversarial_analysis\adversarial_analysis.md`
- L32 analysis: `summary\l32_adversarial_analysis\adversarial_analysis.md`
- L33 recompute: `analysis\l34_l31_sensitive_abstention_recompute\recomputed_metrics.md`
- L34 recompute: `analysis\l34_l32_top5_sensitive_abstention_recompute\recomputed_metrics.md`
- L36 recompute: `analysis\l36_l35_top8_procurement_marker_recompute\recomputed_metrics.md`
- aggregate charts: `summary\edd_score.svg`, `summary\metric_heatmap.svg`, `summary\quality_vs_retrieval.svg`, `summary\latency_vs_edd.svg`
- budget note: `summary\l30_l36_budget_note.md`

## Next Best Work

- Build a small v6 set from still-unseen project titles to test whether title-fragment filtering generalizes beyond v5.
- Add a no-answer diagnostic for false title matches using short/generic fragments.
- Add a qualitative answer review for L33/L34 because EDD is again near ceiling.
- Investigate latency variance before claiming a speed gain.
