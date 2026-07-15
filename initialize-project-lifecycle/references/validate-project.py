#!/usr/bin/env python3
"""Validate lifecycle structure, documentation, skills, and setup-mode consistency."""

from __future__ import annotations

import re
import sys
from pathlib import Path

root = Path(__file__).parent.parent
errors: list[str] = []

REQUIRED_DOCS = (
    "docs/NAVIGATION.md",
    "docs/VISION.md",
    "docs/OVERVIEW.md",
    "docs/components/README.md",
    "docs/adr/FORMAT.md",
    "tasks/ACTIVE.md",
    "tasks/STATUS.md",
    "tasks/TASK-DESIGN.md",
)
REQUIRED_SKILLS = (
    "route-skills",
    "design-before-build",
    "stress-test-design",
    "write-implementation-plan",
    "execute-implementation-plan",
    "develop-with-tdd",
    "debug-systematically",
    "improve-architecture",
    "review-code-changes",
    "verify-before-completion",
    "finish-development-branch",
    "author-skills",
    "create-handoff",
    "initialize-project-lifecycle",
)
PLACEHOLDER_PATTERNS = (
    re.compile(r"\{\{[^}]+\}\}"),
    re.compile(r"\b(?:TBD|TODO)\b"),
    re.compile(r"\b(?:CHANGEME|XXX)\b"),
    re.compile(r"\[Fill[^\]]*\]", re.IGNORECASE),
    re.compile(r"\[(?:Name|One paragraph|Description|Path|Project|Component|Decision rule)[^\]]*\]", re.IGNORECASE),
)


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def frontmatter_block(content: str) -> str:
    stripped = content.lstrip()
    if not stripped.startswith("---\n"):
        return ""
    parts = stripped.split("---", 2)
    return parts[1] if len(parts) == 3 else ""


def frontmatter_value(content: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n]+)$", frontmatter_block(content))
    return match.group(1).strip() if match else None


def field_has_value(content: str, key: str) -> bool:
    inline = frontmatter_value(content, key)
    if inline:
        return True
    return bool(re.search(rf"(?m)^{re.escape(key)}:\s*$\n(?:[ \t]+\S.*\n?)+", frontmatter_block(content)))


def validate_task(task_dir: Path, state: str, *, enforce_folder_state: bool = True) -> None:
    task_md = task_dir / "task.md"
    check(task_md.exists(), f"{task_dir.relative_to(root)}: missing task.md")
    if not task_md.exists():
        return
    content = read(task_md)
    managed = bool(frontmatter_block(content))
    legacy = "<!-- LIFECYCLE:LEGACY -->" in content
    if state == "completed" and legacy:
        return
    check(managed, f"{task_md.relative_to(root)}: missing YAML frontmatter")
    task_id = frontmatter_value(content, "id")
    task_type = frontmatter_value(content, "type")
    modern = bool(task_id and task_type)
    if modern:
        check(task_id == task_dir.name, f"{task_md.relative_to(root)}: id must match directory name")
        allowed_types = {"task", "standalone", "epic_task"} if state == "completed" else {"task", "standalone"}
        check(task_type in allowed_types, f"{task_md.relative_to(root)}: invalid type {task_type!r}")
    else:
        check(False, f"{task_md.relative_to(root)}: id and type are required; mark intentional pre-lifecycle records with LIFECYCLE:LEGACY")
    check(field_has_value(content, "test_criteria"), f"{task_md.relative_to(root)}: missing or empty test_criteria")
    for key in ("summary", "depends_on", "blocked_by", "created"):
        check(field_has_value(content, key), f"{task_md.relative_to(root)}: missing or empty {key}")
    status = frontmatter_value(content, "status")
    allowed = {"planned", "in_progress", "blocked", "completed"}
    check(status in allowed, f"{task_md.relative_to(root)}: invalid task status {status!r}")
    if not enforce_folder_state:
        return
    if state == "completed":
        check(status == "completed", f"{task_md.relative_to(root)}: completed folder requires status: completed")
    elif state == "future":
        check(status == "planned", f"{task_md.relative_to(root)}: future folder requires status: planned")
    else:
        check(status in {"in_progress", "blocked"}, f"{task_md.relative_to(root)}: current folder requires in_progress or blocked status")


