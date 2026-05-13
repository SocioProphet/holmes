#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATURITY = ROOT / "repo.maturity.yaml"

REQUIRED_HEADER_VALUES = {
    "schemaVersion": "repo-maturity.v1",
    "repository": "SocioProphet/holmes",
    "plane": "runtime",
    "status": "active",
    "canonicality": "canonical",
}
REQUIRED_TEXT = [
    "owners:",
    "  - SocioProphet",
    "maturity:",
    "  level: M2",
    "  targetLevel: M3",
    "validation:",
    "  commands:",
    "    - make validate",
    "  ciRequired: true",
    "integrations:",
    "nextActions:",
]
REQUIRED_INTEGRATIONS = {
    "SocioProphet/functional-model-surfaces",
    "SocioProphet/prophet-platform",
    "SocioProphet/sherlock-search",
    "SocioProphet/slash-topics",
    "SociOS-Linux/nlplab",
    "SourceOS-Linux/sourceos-model-carry",
    "SocioProphet/ontogenesis",
    "SocioProphet/policy-fabric",
    "SocioProphet/agentplane",
    "SocioProphet/sociosphere",
}
ALLOWED_VALIDATION_STATUS = {"pending", "passing", "failing", "unknown"}


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, flags=re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"')


def count_list_items_in_section(text: str, section: str) -> int:
    match = re.search(rf"^{re.escape(section)}:\n(?P<body>(?:\s+.*\n?)*)", text, flags=re.MULTILINE)
    if not match:
        return 0
    body = match.group("body")
    return len(re.findall(r"^\s+-\s+", body, flags=re.MULTILINE))


def main() -> int:
    if not MATURITY.exists():
        return fail("missing repo.maturity.yaml")
    text = MATURITY.read_text()

    for key, expected in REQUIRED_HEADER_VALUES.items():
        observed = scalar(text, key)
        if observed != expected:
            return fail(f"{key} must be {expected!r}; got {observed!r}")

    for required in REQUIRED_TEXT:
        if required not in text:
            return fail(f"missing required maturity text: {required}")

    status = scalar(text, "lastKnownStatus")
    if status not in ALLOWED_VALIDATION_STATUS:
        return fail(f"validation.lastKnownStatus must be one of {sorted(ALLOWED_VALIDATION_STATUS)}; got {status!r}")

    missing_integrations = sorted(repo for repo in REQUIRED_INTEGRATIONS if repo not in text)
    if missing_integrations:
        return fail(f"missing integrations: {missing_integrations}")

    evidence_count = count_list_items_in_section(text, "  evidence")
    if evidence_count < 6:
        return fail(f"maturity.evidence should contain at least 6 concrete evidence items; got {evidence_count}")

    next_actions = count_list_items_in_section(text, "nextActions")
    if next_actions < 3:
        return fail(f"nextActions should contain at least 3 roadmap items; got {next_actions}")

    print("OK: Holmes maturity manifest validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
