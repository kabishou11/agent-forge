---
name: forge-architectural-constraints
description: Turn repeated corrections into deterministic architectural constraints. Use when the same mistake recurs, a quick patch would spread a bad pattern, prose guidance is ignored, or a data structure, schema, lint rule, codemod, or CI check could prevent a class of defects.
---

# Forge architectural constraints

Prefer structural prevention over reminders. Mine repeated corrections, find the shape that makes the mistake hard to express, and add the narrowest mechanical check that fails when the problem returns.

These instructions guide the assistant. They do not override required reviews, approvals, host policies, sandbox rules, or user authority.

## Inputs

- A correction log, review comments, or repeated bug pattern with concrete examples.
- Current data models, interfaces, schemas, and ownership boundaries.
- Existing tests, lint rules, type checks, codemods, and CI gates.
- Compatibility requirements and migration constraints.
- The approval process for shared or cross-team changes.

## Workflow

1. Describe the recurring mistake with at least two real examples and the cost of each.
2. Rank interventions in this order: model or data-structure change, then lint/test/CI, then skill or rule guidance, then human review.
3. Prototype the structural fix against realistic, approved data before proposing it broadly.
4. Choose an enforcement point that is deterministic: a type, constraint, schema, codemod, or failing test.
5. Define the failure signal and the migration path, including rollback.
6. Keep required review and approvals; a machine check supplements them, it does not remove them.
7. Reject unbounded rewrites. If a minimal fix would propagate the pattern, propose a bounded root-cause repair with explicit scope.
8. Record the decision, alternatives, and residual risk in a decision log.
9. Verify the constraint catches a deliberately bad sample and still accepts the good path.
10. Retire or narrow the constraint when it produces noise that trains people to bypass it.

Do not claim that prose alone enforces behavior. Say which check fails and what remains a human judgement.

## Stop conditions

- The change needs a shared schema migration or another team's approval.
- No safe rollback exists.
- The prototype requires unapproved production data.
- The constraint cannot be verified without a network or environment that is unavailable. Report `NOT RUN` for that verification.

## Deliverables

- A pattern statement with examples and observed cost.
- The proposed structural constraint and its enforcement point.
- A bad sample that must fail and a good sample that must pass.
- Migration, rollback, ownership, and review notes.
- A decision log with rejected alternatives and residual risk.

## Example

**Input:** Three reviewers corrected a missing null check on the same optional field in different handlers. Past reminders did not stop it.

**Expected output:** A proposal that makes the field non-null at the boundary, plus a migration that supplies a default and a test proving the old bad sample no longer compiles or fails validation. Review requirements stay in place, and a bounded list of handlers is migrated.

**Stop case:** The field is owned by another service and changing it needs an approved cross-team migration. Stop at the proposal with `NOT RUN` for implementation, and do not patch one handler while claiming the class of bugs is fixed.

## Sources

- Local source map with dates and canonical URLs: [references/sources.md](references/sources.md)
- Deeper notes on prevention and migration: [references/field-guide.md](references/field-guide.md)
- Synthetic selection case: [references/smoke-case.md](references/smoke-case.md)
