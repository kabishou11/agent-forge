# Synthetic selection case: forge-intent-alignment

Illustrative only; this is not a model-behavior test.

## Input

A synthetic request says: "Make the nightly export faster before Friday." It supplies no baseline, target, or list of callers.

## Expected artifact schema

```json
{
  "status": "evidence-ready",
  "required_fields": ["status", "goal", "non_goals", "assumptions", "acceptance_checks", "not_run"],
  "stop_status": "not-run"
}
```

## Expected status

`evidence-ready` after the goal, scope, and acceptance checks are stated; `not-run` when no stable baseline or requester confirmation exists.

## Stop case

The requester is unavailable and no safe default exists. Produce a `not-run` artifact and make no code change.
