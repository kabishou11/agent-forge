# Synthetic selection case: forge-architectural-constraints

Illustrative only; this is not a model-behavior test.

## Input

A synthetic review log shows the same missing null check corrected in three handlers for one optional field.

## Expected artifact schema

```json
{
  "status": "evidence-ready",
  "required_fields": ["status", "pattern", "enforcement_point", "bad_sample", "good_sample", "migration", "rollback", "review_required"],
  "stop_status": "stopped"
}
```

## Expected status

`evidence-ready` when a structural constraint and its failing sample are proposed; `stopped` when the change belongs to another owner.

## Stop case

The field is owned by another service and requires an approved cross-team migration. Stop at the proposal without patching one handler.
