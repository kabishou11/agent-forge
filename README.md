# Agent Forge

Ten small, project-local Agent Skills for coding work that has to stay aligned with intent and end with evidence. Use them when a request is vague, a codebase is unfamiliar, a bug report is noisy, or a change needs proof before review.

Agent Forge is not a framework or a plugin. Each skill is a short checklist plus optional local references. Copy one skill folder into a project, read the main file when its trigger applies, and stop at any stage with a useful result.

[简体中文](README.zh-CN.md) | [Runnable example](examples/triage-repro-fix/README.md) | [Validation details](docs/validation.md) | [Contributing](CONTRIBUTING.md)

## Problems it addresses

- **Starting before the request is clear.** Separate observations from the proposed cause, record assumptions, and define acceptance checks before editing.
- **Reading too much or too little.** Target entry points, interfaces, tests, logs, and recent changes instead of reading every file.
- **Confusing a plausible cause with evidence.** Triage the report, capture the exact flow, write a failing regression, then make the smallest repair that addresses the mechanism.
- **Reviewing by preference alone.** Turn "looks right" into a verdict backed by executed checks, counterexamples, and named untested areas.
- **Forcing a fix when stopping is better.** "Not a bug", "not reproduced", "risky", and `NOT RUN` are useful outcomes.

## Quick start: install one skill

