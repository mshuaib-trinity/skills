---
name: stress-test-design
description: Use when an approved design, plan, or architecture idea needs consequence analysis, edge-case exploration, contradiction detection, or durable decision capture.
---

# Stress Test Design

Challenge consequences and unresolved gaps. Do not ask the user to reconfirm decisions already settled
by authoritative context.

## 1. Locate Durable Context

Read the approved design and the minimum relevant sources through `docs/NAVIGATION.md`. Use this
authority order:

1. Direct user instruction
2. Approved design, PRD, or task specification
3. Repository and component vision
4. Accepted ADRs and documented architecture
5. Tests, code, and conventions

If sources disagree, do not silently choose. Record the contradiction and surface its material effect.

## 2. Reuse or Create the Task

Stress testing an existing tracked design belongs to that task:

- Reuse its directory and create `specs/` there.
- Do not create a separate grilling task.
- Do not complete or move the parent task when stress testing ends.

When invoked independently for a durable design with no parent, create
`tasks/future/task-grill-<slug>/task.md`, move it to `tasks/current/`, update the dashboards, and
create `specs/00-overview.md`. Use the formats in
`references/grilling-task-format.md`.

Disposable thought experiments that will not guide future work may remain conversational and untracked.

## 3. Build the Decision Ledger

Before asking anything, classify each design branch:

| Class | Action |
|---|---|
| **Inherited** | Adopt the authoritative decision; record its source |
| **Inferred** | Decide from aligned sources; record rationale |
| **Provisional** | Choose a reversible bounded default; record how to revisit |
| **Contradiction** | Show the conflicting sources and material consequence |
| **User decision** | Ask only for a high-impact unresolved fork |

A clear direct instruction, approved design, governing principle, or accepted ADR can settle a branch.
Current behavior may be inferred from two aligned sources among docs, code, and tests. A reversible local
choice may be provisional from one established pattern when no source conflicts.

## 4. Stress Consequences, Not Repository Facts

Probe concrete failure and edge-case scenarios:

- boundary ownership and dependency direction
- compatibility and migration
- invalid, partial, empty, delayed, or duplicated inputs
- retries, cancellation, concurrency, and recovery
- security, privacy, cost, and latency where relevant
- observability, testing, rollout, and reversibility
- interaction with accepted ADRs and component non-goals

When a scenario exposes a real gap:

- Decide it automatically when inherited, inferred, or safely provisional.
- Ask the user only when alternatives remain vision-compatible and materially differ in product value,
  scope, compatibility, security, cost, or a hard-to-reverse contract.
- Consolidate related user-owned gaps into one checkpoint. Prefer at most two material questions for a
  normal stress test; if more remain, the design is probably under-specified and should return to
  `design-before-build`.

## 5. Capture at Coherent Checkpoints

Write decisions after a coherent analysis checkpoint or before switching topics. Do not perform a file
write for every obvious inherited branch.

| Result | File |
|---|---|
| Scope and status | `specs/00-overview.md` |
| Decision, source, rationale, rejected alternative | `specs/decisions.md` |
| Edge case that changed or pinned behavior | `specs/scenarios.md` |
| Canonical term | `specs/glossary.md` |
| Genuinely unresolved branch | `specs/open-questions.md` |
| ADR-worthy trade-off | `specs/candidate-adrs.md` |

Candidate ADRs must be hard to reverse, surprising without context, and the result of a real trade-off.
Use the repository ADR format, but do not create a numbered ADR during stress testing.

## 6. Report the Outcome

Give the user a compact checkpoint containing:

- **Decisions inherited from context**
- **Decisions made for you**
- **Gaps found and resolved**
- **Contradictions or user decisions still open**
- **Scenarios and verification implications**

Do not ask for approval of decisions the sources already require.

## 7. Close Only What This Session Owns

If using a parent feature task:

1. Mark the stress-test status resolved in `specs/00-overview.md`.
2. Leave the parent `task.md`, folder, and dashboards in their existing implementation state.
3. Continue to planning, implementation, or stop, according to the approved design.

If using a standalone `task-grill-<slug>`:

1. Confirm its test criteria and capture are complete.
2. Mark only that standalone task completed and move it to `tasks/completed/`.
3. Update dashboards and run `python3 scripts/validate-project.py`.

## Red Flags

- Asking where code belongs when vision or an ADR already settles ownership
- Asking one question per branch regardless of materiality
- Treating code as the only auto-resolution source
- Recording every obvious branch with a separate tool call
- Silently deciding a conflicting or irreversible product choice
- Completing a reused parent feature task after its stress-test phase
