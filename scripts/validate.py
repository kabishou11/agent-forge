#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote

REQUIRED_SKILLS = {
    "forge-intent-alignment",
    "forge-signal-first-context",
    "forge-disposable-prototypes",
    "forge-architectural-constraints",
    "forge-verification-harness",
    "forge-triage-repro-fix",
    "forge-evidence-review",
    "forge-depth-first-parallelism",
    "forge-context-budget",
    "forge-formal-boundaries",
}

REQUIRED_SECTIONS = [
    "Inputs",
    "Workflow",
    "Stop conditions",
    "Deliverables",
    "Example",
    "Sources",
]

REQUIRED_FILES = {
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    ".gitignore",
    "docs/sources.md",
    "docs/validation.md",
    "docs/examples/synthetic-walkthrough.md",
    "release-manifest.txt",
    "scripts/smoke.py",
    "scripts/validate.py",
    "tests/test_validate.py",
    ".github/workflows/validate.yml",
}

SKILL_REQUIRED_FILES = (
    "SKILL.md",
    "LICENSE",
    "NOTICES.md",
    "references/sources.md",
    "references/field-guide.md",
    "references/smoke-case.md",
)

EXPECTED_SOURCE_METADATA = {
    "S01": ("2026-01-22", "https://x.com/poteto/status/2014257661035094246"),
    "S02": ("2026-05-26", "https://x.com/poteto/status/2058975157503570132"),
    "S03": ("2026-06-25", "https://x.com/poteto/status/2069824386283319343"),
    "S04": ("2026-09-01", "https://x.com/poteto/status/2094457600259842065"),
    "S05": ("2026-09-10", "https://x.com/poteto/status/2097732320606507506"),
    "S06": ("2026-08-17", "https://x.com/poteto/status/2089067865098113024"),
    "S07": ("2026-10-17", "https://x.com/poteto/status/2111133080526495985"),
    "S08": ("2026-11-03", "https://x.com/poteto/status/2117437607940681849"),
    "S09": ("2026-11-06", "https://x.com/poteto/status/2118416074601545968"),
    "S10": ("2026-11-09", "https://x.com/poteto/status/2119521036660314339"),
    "S11": ("2026-04-26", "https://x.com/poteto/status/2048092593087721736"),
    "S12": ("2026-11-01", "https://x.com/poteto/status/2116580481236115933"),
    "S13": ("2026-10-15", "https://x.com/poteto/status/2110415199962612120"),
    "S14": ("2026-11-15", "https://x.com/poteto/status/2121646643124809848"),
    "S15": ("2026-11-08", "https://x.com/poteto/status/2119313621188849806"),
    "S16": ("2026-10-07", "https://x.com/poteto/status/2107510472601985336"),
}

EXPECTED_SOURCE_IDS = set(EXPECTED_SOURCE_METADATA)

PY_CACHE_PARTS = {".git", "__pycache__", ".pytest_cache"}
PY_CACHE_SUFFIXES = {".pyc", ".pyo"}

FORBIDDEN_ARTIFACT_DIRS = {
    ".venv",
    "venv",
    "node_modules",
    "artifacts",
    "tmp",
    ".cache",
    ".session",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    "dist",
    "build",
    "coverage",
    "htmlcov",
}

FORBIDDEN_FILE_SUFFIXES = {
    ".log",
    ".tmp",
    ".har",
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".7z",
}

MAX_SCAN_BYTES = 2_000_000
MANIFEST_FILE = "release-manifest.txt"

YAML_TYPED_VALUES = {
    "true",
    "false",
    "yes",
    "no",
    "on",
    "off",
    "null",
    "~",
    ".inf",
    "+.inf",
    "-.inf",
    ".nan",
}
YAML_NUMBER_RE = re.compile(
    r"[-+]?(?:(?:[0-9]+(?:\.[0-9]*)?)|(?:\.[0-9]+))(?:[eE][-+]?[0-9]+)?"
)
YAML_BASE_NUMBER_RE = re.compile(r"[-+]?(?:0x[0-9a-fA-F]+|0o[0-7]+|0b[01]+)")
YAML_RESERVED_PLAIN_START = frozenset("-?:,[]{}#&*!|>'\"%@`")
YAML_INLINE_COMMENT_RE = re.compile(r"\s#")

SOURCE_ROW_RE = re.compile(r"^\|\s*(S\d{2})\s*\|")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

