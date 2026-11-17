# Depth-first parallelism field guide

## Choose a question, not a task list

Parallel attempts work when they compete to explain the same observation. They waste effort when each attempt explores a different feature. Write one question, then list the hypotheses that could answer it.

## Hypothesis ledger

| Attempt | Hypothesis | Predicted observation | Falsifier | Workspace | Result | Stop reason |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

The falsifier is written before the attempt. If the observation cannot distinguish the hypothesis, the attempt is not informative.

## Isolation

- Separate checkout or worktree per attempt.
- Separate ports, database names, temporary directories, and browser profiles.
- Separate test accounts or tokens when the system permits.
- A shared read-only baseline artifact is fine; shared mutable state is not.
- Record any accidental sharing and discard the affected results.

## Specialization

Give each attempt a tool or model suited to its angle: one reproduces by replaying a log, another instruments timing, another writes a minimal failing case. Specialization is useful only if the results remain comparable.

## Convergence

Stop an attempt when its hypothesis is eliminated or its evidence is no longer relevant. Compare survivors on the same baseline. Re-run the winner in a clean environment before recommending a change. Preserve the losing attempts' stop reasons so the conclusion can be audited.

## Cost

Parallelism increases short-term resource use. Set an attempt budget and a wall-clock limit. Do not use the number of attempts as a quality metric. One well-designed elimination is better than several redundant runs.

## Failure modes

- Parallel attempts that all test the same hypothesis.
- Shared state contaminating results.
- Keeping every attempt alive after the question is answered.
- Treating volume as confidence.
- Recommending a fix without a clean re-test.
