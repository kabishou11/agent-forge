# Architectural constraints field guide

## Correction mining

Collect repeated corrections in a small table:

| Date | Correction | Context | Root shape | Could a structure prevent it? |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Look for the same mistake expressed in different places. If two examples do not share a shape, do not force a general rule.

## Intervention ladder

Prefer earlier, more deterministic interventions:

1. Data structure, type, schema, or API shape that makes the invalid state unrepresentable.
2. Lint, test, CI, codemod, or checker that fails automatically.
3. Skill or rule guidance that explains the preference.
4. Human review that catches what remains.

The ladder is a priority guide, not a claim that one layer replaces another. Required review and approvals remain required.

## Constraint proposal

```
Pattern:
Examples:
Failure signal:
Enforcement point:
Scope:
Migration:
Rollback:
Good sample:
Bad sample:
Owner and review:
```

A constraint is credible when a deliberately bad sample fails for the stated reason and a good sample still passes. Test both.

## Bounded repair

A quick local patch can spread a bad pattern. A root-cause repair may touch more files, but it must have a boundary. List included call sites, excluded call sites, and the reason for each exclusion. An unbounded rewrite is not a root-cause repair.

## Migration and rollback

For shared schemas or types, state who owns the migration, how old data is handled, and how to revert. If no safe rollback exists, stop and escalate rather than improvising.

## Failure modes

- Writing a prose rule and claiming the class of bugs is fixed.
- Adding a lint rule that cannot distinguish a valid exception.
- Broad migration without ownership or rollback.
- Quick patch that teaches the next author the wrong pattern.
- Treating a passing check as a substitute for required human approval.
