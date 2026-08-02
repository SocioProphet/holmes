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
    "methodFamily",
    "nonAuthorityDeclaration",
}

# CHRONOS carrier alignment (sociosphere/docs/integration/neurosymbolic-chronos-alignment.md
# "Method families and CHRONOS roles" table + "Neuro-symbolic carrier boundary" section).
# Holmes's TruthBounds/ReasoningTrace mechanism is admissible under that doctrine's
# "LNN-style truth-bound propagation" row:
#   admissible use: report lower/upper truth bounds, formula-local inconsistency,
#                   interpretable formula structure
#   forbidden use:  claim global consistency, arbitrary entailment correctness,
#                   or learned rule structure
# This validator enforces that discipline as data, not just prose in PROOF_CLAIM_CONTRACT.md.
ALLOWED_METHOD_FAMILIES = {"LNN-style truth-bound propagation"}
REQUIRED_NON_AUTHORITY_FIELDS = {"consistencyScope", "doesNotAuthorize", "statement"}
# The forbidden-use claims a bounded local result must never be promoted to assert.
REQUIRED_FORBIDDEN_CLAIMS = {"global_consistency", "arbitrary_entailment_correctness"}
FORBIDDEN_CONSISTENCY_SCOPE = "global"
ADMISSIBLE_CONSISTENCY_SCOPES = {"formula_local"}

# Package-level CHRONOS carrier fields: the object crossing the governance boundary
# (Holmes -> Policy Fabric) must carry these alongside what the package already carries
# under existing Holmes vocabulary (e.g. evidenceRefs, explanationTrace.traceId,
# proofCertificate.verificationStatus / verificationPath.result, policyReadyClaim.admissionStatus)
# -- those are cross-referenced from chronosCarrier, not duplicated as new data.
REQUIRED_CHRONOS_CARRIER_FIELDS = {
    "sourceEvidenceRef",
    "methodOutputType",
    "groundingStatus",
    "validationStatus",
    "owningAuthorityPlane",
    "replayRef",
    "governanceDecision",
}
ALLOWED_GROUNDING_STATUSES = {"evidence_grounded", "ungrounded"}
REQUIRED_OWNING_AUTHORITY_PLANE = "SocioProphet/policy-fabric"


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


def validate_method_family_and_non_authority(entry: dict, source: str, index: int) -> int | None:
    """Enforce the LNN-style truth-bound propagation method-family tag and the
    non-authority declaration that a bounded local result must carry. This is the
    concrete, checkable form of the doctrine's forbidden-use column: a bounded
    truth-bound result must never be tagged as authorizing a global-consistency
    or arbitrary-entailment-correctness claim.
    """
    method_family = entry.get("methodFamily")
    if method_family not in ALLOWED_METHOD_FAMILIES:
        return fail(
            f"{source}: reasoningTrace[{index}].methodFamily must be one of "
            f"{sorted(ALLOWED_METHOD_FAMILIES)}; got {method_family!r}"
        )

    declaration = entry.get("nonAuthorityDeclaration")
    if not isinstance(declaration, dict):
        return fail(f"{source}: reasoningTrace[{index}].nonAuthorityDeclaration must be an object")

    missing_fields = REQUIRED_NON_AUTHORITY_FIELDS - set(declaration.keys())
    if missing_fields:
        return fail(
            f"{source}: reasoningTrace[{index}].nonAuthorityDeclaration missing fields: "
            f"{sorted(missing_fields)}"
        )

    consistency_scope = declaration.get("consistencyScope")
    if consistency_scope == FORBIDDEN_CONSISTENCY_SCOPE:
        return fail(
            f"{source}: reasoningTrace[{index}].nonAuthorityDeclaration.consistencyScope is "
            f"'{FORBIDDEN_CONSISTENCY_SCOPE}' — a {ALLOWED_METHOD_FAMILIES!r} result is forbidden "
            "from claiming global consistency; it is advisory bound/inconsistency analysis over a "
            "single formula only (consistencyScope must be 'formula_local')"
        )
    if consistency_scope not in ADMISSIBLE_CONSISTENCY_SCOPES:
        return fail(
            f"{source}: reasoningTrace[{index}].nonAuthorityDeclaration.consistencyScope must be one "
            f"of {sorted(ADMISSIBLE_CONSISTENCY_SCOPES)}; got {consistency_scope!r}"
        )

    does_not_authorize = set(declaration.get("doesNotAuthorize", []))
    missing_claims = REQUIRED_FORBIDDEN_CLAIMS - does_not_authorize
    if missing_claims:
        return fail(
            f"{source}: reasoningTrace[{index}].nonAuthorityDeclaration.doesNotAuthorize must "
            f"include {sorted(missing_claims)}"
        )

    if not str(declaration.get("statement", "")).strip():
        return fail(f"{source}: reasoningTrace[{index}].nonAuthorityDeclaration.statement must be non-empty")

    return None


