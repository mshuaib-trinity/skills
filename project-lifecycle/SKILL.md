---
name: project-lifecycle
description: Use when initializing a brand-new software project that needs a complete lifecycle system from scratch — task management, documentation, ADRs, PRDs, validation script, and self-contained AGENTS.md/AGENTS.md. Invoke once per new project. Do NOT use for adding features to an existing project.
---

# Project Lifecycle — Init Skill

Initialize any new software project with a complete, self-enforcing lifecycle system. After running this skill, the project has everything needed for AI agents and developers to work without losing context.

**Core principle:** The scaffold is generated once. After init, AGENTS.md is self-contained — AI agents need only read it to know all the rules. The skill disappears from the workflow.

## What Gets Created

```
<project-root>/
├── .Codex/
│   └── settings.local.json     (empty, gitignored)
├── tasks/
│   ├── ACTIVE.md               (living state of repo)
│   ├── STATUS.md               (master dashboard)
│   ├── NAVIGATION.md           (system guide)
│   ├── TASK-DESIGN.md          (full lifecycle spec — copy from reference)
│   ├── current/
│   ├── future/
│   ├── completed/
│   └── backlog/
│       └── discovered-issues.md
├── docs/
│   ├── NAVIGATION.md           (documentation index)
│   ├── VISION.md               (template — fill in)
│   ├── OVERVIEW.md             (template — fill in)
│   ├── reference/
│   │   ├── code-conventions.md (fill in per tech stack)
│   │   └── known-gaps.md       (starts empty)
│   └── adr/
│       └── FORMAT.md           (ADR format — copy from reference)
├── PRDs/
│   └── FORMAT.md               (PRD format — copy from reference)
├── scripts/
│   └── validate-project.py     (structural validation — copy from reference)
├── AGENTS.md                   (generated from template)
└── AGENTS.md                   (exact mirror of AGENTS.md)
```

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
mkdir -p tasks/current tasks/future tasks/completed tasks/backlog
mkdir -p docs/adr docs/reference
mkdir -p PRDs scripts .Codex
```

## Step 3 — Generate AGENTS.md and AGENTS.md

Use [Codex-md-template.md](Codex-md-template.md) as the source.

Replace all `{{PLACEHOLDER}}` values with answers from the interview:
- `{{PROJECT_NAME}}` → answer to Q1
- `{{DOMAIN_DESCRIPTION}}` → answer to Q2
- `{{TECH_STACK}}` → answer to Q3
- `{{ARCHITECTURE_NOTE}}` → answer to Q5
- `{{SETUP_COMMANDS}}` → fill in project-specific commands
- `{{ENV_VARS_TABLE}}` → fill in env vars or leave as placeholder row

Write the filled template to `AGENTS.md`. Then copy it identically to `AGENTS.md`:
```bash
cp AGENTS.md AGENTS.md
diff AGENTS.md AGENTS.md   # must produce no output
```

## Step 4 — Create Management Files

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

**docs/VISION.md:** Create with section headers only — the project owner fills in content:
```markdown
# Vision

## What This Platform Is

## What It Is Not

## Core Thesis

## Architecture Layers

## Governing Design Principles

## Target State (What "Good" Looks Like)
```

**docs/OVERVIEW.md:** Create with section headers:
```markdown
# System Overview

## Architecture

## Execution Flow

## Directory Structure

## Key Contracts
```

**docs/reference/known-gaps.md:**
```markdown
# Known Gaps

Issues known but not yet addressed. Update as gaps are found or closed.

| Gap | Impact | Status |
|-----|--------|--------|
| _(none at init)_ | | |
```

## Step 5 — Copy Shared Spec Files

These files are identical across all projects. Copy them verbatim from the InsightAI-Platform reference repo:

```bash
# From reference repo root:
cp <reference-repo>/tasks/TASK-DESIGN.md         tasks/TASK-DESIGN.md
cp <reference-repo>/docs/adr/FORMAT.md            docs/adr/FORMAT.md
cp <reference-repo>/PRDs/FORMAT.md                PRDs/FORMAT.md
cp <reference-repo>/scripts/validate-project.py   scripts/validate-project.py
chmod +x scripts/validate-project.py
```

**Reference repo:** `/Users/mohammedaamirshuaib/Documents/MyProjects/InsightAI-Platform`

If the reference repo is not accessible, use the embedded templates at the bottom of [Codex-md-template.md](Codex-md-template.md).

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

If it fails, read the error list and fix. Common issues: missing prd.md/kanban.md on epics (none should exist yet, so this should pass).

Also verify mirrors are identical:
```bash
diff AGENTS.md AGENTS.md   # must produce no output
```

## Step 8 — Initial Commit

```bash
git add .
git commit -m "chore: initialize project lifecycle system — tasks/, docs/adr/, PRDs/, AGENTS.md, validation script"
```

## Post-Init Checklist

- [ ] AGENTS.md and AGENTS.md are identical (`diff` produces no output)
- [ ] All `{{PLACEHOLDER}}` values replaced in AGENTS.md/AGENTS.md
- [ ] `python scripts/validate-project.py` exits 0
- [ ] tasks/VISION.md stub created (owner fills in content)
- [ ] Initial commit made

## What to Do Next

1. Fill in `docs/VISION.md` — this is the most important document in the repo
2. Fill in `docs/OVERVIEW.md` with architecture details
3. Fill in `docs/reference/code-conventions.md` with project-specific conventions
4. Create the first task in `tasks/future/` before writing any code
5. Read `tasks/TASK-DESIGN.md` for full task lifecycle rules
