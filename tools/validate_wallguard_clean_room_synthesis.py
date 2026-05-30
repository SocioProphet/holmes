#!/usr/bin/env python3
"""Validate WallGuard clean-room synthesis fixtures."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "wallguard-clean-room-synthesis.schema.json"
VALID = ROOT / "examples" / "wallguard-clean-room-synthesis.valid.json"
REJECTED = [
    ROOT / "examples" / "wallguard-clean-room-synthesis.cross-wall.rejected.json",
    ROOT / "examples" / "wallguard-clean-room-synthesis.bad-clean-room.rejected.json",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(instance: dict, schema: dict, *, source_label: str) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        lines = [f"{source_label} failed schema validation:"]
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            lines.append(f" - {location}: {error.message}")
        raise ValueError("\n".join(lines))


def semantic_diagnostics(record: dict) -> list[str]:
    diagnostics: list[str] = []
    spec = record["spec"]
    source_walls = set(spec["sourceWallRefs"])
    destination_wall = spec["destinationWallRef"]
    outcome = spec["wallDecisionOutcome"]
    decision = spec["synthesisDecision"]
    classification = spec["outputClassification"]

    if spec["sourceLabelPreserved"] is not True:
        diagnostics.append("source labels must be preserved")

    if decision == "same_wall_synthesis":
        if outcome != "allow":
            diagnostics.append("same-wall synthesis requires WallGuard allow outcome")
        if len(source_walls) != 1:
            diagnostics.append("same-wall synthesis requires exactly one source wall")
        if destination_wall not in source_walls:
            diagnostics.append("same-wall synthesis destination wall must match source wall")
        if classification != "wall_restricted":
            diagnostics.append("same-wall synthesis output must remain wall_restricted")
        if not spec["residualRestrictions"]:
            diagnostics.append("same-wall synthesis requires residual restrictions")

    if decision == "clean_room_release":
        if outcome != "clean_room_release_allowed":
            diagnostics.append("clean-room release requires clean_room_release_allowed outcome")
        if spec["restrictedPayloadExcluded"] is not True:
            diagnostics.append("clean-room release must exclude restricted payload")
        if classification not in {"clean_room_derived", "public_sanitized"}:
            diagnostics.append("clean-room release output must be clean_room_derived or public_sanitized")
        if not spec["residualRestrictions"]:
            diagnostics.append("clean-room release must retain residual restrictions")

    if decision in {"deny", "quarantine"} and outcome == "allow":
        diagnostics.append("deny/quarantine synthesis cannot use allow outcome")

    if classification in {"firm_approved", "public_sanitized"} and spec["restrictedPayloadExcluded"] is not True:
        diagnostics.append("broader release classifications require restrictedPayloadExcluded=true")

    return diagnostics


def check(path: Path, schema: dict, expected: str) -> dict:
    record = load_json(path)
    validate_schema(record, schema, source_label=str(path.relative_to(ROOT)))
    diagnostics = semantic_diagnostics(record)
    actual = "fail" if diagnostics else "pass"
    result = {"example": path.name, "expected": expected, "actual": actual, "diagnostics": diagnostics}
    if actual != expected:
        raise ValueError(json.dumps(result, indent=2))
    return result


def main() -> int:
    schema = load_json(SCHEMA)
    Draft202012Validator.check_schema(schema)
    results = [check(VALID, schema, "pass")]
    for path in REJECTED:
        results.append(check(path, schema, "fail"))
    print(json.dumps({"ok": True, "checked": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
