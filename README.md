# Holmes

Holmes is SocioProphet's open language intelligence fabric.

It is built to outgrow assistant-grade discovery: classical NLP, neural NLP, semantic search, retrieval, knowledge graphs, foundation-language services, guardrails, evals, and investigative agentic discovery under one governed product surface.

## Product thesis

Component NLP annotates. Holmes investigates.

Holmes is not a chatbot wrapper, a loose model zoo, or a domain NLP repo. It is the governed language layer above search, evidence, retrieval, casefiles, semantic graphs, tools, models, evals, and agents.

## Product family

- **Holmes**: language intelligence fabric.
- **Sherlock Search**: discovery, retrieval, evidence search, and investigation engine.
- **221B**: casefile and workspace surface.
- **Mycroft**: model routing, policy intelligence, and strategic model/service selection.
- **Moriarty Bench**: adversarial eval and red-team harness.
- **Irene Shield**: privacy, masking, identity-sensitive redaction, and sensitive-context handling.
- **The Canon**: curated evidence corpus, provenance records, accepted facts, and source trust.
- **Deduction Engine**: synthesis, contradiction detection, claim extraction, fallacy analysis, and reasoning workflows.

## Layer stack

1. Ingestion: documents, web, OCR handoff, transcripts, tables, metadata, language detection.
2. Linguistic primitives: tokenization, lemmatization, POS, morphology, parsing, NER, normalization.
3. Rule and table techniques: matchers, gazetteers, taxonomies, table extraction, rule-based relation extraction.
4. Classical ML NLP: classifiers, clustering, topic models, sentiment baselines, calibration, explainability.
5. Neural NLP: transformers, embeddings, rerankers, span extraction, relation extraction, multilingual encoders.
6. Foundation language services: extraction, summarization, generation, translation, RAG answering, long-context analysis, tool planning.
7. Retrieval and knowledge: sparse/dense/hybrid retrieval, vector stores, GraphBrain, semantic-serdes, ontogenesis, Slash Topics, Sherlock Search.
8. Topic-model training support: topic seeds, topic boundaries, candidate labels, taxonomy candidates, topic-pack generation receipts, and Slash Topics training references.
9. Guardrails and governance: PII checks, source provenance, prompt-injection checks, policy gates, eval gates, factsheets, promotion records.
10. Agent and tool orchestration: tool contracts, agent identity, sessions, memory, MCP/A2A, execution traces, model routing.

## Slash Topics training role

Holmes supports Slash Topics by producing governed topic-model training artifacts, not opaque topic labels.

For Slash Topics, Holmes emits or prepares topic seeds, positive/negative/adjacent/ambiguous boundary evidence, candidate labels, topic taxonomy candidates, eval slices, and replayable topic-pack generation receipts. Slash Topics owns `/topic` pack semantics and policy membranes; Holmes owns language evidence, candidate generation, model-training support, and promotion evidence required before a topic model or topic pack can become stable.

## NLP component alignment

Holmes explicitly covers these component families:

- basic primitives;
- advanced primitives;
- rule techniques;
- classical ML;
- neural NLP;
- transformers;
- foundation-language services;
- retrieval and knowledge;
- guardrails and governance;
- agent and tool orchestration.

The alignment contract is documented in [`docs/NLP_COMPONENT_ALIGNMENT.md`](docs/NLP_COMPONENT_ALIGNMENT.md). That document is the lower-layer NLP map for Holmes, nlplab, Sherlock Search, Slash Topics, and the platform runtime.

## Repo role

This repo is the Holmes product surface and integration spine.

Normative cross-surface standards live in `SocioProphet/functional-model-surfaces`.
Runtime service deployment should graduate into `SocioProphet/prophet-platform` when contracts and smoke tests are stable.
Linux-native NLP lab execution belongs in `SociOS-Linux/nlplab`.
SourceOS carries clients and signed service references through `SourceOS-Linux/sourceos-model-carry`.

## Initial validation

```bash
make validate
```

Expected result:

```text
OK: Holmes contracts validated
```
