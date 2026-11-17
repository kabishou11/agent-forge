# Synthetic selection case: forge-disposable-prototypes

Illustrative only; this is not a model-behavior test.

## Input

A synthetic importer design must choose between streaming and preloading, using a generated 10,000-row fixture.

## Expected artifact schema

```json
{
  "status": "evidence-ready",
  "required_fields": ["status", "question", "alternatives", "measurements", "recommendation", "disposal", "not_run"],
  "stop_status": "not-run"
}
```

## Expected status

`evidence-ready` when both alternatives use the same fixture and measurement; `not-run` when only private data would make the comparison realistic.

## Stop case

The only realistic fixture is private customer data and no synthetic substitute is approved. Record `not-run` and do not copy the data.
