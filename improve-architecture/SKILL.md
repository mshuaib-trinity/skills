---
name: improve-architecture
description: Use when looking for refactoring, module deepening, coupling reduction, clearer seams, architecture changes, or ways to make code more testable and AI-navigable.
---

# Improve Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

## Glossary

Use these terms exactly in every suggestion. Consistent language is the point — don't drift into "component," "service," "API," or "boundary." Full definitions in [references/language.md](references/language.md).

- **Module** — anything with an interface and an implementation (function, class, package, slice).
- **Interface** — everything a caller must know to use the module: types, invariants, error modes, ordering, config. Not just the type signature.
- **Implementation** — the code inside.
- **Depth** — leverage at the interface: a lot of behaviour behind a small interface. **Deep** = high leverage. **Shallow** = interface nearly as complex as the implementation.
- **Seam** — where an interface lives; a place behaviour can be altered without editing in place. (Use this, not "boundary.")
- **Adapter** — a concrete thing satisfying an interface at a seam.
- **Leverage** — what callers get from depth.
- **Locality** — what maintainers get from depth: change, bugs, knowledge concentrated in one place.

Key principles (see [references/language.md](references/language.md) for the full list):

- **Deletion test**: imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.**
- **One adapter = hypothetical seam. Two adapters = real seam.**

This skill is _informed_ by the project's domain model. The domain language gives names to good seams; ADRs record decisions the skill should not re-litigate.

## Process

### 1. Explore

Read the project's domain docs (`docs/VISION.md`, `docs/OVERVIEW.md`) and any ADRs in the area you're touching first.

Then use the Agent tool with `subagent_type=Explore` to walk the codebase. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates

Present a numbered list of deepening opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Problem** — why the current architecture is causing friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of locality and leverage, and also in how tests would improve

**Use the project's domain vocabulary (from `docs/VISION.md` / `docs/OVERVIEW.md`) for the domain, and [references/language.md](references/language.md) vocabulary for the architecture.** If the domain docs name "OrchestrationAgent," talk about "the orchestration module" — not "the FooBarHandler," and not "the orchestration service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly (e.g. _"contradicts ADR-0007 — but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

Do NOT propose interfaces yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, invoke the **`stress-test-design`** skill and drop into a grilling conversation. That skill spins up an isolated grilling task and captures every resolved decision into its `specs/` folder — reuse it rather than re-implementing capture here. Walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallize. All capture lands in the grilling task's `specs/` (never in the app's `docs/`):

- **Sharpening or coining a term for a deepened module?** Record it in `specs/glossary.md` — same discipline as `stress-test-design`. If the term is load-bearing domain vocabulary, flag it for promotion into `docs/VISION.md` / `docs/OVERVIEW.md` at implementation time (grilling never edits app docs directly).
- **A design choice settled?** → `specs/decisions.md` (decision, why, rejected alternatives).
- **User rejects the candidate with a load-bearing reason?** Offer to capture it as a candidate ADR in `specs/candidate-adrs.md`, framed as: _"Want me to draft this as an ADR so future architecture reviews don't re-suggest it?"_ Use the repo's real ADR template ([docs/adr/FORMAT.md](../../../docs/adr/FORMAT.md)); it gets promoted to a numbered `docs/adr/` ADR only when acted on. Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** See [references/interface-design.md](references/interface-design.md).