PRIVATE_PATH_PATTERNS = [
    ("private home path", re.compile("/" + "home" + "/")),
    ("private user path", re.compile("/" + "Users" + "/")),
    ("private root path", re.compile("/" + "root" + "/")),
    ("workspace path", re.compile("/" + "workspace" + "/")),
    ("private Windows path", re.compile(r"[A-Za-z]:\\" + "Users" + r"\\")),
]

SECRET_PATTERNS = [
    ("possible GitHub token", re.compile(r"\bghp_[A-Za-z0-9]{30,}\b")),
    ("possible GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b")),
    ("possible AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("possible Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    (
        "possible private key",
        re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?" + "PRIVATE KEY-----"),
    ),
    ("possible bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}\b")),
]

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
EMAIL_ALLOWLIST: set[str] = set()

DUMP_KEYWORDS = ("session", "transcript", "cache", "export", "dump")
DUMP_EXTENSIONS = (".json", ".jsonl", ".har", ".zip", ".tar", ".gz", ".log")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def publication_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in PY_CACHE_PARTS for part in rel.parts):
            continue
        if path.suffix.lower() in PY_CACHE_SUFFIXES:
            continue
        yield path


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["missing opening YAML frontmatter delimiter"]
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, ["missing closing YAML frontmatter delimiter"]

    data: dict[str, str] = {}
    for lineno, line in enumerate(lines[1:end], start=2):
        if not line.strip():
            continue
        if line != line.lstrip():
            errors.append(f"frontmatter line {lineno} must not be indented")
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            errors.append(f"frontmatter line {lineno} is not a simple key: value pair")
            continue
        key, raw_value = match.group(1), match.group(2).strip()
        if key in data:
            errors.append(f"duplicate frontmatter field: {key}")
        if not raw_value:
            errors.append(f"frontmatter field {key} must have a scalar value")
            continue

        quoted = False
        quote_char = ""
        value = raw_value
        if raw_value[0] in "'\"":
            quote_char = raw_value[0]
            if len(raw_value) < 2 or raw_value[-1] != quote_char:
                errors.append(f"frontmatter field {key} has an unmatched quote")
                continue
            quoted = True
            value = raw_value[1:-1]
            if quote_char in value:
                errors.append(f"frontmatter field {key} has an internal unescaped quote")
                continue
            if "\\" in value:
                errors.append(f"frontmatter field {key} uses an unsupported quote escape")
                continue
        elif raw_value[-1] in "'\"":
            errors.append(f"frontmatter field {key} has an unmatched quote")
            continue

        if not value:
            errors.append(f"frontmatter field {key} must not be empty")
            continue

        if not quoted:
            if raw_value.startswith(("!", "&", "*")):
                errors.append(
                    f"frontmatter field {key} must not use YAML tags, anchors, or aliases"
                )
                continue
            if re.match(r"^(?:-\s|\?\s|:\s)", raw_value) or raw_value in {"-", "?"}:
                errors.append(f"frontmatter field {key} must not use sequence or mapping syntax")
                continue
            if value[0] in YAML_RESERVED_PLAIN_START:
                errors.append(
                    f"frontmatter field {key} must not start with reserved YAML punctuation"
                )
                continue
            if YAML_INLINE_COMMENT_RE.search(value):
                errors.append(f"frontmatter field {key} must not contain an inline YAML comment")
                continue
            if ": " in value:
                errors.append(f"frontmatter field {key} contains an embedded mapping in a plain scalar")
                continue
            lowered = value.casefold()
            if lowered in YAML_TYPED_VALUES:
                errors.append(f"frontmatter field {key} must be a string, not a YAML boolean or null")
                continue
            if YAML_NUMBER_RE.fullmatch(value) or YAML_BASE_NUMBER_RE.fullmatch(value):
                errors.append(f"frontmatter field {key} must be a string, not a YAML number")
                continue

        data[key] = value

    for key in data:
        if key not in {"name", "description"}:
            errors.append(f"unexpected frontmatter field: {key}")
    return data, errors


