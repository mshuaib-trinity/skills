# CLAUDE.md Template

Replace every `{{PLACEHOLDER}}` before writing to disk. After filling in, copy identically to AGENTS.md.

---

```markdown
# AI Agent Instructions

This file provides guidance to all AI agents (Gemini, GPT, Codex, Cursor, etc.) when working with code in this repository.

> **MIRROR RULE — NON-NEGOTIABLE:**
> `CLAUDE.md` and `AGENTS.md` are **exact mirrors**. Any change to one **must** be applied to the other **in the same commit** — no exceptions. Claude Code reads `CLAUDE.md`; all other AI agents read `AGENTS.md`.

---

## Read First

Before any work, read in this order:

1. [`docs/VISION.md`](docs/VISION.md) — what this platform is and why every decision was made
2. [`tasks/ACTIVE.md`](tasks/ACTIVE.md) — what is in progress right now
3. [`tasks/TASK-DESIGN.md`](tasks/TASK-DESIGN.md) — full task lifecycle rules and formats

---

## Standing Orders

**These are automatic. No user trigger required. No exceptions.**

**Before any work:**
→ Read `tasks/ACTIVE.md`. If the work is not tracked, create a task in `tasks/future/` first.
→ Do not write any code before the task exists in `tasks/current/`.
→ Full task rules, file formats, and lifecycle: [`tasks/TASK-DESIGN.md`](tasks/TASK-DESIGN.md)

**During any work:**
→ Update `tasks/ACTIVE.md` whenever task state changes.
→ Update the relevant `docs/` file the moment code changes — not after. An undocumented change is an incomplete change.
→ Doc trigger table (what to update when): [`docs/NAVIGATION.md`](docs/NAVIGATION.md)
→ Out-of-scope discoveries → `tasks/backlog/discovered-issues.md` or a new task. Never silently absorbed.
→ Update `kanban.md` immediately when any epic task changes status — do not wait.

**Every architectural decision:**
→ Write an ADR in `docs/adr/` before marking work complete.
→ ADR format and append-only rules: [`docs/adr/FORMAT.md`](docs/adr/FORMAT.md)

**Before marking any task complete:**
→ Run the full completion checklist: [`tasks/TASK-DESIGN.md#completion-checklist`](tasks/TASK-DESIGN.md#completion-checklist)
→ Run `python scripts/validate-project.py` — must pass before closing any task.
→ Confirm in your response that docs, task state, kanban, STATUS.md, and folder moves are all done.

**CLAUDE.md + AGENTS.md:**
→ Always identical mirrors. Update both whenever any rule, architecture, or contract changes.
→ A stale or diverged file is a rule violation — fix it immediately, not deferred.

**Code quality (non-negotiable):**
→ Full conventions: [`docs/reference/code-conventions.md`](docs/reference/code-conventions.md)

---

## Project Overview

| Attribute | Value |
|---|---|
| **Name** | {{PROJECT_NAME}} |
| **Domain** | {{DOMAIN_DESCRIPTION}} |
| **Tech Stack** | {{TECH_STACK}} |

Full architecture: [`docs/OVERVIEW.md`](docs/OVERVIEW.md) | Architecture decisions: [`docs/adr/`](docs/adr/)

---

## Architecture at a Glance

{{ARCHITECTURE_NOTE}}

Full details: [`docs/OVERVIEW.md`](docs/OVERVIEW.md) | Why these decisions: [`docs/adr/`](docs/adr/)

---

## Setup & Commands

```bash
{{SETUP_COMMANDS}}
python scripts/validate-project.py  # validate project structure
```

---

## Environment Variables

| Variable | Required | Notes |
|---|---|---|
| {{ENV_VARS_TABLE}} | | |

---

## Key Guides

| Task | Read This |
|---|---|
| Find any documentation | [`docs/NAVIGATION.md`](docs/NAVIGATION.md) |
| Code style and conventions | [`docs/reference/code-conventions.md`](docs/reference/code-conventions.md) |
| Known issues and gaps | [`docs/reference/known-gaps.md`](docs/reference/known-gaps.md) |
| Write or read an ADR | [`docs/adr/FORMAT.md`](docs/adr/FORMAT.md) |
| Write or read a PRD | [`PRDs/FORMAT.md`](PRDs/FORMAT.md) |
| Task lifecycle rules | [`tasks/TASK-DESIGN.md`](tasks/TASK-DESIGN.md) |
```
