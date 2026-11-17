# Intent alignment field guide

## What good alignment looks like

A useful restatement is shorter than the implementation plan and specific enough that a reviewer can say "yes, that is what I meant" or "no, you changed the scope". It names the user-visible outcome, the boundary of the change, and the evidence that would count.

## Separation table

| Question | Record as | Avoid |
| --- | --- | --- |
| What happened? | Observation with source | Turning a guess into a fact |
| What did the reporter think caused it? | Quoted hypothesis | Repeating the hypothesis as the goal |
| What should change? | Goal and non-goals | A list of implementation steps |
| How will we know? | Acceptance check | "It works" or "looks good" |
| What is still unclear? | Open question or assumption | Silent assumption |

## Vocabulary gaps

When the requester and the codebase use different words, write both vocabularies side by side. A storyboard can help: sketch the user-visible sequence, the states, and the decisions before choosing production code. Treat the storyboard as a communication device, not as evidence that the implementation is correct.

If a technique is adapted from another discipline or another author's example, label the adaptation as ours. Do not imply that the original author produced this implementation.

## Clarifying questions

Ask only when the answer changes the next action. Good questions are bounded:

- "Should the output format stay unchanged, or may the column order change?"
- "Is the target a measured improvement, or only removal of the timeout?"
- "Who owns the caller that would need a migration?"

Bundle non-blocking questions into an assumption list and continue. Do not stall on preferences that can be revisited.

## Decision log shape

Record the date, the decision, the alternatives, the evidence, and the owner. When scope changes later, link the new decision to the earlier one instead of rewriting history.

## Failure modes

- A long restatement that repeats the request without adding a check.
- Adopting a speculative root cause and "fixing" it before reproducing.
- Treating a preference as an acceptance criterion.
- Asking for approval inside the assistant when the host owns approvals.
- Claiming a result after an unexecuted step. Use `NOT RUN` instead.