def section_body(text: str, heading: str) -> str:
    pattern = re.compile(r"^##\s+" + re.escape(heading) + r"\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    rest = text[match.end() :]
    next_heading = re.search(r"^##\s+", rest, re.MULTILINE)
    return rest[: next_heading.start()] if next_heading else rest


def extract_links(text: str) -> list[str]:
    return [match.group(1).strip() for match in MARKDOWN_LINK_RE.finditer(text)]


def check_link_target(base_file: Path, target: str, root: Path, skill_root: Path | None) -> list[str]:
    errors: list[str] = []
    clean = target.strip()
    if clean.startswith("<") and clean.endswith(">"):
        clean = clean[1:-1]
    if not clean or clean.startswith("#"):
        return errors
    if clean.startswith(("http://", "https://", "mailto:", "tel:", "//")):
        return errors
    clean = clean.split("#", 1)[0]
    if not clean:
        return errors
    clean = unquote(clean)
    if Path(clean).is_absolute():
        return [f"{base_file}: link must be relative, got {target}"]
    resolved = (base_file.parent / clean).resolve()
    root_resolved = root.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError:
        return [f"{base_file}: link escapes repository: {target}"]
    if skill_root is not None:
        try:
            resolved.relative_to(skill_root.resolve())
        except ValueError:
            errors.append(f"{base_file}: link escapes skill directory: {target}")
    if not resolved.exists():
        errors.append(f"{base_file}: link target does not exist: {target}")
    return errors


def check_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    root_resolved = root.resolve()
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if any(part in PY_CACHE_PARTS for part in rel.parts):
            continue
        try:
            text = read_text(path)
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{rel}: cannot read markdown: {exc}")
            continue
        skill_root = None
        if len(rel.parts) >= 2 and rel.parts[0] == "skills":
            skill_root = root / "skills" / rel.parts[1]
        for target in extract_links(text):
            errors.extend(check_link_target(path, target, root_resolved, skill_root))
    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_dir}: missing SKILL.md"]
    try:
        text = read_text(skill_file)
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{skill_file}: cannot read: {exc}"]

    frontmatter, frontmatter_errors = parse_frontmatter(text)
    errors.extend(f"{skill_file}: {item}" for item in frontmatter_errors)

    name = frontmatter.get("name")
    if not name:
        errors.append(f"{skill_file}: missing name")
    else:
        if name != skill_dir.name:
            errors.append(f"{skill_file}: name {name!r} does not match directory {skill_dir.name!r}")
        if not (1 <= len(name) <= 64):
            errors.append(f"{skill_file}: name must be 1-64 characters")
        if not NAME_RE.fullmatch(name):
            errors.append(f"{skill_file}: name must be lowercase kebab-case without consecutive hyphens")
        if not name.startswith("forge-"):
            errors.append(f"{skill_file}: name must start with forge-")

    description = frontmatter.get("description")
    if not description:
        errors.append(f"{skill_file}: missing description")
    else:
        if not (1 <= len(description) <= 1024):
            errors.append(f"{skill_file}: description must be 1-1024 characters")
        if not re.search(r"\bUse when\b", description, re.IGNORECASE):
            errors.append(f"{skill_file}: description needs a 'Use when' trigger clause")

    headings = re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    if headings != REQUIRED_SECTIONS:
        errors.append(
            f"{skill_file}: section headings must be exactly {REQUIRED_SECTIONS}, got {headings}"
        )

    line_count = len(text.splitlines())
    if not (40 <= line_count <= 90):
        errors.append(f"{skill_file}: main skill must be 40-90 lines, got {line_count}")

    example = section_body(text, "Example")
    for marker in ("**Input:**", "**Expected output:**", "**Stop case:**"):
        if marker not in example:
            errors.append(f"{skill_file}: Example is missing {marker}")

    if "NOT RUN" not in text:
        errors.append(f"{skill_file}: must mention NOT RUN for unexecuted work")

    if not re.search(r"do not override", text, re.IGNORECASE):
        errors.append(f"{skill_file}: must state that instructions do not override host policy")
    return errors


