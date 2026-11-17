# Evidence-first review field guide

## Review brief

```
Intent:
Change:
Highest-risk claim:
Evidence available:
Checks to run:
Out of scope:
Decision needed:
```

The brief keeps review tied to a decision. If no decision changes, a finding is probably a preference or noise.

## Counterexample discipline

For each concern, write:

1. The assumption being challenged.
2. A concrete input, sequence, or consumer that would break it.
3. The command or inspection that executes the challenge.
4. The observed result.

A concern that cannot be executed can still be recorded, but label it as untested. Do not present a hypothetical as a demonstrated defect.

## Speculative review swarms

Broad adversarial review can produce many plausible-sounding issues without evidence and spend tokens on low-value nitpicks. Prefer a small number of executable questions. The later position in the source material favors empirical and formal verification over summoning a speculative swarm; do not use the earlier enthusiasm as the current default.

## Formal claims

When a change cites a model, proof, or checker:

- Identify the property and its assumptions.
- Identify the checked bounds.
- Ask whether the counterexample, if any, reproduces at runtime.
- Refuse to convert "no counterexample within bounds" into "no bugs".

## Outside-diff consumers

Check shared types, style systems, themes, feature flags, roles, localization, and alternate entry points when the diff changes a shared contract. A large migration can pass local visual checks and still leave hidden consumers.

## Finding format

```
Severity: blocking | non-blocking | preference
Location: path:line
Claim:
Counterexample or command:
Observed result:
Impact:
Suggested next step:
```

## Failure modes

- Listing style preferences as defects.
- Reporting a formal result without bounds.
- Treating a passing test as evidence for a different claim.
- Generating hypothetical risks instead of running a check.
- Omitting what was not run.
