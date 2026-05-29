---
name: project-lifecycle
description: Use when initializing a brand-new software project that needs a complete lifecycle system from scratch — task management, documentation, ADRs, epic/task PRDs, validation script, and self-contained CLAUDE.md/AGENTS.md. Invoke once per new project. Do NOT use for adding features to an existing project.
---

# Project Lifecycle — Init Skill

Initialize any new software project with a complete, self-enforcing lifecycle system. After
running this skill, the project has everything needed for AI agents and developers to work
without losing context.

**Core principle:** The scaffold is generated once. After init, `CLAUDE.md` is self-contained —
AI agents need only read it to know all the rules. The skill disappears from the workflow.

Every file this skill writes is sourced from this skill's own `references/` directory, so init
works in any repository on any machine.

## What Gets Created

```
<project-root>/
├── .claude/
│   └── settings.local.json     (empty, gitignored)
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
├── CLAUDE.md                   (generated/merged from template)
└── AGENTS.md                   (exact mirror of CLAUDE.md)
```

> **PRDs are task- and epic-specific.** A PRD lives *inside* its epic directory
> (`epic-<slug>/prd.md`). Planning, brainstorming, and grilling sessions each create a task and
> write their artifacts into that task's directory. See
> [task-design-template.md](references/task-design-template.md).

## Step 1 — Interview

Ask these 5 questions before creating any files. Do not proceed without answers.

```
1. Project name?
   (e.g. "InsightAI Platform — Sakila Analytics")

2. One-sentence domain description?
   (e.g. "Natural language → SQL → visualization → narrative insights")

3. Tech stack summary?
   (e.g. "FastAPI + React + PostgreSQL 16")

4. Primary language? (Python / TypeScript / Go / other)

5. Brief architecture note? (2-3 sentences)
   (e.g. "Multi-agent backend, React frontend, two databases")
```

## Step 2 — Create Directory Scaffold

```bash
mkdir -p tasks/current tasks/future tasks/completed tasks/reviews tasks/backlog
mkdir -p docs/adr docs/reference
mkdir -p scripts .claude
```

## Step 3 — Generate (or Merge) CLAUDE.md and AGENTS.md

Source: [claude-md-template.md](references/claude-md-template.md). Read its "How to apply"
header — the behavior differs depending on whether the files already exist.

Replace every `{{PLACEHOLDER}}` with answers from the interview:
- `{{PROJECT_NAME}}` → Q1
- `{{DOMAIN_DESCRIPTION}}` → Q2
- `{{PRIMARY_LANGUAGE}}` → Q4
- `{{TECH_STACK}}` → Q3
- `{{ARCHITECTURE_NOTE}}` → Q5
- `{{SETUP_COMMANDS}}` → project-specific setup/run commands
- `{{ENV_VAR}}` / `{{ENV_VARS_TABLE}}` rows → env vars, or leave a single placeholder row

**If `CLAUDE.md` / `AGENTS.md` do NOT exist:** write the full filled template to both.

**If they already exist:** do NOT overwrite. Prepend the lifecycle block (everything between
the `<!-- LIFECYCLE:BEGIN -->` and `<!-- LIFECYCLE:END -->` markers) to the top of each file,
just under the first H1, leaving existing content intact. Then reconcile any duplicated task
rules — keep the stricter one.

Then ensure the two files are identical:
```bash
cp CLAUDE.md AGENTS.md
diff CLAUDE.md AGENTS.md   # must produce no output
```

## Step 4 — Create Management & Doc Files

**tasks/ACTIVE.md:**
```markdown
# Active Work
_Updated: {{DATE}}_

## In Progress
_(none)_

## Blocked
_(none)_

## Up Next (Ready to Start)
_(none — add first tasks here)_

## Recently Completed
_(none yet)_
```

**tasks/STATUS.md:**
```markdown
# Task Status Dashboard

**Last updated:** {{DATE}} — project initialized

| Task | Type | Summary | State | Folder |
|------|------|---------|-------|--------|
| _(none yet)_ | | | | |
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
CLAUDE.md links here; keep them in sync.
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
| New module / component added | `OVERVIEW.md`, relevant deep-dive, `CLAUDE.md`/`AGENTS.md` |
| Behavior of existing component changed | `OVERVIEW.md`, relevant deep-dive |
| New env variable | `reference/environment.md`, `CLAUDE.md`/`AGENTS.md` |
| Architectural decision | `adr/` (new ADR, append-only) |
| New gotcha or constraint | `CLAUDE.md`/`AGENTS.md` (Known Gotchas) |
| New rule or contract | `CLAUDE.md`/`AGENTS.md` (Critical Rules) — both mirrors |
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

Full reference for every variable the project reads. Mirror the summary table in CLAUDE.md.

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
(e.g. `.claude/skills/project-lifecycle`). Use the Read tool on each reference file and
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
and that `CLAUDE.md` == `AGENTS.md`. At init no epics exist yet, so it should pass cleanly.

```bash
diff CLAUDE.md AGENTS.md   # must produce no output
```

## Step 8 — Initial Commit

```bash
git add .
git commit -m "chore: initialize project lifecycle system — tasks/, docs/, CLAUDE.md, validation script"
```

## Post-Init Checklist

- [ ] CLAUDE.md and AGENTS.md are identical (`diff` produces no output)
- [ ] All `{{PLACEHOLDER}}` values replaced in CLAUDE.md/AGENTS.md
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
