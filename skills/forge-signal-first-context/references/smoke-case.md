# Synthetic selection case: forge-signal-first-context

Illustrative only; this is not a model-behavior test.

## Input

A synthetic defect report says a regional tax total is wrong in a large repository with no known entry point.

## Expected artifact schema

```json
{
  "status": "evidence-ready",
  "required_fields": ["status", "question", "facts", "exclusions", "unknowns", "next_observation", "not_run"],
  "stop_status": "not-run"
}
```

## Expected status

`evidence-ready` when the context packet names entry points, interfaces, tests, and unknowns; `not-run` when the next observation needs unavailable credentials.

## Stop case

The tax provider needs an unapproved live credential. Stop before editing and record the blocked observation.
