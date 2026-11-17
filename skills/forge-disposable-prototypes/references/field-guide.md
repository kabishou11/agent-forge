# Disposable prototype field guide

## When a prototype is worth it

Use one when a decision depends on behavior that is cheaper to observe than to argue about: relative performance, API ergonomics, parser complexity, migration shape, or an interaction that a document cannot settle. Do not use one to avoid reading a stable interface or to build a shadow implementation.

## Prototype brief

```
Question:
Decision it informs:
Alternatives:
Shared fixture:
Measurement:
Timebox:
Disposal plan:
```

The brief fits in a short paragraph. If the alternatives do not share a measurement, the comparison is not useful.

## Isolation rules

- Put throwaway code outside production entry points and published interfaces.
- Use a separate branch, scratch directory, or clearly named research file.
- Do not wire the prototype into CI, releases, or on-call paths.
- Keep secrets and private data out; prefer synthetic fixtures.
- Record the exact version, flags, and hardware or environment when performance matters.

## Comparison table

| Alternative | Correctness result | Cost signal | Complexity | Notes |
| --- | --- | --- | --- | --- |
| A |  |  |  |  |
| B |  |  |  |  |
| No change |  |  |  |  |

A result without a check for correctness is only a speed or convenience observation. Say so.

## Promotion

Promotion is a separate decision. A promoted prototype must be rewritten to production conventions and covered by tests. Do not promote by renaming a research file. Record what the prototype did not test.

## Labeling adaptations

A storyboard, animatic, or visualization from another field can inspire a code prototype. State that the adaptation and implementation are ours, and do not attribute the implementation to the source author. A visual aid is not proof that the code behaves correctly.

## Failure modes

- A prototype that becomes a dependency without review.
- Comparing implementations with different fixtures.
- Measuring only the happy path.
- Keeping the prototype because effort was already spent.
- Reporting an inconclusive result as a recommendation.
