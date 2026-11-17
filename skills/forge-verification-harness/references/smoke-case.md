# Synthetic selection case: forge-verification-harness

Illustrative only; this is not a model-behavior test.

## Input

A synthetic export feature has two roles, a background job, and a download artifact, but no end-to-end driver.

## Expected artifact schema

```json
{
  "status": "evidence-ready",
  "required_fields": ["status", "driver_commands", "feature_map", "artifact_paths", "isolation", "not_run"],
  "stop_status": "not-run"
}
```

## Expected status

`evidence-ready` after one isolated end-to-end run with before and after artifacts; `not-run` when only a shared production account is available.

## Stop case

The only account is a shared production administrator. Stop with `not-run` and do not trigger the export.
