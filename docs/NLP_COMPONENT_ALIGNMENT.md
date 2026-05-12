# NLP Component Alignment

## Purpose

Holmes needs a disciplined NLP component map so it can support primitive analysis, task models, retrieval, evidence, semantic graph conversion, policy, topic-model training, and agentic investigation without becoming a loose model zoo.

This document records the lower-level NLP families Holmes must cover and how those families map across Holmes, nlplab, Sherlock Search, Slash Topics, and prophet-platform.

## Component map

| Family | Holmes surface | Lab/runtime owner | Sherlock and Slash Topics boundary |
| --- | --- | --- | --- |
| Basic primitives | `language.primitive.v1/Analyze` | `SociOS-Linux/nlplab` prototypes adapters; `prophet-platform` hosts stable services | Sherlock indexes primitive outputs only as pointer-backed evidence; Slash Topics may consume normalized language features as training evidence, not admitted topics |
| Advanced primitives | dependency parsing, semantic role labeling, coreference, morphology extensions | `nlplab` evaluates parser, SRL, and coreference adapters | Sherlock searches over parse, entity, and relation evidence; Slash Topics may use these structures for candidate topic boundaries and topic-feature extraction |
| Rule techniques | rule packs, gazetteers, dictionaries, regular expressions, table/header rules | `nlplab` keeps rule DSL experiments; Holmes promotes validated rule packs | Preserve rule version, policy decision, source, handling tags, evidence refs, and topic-pack training refs |
| Classical ML | CRF, SVM/logistic/maxent, clustering, topic modeling, similarity baselines | `nlplab` benchmarks and calibrates classical models | Sherlock retrieves model outputs with corpus, model, and eval refs; Slash Topics consumes clustering/topic assignments as governed topic-model candidates |
| Neural NLP | sequence/text models and embedding pipelines | `nlplab` handles PyTorch/ONNX experiments and benchmarks | Index spans, classes, and embedding metadata under evidence controls; Slash Topics consumes embeddings only through receipt-backed training packs |
| Transformers | token classification, text classification, relation extraction, embeddings, reranking, translation, summarization, RAG | `nlplab` evaluates candidate models; Mycroft routes by cost, quality, privacy, and latency | Search and rerank evidence packets under policy ceilings; topic-training outputs require corpus, eval, guardrail, and rollback records |
| Task models | entities, numeric entities, PII, sentiment, target sentiment, categories, concepts, keywords, relations, emotion, tone, topic assignments | Holmes exposes stable contract families after eval and promotion | Sherlock indexes outputs with provenance and confidence; Slash Topics receives topic seeds, labels, taxonomies, negative examples, and training receipts |

## Architectural claim

A component NLP library can extract spans, tags, classes, relations, and task predictions. Holmes must do more:

- bind every output to corpus, model, policy, eval, and evidence references;
- route among rule, classical, neural, transformer, and foundation-language paths using explicit cost, latency, quality, and privacy constraints;
- preserve source provenance and rollback metadata;
- convert selected outputs into semantic graph candidates;
- produce governed topic-training inputs for Slash Topics, including topic seeds, candidate labels, topic boundaries, negative examples, evaluation slices, and topic-pack generation receipts;
- support contradiction detection, claim extraction, and casefile assembly;
- keep retrieval, topic training, indexing, and truth promotion as separate surfaces;
- require promotion evidence before a pipeline becomes stable.

The target position is:

> Component NLP annotates. Holmes investigates, governs, retrieves, graphs, trains topic surfaces, reasons, and promotes with evidence.

## Slash Topics training alignment

Slash Topics are governed, signed, replayable scopes for search and knowledge surfaces. Holmes must help Slash Topics train new topic models by emitting evidence-bound training artifacts rather than opaque model outputs.

Holmes-owned outputs for Slash Topics should include:

1. `TopicSeedCandidate` records derived from keywords, concepts, entities, clusters, claims, and evidence spans;
2. `TopicBoundaryEvidence` records that separate positive, negative, adjacent, and ambiguous topic examples;
3. `TopicLabelCandidate` records with source spans, language, confidence, and curator-review status;
4. `TopicTaxonomyCandidate` records mapping broader, narrower, related, excluded, and membrane-scoped topic relations;
5. `SlashTopicTrainingRef` records pointing to corpus snapshots, model versions, rule packs, eval slices, policy decisions, and rollback refs;
6. `TopicPackGenerationReceipt` records for candidate `/topic` pack creation, replay, and promotion.

Holmes may propose topic-model candidates. Slash Topics owns topic-pack semantics and membranes. Policy Fabric owns admission. Sherlock indexes topic evidence and retrieval behavior. The Canon records accepted topic evidence and source trust.

No Holmes topic model may be promoted without:

- corpus snapshot and split manifest;
- topic taxonomy version;
- positive, negative, adjacent, and ambiguous examples;
- topic-model eval record;
- membrane/policy decision reference;
- training eligibility and redaction check;
- replayable topic-pack generation receipt;
- rollback reference.

## Algorithm selection doctrine

Holmes should not default every task to transformers.

Use rules when the variation space is bounded, latency requirements are strict, labels are unavailable, or policy-sensitive patterns need deterministic inspection.

Use classical ML when training must be fast, features are strong, labels exist, and the workload is CPU-bound or latency-sensitive.

Use neural non-transformer models when higher quality is required but transformer runtime cost is unacceptable.

Use transformers and foundation-language services when multilinguality, semantic abstraction, long-context synthesis, or task quality justifies compute cost and governance overhead.

Use hybrid pipelines when deterministic guards, statistical extraction, retrieval grounding, topic training, and foundation-language synthesis must be composed under one evidence contract.

## Required executable proof

Holmes should not claim runtime superiority until `nlplab` produces benchmark receipts for:

1. primitive quality and speed;
2. entity, relation, and classification metrics;
3. PII and sensitive-context precision/recall;
4. retrieval impact through Sherlock evidence packets;
5. semantic graph conversion fidelity;
6. Slash Topics topic-model training quality, topic-boundary precision/recall, and topic-pack replay fidelity;
7. policy propagation and rollback coverage;
8. cost, latency, and memory profiles across CPU and GPU lanes.

## Required records

The next standards and runtime work should define or import these records:

- `LanguageAnalysisRecord`;
- `PrimitiveSpan`;
- `EntityMention`;
- `RelationMention`;
- `ClassificationDecision`;
- `TopicAssignment`;
- `TopicSeedCandidate`;
- `TopicBoundaryEvidence`;
- `TopicLabelCandidate`;
- `TopicTaxonomyCandidate`;
- `SlashTopicTrainingRef`;
- `TopicPackGenerationReceipt`;
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
7. Slash Topics training reference when the output affects topic models or topic packs;
8. guardrail policy result;
9. evidence receipt;
10. promotion record;
11. rollback reference.

This keeps local labs, governed platform services, SourceOS clients, Slash Topics, and Sherlock retrieval connected without collapsing those layers into one monolith.
