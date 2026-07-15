---
name: design-before-build
description: Use when new behavior, workflow, architecture, or unclear requirements contain material choices that should be resolved before implementation.
---

# Design Before Build

Turn an idea into an approved, durable design without re-asking what authoritative project context
already settles.

<HARD-GATE>
Do not implement unresolved behavior or architecture before the design is approved. This gate applies
to the unresolved decisions, not to operational work, established bug contracts, or behavior-neutral
micro edits.
</HARD-GATE>

## 1. Classify Scope

Use `tasks/TASK-DESIGN.md` when present.

| Situation | Action |
|---|---|
| Operational, micro, or established bug behavior | Skip this skill |
| Disposable ideation with no accepted direction or durable artifact | Explore conversationally; do not create a task |
| Small new behavior with one source-supported approach | Produce a compact design and one approval checkpoint |
| Material product, workflow, compatibility, or architecture trade-off | Use the full design flow |
| Design already approved | Continue to stress testing or planning only if useful |

Task tracking and design depth are independent. A tracked change may not need design; disposable
ideation may remain conversational until the user accepts a direction intended to guide future work.

## 2. Resolve Context Before Asking

Read the minimum relevant context through `docs/NAVIGATION.md`, then apply this authority order:

1. Direct user instruction
2. Approved PRD, task specification, or prior design
3. Repository and component vision
4. Accepted ADRs and documented architecture
5. Tests, code, and conventions

Maintain a small decision ledger:

- **Inherited:** directly settled by an authoritative source
- **Inferred:** source-supported and safe to decide
- **Provisional:** reversible bounded default
- **Contradiction:** authoritative sources disagree
- **User decision:** unresolved choice with material product or contract impact

Do not ask the user to confirm inherited or inferred decisions. Tell them what you adopted and why.

## 3. Ask Only Genuine Design Questions

Ask only when the answer cannot be discovered and choosing incorrectly would materially change
product direction, scope, compatibility, security, cost, user experience, or a hard-to-reverse
contract. Consolidate closely related blockers into one checkpoint; do not serialize obvious
confirmations over many turns.

A reversible local choice is not a blocker. Choose the recommended default, record it as provisional,
and continue.

## 4. Explore Real Alternatives

Propose alternatives only when they are genuinely viable and materially different. Lead with the
recommendation and its rationale. Do not invent three cosmetic options to satisfy a quota.

For existing codebases:

- Follow established seams and naming unless the design intentionally changes them.
- Include only architecture improvements needed by the goal.
- Check relevant ADRs before reopening a settled decision.
- Define ownership, interfaces, data flow, failure behavior, testing, and documentation impact.

## 5. Present and Approve Coherently

Present the design at a scale matching its complexity:

- Compact design: goal, chosen behavior, affected seam, verification.
- Full design: architecture, responsibilities, contracts/data flow, errors, migration, testing,
  documentation, and unresolved decisions.

Include a **Decisions made from context** section so the user can audit autonomous choices. Ask for
approval once after the coherent design. Use at most one earlier consolidated question checkpoint;
add another only when the first answer reveals a new material fork that could not have been known.

## 6. Capture Durable Designs

When the design becomes durable:

1. Reuse an active in-scope task; otherwise create it in `tasks/future/`, then move it to
   `tasks/current/` before writing the artifact.
2. Save a standalone design to `tasks/current/task-<slug>/design.md`, or use an epic's `prd.md`.
3. Update `tasks/ACTIVE.md` and `tasks/STATUS.md`.
4. Self-review for placeholders, contradictions, ambiguity, and scope.
5. Ask for review of the written design only when the file materially differs from what was approved.

Do not commit automatically. Commit only when the user requested it or the active workflow separately
authorizes it.

## 7. Choose the Next Step

- Non-trivial unresolved consequences remain: use `stress-test-design`.
- A detailed execution sequence would reduce implementation risk: use `write-implementation-plan`.
- The design is intentionally design-only: stop after capture.
- The change is small and settled: proceed with its focused implementation workflow.

The full build loop is not a mandatory ceremony.

## Visual Companion

Offer the visual companion only when a diagram or mockup would materially improve a pending design
decision. Do not interrupt text-only or already-settled work to offer it. If accepted, read
`references/visual-companion.md` before use.

## Red Flags

- Asking a question answered by vision, component docs, ADRs, code, or tests
- Treating every tracked change as a full design project
- Inventing alternatives with no meaningful trade-off
- Requiring approval after every section
- Creating a task for disposable ideation
- Forcing design-only work into an implementation plan
- Committing a design without authorization
