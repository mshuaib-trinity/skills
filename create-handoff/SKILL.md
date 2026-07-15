---
name: create-handoff
description: Use when the user asks for a handoff, wants to resume in a new session, needs in-flight work packaged for another agent, or wants a durable continuation note.
argument-hint: "What will the next session focus on?"
---

# Create Handoff

<what-to-do>

Write a handoff document that lets a fresh agent continue this work without re-deriving context. Capture **in-flight state** — where we are mid-work and how to resume — which is exactly what `STATUS.md` (completed-task ledger) and `specs/` (resolved grilling decisions) do not record.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, `specs/`, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information — API keys, passwords, tokens, PII. This file is committed to the repo, so redaction matters.

If the user passed an argument, treat it as the focus of the next session and tailor the "What's next" section to it.

</what-to-do>

<where-to-save>

## Pick the location (hybrid)

1. **The conversation maps to one active task in `tasks/current/`** → write `tasks/current/<task-slug>/handoff.md`. One live handoff per task — **overwrite** it if it already exists. It travels to `tasks/completed/` with the task as part of its record.

2. **No single task** (exploration, no task yet, or the conversation spans several tasks) → write `tasks/handoffs/<YYYY-MM-DD>-<topic-slug>.md`. Create the `tasks/handoffs/` directory lazily if it does not exist.

A central handoff is a continuity record, not a reason to create a repository task.

To decide: read `tasks/ACTIVE.md`. If this conversation clearly belongs to one active task, use (1).
Otherwise use (2). Ask only when choosing the wrong task would materially misroute the continuation.

## Drop a resume pointer

After writing the handoff, add or update a single pointer line at the top of `tasks/ACTIVE.md`, just under the `_Updated:_` line:

```
▶ Resume: <actual-handoff-path> — <one-line focus>
```

Use the exact path written above—either the active task path or `tasks/handoffs/...`. Keep only the
most recent pointer; replace any existing `▶ Resume:` line.

Neither location is scanned by `scripts/validate-project.py`, so handoffs never affect validation.

</where-to-save>

<document-format>

Use the fixed template in [handoff-template.md](references/handoff-template.md). Fill every section; if a section is genuinely empty, write `_None._` rather than deleting it. Keep it tight — link, don't restate.

</document-format>

<suggested-skills>

Every handoff ends with a "Suggested skills" section pointing the next agent at the right tool. Tailor it to what's left to do. Options in this repo:

- **`design-before-build`** — if the next step is turning a still-fuzzy idea into an approved design before any code.
- **`stress-test-design`** — if requirements or the design are fuzzy and need stress-testing. It captures decisions into the task's `specs/`.
- **`write-implementation-plan`** — if the design is settled and the next step is a task-by-task implementation plan (written into the task tree).
- **`execute-implementation-plan`** — if a plan exists and the next step is executing it (it picks subagent-per-task / parallel / inline mode).
- **`finish-development-branch`** — if implementation is done and the next step is closing the task (completion checklist + validator) and merging/PR.
- **`improve-architecture`** — if the next step is refactoring, consolidating modules, or reducing coupling.
- **`initialize-project-lifecycle`** — only for initializing a brand-new project (not for this repo's ongoing work).
- General process skills (`debug-systematically`, `develop-with-tdd`, `verify-before-completion`, `review-code-changes`) when the next step is debugging, implementing, verifying, or reviewing.

Only suggest skills that genuinely fit the next step — do not list all of them.

</suggested-skills>

<staleness>

- **Per-task `handoff.md`:** one live file, overwritten on each new handoff. It is archived with the task when it moves to `tasks/completed/`. No manual cleanup needed.
- **Central `tasks/handoffs/` docs:** dated. Delete a dated handoff once its work has resumed and finished, so the directory reflects only live or recent continuity points.
- Always replace the `▶ Resume:` pointer in `ACTIVE.md` rather than stacking multiple.

</staleness>
