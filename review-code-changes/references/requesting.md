# Requesting Code Review

Dispatch a code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted
context for evaluation — never your session's history. This keeps the reviewer focused on the work product,
not your thought process, and preserves your own context for continued work.

**Core principle:** Review early, review often.

## When to Request

**Mandatory:** after each task in subagent-driven execution; after completing a major feature; before merge to main.

**Optional but valuable:** when stuck (fresh perspective); before refactoring (baseline check); after fixing a complex bug.

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code reviewer subagent:** use the Task/Agent tool with `general-purpose` type, filling the
template at `code-reviewer.md` (co-located in this references/ dir).

**Placeholders:**
- `{DESCRIPTION}` — brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` — what it should do (e.g. "Task 2 from tasks/current/epic-deployment/plan.md")
- `{BASE_SHA}` — starting commit
- `{HEAD_SHA}` — ending commit

**3. Act on feedback:** fix Critical immediately; fix Important before proceeding; note Minor for later;
push back if the reviewer is wrong (with reasoning). To act on the feedback itself, see `receiving.md`.

## Integration with Workflows

- **Subagent-driven execution:** review after EACH task; catch issues before they compound.
- **Inline execution:** review after each task or at natural checkpoints.
- **Ad-hoc:** review before merge, or when stuck.

## Red Flags

**Never:** skip review because "it's simple"; ignore Critical issues; proceed with unfixed Important issues;
argue with valid technical feedback.

**If the reviewer is wrong:** push back with technical reasoning; show code/tests that prove it works;
request clarification.
