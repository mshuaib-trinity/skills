# ADR Format

Architecture Decision Records capture significant decisions made in this codebase —
decisions that would surprise a future developer or AI agent if they encountered the
outcome without knowing the reasoning.

**ADRs are append-only.** Once accepted, an ADR is never edited. It is a historical record.

---

## When to Write an ADR

Write one when you make a decision that:
- Chooses one architectural approach over viable alternatives
- Establishes a boundary or contract that other code must respect
- Would be costly or confusing to reverse without understanding the original reasoning
- Would surprise a future developer who reads the code without context

**Do NOT write one for:**
- Implementation details (how a function works internally)
- Style choices (naming conventions, formatting)
- Decisions that are self-evident from reading the code
- Decisions that were obvious and had no real alternatives

**Decision rule:** If a future developer might ask "why was this done this way?", write an ADR.

---

## Format

````markdown
# ADR-[NUMBER]: [Title — active voice, present tense]

**Status:** Accepted | Superseded by [ADR-XXX](ADR-XXX-slug.md)
**Date:** YYYY-MM-DD

## Context
[What problem existed. Why a decision was needed. What forces were at play.
What alternatives were considered and why they were rejected.]

## Decision
[What was decided. The actual choice, stated plainly. Not the reasoning — that goes in Context.]

## Consequences
[What this enables. What constraints it creates. What becomes harder or impossible.
What must be maintained going forward as a result of this decision.]
````

---

## Writing Guide

### Title
Use active voice, present tense. Describe the decision, not the problem.

| ❌ Bad title | ✅ Good title |
|---|---|
| Database problems | Two-Database Architecture for Platform and Analytics Data |
| Auth decision | JWT Tokens for Session Authentication |
| How we handle streaming | SSE Streaming with MessageEnvelope for Progressive Output |

### Context
This is the most important section. Answer:
- What was the situation before this decision?
- What options did you consider?
- Why did you reject the alternatives?
- What constraints or requirements shaped the choice?

```markdown
## Context
The platform needs to stream multi-agent output to the frontend as it arrives.
We considered three approaches:
1. Polling: Client polls every N seconds. Simple but adds latency and unnecessary requests.
2. WebSockets: Bidirectional. More complex to manage; we only need server→client.
3. SSE (Server-Sent Events): Unidirectional, HTTP-native, works with existing infrastructure.
SSE is sufficient for our use case and requires no additional infrastructure.
```

### Decision
Be direct. One or two sentences.

```markdown
## Decision
All agent output is streamed as SSE events. Each event carries a MessageEnvelope
with a ContentType field for frontend routing.
```

### Consequences
Be honest about trade-offs. Include what becomes harder, not just what improves.

```markdown
## Consequences
- Frontend renders output progressively — users see results before workflow completes.
- ContentType is the stable API contract between backend and frontend.
- SSE is unidirectional — if bidirectional streaming is ever needed, this decision needs revisiting.
- All future agent output types must register a ContentType and a frontend renderer.
```

---

## Rules

1. **ADRs are append-only.** Never edit an accepted ADR.
2. **To reverse a decision:** Write a new ADR that supersedes the old one.
   Set the old ADR's status to `Superseded by ADR-XXX`.
3. **Number sequentially:** ADR-001, ADR-002, etc.
4. **File naming:** `ADR-[NUMBER]-[slug].md` (e.g. `ADR-001-two-database-architecture.md`)
5. **Date is the decision date**, not the writing date.
6. **One decision per ADR.** If you're making two decisions, write two ADRs.

---

## Supersession Pattern

When you reverse a decision:

**Old ADR (ADR-003):**
```markdown
**Status:** Superseded by [ADR-012](ADR-012-new-decision.md)
```

**New ADR (ADR-012):**
```markdown
# ADR-012: [New decision]

**Status:** Accepted
**Date:** YYYY-MM-DD

## Context
ADR-003 established X. Since then, [what changed]. This ADR supersedes ADR-003.
...
```

The old ADR stays in the repository. It explains the history.

---

## Index

Update this table every time a new ADR is added.

| ADR | Title | Status |
|-----|-------|--------|
| _(none yet — add entries as ADRs are written)_ | | |
