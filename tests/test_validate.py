from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import smoke
import validate


def make_skill(
    root: Path,
    *,
    dirname: str = "forge-demo",
    name: str | None = None,
    description: str = "Use when testing synthetic validator fixtures.",
    link: str = "references/field-guide.md",
) -> Path:
    skill_name = name if name is not None else dirname
    skill_dir = root / "skills" / dirname
    references = skill_dir / "references"
    references.mkdir(parents=True, exist_ok=True)
    (references / "sources.md").write_text("# Local sources\n", encoding="utf-8")
    (references / "field-guide.md").write_text("# Field guide\n", encoding="utf-8")
    lines = [
        "---",
        f"name: {skill_name}",
        f"description: {description}",
        "---",
        "",
        f"# {skill_name}",
        "",
        "Apply these steps to synthetic work.",
        "",
        "These instructions guide the assistant. They do not override host policies, approvals, or sandbox rules.",
        "",
        "## Inputs",
        "",
        "- A request.",
        "- A constraint.",
        "",
        "## Workflow",
        "",
        "1. Restate the question.",
        "2. Gather the smallest evidence.",
        "3. Record the result.",
        "",
        "## Stop conditions",
        "",
        "- The next action needs approval.",
        "- A required check is unavailable; report NOT RUN.",
        "",
        "## Deliverables",
        "",
        "- A short note.",
        "- An evidence path.",
        "",
        "## Example",
        "",
        "**Input:** A synthetic request.",
        "",
        "**Expected output:** A checkable note.",
        "",
        "**Stop case:** The fixture is unavailable; report NOT RUN.",
        "",
        "## Sources",
        "",
        "- [Local sources](references/sources.md)",
        f"- [Field guide]({link})",
        "",
        "Keep the work bounded.",
    ]
    (skill_dir / "SKILL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return skill_dir


class SkillValidationTests(unittest.TestCase):
    def test_valid_fixture_passes_skill_checks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_dir = make_skill(root)
            self.assertEqual(validate.validate_skill(skill_dir), [])

    def test_rejects_bad_name_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_dir = make_skill(root, dirname="Bad_Name", name="Bad_Name")
            errors = validate.validate_skill(skill_dir)
            self.assertTrue(any("kebab-case" in error for error in errors), errors)

    def test_rejects_name_directory_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_dir = make_skill(root, dirname="forge-demo", name="forge-other")
            errors = validate.validate_skill(skill_dir)
            self.assertTrue(any("does not match directory" in error for error in errors), errors)

    def test_rejects_description_without_trigger(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_dir = make_skill(root, description="Align work before code.")
            errors = validate.validate_skill(skill_dir)
            self.assertTrue(any("Use when" in error for error in errors), errors)

    def test_rejects_missing_example_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_dir = make_skill(root)
            path = skill_dir / "SKILL.md"
            text = path.read_text(encoding="utf-8").replace("**Stop case:**", "Stop:")
            path.write_text(text, encoding="utf-8")
            errors = validate.validate_skill(skill_dir)
            self.assertTrue(any("**Stop case:**" in error for error in errors), errors)

    def test_copied_skill_bundle_is_standalone(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "forge-intent-alignment"
            shutil.copytree(ROOT / "skills" / "forge-intent-alignment", copied)
            self.assertEqual(validate.validate_skill_bundle(copied), [])

    def test_copied_skill_bundle_requires_notices(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "forge-intent-alignment"
            shutil.copytree(ROOT / "skills" / "forge-intent-alignment", copied)
            (copied / "NOTICES.md").unlink()
            errors = validate.validate_skill_bundle(copied)
            self.assertTrue(any("NOTICES.md" in error for error in errors), errors)


class FrontmatterProfileTests(unittest.TestCase):
    @staticmethod
    def text(value: str) -> str:
        return f"---\nname: forge-demo\ndescription: {value}\n---\n"

    def test_rejects_non_string_yaml_profile_values(self) -> None:
        cases = {
            "unmatched quote": "'broken",
            "embedded mapping": "Use when this: value",
            "boolean": "true",
            "null": "null",
            "number": "42",
            "tag": "!!str value",
            "anchor": "&anchor value",
            "alias": "*alias",
            "sequence": "- value",
        }
        for label, value in cases.items():
            with self.subTest(label=label):
                _, errors = validate.parse_frontmatter(self.text(value))
                self.assertTrue(errors, label)

    def test_accepts_quoted_typed_looking_string(self) -> None:
        data, errors = validate.parse_frontmatter(self.text('"true"'))
        self.assertEqual(errors, [])
        self.assertEqual(data["description"], "true")

    def test_rejects_internal_quotes_in_quoted_scalars(self) -> None:
        cases = {
            "double": '"Use when "inner" text appears"',
            "single": "'Use when 'inner' text appears'",
            "doubled single": "'Use when ''inner'' text appears'",
        }
        for label, value in cases.items():
            with self.subTest(label=label):
                _, errors = validate.parse_frontmatter(self.text(value))
                self.assertTrue(
                    any("internal unescaped quote" in error for error in errors), errors
                )

    def test_rejects_unsupported_escape_in_quoted_scalar(self) -> None:
        _, errors = validate.parse_frontmatter(self.text('"Use when \\q appears"'))
        self.assertTrue(any("unsupported quote escape" in error for error in errors), errors)

    def test_rejects_plain_inline_comments(self) -> None:
        cases = {
            "space": "Use when this triggers # not part of the trigger",
            "tab": "Use when this triggers\t# not part of the trigger",
        }
        for label, value in cases.items():
            with self.subTest(label=label):
                _, errors = validate.parse_frontmatter(self.text(value))
                self.assertTrue(
                    any("inline YAML comment" in error for error in errors), errors
                )

    def test_rejects_reserved_leading_yaml_punctuation(self) -> None:
        punctuation = ("-", "?", ":", ",", "[", "]", "{", "}", "#", "|", ">", "%", "@", "`")
        for char in punctuation:
            with self.subTest(punctuation=char):
                _, errors = validate.parse_frontmatter(self.text(f"{char}value"))
                self.assertTrue(
                    any("reserved YAML punctuation" in error for error in errors), errors
                )


class LinkValidationTests(unittest.TestCase):
    def test_rejects_missing_link_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_skill(root, link="references/missing.md")
            errors = validate.check_markdown_links(root)
            self.assertTrue(any("does not exist" in error for error in errors), errors)

    def test_rejects_link_escaping_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            make_skill(root, link="../../outside.md")
            (root / "outside.md").write_text("# Outside\n", encoding="utf-8")
            errors = validate.check_markdown_links(root)
            self.assertTrue(any("escapes skill directory" in error for error in errors), errors)


class SourceValidationTests(unittest.TestCase):
    @staticmethod
    def write_source_fixture(root: Path, central_row: str, local_row: str) -> None:
        docs = root / "docs"
        docs.mkdir(parents=True, exist_ok=True)
        (docs / "sources.md").write_text(
            "\n".join(
                [
                    "# Sources",
                    "| ID | Date | URL | Theme | Skills using it |",
                    "| --- | --- | --- | --- | --- |",
                    central_row,
                    "",
                ]
            ),
            encoding="utf-8",
        )
        references = root / "skills" / "forge-demo" / "references"
        references.mkdir(parents=True, exist_ok=True)
        (references / "sources.md").write_text(
            "\n".join(
                [
                    "# Local sources",
                    "| ID | Date | URL | Relevance |",
                    "| --- | --- | --- | --- |",
                    local_row,
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def test_accepts_reciprocal_source_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = "| S01 | 2026-01-01 | https://example.com/s01 | theme | forge-demo |"
            local = "| S01 | 2026-01-01 | https://example.com/s01 | relevance |"
            self.write_source_fixture(root, row, local)
            self.assertEqual(validate.validate_sources(root, {"S01"}), [])

    def test_rejects_local_source_missing_from_catalogue(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = "| S01 | 2026-01-01 | https://example.com/s01 | theme | forge-demo |"
            local = "| S02 | 2026-01-02 | https://example.com/s02 | relevance |"
            self.write_source_fixture(root, row, local)
            errors = validate.validate_sources(root, {"S01"})
            self.assertTrue(
                any("missing from the central catalogue" in error for error in errors), errors
            )

    def test_rejects_wrong_canonical_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = "| S01 | 2026-01-01 | https://example.com/s01 | theme | forge-demo |"
            local = "| S01 | 2026-01-01 | https://example.com/s01 | relevance |"
            self.write_source_fixture(root, row, local)
            errors = validate.validate_sources(root, {"S01"}, check_canonical=True)
            self.assertTrue(any("canonical" in error for error in errors), errors)

    def test_canonical_s04_and_s05_are_distinct(self) -> None:
        self.assertEqual(
            validate.EXPECTED_SOURCE_METADATA["S04"],
            ("2026-09-01", "https://x.com/poteto/status/2094457600259842065"),
        )
        self.assertEqual(
            validate.EXPECTED_SOURCE_METADATA["S05"],
            ("2026-09-10", "https://x.com/poteto/status/2097732320606507506"),
        )
        self.assertNotEqual(
            validate.EXPECTED_SOURCE_METADATA["S04"],
            validate.EXPECTED_SOURCE_METADATA["S05"],
        )

    def test_repository_catalogue_keeps_s04_and_s05_distinct(self) -> None:
        text = (ROOT / "docs" / "sources.md").read_text(encoding="utf-8")
        rows, errors = validate.parse_source_rows(text, central=True)
        self.assertEqual(errors, [])
        found = {source_id: (date, url) for source_id, date, url, _rest in rows}
        self.assertEqual(
            found["S04"],
            ("2026-09-01", "https://x.com/poteto/status/2094457600259842065"),
        )
        self.assertEqual(
            found["S05"],
            ("2026-09-10", "https://x.com/poteto/status/2097732320606507506"),
        )
        self.assertNotEqual(found["S04"], found["S05"])

    def test_rejects_duplicate_canonical_source_url(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            central = "\n".join(
                [
                    "| S01 | 2026-01-01 | https://example.com/shared | theme | forge-demo |",
                    "| S02 | 2026-01-02 | https://example.com/shared | theme | forge-demo |",
                ]
            )
            local = "\n".join(
                [
                    "| S01 | 2026-01-01 | https://example.com/shared | relevance |",
                    "| S02 | 2026-01-02 | https://example.com/shared | relevance |",
                ]
            )
            self.write_source_fixture(root, central, local)
            errors = validate.validate_sources(root, {"S01", "S02"})
            self.assertTrue(any("duplicate canonical source URL" in error for error in errors), errors)

    def test_rejects_orphan_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            row = "| S01 | 2026-01-01 | https://example.com/s01 | theme |  |"
            local = "| S01 | 2026-01-01 | https://example.com/s01 | relevance |"
            self.write_source_fixture(root, row, local)
            errors = validate.validate_sources(root, {"S01"})
            self.assertTrue(any("orphan" in error for error in errors), errors)


class PublicationHygieneTests(unittest.TestCase):
    def test_detects_assembled_private_path_token_and_email(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            private_path = "/" + "home/" + "demo" + "/notes.txt"
            token = "ghp_" + "A" * 36
            email = "person" + "@" + "example" + "." + "org"
            (root / "notes.md").write_text(
                "\n".join([private_path, token, email]) + "\n", encoding="utf-8"
            )
            errors = validate.scan_publication(root)
            joined = "\n".join(errors)
            self.assertIn("private home path", joined)
            self.assertIn("possible GitHub token", joined)
            self.assertIn("email address", joined)

    def test_clean_fixture_passes_hygiene_scan(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "notes.md").write_text(
                "Use a synthetic fixture and an approved test account.\n", encoding="utf-8"
            )
            self.assertEqual(validate.scan_publication(root), [])

    def test_rejects_forbidden_artifact_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "artifacts").mkdir()
            (root / "artifacts" / "report.md").write_text("data\n", encoding="utf-8")
            errors = validate.check_forbidden_publication_artifacts(root)
            self.assertTrue(any("forbidden publication artifact directory" in error for error in errors), errors)

    def test_rejects_forbidden_log_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "debug.log").write_text("tool output\n", encoding="utf-8")
            errors = validate.check_forbidden_publication_artifacts(root)
            self.assertTrue(any("forbidden publication artifact file" in error for error in errors), errors)

    def test_flags_oversized_publication_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "large.txt").write_bytes(b"x" * (validate.MAX_SCAN_BYTES + 1))
            errors = validate.scan_publication(root)
            self.assertTrue(any("exceeds publication scan limit" in error for error in errors), errors)

    def test_manifest_accepts_exact_file_set(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("# Readme\n", encoding="utf-8")
            (root / "release-manifest.txt").write_text(
                "README.md\nrelease-manifest.txt\n", encoding="utf-8"
            )
            self.assertEqual(validate.validate_release_manifest(root), [])

    def test_manifest_rejects_unlisted_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("# Readme\n", encoding="utf-8")
            (root / "debug.log").write_text("tool output\n", encoding="utf-8")
            (root / "release-manifest.txt").write_text(
                "README.md\nrelease-manifest.txt\n", encoding="utf-8"
            )
            errors = validate.validate_release_manifest(root)
            self.assertTrue(any("not listed in the release manifest" in error for error in errors), errors)

    def test_manifest_rejects_log_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "release-manifest.txt").write_text(
                "release-manifest.txt\ndebug.log\n", encoding="utf-8"
            )
            (root / "debug.log").write_text("tool output\n", encoding="utf-8")
            errors = validate.validate_release_manifest(root)
            self.assertTrue(any("log, temporary, or archive files" in error for error in errors), errors)


class SmokeCaseTests(unittest.TestCase):
    @staticmethod
    def write_case(root: Path, schema: str) -> Path:
        case_path = root / "smoke-case.md"
        case_path.write_text(
            "\n".join(
                [
                    "# Case",
                    "Illustrative only; this is not a model-behavior test.",
                    "## Input",
                    "A synthetic request.",
                    "## Expected artifact schema",
                    "```json",
                    schema,
                    "```",
                    "## Expected status",
                    "`not-run` when blocked.",
                    "## Stop case",
                    "Stop when blocked.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        return case_path

    def test_repository_smoke_cases_are_valid(self) -> None:
        errors = smoke.validate_all(ROOT)
        self.assertEqual(errors, [], "\n".join(errors))

    def test_smoke_case_rejects_non_string_status_without_traceback(self) -> None:
        schemas = {
            "list status": (
                '{"status": ["evidence-ready"], '
                '"required_fields": ["status", "goal", "scope", "note"], '
                '"stop_status": "not-run"}'
            ),
            "dict status": (
                '{"status": {"value": "evidence-ready"}, '
                '"required_fields": ["status", "goal", "scope", "note"], '
                '"stop_status": "not-run"}'
            ),
            "list stop_status": (
                '{"status": "evidence-ready", '
                '"required_fields": ["status", "goal", "scope", "note"], '
                '"stop_status": ["not-run"]}'
            ),
            "dict stop_status": (
                '{"status": "evidence-ready", '
                '"required_fields": ["status", "goal", "scope", "note"], '
                '"stop_status": {"value": "not-run"}}'
            ),
        }
        for label, schema in schemas.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                case_path = self.write_case(Path(temp), schema)
                errors = smoke.validate_case(case_path)
                self.assertTrue(
                    any(
                        "status must be one of" in error
                        or "stop_status must be one of" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_smoke_case_rejects_unhashable_required_fields(self) -> None:
        schemas = {
            "list field": (
                '{"status": "evidence-ready", '
                '"required_fields": ["status", ["goal"], "scope", "note"], '
                '"stop_status": "not-run"}'
            ),
            "dict field": (
                '{"status": "evidence-ready", '
                '"required_fields": ["status", {"goal": true}, "scope", "note"], '
                '"stop_status": "not-run"}'
            ),
        }
        for label, schema in schemas.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                case_path = self.write_case(Path(temp), schema)
                errors = smoke.validate_case(case_path)
                self.assertTrue(
                    any("invalid artifact field name" in error for error in errors), errors
                )

    def test_smoke_case_rejects_missing_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case_path = root / "smoke-case.md"
            case_path.write_text(
                "\n".join(
                    [
                        "# Case",
                        "Illustrative only; this is not a model-behavior test.",
                        "## Input",
                        "A synthetic request.",
                        "## Expected artifact schema",
                        "```json",
                        '{"required_fields": ["status", "goal"], "stop_status": "not-run"}',
                        "```",
                        "## Expected status",
                        "`not-run` when blocked.",
                        "## Stop case",
                        "Stop when blocked.",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            errors = smoke.validate_case(case_path)
            self.assertTrue(any("status must be one of" in error for error in errors), errors)


class RepositoryTests(unittest.TestCase):
    def test_repository_passes_all_checks(self) -> None:
        errors = validate.validate_repository(ROOT)
        self.assertEqual(errors, [], "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