Clone the public repository at [github.com/kabishou11/agent-forge](https://github.com/kabishou11/agent-forge), then run the snippet from the repository root. Copy only the skills you need into a project-level skill directory. The guard refuses an existing file, directory, or symlink, so it never merges into or overwrites user content.

Codex-style `.agents/skills` example:

```bash
set -eu
TARGET=../target-project
SKILL=forge-intent-alignment

mkdir -p "$TARGET/.agents/skills"
DEST="$TARGET/.agents/skills/$SKILL"
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  printf 'Refusing to overwrite existing destination: %s\n' "$DEST" >&2
  exit 1
fi
cp -R "skills/$SKILL" "$DEST"
```

OpenCode `.opencode/skills` example:

```bash
set -eu
TARGET=../target-project
SKILL=forge-verification-harness

mkdir -p "$TARGET/.opencode/skills"
DEST="$TARGET/.opencode/skills/$SKILL"
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  printf 'Refusing to overwrite existing destination: %s\n' "$DEST" >&2
  exit 1
fi
cp -R "skills/$SKILL" "$DEST"
```

Run one snippet per selected skill and change `SKILL` each time. A copied folder is self-contained: its relative links, `LICENSE`, `NOTICES.md`, and references travel with it.

The resulting shape is:

```text
<target-project>/.agents/skills/forge-intent-alignment/SKILL.md
<target-project>/.agents/skills/forge-intent-alignment/LICENSE
<target-project>/.agents/skills/forge-intent-alignment/NOTICES.md
<target-project>/.agents/skills/forge-intent-alignment/references/field-guide.md
<target-project>/.agents/skills/forge-intent-alignment/references/sources.md
<target-project>/.agents/skills/forge-intent-alignment/references/smoke-case.md
```

Do not copy the whole repository into the skills root, add a nested `skills/` level, or place `SKILL.md` directly at `.agents/skills/SKILL.md`. Some hosts also document user-level directories; follow the host's own documentation. Agent Forge does not install globally or automatically.

## First workflow: from bug report to reviewed fix

The runnable example follows one synthetic defect through the triage workflow:

```bash
python3 examples/triage-repro-fix/run_demo.py --output .forge-demo-output
```

Expected final lines:

```text
status: evidence-ready
artifacts: .forge-demo-output
```

It reads a tiny fictional [bug report](examples/triage-repro-fix/bug-report.md), writes an intent brief, makes a regression test fail, applies a one-line repair, reruns the same test, and produces an evidence review. Inspect `intent-brief.md`, `repro-failure.txt`, `bounded-fix.diff`, `verification-pass.txt`, and `evidence-review.md`, then delete the output directory. The path is relative, and the demo refuses an existing file, directory, or symlink.

The verdict requires the expected assertion failures before the repair, the same test passing after it, and successful review checks. An import, syntax, harness error, or unrelated failure returns `needs-work` and stays visible in the artifacts. This is an executable artifact flow, not a test of whether a language model follows the skill. Full details are in the [example README](examples/triage-repro-fix/README.md).

## The ten skills

| Skill | Reach for it when | Useful output |
| --- | --- | --- |
| [forge-intent-alignment](skills/forge-intent-alignment/SKILL.md) | The request is vague, mixes symptoms with causes, changes scope, or needs acceptance checks. | Intent brief, assumptions, acceptance checks |
| [forge-signal-first-context](skills/forge-signal-first-context/SKILL.md) | The codebase is unfamiliar or large, or exploration is drifting into reading every file. | Context packet with facts, provenance, and exclusions |
| [forge-disposable-prototypes](skills/forge-disposable-prototypes/SKILL.md) | Alternatives need comparison and one open question blocks a design decision. | Timeboxed prototype, measurement table, discard decision |
| [forge-architectural-constraints](skills/forge-architectural-constraints/SKILL.md) | The same correction keeps recurring, or a quick patch would spread a bad pattern. | Structural fix, enforcement point, migration and rollback |
| [forge-verification-harness](skills/forge-verification-harness/SKILL.md) | A change needs repeatable end-to-end checks, a driver, isolated state, or a user Feature Map. | Working driver, Feature Map, before/after artifacts |
| [forge-triage-repro-fix](skills/forge-triage-repro-fix/SKILL.md) | A defect report needs triage, exact reproduction, a failing test, and a bounded repair. | Verdict, reproduction, failing test, mechanism note |
| [forge-evidence-review](skills/forge-evidence-review/SKILL.md) | A diff, fix, design, or formal claim needs independent review with executable evidence. | Verdict, counterexamples, blocking findings, untested areas |
| [forge-depth-first-parallelism](skills/forge-depth-first-parallelism/SKILL.md) | One failure has competing hypotheses and isolated workspaces are available. | Hypothesis ledger and elimination evidence |
| [forge-context-budget](skills/forge-context-budget/SKILL.md) | The session is overloaded, many skills could apply, or instructions need ablation. | Context manifest, trigger notes, ablation result |
| [forge-formal-boundaries](skills/forge-formal-boundaries/SKILL.md) | A model, proof, state machine, or bounded check is proposed as evidence. | Assumptions, bounds, counterexample interpretation, residual risk |

A task can use several skills. Read a main file only when its trigger applies, and open references only when the next step needs them.

## Using a skill in a session

1. Ask the host to load the skill by name, for example `forge-intent-alignment`.
2. Give it the request, the relevant files, and any existing evidence.
3. Let the skill stop when the next step needs approval, a missing environment, or a different owner.

## Documentation and contributions

- [Runnable triage example](examples/triage-repro-fix/README.md) — input, commands, artifacts, and checks.
- [Synthetic composition walkthrough](docs/examples/synthetic-walkthrough.md) — how several skills can fit together.
- [Source catalogue](docs/sources.md) — public writing that informed the themes.
- [Validation and compatibility](docs/validation.md) — checks, host references, and the untested boundary.
- [Contributing](CONTRIBUTING.md) — skill changes, sources, privacy, commit format, and checks.
- [Changelog](CHANGELOG.md) and [third-party notices](THIRD_PARTY_NOTICES.md).

## Compatibility and verification

Skill folders follow the Agent Skills layout: a lowercase kebab-case name matching the folder, a trigger-oriented description, and local references. The documented copy snippets are exercised in project-scoped temporary directories; live host discovery and model behavior are not tested. See [validation and compatibility](docs/validation.md) for the host references, checks, and exact boundary.

## Attribution and license

Agent Forge is independent original work inspired by public writing from Lauren Tan (@poteto). It is not official, affiliated, sponsored, reviewed, or endorsed by her or by any of her employers or companies. Original material is MIT licensed; source posts remain their authors' property. See [sources](docs/sources.md), [notices](THIRD_PARTY_NOTICES.md), and [LICENSE](LICENSE). Each skill folder carries its own `LICENSE` and `NOTICES.md`.
