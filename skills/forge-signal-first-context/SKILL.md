---
name: forge-signal-first-context
description: Gather high-signal repository context before editing code. Use when starting an unfamiliar task, reading a large codebase, chasing a failure, or when an agent is tempted to read every file instead of targeting entry points, interfaces, tests, logs, and recent changes.
---

# Forge signal-first context

Build a small context packet from the artifacts most likely to change the next action. Read narrowly, record provenance, and avoid copying stale or deprecated patterns into new work.

These instructions guide the assistant. They do not override host policies, approvals, sandbox rules, or user authority.

## Inputs

- The task statement and the exact question the next edit must answer.
- Repository entry points, public interfaces, schemas, and configuration files.
- Failing tests, logs, stack traces, screenshots, and a recent change history if available.
- User reports and product expectations that define intended behavior.
- A time or token budget for exploration.

## Workflow

1. Write the first question as a sentence, for example: "Which component decides export format?"
2. Start with the smallest high-signal set: the entry point, the interface it calls, the nearest test, and relevant config.
3. Follow references only when they answer the question; stop when the call path is explained.
4. Prefer current code and executable checks over prose docs that may have drifted.
5. Sample large directories rather than reading every file; note what was sampled.
6. Record each fact with its file path, symbol, and date or revision when available.
7. Separate facts, inferences, and open questions in the context packet.
8. Check for deprecated or forbidden patterns before reusing an example from the repository.
9. If the question survives static reading, design the smallest runtime observation.
10. Hand the packet to the implementation loop; keep the outer loop focused on new external context.

Do not turn exploration into a rewrite. If a file is not connected to the question, leave it out and say so.

## Stop conditions

- The context is too thin to support a safe hypothesis.
- Sources contradict each other and the newer source is unclear.
- The next observation needs network access, credentials, production data, or approval.
- The budget is exhausted. Summarize what is known and report the unexecuted step as `NOT RUN`.

## Deliverables

- A one-paragraph problem framing with the current question.
- A context packet listing facts, file references, and provenance.
- Candidate files to change and files deliberately excluded.
- Unknowns, conflicting evidence, and the next smallest experiment.
- A statement of what was not executed.

## Example

**Input:** "Checkout returns the wrong tax total for one region." The repository has thousands of files and an outdated architecture note.

**Expected output:** A packet naming the checkout entry point, tax provider adapter, relevant config, the closest failing test, and the region-specific branch. It records one inference and two unknowns, excludes unrelated UI files, and proposes one runtime request with a synthetic order.

**Stop case:** The tax provider requires a live credential that is not available. Stop before editing with `NOT RUN`, document the exact blocked observation, and leave the repository unchanged.

## Sources

- Local source map with dates and canonical URLs: [references/sources.md](references/sources.md)
- Deeper notes on context packets and sampling: [references/field-guide.md](references/field-guide.md)
- Synthetic selection case: [references/smoke-case.md](references/smoke-case.md)
