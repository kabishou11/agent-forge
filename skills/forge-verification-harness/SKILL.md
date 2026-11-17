---
name: forge-verification-harness
description: Build reusable verification infrastructure and a user Feature Map before trusting an agent workflow. Use when a change needs end-to-end checking, a CLI or driver must be repeatable, environments need isolation, or verification claims depend on authentication, fixtures, ports, browser state, or user-visible flows.
---

# Forge verification harness

Create a working driver plus a user-facing map before declaring work ready. Verification is an executable capability, not a paragraph describing intent.

These instructions guide the assistant. They do not override host policies, approvals, sandbox rules, credential rules, or user authority.

## Inputs

- The user-visible features and the flows that must keep working.
- Supported surfaces: API, CLI, web UI, native app, or another driver target.
- Safe test credentials, seed data, fixture owners, and cleanup rules.
- Environment constraints: checkout, build, ports, browser profiles, and user state.
- The current manual checks, scripts, and known gaps.

## Workflow

1. List the meaningful subsystem and the user flows it serves; keep the map small enough to maintain.
2. Build or reuse a CLI or driver that performs the flow without manual clicking.
3. Make commands discoverable with `--help`, stable JSON output, and actionable errors.
4. Add a dry run for dangerous or destructive actions before enabling execution.
5. Seed data and isolate checkout, build output, ports, browser profile, and user state.
6. Record the authentication path without logging secrets; use approved test accounts only.
7. Run one full end-to-end flow before calling the harness ready.
8. Save before and after artifacts for the exact scenario being verified.
9. Maintain the Feature Map as flows, states, roles, themes, and outside-diff consumers change.
10. Replace repeated mechanical steps with scripts rather than re-running an agent by hand.
11. State clearly that a passing harness proves only the checks it ran, not general correctness.

Use one meaningful subsystem per verification model or skill where the map permits. Do not claim support for a surface that has no runnable driver.

## Stop conditions

- A destructive action lacks a dry run or approval.
- Test credentials, data, or an isolated environment are unavailable.
- The harness cannot observe the user-visible result it claims to check.
- Isolation is impossible and the run would touch shared or production state. Stop with `NOT RUN`.

## Deliverables

- Driver commands, including help and JSON modes.
- A current Feature Map with flows, roles, states, consumers, and known gaps.
- Seed and cleanup instructions and isolation notes.
- A run log with before and after artifacts for one complete flow.
- An explicit list of what the harness does not verify.

## Example

**Input:** A report export feature has a download button, a background job, and two role-based views. There is no automated end-to-end check.

**Expected output:** A CLI driver that seeds an approved account, starts an isolated job, waits for completion, downloads the artifact, and prints JSON with row counts and a checksum. The Feature Map lists both roles and the empty, running, failed, and complete states. One full run is recorded with before and after artifacts.

**Stop case:** The only available account is a shared production administrator. Stop with `NOT RUN`, document the missing isolated account, and do not log in or trigger the export.

## Sources

- Local source map with dates and canonical URLs: [references/sources.md](references/sources.md)
- Deeper notes on drivers and Feature Maps: [references/field-guide.md](references/field-guide.md)
- Synthetic selection case: [references/smoke-case.md](references/smoke-case.md)
