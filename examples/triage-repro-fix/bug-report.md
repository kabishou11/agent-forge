# Synthetic bug report

A draft with two tags saves only the first tag.

Reporter guess: the cache is dropping the second tag.

Steps:

1. Open a draft.
2. Add the tags `alpha` and `beta`.
3. Save the draft and reopen it.

Expected: both tags remain.

Actual: only `alpha` remains.

The report does not include a log, a version, or a performance target. The local fixture has no production account and needs no network access.
