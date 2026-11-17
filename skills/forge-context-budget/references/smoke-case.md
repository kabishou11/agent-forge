# Synthetic selection case: forge-context-budget

Illustrative only; this is not a model-behavior test.

## Input

A synthetic session has six loaded skills, three long logs, and two architecture documents, while the next decision is whether a retry loop duplicates writes.

## Expected artifact schema

```json
{
  "status": "evidence-ready",
  "required_fields": ["status", "question", "skills_loaded", "included", "excluded", "ablation", "not_run"],
  "stop_status": "not-run"
}
```

## Expected status

`evidence-ready` when the context manifest is narrowed to the retry question and exclusions are recorded; `not-run` when the only useful log cannot be filtered safely.

## Stop case

The only useful log is a multi-gigabyte export that cannot be filtered in-session. Record `not-run` and propose a bounded extraction instead.
