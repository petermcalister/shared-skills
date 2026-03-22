#!/usr/bin/env python3
"""Library management CLI for shared-skills.

Commands:
    library-status    Show shared-skills repo status and discovered content
    library-setup     Configure a consumer project to use shared skills
    library-link      Create/refresh symlinks for all shared content
    library-verify    Verify skill discovery in a consumer project
    library-push      Commit and push shared-skills changes
    library-sync      Pull latest shared skills from remote
    library-list      List all available shared skills
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Resolve shared-skills repo root (parent of tools/)
SHARED_SKILLS_DIR = Path(__file__).resolve().parent.parent.parent

# The shared content locations
SHARED_LOCATIONS = {
    "skills": {
        "shared": SHARED_SKILLS_DIR / ".claude" / "skills",
        "local": ".claude/skills",
        "detect": lambda p: (p / "SKILL.md").is_file(),  # skills are directories with SKILL.md
        "is_dir": True,
    },
    "agents": {
        "shared": SHARED_SKILLS_DIR / ".claude" / "agents",
        "local": ".claude/agents",
        "detect": lambda p: p.suffix == ".md",  # agents are .md files
        "is_dir": False,
    },
    "commands": {
        "shared": SHARED_SKILLS_DIR / ".claude" / "commands",
        "local": ".claude/commands",
        "detect": lambda p: p.suffix == ".md",  # commands are .md files
        "is_dir": False,
    },
    "tools": {
        "shared": SHARED_SKILLS_DIR / "tools",
        "local": "tools",
        "detect": lambda p: (p / "run.py").is_file(),  # tools are directories with run.py
        "is_dir": True,
    },
}


def _find_shared_items(location: str) -> set[str]:
    """Find all shared items in a location."""
    loc = SHARED_LOCATIONS[location]
    shared_path = loc["shared"]
    if not shared_path.exists():
        return set()

    if loc["is_dir"]:
        return {d.name for d in shared_path.iterdir() if d.is_dir() and loc["detect"](d)}
    else:
        return {f.name for f in shared_path.iterdir() if loc["detect"](f)}


def _find_skills() -> list[dict]:
    """Find all SKILL.md files and extract name + description."""
    skills = []
    skills_path = SHARED_LOCATIONS["skills"]["shared"]
    if not skills_path.exists():
        return skills
    for skill_dir in sorted(skills_path.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        name = skill_dir.name
        description = ""
        content = skill_md.read_text(encoding="utf-8")
        # Parse YAML frontmatter
        lines = content.split("\n")
        if lines[0].strip() == "---":
            for line in lines[1:]:
                if line.strip() == "---":
                    break
                if line.startswith("description:"):
                    val = line[len("description:"):].strip()
                    if val in (">", "|", ">-", "|-"):
                        continue
                    description = val.strip('"').strip("'")
                elif description == "" and line.startswith("  "):
                    description += " " + line.strip()
        skills.append({"name": name, "description": description[:100], "path": str(skill_dir)})
    return skills


def _find_commands() -> list[str]:
    """Find all slash command .md files."""
    commands_path = SHARED_LOCATIONS["commands"]["shared"]
    if not commands_path.exists():
        return []
    return sorted(p.stem for p in commands_path.glob("*.md"))


def _is_junction(path: Path) -> bool:
    """Check if a path is a Windows directory junction."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        FILE_ATTRIBUTE_REPARSE_POINT = 0x0400
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
        return attrs != -1 and bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
    except Exception:
        return False


def _junction_target(path: Path) -> Path | None:
    """Resolve the target of a Windows directory junction."""
    try:
        return path.resolve()
    except OSError:
        return None


def _create_junction(link_path: Path, target_path: Path):
    """Create a Windows directory junction via PowerShell."""
    subprocess.run(
        ["powershell", "-NoProfile", "-c",
         f"New-Item -ItemType Junction -Path '{link_path}' -Target '{target_path}'"],
        capture_output=True, check=True,
    )


