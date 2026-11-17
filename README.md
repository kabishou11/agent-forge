# **Agent Forge** — Forge intent into verifiable engineering

Agent Forge is an independent, publication-ready collection of ten focused Agent Skills for coding work that must stay aligned with intent and end in evidence. It is a workflow toolkit, not a summary dump. Each skill has a short main file for execution, plus local references opened only when needed.

[简体中文](README.zh-CN.md) | [Source catalogue](docs/sources.md) | [Validation](docs/validation.md) | [Synthetic walkthrough](docs/examples/synthetic-walkthrough.md)

## Why this exists

Coding agents often fail in predictable places: they start before clarifying the goal, read too much or too little context, confuse a plausible cause with evidence, and declare success without running the flow. Agent Forge turns those failure points into small, stoppable workflows. Every stage can produce a useful result, including "non-bug", "not reproduced", "fix stopped as risky", or `NOT RUN`.

The skills are structural and instructional. They do not enforce behavior, expand permissions, replace review, or guarantee better outcomes.

## The ten workflows

| Skill | Use it when | Typical artifact |
| --- | --- | --- |
| [forge-intent-alignment](skills/forge-intent-alignment/SKILL.md) | The request is vague, mixes symptoms with causes, changes scope, or needs a restatement and acceptance checks. | Intent brief, assumptions, acceptance checks |
| [forge-signal-first-context](skills/forge-signal-first-context/SKILL.md) | The codebase is unfamiliar or large, or exploration is drifting into reading every file. | Context packet with facts, provenance, exclusions |
| [forge-disposable-prototypes](skills/forge-disposable-prototypes/SKILL.md) | Alternatives need comparison and one open question blocks a design decision. | Timeboxed prototype, measurement table, discard decision |
| [forge-architectural-constraints](skills/forge-architectural-constraints/SKILL.md) | The same correction keeps recurring, or a quick patch would spread a bad pattern. | Structural fix, enforcement point, migration and rollback |
| [forge-verification-harness](skills/forge-verification-harness/SKILL.md) | A change needs repeatable end-to-end checks, a driver, isolated state, or a user Feature Map. | Working driver, Feature Map, before/after artifacts |
| [forge-triage-repro-fix](skills/forge-triage-repro-fix/SKILL.md) | A defect report needs triage, exact reproduction, a failing test, and a bounded repair. | Verdict, reproduction, failing test, mechanism note |
| [forge-evidence-review](skills/forge-evidence-review/SKILL.md) | A diff, fix, design, or formal claim needs independent review with executable evidence. | Verdict, counterexamples, blocking findings, untested areas |
| [forge-depth-first-parallelism](skills/forge-depth-first-parallelism/SKILL.md) | One failure has competing hypotheses and isolated workspaces are available. | Hypothesis ledger and elimination evidence |
| [forge-context-budget](skills/forge-context-budget/SKILL.md) | The session is overloaded, many skills could apply, or instructions need ablation. | Context manifest, trigger notes, ablation result |
| [forge-formal-boundaries](skills/forge-formal-boundaries/SKILL.md) | A model, proof, state machine, or bounded check is proposed as evidence. | Assumptions, bounds, counterexample interpretation, residual risk |

## Choice guide

- **Not sure what the user wants:** start with intent alignment.
- **New or large repository:** start with signal-first context, then narrow to a decision.
- **Several designs, no evidence:** use a disposable prototype.
- **A mistake keeps coming back:** move to architectural constraints.
- **You need to prove a flow works:** build a verification harness before claiming readiness.
- **A bug report arrived:** use the stoppable triage, reproduction, and fix loop.
- **A change is ready for review:** require evidence-first review, not a speculative nitpick swarm.
- **A failure has multiple explanations:** go depth-first with parallel attempts on one question.
- **The session or skill set is bloated:** use the context budget.
- **Someone cites a proof or model:** apply the formal verification boundaries.

A task can use several skills, but the main file should be read only when its trigger applies. Open references on demand.

## Installation

Acquire Agent Forge only from its public project page or release archive. If the publisher provides a clone URL, use only the Agent Forge URL; no other repository is a source for these skill folders.

Copy selected skill folders into the skill directory used by your host, preserving the folder, `references/`, `LICENSE`, and `NOTICES.md`. Each skill is self-contained, including its own source map and notices. Do not copy the whole repository into the skills root, do not add a nested `skills/` level, and do not overwrite or merge into an existing destination.

Project-level Codex-style example with a relative target and a refusal guard:

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

Project-level OpenCode example:

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

