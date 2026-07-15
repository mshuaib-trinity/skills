---
name: initialize-project-lifecycle
description: Use when starting or repairing a software project's task, documentation, ADR, validation, skill, and root-instruction lifecycle scaffold.
---

# Initialize Project Lifecycle

Create a usable lifecycle system from repository evidence. Do not generate empty ceremonial files or ask
the owner to repeat facts that the repository already proves.

## Outcome

A valid project has:

- mode-correct root instructions and installed skills
- proportional task policy and task dashboards
- substantive vision and overview documents
- work-area navigation plus optional component guides
- ADR format and documentation triggers
- a structural validator that checks the scaffold it promises

## 1. Discover Before Interviewing

Inspect, without mutation:

- existing `AGENTS.md`, `CLAUDE.md`, `.agents/`, and `.claude/`
- README, manifests, lockfiles, language/tool configuration, source/test layout
- existing docs, ADRs, tasks, scripts, CI, and setup commands
- current Git state so unrelated changes are preserved

Prepare an evidence table for project name, domain, primary language, stack, architecture, setup/test
commands, setup mode, and restricted operations. Mark each value confirmed, inferred, conflicting, or
unknown.

## 2. Ask Only for Unresolved Inputs

Use one consolidated checkpoint for unknown or conflicting values. A blank repository may require all
of these; an established repository may require none:

- setup mode: `claude+agents` or `agents-only`
- project name and one-sentence domain
- what the product is and is not, its core thesis, governing principles, and target state
- primary language and stack
- short architecture note, current system map, and execution flow
- setup, test, and run commands
- restricted files or operations

Show inferred values and their sources instead of asking open-ended questions. Do not proceed through a
conflict that would overwrite existing operating rules.

## 3. Select the Setup Mode

| Mode | Required output |
|---|---|
| `claude+agents` | `.agents/skills/`, `.claude/skills/`, `AGENTS.md`, `CLAUDE.md`; root files are exact mirrors |
| `agents-only` | `.agents/skills/`, `AGENTS.md`; no `CLAUDE.md`, `.claude/`, or mirror rule |

Use:
- `references/root-instructions-claude-agents-template.md`
- `references/root-instructions-agents-only-template.md`

Merge into existing root instructions; do not overwrite unrelated project-specific invariants. Replace
all placeholders. In mirror mode, write `AGENTS.md`, copy the final content to `CLAUDE.md`, and verify
`diff AGENTS.md CLAUDE.md`.

If `agents-only` is selected while `CLAUDE.md` or `.claude/` already exists, stop and request explicit
approval before deleting or archiving it. Setup-mode selection alone is not deletion authorization.
When existing root rules conflict with the template, preserve both until the owner resolves the
behavioral conflict; do not automatically choose whichever wording sounds stricter.

## 4. Install the Skill Library

The parent of this initializer directory is the skill-library source. Verify it contains every skill
named by the generated root Skill Protocol.

- Copy missing sibling skill directories into `.agents/skills/`.
- Treat an existing `.agents/skills/` version as canonical unless the user explicitly requested a
  skill refresh. When source and installed versions differ, show the material diff and resolve it
  before claiming initialization complete.
- In `claude+agents` mode, mirror the finalized `.agents/skills/` library into `.claude/skills/`.
  Ask before overwriting a differing existing Claude skill.
- Verify shared skill content with `diff -qr .agents/skills .claude/skills` in mirror mode.

Never create empty skill directories while generating root instructions that require unavailable skills.
If the source library is incomplete, stop and report the missing names.

For `claude+agents`, create `.claude/settings.local.json` as `{}` only when absent and ensure that
file is ignored without replacing existing ignore rules.

## 5. Create the Lifecycle Structure

Create missing directories:

```text
tasks/{current,future,completed,reviews,handoffs,backlog}
docs/{adr,reference,components}
scripts/
```

Create or merge:

- `tasks/ACTIVE.md`, `tasks/STATUS.md`, and `tasks/NAVIGATION.md`
- `tasks/backlog/discovered-issues.md`
- `docs/NAVIGATION.md` with a work-area context map and Doc Trigger Table
- `docs/VISION.md` and `docs/OVERVIEW.md`
- `docs/reference/{code-conventions,environment,known-gaps}.md`
- `docs/components/README.md`

Copy the canonical references:

```bash
cp <skill-dir>/references/task-design-template.md tasks/TASK-DESIGN.md
cp <skill-dir>/references/adr-format-template.md docs/adr/FORMAT.md
cp <skill-dir>/references/component-doc-guide.md docs/components/README.md
cp <skill-dir>/references/validate-project.py scripts/validate-project.py
chmod +x scripts/validate-project.py
```

When canonical targets already exist, compare and merge deliberately. Do not replace repository-specific
validator checks.

## 6. Write Substantive Context

`docs/VISION.md` must state what the product is and is not, its core thesis, architecture layers,
governing decision principles, and target state. Use `references/vision-guide.md`.

`docs/OVERVIEW.md` must describe the current system map, execution flow, directory responsibilities,
and key contracts.

`docs/NAVIGATION.md` must route each significant work area to intent/architecture, primary code entry
points, tests, relevant ADRs, and `tasks/ACTIVE.md`.

Create a component guide from `references/component-doc-template.md` only when the selection rubric in
`docs/components/README.md` applies. Do not create one guide per directory.

If repository evidence cannot support meaningful vision or overview content, pause for owner input.
Header-only files, bracketed template prompts, placeholders, `CHANGEME`, `XXX`, and “fill this later”
text are not initialized documentation.

## 7. Verify

Run:

```bash
python3 scripts/validate-project.py
```

In `claude+agents` mode also run:

```bash
diff AGENTS.md CLAUDE.md
diff -qr .agents/skills .claude/skills
```

Fix validation errors and repeat. The validator checks task structure across lifecycle states,
substantive docs, unresolved placeholders, local navigation links, setup-mode consistency, required
skills, and root mirrors.

## 8. Handoff and Optional Commit

Report:

- values inferred from repository evidence
- questions the owner answered
- files created or merged
- existing content preserved
- validation commands and outputs
- any project-specific validator extensions still recommended

Do not commit automatically. Commit only when the user explicitly requested a commit or separately
approved the Git action.

## Red Flags

- Asking a fixed interview before inspecting the repository
- Generating blank vision or overview stubs and declaring success
- Creating empty skill directories
- Overwriting existing instructions, skills, docs, or validator extensions
- Mixing `claude+agents` with `agents-only` paths or mirror rules
- Leaving template placeholders in current documentation
- Treating lifecycle initialization as proof that application behavior works
