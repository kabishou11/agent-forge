#!/usr/bin/env python3

from __future__ import annotations

import argparse
import difflib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXAMPLE_DIR = Path(__file__).resolve().parent
FIXTURE_DIR = EXAMPLE_DIR / "fixture"
BUG_REPORT = EXAMPLE_DIR / "bug-report.md"
EXPECTED_REPRO_FAILURES = (
    "test_keeps_both_tags",
    "test_strips_empty_segments",
)
HARNESS_ERROR_MARKERS = (
    "SyntaxError",
    "IndentationError",
    "ImportError",
    "ModuleNotFoundError",
    "Failed to import test module",
    "_FailedTest",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_python(workspace: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    return subprocess.run(
        [sys.executable, *args],
        cwd=workspace,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def transcript(command: list[str], result: subprocess.CompletedProcess[str]) -> str:
    return "\n".join(
        [
            "$ python " + " ".join(command),
            f"exit: {result.returncode}",
            "",
            "stdout:",
            result.stdout.rstrip(),
            "",
            "stderr:",
            result.stderr.rstrip(),
            "",
        ]
    )


def check_reproduction(result: subprocess.CompletedProcess[str]) -> tuple[bool, list[str]]:
    output = "\n".join([result.stdout, result.stderr])
    problems: list[str] = []
    if result.returncode == 0:
        problems.append("the regression test passed before the repair")
    if "ERROR:" in output or "errors=" in output or any(
        marker in output for marker in HARNESS_ERROR_MARKERS
    ):
        problems.append("the failed run contains a harness, import, or syntax error")
    for name in EXPECTED_REPRO_FAILURES:
        if f"FAIL: {name}" not in output:
            problems.append(f"missing expected assertion failure: {name}")
    expected_count = f"FAILED (failures={len(EXPECTED_REPRO_FAILURES)})"
    if expected_count not in output:
        problems.append(f"expected {expected_count!r} in the reproduction output")
    if "AssertionError" not in output:
        problems.append("the reproduction output has no AssertionError")
    return not problems, problems


def check_verification(result: subprocess.CompletedProcess[str]) -> tuple[bool, list[str]]:
    output = "\n".join([result.stdout, result.stderr])
    problems: list[str] = []
    if result.returncode != 0:
        problems.append("the regression test did not pass after the repair")
    if "OK" not in output:
        problems.append("the verification output has no OK result")
    if "FAILED" in output or "ERROR:" in output:
        problems.append("the verification output still contains a failure or error")
    return not problems, problems


def check_review(
    result: subprocess.CompletedProcess[str], review_status: str
) -> tuple[bool, list[str]]:
    problems: list[str] = []
    if result.returncode != 0:
        problems.append("the review checks did not complete successfully")
    if review_status != "pass":
        problems.append(f"the review checks reported {review_status!r}")
    return not problems, problems


def write_intent(output: Path, report: str) -> None:
    text = "\n".join(
        [
            "# Intent brief",
            "",
            "## Report (verbatim)",
            "",
            *[f"> {line}" if line else ">" for line in report.splitlines()],
            "",
            "## Observations",
            "",
            "- A draft with two tags saves only the first tag.",
            "- The report supplies steps, expected behavior, and actual behavior.",
            "- The report supplies no log, version, production account, or performance target.",
            "",
            "## Theory, not evidence",
            "",
            "- The cache explanation is the reporter's guess. This demo does not test the cache.",
            "",
            "## Acceptance checks",
            "",
            "- `split_tags(\"alpha, beta\")` returns both tags in order.",
            "- Surrounding whitespace and empty segments are ignored.",
            "- Empty input returns an empty list.",
            "- The same regression test fails before the repair and passes after it.",
            "",
            "## Scope",
            "",
            "- One synthetic parsing function and one bounded repair.",
            "- No network, production data, real user content, or cache behavior.",
            "",
        ]
    )
    (output / "intent-brief.md").write_text(text, encoding="utf-8")


def build_diff() -> str:
    before = read(FIXTURE_DIR / "buggy_tags.py").splitlines(keepends=True)
    after = read(FIXTURE_DIR / "fixed_tags.py").splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            before,
            after,
            fromfile="tags.py (before)",
            tofile="tags.py (after)",
        )
    )


def write_review(
    output: Path,
    gates: dict[str, bool],
    notes: dict[str, list[str]],
    review_checks: int,
) -> None:
    verdict = "evidence-ready" if all(gates.values()) else "needs-work"
    stages = (
        ("Reproduction", "reproduction", "repro-failure.txt"),
        ("Verification", "verification", "verification-pass.txt"),
        ("Review", "review", "review-checks.json"),
    )
    lines = [
        "# Evidence review",
        "",
        f"Verdict: `{verdict}` for this synthetic fixture.",
        "",
        "## Stage gates",
        "",
        "- Intent and acceptance checks: `intent-brief.md`.",
        "- Repair: one bounded change (`bounded-fix.diff`).",
    ]
    for label, key, artifact in stages:
        state = "pass" if gates[key] else "fail"
        detail = "; ".join(notes[key]) if notes[key] else "expected result observed"
        if key == "review":
            detail = f"{review_checks} edge checks executed; {detail}"
        lines.append(f"- {label}: `{state}` — {detail} (`{artifact}`).")
    if not all(gates.values()):
        lines.extend(["", "## Blocking findings", ""])
        for label, key, _artifact in stages:
            if not gates[key]:
                lines.append(f"- {label}: {'; '.join(notes[key])}")
    lines.extend(
        [
            "",
            "## Untested",
            "",
            "- This fixture does not test whether a language model follows a skill.",
            "- It does not test host discovery or installation.",
            "- It does not test real project code, cache behavior, or production data.",
            "",
        ]
    )
    (output / "evidence-review.md").write_text("\n".join(lines), encoding="utf-8")


def run(output: Path) -> int:
    report = read(BUG_REPORT)
    output.mkdir(parents=True, exist_ok=True)
    write_intent(output, report)
    (output / "bounded-fix.diff").write_text(build_diff(), encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix=".forge-demo-work-", dir=Path.cwd()) as temp:
        workspace = Path(temp)
        shutil.copyfile(FIXTURE_DIR / "buggy_tags.py", workspace / "tags.py")
        shutil.copyfile(FIXTURE_DIR / "test_tags.py", workspace / "test_tags.py")
        shutil.copyfile(FIXTURE_DIR / "review_checks.py", workspace / "review_checks.py")

        test_command = ["-m", "unittest", "-v", "test_tags"]
        repro = run_python(workspace, test_command)
        (output / "repro-failure.txt").write_text(
            transcript(test_command, repro), encoding="utf-8"
        )

        shutil.copyfile(FIXTURE_DIR / "fixed_tags.py", workspace / "tags.py")
        verification = run_python(workspace, test_command)
        (output / "verification-pass.txt").write_text(
            transcript(test_command, verification), encoding="utf-8"
        )

        review = run_python(workspace, ["review_checks.py"])
        (output / "review-checks.json").write_text(review.stdout, encoding="utf-8")
        try:
            review_data = json.loads(review.stdout)
        except json.JSONDecodeError:
            review_data = {"status": "fail", "checks": 0}

    review_status = str(review_data.get("status", "fail"))
    review_checks = int(review_data.get("checks", 0))
    reproduction_ok, reproduction_notes = check_reproduction(repro)
    verification_ok, verification_notes = check_verification(verification)
    review_ok, review_notes = check_review(review, review_status)
    gates = {
        "reproduction": reproduction_ok,
        "verification": verification_ok,
        "review": review_ok,
    }
    notes = {
        "reproduction": reproduction_notes,
        "verification": verification_notes,
        "review": review_notes,
    }
    status = "evidence-ready" if all(gates.values()) else "needs-work"

    write_review(output, gates, notes, review_checks)
    result = {
        "scenario": "synthetic dropped-second-tag report",
        "status": status,
        "repro_exit": repro.returncode,
        "verification_exit": verification.returncode,
        "review_status": review_status,
        "review_checks": review_checks,
        "reproduction_ok": reproduction_ok,
        "verification_ok": verification_ok,
        "review_ok": review_ok,
        "gate_notes": notes,
        "model_behavior_tested": False,
        "artifacts": sorted(
            {path.name for path in output.iterdir() if path.is_file()} | {"result.json"}
        ),
    }
    (output / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )

    print(f"status: {status}")
    print(f"artifacts: {output}")
    if status != "evidence-ready":
        print(
            "expected a failing reproduction, a passing verification, and passing review checks",
            file=sys.stderr,
        )
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the synthetic triage, reproduction, fix, and review demo."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="relative directory for output artifacts; must not already exist",
    )
    args = parser.parse_args(argv)
    output = Path(args.output)
    if output.is_absolute():
        print("output must be relative to the current directory", file=sys.stderr)
        return 2
    try:
        output.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        print("output must stay inside the current checkout", file=sys.stderr)
        return 2
    if output.exists() or output.is_symlink():
        print(
            f"Refusing to overwrite existing output path: {output}",
            file=sys.stderr,
        )
        return 1
    return run(output)


if __name__ == "__main__":
    raise SystemExit(main())
