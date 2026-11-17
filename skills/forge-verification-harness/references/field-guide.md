# Verification harness field guide

## Harness contract

A useful harness has a small, documented contract:

- `--help` explains the available flows and required inputs.
- `--json` returns machine-readable results with a stable schema.
- Errors identify the failed step and a next action.
- Dangerous actions support `--dry-run`.
- Every run creates an artifact directory for logs, screenshots, downloads, and summaries.
- Exit codes distinguish pass, verified failure, and infrastructure failure.

## Isolation checklist

- Fresh or disposable checkout and build directory.
- Per-run ports, databases, and temporary storage.
- Isolated browser profile or user state.
- Approved test account or token; never log the secret.
- Cleanup that runs even after a failure.
- No shared production state by default.

## Feature Map

Map behavior users depend on, not just internal modules:

| Flow | Role or state | Entry point | Expected artifact | Known gap |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Include empty, loading, error, and partial states. For broad changes, list outside-diff consumers such as themes, roles, localization, and alternate entry points. Keep one meaningful subsystem per map when possible.

## Run log

Record the command, environment, input fixture, start time, result, and artifact path. For a before/after comparison, store both artifacts and the exact scenario identifier. A screenshot alone is weak evidence unless the assertion and the state are stated.

## Surfaces

API, CLI, web, and native surfaces can share the same principles, but each needs a driver that actually observes the surface. Do not claim a surface is verified because a lower-level unit test passes.

## Budget and automation

Put repeated setup, seeding, and cleanup into scripts. Filter noisy routine events before they enter the main loop. Keep a manual fallback documented for infrastructure failures.

## Failure modes

- A driver that clicks through a happy path but cannot assert the result.
- Shared accounts or databases that make runs order-dependent.
- Logging credentials or user data into artifacts.
- A Feature Map that lists modules but not user flows.
- Declaring readiness before one full end-to-end run.
- Treating a passing harness as proof of correctness beyond its checks.
