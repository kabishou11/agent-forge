---
name: forge-depth-first-parallelism
description: Explore one or a few questions deeply with parallel attempts. Use when a failure has competing hypotheses, a reproduction is flaky, multiple isolated workspaces are available, or broad searching would waste effort without eliminating any explanation.
---

# Forge depth-first parallelism

Concentrate parallel capacity on a small number of questions. Give each attempt an explicit hypothesis and an elimination test, then converge on the evidence instead of collecting unrelated findings.

These instructions guide the assistant. They do not override host policies, approvals, sandbox rules, or user authority.

## Inputs

- One or a few questions worth answering, with the decision each will inform.
- Competing hypotheses and the observations that would eliminate each.
- Isolated workspaces: checkouts, ports, browser profiles, temporary storage, and test data.
- Available tools or models and their strengths.
- A shared place to record attempts and results.

## Workflow

1. Write the question and the maximum useful number of attempts.
2. Enumerate hypotheses with a predicted observation and a falsifier for each.
3. Confirm that attempts can run without sharing mutable state.
4. Assign one hypothesis or reproduction angle per attempt; specialize tools when useful.
5. Use the same baseline and artifact format so results are comparable.
6. Keep a shared ledger of attempt, hypothesis, command, result, and stop reason.
7. Stop losing attempts early; do not keep them alive to look busy.
8. Converge: compare elimination evidence and choose the best-supported explanation or next experiment.
9. Re-test the winner in a clean isolated environment before recommending a fix.
10. Record unresolved hypotheses and do not present parallel volume as confidence.

Breadth is useful only after a question is answered; do not spray unrelated tasks to increase apparent activity.

## Stop conditions

- Attempts would share a mutable database, port, account, or workspace.
- Resource limits make the comparison unreliable.
- No hypothesis has an observable elimination test.
- The question is already answered or no longer relevant. Stop and report `NOT RUN` for abandoned attempts.

## Deliverables

- The question, attempt budget, and isolation plan.
- Hypothesis ledger with predicted observations and falsifiers.
- Per-attempt commands, logs, results, and stop reasons.
- Elimination evidence and the chosen explanation or next step.
- Unresolved hypotheses and a clean re-test result when available.

## Example

**Input:** A test fails intermittently, and three explanations are plausible: timing, shared fixture state, or an order-dependent cache. Three isolated checkouts and ports are available.

**Expected output:** Three attempts run the same test with variant conditions. Timing is eliminated by a slowed clock, shared fixture state is eliminated by a per-attempt database, and the cache hypothesis survives. The winner is re-tested in a clean workspace, and the ledger records why the other two stopped.

**Stop case:** All attempts would use one shared database and no isolated instance can be created. Stop before running with `NOT RUN`, document the isolation gap, and do not compare contaminated results.

## Sources

- Local source map with dates and canonical URLs: [references/sources.md](references/sources.md)
- Deeper notes on hypothesis ledgers: [references/field-guide.md](references/field-guide.md)
- Synthetic selection case: [references/smoke-case.md](references/smoke-case.md)