def validate_skill_bundle(skill_dir: Path) -> list[str]:
    errors = validate_skill(skill_dir)
    for relative in SKILL_REQUIRED_FILES:
        path = skill_dir / relative
        if not path.is_file():
            errors.append(f"{path}: required file is missing from the skill bundle")

    license_path = skill_dir / "LICENSE"
    if license_path.is_file():
        try:
            license_text = read_text(license_path)
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{license_path}: cannot read: {exc}")
        else:
            for phrase in (
                "MIT License",
                "Copyright (c) 2026 Agent Forge contributors",
                "Permission is hereby granted",
            ):
                if phrase not in license_text:
                    errors.append(f"{license_path}: missing {phrase!r}")
    else:
        errors.append(f"{license_path}: required file is missing")

    notices_path = skill_dir / "NOTICES.md"
    if notices_path.is_file():
        try:
            notices_text = read_text(notices_path)
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{notices_path}: cannot read: {exc}")
        else:
            for phrase in ("not official", "not affiliated", "MIT", "references/sources.md"):
                if phrase not in notices_text:
                    errors.append(f"{notices_path}: missing {phrase!r}")
    else:
        errors.append(f"{notices_path}: required file is missing")

    for markdown in sorted(skill_dir.rglob("*.md")):
        rel = markdown.relative_to(skill_dir)
        if any(part in PY_CACHE_PARTS for part in rel.parts):
            continue
        try:
            text = read_text(markdown)
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{markdown}: cannot read: {exc}")
            continue
        for target in extract_links(text):
            errors.extend(check_link_target(markdown, target, skill_dir, skill_dir))
    return errors


def parse_source_rows(text: str, *, central: bool) -> tuple[list[tuple[str, str, str, list[str]]], list[str]]:
    rows: list[tuple[str, str, str, list[str]]] = []
    errors: list[str] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not SOURCE_ROW_RE.match(line):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 4:
            errors.append(f"source row at line {lineno} has too few columns")
            continue
        source_id, date, url = parts[0], parts[1], parts[2]
        if not DATE_RE.fullmatch(date):
            errors.append(f"source {source_id} has invalid date {date!r}")
        if not url.startswith("https://"):
            errors.append(f"source {source_id} must use an https URL")
        if central and len(parts) < 5:
            errors.append(f"central source {source_id} needs a skill mapping column")
            continue
        rows.append((source_id, date, url, parts[3:]))
    return rows, errors


def validate_sources(
    root: Path,
    expected_ids: set[str] | None = None,
    *,
    check_canonical: bool = False,
) -> list[str]:
    errors: list[str] = []
    central_path = root / "docs" / "sources.md"
    if not central_path.is_file():
        return [f"{central_path}: missing central source catalogue"]
    try:
        central_text = read_text(central_path)
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{central_path}: cannot read: {exc}"]

    central_rows, row_errors = parse_source_rows(central_text, central=True)
    errors.extend(f"{central_path}: {item}" for item in row_errors)
    if not central_rows:
        errors.append(f"{central_path}: no source rows found")

    central: dict[str, dict[str, object]] = {}
    for source_id, date, url, rest in central_rows:
        if source_id in central:
            errors.append(f"{central_path}: duplicate source ID {source_id}")
            continue
        skills_field = rest[1] if len(rest) > 1 else ""
        skills = set(re.findall(r"forge-[a-z0-9-]+", skills_field))
        if not skills:
            errors.append(f"{central_path}: source {source_id} is an orphan with no skill")
        central[source_id] = {"date": date, "url": url, "skills": skills}

    if expected_ids is not None:
        missing = sorted(expected_ids - set(central))
        extra = sorted(set(central) - expected_ids)
        if missing:
            errors.append(f"{central_path}: missing expected source IDs: {', '.join(missing)}")
        if extra:
            errors.append(f"{central_path}: unexpected source IDs: {', '.join(extra)}")

    if check_canonical:
        for source_id in sorted(set(central) & set(EXPECTED_SOURCE_METADATA)):
            expected_date, expected_url = EXPECTED_SOURCE_METADATA[source_id]
            if central[source_id]["date"] != expected_date:
                errors.append(
                    f"{central_path}: source {source_id} date {central[source_id]['date']!r} "
                    f"does not match canonical {expected_date!r}"
                )
            if central[source_id]["url"] != expected_url:
                errors.append(
                    f"{central_path}: source {source_id} URL does not match the canonical URL"
                )

    url_to_ids: dict[str, list[str]] = {}
    for source_id, info in central.items():
        url_to_ids.setdefault(str(info["url"]), []).append(source_id)
    for url, source_ids in url_to_ids.items():
        if len(source_ids) > 1:
            errors.append(
                f"{central_path}: duplicate canonical source URL used by "
                f"{', '.join(sorted(source_ids))}: {url}"
            )

    skills_root = root / "skills"
    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir()) if skills_root.is_dir() else []
    known_skills = {path.name for path in skill_dirs}

    for source_id, info in central.items():
        for skill in sorted(info["skills"]):
            if skill not in known_skills:
                errors.append(f"{central_path}: source {source_id} references unknown skill {skill}")

    for skill_dir in skill_dirs:
        local_path = skill_dir / "references" / "sources.md"
        if not local_path.is_file():
            errors.append(f"{local_path}: missing local source map")
            continue
        try:
            local_text = read_text(local_path)
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{local_path}: cannot read: {exc}")
            continue
        local_rows, local_errors = parse_source_rows(local_text, central=False)
        errors.extend(f"{local_path}: {item}" for item in local_errors)
        local: dict[str, tuple[str, str]] = {}
        for source_id, date, url, _rest in local_rows:
            if source_id in local:
                errors.append(f"{local_path}: duplicate source ID {source_id}")
                continue
            if source_id not in central:
                errors.append(f"{local_path}: source {source_id} is missing from the central catalogue")
                continue
            if date != central[source_id]["date"]:
                errors.append(f"{local_path}: source {source_id} date does not match the central catalogue")
            if url != central[source_id]["url"]:
                errors.append(f"{local_path}: source {source_id} URL does not match the central catalogue")
            local[source_id] = (date, url)

        expected = {
            source_id for source_id, info in central.items() if skill_dir.name in info["skills"]
        }
        missing = sorted(expected - set(local))
        extra = sorted(set(local) - expected)
        if missing:
            errors.append(f"{local_path}: missing sources required by the catalogue: {', '.join(missing)}")
        if extra:
            errors.append(f"{local_path}: sources not assigned to this skill: {', '.join(extra)}")
        if not local_rows:
            errors.append(f"{local_path}: no local source rows found")

    for source_id, info in central.items():
        if not info["skills"]:
            errors.append(f"{central_path}: source {source_id} is unused (orphan)")

    return errors


