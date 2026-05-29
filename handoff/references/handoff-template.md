# Handoff Template

Fill every section. If one is genuinely empty, write `_None._` — do not delete it. Link to
artifacts (commits, diffs, ADRs, `specs/`, plans) by path or URL; never paste their content.

```md
# Handoff: <topic>

**Date:** YYYY-MM-DD
**Next-session focus:** <from the skill argument, or "open — continue current work">
**Active task(s):** <link(s) to tasks/current/<slug>/ and the ACTIVE.md row(s)>

## Where we are
<Current mid-work state in 2-5 sentences. What is half-done, what is stable, what is the
shape of the work right now. This is the part no other artifact records.>

## What's done this session
- <change + reference: commit hash, file path, or spec section — do not restate the diff>
- ...

## What's next
1. <The exact next step — concrete, not "continue the work">
2. <Commands to run to pick up, e.g. `source .venv/bin/activate && pytest tests/ -q`>
3. ...

## Key decisions
<Reference where each decision lives — docs/adr/ADR-NNN-*.md, a task's specs/decisions.md,
or specs/candidate-adrs.md. One line each, link don't restate.>

## Open questions / blockers
- <Unresolved question, and what's needed to resolve it> | _None._

## Gotchas
- <Anything that will bite the next agent: a flaky step, a non-obvious constraint, a
  workaround in place> | _None._

## Suggested skills
- <skill> — <why it fits the next step>
```

## Notes

- **Redaction:** strip API keys, passwords, tokens, and PII before saving. This file is committed.
- **One live per-task handoff:** if `tasks/current/<task>/handoff.md` already exists, overwrite it.
- **Resume pointer:** after saving, set the `▶ Resume:` line at the top of `tasks/ACTIVE.md` to this file's path.
