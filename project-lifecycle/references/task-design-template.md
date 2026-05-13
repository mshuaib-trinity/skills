# Task Management System — Design Guide

**Purpose:** Define how tasks are created, tracked, and completed in this repository.
This is the canonical reference for all AI agents and contributors.
The rules in this file are **mandatory and proactive** — no user prompt required to enforce them.

---

## What Requires a Task Entry

- **Always create a task:** meaningful changes to logic, structure, or behaviour; anything explicitly requested by the user
- **No task needed:** trivial mechanical edits (typo fixes, version number bumps, single-line config changes)

When in doubt: if the change could break something or requires thought, create a task.

---

## Two Levels of Work

### Epic
A large initiative with a goal, PRD, and a set of tasks.

- Lives as a directory in `future/`, `current/`, or `completed/`
- Has a `task.md` header, `prd.md`, and `kanban.md`
- Contains a `tasks/` subdirectory with its work units

### Task (within an Epic)
An independently-testable unit of work inside an epic.

- Lives inside the epic under `tasks/<task-slug>/`
- Has a `task.md` header and optional `plan.md`
- Must have a `test_criteria` field — if you cannot test it independently, it is too large

### Standalone
A meaningful change with no parent epic.

- Lives directly in `future/`, `current/`, or `completed/`
- Has a `task.md` header only (no `kanban.md`, no sub-tasks)
- Distinguished by `type: standalone`

---

## File Formats

### task.md — Epic Header
```yaml
---
id: epic-<slug>
type: epic
status: planned | in_progress | completed
summary: one-line description of the initiative
goal: what does completing this epic achieve?
created: YYYY-MM-DD
---
```

### task.md — Task within Epic
```yaml
---
id: task-<n>-<slug>
type: task
epic: epic-<parent-slug>
status: planned | in_progress | blocked | completed
summary: one-line description of the work
depends_on: [task-id-1, task-id-2]   # or []
blocked_by: task-id | external description | ~
test_criteria: one sentence — what proves this task is done?
created: YYYY-MM-DD
---
```

### task.md — Standalone
```yaml
---
id: task-<slug>
type: standalone
status: planned | in_progress | blocked | completed
summary: one-line description
depends_on: []
blocked_by: ~
test_criteria: one sentence — what proves this task is done?
created: YYYY-MM-DD
---
```

### prd.md — Epic Product Requirements
```markdown
# PRD: <Epic Name>

## Goal
What does completing this epic achieve? One paragraph.

## Requirements
- Specific, testable requirement 1
- Specific, testable requirement 2
- (each requirement maps to one or more tasks)

## Out of Scope
- Explicit non-goal 1 (prevents scope creep)
- Explicit non-goal 2
```

### kanban.md — Epic Task Board
```markdown
# Epic: <slug> — Kanban

| # | Task | Status | Depends On | Test Criteria |
|---|------|--------|------------|---------------|
| 1 | task-1-slug | ⬜ planned | — | one-sentence verification |
| 2 | task-2-slug | ⬜ planned | 1 | one-sentence verification |

## Dependency Flow
[Describe which tasks are parallel and which are sequential]
```

**Status icons:** ⬜ planned | 🔄 in_progress | 🚧 blocked | ✅ completed

---

## Completion Checklist {#completion-checklist}

Every task must pass all applicable steps before `status: completed` is set.
Run this before closing any task — no exceptions, no reminders needed.

**Five mandatory updates:**

- [ ] 1. `task.md` — set `status: completed`
- [ ] 2. `kanban.md` — update row to ✅ completed (epics only)
- [ ] 3. `tasks/ACTIVE.md` — move task out of In Progress; update Up Next
- [ ] 4. `tasks/STATUS.md` — update Last updated line
- [ ] 5. `docs/` — update every file affected by the code change
         Trigger table → [`docs/NAVIGATION.md`](../docs/NAVIGATION.md)

**Folder moves (mandatory, immediate — no deferral):**
- Completed task → `tasks/completed/`
- Completed epic (all tasks done) → `tasks/completed/`
- New epic starting → move from `tasks/future/` to `tasks/current/`

**For architectural changes (additional):**
- [ ] 6. Write ADR in `docs/adr/` if an architectural decision was made
- [ ] 7. Update `CLAUDE.md` and `AGENTS.md` identically if any rule or contract changed

**Run before closing:**
```bash
python scripts/validate-project.py
```

> Work is not complete until all applicable items are checked and the validation script passes.

---

## Lifecycle Rules

1. Create tasks in `future/` first.
2. Move to `current/` and update `ACTIVE.md` when work begins.
3. A task with unresolved dependencies stays in `current/` with `status: blocked`.
4. Move to `completed/` only after `test_criteria` passes.
5. Out-of-scope discoveries go to `backlog/discovered-issues.md` or become a new standalone — never absorbed silently into the running task.
6. Spawned tasks reference their origin: `summary: "Fix X found during epic-Y task-2"`.

---

## Task Design Principles

### The One-Sentence Test
If you cannot describe the change in one sentence, the task is too large.

### Independent Testability
Each task delivers a working, testable artifact. Do not cut tasks in horizontal layers where nothing is verifiable until the last one.

### One test_criteria per task
If you need multiple independent criteria, split the task.

### Vertical Slices, Not Horizontal Layers

| ❌ Bad (horizontal layers) | ✅ Good (vertical slices) |
|---------------------------|--------------------------|
| task-1: all DB schema changes | task-1: user table + login query + test |
| task-2: all API endpoints | task-2: user endpoint + auth middleware + test |
| task-3: all UI components | task-3: login page + session flow + E2E test |

### Parallel vs Sequential
Tasks that can run in parallel have no dependency between them. Make this explicit in `kanban.md`.

---

## ACTIVE.md Contract

`ACTIVE.md` is the living state of the repository. It must always reflect reality.

Update when:
- A task moves to `current/`
- A task's state changes (planned → in_progress → blocked → completed)
- A task moves to `completed/`

### Format
```markdown
# Active Work
_Updated: YYYY-MM-DD_

## In Progress
| Task | Type | Summary | Current State |
|------|------|---------|---------------|
| epic-example | epic | Short summary | task-2 of 4 — doing X |

## Blocked
| Task | Blocked By | Summary |
|------|------------|---------|
| task-3 | task-2 | Cannot proceed until task-2 is stable |

## Up Next (Ready to Start)
| Task | Type | Depends On |
|------|------|------------|
| epic-next-thing | epic | — |

## Recently Completed
- task-example (YYYY-MM-DD) — one-line description
```

Omit any section that has no entries.

---

## Migration Note

Tasks in `completed/` that predate this system retain their original structure.
The new format applies to all work going forward.
