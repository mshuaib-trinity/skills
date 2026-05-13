# PRD Format

This repository uses three levels of planning. Each level has a specific format and purpose.
Mixing levels (e.g. putting product direction in an epic PRD) is a common mistake — avoid it.

---

## Three Levels of Planning

| Level | Document | When to Write |
|---|---|---|
| **Product direction** | `docs/VISION.md` | Once, at project start. Updated only when direction changes. |
| **Feature scope** | `<epic>/prd.md` | Every epic — defines goals, requirements, and what is out of scope. |
| **Cross-cutting initiative** | `PRDs/<name>.md` | Only when 2+ epics share a goal not covered by VISION.md. |

**Decision rule:** If you can explain the initiative by pointing to `docs/VISION.md`, you do not need a PRD in `PRDs/`. The initiative PRD is for work that goes beyond what the vision already covers.

---

## Level 1 — Epic PRD (`<epic>/prd.md`)

Written for every epic. Lives inside the epic directory. Short and focused.

### Format

```markdown
# PRD: <Epic Name>

## Goal
What does completing this epic achieve? One paragraph maximum.
Write from the perspective of value delivered, not tasks completed.

Good: "Users can log in with email/password and remain authenticated across sessions."
Bad: "Implement authentication endpoint and session management."

## Requirements
- [Specific, testable requirement]
- [Specific, testable requirement]
- (Add one bullet per distinct deliverable)

## Out of Scope
- [Explicit non-goal — prevents scope creep]
- [Explicit non-goal]
```

### What Makes a Good Requirement

Each requirement must be:
- **Specific** — not "improve performance" but "API responds in under 200ms for 95th percentile"
- **Testable** — you can write a test or manually verify it
- **Atomic** — one thing, not "X and Y and Z"
- **In scope** — if it's not in scope, put it in Out of Scope

| ❌ Bad requirement | ✅ Good requirement |
|---|---|
| Make the system faster | API p95 latency < 200ms measured with k6 |
| Add authentication | Email/password login returns JWT; invalid creds return 401 |
| Fix the UI | Login form shows inline error for invalid email format |
| Handle errors properly | All API errors return `{error: string, code: string}` structure |

### What Makes Good Out of Scope

Out of Scope prevents silent scope creep. Include things that:
- Someone might reasonably assume are included
- Are related but deliberately deferred
- Would significantly change the effort if included

```markdown
## Out of Scope
- OAuth / social login (deferred to separate epic)
- Password reset flow (separate epic)
- Multi-factor authentication
- Rate limiting on login endpoint (tracked in backlog)
```

---

## Level 2 — Initiative PRD (`PRDs/<name>.md`)

Only write this when 2+ epics share a single goal that VISION.md doesn't cover.

### Format

```markdown
# <Initiative Name>

**context:** [Why this initiative exists NOW — what changed or what need emerged.
              What would happen if we didn't do this?
              One paragraph maximum.]

**epics:**
- [epic-slug-1](../tasks/current/epic-slug-1/task.md) — one-line summary
- [epic-slug-2](../tasks/future/epic-slug-2/task.md) — one-line summary
- [epic-slug-3](../tasks/future/epic-slug-3/task.md) — one-line summary

**done_when:** [Specific, testable criteria that confirm this initiative is complete.
               Must be verifiable without ambiguity. One or two sentences.]
```

### Rules

1. **Keep it short.** If you need more than 3 sections, the initiative is too broad — split it.
2. **Link every epic.** PRDs without links rot. A link that breaks tells you the epic was moved.
3. **done_when must be testable.** "Works well" is not testable. Examples:

| ❌ Bad done_when | ✅ Good done_when |
|---|---|
| System works well | All child epics in `tasks/completed/` and `validate-project.py` passes |
| Performance improved | p95 API latency < 200ms in staging load test (100 concurrent users) |
| Better developer experience | New dev can run `make dev` and see the app working in under 5 minutes |
| Refactoring complete | No imports cross the framework/domain boundary (`grep` check passes in CI) |

### Example — Good Initiative PRD

```markdown
# Framework Reusability Initiative

**context:** The platform was built with Sakila Analytics as the only domain.
Three features added in the last sprint hard-coded Sakila-specific concepts into
the framework layer, making it impossible to deploy with a different domain without
surgery. This initiative closes those gaps before a second domain is started.

**epics:**
- [epic-framework-boundary](../tasks/current/epic-framework-boundary/task.md) — enforce framework/domain boundary via AgentFactory protocol
- [epic-remove-hardcoded-constants](../tasks/future/epic-remove-hardcoded-constants/task.md) — remove all domain-specific constants from framework
- [epic-integration-tests](../tasks/future/epic-integration-tests/task.md) — add framework-level integration tests with mock domain

**done_when:** All three epics are in `tasks/completed/`, `grep -r "sakila" backend/ai/core/` returns
empty, and the CI framework boundary check passes on every PR.
```

---

## Level 3 — VISION.md (Product Direction)

Not a PRD — a vision document. See [`vision-guide.md`](vision-guide.md) for the full writing guide.

Use VISION.md for:
- The core thesis of the product
- Architectural principles that settle future debates
- The target state (what "done" looks like)
- What the system explicitly is NOT

**Never put feature requirements in VISION.md.** Requirements go in epic PRDs.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Writing requirements that are really goals | Make it testable or move it to the Goal section |
| Missing Out of Scope section | Always write it — what you don't include matters as much as what you do |
| Initiative PRD when VISION.md covers it | Read VISION.md first; only create PRDs/ file if VISION doesn't explain the why |
| done_when that can't be verified | Rewrite it until someone can check it without asking you what it means |
| PRD longer than one page | Split the epic into smaller epics |
