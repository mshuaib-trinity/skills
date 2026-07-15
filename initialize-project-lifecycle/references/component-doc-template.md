# Component: {{COMPONENT_NAME}}

Use this template only when the component-selection rubric in `docs/components/README.md` applies.
Delete instructional text and replace every placeholder before treating the guide as current truth.

## Intent and Responsibility

{{WHAT_THE_COMPONENT_OWNS_AND_WHY_IT_EXISTS}}

## Non-Goals

- {{EXPLICIT_NON_GOAL}}

## Governing Decision Principles

1. **{{PRINCIPLE_NAME}}.** {{DECISION_RULE}}

## Ownership and Dependency Direction

{{WHAT_DEPENDS_ON_WHAT_AND_WHICH_IMPORT_DIRECTIONS_ARE_FORBIDDEN}}

## Current Architecture and Data Flow

{{SHORT_CURRENT_STATE_DESCRIPTION}}

## Primary Entry Points

| Concern | Path |
|---|---|
| {{CONCERN}} | `{{PATH}}` |

## Extension Seams and Invariants

- {{STABLE_INTERFACE_OR_INVARIANT}}

## Failure Behavior and Verification

{{FAILURE_POLICY}}

- Tests: `{{TEST_PATH_OR_COMMAND}}`

## Related Decisions and Current Work

- ADRs: {{ADR_LINKS_OR_NONE}}
- Active work: [`tasks/ACTIVE.md`](../../tasks/ACTIVE.md)
