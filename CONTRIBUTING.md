# Contributing

Contributions are welcome when they keep the toolkit focused, original, and testable.

## Before changing a skill

1. Check whether the change belongs in a main skill or in an on-demand reference. Keep the main file short and imperative.
2. Use a `forge-` prefix and a lowercase kebab-case directory name that exactly matches the YAML `name`.
3. Keep the description trigger-oriented. Say when to invoke the skill, not only what it covers.
4. Preserve the section order: Inputs, Workflow, Stop conditions, Deliverables, Example, Sources.
5. Keep the example concrete and include an input, a checkable expected output, and a stop case.
6. Keep every relative link inside the skill directory. A copied skill must remain self-contained.
7. Keep the skill's `LICENSE`, `NOTICES.md`, and `references/smoke-case.md` in sync with the workflow. The smoke case is a structural fixture, not a model-behavior test.
8. Use the restricted frontmatter profile: simple string scalars only. Do not add mappings, typed YAML values, tags, anchors, aliases, or sequences.
9. Do not claim that markdown guarantees behavior, overrides host policy, or expands permissions.

## Sources

Add a stable source ID only when it materially informs a skill. Update the central catalogue and every affected local map together. A source ID must have a date and canonical URL, and every catalogue entry must be used by at least one skill. Prefer original paraphrase. Do not paste article text, code, or full posts.

## Privacy and attribution

Do not include credentials, private absolute paths, personal email addresses, customer data, or session exports. Test fixtures for detectors must assemble synthetic strings at runtime rather than embedding real secrets. Label adaptations as original work and do not imply endorsement by a referenced author.

## Validation

Run:

```bash
python scripts/validate.py
python scripts/smoke.py
python -m unittest discover -s tests -v
```

Add a negative test when you add a new validator rule. Tests must run offline with the standard library. Do not commit generated caches, artifacts, logs, or local environment files. Update `release-manifest.txt` for every intended publication file; the validator fails on an unlisted file or a manifest entry that is not part of the release.

## Review

Changes should describe the user-visible problem, the evidence, and the untested boundary. Do not present a structural check as proof of model behavior.
