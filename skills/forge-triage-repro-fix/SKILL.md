---
name: forge-triage-repro-fix
description: Run a stoppable triage, reproduction, and fix loop for a reported defect. Use when a bug report arrives, a failure needs a failing test, a fix is risky, or non-bug, failed reproduction, and stopped repair need to count as valid outcomes instead of forcing code.
---

# Forge triage, reproduce, fix

Treat each stage as independently stoppable. Establish what is observed, reproduce it exactly, learn the mechanism, then make the smallest defensible repair and prove it against the same scenario.

These instructions guide the assistant. They do not override host policies, approvals, sandbox rules, or user authority.

## Inputs

- The original report, quoted without adopting its speculative root cause.
- The closest available environment and the verification harness or manual steps.
- Logs, artifacts, versions, and configuration relevant to the report.
- Ownership, compatibility, and review constraints.
- A place to store reproduction and before/after artifacts.

## Workflow

1. Triage: restate the report in observable terms and decide whether it is a defect, expected behavior, duplicate, or unknown.
2. Reproduce the exact report first. Save commands, inputs, environment, and artifacts.
3. If reproduction fails, report that result; do not substitute a nearby bug and call it the same issue.
4. Write a failing test or deterministic check that captures the reproduced behavior.
5. Explain the mechanism: how it happens, why the code has that shape, and what related history matters.
6. Choose the smallest fix with the least code that addresses the mechanism rather than masking the symptom.
7. Verify before and after with the same exact reproduction and the focused test.
8. Check consumers outside the immediate diff, including themes, states, roles, and callers, when the change is broad.
9. Record the decision log and any residual risk.
10. Stop at any stage when evidence, safety, or scope does not support continuing. A stopped repair is a valid result.

Do not turn "the fix might be risky" into an unbounded rewrite. Bound the repair and name what is excluded.

## Stop conditions

- Triage concludes this is not a bug, is a duplicate, or is working as intended.
- The exact report cannot be reproduced in an approved environment.
- The fix needs a migration, approval, or ownership change beyond the task.
- The smallest safe fix cannot be bounded.
- Verification is blocked. Report `NOT RUN` for the missing execution, not a guessed outcome.

## Deliverables

- Triage verdict with evidence and the quoted report.
- Reproduction commands and artifacts, or a documented failed reproduction.
- A failing test before the fix and its passing result after.
- A concise mechanism note covering how, why, and relevant history.
- The fix, verification artifacts, residual risk, and decision log.
- A clear stopped state when applicable.

## Example

**Input:** "Saving a draft loses the second tag." The reporter guesses a cache bug, but the report includes a two-tag example and the app version.

**Expected output:** Triage records a likely defect without adopting the cache theory. The exact two-tag flow is reproduced, a failing test captures the second tag being dropped, and the mechanism is traced to request parsing. A bounded parser fix is verified with the same flow and a consumer check for both tag fields.

**Stop case:** The exact flow cannot run because the test account lacks draft permissions. Stop after triage with `NOT RUN`, document the blocked reproduction, and do not change the parser on a hunch.

## Sources

- Local source map with dates and canonical URLs: [references/sources.md](references/sources.md)
- Deeper notes on reproduction and bounded repair: [references/field-guide.md](references/field-guide.md)
- Synthetic selection case: [references/smoke-case.md](references/smoke-case.md)
