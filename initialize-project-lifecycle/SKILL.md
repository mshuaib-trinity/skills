---
name: initialize-project-lifecycle
description: Use when starting a brand-new software project that needs task management, documentation, ADRs, validation, and root agent instruction files.
---

# Initialize Project Lifecycle

Initialize any new software project with a complete, self-enforcing lifecycle system. After
running this skill, the project has everything needed for AI agents and developers to work
without losing context.

**Core principle:** The scaffold is generated once. After init, the root agent instruction file
(`AGENTS.md`, and optionally mirrored `CLAUDE.md`) is self-contained — AI agents need only read
it to know the operating rules. The skill disappears from the workflow.

Every file this skill writes is sourced from this skill's own `references/` directory, so init
works in any repository on any machine.

## What Gets Created

There are two setup modes:

| Mode | Creates | Mirror rule |
|---|---|---|
| `claude+agents` | `.claude/`, `.agents/`, `CLAUDE.md`, `AGENTS.md` | Yes. `CLAUDE.md` and `AGENTS.md` must be exact mirrors. |
| `agents-only` | `.agents/`, `AGENTS.md` | No. Do not create `.claude/`, `CLAUDE.md`, or mirror rules. |

```
<project-root>/
├── .agents/                    (always)
├── .claude/                    (claude+agents mode only)
│   └── settings.local.json     (empty, gitignored, claude+agents mode only)
├── tasks/
│   ├── ACTIVE.md               (living state of repo)
│   ├── STATUS.md               (master ledger)
│   ├── NAVIGATION.md           (task system guide)
│   ├── TASK-DESIGN.md          (full lifecycle spec — from reference)
│   ├── current/
│   ├── future/
│   ├── completed/
│   ├── reviews/                (dated review/audit records)
│   └── backlog/
│       └── discovered-issues.md
├── docs/
│   ├── NAVIGATION.md           (doc index + Doc Trigger Table)
│   ├── VISION.md               (template — fill in)
│   ├── OVERVIEW.md             (template — fill in)
│   ├── reference/
│   │   ├── code-conventions.md (fill in per tech stack)
│   │   ├── environment.md      (env var reference)
│   │   └── known-gaps.md       (starts empty)
│   └── adr/
│       └── FORMAT.md           (ADR format — from reference)
├── scripts/
│   └── validate-project.py     (structural validation — from reference)
├── AGENTS.md                   (always)
└── CLAUDE.md                   (claude+agents mode only; exact mirror of AGENTS.md)
```

> **PRDs are task- and epic-specific.** A PRD lives *inside* its epic directory
> (`epic-<slug>/prd.md`). Planning, design-before-build, and grilling sessions each create a task and
> write their artifacts into that task's directory. See
> [task-design-template.md](references/task-design-template.md).

## Step 1 — Interview

Ask these 7 questions before creating any files. Do not proceed without answers.

```
1. Setup mode?
   - claude+agents: create both .claude/.agents and mirrored CLAUDE.md/AGENTS.md
   - agents-only: create .agents and AGENTS.md only; no Claude files or mirror rules

2. Project name?
   (e.g. "InsightAI Platform — Sakila Analytics")

3. One-sentence domain description?
   (e.g. "Natural language → SQL → visualization → narrative insights")

4. Tech stack summary?
   (e.g. "FastAPI + React + PostgreSQL 16")

5. Primary language? (Python / TypeScript / Go / other)

6. Brief architecture note? (2-3 sentences)
   (e.g. "Multi-agent backend, React frontend, two databases")

7. Restricted files or operations? (comma-separated, or "none")
   (e.g. "production env vars, auth config, database migration scripts")
```

## Step 2 — Create Directory Scaffold

```bash
mkdir -p tasks/current tasks/future tasks/completed tasks/reviews tasks/backlog
mkdir -p docs/adr docs/reference
mkdir -p scripts .agents
# claude+agents mode only:
mkdir -p .claude
```

## Step 3 — Generate Root Agent Instructions

Pick the template from Q1:

| Mode | Template |
|---|---|
| `claude+agents` | [root-instructions-claude-agents-template.md](references/root-instructions-claude-agents-template.md) |
| `agents-only` | [root-instructions-agents-only-template.md](references/root-instructions-agents-only-template.md) |

