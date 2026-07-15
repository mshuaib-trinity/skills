---
name: write-implementation-plan
description: Use when approved requirements or a design need to become a task-by-task implementation plan before code changes.
---

# Write Implementation Plan

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the write-implementation-plan skill to create the implementation plan."

**Context:** If working in an isolated worktree, it should have been created via the `prepare-isolated-workspace` skill at execution time.

Use this skill only when a detailed durable plan will reduce execution risk. A compact settled change
may proceed through its focused implementation workflow, and design-only work may stop without a plan.

**Save plans into the AgentKit task tree** (the repo task protocol tracks all meaningful work under `tasks/current/`):
- If design-before-build already created the task/epic, write the plan there: `tasks/current/task-<slug>/plan.md` (standalone) or `tasks/current/epic-<slug>/plan.md` (epic).
- A saved implementation plan is a durable artifact. If no task exists, create `tasks/future/task-<slug>/task.md`, move it to `tasks/current/`, update dashboards, then write the plan. Use an epic only when the design has multiple independently testable slices.
- For an epic, mirror each plan Task into a row in `kanban.md` (and optionally a stub `tasks/<task-id>/task.md` with `test_criteria`) so execution can track status.
- Update `tasks/ACTIVE.md` / `tasks/STATUS.md` per the repo task protocol.
- A user may request a conversational outline instead; that is not this skill and does not create a plan artifact.

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during design-before-build. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Record the verified checkpoint" - step

Do not include `git add`, `git commit`, push, or PR steps unless the user explicitly authorized that
Git action for this work. Authorization to implement is not authorization to commit.

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use execute-implementation-plan to implement this plan task-by-task (it selects subagent-per-task / parallel / inline mode). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Record the verified checkpoint**

Mark the plan step complete and record the fresh test output in the task artifact. If the user has
explicitly authorized commits, add a separate exact staging/commit step scoped to these files.
````

## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Remember
- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, and evidence-backed checkpoints

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

## Execution Handoff

After saving the plan:

**"Plan complete and saved to `tasks/current/<task-or-epic>/plan.md`.**

- **REQUIRED SUB-SKILL:** Use execute-implementation-plan to implement it.
- execute-implementation-plan selects the execution mode: **subagent-per-task** (default — fresh subagent + two-stage review), **parallel dispatch** for fully-independent tasks, or **inline** when subagents aren't available.