def _sync_location(project_dir: Path, location: str, repair: bool = False) -> dict:
    """Sync symlinks/junctions for a single shared content location.

    Returns dict with created, existing, removed, repaired, and errors lists.
    On Windows, uses directory junctions (no elevation required) for
    directories and file copies for files, falling back from os.symlink().

    If repair=True, plain directories/files that match shared items are
    replaced with proper symlinks/junctions/copies.
    """
    loc = SHARED_LOCATIONS[location]
    shared_path = loc["shared"]
    target_dir = project_dir / loc["local"]

    if not shared_path.exists():
        return {"created": [], "existing": [], "removed": [], "repaired": [], "errors": []}

    target_dir.mkdir(parents=True, exist_ok=True)

    shared_items = _find_shared_items(location)
    created, existing, removed, repaired, errors = [], [], [], [], []

    for item_name in sorted(shared_items):
        link_path = target_dir / item_name
        source_path = shared_path / item_name

        # Check for existing symlink or junction
        if link_path.is_symlink() or _is_junction(link_path):
            try:
                current_target = link_path.resolve()
                if current_target == source_path.resolve():
                    existing.append(item_name)
                    continue
                # Points elsewhere — remove and re-create
                if link_path.is_symlink():
                    link_path.unlink()
                else:
                    # Junctions must be removed as directories
                    link_path.rmdir()
            except OSError:
                if link_path.is_symlink():
                    link_path.unlink()
                elif link_path.exists():
                    link_path.rmdir()
        elif link_path.exists():
            if repair:
                # Replace stale plain copy with proper link
                import shutil
                if link_path.is_dir():
                    shutil.rmtree(str(link_path))
                else:
                    link_path.unlink()
                repaired.append(item_name)
            else:
                # Real file/directory — skip, don't overwrite local work
                existing.append(item_name)
                continue

        # Create link: try symlink first, fall back on Windows to
        # directory junctions (dirs) or hardlinks (files) — both write through
        try:
            os.symlink(str(source_path).replace("\\", "/"), str(link_path),
                        target_is_directory=loc["is_dir"])
            created.append(item_name)
        except OSError:
            try:
                if loc["is_dir"] and sys.platform == "win32":
                    _create_junction(link_path, source_path)
                    created.append(item_name)
                elif not loc["is_dir"]:
                    # Hardlink: no elevation needed, writes through in both directions
                    os.link(str(source_path), str(link_path))
                    created.append(item_name)
                else:
                    raise
            except Exception as e2:
                errors.append({"item": item_name, "error": str(e2)})

    # Remove stale symlinks/junctions pointing into shared-skills
    for item in target_dir.iterdir():
        is_link = item.is_symlink() or _is_junction(item)
        if is_link:
            try:
                target = item.resolve()
                if str(shared_path.resolve()) in str(target) and item.name not in shared_items:
                    if item.is_symlink():
                        item.unlink()
                    else:
                        item.rmdir()
                    removed.append(item.name)
            except OSError:
                pass

    # Maintain .gitignore
    _update_gitignore(target_dir, shared_items, location)

    return {
        "created": created,
        "existing": existing,
        "removed": removed,
        "repaired": repaired,
        "errors": errors,
    }


def _sync_all_locations(project_dir: Path, repair: bool = False) -> dict:
    """Sync symlinks for all shared content locations."""
    results = {}
    for location in SHARED_LOCATIONS:
        results[location] = _sync_location(project_dir, location, repair=repair)
    return results


def _update_gitignore(target_dir: Path, shared_names: set[str], location: str):
    """Write a .gitignore in the target dir that ignores symlinked shared content."""
    gitignore_path = target_dir / ".gitignore"
    header = f"# Shared {location} (managed by library-link, do not edit)"
    footer = f"# End shared {location}"

    # Legacy headers to clean up from earlier versions
    legacy_headers = [
        f"# Symlinked shared {location} (managed by library-link, do not edit)",
    ]
    legacy_footers = [
        f"# End shared {location}",
    ]

    # Read existing lines outside any managed block (current or legacy)
    all_headers = [header] + legacy_headers
    existing_lines = []
    in_managed_block = False
    if gitignore_path.exists():
        for line in gitignore_path.read_text(encoding="utf-8").splitlines():
            if line in all_headers:
                in_managed_block = True
                continue
            if in_managed_block:
                if line in legacy_footers or line == footer:
                    in_managed_block = False
                continue
            existing_lines.append(line)

    # Build the managed block
    loc = SHARED_LOCATIONS[location]
    suffix = "/" if loc["is_dir"] else ""
    managed = [header]
    for name in sorted(shared_names):
        managed.append(f"{name}{suffix}")
    managed.append(footer)

    # Strip trailing blank lines from existing content
    while existing_lines and existing_lines[-1].strip() == "":
        existing_lines.pop()

    all_lines = existing_lines + [""] + managed if existing_lines else managed
    gitignore_path.write_text("\n".join(all_lines) + "\n", encoding="utf-8")


