# Synthetic selection case: forge-depth-first-parallelism

Illustrative only; this is not a model-behavior test.

## Input

A synthetic flaky test has three plausible causes: timing, shared fixture state, or an order-dependent cache. Three isolated workspaces are available.

## Expected artifact schema

```json
{
  "status": "evidence-ready",
  "required_fields": ["status", "question", "hypotheses", "attempts", "eliminations", "winner", "unresolved"],
  "stop_status": "not-run"
}
```

## Expected status

`evidence-ready` when one hypothesis survives a clean re-test and the others have recorded stop reasons; `not-run` when isolation is impossible.

## Stop case

All attempts would share one mutable database. Stop before running, record the isolation gap, and do not compare contaminated results.
