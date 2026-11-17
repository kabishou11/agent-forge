---
name: forge-context-budget
description: Budget context, skills, and tokens deliberately for a coding task. Use when a session is overloaded, many skills could apply, logs or routine events are expensive, a workflow needs ablation, or an agent is reading broadly instead of answering a specific question.
---

# Forge context and token budget

Spend context on the next decision, not on everything available. Load only skills that match the task, keep provenance for included material, and measure whether extra instructions actually help.

These instructions guide the assistant. They do not override host policies, approvals, sandbox rules, model limits, or user authority.

## Inputs

- The current question and the next decision it supports.
- Candidate skills, references, files, logs, and external context.
- Known costs: context size, latency, tool calls, and routine event volume.
- Model or workflow changes that may affect which instructions are useful.
- A place to record the context manifest and any ablation result.

## Workflow

1. State the question and the smallest evidence needed to answer it.
2. Select skills by their when-to-use descriptions; record why each was loaded.
3. Load a main skill first and open references on demand.
4. Prefer targeted excerpts, symbols, and summaries with paths over full-file dumps.
5. Delegate narrow searches or parallel attempts when they reduce repeated context.
6. Script repeated mechanical work and filter expensive routine events before they enter the main loop.
7. Separate outer-loop context gathering from inner-loop execution; re-evaluate when the question changes.
8. When instructions change, ablate one section at a time and compare observable effects.
9. Treat an unmeasured ablation as a hypothesis, not an improvement claim.
10. Drop stale references and record what was excluded.
11. Close with a context manifest so a later session can reconstruct the budget.

A personal cadence for reviewing routine events is not a platform limit. Do not create schedulers or background jobs unless the task authorizes them.

## Stop conditions

- The budget cannot cover the question; narrow or split the question.
- Skills conflict and the host's precedence rules must decide.
- An ablation cannot be measured; label the result as a hypothesis and report `NOT RUN` for the comparison.
- Loading more context would require unapproved data or credentials.

## Deliverables

- Context manifest: question, included sources, excluded sources, and reasons.
- Loaded skills with the trigger that selected each one.
- Scripts or filters that remove repeated mechanical work.
- A token or effort note with observed costs when available.
- Ablation result or a clearly labeled unmeasured hypothesis.

## Example

**Input:** A debugging session has loaded six skills, three long logs, and two architecture documents. The next decision is whether a retry loop causes duplicate writes.

**Expected output:** The manifest keeps the triage and verification skills, opens one reference on reproduction, excerpts the retry code and the failing log window, excludes unrelated UI docs, and scripts log filtering. The next experiment is one retry observation with a clear artifact. Unused skill sections are listed for a later ablation test.

**Stop case:** The only useful log is a multi-gigabyte export that cannot be filtered safely in the session. Stop with `NOT RUN` for the log analysis, propose a bounded extraction script, and do not paste the full export.

## Sources

- Local source map with dates and canonical URLs: [references/sources.md](references/sources.md)
- Deeper notes on budgeting and ablation: [references/field-guide.md](references/field-guide.md)
- Synthetic selection case: [references/smoke-case.md](references/smoke-case.md)
