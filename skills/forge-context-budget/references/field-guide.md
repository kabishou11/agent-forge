# Context and token budget field guide

## Budget by question

Write the current question at the top of the session notes. For each candidate source, ask whether it could change the next action. If not, exclude it and record why. Keeping a short exclusion list is often more valuable than a long inclusion list.

## Skill selection

Use the skill description as the trigger. A skill should be loaded because the task matches its when-to-use clause, not because it is related to the general topic. When several skills overlap:

1. Choose the one closest to the current decision.
2. Note the conflicting guidance.
3. Follow the host's precedence and approval rules.
4. Drop one after the decision moves on.

## Context manifest

```
Question:
Skills loaded (trigger):
Sources included (path, reason):
Sources excluded (reason):
Estimated cost or observed cost:
Next decision:
```

An estimate is not a measurement. Label it.

## Routine events

Repeated mechanical events can flood the main loop. Filter or summarize them before inclusion, and move repeated actions into scripts. A personal review cadence, such as checking a queue hourly, is a habit, not a platform-imposed limit. Do not create schedulers or background jobs without explicit authorization.

## Ablation

When changing instructions or skill sections, test one change at a time:

| Variant | Section changed | Observed effect | Confidence |
| --- | --- | --- | --- |
| Baseline |  |  |  |
| A |  |  |  |
| B |  |  |  |

Models change, so a section that helped yesterday may be noise today. Remove stale guidance when evidence shows it is not helping. If you cannot measure, record a hypothesis and do not claim an improvement.

## Failure modes

- Loading every skill because the task is broad.
- Pasting whole files or logs instead of targeted excerpts.
- Counting tokens without checking whether the content changed a decision.
- Keeping stale sections forever.
- Treating a cadence recommendation as a hard platform rule.
- Reporting an unrun ablation as a success.