def _print_sync_results(results: dict):
    """Print human-readable sync results across all locations."""
    total_created = 0
    total_existing = 0
    total_repaired = 0
    for location, result in results.items():
        if result.get("repaired"):
            total_repaired += len(result["repaired"])
            print(f"  {location}: repaired {len(result['repaired'])}")
            for item in result["repaired"]:
                print(f"    ~ {item}")
        if result["created"]:
            total_created += len(result["created"])
            print(f"  {location}: linked {len(result['created'])}")
            for item in result["created"]:
                print(f"    + {item}")
        if result["removed"]:
            print(f"  {location}: removed {len(result['removed'])} stale")
            for item in result["removed"]:
                print(f"    - {item}")
        if result["errors"]:
            for e in result["errors"]:
                print(f"  ! {location}/{e['item']}: {e['error']}")
        total_existing += len(result["existing"])

    if total_created == 0 and total_repaired == 0 and not any(r["removed"] for r in results.values()):
        print(f"All shared content already linked ({total_existing} items).")


def link():
    """Create symlinks from a consumer project to all shared content.

    Symlinks .claude/skills/, .claude/agents/, and .claude/commands/ from
    the shared-skills repo into the consumer project. Manages .gitignore
    in each directory to prevent symlinked content from being tracked.
    """
    parser = argparse.ArgumentParser(description="Symlink shared content into a consumer project")
    parser.add_argument("project_dir", nargs="?", default=".",
                        help="Path to the consumer project root (default: current directory)")
    parser.add_argument("--repair", action="store_true",
                        help="Replace plain directory/file copies with proper symlinks/junctions")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    project = Path(args.project_dir).resolve()
    if not project.is_dir():
        print(f"Error: {project} is not a directory", file=sys.stderr)
        sys.exit(1)

    results = _sync_all_locations(project, repair=args.repair)

    if args.json:
        print(json.dumps({"project": str(project), **results}, indent=2))
    else:
        _print_sync_results(results)


def status():
    """Show shared-skills repo status and discovered content."""
    parser = argparse.ArgumentParser(description="Shared-skills repo status")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    skills = _find_skills()
    commands = _find_commands()
    agents = sorted(_find_shared_items("agents"))
    tools = sorted(_find_shared_items("tools"))

    # Git status
    dirty = False
    branch = "unknown"
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=str(SHARED_SKILLS_DIR),
        )
        dirty = bool(result.stdout.strip())
        result2 = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=str(SHARED_SKILLS_DIR),
        )
        branch = result2.stdout.strip()
    except Exception:
        pass

    output = {
        "repo": str(SHARED_SKILLS_DIR),
        "branch": branch,
        "dirty": dirty,
        "skills": skills,
        "commands": commands,
        "agents": agents,
        "tools": tools,
        "skill_count": len(skills),
        "command_count": len(commands),
        "agent_count": len(agents),
        "tool_count": len(tools),
    }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Shared Skills: {SHARED_SKILLS_DIR}")
        print(f"Branch: {branch}{'  (uncommitted changes)' if dirty else ''}")
        print(f"\nSkills ({len(skills)}):")
        for s in skills:
            print(f"  {s['name']}")
        print(f"\nCommands ({len(commands)}):")
        for c in commands:
            print(f"  /{c}")
        print(f"\nAgents ({len(agents)}):")
        for a in agents:
            print(f"  {a}")
        print(f"\nTools ({len(tools)}):")
        for t in tools:
            print(f"  {t}")


def list_skills():
    """List all available shared skills with descriptions."""
    parser = argparse.ArgumentParser(description="List shared skills")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    skills = _find_skills()

    if args.json:
        print(json.dumps(skills, indent=2))
    else:
        for s in skills:
            print(f"  {s['name']:<25} {s['description']}")


