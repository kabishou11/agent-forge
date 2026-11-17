# Formal verification boundaries field guide

## Four artifacts

Keep these separate:

| Artifact | Question | Owner |
| --- | --- | --- |
| Human intent | What do people actually need? | Product or requester |
| Specification | What properties are required? | Design or domain owner |
| Model | What did we encode for the checker? | Model author |
| Implementation | What runs in production? | Engineering owner |

A gap between any two is a source of false confidence. Write the gap down.

## Property statement

For each property, state:

- The invariant or liveness condition.
- The assumptions: environment, scheduling, message delivery, clock, data.
- The bound: depth, steps, state count, or scope.
- The abstraction: what the model deliberately omits.
- The runtime observation that would support or refute a counterexample.

A bounded check proves only that no violation was found within the model and bounds. It does not prove the implementation matches the model.

## One meaningful subsystem

Choose a subsystem with a clear boundary and a user-visible flow. A model that tries to include everything becomes hard to review and easy to drift. Visualize the flow or statechart to align reviewers, but do not treat the image as evidence.

## Counterexample interpretation

Ask in order:

1. Is the property itself wrong or underspecified?
2. Is the model wrong or missing an assumption?
3. Is the implementation genuinely exposed?
4. Can the runtime reproduce the behavior?

If the counterexample cannot be connected to runtime evidence, report the limit. Pair formal and empirical checks when possible.

## Drift

Models age. Record the commit or design version modeled, the date checked, and the trigger for rechecking, such as a protocol, configuration, or dependency change.

## Failure modes

- Claiming a proof guarantees no bugs.
- Reporting a checker result without bounds.
- Using a diagram as proof.
- Hiding assumptions in the tool configuration only.
- Ignoring a counterexample because the runtime test is inconvenient.
- Treating a formal skill as a replacement for required review.
