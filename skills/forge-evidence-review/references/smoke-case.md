# Synthetic selection case: forge-evidence-review

Illustrative only; this is not a model-behavior test.

## Input

A synthetic parser fix passes its new test, and the reviewer suspects a legacy import regression without evidence.

## Expected artifact schema

```json
{
  "status": "evidence-ready",
  "required_fields": ["status", "verdict", "executed_checks", "counterexamples", "blocking_findings", "untested", "not_run"],
  "stop_status": "not-run"
}
```

## Expected status

`evidence-ready` when the suspected regression is executed as a concrete counterexample; `not-run` when the required fixture is unavailable.

## Stop case

The legacy fixture needs an unapproved private data set. Record `not-run`, report the remaining confidence honestly, and do not claim the regression is absent.
