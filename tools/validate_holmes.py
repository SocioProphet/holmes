#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
EXAMPLE = ROOT / "examples" / "holmes-surface.json"
REASONING_EXAMPLE = ROOT / "examples" / "holmes-proof-claim-contract.json"
SCHEMA_FILES = [
    SCHEMA_DIR / "holmes-surface.schema.json",
    SCHEMA_DIR / "holmes-proof-claim-contract.schema.json",
]
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
REQUIRED_INTEGRATIONS = {
    "standards",
    "platform",
    "search",
    "slashTopics",
    "lab",
    "sourceosCarry",
}
REQUIRED_MAPPINGS = {
    "Claim",
    "ProofCertificate",
    "ExplanationTrace",
    "ContradictionReport",
    "TruthBounds",
}
REQUIRED_HOLMES_SEGMENT = ["Propose", "Explain", "Verify"]
REJECTED_BEFORE_POLICY = "rejected_before_policy"
REQUIRED_REASONING_TRACE = {
    "ruleName",
    "premises",
    "conclusion",
    "evidenceRefs",
    "confidence",
    "truthBounds",
}


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def require_set(spec: dict, field: str, required: set[str]) -> int | None:
    observed = set(spec.get(field, []))
    missing = required - observed
    if missing:
        return fail(f"missing {field}: {sorted(missing)}")
    return None


def validate_schema_files() -> int | None:
    for schema_path in SCHEMA_FILES:
        if not schema_path.exists():
            return fail(f"missing schema: {schema_path.relative_to(ROOT)}")
        try:
            load_json(schema_path)
        except json.JSONDecodeError as exc:
            return fail(f"invalid schema JSON {schema_path.relative_to(ROOT)}: {exc}")
    return None


def validate_surface_data(data: dict, source: str = "HolmesSurface") -> int | None:
    if data.get("apiVersion") != "holmes.socioprophet.dev/v1":
        return fail(f"{source}: wrong apiVersion")
    if data.get("kind") != "HolmesSurface":
        return fail(f"{source}: wrong kind")
    metadata = data.get("metadata", {})
    if not metadata.get("name") or not metadata.get("version"):
        return fail(f"{source}: missing metadata.name or metadata.version")
    spec = data.get("spec", {})
    if spec.get("product") != "Holmes":
        return fail(f"{source}: spec.product must be Holmes")
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
    missing_integrations = sorted(REQUIRED_INTEGRATIONS - set(integrations.keys()))
    if missing_integrations:
        return fail(f"{source}: missing integrations: {missing_integrations}")
    return None


def validate_surface(path: Path = EXAMPLE) -> int | None:
    if not path.exists():
        return fail(f"missing {path.relative_to(ROOT)}")
    try:
        data = load_json(path)
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
    return validate_surface_data(data, str(path.relative_to(ROOT)))


def validate_reasoning_contract_data(reasoning: dict, source: str = "HolmesReasoningContract") -> int | None:
    if reasoning.get("apiVersion") != "holmes.socioprophet.dev/v1":
        return fail(f"{source}: wrong reasoning contract apiVersion")
    if reasoning.get("kind") != "HolmesReasoningContract":
        return fail(f"{source}: wrong reasoning contract kind")
    metadata = reasoning.get("metadata", {})
    if not metadata.get("name") or not metadata.get("version"):
        return fail(f"{source}: missing metadata.name or metadata.version")
    reasoning_spec = reasoning.get("spec", {})
    if reasoning_spec.get("candidateOnlyStatus") != "candidate_only":
        return fail(f"{source}: candidateOnlyStatus must be candidate_only")
    actual_segment = reasoning_spec.get("holmesOwnedSegment", [])
    if actual_segment != REQUIRED_HOLMES_SEGMENT:
        return fail(
            f"{source}: holmesOwnedSegment must be ordered exactly as [Propose, Explain, Verify]; "
            f"got {actual_segment}"
        )
    mappings = set(reasoning_spec.get("contractMappings", {}).keys())
    missing_mappings = REQUIRED_MAPPINGS - mappings
    if missing_mappings:
        return fail(f"{source}: missing contract mappings: {sorted(missing_mappings)}")
    worked_examples = reasoning_spec.get("workedExamples", {})
    for key in ["documentSpanToPolicyReadyClaim", "vectorCandidateVerificationPath"]:
        if key not in worked_examples:
            return fail(f"{source}: missing worked example: {key}")
    doc_example = worked_examples["documentSpanToPolicyReadyClaim"]
    reasoning_trace = doc_example.get("reasoningTrace", [])
    if not reasoning_trace:
        return fail(f"{source}: documentSpanToPolicyReadyClaim must include reasoningTrace")
    for index, entry in enumerate(reasoning_trace):
        missing_reasoning_fields = REQUIRED_REASONING_TRACE - set(entry.keys())
        if missing_reasoning_fields:
            return fail(
                f"{source}: missing reasoningTrace fields at index {index}: {sorted(missing_reasoning_fields)}"
            )
    vector_example = worked_examples["vectorCandidateVerificationPath"]
    if vector_example.get("candidateClaim", {}).get("status") != "candidate_only":
        return fail(f"{source}: vector candidateClaim status must be candidate_only")
    if vector_example.get("verificationPath", {}).get("result") != REJECTED_BEFORE_POLICY:
        return fail(f"{source}: vector verification path result must be rejected_before_policy")
    return None


def validate_reasoning_contract(path: Path = REASONING_EXAMPLE) -> int | None:
    if not path.exists():
        return fail(f"missing {path.relative_to(ROOT)}")
    try:
        reasoning = load_json(path)
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
    return validate_reasoning_contract_data(reasoning, str(path.relative_to(ROOT)))


def main() -> int:
    for validator in [validate_schema_files, validate_surface, validate_reasoning_contract]:
        result = validator()
        if result is not None:
            return result
    print("OK: Holmes contracts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
