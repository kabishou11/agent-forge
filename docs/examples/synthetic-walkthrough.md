# Synthetic walkthrough

This is an illustrative, offline example. It uses a fictional export flow and invented observations. It is not a behavioral evaluation, a benchmark, or proof that a host will follow the skills.

## Scenario input

A fictional service has a nightly "ledger export" with two callers. A synthetic report says:

> "The export is too slow and sometimes skips the last page. Please make it faster and fix the missing rows before Friday. I think the cache is dropping the page."

There is no baseline duration, no target, and no approved production account. A local fixture with 1,000 generated rows and a test-only account is available.

## Expected composition

1. **forge-intent-alignment** separates the report from the cache theory, restates the goal as "same rows, faster with a measured target", and records the missing target as an assumption.
2. **forge-signal-first-context** reads the export entry point, the pagination boundary, the nearest test, and the fixture configuration. It excludes unrelated UI files and records the sampling.
3. **forge-verification-harness** builds a local driver that starts the export with the generated fixture, waits for completion, and records row count and checksum. It uses an isolated port and temporary storage.
4. **forge-triage-repro-fix** attempts the exact report. The missing last page reproduces with the fixture; the timing claim is marked unmeasured because no stable baseline exists.
5. **forge-architectural-constraints** is considered because the paging bug may recur, but no change is made until the mechanism is known. The decision log records the deferral.

## Checkable expected output

- An intent brief that quotes the report, labels the cache statement as a theory, and lists the missing performance target as an open assumption.
- A context packet naming the export entry point, the pagination boundary, the closest test, and the fixture.
- A harness command with `--help` and `--json` behavior, plus one complete local run artifact containing row count and checksum.
- A reproduction artifact for the missing-page behavior and a failing test that fails for the same reason.
- A final status that says the missing-page defect was reproduced, while the performance claim remains `NOT RUN` because no stable baseline was approved.

## Stop case

If the synthetic fixture cannot run because the test account is unavailable, the workflow stops after triage. The report records `NOT RUN` for reproduction and verification, keeps the repository unchanged, and does not claim the cache theory is correct or the rows are fixed.

## What this example does not show

- It does not execute in this repository.
- It does not prove the skills improve outcomes.
- It does not establish host discovery or installation behavior.
- It does not replace required review, approvals, or security checks.
