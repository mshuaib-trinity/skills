---
name: author-skills
description: Use when creating, editing, renaming, testing, or validating agent skills, SKILL.md frontmatter, descriptions, references, scripts, or pressure scenarios.
---

# Author Skills

Author skills with evaluation-driven development. A skill is deployed process behavior, so observe the
failure before changing the instructions.

**REQUIRED BACKGROUND:** Use `develop-with-tdd` for the RED-GREEN-REFACTOR model.

## Core Rules

1. **No skill change without a failing or gap-revealing baseline.**
   - New skill: run representative behavior without the skill.
   - Existing skill: run scenarios against the unmodified current version.
2. Make the smallest instruction change that addresses observed failures.
3. Re-run the same scenarios, capture new rationalizations, and close loopholes.
4. Do not move to another skill until the edited skill passes locally.
5. For a cross-skill contract, run an end-to-end suite after every participant passes locally.
6. Commit, push, or publish only when the user authorized those Git actions.

Read [testing-skills-with-subagents.md](references/testing-skills-with-subagents.md) before editing or
deploying. It owns scenario construction, combined pressure, rationalization capture, meta-testing,
and pass criteria.

## What Belongs in a Skill

Create or extend a skill for reusable techniques, patterns, workflows, or reference knowledge.
Project-specific facts and invariants belong in root instructions or repository docs. Deterministic
mechanical constraints belong in scripts or validators.

| Skill type | Evaluation |
|---|---|
| Discipline | Combined-pressure compliance and rationalization resistance |
| Technique | Application, variation, and missing-information scenarios |
| Pattern | Recognition, application, and counter-examples |
| Reference | Retrieval, application, and common-use gap tests |

## Directory Contract

```text
skill-name/
├── SKILL.md
├── references/
└── scripts/
```

- `SKILL.md` is the only file at the skill root.
- Put non-executable guides, prompts, templates, examples, and fixtures under `references/`.
- Put executable helpers under `scripts/`.
- Keep references one level deep from `SKILL.md`; avoid reference-to-reference routing.
- Use lowercase kebab-case directories and support filenames. `SKILL.md` is the only uppercase exception.
- Reuse assets and scripts instead of retyping large content.

## Frontmatter and Discovery

Required frontmatter:

```yaml
---
name: skill-name
description: Use when <specific triggering conditions, symptoms, or request types>.
---
```

- `name`: letters, numbers, and hyphens; 64 characters maximum.
- `description`: third person, 1024 characters maximum, preferably under 500.
- Start the description with “Use when”.
- Describe only when to load the skill. Do not summarize its process; agents may execute the summary
  without reading the body.
- Include concrete trigger vocabulary users and agents will search for.

Good:

```yaml
description: Use when tests have race conditions, timing dependencies, or inconsistent results.
```

Bad:

```yaml
description: Use for async tests by replacing sleeps with polling and then re-running the suite.
```

The bad description leaks workflow and becomes a shortcut.

## Progressive Disclosure

Assume the agent is capable. Keep only the operating interface and critical decision rules in
`SKILL.md`; move detailed methods and examples into references.

Targets:

- Frequently loaded routing skills: as short as the behavior permits.
- Other skills: aim for under 500 words; exceed only when the main workflow genuinely requires it.
- `SKILL.md` body: always under 500 lines.

For complete authoring guidance on degrees of freedom, workflows, scripts, validation loops, and
reference organization, read [anthropic-best-practices.md](references/anthropic-best-practices.md).

## Evaluation-Driven Workflow

### RED — Observe Current Failure

1. Write at least three representative scenarios. Discipline skills combine three or more pressures.
2. Run them against:
   - no skill, when creating a new skill;
   - the unmodified current skill, when editing.
3. Record exact choices, missed steps, exploration paths, and rationalizations.
4. Define explicit PASS/FAIL criteria before editing.

### GREEN — Make the Minimal Change

1. Address observed failures, not hypothetical ones.
2. Use the right degree of freedom:
   - low for fragile operations;
   - medium for preferred patterns with controlled variation;
   - high for contextual judgment.
3. Keep terminology consistent.
4. Prefer one strong example over several shallow examples.
5. Run the same scenarios and verify the original failure is gone.

### REFACTOR — Close Loopholes

1. Capture new rationalizations verbatim.
2. Add the smallest explicit counter, decision rule, or red flag.
3. Re-run original and new scenarios.
4. Stop when the agent complies under expected pressure and no new high-confidence loophole remains.

## Quality Gate

Before deployment:

- [ ] Baseline behavior was observed before editing
- [ ] Name and trigger-only description are valid
- [ ] Instructions address observed failures
- [ ] GREEN and REFACTOR scenarios pass
- [ ] Main file is concise and support files follow the directory contract
- [ ] Every local link resolves and references are one level deep
- [ ] Scripts handle errors and expose actionable validation output
- [ ] No unauthorized external, commit, push, or publish action is embedded
- [ ] Repository-specific docs and validators are updated when the skill contract changes

If repository instructions require mirrored skill libraries:

1. Read the root parity rule.
2. Synchronize the finalized canonical skill.
3. Run the concrete parity command, for example:
   `diff -qr .agents/skills .claude/skills`.
4. Treat any difference as a failed deployment gate.

## Common Failures

| Failure | Correction |
|---|---|
| Editing before a baseline | Restore current behavior and run RED first |
| Testing an edit “without skill” | Test the unmodified current skill |
| Academic-only evaluation | Use realistic application or pressure scenarios |
| Description summarizes steps | Keep only triggers in frontmatter |
| Heavy detail remains in main | Move it to a directly linked reference |
| Support files at skill root | Move them under `references/` or `scripts/` |
| Batch-editing skills without local GREEN | Verify each skill before the next |
| Trusting an agent success report | Inspect diffs and run evaluations yourself |
| Mirrored directories differ | Synchronize and re-run the parity command |

## Final Rule

No observed baseline, no skill change. No fresh GREEN evidence, no deployment claim.