def validate_epic(epic_dir: Path, state: str) -> None:
    task_md = epic_dir / "task.md"
    legacy = (epic_dir / "LEGACY.md").exists()
    if state != "completed" or not legacy:
        check(task_md.exists(), f"{epic_dir.relative_to(root)}: missing task.md")
        if task_md.exists():
            content = read(task_md)
            status = frontmatter_value(content, "status")
            check(frontmatter_value(content, "id") == epic_dir.name, f"{task_md.relative_to(root)}: id must match directory name")
            check(frontmatter_value(content, "type") == "epic", f"{task_md.relative_to(root)}: type must be epic")
            for key in ("summary", "goal", "created"):
                check(field_has_value(content, key), f"{task_md.relative_to(root)}: missing or empty {key}")
            expected = "completed" if state == "completed" else "planned" if state == "future" else None
            if expected:
                check(status == expected, f"{task_md.relative_to(root)}: expected status: {expected}")
            else:
                check(status in {"in_progress", "blocked"}, f"{task_md.relative_to(root)}: current epic requires in_progress or blocked status")
    check((epic_dir / "prd.md").exists(), f"{epic_dir.relative_to(root)}: missing prd.md")
    check((epic_dir / "kanban.md").exists(), f"{epic_dir.relative_to(root)}: missing kanban.md")
    tasks_subdir = epic_dir / "tasks"
    if tasks_subdir.exists():
        for task_dir in sorted(tasks_subdir.iterdir()):
            if task_dir.is_dir():
                validate_task(task_dir, state, enforce_folder_state=state in {"future", "completed"})


def validate_task_tree() -> None:
    for state in ("current", "future", "completed"):
        state_path = root / "tasks" / state
        check(state_path.exists(), f"tasks/{state} is missing")
        if not state_path.exists():
            continue
        for entry in sorted(state_path.iterdir()):
            if not entry.is_dir() or entry.name.startswith("."):
                continue
            if entry.name.startswith("epic-"):
                validate_epic(entry, state)
            elif entry.name.startswith("task-"):
                validate_task(entry, state)
            else:
                check(False, f"{entry.relative_to(root)}: task directory must start with task- or epic-")


def validate_docs() -> None:
    for relative in REQUIRED_DOCS:
        check((root / relative).exists(), f"{relative} is missing")

    for relative, minimum_words in (("docs/VISION.md", 80), ("docs/OVERVIEW.md", 80)):
        path = root / relative
        if path.exists():
            words = re.findall(r"\b\w+\b", read(path))
            check(len(words) >= minimum_words, f"{relative} is not substantive ({len(words)} words)")
    vision = read(root / "docs" / "VISION.md")
    vision_headings = ("What This Platform Is", "What It Is Not", "Core Thesis", "Architecture Layers", "Governing Design Principles", "Target State")
    for heading in vision_headings:
        heading_pattern = rf"(?m)^## {re.escape(heading)}[^\n]*$"
        check(bool(re.search(heading_pattern, vision)), f"docs/VISION.md: missing required section {heading}")
        section = re.search(rf"(?ms)^## {re.escape(heading)}[^\n]*$\n(.*?)(?=^## |\Z)", vision)
        words = re.findall(r"\b\w+\b", section.group(1) if section else "")
        check(len(words) >= 12, f"docs/VISION.md: section {heading} is not substantive")
    overview = read(root / "docs" / "OVERVIEW.md")
    for heading in ("Architecture", "Execution Flow", "Directory Structure", "Key Contracts"):
        heading_pattern = rf"(?m)^## {re.escape(heading)}[^\n]*$"
        check(bool(re.search(heading_pattern, overview)), f"docs/OVERVIEW.md: missing required section {heading}")
        section = re.search(rf"(?ms)^## {re.escape(heading)}[^\n]*$\n(.*?)(?=^## |\Z)", overview)
        words = re.findall(r"\b\w+\b", section.group(1) if section else "")
        check(len(words) >= 12, f"docs/OVERVIEW.md: section {heading} is not substantive")

    placeholder_paths = [p for p in REQUIRED_DOCS if p != "docs/adr/FORMAT.md"]
    placeholder_files = [root / "AGENTS.md", *(root / p for p in placeholder_paths)]
    for path in placeholder_files:
        if not path.exists():
            continue
        content = read(path)
        for pattern in PLACEHOLDER_PATTERNS:
            check(not pattern.search(content), f"{path.relative_to(root)} contains unresolved placeholder text")

    nav_files = [root / "docs" / "NAVIGATION.md"]
    components = root / "docs" / "components"
    if components.exists():
        nav_files.extend(sorted(components.glob("*.md")))
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    navigation = read(root / "docs" / "NAVIGATION.md")
    for marker in ("Work-Area Context Map", "Primary entry points", "Tests / verification", "Decisions and active work", "Doc Trigger Table"):
        check(marker in navigation, f"docs/NAVIGATION.md: missing required routing marker {marker}")
    map_match = re.search(r"(?ms)^## Work-Area Context Map\s*$\n(.*?)(?=^## |\Z)", navigation)
    map_rows = [line for line in (map_match.group(1).splitlines() if map_match else []) if line.startswith("|") and "---" not in line]
    check(len(map_rows) >= 2 and any(line.count("|") >= 6 for line in map_rows[1:]), "docs/NAVIGATION.md: Work-Area Context Map has no populated routing row")
    for path in nav_files:
        if not path.exists():
            continue
        for target in link_pattern.findall(read(path)):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            check(resolved.exists(), f"{path.relative_to(root)}: broken local link {target}")
        text_without_links = link_pattern.sub("", read(path))
        for token in re.findall(r"`([^`]+)`", text_without_links):
            if "/" not in token or any(value in token for value in (" ", "*", "<", ">", "{{")):
                continue
            candidate = token.rstrip(".,:;")
            if candidate.startswith(("http://", "https://")):
                continue
            check((root / candidate).exists(), f"{path.relative_to(root)}: missing referenced path {candidate}")

    status_doc = read(root / "tasks" / "STATUS.md")
    current_match = re.search(r"(?ms)^## Current Work\s*$\n(.*?)(?=^## |\Z)", status_doc)
    current_section = current_match.group(1) if current_match else ""
    current_lines = [line for line in current_section.splitlines() if line.strip()]
    if "_None._" not in current_section:
        check(len(current_lines) >= 2 and current_lines[0].startswith("| Task |") and "---" in current_lines[1], "tasks/STATUS.md: Current Work table header is malformed")
    current_rows = [line for line in current_lines[2:] if line.startswith("|") and "---" not in line]
    dashboard_paths = {line.strip("|").split("|")[4].strip() for line in current_rows if len(line.strip("|").split("|")) == 5}
    actual_paths = {str(path.relative_to(root)) for path in (root / "tasks" / "current").iterdir() if path.is_dir() and path.name.startswith(("task-", "epic-"))}
    check(dashboard_paths == actual_paths, f"tasks/STATUS.md: Current Work paths differ from task tree ({dashboard_paths} != {actual_paths})")
    completed_match = re.search(r"(?ms)^## Completed Work\s*$\n(.*?)(?=^## |\Z)", status_doc)
    completed_section = completed_match.group(1) if completed_match else ""
    completed_lines = [line for line in completed_section.splitlines() if line.strip()]
    if "_None._" not in completed_section:
        check(len(completed_lines) >= 2 and completed_lines[0].startswith("| Task |") and "---" in completed_lines[1], "tasks/STATUS.md: Completed Work table header is malformed")


