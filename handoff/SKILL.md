---
name: handoff
description: Compact the current conversation into a handoff document so a fresh agent can resume the work. Saves into the task tree (not OS temp) — per-task handoff.md when the conversation maps to one active task, otherwise a dated tasks/handoffs/ doc — and drops a resume pointer in ACTIVE.md. Use when the user says "create a handoff", "/handoff", "hand this off", "I need to continue this in a new session", or wants to package in-flight work for someone to pick up cold.
argument-hint: "What will the next session focus on?"
---

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

To decide: read `tasks/ACTIVE.md`. If exactly one task is In Progress and this conversation is about it, use (1). Otherwise use (2). When in doubt, ask the user which task this continues.

## Drop a resume pointer

After writing the handoff, add or update a single pointer line at the top of `tasks/ACTIVE.md`, just under the `_Updated:_` line:

```
▶ Resume: tasks/current/<task-slug>/handoff.md — <one-line focus>
```

This is how the next session finds the latest handoff instantly. Keep only the most recent pointer; replace any existing `▶ Resume:` line.

Neither location is scanned by `scripts/validate-project.py`, so handoffs never affect validation.

</where-to-save>

<document-format>

Use the fixed template in [handoff-template.md](references/handoff-template.md). Fill every section; if a section is genuinely empty, write `_None._` rather than deleting it. Keep it tight — link, don't restate.

</document-format>

<suggested-skills>

Every handoff ends with a "Suggested skills" section pointing the next agent at the right tool. Tailor it to what's left to do. Options in this repo:

- **`grill-with-docs`** — if requirements or the design are still fuzzy. It spins up a grilling task and captures decisions into `specs/`.
- **`improve-codebase-architecture`** — if the next step is refactoring, consolidating modules, or reducing coupling.
- **`project-lifecycle`** — only for initializing a brand-new project (not for this repo's ongoing work).
- General process skills (`systematic-debugging`, `test-driven-development`, `verification-before-completion`, `requesting-code-review`) when the next step is debugging, implementing, verifying, or reviewing.

Only suggest skills that genuinely fit the next step — do not list all of them.

</suggested-skills>

<staleness>

- **Per-task `handoff.md`:** one live file, overwritten on each new handoff. It is archived with the task when it moves to `tasks/completed/`. No manual cleanup needed.
- **Central `tasks/handoffs/` docs:** dated. Delete a dated handoff once its work has resumed and finished, so the directory reflects only live or recent continuity points.
- Always replace the `▶ Resume:` pointer in `ACTIVE.md` rather than stacking multiple.

</staleness>
