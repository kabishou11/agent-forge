# Triage, reproduce, fix demo

A self-contained, offline example for the [forge-triage-repro-fix](../../skills/forge-triage-repro-fix/SKILL.md) workflow. It turns a synthetic bug report into an intent brief, a deterministic failing regression, a bounded repair, a passing rerun of the same test, and an evidence review.

This executes the artifact flow. It does not test whether a language model follows the skill, and it does not use real project data.

## Run it

From the repository root:

```bash
python3 examples/triage-repro-fix/run_demo.py --output .forge-demo-output
```

Expected final lines:

```text
status: evidence-ready
artifacts: .forge-demo-output
```

The output path is relative and must not already exist. The demo refuses to overwrite it. Delete `.forge-demo-output` after inspecting the artifacts; it is not part of the repository.

## What the script does

1. Reads the [synthetic bug report](bug-report.md) and writes an intent brief that keeps the reporter's cache theory separate from observed behavior.
2. Copies the [buggy fixture](fixture/buggy_tags.py) into an isolated workspace beneath the current checkout.
3. Runs the [regression test](fixture/test_tags.py) and requires the expected assertion failures for the dropped tag, not just any nonzero exit.
4. Applies the [bounded repair](fixture/fixed_tags.py) and reruns the same test, checking that it passes.
5. Runs [additional review checks](fixture/review_checks.py) and writes an evidence review.
6. Removes the temporary workspace and leaves only the requested artifacts.

An import, syntax, or harness error is preserved in `repro-failure.txt` but does not count as reproduction. Unexpected passing before the repair, failure after the repair, or failed review checks all produce `needs-work`.

## Artifacts

- `intent-brief.md` records the quoted report, the untested theory, and acceptance checks.
- `repro-failure.txt` shows the regression test failing before the repair.
- `bounded-fix.diff` shows the one-line change.
- `verification-pass.txt` shows the same test passing after the repair.
- `review-checks.json` records the executed edge checks.
- `evidence-review.md` states the verdict and the untested boundary.
- `result.json` records the status, stage gates, exit codes, and gate notes.

## Check the example

```bash
python3 -m unittest discover -s tests -v
```

The test suite runs this demo in a project-scoped temporary directory and checks the artifacts, the expected failing-before/passing-after sequence, the repair diff, and the review status. It also mutates copied fixtures to check invalid reproduction, unexpected passing before repair, failure after repair, and review-only failure. Host discovery and model behavior remain outside the test.
