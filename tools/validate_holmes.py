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
REQUIRED_EVIDENCE = {
    "corpusRef",
    "pipelineOrModelRef",
    "evalRecord",
    "guardrailPolicy",
    "evidenceReceipt",
    "promotionRecord",
    "rollbackRef",
}


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def main() -> int:
    if not EXAMPLE.exists():
        return fail("missing examples/holmes-surface.json")
    data = json.loads(EXAMPLE.read_text())
    if data.get("apiVersion") != "holmes.socioprophet.dev/v1":
        return fail("wrong apiVersion")
    if data.get("kind") != "HolmesSurface":
        return fail("wrong kind")
    spec = data.get("spec", {})
    components = set(spec.get("components", []))
    missing_components = REQUIRED_COMPONENTS - components
    if missing_components:
        return fail(f"missing components: {sorted(missing_components)}")
    evidence = set(spec.get("requiredPromotionEvidence", []))
    missing_evidence = REQUIRED_EVIDENCE - evidence
    if missing_evidence:
        return fail(f"missing promotion evidence: {sorted(missing_evidence)}")
    integrations = spec.get("integrations", {})
    for key in ["standards", "platform", "search", "lab", "sourceosCarry"]:
        if key not in integrations:
            return fail(f"missing integration: {key}")
    print("OK: Holmes contracts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
