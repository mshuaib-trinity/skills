---
name: route-skills
description: Use when a new request needs work classification or selection of process skills based on risk, durability, and uncertainty.
---

# Route Skills

<SUBAGENT-STOP>
If dispatched to execute a bounded subtask, follow the parent task and skip routing.
</SUBAGENT-STOP>

## Route Before Acting

1. Follow the host instruction hierarchy, the user's scope, and repository instructions. Skills never
   override higher-priority instructions.
2. Read the minimum authoritative context needed to classify the request. Use `docs/NAVIGATION.md`
   when present.
3. Apply the canonical work classes in `tasks/TASK-DESIGN.md`:
   - **Operational or micro:** act directly; do not create a repository task.
   - **Tracked but settled:** reuse or create a task, then use only the relevant implementation,
     debugging, review, or verification skill.
   - **Tracked with unresolved behavior or trade-offs:** use `design-before-build`.
   - **Epic:** design and decompose before implementation.
4. Invoke a skill when its stated trigger matches the current situation. Do not run the complete build
   loop by default.

## Evidence Before Questions

Resolve context from user instructions, approved task artifacts, vision/component docs, ADRs, then
code and tests. Ask only when evidence conflicts or an unresolved choice materially changes scope,
product behavior, compatibility, security, cost, or an irreversible contract.

## Common Routes

| Situation | Skill |
|---|---|
| New behavior or design trade-off | `design-before-build` |
| Approved design needs challenge | `stress-test-design` |
| Bug or unexpected behavior | `debug-systematically` |
| Focused feature or fix | `develop-with-tdd` |
| Approved design needs a detailed plan | `write-implementation-plan` |
| Existing plan needs execution | `execute-implementation-plan` |
| Architecture deepening | `improve-architecture` |
| Skill changes | `author-skills` |
| Standalone read-only review | `review-code-changes` |
| Completion claim | Applicable review, then `verify-before-completion` |
| Branch/task closure | `finish-development-branch` |

## Red Flags

- Creating a task merely because the user asked a question
- Using line count as a proxy for impact
- Running design for an established bug contract
- Asking the user to restate documented direction
- Treating an agent checklist item as a repository task
