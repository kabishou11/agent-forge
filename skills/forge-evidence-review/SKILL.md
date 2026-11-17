---
name: forge-evidence-review
description: Review a change by executing hypotheses and counterexamples rather than generating speculative nitpicks. Use when a diff, fix, design, or formal claim needs independent review, when a reviewer is tempted to summon a broad adversarial swarm, or when regression and outside-diff behavior matter.
---

# Forge evidence-first review

Make review empirical. Restate the intended outcome, run the checks that can falsify the change, and keep preferences separate from defects.

These instructions guide the assistant. They do not override host policies, approvals, sandbox rules, review requirements, or user authority.

## Inputs

- The change under review and the intent or acceptance checks it claims to satisfy.
- Reproduction steps, a harness, fixtures, and any before/after artifacts.
- Relevant callers, consumers, themes, states, and compatibility constraints.
- The specific decision the review must support.
- Any formal model, spec, or proof claim and its stated bounds.

## Workflow

1. Restate the intended behavior and the review question in one or two sentences.
2. Read the diff with the intent in hand; identify the highest-risk claim first.
3. Run the existing focused tests and the exact reproduction when available.
4. For each real concern, build a concrete counterexample and execute it.
5. Stop pursuing a hypothesis once evidence eliminates it; record the result.
6. Avoid broad speculative-review swarms and nitpicks that cannot change the decision.
7. Check outside-diff consumers when a shared type, style, theme, state, or interface changed.
8. Separate blocking defects, non-blocking improvements, and personal preferences.
9. Cite file and line locations and the artifact or command that supports each finding.
10. Treat a formal result as bounded evidence; pair counterexamples with runtime reproduction where possible.
11. State what was not run and what remains unknown.

An independent review that only reads prose and lists hypothetical risks is not equivalent to executing a counterexample.

## Stop conditions

- No runnable evidence is available for the highest-risk claim.
- Verification needs credentials, data, or an environment that is not authorized.
- The review would only produce style preferences with no decision impact.
- A formal claim exceeds its stated assumptions or bounds and cannot be tested at runtime. Report `NOT RUN` for the unverified part.

## Deliverables

- Review verdict and the intent being checked.
- Executed commands, tests, and counterexamples with results.
- Blocking findings with file references and evidence.
- Non-blocking suggestions and explicit preferences.
- Untested areas, residual risk, and any formal-claim limits.

## Example

**Input:** A parser fix passes its new test. The reviewer suspects a regression in the legacy import path but has no proof.

**Expected output:** The reviewer runs the exact failing report, the new test, and a legacy fixture. The legacy fixture fails, producing a concrete counterexample tied to a specific branch and file line. The verdict blocks the merge on that evidence; a separate formatting preference is labeled non-blocking.

**Stop case:** The legacy fixture requires a private data set that is not approved. Stop with `NOT RUN` for that check, report the remaining confidence honestly, and do not claim the regression is absent.

## Sources

- Local source map with dates and canonical URLs: [references/sources.md](references/sources.md)
- Deeper notes on counterexamples and review scope: [references/field-guide.md](references/field-guide.md)
- Synthetic selection case: [references/smoke-case.md](references/smoke-case.md)
