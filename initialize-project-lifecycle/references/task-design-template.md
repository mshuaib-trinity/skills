# Task Management System — Design Guide

**Purpose:** Define how tasks are created, tracked, and completed in this repository.
This is the canonical reference for all AI agents and contributors.
The rules in this file are **mandatory and proactive** — no user prompt required to enforce them.

Copy this file verbatim to `tasks/TASK-DESIGN.md` at init.

---

## Classify Work Before Creating a Task

Task tracking records durable, risky, or coordinated work. It is not a receipt for every user request.
Classify the work by semantic impact and durability, not line count.

| Class | Repository task? | Examples |
|---|---|---|
| **Operational** | No | Read-only inspection or diagnosis, status, fetch, pull, branch switching, running an existing test or formatter |
| **Micro** | No | Immediately reversible, behavior-neutral edits such as typos, formatting, or comment cleanup |
| **Tracked standalone** | Yes | Behavior or contract changes, regression fixes, meaningful docs/skills, durable design decisions, coordinated validation |
| **Epic** | Yes | Multiple independently testable slices, dependencies, owners, or multi-session delivery |

### Always-tracked overrides

Create or reuse a task regardless of apparent size when work changes runtime or production behavior,
public APIs, security, data or schemas, provider/framework boundaries, architecture, migrations, or
durable lifecycle and skill rules. A one-line production configuration change can therefore require a
task while a twenty-line formatting cleanup may not.

### Reuse before creating

Read `tasks/ACTIVE.md` first. If the work is already within an active task's goal and acceptance
criteria, attach artifacts and progress there. Do not create a duplicate task or a separate grilling
task for one phase of existing work.

### Record without creating a task

- Standalone read-only reviews and audits may live in `tasks/reviews/`.
- Cross-session continuity with no active task may live in `tasks/handoffs/`.
- Unapproved or out-of-scope findings go to `tasks/backlog/discovered-issues.md`.
- Diagnosis does not authorize remediation; accepted remediation is classified separately.

### Task tracking does not select workflow depth

A task does not automatically require the entire design-to-plan chain:

- Established bug behavior: tracked task + `debug-systematically` + `develop-with-tdd`.
- Straightforward but high-impact change: tracked task + focused implementation and verification.
- New behavior or unresolved trade-offs: `design-before-build`, proportional `stress-test-design`,
  then `write-implementation-plan` when a written plan adds value.
- Design-only work may end after its durable decisions are captured.

If classification remains genuinely ambiguous, prefer the lower-overhead class only when the work is
reversible, behavior-neutral, produces no durable decision, and needs no cross-session coordination.

---

## Two Levels of Work

### Epic
A large initiative with a goal, a PRD, and a set of tasks.

- Lives as a directory in `future/`, `current/`, or `completed/`, named `epic-<slug>/`
- Has a `task.md` header, a `prd.md`, and a `kanban.md`
- Contains a `tasks/` subdirectory holding its work units

### Task (within an Epic)
An independently-testable unit of work inside an epic.

- Lives inside the epic under `tasks/<task-slug>/`
- Has a `task.md` header and any planning artifacts it needs (`design.md`, `plan.md`)
- Must have a `test_criteria` field — if you cannot test it independently, it is too large

### Standalone
A meaningful change with no parent epic.

- Lives directly in `future/`, `current/`, or `completed/`, named `task-<slug>/`
- Has a `task.md` header only (no `kanban.md`, no sub-tasks)
- Distinguished by `type: standalone`

---

## Task Directories Are Containers for Planning Artifacts

A task or epic directory holds **everything** about that work — not just the header.
This is where PRDs, designs, and plans live. PRDs are always task- or epic-specific.

```
tasks/current/epic-<slug>/
├── task.md          # epic header (required)
├── prd.md           # product requirements for the epic (required for epics)
├── kanban.md        # task board (required for epics)
└── tasks/
    └── task-1-<slug>/
        ├── task.md       # task header (required)
        ├── plan.md       # implementation plan (optional)
        └── design.md  # output of a design-before-build session (optional)
```

When a design or grilling session is classified as tracked, create or reuse the task before writing
its first durable artifact. Disposable ideation that produces no accepted design may remain in the
conversation. The session becomes tracked work when its decisions are intended to guide future work.

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

## prd.md — Epic Product Requirements

Every epic has a `prd.md` in its directory. Keep it under one page. If it grows past
one page, the epic is too big — split it.

```markdown
# PRD: <Epic Name>

## Goal
What does completing this epic achieve? One paragraph.
Write from the perspective of value delivered, not tasks completed.

Good: "Users can log in with email/password and stay authenticated across sessions."
Bad:  "Implement authentication endpoint and session management."

## Requirements
- [Specific, testable requirement]
- [Specific, testable requirement]
- (each requirement maps to one or more tasks)

## Out of Scope
- [Explicit non-goal — prevents scope creep]
- [Explicit non-goal]
```

### What makes a good requirement
Each requirement must be **specific**, **testable**, **atomic**, and **in scope**.

| ❌ Bad requirement | ✅ Good requirement |
|---|---|
| Make the system faster | API p95 latency < 200ms measured with k6 |
| Add authentication | Email/password login returns a JWT; invalid creds return 401 |
| Fix the UI | Login form shows an inline error for invalid email format |
| Handle errors properly | All API errors return `{error: string, code: string}` |

### What makes good Out of Scope
Out of Scope prevents silent scope creep. Include things that someone might reasonably
assume are included, are deliberately deferred, or would change the effort significantly.