def validate_chronos_carrier(carrier: object, source: str, worked_example_key: str) -> int | None:
    """Validate the package-level CHRONOS carrier block on a worked example — the
    object that crosses the Holmes -> Policy Fabric governance boundary. See
    sociosphere/docs/integration/neurosymbolic-chronos-alignment.md, "Neuro-symbolic
    carrier boundary".
    """
    if not isinstance(carrier, dict):
        return fail(f"{source}: workedExamples.{worked_example_key}.chronosCarrier must be an object")

    missing_fields = REQUIRED_CHRONOS_CARRIER_FIELDS - set(carrier.keys())
    if missing_fields:
        return fail(
            f"{source}: workedExamples.{worked_example_key}.chronosCarrier missing fields: "
            f"{sorted(missing_fields)}"
        )

    if not str(carrier.get("sourceEvidenceRef", "")).strip():
        return fail(f"{source}: workedExamples.{worked_example_key}.chronosCarrier.sourceEvidenceRef must be non-empty")

    if carrier.get("groundingStatus") not in ALLOWED_GROUNDING_STATUSES:
        return fail(
            f"{source}: workedExamples.{worked_example_key}.chronosCarrier.groundingStatus must be one of "
            f"{sorted(ALLOWED_GROUNDING_STATUSES)}; got {carrier.get('groundingStatus')!r}"
        )

    if carrier.get("owningAuthorityPlane") != REQUIRED_OWNING_AUTHORITY_PLANE:
        return fail(
            f"{source}: workedExamples.{worked_example_key}.chronosCarrier.owningAuthorityPlane must be "
            f"{REQUIRED_OWNING_AUTHORITY_PLANE!r}; Holmes never declares itself the owning authority plane"
        )

    if not str(carrier.get("replayRef", "")).strip():
        return fail(f"{source}: workedExamples.{worked_example_key}.chronosCarrier.replayRef must be non-empty")

    if not str(carrier.get("governanceDecision", "")).strip():
        return fail(f"{source}: workedExamples.{worked_example_key}.chronosCarrier.governanceDecision must be non-empty")

    return None


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
        result = validate_method_family_and_non_authority(entry, source, index)
        if result is not None:
            return result
    doc_carrier_result = validate_chronos_carrier(
        doc_example.get("chronosCarrier"), source, "documentSpanToPolicyReadyClaim"
    )
    if doc_carrier_result is not None:
        return doc_carrier_result
    vector_example = worked_examples["vectorCandidateVerificationPath"]
    if vector_example.get("candidateClaim", {}).get("status") != "candidate_only":
        return fail(f"{source}: vector candidateClaim status must be candidate_only")
    if vector_example.get("verificationPath", {}).get("result") != REJECTED_BEFORE_POLICY:
        return fail(f"{source}: vector verification path result must be rejected_before_policy")
    vector_carrier_result = validate_chronos_carrier(
        vector_example.get("chronosCarrier"), source, "vectorCandidateVerificationPath"
    )
    if vector_carrier_result is not None:
        return vector_carrier_result
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
