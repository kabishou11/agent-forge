# Synthetic selection case: forge-formal-boundaries

Illustrative only; this is not a model-behavior test.

## Input

A synthetic lease protocol has a written mutual-exclusion invariant and a bounded model, but no runtime reproduction of the proposed counterexample.

## Expected artifact schema

```json
{
  "status": "evidence-ready",
  "required_fields": ["status", "intent", "specification", "model_scope", "assumptions", "bounds", "checker_result", "runtime_link", "residual_risk"],
  "stop_status": "not-run"
}
```

## Expected status

`evidence-ready` when the claim is limited to the checked model and bounds; `not-run` when the runtime link or model assumption cannot be verified.

## Stop case

The model assumes clock behavior the runtime cannot provide and no owner can confirm it. Record `not-run` for the broader claim and do not present the model as proof of production safety.
