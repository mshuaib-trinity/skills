#!/usr/bin/env python3
"""Validate project management structure.

Copy this verbatim to `scripts/validate-project.py` at init. It is the
structural guard for the lifecycle system — every task closes only after this
exits 0.

Checks:
  - every epic in current/ or future/ has prd.md + kanban.md
  - every task / standalone has task.md with a test_criteria field
  - tasks/ACTIVE.md, tasks/STATUS.md, tasks/TASK-DESIGN.md exist
  - AGENTS.md exists
  - if CLAUDE.md exists, CLAUDE.md and AGENTS.md are identical mirrors
  - docs/adr/ and docs/adr/FORMAT.md exist
  - docs/NAVIGATION.md exists

Exit 0 if valid, exit 1 with an error list if not.

Project-specific checks (e.g. import-boundary greps) go in the clearly marked
section at the bottom — keep the generic checks above untouched.
"""

import sys
from pathlib import Path

root = Path(__file__).parent.parent
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate_epic(epic_dir: Path) -> None:
    check((epic_dir / "prd.md").exists(), f"{epic_dir.name}: missing prd.md")
    check((epic_dir / "kanban.md").exists(), f"{epic_dir.name}: missing kanban.md")
    tasks_subdir = epic_dir / "tasks"
    if tasks_subdir.exists():
        for task_dir in tasks_subdir.iterdir():
            if task_dir.is_dir():
                validate_task(task_dir)


def validate_task(task_dir: Path) -> None:
    task_md = task_dir / "task.md"
    check(task_md.exists(), f"{task_dir.name}: missing task.md")
    if task_md.exists():
        content = task_md.read_text()
        check(
            "test_criteria:" in content,
            f"{task_dir.name}/task.md: missing test_criteria field",
        )


def validate_standalone(standalone_dir: Path) -> None:
    task_md = standalone_dir / "task.md"
    check(task_md.exists(), f"{standalone_dir.name}: missing task.md")
    if task_md.exists():
        content = task_md.read_text()
        check(
            "test_criteria:" in content,
            f"{standalone_dir.name}/task.md: missing test_criteria field",
        )


# --- Generic structural checks (do not edit per project) -------------------

for state_dir in ["tasks/current", "tasks/future"]:
    state_path = root / state_dir
    if not state_path.exists():
        continue
    for entry in sorted(state_path.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("epic-"):
            validate_epic(entry)
        elif entry.name.startswith("task-"):
            validate_standalone(entry)

check((root / "tasks" / "ACTIVE.md").exists(), "tasks/ACTIVE.md is missing")
check((root / "tasks" / "STATUS.md").exists(), "tasks/STATUS.md is missing")
check(
    (root / "tasks" / "TASK-DESIGN.md").exists(),
    "tasks/TASK-DESIGN.md is missing",
)
check((root / "AGENTS.md").exists(), "AGENTS.md is missing")
check((root / "docs" / "NAVIGATION.md").exists(), "docs/NAVIGATION.md is missing")
check((root / "docs" / "adr").exists(), "docs/adr/ directory is missing")
check(
    (root / "docs" / "adr" / "FORMAT.md").exists(),
    "docs/adr/FORMAT.md is missing",
)

# In claude+agents mode, CLAUDE.md and AGENTS.md must be exact mirrors.
# In agents-only mode, CLAUDE.md is intentionally absent and this check is skipped.
claude_md = root / "CLAUDE.md"
agents_md = root / "AGENTS.md"
if claude_md.exists() and agents_md.exists():
    check(
        claude_md.read_text() == agents_md.read_text(),
        "CLAUDE.md and AGENTS.md have diverged — they must be identical mirrors",
    )

# --- Project-specific checks (edit freely) ---------------------------------
# Add greps, import-boundary checks, or naming rules unique to this project
# below. Example (uncomment and adapt):
#
# def validate_layer_boundaries() -> None:
#     core = root / "src" / "core"
#     if not core.exists():
#         return
#     for path in core.rglob("*.py"):
#         content = path.read_text()
#         rel = path.relative_to(root)
#         check(
#             "from domain" not in content and "import domain" not in content,
#             f"{rel}: core must not import from domain",
#         )
#
# validate_layer_boundaries()

# --- Report ----------------------------------------------------------------

if errors:
    print("❌ Project structure validation failed:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"✅ Project structure valid ({root.name})")
