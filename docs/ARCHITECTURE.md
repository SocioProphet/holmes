# Holmes Architecture

## Objective

Holmes is the governed language intelligence fabric for SocioProphet.

It connects classical NLP, neural NLP, retrieval, semantic graphs, foundation-language services, guardrails, evals, tools, and agents into an evidence-first discovery product.

## Product components

### Sherlock Search

Discovery, retrieval, evidence search, and investigation.

### 221B

Casefile and workspace surface for investigations, projects, and review bundles.

### Mycroft

Model routing, policy intelligence, cost/latency/quality/privacy selection, and fallback strategy.

### Moriarty Bench

Adversarial evals, prompt-injection tests, retrieval sabotage tests, hallucination regression tests, and safety regressions.

### Irene Shield

Privacy, PII masking, source masking, consent boundaries, identity-sensitive redaction, and sensitive-context handling.

### The Canon

Curated evidence corpus, provenance-backed accepted facts, citation records, source trust records, and knowledge-base manifests.

### Deduction Engine

Claim extraction, contradiction detection, fallacy analysis, summarization, synthesis, and report generation.

## Data flow

```text
ingest
  -> linguistic analysis
  -> extraction and normalization
  -> retrieval and graph conversion
  -> guarded foundation-language services
  -> deduction and casefile assembly
  -> evidence records and promotion outputs
```

## Service boundaries

Holmes should not embed every model or data source directly. It should compose governed services:

- functional model surfaces from `functional-model-surfaces`;
- runtime platform services from `prophet-platform`;
- search and retrieval from `sherlock-search`;
- local NLP lab outputs from `SociOS-Linux/nlplab`;
- SourceOS client references from `sourceos-model-carry`.

## Internal transport

Internal services should be TriTRPC-first. Gateway routes may exist for web clients and third-party integration.

Recommended method families:

- `language.primitive.v1/Analyze`
- `language.entity.v1/Extract`
- `language.relation.v1/Extract`
- `language.classify.v1/Classify`
- `language.embed.v1/Embed`
- `language.rerank.v1/Rerank`
- `language.translate.v1/Translate`
- `language.summarize.v1/Summarize`
- `language.rag.v1/Answer`
- `language.graph.v1/ToSemanticGraph`
- `language.govern.v1/Evaluate`

## Promotion rule

No Holmes pipeline, model, adapter, retrieval package, or agent route becomes stable without:

1. dataset or corpus reference;
2. pipeline or model artifact reference;
3. eval record;
4. guardrail policy;
5. evidence receipt;
6. signed promotion record;
7. rollback reference.
