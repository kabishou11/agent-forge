---
name: forge-disposable-prototypes
description: Use a disposable research prototype to answer one open design question. Use when alternatives need comparison, an approach is uncertain, a measurement is missing, or a storyboard or spike would reduce implementation risk without becoming production code.
---

# Forge disposable prototypes

Answer one question with the least code that produces evidence. Treat the prototype as research material: label it, keep it isolated, measure it, and discard it unless a separate decision promotes the idea.

These instructions guide the assistant. They do not override host policies, approvals, sandbox rules, or user authority.

## Inputs

- One open question and the decision it will inform.
- Candidate approaches, with the assumptions that distinguish them.
- Synthetic or approved fixtures, and a measurement method.
- A timebox and a safe place to work outside the production path.
- Constraints that cannot be violated, such as privacy or platform limits.

## Workflow

1. State the question and the decision criteria before writing code.
2. Reject questions that cannot produce an observable result; sharpen them first.
3. Choose the smallest scaffold that exercises the contested behavior.
4. Keep the prototype isolated from production entry points and committed interfaces.
5. Use the same fixture and measurement for every alternative.
6. Record commands, inputs, versions, and raw results next to the question.
7. Compare alternatives in a compact table; include a "no change" baseline when useful.
8. Note where the prototype diverges from real constraints and what that invalidates.
9. Recommend one path, or recommend stopping when evidence is inconclusive.
10. Discard the prototype by default. If the team promotes it, rewrite it with tests and production conventions.

When adapting a storyboard or animation technique to code, label the adaptation as our own and do not present it as the original author's implementation.

## Stop conditions

- The question is too broad to measure in one prototype.
- The prototype needs production data, credentials, or access that is not authorized.
- Results are inconclusive within the timebox. Report the limitation as `NOT RUN` for the unresolved part.
- The prototype would become an unreviewed production dependency.

## Deliverables

- The question, decision criteria, and timebox.
- Prototype location or a note that no durable artifact was kept.
- Commands, fixtures, measurements, and a comparison table.
- A recommendation with confidence and caveats.
- A discard or promotion decision, including the tests required for promotion.

## Example

**Input:** "Should the importer stream rows or load the file before validation?" There is a synthetic 10,000-row fixture and a memory limit.

**Expected output:** Two throwaway scripts, run with identical fixtures, producing peak memory, elapsed time, and validation failure counts. The table shows streaming uses less memory but complicates partial-error reporting; the recommendation names the tradeoff and keeps the prototype out of the production package.

**Stop case:** The only realistic fixture is private customer data and no synthetic substitute is approved. Stop with `NOT RUN`, document the missing evidence, and do not copy private data into the repository.

## Sources

- Local source map with dates and canonical URLs: [references/sources.md](references/sources.md)
- Deeper notes on prototype discipline: [references/field-guide.md](references/field-guide.md)
- Synthetic selection case: [references/smoke-case.md](references/smoke-case.md)