Run one snippet per selected skill. The guard checks an existing file, directory, or symlink before copying, so a failed check does not merge into a partial destination.

The resulting shape must be:

```text
<target-project>/.agents/skills/forge-intent-alignment/SKILL.md
<target-project>/.agents/skills/forge-intent-alignment/LICENSE
<target-project>/.agents/skills/forge-intent-alignment/NOTICES.md
<target-project>/.agents/skills/forge-intent-alignment/references/field-guide.md
<target-project>/.agents/skills/forge-intent-alignment/references/sources.md
<target-project>/.agents/skills/forge-intent-alignment/references/smoke-case.md
```

Wrong shapes include `<target-project>/.agents/skills/skills/forge-intent-alignment/` and a main file placed directly at `.agents/skills/SKILL.md`. Some hosts also document user-level skill directories; follow the host's own documentation for those locations. This repository does not install anything globally or automatically.

Host discovery is documented, but live installation and behavior in any host were **not tested** here. The layout is structurally compatible with the Agent Skills conventions checked on 2026-11-18: lowercase kebab-case name matching the parent directory, a trigger-oriented description, and progressive disclosure through local references. Public host references checked on that date: [Agent Skills specification](https://agentskills.io/specification), [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills.md), and [OpenCode skills documentation](https://opencode.ai/docs/skills/). Agent Forge is not a plugin package.

## Example

A synthetic walkthrough shows the intended composition across intent, context, harness, and triage skills. It is illustrative, not a behavioral evaluation: [docs/examples/synthetic-walkthrough.md](docs/examples/synthetic-walkthrough.md).

Minimal usage pattern inside an agent session:

1. Ask the host to load `forge-intent-alignment` and restate the goal.
2. Load `forge-signal-first-context` only after the question is clear.
3. Add a verification harness when the claim needs an end-to-end check.
4. Use triage or evidence-first review to keep the result stoppable and checkable.

## Validation

Requires Python 3.11 or newer and no network access for the checks themselves:

```bash
python scripts/validate.py
python scripts/smoke.py
python -m unittest discover -s tests -v
```

The validator checks the restricted string-scalar frontmatter profile, name and description rules, section order and main-file size, example markers, relative links, per-skill link containment, standalone license and notices, synthetic smoke-case schemas, canonical and reciprocal source mappings, duplicate source URLs, the release manifest, forbidden publication artifacts, oversized files, and pattern-based privacy hygiene. The suite includes negative mutation tests for bad names, missing triggers, broken links, missing sources, duplicate source URLs, malformed frontmatter, missing notices, forbidden artifacts, oversized files, manifest drift, smoke-case errors, and synthetic leak fixtures. GitHub Actions runs all three commands; the workflow's checkout and Python setup steps need network access even though validation is offline.

Privacy scanning is a heuristic, not proof that no secret exists. The release manifest must match the repository file set exactly, so an unexpected log, cache, session export, or other artifact fails validation. Python cache files and `.git` are excluded from the publication scan; artifact and dump directories are not silently ignored.

Passing these checks does not prove that a model follows the workflow, that a host discovers the skills, that output quality improves, or that costs fall. The exact boundary is documented in [docs/validation.md](docs/validation.md).

## Attribution and rights

Agent Forge is an independent adaptation inspired by public writing from Lauren Tan (@poteto). It is **not official, affiliated, sponsored, reviewed, or endorsed** by Lauren Tan or by any of her employers or companies. It is not pstack code, and no article text, repository code, or full post was copied. The templates, labels, workflow wording, validator, tests, and examples here are original adaptations and should not be attributed to the source author.

The public posts listed in [docs/sources.md](docs/sources.md) remain their authors' property. URLs are provided for attribution; public readability does not grant sublicensing rights. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Original material in this repository is released under the [MIT License](LICENSE). That license applies only to our original work. Each skill folder carries its own copy of `LICENSE` and `NOTICES.md` so a selected-folder installation preserves the rights notes without the repository root.

## Limits

- These are instructions and artifacts. They do not override host policies, approvals, sandbox rules, credentials, or user authority.
- A skill can stop without a fix. "Not a bug", "not reproduced", "risky", and `NOT RUN` are valid outcomes.
- Verification covers only the checks that actually ran.
- Formal results are bounded by assumptions and model scope; they are not bug-free guarantees.
- The validator proves structural consistency, not behavior, quality, security, or cost impact.
- No productivity or PR-count claims are made. The toolkit does not measure performance that way.
- Public availability of a source does not make its contents reusable beyond the source's own terms.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CHANGELOG.md](CHANGELOG.md).
