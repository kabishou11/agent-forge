# Synthetic selection case: forge-triage-repro-fix

Illustrative only; this is not a model-behavior test.

## Input

A synthetic report says a draft loses its second tag and guesses that a cache is responsible.

## Expected artifact schema

```json
{
  "status": "evidence-ready",
  "required_fields": ["status", "triage_verdict", "reproduction", "failing_test", "mechanism", "verification", "residual_risk"],
  "stop_status": "stopped"
}
```

## Expected status

`evidence-ready` when the exact two-tag flow is reproduced and verified; `stopped` when triage finds a non-bug or the fix is too risky to bound.

## Stop case

Triage concludes the behavior is intentional for that role. Stop with a `stopped` verdict and make no speculative parser change.
