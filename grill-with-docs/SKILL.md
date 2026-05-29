---
name: grill-with-docs
description: Interview the user relentlessly about a plan or design until reaching shared understanding, capturing every resolved decision, scenario, term, and open question into an isolated grilling task's specs/ folder so no context is lost. Use when the user wants to stress-test a plan, get grilled on a design, poke holes in an approach, or says "grill me", "grill with docs", "challenge my thinking", or "stress test this".
---

<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead of asking.

The difference from a plain grilling session: **everything we resolve is captured as we go** into an isolated grilling task, so the session leaves a durable record instead of evaporating into the conversation.

</what-to-do>

<session-bootstrap>

## Always create the grilling task at the start

Before asking the first question, create the grilling task. This is non-negotiable — capture-by-default is the entire point of this skill.

1. Pick a short slug for the topic (e.g. `workflow-contract`, `auth-rework`).
2. Create `tasks/current/task-grill-<slug>/task.md` (standalone task — format below).
3. Create the `tasks/current/task-grill-<slug>/specs/` folder with its starter modules (see [grilling-task-format.md](references/grilling-task-format.md)).
4. Update `tasks/ACTIVE.md` (add to **In Progress**, type `grill`) and `tasks/STATUS.md` (set the `Last updated` line).

The `specs/` folder is the **isolated capture area**. It is deliberately separate from the application's real `docs/` — grilling produces draft thinking, not application documentation. Nothing in a grilling task touches `docs/` or the repo root.

`task.md` for a grilling task:

```yaml
---
id: task-grill-<slug>
type: standalone
status: in_progress
summary: Grilling session — stress-testing <one-line topic>
depends_on: []
blocked_by: ~
test_criteria: shared understanding reached on <topic>; all resolved context captured in specs/
created: YYYY-MM-DD
---
```

</session-bootstrap>

<capture-protocol>

## Write inline, never batch

As each decision crystallises, write it to the right spec module immediately — in the same turn you resolve it. Do not wait until the end of the session to "write it all up"; that is how context gets lost. The spec modules and their formats are defined in [grilling-task-format.md](references/grilling-task-format.md). In short:

| What you just resolved | Where it goes |
|---|---|
| The plan / what's under stress-test | `specs/00-overview.md` |
| A decision + its rationale + rejected alternatives | `specs/decisions.md` |
| A concrete edge-case scenario you probed | `specs/scenarios.md` |
| A sharpened or disambiguated term | `specs/glossary.md` |
| A branch left unresolved | `specs/open-questions.md` |
| A decision that meets the ADR bar | `specs/candidate-adrs.md` |

</capture-protocol>

<grilling-technique>

## Sharpen fuzzy language

When I use a vague or overloaded term, propose a precise canonical term and record it in `specs/glossary.md`. "You're saying 'account' — do you mean the Customer or the User? Those are different things." If the same term recurs with a different meaning later, call out the conflict against what's already in the glossary.

## Discuss concrete scenarios

When domain relationships or behaviours are discussed, stress-test them with specific invented scenarios that probe edge cases and force precision about boundaries. Record the ones that change the design in `specs/scenarios.md`.

## Cross-reference with code

When I state how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code does X, but you just said Y — which is right?" Resolved contradictions become decisions.

## Capture candidate ADRs sparingly

Only flag a decision as ADR-worthy when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful.
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons.

If any of the three is missing, it is just a decision (`specs/decisions.md`), not a candidate ADR.

**Candidate ADRs are drafts, not real ADRs.** Write them into `specs/candidate-adrs.md` using this repo's actual ADR template (Context / Decision / Consequences — see [docs/adr/FORMAT.md](../../../docs/adr/FORMAT.md)). Do **not** create files in `docs/adr/` during grilling: real ADRs are append-only, numbered, and only land when the decision is implemented. The candidate draft is what gets promoted to a numbered `docs/adr/ADR-NNN-<slug>.md` later, during the implementation task — not here.

</grilling-technique>

<completion>

## Closing the session

When shared understanding is reached:

1. Make sure every resolved item is captured in `specs/` (the test_criteria for the task).
2. Set `task.md` `status: completed` and move the task folder to `tasks/completed/`.
3. Update `tasks/ACTIVE.md` (remove from In Progress) and `tasks/STATUS.md` (set the `Last updated` line).
4. Run `python scripts/validate-project.py` — it must pass.

The `specs/` folder is now the durable record. When the plan is actually implemented, the implementation task draws requirements from `specs/`, and any candidate ADRs get promoted into `docs/adr/` in the repo's real format.

</completion>
