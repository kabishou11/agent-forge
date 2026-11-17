---
name: forge-intent-alignment
description: Align a coding request with the user's real intent before writing code. Use when a request is vague, mixes symptoms with causes, uses unfamiliar vocabulary, changes scope mid-thread, or needs a restatement, storyboard, and acceptance checks before implementation.
---

# Forge intent alignment

Turn the request into a small, checkable target before choosing an implementation. Keep the user's words, separate observation from theory, and make assumptions visible.

These instructions guide the assistant. They do not override host policies, approvals, sandbox rules, or user authority.

## Inputs

- The original request, report, or ticket, quoted without cleanup.
- Known constraints: compatibility, deadlines, ownership, environments, and non-goals.
- Any observed behavior, logs, screenshots, or reproduction steps already supplied.
- The vocabulary used by the requester and by the codebase.
- Existing acceptance tests, feature maps, or product expectations.

## Workflow

1. Capture the request verbatim in a short intent brief.
2. Separate observations from speculative root causes. Do not repeat a guessed cause as fact.
3. Restate the goal, non-goals, affected users, and success signal in plain language.
4. List ambiguous terms and offer a concrete interpretation for each.
5. Ask one blocking question at a time when the answer changes the work; otherwise record the assumption.
6. Storyboard the user-visible flow before production code when the vocabulary gap is large.
7. Convert the restated goal into a few acceptance checks that can fail.
8. Flag any request that requires new permissions, credentials, or approvals, and wait for the host process.
9. Start implementation only after the restatement is accepted or every assumption is explicit.
10. Keep a decision log for scope changes so later work can be reviewed against the same intent.

Prefer one short, high-signal restatement over a long plan. Stop early when the request is a question, not a build task.

## Stop conditions

- The request conflicts with itself or with a known constraint.
- The next step needs approval, credentials, production access, or a policy exception.
- The requester cannot confirm the goal and no safe default exists.
- The task asks for a speculative root cause instead of an observable outcome.
- A required source or environment is unavailable. Report `NOT RUN`; do not invent evidence.

## Deliverables

- Intent brief: goal, non-goals, users, constraints, and assumptions.
- Vocabulary notes and resolved or open interpretations.
- Acceptance checks with observable pass and fail signals.
- Decision log entries for scope or interpretation changes.
- A clear statement of anything not run.

## Example

**Input:** "The nightly export is too slow; make it faster before Friday." The report contains no duration, no target, and no baseline; the export has two callers.

**Expected output:** A restatement naming the export flow, its two callers, the measured baseline, a proposed target, a non-goal such as not changing the output format, and three acceptance checks: the same rows are produced, a repeatable benchmark improves, and both callers still pass. Assumptions that need confirmation are marked.

**Stop case:** No stable benchmark data exists and the requester is unavailable. Stop with `NOT RUN`, propose the smallest measurement harness, and do not claim speed changed.

## Sources

- Local source map with dates and canonical URLs: [references/sources.md](references/sources.md)
- Deeper notes on restatement and storyboards: [references/field-guide.md](references/field-guide.md)
- Synthetic selection case: [references/smoke-case.md](references/smoke-case.md)
