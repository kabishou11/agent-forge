# Validation

Agent Forge validates its own structure and publication hygiene. It does not evaluate whether a language model follows a skill, and it does not benchmark agent quality, cost, or productivity.

## Commands

Run from the repository root with Python 3.11 or newer:

```bash
python scripts/validate.py
python scripts/smoke.py
python -m unittest discover -s tests -v
```

The validators exit non-zero and print each finding when a check fails. The test suite uses only the Python standard library and makes no network calls.

## Restricted frontmatter profile

The repository intentionally supports only a small string-scalar subset of YAML, not the full language:

- Frontmatter begins and ends with an unindented `---` line.
- Each non-empty line is an unindented `key: value` pair. Keys match `[A-Za-z_][A-Za-z0-9_-]*`; only `name` and `description` are allowed, once each.
- Values must be non-empty scalars. A plain scalar cannot begin with a reserved YAML indicator character (`-`, `?`, `:`, `,`, `[`, `]`, `{`, `}`, `#`, `&`, `*`, `!`, `|`, `>`, `'`, `"`, `%`, `@`, or a backtick). It cannot contain `: ` (embedded mapping) or whitespace followed by `#` (inline comment), and it cannot be a YAML boolean, null, base or float number, tag, anchor, alias, sequence, mapping, collection, or block.
- Quoted scalars must wrap the entire value in one matching pair of single or double quotes. The matching quote must not appear inside the value, and backslash escape sequences are unsupported and rejected. A quoted scalar is always read as a string, so `"true"` and `"42"` are strings while bare `true` and `42` are rejected.
- Indentation, duplicate keys, unexpected keys, and empty values are rejected.

Existing release files pass this profile. The validator is not a general YAML implementation and should not be described as one.

## What is checked

- Required publication files exist at the documented paths.
- Every `skills/forge-*/SKILL.md` has restricted-profile frontmatter with `name` and `description` string fields.
- The name matches its parent directory, is 1 to 64 characters, uses lowercase kebab-case, and has no consecutive hyphens.
- The description is within 1 to 1024 characters and contains a `Use when` trigger clause.
- The required sections are present in order: Inputs, Workflow, Stop conditions, Deliverables, Example, Sources.
- The main `SKILL.md` is between 40 and 90 lines.
- The example contains `Input:`, `Expected output:`, and `Stop case:` markers.
- Every relative markdown link resolves to an existing file.
- Every relative link inside a skill stays within that skill directory, so a copied skill folder is self-contained.
- Every skill folder contains `LICENSE`, `NOTICES.md`, local source and field-guide references, and a synthetic smoke case. A copied folder passes the standalone bundle check.
- The central source catalogue and every local source map agree on IDs, dates, and URLs.
- The catalogue's canonical dates and URLs match the fixed source metadata, including distinct S04 and S05 entries, and no two source IDs share one canonical URL.
- Each skill's local source set matches the central "Skills using it" mapping exactly.
- No central source is unused, and no local source is missing from the catalogue.
- Each smoke case is clearly labeled as illustrative, has the required input, schema, status, and stop-case sections, and declares a valid artifact status plus `status` and other artifact fields.
- The release manifest matches the publishable file set exactly. Unlisted files, missing entries, Python cache paths, artifact directories, and log or temporary files fail validation.
- Publication files are not silently skipped for size. An oversized file produces an error instead of being exempted from the release.
- Publication files do not contain detected private absolute paths, email addresses, or common credential shapes. There is no license-contact email in this repository; the rule has no email allowlist by default.

## Negative mutation tests

The unittest suite does not only run the happy path. It mutates synthetic fixtures to prove the validator can fail:

- A bad skill name with uppercase characters and a directory mismatch.
- A description without a `Use when` trigger.
- A relative link that points outside the skill folder or to a missing file.
- A local source entry missing from the central catalogue.
- A duplicate canonical source URL and a mismatch between the fixed S04/S05 metadata and the catalogue.
- Unmatched quotes, internal unescaped quotes, unsupported quote escapes, inline comments, reserved leading YAML punctuation, embedded mapping syntax, booleans, nulls, numbers, tags, anchors, aliases, and sequence syntax in frontmatter.
- A copied skill folder missing its notices.
- A publication leak assembled at test time rather than stored as a credential.
- A forbidden artifact directory, a forbidden log file, and an oversized publication file.
- A release manifest with an unlisted file or a log entry.
- A smoke case missing a required artifact status.
- A smoke case with a list or object status, or with unhashable entries in `required_fields`.

The leak fixtures build strings from fragments so the test file does not itself embed a credential-shaped literal. Each negative test asserts that the expected check reports an error.

Publication hygiene uses heuristic pattern checks for secrets, private absolute paths, email addresses, and suspicious dump filenames. It does not prove that no secret exists. It also does not classify proper nouns as real project names; the examples use fictional service names and are reviewed manually.

## Worked example

The synthetic walkthrough in [examples/synthetic-walkthrough.md](examples/synthetic-walkthrough.md) is an illustrative, offline example of how the skills compose. Each skill also ships a `references/smoke-case.md` that names a synthetic input, an expected artifact schema and status fields, and a stop case. These are repeatable structural fixtures, not model-behavior evaluations, benchmarks, or evidence that a host model will follow the workflow.

## Offline boundary

Validation is offline after the repository and Python runtime are present. The GitHub Actions workflow uses `actions/checkout` and Python setup, which require network access to GitHub and the package mirror used by the runner. That workflow infrastructure is not part of the offline validators.

## Exact untested boundary

Passing the schema, link, source-map, and hygiene checks does not prove that:

- A host application discovers these skills. Discovery rules are documented by the host, but no live host installation or behavior was tested here.
- A model will follow the instructions, load a reference on demand, or preserve the intended order.
- Work produced with a skill is better, faster, cheaper, or safer than work without it.
- A smoke case predicts real model output. It checks fixture structure and status vocabulary only.
- A security review, formal proof, or human approval is complete.
- The privacy scan proves that no secret exists.
- A skill's advice overrides host policies, approvals, sandbox rules, or user authority.

These are compatibility and structural checks only. The toolkit is not a plugin package, and the repository does not install skills globally.