def scan_publication(root: Path) -> list[str]:
    errors: list[str] = []
    for path in publication_files(root):
        rel = path.relative_to(root)
        try:
            size = path.stat().st_size
        except OSError as exc:
            errors.append(f"{rel}: cannot stat publication file: {exc}")
            continue
        if size > MAX_SCAN_BYTES:
            errors.append(
                f"{rel}: exceeds publication scan limit of {MAX_SCAN_BYTES} bytes; "
                "oversized files are not exempt from the release"
            )
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            errors.append(f"{rel}: not valid UTF-8 text; cannot scan publication file")
            continue
        except OSError as exc:
            errors.append(f"{rel}: cannot read publication file: {exc}")
            continue

        for label, pattern in PRIVATE_PATH_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{rel}:{line}: {label} detected")

        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{rel}:{line}: {label} detected")

        for match in EMAIL_RE.finditer(text):
            if match.group(0).lower() in EMAIL_ALLOWLIST:
                continue
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{rel}:{line}: email address detected")
    return errors


def check_forbidden_publication_artifacts(root: Path) -> list[str]:
    errors: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        relative = current.relative_to(root)
        kept: list[str] = []
        for name in dirnames:
            if name in PY_CACHE_PARTS:
                continue
            if name in FORBIDDEN_ARTIFACT_DIRS:
                errors.append(
                    f"{(relative / name).as_posix()}: forbidden publication artifact directory"
                )
                continue
            kept.append(name)
        dirnames[:] = kept
        for name in filenames:
            if Path(name).suffix.lower() in FORBIDDEN_FILE_SUFFIXES:
                errors.append(
                    f"{(relative / name).as_posix()}: forbidden publication artifact file"
                )
    return errors


def manifest_candidate_files(root: Path) -> set[str]:
    files: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        relative = current.relative_to(root)
        dirnames[:] = [
            name
            for name in dirnames
            if name not in PY_CACHE_PARTS and name not in FORBIDDEN_ARTIFACT_DIRS
        ]
        for name in filenames:
            if Path(name).suffix.lower() in PY_CACHE_SUFFIXES:
                continue
            files.add((relative / name).as_posix())
    return files


