#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVALID_DIR = ROOT / "fixtures" / "invalid"
sys.path.insert(0, str(ROOT / "tools"))

import validate_holmes  # noqa: E402


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def validate_invalid_fixture(path: Path) -> tuple[bool, str]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return True, f"invalid JSON rejected: {exc}"

    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
        if path.name.startswith("holmes-surface-"):
            result = validate_holmes.validate_surface_data(data, str(path.relative_to(ROOT)))
        elif path.name.startswith("proof-claim-"):
            result = validate_holmes.validate_reasoning_contract_data(data, str(path.relative_to(ROOT)))
        else:
            return False, "unknown fixture family; expected holmes-surface-* or proof-claim-*"

    if result is None:
        return False, "fixture unexpectedly passed validation"
    return True, stderr.getvalue().strip() or "fixture rejected"


def main() -> int:
    if not INVALID_DIR.exists():
        return fail("missing fixtures/invalid")
    fixtures = sorted(INVALID_DIR.glob("*.json"))
    if len(fixtures) < 4:
        return fail(f"expected at least 4 invalid fixtures; got {len(fixtures)}")

    failures: list[str] = []
    for fixture in fixtures:
        rejected, reason = validate_invalid_fixture(fixture)
        if not rejected:
            failures.append(f"{fixture.relative_to(ROOT)}: {reason}")
        else:
            print(f"OK: rejected {fixture.relative_to(ROOT)} — {reason}")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print("OK: Holmes negative fixtures rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
