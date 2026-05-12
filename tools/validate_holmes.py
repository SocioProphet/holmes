#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "holmes-surface.json"
REQUIRED_COMPONENTS = {
    "sherlock-search",
    "221b",
    "mycroft-router",
    "moriarty-bench",
    "irene-shield",
    "the-canon",
    "deduction-engine",
}
REQUIRED_COMPONENT_FAMILIES = {
    "basic-primitives",
    "advanced-primitives",
    "rule-techniques",
    "classical-ml",
    "neural-nlp",
    "transformers",
    "foundation-language-services",
    "retrieval-and-knowledge",
    "guardrails-and-governance",
    "agent-and-tool-orchestration",
}
REQUIRED_NLP_TASKS = {
    "language-identification",
    "sentence-segmentation",
    "tokenization",
    "lemmatization",
    "part-of-speech-tagging",
    "morphological-features",
    "dependency-parsing",
    "semantic-role-labeling",
    "entity-extraction",
    "numeric-entity-extraction",
    "pii-extraction",
    "coreference-resolution",
    "relation-extraction",
    "text-classification",
    "zero-shot-classification",
    "sentiment-classification",
    "target-sentiment-extraction",
    "keyword-extraction",
    "category-classification",
    "concept-linking",
    "topic-modeling",
    "topic-model-training",
    "topic-taxonomy-induction",
    "topic-pack-generation",
    "topical-clustering",
    "text-similarity",
    "table-header-identification",
    "claim-extraction",
    "contradiction-detection",
    "semantic-graph-conversion",
    "evidence-governance",
}
REQUIRED_METHOD_FAMILIES = {
    "language.topic.v1/Propose",
    "language.topic.v1/Train",
}
REQUIRED_EVIDENCE = {
    "corpusRef",
    "pipelineOrModelRef",
    "algorithmFamily",
    "taskContract",
    "evalRecord",
    "latencyFootprintRecord",
    "slashTopicsTrainingRef",
    "guardrailPolicy",
    "evidenceReceipt",
    "promotionRecord",
    "rollbackRef",
}


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def require_set(spec: dict, field: str, required: set[str]) -> int | None:
    observed = set(spec.get(field, []))
    missing = required - observed
    if missing:
        return fail(f"missing {field}: {sorted(missing)}")
    return None


def main() -> int:
    if not EXAMPLE.exists():
        return fail("missing examples/holmes-surface.json")
    data = json.loads(EXAMPLE.read_text())
    if data.get("apiVersion") != "holmes.socioprophet.dev/v1":
        return fail("wrong apiVersion")
    if data.get("kind") != "HolmesSurface":
        return fail("wrong kind")
    spec = data.get("spec", {})
    for field, required in [
        ("components", REQUIRED_COMPONENTS),
        ("componentFamilies", REQUIRED_COMPONENT_FAMILIES),
        ("nlpTasks", REQUIRED_NLP_TASKS),
        ("methodFamilies", REQUIRED_METHOD_FAMILIES),
        ("requiredPromotionEvidence", REQUIRED_EVIDENCE),
    ]:
        result = require_set(spec, field, required)
        if result is not None:
            return result
    integrations = spec.get("integrations", {})
    for key in ["standards", "platform", "search", "slashTopics", "lab", "sourceosCarry"]:
        if key not in integrations:
            return fail(f"missing integration: {key}")
    print("OK: Holmes contracts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
