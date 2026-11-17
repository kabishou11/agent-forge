# Signal-first context field guide

## The context packet

Keep the packet on one screen when possible:

```
Question:
Facts:
  - path/symbol: fact (source, date)
Inferences:
Open questions:
Candidate files:
Excluded:
Next observation:
```

Every fact should be traceable. If a fact came from a stale document, mark it as stale rather than deleting the uncertainty.

## Reading order

1. Entry point or route for the user-visible flow.
2. Interface, schema, or type crossing the boundary.
3. Closest existing test or reproduction.
4. Configuration that changes behavior.
5. Recent changes touching the same symbols.
6. Documentation, treated as a hypothesis until checked against code.

Stop when the call path for the current question is explained. You do not need a complete architecture map for a one-line defect.

## Sampling large repositories

- List directory names before opening files.
- Read one representative implementation and one test.
- Search by symbol or error text, not by guessing filenames.
- Prefer current call sites over examples in archived folders.
- Note deprecated patterns explicitly so they are not copied into new code.

## Outer loop and inner loop

The outer loop gathers external context: reports, docs, logs, environment facts. The inner loop edits and checks code. Mixing them without a record produces thrash. When the inner loop discovers a missing external fact, pause, name it, and return to the outer loop deliberately.

## Privacy and provenance

Do not paste private customer data, credentials, or personal paths into the packet. Use synthetic examples or redact before storing. A path that identifies a machine or user should not appear in a shared artifact.

## Failure modes

- Reading every file "to be safe" and then losing the question.
- Copying the first example found even if it is deprecated.
- Treating a comment or README as current behavior.
- Reporting an inference as an observation.
- Calling a skipped runtime check a success.
