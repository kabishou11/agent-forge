from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "triage-repro-fix"
DEMO = EXAMPLE / "run_demo.py"


def run_demo(
    workdir: Path, output: str, demo: Path = DEMO
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(demo), "--output", output],
        cwd=workdir,
        capture_output=True,
        text=True,
        check=False,
    )


def copied_example(workdir: Path) -> Path:
    example = workdir / "example"
    shutil.copytree(
        EXAMPLE,
        example,
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    return example


class ExampleWorkflowTests(unittest.TestCase):
    def test_demo_produces_checked_artifacts(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".forge-example-test-") as temp:
            workdir = Path(temp)
            result = run_demo(workdir, "artifacts")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("status: evidence-ready", result.stdout)

            output = workdir / "artifacts"
            expected = {
                "bounded-fix.diff",
                "evidence-review.md",
                "intent-brief.md",
                "repro-failure.txt",
                "result.json",
                "review-checks.json",
                "verification-pass.txt",
            }
            self.assertEqual(
                {path.name for path in output.iterdir() if path.is_file()},
                expected,
            )

            data = json.loads((output / "result.json").read_text(encoding="utf-8"))
            self.assertEqual(data["status"], "evidence-ready")
            self.assertEqual(data["scenario"], "synthetic dropped-second-tag report")
            self.assertNotEqual(data["repro_exit"], 0)
            self.assertEqual(data["verification_exit"], 0)
            self.assertEqual(data["review_status"], "pass")
            self.assertTrue(data["reproduction_ok"])
            self.assertTrue(data["verification_ok"])
            self.assertTrue(data["review_ok"])
            self.assertFalse(data["model_behavior_tested"])

            repro = (output / "repro-failure.txt").read_text(encoding="utf-8")
            verification = (output / "verification-pass.txt").read_text(encoding="utf-8")
            self.assertIn("exit: 1", repro)
            self.assertIn("FAILED", repro)
            self.assertIn("exit: 0", verification)
            self.assertIn("OK", verification)

            diff = (output / "bounded-fix.diff").read_text(encoding="utf-8")
            self.assertIn('parts if part][:1]', diff)
            self.assertIn('parts if part]\n', diff)

            intent = (output / "intent-brief.md").read_text(encoding="utf-8")
            self.assertIn("Theory, not evidence", intent)
            self.assertIn("cache", intent)
            self.assertIn("alpha", intent)

            review = (output / "evidence-review.md").read_text(encoding="utf-8")
            self.assertIn("Verdict: `evidence-ready`", review)
            self.assertIn("Reproduction: `pass`", review)
            self.assertIn("Verification: `pass`", review)
            self.assertIn("Review: `pass`", review)
            self.assertIn("does not test whether a language model follows a skill", review)

            leftovers = [
                path.name
                for path in workdir.iterdir()
                if path.name.startswith(".forge-demo-work-")
            ]
            self.assertEqual(leftovers, [])

    def test_demo_refuses_existing_output_directory(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".forge-example-test-") as temp:
            workdir = Path(temp)
            output = workdir / "artifacts"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("user content\n", encoding="utf-8")
            result = run_demo(workdir, "artifacts")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to overwrite existing output path", result.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "user content\n")
            self.assertEqual({path.name for path in output.iterdir()}, {"keep.txt"})

    def test_demo_requires_a_relative_output_path(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".forge-example-test-") as temp:
            workdir = Path(temp)
            output = workdir / "absolute-output"
            result = run_demo(workdir, str(output))
            self.assertEqual(result.returncode, 2)
            self.assertIn("output must be relative", result.stderr)
            self.assertFalse(output.exists())

    def test_demo_refuses_existing_output_symlink(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".forge-example-test-") as temp:
            workdir = Path(temp)
            target = workdir / "user-target"
            target.mkdir()
            sentinel = target / "keep.txt"
            sentinel.write_text("user content\n", encoding="utf-8")
            (workdir / "artifacts").symlink_to(target, target_is_directory=True)
            result = run_demo(workdir, "artifacts")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to overwrite existing output path", result.stderr)
            self.assertTrue((workdir / "artifacts").is_symlink())
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "user content\n")


class ExampleFailureModeTests(unittest.TestCase):
    def assert_needs_work(self, output: Path) -> dict:
        data = json.loads((output / "result.json").read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "needs-work")
        self.assertNotEqual(data["status"], "evidence-ready")
        review = (output / "evidence-review.md").read_text(encoding="utf-8")
        self.assertIn("Verdict: `needs-work`", review)
        self.assertNotIn("Verdict: `evidence-ready`", review)
        self.assertTrue((output / "repro-failure.txt").is_file())
        return data

    def test_invalid_reproduction_is_not_evidence_ready(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".forge-example-test-") as temp:
            workdir = Path(temp)
            example = copied_example(workdir)
            (example / "fixture" / "buggy_tags.py").write_text(
                "def split_tags(:\n", encoding="utf-8"
            )
            result = run_demo(workdir, "artifacts", example / "run_demo.py")
            self.assertNotEqual(result.returncode, 0)
            data = self.assert_needs_work(workdir / "artifacts")
            self.assertNotEqual(data["repro_exit"], 0)
            self.assertFalse(data["reproduction_ok"])
            self.assertTrue(data["verification_ok"])
            notes = " ".join(data["gate_notes"]["reproduction"])
            self.assertIn("syntax", notes)

    def test_unexpected_pass_before_repair_is_not_evidence_ready(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".forge-example-test-") as temp:
            workdir = Path(temp)
            example = copied_example(workdir)
            buggy = example / "fixture" / "buggy_tags.py"
            buggy.write_text(
                (example / "fixture" / "fixed_tags.py").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            result = run_demo(workdir, "artifacts", example / "run_demo.py")
            self.assertNotEqual(result.returncode, 0)
            data = self.assert_needs_work(workdir / "artifacts")
            self.assertEqual(data["repro_exit"], 0)
            self.assertFalse(data["reproduction_ok"])
            self.assertTrue(data["verification_ok"])

    def test_failure_after_repair_is_not_evidence_ready(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".forge-example-test-") as temp:
            workdir = Path(temp)
            example = copied_example(workdir)
            fixed = example / "fixture" / "fixed_tags.py"
            fixed.write_text(
                (example / "fixture" / "buggy_tags.py").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            result = run_demo(workdir, "artifacts", example / "run_demo.py")
            self.assertNotEqual(result.returncode, 0)
            data = self.assert_needs_work(workdir / "artifacts")
            self.assertTrue(data["reproduction_ok"])
            self.assertNotEqual(data["verification_exit"], 0)
            self.assertFalse(data["verification_ok"])

    def test_review_edge_failure_blocks_evidence_ready(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT, prefix=".forge-example-test-") as temp:
            workdir = Path(temp)
            example = copied_example(workdir)
            fixed = example / "fixture" / "fixed_tags.py"
            fixed.write_text(
                "\n".join(
                    [
                        '"""Synthetic fixture with a narrow repair."""',
                        "",
                        "",
                        "def split_tags(raw: str) -> list[str]:",
                        '    parts = [part.strip() for part in raw.split(",")]',
                        "    return list(dict.fromkeys(part for part in parts if part))",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            result = run_demo(workdir, "artifacts", example / "run_demo.py")
            self.assertNotEqual(result.returncode, 0)
            data = self.assert_needs_work(workdir / "artifacts")
            self.assertTrue(data["reproduction_ok"])
            self.assertTrue(data["verification_ok"])
            self.assertEqual(data["review_status"], "fail")
            self.assertFalse(data["review_ok"])


if __name__ == "__main__":
    unittest.main()
