"""Execute the documented copy snippets in project-scoped temporary directories.

These tests cover file copying, bundle completeness, link resolution, and refusal
guards. They do not test host discovery or whether a model follows a skill.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate

README_FILES = ("README.md", "README.zh-CN.md")
BASH_BLOCK_RE = re.compile(r"```bash\r?\n(.*?)```", re.DOTALL)
SKILL_RE = re.compile(r"^SKILL=(forge-[a-z0-9-]+)$", re.MULTILINE)
TARGET_RE = re.compile(r"(\.agents/skills|\.opencode/skills)")


def install_blocks(text: str) -> list[str]:
    return [
        block.strip() + "\n"
        for block in BASH_BLOCK_RE.findall(text)
        if "TARGET=../target-project" in block and "cp -R" in block
    ]


def block_details(block: str) -> tuple[str, str]:
    skill_match = SKILL_RE.search(block)
    target_match = TARGET_RE.search(block)
    if skill_match is None or target_match is None:
        raise AssertionError(f"install block is missing a skill or target: {block!r}")
    return target_match.group(1), skill_match.group(1)


def snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def prepare_workspace(temp: Path) -> tuple[Path, Path]:
    repo = temp / "repo"
    repo.mkdir()
    shutil.copytree(ROOT / "skills", repo / "skills")
    target = temp / "target-project"
    notes = target / "notes"
    notes.mkdir(parents=True)
    sentinel = notes / "user-note.txt"
    sentinel.write_text("user content stays here\n", encoding="utf-8")
    return repo, target


def run_block(repo: Path, block: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        ["bash", "-eu", "-c", block],
        cwd=repo,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


class DocumentedInstallationTests(unittest.TestCase):
    def test_readmes_share_the_same_install_snippets(self) -> None:
        snippets = {
            name: install_blocks((ROOT / name).read_text(encoding="utf-8"))
            for name in README_FILES
        }
        for name, blocks in snippets.items():
            with self.subTest(readme=name):
                self.assertEqual(len(blocks), 2)
        self.assertEqual(snippets["README.md"], snippets["README.zh-CN.md"])
        combined = "\n".join(snippets["README.md"])
        self.assertIn(".agents/skills", combined)
        self.assertIn(".opencode/skills", combined)
        self.assertIn("forge-intent-alignment", combined)
        self.assertIn("forge-verification-harness", combined)
        self.assertNotIn("$HOME", combined)
        self.assertNotIn("~", combined)

    def test_documented_copy_installs_exact_self_contained_bundle(self) -> None:
        for name in README_FILES:
            blocks = install_blocks((ROOT / name).read_text(encoding="utf-8"))
            for block in blocks:
                subdir, skill = block_details(block)
                with self.subTest(readme=name, skill=skill):
                    with tempfile.TemporaryDirectory(
                        dir=ROOT, prefix=".forge-install-test-"
                    ) as temp:
                        repo, target = prepare_workspace(Path(temp))
                        result = run_block(repo, block)
                        self.assertEqual(result.returncode, 0, result.stderr)

                        destination = target / subdir / skill
                        source = ROOT / "skills" / skill
                        self.assertEqual(snapshot(destination), snapshot(source))
                        self.assertEqual(
                            (destination / "SKILL.md").read_text(encoding="utf-8"),
                            (source / "SKILL.md").read_text(encoding="utf-8"),
                        )
                        for relative in (
                            "LICENSE",
                            "NOTICES.md",
                            "references/field-guide.md",
                            "references/sources.md",
                            "references/smoke-case.md",
                        ):
                            self.assertTrue((destination / relative).is_file(), relative)

                        self.assertEqual(validate.validate_skill_bundle(destination), [])
                        self.assertEqual(validate.check_markdown_links(destination), [])
                        self.assertEqual(
                            (target / "notes" / "user-note.txt").read_text(encoding="utf-8"),
                            "user content stays here\n",
                        )

    def test_guard_refuses_existing_directory_without_changing_it(self) -> None:
        for name in README_FILES:
            blocks = install_blocks((ROOT / name).read_text(encoding="utf-8"))
            for block in blocks:
                subdir, skill = block_details(block)
                with self.subTest(readme=name, skill=skill):
                    with tempfile.TemporaryDirectory(
                        dir=ROOT, prefix=".forge-install-test-"
                    ) as temp:
                        repo, target = prepare_workspace(Path(temp))
                        first = run_block(repo, block)
                        self.assertEqual(first.returncode, 0, first.stderr)
                        destination = target / subdir / skill
                        before = snapshot(destination)

                        second = run_block(repo, block)
                        self.assertNotEqual(second.returncode, 0)
                        self.assertIn(
                            "Refusing to overwrite existing destination", second.stderr
                        )
                        self.assertEqual(snapshot(destination), before)
                        self.assertEqual(
                            (target / "notes" / "user-note.txt").read_text(encoding="utf-8"),
                            "user content stays here\n",
                        )

    def test_guard_refuses_existing_file_without_changing_it(self) -> None:
        for name in README_FILES:
            blocks = install_blocks((ROOT / name).read_text(encoding="utf-8"))
            for block in blocks:
                subdir, skill = block_details(block)
                with self.subTest(readme=name, skill=skill):
                    with tempfile.TemporaryDirectory(
                        dir=ROOT, prefix=".forge-install-test-"
                    ) as temp:
                        repo, target = prepare_workspace(Path(temp))
                        destination = target / subdir / skill
                        destination.parent.mkdir(parents=True)
                        destination.write_text("keep this file\n", encoding="utf-8")

                        result = run_block(repo, block)
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn(
                            "Refusing to overwrite existing destination", result.stderr
                        )
                        self.assertEqual(
                            destination.read_text(encoding="utf-8"), "keep this file\n"
                        )

    def test_guard_refuses_existing_symlink_without_touching_target(self) -> None:
        for name in README_FILES:
            blocks = install_blocks((ROOT / name).read_text(encoding="utf-8"))
            for block in blocks:
                subdir, skill = block_details(block)
                with self.subTest(readme=name, skill=skill):
                    with tempfile.TemporaryDirectory(
                        dir=ROOT, prefix=".forge-install-test-"
                    ) as temp:
                        temp_path = Path(temp)
                        repo, target = prepare_workspace(temp_path)
                        user_dir = target / "user-skill-placeholder"
                        user_dir.mkdir()
                        sentinel = user_dir / "keep.txt"
                        sentinel.write_text("user content stays here\n", encoding="utf-8")
                        destination = target / subdir / skill
                        destination.parent.mkdir(parents=True)
                        destination.symlink_to(user_dir, target_is_directory=True)

                        result = run_block(repo, block)
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn(
                            "Refusing to overwrite existing destination", result.stderr
                        )
                        self.assertTrue(destination.is_symlink())
                        self.assertEqual(
                            sentinel.read_text(encoding="utf-8"),
                            "user content stays here\n",
                        )
                        self.assertEqual(
                            (target / "notes" / "user-note.txt").read_text(encoding="utf-8"),
                            "user content stays here\n",
                        )


if __name__ == "__main__":
    unittest.main()
