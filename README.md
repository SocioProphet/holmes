# Holmes

Holmes is SocioProphet's open language intelligence fabric.

It is built to outgrow assistant-grade discovery: classical NLP, neural NLP, semantic search, retrieval, knowledge graphs, foundation-language services, guardrails, evals, and investigative agentic discovery under one governed product surface.

## Product thesis

Watson-style systems answer. Holmes investigates.

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
8. Guardrails and governance: PII checks, source provenance, prompt-injection checks, policy gates, eval gates, factsheets, promotion records.
9. Agent and tool orchestration: tool contracts, agent identity, sessions, memory, MCP/A2A, execution traces, model routing.

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
