# Source catalogue

Agent Forge is an independent adaptation. The links below are primary public posts that informed the themes of this toolkit. They are not bundled content, and no article text, code, or full post is reproduced here. Each row is an original paraphrase of a theme, with a stable ID used by the skill-local source maps.

Dates follow the Asia/Shanghai calendar date supplied with the source pointer. URLs are canonical links to the original authors' public posts. Rights in those posts remain with their authors. Reading a public post does not grant a sublicense to its contents.

## Catalogue

| ID | Date | URL | Theme (original paraphrase) | Skills using it |
| --- | --- | --- | --- | --- |
| S01 | 2026-01-22 | https://x.com/poteto/status/2014257661035094246 | Clarify the goal and gather high-signal context before code; avoid reading every file or importing stale patterns. | forge-intent-alignment, forge-signal-first-context, forge-context-budget |
| S02 | 2026-05-26 | https://x.com/poteto/status/2058975157503570132 | Work depth-first with hypotheses and elimination; reproduce, write a failing test, explain mechanism, then make the smallest high-impact change. | forge-intent-alignment, forge-disposable-prototypes, forge-triage-repro-fix, forge-depth-first-parallelism |
| S03 | 2026-06-25 | https://x.com/poteto/status/2069824386283319343 | Verification is the bottleneck; a reusable control CLI isolates checkout, build, ports, browser, and user state, and every stage may stop. | forge-verification-harness, forge-triage-repro-fix |
| S04 | 2026-09-01 | https://x.com/poteto/status/2094457600259842065 | A verification skill needs a working CLI or driver and a user-facing Feature Map; run one complete flow before calling it ready. | forge-verification-harness |
| S05 | 2026-09-10 | https://x.com/poteto/status/2097732320606507506 | Restate the original report without parroting a speculative cause; use disposable prototypes to answer open questions and design caller-first. | forge-intent-alignment, forge-disposable-prototypes, forge-triage-repro-fix, forge-evidence-review |
| S06 | 2026-08-17 | https://x.com/poteto/status/2089067865098113024 | Correction priority starts with architecture and data structures, then lint, tests, CI, skills, and human review; required review remains. | forge-architectural-constraints |
| S07 | 2026-10-17 | https://x.com/poteto/status/2111133080526495985 | Align intent first, mine repeated corrections, and prefer deterministic constraints over prose. | forge-intent-alignment, forge-architectural-constraints |
| S08 | 2026-11-03 | https://x.com/poteto/status/2117437607940681849 | Abstract adversarial review often spends tokens on nitpicks; later guidance favors empirical and formal verification. | forge-evidence-review |
| S09 | 2026-11-06 | https://x.com/poteto/status/2118416074601545968 | Formal methods are not a bug-free guarantee; intent, spec, model, and implementation differ, and bounded checking has limits. | forge-evidence-review, forge-formal-boundaries |
| S10 | 2026-11-09 | https://x.com/poteto/status/2119521036660314339 | Use one meaningful subsystem per verification model and visualize user flows as a review aid. | forge-verification-harness, forge-formal-boundaries |
| S11 | 2026-04-26 | https://x.com/poteto/status/2048092593087721736 | Run depth-first parallel attempts and reproductions on one or a few questions, specializing tools to each attempt. | forge-evidence-review, forge-depth-first-parallelism |
| S12 | 2026-11-01 | https://x.com/poteto/status/2116580481236115933 | Script repeated mechanical agent work and filter expensive routine events; a cited hourly cadence is a personal habit, not a platform limit. | forge-verification-harness, forge-context-budget |
| S13 | 2026-10-15 | https://x.com/poteto/status/2110415199962612120 | Tune or ablate unneeded skill sections as models change, and evaluate the effects. | forge-context-budget |
| S14 | 2026-11-15 | https://x.com/poteto/status/2121646643124809848 | Minimal quick fixes can propagate bad patterns; bounded root-cause repair may be broader but is not unlimited rewrite permission. | forge-architectural-constraints, forge-triage-repro-fix |
| S15 | 2026-11-08 | https://x.com/poteto/status/2119313621188849806 | Admit a vocabulary gap, clarify and restate, and storyboard before production; code adaptations are labeled as ours. | forge-intent-alignment, forge-disposable-prototypes |
| S16 | 2026-10-07 | https://x.com/poteto/status/2107510472601985336 | Separate the outer loop that gathers external context from the inner loop that executes; another project's automation is not permission. | forge-signal-first-context, forge-context-budget |

## Reciprocity

Every catalogue row names at least one skill. Every skill has a local `references/sources.md` with the same IDs, dates, and URLs, limited to the sources relevant to that skill. The validator checks both directions, compares the catalogue to fixed canonical metadata, and fails on an orphan source, a mismatched mapping, or a canonical URL shared by two source IDs. S04 and S05 are distinct entries with distinct dates and URLs.

## Boundaries

This catalogue records inspiration and reference, not endorsement. Neither the source authors nor any of their employers or companies authored, reviewed, or approved this repository. The toolkit's templates, labels, checks, and validator are original work. Where a technique comes from another field, the adaptation is labeled as ours in the relevant skill.

Source links are provided for attribution and further reading. They are not required at runtime, and no skill depends on a network fetch.