Read the template's "How to apply" header before writing. The behavior differs depending on
whether the target instruction file already exists.

Replace every `{{PLACEHOLDER}}` with answers from the interview:
- `{{PROJECT_NAME}}` → Q2
- `{{DOMAIN_DESCRIPTION}}` → Q3
- `{{PRIMARY_LANGUAGE}}` → Q5
- `{{TECH_STACK}}` → Q4
- `{{ARCHITECTURE_NOTE}}` → Q6
- `{{RESTRICTED_FILES}}` → Q7
- `{{SETUP_COMMANDS}}` → project-specific setup/run commands

**claude+agents mode:**
- If `CLAUDE.md` / `AGENTS.md` do not exist, write the filled mirror template to both.
- If they already exist, merge the lifecycle block into both, reconcile duplicated task rules,
  and keep the stricter rule.
- Ensure the two files are identical:
  ```bash
  cp AGENTS.md CLAUDE.md
  diff AGENTS.md CLAUDE.md   # must produce no output
  ```

**agents-only mode:**
- Write or merge the filled agents-only template into `AGENTS.md`.
- Do not create `CLAUDE.md`.
- Do not create mirror rules.
- If a stale `CLAUDE.md` exists only because of a prior attempted init, ask before deleting it.

## Step 4 — Create Management & Doc Files

**tasks/ACTIVE.md:**
```markdown
# Active Work
_Updated: {{DATE}}_

## In Progress
_None._

## Up Next (Ready to Start)
_None._

## Recently Completed
_None._
```

**tasks/STATUS.md:**
```markdown
# Task Status Dashboard

**Last updated:** {{DATE}} — project initialized

## Current Work
_None._

## Recently Completed
_None._

Historical task details live in `tasks/completed/`. Keep this dashboard focused on current
state and the most recent completed work only.
```

**tasks/NAVIGATION.md:**
```markdown
# Task System Navigation

How the task system works: [tasks/TASK-DESIGN.md](TASK-DESIGN.md)
Active work: [tasks/ACTIVE.md](ACTIVE.md)
All task status: [tasks/STATUS.md](STATUS.md)

## Directory Roles

| Directory | Contains | Edit when |
|---|---|---|
| `tasks/future/` | Planned but not started | Planning new work |
| `tasks/current/` | Actively in progress | Starting work |
| `tasks/completed/` | Done and verified | Closing tasks |
| `tasks/reviews/` | Dated review/audit records | After a review session |
| `tasks/backlog/` | Discovered issues, not yet tasked | Finding scope creep |

## Lifecycle
future/ → current/ → completed/
```

**tasks/backlog/discovered-issues.md:**
```markdown
# Discovered Issues Backlog

Issues found during work that were out of scope for the running task.

## Format

**[Issue title] — discovered YYYY-MM-DD**
- **Symptom:** what the user/developer sees
- **Root cause:** technical explanation
- **Fix:** resolution applied, or "Open"
- **Status:** ✅ Fixed | 🔴 Open
```

**docs/NAVIGATION.md** — the documentation index and the **canonical Doc Trigger Table**.
Root agent instructions link here; keep them in sync.
```markdown
# Documentation Navigation

| Goal | Read |
|---|---|
| Understand the system | [`OVERVIEW.md`](OVERVIEW.md) |
| Understand why decisions were made | [`VISION.md`](VISION.md), [`adr/`](adr/FORMAT.md) |
| Code style and conventions | [`reference/code-conventions.md`](reference/code-conventions.md) |
| Environment variables | [`reference/environment.md`](reference/environment.md) |
| Known issues and gaps | [`reference/known-gaps.md`](reference/known-gaps.md) |

## Doc Trigger Table

The moment code changes, update the matching docs in the **same change**.

| Code change | Docs to update |
|---|---|
| New module / component added | `OVERVIEW.md`, relevant deep-dive, root agent instructions if the operating contract changed |
| Behavior of existing component changed | `OVERVIEW.md`, relevant deep-dive |
| New env variable | `reference/environment.md` |
| Architectural decision | `adr/` (new ADR, append-only) |
| New gotcha or constraint | root agent instructions only if it belongs in the operating contract |
| New rule or contract | root agent instructions (mirror in `claude+agents` mode) |
```

