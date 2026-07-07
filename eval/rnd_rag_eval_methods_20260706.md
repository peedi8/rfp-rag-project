# R&D note: RAG improvement methods beyond question diversification

Date: 2026-07-06

## Local R&D lookup

The local R&D Workbench did not contain existing RAG evaluation test packs, references, or saved local evidence for this topic. I therefore treated the external sources below as new research leads, not as already-vetted project doctrine.

## Useful methods for the next loops

1. Component-wise RAG evaluation
   - Split retrieval quality, context relevance, answer relevance, faithfulness/groundedness, and abstention instead of treating EDD as one opaque score.
   - Project fit: keep EDD, but add per-case failure labels for retrieval miss, retrieval contamination, generator miss, unsupported claim, and over-refusal.

2. Metamorphic/property tests
   - Same intent with different wording should keep the same answer and evidence.
   - Adding irrelevant documents should not change the answer.
   - Removing the only supporting evidence should force abstention or "not found in documents."
   - Project fit: make v6 include paraphrase invariance, irrelevant-context injection, and evidence-removal checks.

3. Corpus perturbation and negative controls
   - Inject near-duplicate wrong documents, remove gold chunks, shuffle rank positions, or provide only generic title fragments.
   - Project fit: make v7 test title-fragment false positives and decoy chunk attraction.

4. Claim-level citation audit
   - Break an answer into atomic claims and require each factual claim to map to retrieved evidence.
   - Project fit: create unsupported-claim rate and citation clarity metrics for high-EDD answers that still feel weak to a human reviewer.

5. Judge calibration and disagreement checks
   - Before trusting a judge, run planted pass/fail examples: hallucinated answer, wrong-document evidence, over-refusal, and too-long-but-correct answer.
   - Project fit: keep L20-L24 style calibration as a gate before new scored runs.

6. Statistical and exposure gates
   - Small EDD gains on exposed sets should not be promoted as general performance.
   - Project fit: require first-run frozen-set evidence, minimum effect size, and explicit labels for exposed-set retry, same-answer recompute, diagnostic-only, and candidate-only results.

7. Latency and cost decomposition
   - Separate retrieval, filtering/reranking, generation, and judge time/cost.
   - Project fit: make v9 measure where the 17-25s latency actually comes from before changing top_k globally.

## Source leads

- Ragas metrics: https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/
- TruLens RAG Triad: https://www.trulens.org/getting_started/core_concepts/rag_triad/
- LlamaIndex retrieval metrics: https://developers.llamaindex.ai/python/framework-api-reference/evaluation/metrics/
- ARES: https://arxiv.org/abs/2311.09476
- RAGChecker: https://arxiv.org/abs/2408.08067
- LangSmith RAG evaluation tutorial: https://docs.langchain.com/langsmith/evaluate-rag-tutorial
- DeepEval faithfulness metric: https://deepeval.com/docs/metrics-faithfulness

## Proposed loop order

- v6: unseen title-fragment and metamorphic checks.
- v7: corpus perturbation and generic-title false-positive traps.
- v8: claim-level citation audit plus human-readable evidence-fit review.
- v9: latency/cost trace and minimum-effect-size gate.
