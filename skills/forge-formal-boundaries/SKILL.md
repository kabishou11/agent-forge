---
name: forge-formal-boundaries
description: Use formal methods as bounded evidence, not a bug-free guarantee. Use when a protocol, state machine, or concurrency design needs a model, a counterexample needs interpretation, a proof claim is made, or intent, specification, model, and implementation may drift apart.
---

# Forge formal verification boundaries

Separate human intent, the written specification, the formal model, and the running implementation. Model one meaningful subsystem, state the assumptions and bounds, and connect any counterexample back to runtime evidence.

These instructions guide the assistant. They do not override host policies, approvals, sandbox rules, tool availability, or user authority.

## Inputs

- The human intent and the user-visible flow being modeled.
- The written specification, including invariants and allowed states.
- The model, tool configuration, and the exact bounds to be checked.
- The runtime implementation and a reproduction harness when available.
- Known assumptions, environment limits, and ownership of the model.

## Workflow

1. Write the human intent and the proposed property in separate statements.
2. Define the model boundary: one meaningful subsystem, its inputs, outputs, and environment assumptions.
3. State every invariant, liveness property, and bound before running a checker.
4. Build or inspect the model; record where it abstracts away implementation detail.
5. Visualize the user flow or statechart as a review aid, not as proof by image.
6. Run the model checker within its stated bounds and save the configuration and output.
7. Interpret a counterexample as a question: is the model wrong, the property wrong, or the implementation exposed?
8. Reproduce the counterexample against real runtime behavior when the environment allows.
9. Record drift risk between intent, spec, model, and code, and who reviews each.
10. State confidence narrowly: checked properties within bounds, not general correctness.
11. Revisit the model when the subsystem or assumptions change.

Do not claim that a proof, a bounded check, or a diagram proves the absence of all bugs. A formal result is evidence under assumptions.

## Stop conditions

- The specification or model drifts from intent and no owner can resolve it.
- A property lies outside the configured bounds.
- The checker or runtime environment is unavailable. Report `NOT RUN` for the unexecuted part.
- A counterexample cannot be reproduced and the difference is not explained.
- The change requires approval or a policy exception.

## Deliverables

- Intent, specification, property, and model boundary statements.
- Assumptions, abstractions, and exact checking bounds.
- Checker configuration, command, and raw result.
- Counterexample interpretation with a runtime artifact when available.
- A bounded confidence statement and residual drift risk.

## Example

**Input:** A lock protocol has a written invariant that two owners cannot hold the same lease, and a bounded model is proposed.

**Expected output:** The model covers one lease subsystem, names assumptions about clock skew and message loss, lists the mutual-exclusion property, states the checked depth, and saves the checker output. A counterexample is interpreted against a runtime harness with an injected delay, and the final claim is limited to the checked bounds.

**Stop case:** The model assumes a clock behavior the runtime cannot provide, and no owner can confirm the assumption. Stop with `NOT RUN` for the unbounded claim, document the drift, and do not present the model as proof of production safety.

## Sources

- Local source map with dates and canonical URLs: [references/sources.md](references/sources.md)
- Deeper notes on model boundaries and counterexamples: [references/field-guide.md](references/field-guide.md)
- Synthetic selection case: [references/smoke-case.md](references/smoke-case.md)