def validate_release_manifest(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / MANIFEST_FILE
    if not manifest_path.is_file():
        return [f"{manifest_path}: release manifest is missing"]
    try:
        lines = read_text(manifest_path).splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{manifest_path}: cannot read: {exc}"]

    entries: list[str] = []
    for lineno, line in enumerate(lines, start=1):
        entry = line.strip()
        if not entry or entry.startswith("#"):
            continue
        entry_path = Path(entry)
        if "\\" in entry or entry.startswith("./"):
            errors.append(f"{manifest_path}:{lineno}: use a plain repository-relative path")
            continue
        if entry_path.is_absolute() or ".." in entry_path.parts:
            errors.append(f"{manifest_path}:{lineno}: path must stay inside the repository")
            continue
        if any(part in PY_CACHE_PARTS for part in entry_path.parts):
            errors.append(f"{manifest_path}:{lineno}: Python cache or .git paths are not publishable")
            continue
        if any(part in FORBIDDEN_ARTIFACT_DIRS for part in entry_path.parts):
            errors.append(f"{manifest_path}:{lineno}: artifact, cache, or session paths are not publishable")
            continue
        if entry_path.suffix.lower() in FORBIDDEN_FILE_SUFFIXES:
            errors.append(f"{manifest_path}:{lineno}: log, temporary, or archive files are not publishable")
            continue
        entries.append(entry)

    seen: set[str] = set()
    for entry in entries:
        if entry in seen:
            errors.append(f"{manifest_path}: duplicate manifest entry {entry}")
        seen.add(entry)
        if not (root / entry).is_file():
            errors.append(f"{manifest_path}: listed file does not exist: {entry}")

    actual = manifest_candidate_files(root)
    for entry in sorted(actual - seen):
        errors.append(f"{manifest_path}: file is not listed in the release manifest: {entry}")
    for entry in sorted(seen - actual):
        if (root / entry).is_file():
            errors.append(f"{manifest_path}: manifest entry is outside the publishable file set: {entry}")
    return errors


def check_no_research_dumps(root: Path) -> list[str]:
    errors: list[str] = []
    for path in publication_files(root):
        name = path.name.lower()
        if name.endswith(DUMP_EXTENSIONS) and any(keyword in name for keyword in DUMP_KEYWORDS):
            errors.append(f"{path.relative_to(root)}: possible research, cache, or session dump")
    return errors


def validate_readmes(root: Path) -> list[str]:
    errors: list[str] = []
    for name in ("README.md", "README.zh-CN.md"):
        path = root / name
        if not path.is_file():
            continue
        try:
            text = read_text(path)
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{path}: cannot read: {exc}")
            continue
        for skill in sorted(REQUIRED_SKILLS):
            if skill not in text:
                errors.append(f"{path}: does not mention {skill}")
        for snippet in (
            "TARGET=../target-project",
            '[ -e "$DEST" ] || [ -L "$DEST" ]',
            "Refusing to overwrite existing destination",
        ):
            if snippet not in text:
                errors.append(f"{path}: missing safe installation guard {snippet!r}")
        if "/path/to/target-project" in text:
            errors.append(f"{path}: use a relative installation target, not a placeholder absolute path")
    return errors


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for relative in sorted(REQUIRED_FILES):
        if not (root / relative).is_file():
            errors.append(f"{relative}: required file is missing")

    skills_root = root / "skills"
    skill_dirs = []
    if not skills_root.is_dir():
        errors.append("skills/: directory is missing")
    else:
        skill_dirs = sorted(
            path for path in skills_root.iterdir() if path.is_dir() and path.name.startswith("forge-")
        )
        names = {path.name for path in skill_dirs}
        missing = sorted(REQUIRED_SKILLS - names)
        extra = sorted(names - REQUIRED_SKILLS)
        if missing:
            errors.append(f"skills/: missing required skills: {', '.join(missing)}")
        if extra:
            errors.append(f"skills/: unexpected skills: {', '.join(extra)}")
        if len(skill_dirs) != len(REQUIRED_SKILLS):
            errors.append(f"skills/: expected {len(REQUIRED_SKILLS)} skills, found {len(skill_dirs)}")
        for skill_dir in skill_dirs:
            errors.extend(validate_skill_bundle(skill_dir))

    errors.extend(check_markdown_links(root))
    errors.extend(validate_sources(root, EXPECTED_SOURCE_IDS, check_canonical=True))
    errors.extend(scan_publication(root))
    errors.extend(check_forbidden_publication_artifacts(root))
    errors.extend(check_no_research_dumps(root))
    errors.extend(validate_release_manifest(root))
    errors.extend(validate_readmes(root))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Agent Forge repository.")
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
    errors = validate_repository(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"\n{len(errors)} validation error(s)")
        return 1
    print("OK: Agent Forge repository checks passed")
    print("Note: structural checks do not prove model behavior or host discovery.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