def setup():
    """Configure a consumer project to use shared skills.

    Creates/updates .claude/settings.json with additionalDirectories,
    registers the SessionStart verification hook, and creates symlinks
    for all shared content (skills, agents, commands).
    """
    parser = argparse.ArgumentParser(description="Set up shared skills in a consumer project")
    parser.add_argument("project_dir", help="Path to the consumer project root")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    project = Path(args.project_dir).resolve()
    if not project.is_dir():
        print(f"Error: {project} is not a directory", file=sys.stderr)
        sys.exit(1)

    claude_dir = project / ".claude"
    claude_dir.mkdir(exist_ok=True)
    settings_path = claude_dir / "settings.json"
    shared_path = str(SHARED_SKILLS_DIR).replace("\\", "/")

    # Load or create settings
    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    else:
        settings = {}

    # Merge additionalDirectories
    perms = settings.setdefault("permissions", {})
    add_dirs = perms.setdefault("additionalDirectories", [])
    if shared_path not in add_dirs:
        add_dirs.append(shared_path)

    # Add SessionStart hook
    hooks = settings.setdefault("hooks", {})
    verify_cmd = f"bash {shared_path}/scripts/verify-shared-skills.sh"
    session_hooks = hooks.get("SessionStart", [])

    # Check if hook already exists
    already_has = any(
        verify_cmd in str(h)
        for hook_group in session_hooks
        for h in hook_group.get("hooks", [])
    )

    if not already_has:
        session_hooks.append({
            "hooks": [{
                "type": "command",
                "command": verify_cmd,
            }]
        })
        hooks["SessionStart"] = session_hooks

    # Write settings
    settings_path.write_text(json.dumps(settings, indent=2), encoding="utf-8")

    # Create symlinks for all shared content
    link_results = _sync_all_locations(project)

    result = {
        "project": str(project),
        "settings_path": str(settings_path),
        "shared_skills_dir": shared_path,
        "additionalDirectories_added": shared_path not in add_dirs,
        "hook_added": not already_has,
        "links": link_results,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Configured: {project}")
        print(f"  Settings: {settings_path}")
        print(f"  additionalDirectories: {shared_path}")
        print(f"  SessionStart hook: {'added' if not already_has else 'already present'}")
        _print_sync_results(link_results)
        print(f"\nRestart Claude Code in {project} to pick up shared content.")


def verify():
    """Verify skill discovery (runs the verification script)."""
    script = SHARED_SKILLS_DIR / "scripts" / "verify-shared-skills.sh"
    if not script.exists():
        print(f"Error: {script} not found", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run(["bash", str(script)], cwd=str(SHARED_SKILLS_DIR))
    sys.exit(result.returncode)


def push():
    """Commit and push shared-skills changes."""
    parser = argparse.ArgumentParser(description="Push shared-skills changes")
    parser.add_argument("message", nargs="?", default="Update shared skills", help="Commit message")
    args = parser.parse_args()

    # Check for changes
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=str(SHARED_SKILLS_DIR),
    )
    if not result.stdout.strip():
        print("No changes to push in shared-skills")
        return

    print("Changes:")
    subprocess.run(["git", "status", "--short"], cwd=str(SHARED_SKILLS_DIR))
    print()

    subprocess.run(["git", "add", "-A"], cwd=str(SHARED_SKILLS_DIR))
    subprocess.run(["git", "commit", "-m", args.message], cwd=str(SHARED_SKILLS_DIR))
    subprocess.run(["git", "push"], cwd=str(SHARED_SKILLS_DIR))


def sync():
    """Pull latest shared skills from remote and refresh symlinks."""
    parser = argparse.ArgumentParser(description="Sync shared skills")
    parser.add_argument("--project", default=".", help="Consumer project to refresh symlinks in")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    result = subprocess.run(
        ["git", "pull", "--rebase"],
        capture_output=True, text=True, cwd=str(SHARED_SKILLS_DIR),
    )

    # Refresh symlinks in the consumer project
    project = Path(args.project).resolve()
    link_results = {}
    if (project / ".claude").exists():
        link_results = _sync_all_locations(project)

    if args.json:
        print(json.dumps({
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
            "returncode": result.returncode,
            "skills": _find_skills(),
            "symlinks": link_results,
        }, indent=2))
    else:
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        skills = _find_skills()
        print(f"\nAvailable skills ({len(skills)}):")
        for s in skills:
            print(f"  {s['name']}")
        if link_results:
            print()
            _print_sync_results(link_results)
