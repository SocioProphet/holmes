# NLP Component Alignment

## Purpose

Holmes needs a disciplined NLP component map so it can support primitive analysis, task models, retrieval, evidence, semantic graph conversion, policy, and agentic investigation without becoming a loose model zoo.

This document records the lower-level NLP families Holmes must cover and how those families map across Holmes, nlplab, Sherlock Search, and prophet-platform.

## Component map

| Family | Holmes surface | Lab/runtime owner | Sherlock boundary |
| --- | --- | --- | --- |
| Basic primitives | `language.primitive.v1/Analyze` | `SociOS-Linux/nlplab` prototypes adapters; `prophet-platform` hosts stable services | Index primitive outputs only as pointer-backed evidence |
| Advanced primitives | dependency parsing, semantic role labeling, coreference, morphology extensions | `nlplab` evaluates parser, SRL, and coreference adapters | Search over parse, entity, and relation evidence without canonical-truth claims |
| Rule techniques | rule packs, gazetteers, dictionaries, regular expressions, table/header rules | `nlplab` keeps rule DSL experiments; Holmes promotes validated rule packs | Preserve rule version, policy decision, source, handling tags, and evidence refs |
| Classical ML | CRF, SVM/logistic/maxent, clustering, topic modeling, similarity baselines | `nlplab` benchmarks and calibrates classical models | Retrieve model outputs with corpus, model, and eval refs |
| Neural NLP | sequence/text models and embedding pipelines | `nlplab` handles PyTorch/ONNX experiments and benchmarks | Index spans, classes, and embedding metadata under evidence controls |
| Transformers | token classification, text classification, relation extraction, embeddings, reranking, translation, summarization, RAG | `nlplab` evaluates candidate models; Mycroft routes by cost, quality, privacy, and latency | Search and rerank evidence packets under policy ceilings |
| Task models | entities, numeric entities, PII, sentiment, target sentiment, categories, concepts, keywords, relations, emotion, tone | Holmes exposes stable contract families after eval and promotion | Sherlock indexes outputs with provenance and confidence |

## Architectural claim

A component NLP library can extract spans, tags, classes, relations, and task predictions. Holmes must do more:

- bind every output to corpus, model, policy, eval, and evidence references;
- route among rule, classical, neural, transformer, and foundation-language paths using explicit cost, latency, quality, and privacy constraints;
- preserve source provenance and rollback metadata;
- convert selected outputs into semantic graph candidates;
- support contradiction detection, claim extraction, and casefile assembly;
- keep retrieval and indexing separate from truth promotion;
- require promotion evidence before a pipeline becomes stable.

The target position is:

> Component NLP annotates. Holmes investigates, governs, retrieves, graphs, reasons, and promotes with evidence.

## Algorithm selection doctrine

Holmes should not default every task to transformers.

Use rules when the variation space is bounded, latency requirements are strict, labels are unavailable, or policy-sensitive patterns need deterministic inspection.

Use classical ML when training must be fast, features are strong, labels exist, and the workload is CPU-bound or latency-sensitive.

Use neural non-transformer models when higher quality is required but transformer runtime cost is unacceptable.

Use transformers and foundation-language services when multilinguality, semantic abstraction, long-context synthesis, or task quality justifies compute cost and governance overhead.

Use hybrid pipelines when deterministic guards, statistical extraction, retrieval grounding, and foundation-language synthesis must be composed under one evidence contract.

## Required executable proof

Holmes should not claim runtime superiority until `nlplab` produces benchmark receipts for:

1. primitive quality and speed;
2. entity, relation, and classification metrics;
3. PII and sensitive-context precision/recall;
4. retrieval impact through Sherlock evidence packets;
5. semantic graph conversion fidelity;
6. policy propagation and rollback coverage;
7. cost, latency, and memory profiles across CPU and GPU lanes.

## Required records

The next standards and runtime work should define or import these records:

- `LanguageAnalysisRecord`;
- `PrimitiveSpan`;
- `EntityMention`;
- `RelationMention`;
- `ClassificationDecision`;
- `TopicAssignment`;
- `SentimentDecision`;
- `KeywordCandidate`;
- `ClaimRecord`;
- `SemanticGraphCandidate`;
- `LanguagePipelineReceipt`;
- `HolmesEvidencePacket`.

## Promotion rule

A Holmes NLP component graduates only when it has:

1. corpus reference;
2. pipeline or model reference;
3. algorithm family declaration;
4. task contract;
5. quality evaluation;
6. latency and footprint measurement;
7. guardrail policy result;
8. evidence receipt;
9. promotion record;
10. rollback reference.

This keeps local labs, governed platform services, SourceOS clients, and Sherlock retrieval connected without collapsing those layers into one monolith.
