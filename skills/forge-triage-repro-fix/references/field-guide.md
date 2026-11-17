# Triage, reproduction, and repair field guide

## Stage gates

Each stage has an entry check and an exit artifact:

| Stage | Entry | Exit artifact |
| --- | --- | --- |
| Triage | Report and context | Verdict: defect, non-bug, duplicate, or unknown |
| Reproduction | Verdict worth testing | Exact steps, inputs, environment, and artifact |
| Failing test | Stable reproduction | Test that fails for the reported reason |
| Mechanism | Failing test | How, why, and relevant history |
| Repair | Mechanism | Smallest bounded change |
| Verification | Repair | Before/after evidence from the same scenario |

A failure at any gate is a result, not a reason to improvise a different task.

## Restating the report

Quote the report, then write an observable restatement. Keep the reporter's hypothesis in a separate line labeled "reporter's theory". Do not let that theory choose the reproduction path until evidence supports it.

## Reproduction record

```
Report:
Environment:
Steps:
Inputs or fixture:
Observed:
Expected:
Artifact paths:
Attempts that did not reproduce:
```

Repeat the exact scenario before and after the fix. If a flaky failure resists repetition, use the depth-first strategy to isolate the condition rather than averaging away the signal.

## Mechanism note

Answer three questions:

- How does the behavior occur in the current code?
- Why does the code have this shape? Include relevant history or constraints.
- What related code or consumers could share the same mechanism?

This note prevents a symptom-level patch and guides the scope of verification.

## Bounded repair

Choose the smallest change that addresses the mechanism. If the minimal change would spread a bad pattern, propose a bounded root-cause repair: list the included call sites, excluded call sites, migration needs, and rollback. A risky fix can stop as "not attempted" with evidence.

## Broad changes

For large migrations, check visual and behavioral consumers outside the immediate diff: themes, states, roles, alternate entry points, and data shapes. A passing visual check does not prove hidden dependencies are gone.

## Failure modes

- Fixing a nearby bug because the reported one is hard to reproduce.
- Writing a test that passes before the fix.
- Treating a failed reproduction as proof the report is false.
- Calling a stopped repair a failure.
- Reporting verification that did not run. Use `NOT RUN`.