```markdown
## Out of Scope
- OAuth / social login (deferred to separate epic)
- Password reset flow (separate epic)
- Rate limiting on login endpoint (tracked in backlog)
```

> **Product direction vs feature scope:** the project's overall direction lives in
> `docs/VISION.md`, written once. Per-epic feature scope lives in the epic's `prd.md`.
> Never put feature requirements in VISION.md, and never restate the vision in a PRD.

---

## Completion Checklist {#completion-checklist}

Every task must pass all applicable steps before `status: completed` is set.
Run this before closing any task — no exceptions, no reminders needed.

**Seven mandatory updates:**

- [ ] 1. `task.md` — set `status: completed`
- [ ] 2. `kanban.md` — update row to ✅ completed (epics only)
- [ ] 3. `tasks/ACTIVE.md` — move task out of In Progress; update Up Next
- [ ] 4. `tasks/STATUS.md` — update the Last updated line + the row
- [ ] 5. `docs/` — update every file affected by the code change
         (Doc Trigger Table → [`docs/NAVIGATION.md`](../docs/NAVIGATION.md))
- [ ] 6. Run `review-code-changes` for features, behavior changes, refactors, and
         substantial docs/skill changes
- [ ] 7. Run `verify-before-completion` before claiming the work is complete

**Folder moves (mandatory, immediate — no deferral):**
- Completed task → `tasks/completed/`
- Completed epic (all tasks done) → `tasks/completed/`
- New epic starting → move from `tasks/future/` to `tasks/current/`

**For architectural changes (additional):**
- [ ] 8. Write an ADR in `docs/adr/` if an architectural decision was made
- [ ] 9. Update root agent instructions if any rule or contract changed. In `claude+agents`
         setups, update `CLAUDE.md` and `AGENTS.md` identically.

**Run before closing:**
```bash
python3 scripts/validate-project.py
```

> Work is not complete until all applicable items are checked and the validation script passes.

---

## Lifecycle Rules

1. Create new tasks in `future/` first.
2. Move to `current/` and update `ACTIVE.md` when work begins.
3. A task with unresolved dependencies stays in `current/` with `status: blocked`.
4. Move to `completed/` only after `test_criteria` passes.
5. Out-of-scope discoveries go to `backlog/discovered-issues.md` or become a new
   standalone — never absorbed silently into the running task.
6. Spawned tasks reference their origin: `summary: "Fix X found during epic-Y task-2"`.
7. Mechanical Git operations never trigger `finish-development-branch`; that skill closes already
   tracked implementation work.

---

## Skill Workflow Rules

The skill system is part of the task lifecycle, not an optional helper.

| Situation | Required skill |
|---|---|
| Start any task or decide what process applies | `route-skills` |
| New behavior, workflow changes, architecture changes, unclear requirements | `design-before-build` |
| Non-trivial design, plan, or architecture idea needs challenge | `stress-test-design` |
| Approved design needs ordered implementation work | `write-implementation-plan` |
| Written plan needs execution | `execute-implementation-plan` |
| Feature or bugfix where a focused failing test can be written | `develop-with-tdd` |
| Bug, failing test, or unexpected behavior | `debug-systematically` |
| Refactor, deepening, coupling reduction, or testability improvement | `improve-architecture` |
| Implemented work is ready for review or review feedback arrives | `review-code-changes` |
| About to claim complete, fixed, passing, ready, or mergeable | `verify-before-completion` |
| Task/branch/PR closure | `finish-development-branch` |

Design, plan, stress-test, review, and handoff artifacts for tracked work must live in the relevant
task directory. Standalone read-only review records may live in `tasks/reviews/`, and a handoff with
no active task may live in `tasks/handoffs/`. Skills must not write a parallel planning history
outside `tasks/`.

---

## Task Design Principles

### The One-Sentence Test
If you cannot describe the change in one sentence, the task is too large.

### Independent Testability
Each task delivers a working, testable artifact. Do not cut tasks in horizontal layers
where nothing is verifiable until the last one.

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

## The Three Dashboards

The task system keeps three living files at `tasks/` root. They must always reflect reality.

### ACTIVE.md — what is happening now
The single source of truth for in-flight work. Update when a task moves to `current/`,
changes state, or completes.

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

### STATUS.md — current-state ledger
The compact dashboard for current work and recent completions. The Last updated line changes
on every state change. Historical detail belongs in each task's folder under `tasks/completed/`,
not in a giant dashboard paragraph.

```markdown
# Task Status Dashboard

**Last updated:** YYYY-MM-DD — <what changed>

## Current Work
| Task | Type | Summary | State | Folder |
|------|------|---------|-------|--------|
| task-example | Standalone | Short summary | In Progress | tasks/current/task-example |

## Recently Completed
| Task | Type | Summary | State | Folder |
|------|------|---------|-------|--------|
| task-previous | Standalone | Short summary | Completed | tasks/completed/task-previous |

Historical task details live in `tasks/completed/`. Keep this dashboard focused on current
state and the most recent completed work only.
```

### NAVIGATION.md — the map
Explains the directory roles and the lifecycle. Rarely changes after init.

---

## tasks/reviews/ — Review & Audit Records

`tasks/reviews/` holds point-in-time review documents: architecture reviews, code-cleanup
audits, schema reviews. They are dated, read-only records — not tasks. Name them
`<topic>-review-YYYY-MM-DD.md`. A review may spawn tasks (in `future/`) or backlog entries;
link them from the review so the trail is traceable.

---

## Migration Note

Tasks in `completed/` that predate this system retain their original structure.
The new format applies to all work going forward.
