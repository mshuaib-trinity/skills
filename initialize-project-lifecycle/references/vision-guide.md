# VISION.md — Writing Guide

`docs/VISION.md` is the most important document in any repository.
Every architectural decision, every convention, every boundary flows from it.
**If a proposed change feels wrong, check it against the vision first.**

An AI agent or new developer should be able to read VISION.md and understand
not just WHAT the system does, but WHY every major decision was made.

---

## What Makes a Good VISION.md

**Good:**
- Explains the "why" behind every major architectural decision
- Explicitly states what the system is NOT (prevents scope creep)
- Names governing principles that can settle future arguments
- Describes what "done" looks like (target state)
- Short enough to read in 10 minutes

**Bad:**
- A feature list or product spec
- Architecture diagrams without explanations
- "We use React because it's popular"
- So long nobody reads it

---

## Section-by-Section Guide

### § 1 — What This Platform Is

One paragraph. Answer: what problem does this solve, for whom, and how?

```markdown
## What This Platform Is

InsightAI Platform is a reusable multi-agent chatbot framework. Its Sakila Analytics
deployment lets non-technical users ask natural language questions about a film rental
database and receive SQL results, visualizations, and narrative insights — without
writing a single query.
```

**What to avoid:** Don't list features. Describe the core capability and who benefits.

---

### § 2 — What It Is NOT

Explicit non-goals prevent future scope creep. Be direct.

```markdown
## What It Is Not

- **Not a monolithic app.** The framework and domain are separate layers. You swap
  the domain, not the framework.
- **Not a prototype.** Every layer is production-quality: auth, persistence, streaming,
  error handling.
- **Not a one-domain tool.** Sakila is the reference implementation. The framework
  works for any domain.
```

**Rule:** Every "not" should prevent a real misunderstanding someone might have.
If it's obvious, skip it.

---

### § 3 — Core Thesis

The single insight driving the architecture. One paragraph.

```markdown
## Core Thesis

Chatbot applications share common infrastructure: authentication, session persistence,
streaming, multi-agent orchestration, and LLM provider abstraction. Building these
once and varying only the domain logic (the agents, their tools, their outputs)
is cheaper, safer, and more maintainable than rebuilding per project.
```

**Test:** Can you explain this to someone in 30 seconds? If not, it's too complex.

---

### § 4 — Architecture Layers

Name the layers explicitly. Order from most stable (bottom) to most volatile (top).

```markdown
## Architecture Layers

| Layer | What It Is | Change Rate |
|---|---|---|
| Layer 1 — Frontend Shell | React app, auth, session UI, streaming renderer | Slow |
| Layer 2 — Backend Infrastructure | FastAPI, auth, session persistence, SSE streaming | Very slow |
| Layer 3 — AI Framework | Orchestrator, agents, LLM clients, communication | Slow |
| Layer 4 — Domain Module | Domain-specific agents, prompts, SQL, tools | Fast |
```

**Rule:** Deeper layers must never import from higher layers.
State this as a contract, not a preference.

---

### § 5 — Framework/Domain Boundary (if applicable)

If your architecture has a hard boundary between reusable and domain-specific code,
make it explicit here. This is the most important contract in the codebase.

```markdown
## Framework/Domain Boundary

The framework NEVER imports from the domain. The domain imports from the framework.
The only surface the backend exposes to the domain is the `AgentFactory` protocol.

Violation check (run in CI):
grep -r "domain_module_name" framework_directory/   # must return empty
```

---

### § 6 — Governing Design Principles

Two or three principles max. These should settle future architectural debates.
Each principle should be a decision rule, not a vague value.

```markdown
## Governing Design Principles

**Principle 1 — Developer Cognitive Load First**
When choosing between two equivalent approaches, pick the one that is easier to
understand when you return to it in six months. Explicit over implicit. Localized
over distributed. Readable over clever.

**Principle 2 — Reusability as Co-Principle**
Every design decision must work for a second domain without modification. If you
cannot explain how a non-Sakila domain would use this code, the design is wrong.
```

**Test:** Can a developer use these to resolve a real disagreement? If the principle
is too vague to settle an argument, rewrite it.

---

### § 7 — Target State (What "Good" Looks Like)

Describe the end state when the project is complete and healthy.
This is the north star for all work.

```markdown
## Target State

The platform is "done" when:
- A developer can add a new domain by creating one directory and one import change
- The framework has zero domain-specific imports
- Every architectural decision has an ADR
- A new developer can read VISION.md and OVERVIEW.md and start contributing in one day
```

---

### § 8 — What to Read Next

A short navigation guide pointing to the next documents.

```markdown
## What to Read Next

| Goal | Read |
|---|---|
| Understand the system | `docs/OVERVIEW.md` |
| Start working | `tasks/ACTIVE.md` → `tasks/TASK-DESIGN.md` |
| Understand an architectural decision | `docs/adr/` |
| Add a new feature | `docs/NAVIGATION.md` |
```

---

## VISION.md Template

Use this as the starting point. Fill in every section — do not leave placeholders in production.

```markdown
# Vision

## What This Platform Is

[One paragraph: what problem, for whom, how]

## What It Is Not

- **Not [X].** [Why this matters to clarify]
- **Not [Y].** [Why this matters to clarify]

## Core Thesis

[One paragraph: the single insight driving the architecture]

## Architecture Layers

| Layer | What It Is | Change Rate |
|---|---|---|
| Layer 1 — [Name] | [Description] | Fast / Slow / Very slow |
| Layer 2 — [Name] | [Description] | Fast / Slow / Very slow |

## Framework/Domain Boundary

[If applicable: state the contract explicitly]

## Governing Design Principles

**Principle 1 — [Name]**
[Decision rule, not vague value]

**Principle 2 — [Name]**
[Decision rule, not vague value]

## Target State

The platform is "done" when:
- [Specific, verifiable criterion]
- [Specific, verifiable criterion]

## What to Read Next

| Goal | Read |
|---|---|
| Understand the system | `docs/OVERVIEW.md` |
| Start working | `tasks/ACTIVE.md` |
| Understand a decision | `docs/adr/` |
```

---

## Quality Checklist

Before marking VISION.md complete:

- [ ] Can you explain the core thesis in 30 seconds?
- [ ] Does each "What It Is Not" prevent a real misunderstanding?
- [ ] Can a developer use the principles to resolve a real argument?
- [ ] Is the target state specific and verifiable (not "production-ready")?
- [ ] Does every major architectural decision trace back to a principle?
- [ ] Can a new developer read it in under 10 minutes?
