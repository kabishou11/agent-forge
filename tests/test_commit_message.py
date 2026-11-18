from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_commit_message


class CommitMessageTests(unittest.TestCase):
    def test_accepts_documented_subject_forms(self) -> None:
        subjects = (
            "feat(triage): add deterministic reproduction demo",
            "fix(install): refuse to overwrite an existing output",
            "docs(readme): explain project-local installation",
            "test(docs): execute the installation snippets",
            "chore(repo): remove stale cache files",
        )
        for subject in subjects:
            with self.subTest(subject=subject):
                self.assertEqual(check_commit_message.validate_message(subject), [])

    def test_accepts_body_and_footer(self) -> None:
        message = "\n".join(
            [
                "fix(install): refuse existing destinations",
                "",
                "Check for files, directories, and symlinks before copying.",
                "",
                "Refs: installation-guard",
            ]
        )
        self.assertEqual(check_commit_message.validate_message(message), [])

    def test_rejects_uppercase_type_and_summary(self) -> None:
        cases = (
            "Feat(readme): add a demo",
            "feat(Readme): add a demo",
            "feat(readme): Add a demo",
        )
        for message in cases:
            with self.subTest(message=message):
                errors = check_commit_message.validate_message(message)
                self.assertTrue(errors, message)

    def test_rejects_missing_colon_and_empty_scope(self) -> None:
        cases = (
            "feat add a demo",
            "feat(): add a demo",
            "feat(scope):",
        )
        for message in cases:
            with self.subTest(message=message):
                errors = check_commit_message.validate_message(message)
                self.assertTrue(errors, message)

    def test_rejects_unscoped_subject(self) -> None:
        cases = (
            "feat: add a demo",
            "docs: explain installation",
        )
        for message in cases:
            with self.subTest(message=message):
                errors = check_commit_message.validate_message(message)
                self.assertTrue(
                    any("type(scope): summary" in error for error in errors), errors
                )

    def test_rejects_trailing_period_and_long_subject(self) -> None:
        cases = (
            "feat(example): add a demo.",
            "feat(example): " + "x" * check_commit_message.MAX_SUBJECT_LENGTH,
        )
        for message in cases:
            with self.subTest(message=message):
                errors = check_commit_message.validate_message(message)
                self.assertTrue(errors, message)

    def test_rejects_coauthor_and_tool_trailers(self) -> None:
        coauthor = (
            "feat(example): add a demo\n\nCo-authored-by: Someone <"
            + "person"
            + "@"
            + "example"
            + "."
            + "org"
            + ">"
        )
        cases = (
            coauthor,
            "feat(example): add a demo\n\n" + "Generated " + "with a local tool",
            "feat(example): add a demo\n\n" + "Made " + "by a local tool",
            "feat(example): add a demo\n\n" + "tool-" + "generated signature",
        )
        for message in cases:
            with self.subTest(message=message):
                errors = check_commit_message.validate_message(message)
                self.assertTrue(errors, message)

    def test_rejects_empty_message(self) -> None:
        self.assertTrue(check_commit_message.validate_message(""))
        self.assertTrue(check_commit_message.validate_message("\n\n"))


if __name__ == "__main__":
    unittest.main()
