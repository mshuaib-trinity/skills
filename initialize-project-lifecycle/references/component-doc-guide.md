# Component Documentation

Component guides are the durable current-intent layer between repository vision and source code.
They prevent root instructions and the system overview from accumulating component internals.

## Selection Rubric

Create `docs/components/<component>.md` when at least one is true:

- The component has an independent responsibility with a meaningful contract or dependency seam.
- Its non-goals or principles settle recurring design questions.
- It spans enough packages, adapters, or tests that navigation is repeatedly expensive.
- It is expected to evolve behind a stable interface.
- Maintainers can understand the code but still need to know why ownership is divided this way.

Do not create a guide for leaf utilities, self-explanatory modules, or temporary implementation details.

## Ownership of Truth

| Source | Owns |
|---|---|
| `docs/VISION.md` | Repository north star and governing principles |
| `docs/OVERVIEW.md` | System map and end-to-end flow |
| `docs/components/*.md` | Current component intent, seams, invariants, and navigation |
| `docs/adr/` | Historical rationale |
| `tasks/` | Change context |
| Code and tests | Executable behavior |

On task completion, promote durable current truth from task specs into the relevant component guide.
Do not copy the full task history into permanent docs.

## Required Shape

Use the initializer's `references/component-doc-template.md`. Each guide contains intent, non-goals,
decision principles, ownership, current data flow, entry points, extension seams, invariants, failure
behavior, verification routes, related ADRs, and active-work lookup.

## Current Guides

_No component guides at initialization._ Replace this line with links when the first qualifying guide
is created.
