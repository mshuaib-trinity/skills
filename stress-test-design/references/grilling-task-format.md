# Grilling Task Format

A grilling session lives as a standalone task with an isolated `specs/` folder:

```
tasks/current/task-grill-<slug>/
├── task.md                  ← standalone task header (status, test_criteria)
└── specs/                   ← isolated capture area — never touches app docs/
    ├── 00-overview.md
    ├── decisions.md
    ├── scenarios.md
    ├── glossary.md
    ├── open-questions.md
    └── candidate-adrs.md
```

Create the modules lazily — only write a module the first time it has content. `00-overview.md` is the one exception: write it at the start so the task is self-describing.

`validate-project.py` treats `task-grill-<slug>/` as a standalone (it only requires `task.md` with a `test_criteria` field). The `specs/` subfolder is ignored by validation, so any module layout is safe.

---

## Module formats

### 00-overview.md

```md
# Grilling: <topic>

**Started:** YYYY-MM-DD

## What we're stress-testing
<one or two paragraphs describing the plan / design under grill>

## Status
<in progress | resolved — shared understanding reached>
```

### decisions.md

One entry per resolved decision. Lead with the decision, then why, then what was rejected.

```md
## <Short decision title>
**Decided:** <the choice, stated plainly>
**Why:** <the reasoning that settled it>
**Rejected:** <alternatives considered and why they lost> (omit if there were none)
```

### scenarios.md

Only the scenarios that actually changed or pinned down the design.

```md
## <Scenario name>
**Setup:** <the concrete situation>
**Resolved behaviour:** <what should happen, decided during the grill>
```

### glossary.md

Sharpened terminology only — terms specific to this topic, not general programming concepts. Be opinionated: pick the canonical term, list the rejected synonyms under `_Avoid_`.

```md
**<Canonical term>:**
<one or two sentence definition — what it IS, not what it does>
_Avoid_: <synonyms we are deliberately not using>
```

### open-questions.md

Branches left unresolved. Each should be answerable later — phrase it as a question with what's blocking the answer.

```md
## <The open question>
**Blocked on:** <what's needed to resolve it — a decision, more info, a stakeholder>
**Leaning:** <current best guess, if any>
```

### candidate-adrs.md

Draft ADRs for decisions that meet the ADR bar (hard to reverse + surprising without context + a real trade-off). Use this repo's real ADR template so the draft can be promoted directly into `docs/adr/` at implementation time. Leave the number as `NNN` — it gets assigned when promoted.

```md
# ADR-NNN: <Title — imperative, present tense>

**Status:** Draft (candidate — promote to docs/adr/ when implemented)
**Date:** YYYY-MM-DD

## Context
<what problem exists, why a decision is needed, what forces are at play>

## Decision
<what we decided, stated plainly>

## Consequences
<what this enables, what constraints it creates, what becomes harder>
```

---

## Why this stays out of `docs/`

The application's `docs/` (and especially `docs/adr/`) is current-state documentation that
changes when code changes. A grilling session is upstream of that — it produces draft
thinking about a plan that may not be implemented for a while, or at all. Keeping it inside
the grilling task means:

- The app docs never carry speculative or abandoned decisions.
- `docs/adr/`'s append-only, numbered convention is never violated by half-baked drafts.
- Everything a session produced is in one place, attached to the task that produced it.

Promotion to real app docs happens later, deliberately, as part of the implementation task.
