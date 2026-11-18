#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ALLOWED_TYPES = {
    "feat",
    "fix",
    "docs",
    "test",
    "refactor",
    "chore",
    "build",
    "ci",
    "perf",
    "revert",
}
SUBJECT_RE = re.compile(
    r"^(?P<type>[a-z]+)\((?P<scope>[a-z0-9][a-z0-9-]*)\): (?P<summary>.+)$"
)
FORBIDDEN_TRAILERS = (
    ("coauthor trailer", re.compile(r"^co-authored-by:", re.IGNORECASE)),
    ("generated-by trailer", re.compile(r"^generated (?:with|by)\b", re.IGNORECASE)),
    ("tool trailer", re.compile(r"^(?:made|created|assisted) (?:with|by)\b", re.IGNORECASE)),
    ("tool signature", re.compile(r"^tool-generated\b", re.IGNORECASE)),
)
MAX_SUBJECT_LENGTH = 72


def validate_message(text: str) -> list[str]:
    lines = text.splitlines()
    if not lines or not lines[0].strip():
        return ["commit subject is required"]
    subject = lines[0].rstrip()
    errors: list[str] = []
    if len(subject) > MAX_SUBJECT_LENGTH:
        errors.append(f"subject must be at most {MAX_SUBJECT_LENGTH} characters")
    match = SUBJECT_RE.fullmatch(subject)
    if match is None:
        errors.append("subject must match type(scope): summary")
    else:
        if match.group("type") not in ALLOWED_TYPES:
            errors.append(
                f"type must be one of {', '.join(sorted(ALLOWED_TYPES))}"
            )
        summary = match.group("summary")
        if not summary[0].islower() and not summary[0].isdigit():
            errors.append("summary must start with a lowercase letter or digit")
        if summary.endswith("."):
            errors.append("summary must not end with a period")
    for lineno, line in enumerate(lines[1:], start=2):
        for label, pattern in FORBIDDEN_TRAILERS:
            if pattern.match(line.strip()):
                errors.append(f"line {lineno}: remove the {label}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check a commit message against the Agent Forge contribution rules."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="message file; read standard input when omitted",
    )
    args = parser.parse_args(argv)
    if args.path:
        try:
            text = Path(args.path).read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot read {args.path}: {exc}", file=sys.stderr)
            return 2
    else:
        text = sys.stdin.read()
    errors = validate_message(text)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("OK: commit message follows the contribution format")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
