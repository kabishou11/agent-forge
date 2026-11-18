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

## Validation and examples

Run from the repository root with Python 3.11 or newer:

```bash
python3 scripts/validate.py
python3 scripts/smoke.py
python3 -m unittest discover -s tests -v
```

The tests execute the documented installation snippets in project-scoped temporary directories, check the installed bundle and relative links, exercise the refusal guard, and run the triage demo. They do not install globally or test host discovery. If you run the demo yourself, use a relative `--output` path and remove the output directory afterwards.

Add a negative test when you add a new validator rule. Tests must run offline with the standard library. Do not commit generated caches, artifacts, logs, or local environment files. Update `release-manifest.txt` for every intended publication file; the validator fails on an unlisted file or a manifest entry that is not part of the release.

## Commit messages

Use Conventional Commits with a lowercase imperative subject and a required scope:

```text
type(scope): summary
```

Common types are `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `build`, `ci`, `perf`, and `revert`. Type and scope are lowercase; scope is kebab-case. Group related edits into one logical commit and keep unrelated formatting or cleanup out of it.

The lightweight checker validates the format, case, and trailers. It does not judge whether the summary verb is imperative in English; reviewers check the wording. Apply the scope rule to new commits and do not rewrite history solely to add scopes to legacy commits.

Do not create empty commits, rewrite pushed history, or add coauthor or tool-generation trailers. Run the checks before submitting. A draft message can be checked offline:

```bash
python3 scripts/check_commit_message.py message.txt
```

For example:

```text
docs(readme): explain project-local installation
test(install): execute documented copy snippets
feat(example): add runnable triage workflow
```

## Review

Changes should describe the user-visible problem, the evidence, and the untested boundary. Do not present a structural check as proof of model behavior.