def setup_mode() -> str | None:
    agents = root / "AGENTS.md"
    if not agents.exists():
        return None
    match = re.search(r"\|\s*Agent setup mode\s*\|\s*([^|]+)\|", read(agents))
    return match.group(1).strip() if match else None


def validate_skills(directory: Path, label: str) -> None:
    check(directory.exists(), f"{label} skill directory is missing")
    if not directory.exists():
        return
    for skill in REQUIRED_SKILLS:
        check((directory / skill / "SKILL.md").exists(), f"{label}: missing required skill {skill}")


def validate_mode_and_skills() -> None:
    agents = root / "AGENTS.md"
    claude = root / "CLAUDE.md"
    check(agents.exists(), "AGENTS.md is missing")
    mode = setup_mode()
    check(mode in {"claude+agents", "agents-only"}, "AGENTS.md has missing or invalid Agent setup mode")
    validate_skills(root / ".agents" / "skills", ".agents")

    if mode == "claude+agents":
        check(claude.exists(), "claude+agents mode requires CLAUDE.md")
        if agents.exists() and claude.exists():
            check(read(agents) == read(claude), "CLAUDE.md and AGENTS.md must be exact mirrors")
        validate_skills(root / ".claude" / "skills", ".claude")
        if (root / ".agents" / "skills").exists() and (root / ".claude" / "skills").exists():
            agent_files = {
                p.relative_to(root / ".agents" / "skills"): p.read_bytes()
                for p in (root / ".agents" / "skills").rglob("*")
                if p.is_file()
            }
            claude_files = {
                p.relative_to(root / ".claude" / "skills"): p.read_bytes()
                for p in (root / ".claude" / "skills").rglob("*")
                if p.is_file()
            }
            check(agent_files == claude_files, ".agents/skills and .claude/skills have diverged")
    elif mode == "agents-only":
        check(not claude.exists(), "agents-only mode must not contain CLAUDE.md")
        check(not (root / ".claude").exists(), "agents-only mode must not contain .claude/")


validate_task_tree()
validate_docs()
validate_mode_and_skills()

# --- Project-specific checks (edit freely) ---------------------------------
# Add import-boundary, retired-path, schema, or naming checks below this line.

if errors:
    print("❌ Project structure validation failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(f"✅ Project structure valid ({root.name})")