**docs/VISION.md** — section headers only; the owner fills in content.
See [vision-guide.md](references/vision-guide.md) for the full writing guide.
```markdown
# Vision

## What This Platform Is

## What It Is Not

## Core Thesis

## Architecture Layers

## Governing Design Principles

## Target State (What "Good" Looks Like)
```

**docs/OVERVIEW.md:**
```markdown
# System Overview

## Architecture

## Execution Flow

## Directory Structure

## Key Contracts
```

**docs/reference/environment.md:**
```markdown
# Environment Variables

Full reference for every variable the project reads.

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| _(none yet)_ | | | |
```

**docs/reference/known-gaps.md:**
```markdown
# Known Gaps

Issues known but not yet addressed. Update as gaps are found or closed.

| Gap | Impact | Status |
|-----|--------|--------|
| _(none at init)_ | | |
```

## Step 5 — Copy Shared Spec Files (from this skill)

These files are identical across all projects. Copy them verbatim from this skill's
`references/` directory — substitute the skill's absolute path for `<skill-dir>`:

```bash
cp <skill-dir>/references/task-design-template.md   tasks/TASK-DESIGN.md
cp <skill-dir>/references/adr-format-template.md     docs/adr/FORMAT.md
cp <skill-dir>/references/validate-project.py        scripts/validate-project.py
chmod +x scripts/validate-project.py
```

`<skill-dir>` is the directory containing this `SKILL.md`
(e.g. `.agents/skills/initialize-project-lifecycle`). Use the Read tool on each reference file and
write the content if `cp` is not convenient.

## Step 6 — Create docs/reference/code-conventions.md

Create `docs/reference/code-conventions.md` with a stub for the tech stack:

```markdown
# Code Conventions

## Language: {{PRIMARY_LANGUAGE}}

[Fill in project-specific conventions: imports, logging, error handling, testing patterns]

## General Rules
- No commented-out code
- All functions have type hints / JSDoc
- Logging over print/console.log
- Errors handled at boundaries, not swallowed
```

## Step 7 — Verify

```bash
python scripts/validate-project.py
```

Expected: `✅ Project structure valid (<project-name>)`

The validator checks: epics have `prd.md` + `kanban.md`; every task has `test_criteria`;
`ACTIVE.md`, `STATUS.md`, `TASK-DESIGN.md`, `docs/NAVIGATION.md`, `docs/adr/FORMAT.md` exist;
`AGENTS.md` exists; and, only when `CLAUDE.md` exists, that `CLAUDE.md == AGENTS.md`.
At init no epics exist yet, so it should pass cleanly.

```bash
# claude+agents mode only:
diff AGENTS.md CLAUDE.md   # must produce no output
```

## Step 8 — Initial Commit

```bash
git add .
git commit -m "chore: initialize project lifecycle system"
```

## Post-Init Checklist

- [ ] Setup mode recorded in the generated root instructions
- [ ] `AGENTS.md` exists
- [ ] `CLAUDE.md` exists only in `claude+agents` mode
- [ ] `CLAUDE.md` and `AGENTS.md` are identical in `claude+agents` mode (`diff` produces no output)
- [ ] All `{{PLACEHOLDER}}` values replaced in root agent instructions
- [ ] Restricted files/operations are listed or explicitly set to `none`
- [ ] `docs/NAVIGATION.md` exists with the Doc Trigger Table
- [ ] `tasks/reviews/` exists
- [ ] `python scripts/validate-project.py` exits 0
- [ ] Initial commit made

## What to Do Next

1. Fill in `docs/VISION.md` — the most important document in the repo ([guide](references/vision-guide.md))
2. Fill in `docs/OVERVIEW.md` with architecture details
3. Fill in `docs/reference/code-conventions.md` with project-specific conventions
4. Create the first task in `tasks/future/` before writing any code
5. Read `tasks/TASK-DESIGN.md` for full task lifecycle rules and PRD format
6. Use the task-rooted skill workflow for all meaningful work:
   `route-skills` chooses the process; `design-before-build` and `stress-test-design`
   capture design context inside the task; `write-implementation-plan` and
   `execute-implementation-plan` carry out the work; `review-code-changes` and
   `verify-before-completion` gate closure; `finish-development-branch` runs the
   Completion Checklist and project validator.
