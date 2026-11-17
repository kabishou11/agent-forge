#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_STATUSES = {"evidence-ready", "stopped", "not-run"}
REQUIRED_HEADINGS = (
    "## Input",
    "## Expected artifact schema",
    "## Expected status",
    "## Stop case",
)
JSON_BLOCK_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)
FIELD_RE = re.compile(r"[a-z][a-z0-9_]*")


def validate_case(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{path}: cannot read: {exc}"]

    if "not a model-behavior test" not in text.casefold():
        errors.append(f"{path}: must state that the case is not a model-behavior test")
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"{path}: missing heading {heading}")

    match = JSON_BLOCK_RE.search(text)
    if match is None:
        errors.append(f"{path}: missing JSON artifact schema")
        return errors
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON artifact schema: {exc}")
        return errors
    if not isinstance(data, dict):
        errors.append(f"{path}: artifact schema must be a JSON object")
        return errors

    status = data.get("status")
    status_valid = isinstance(status, str) and status in ALLOWED_STATUSES
    if not status_valid:
        errors.append(f"{path}: status must be one of {sorted(ALLOWED_STATUSES)}")
    stop_status = data.get("stop_status")
    stop_status_valid = isinstance(stop_status, str) and stop_status in ALLOWED_STATUSES
    if not stop_status_valid:
        errors.append(f"{path}: stop_status must be one of {sorted(ALLOWED_STATUSES)}")
    if status_valid and stop_status_valid and status == stop_status:
        errors.append(f"{path}: stop_status must differ from status")

    fields = data.get("required_fields")
    if not isinstance(fields, list) or len(fields) < 4:
        errors.append(f"{path}: required_fields must be a list with at least four entries")
    else:
        all_strings = all(isinstance(field, str) for field in fields)
        if all_strings and len(fields) != len(set(fields)):
            errors.append(f"{path}: required_fields must be unique")
        if "status" not in fields:
            errors.append(f"{path}: required_fields must include status")
        for field in fields:
            if not isinstance(field, str) or not FIELD_RE.fullmatch(field):
                errors.append(f"{path}: invalid artifact field name {field!r}")
    return errors


def validate_all(root: Path) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return [f"{skills_root}: skills directory is missing"]
    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append(f"{skills_root}: no skill directories found")
    for skill_dir in skill_dirs:
        case_path = skill_dir / "references" / "smoke-case.md"
        if not case_path.is_file():
            errors.append(f"{case_path}: missing synthetic smoke case")
            continue
        errors.extend(validate_case(case_path))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate synthetic skill smoke cases offline.")
    parser.add_argument(
        "root",
        nargs="?",
        default=str(Path(__file__).resolve().parents[1]),
        help="repository root (defaults to the parent of this script)",
    )
    args = parser.parse_args(argv)
    root = Path(args.root)
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    errors = validate_all(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"\n{len(errors)} smoke-case error(s)")
        return 1
    print("OK: synthetic smoke cases are structurally valid")
    print("Note: these are repeatable fixtures, not model-behavior evaluations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
