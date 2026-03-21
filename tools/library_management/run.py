#!/usr/bin/env python3
"""Library management CLI for shared-skills.

Commands:
    library-status    Show shared-skills repo status and discovered skills
    library-setup     Configure a consumer project to use shared skills
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
SKILLS_PATH = SHARED_SKILLS_DIR / ".claude" / "skills"
COMMANDS_PATH = SHARED_SKILLS_DIR / ".claude" / "commands"


def _find_skills() -> list[dict]:
    """Find all SKILL.md files and extract name + description."""
    skills = []
    if not SKILLS_PATH.exists():
        return skills
    for skill_dir in sorted(SKILLS_PATH.iterdir()):
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
    if not COMMANDS_PATH.exists():
        return []
    return sorted(p.stem for p in COMMANDS_PATH.glob("*.md"))


def _sync_symlinks(project_dir: Path) -> dict:
    """Create/update symlinks from a consumer project's .claude/skills/ to shared skills.

    Returns dict with created, existing, removed, and errors lists.
    """
    target_skills_dir = project_dir / ".claude" / "skills"
    target_skills_dir.mkdir(parents=True, exist_ok=True)

    shared_skills = {d.name for d in SKILLS_PATH.iterdir() if (d / "SKILL.md").is_file()}
    created, existing, removed, errors = [], [], [], []

    # Create/update symlinks for each shared skill
    for skill_name in sorted(shared_skills):
        link_path = target_skills_dir / skill_name
        source_path = SKILLS_PATH / skill_name

        if link_path.is_symlink():
            # Already a symlink — check if it points to the right place
            try:
                current_target = Path(os.readlink(str(link_path)))
                # Normalise for comparison
                if current_target.resolve() == source_path.resolve():
                    existing.append(skill_name)
                    continue
                # Wrong target — remove and recreate
                link_path.unlink()
            except OSError:
                link_path.unlink()
        elif link_path.exists():
            # Real directory (local skill) — skip, don't overwrite local work
            existing.append(skill_name)
            continue

        try:
            # Use forward slashes for cross-platform symlink compatibility
            os.symlink(str(source_path).replace("\\", "/"), str(link_path))
            created.append(skill_name)
        except OSError as e:
            errors.append({"skill": skill_name, "error": str(e)})

    # Remove stale symlinks that point to skills no longer in shared-skills
    for item in target_skills_dir.iterdir():
        if item.is_symlink():
            try:
                target = Path(os.readlink(str(item))).resolve()
                if str(SKILLS_PATH.resolve()) in str(target) and item.name not in shared_skills:
                    item.unlink()
                    removed.append(item.name)
            except OSError:
                pass

    # Maintain .gitignore so symlinked skills aren't tracked in the consumer repo
    _update_skills_gitignore(target_skills_dir, shared_skills)

    return {
        "created": created,
        "existing": existing,
        "removed": removed,
        "errors": errors,
    }


def _update_skills_gitignore(skills_dir: Path, shared_skill_names: set[str]):
    """Write a .gitignore in .claude/skills/ that ignores symlinked shared skills."""
    gitignore_path = skills_dir / ".gitignore"
    header = "# Symlinked shared skills (managed by library-link, do not edit)\n"

    # Read existing lines that aren't managed by us
    existing_lines = []
    in_managed_block = False
    if gitignore_path.exists():
        for line in gitignore_path.read_text(encoding="utf-8").splitlines():
            if line == header.strip():
                in_managed_block = True
                continue
            if in_managed_block:
                if line.startswith("# End shared skills"):
                    in_managed_block = False
                continue
            existing_lines.append(line)

    # Build the managed block
    managed = [header.strip()]
    for name in sorted(shared_skill_names):
        managed.append(f"{name}/")
    managed.append("# End shared skills")

    # Combine and write
    all_lines = existing_lines + [""] + managed if existing_lines else managed
    gitignore_path.write_text("\n".join(all_lines) + "\n", encoding="utf-8")


def link():
    """Create symlinks from a consumer project to shared skills.

    This is the primary mechanism for making shared skills discoverable
    by Claude Code, working around the additionalDirectories limitation.
    """
    parser = argparse.ArgumentParser(description="Symlink shared skills into a consumer project")
    parser.add_argument("project_dir", nargs="?", default=".",
                        help="Path to the consumer project root (default: current directory)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    project = Path(args.project_dir).resolve()
    if not project.is_dir():
        print(f"Error: {project} is not a directory", file=sys.stderr)
        sys.exit(1)

    result = _sync_symlinks(project)

    if args.json:
        print(json.dumps({"project": str(project), **result}, indent=2))
    else:
        if result["created"]:
            print(f"Linked {len(result['created'])} skill(s):")
            for s in result["created"]:
                print(f"  + {s}")
        if result["existing"]:
            print(f"Already present: {len(result['existing'])} skill(s)")
        if result["removed"]:
            print(f"Removed stale: {len(result['removed'])} symlink(s)")
            for s in result["removed"]:
                print(f"  - {s}")
        if result["errors"]:
            print(f"Errors: {len(result['errors'])}")
            for e in result["errors"]:
                print(f"  ! {e['skill']}: {e['error']}")
        if not result["created"] and not result["removed"]:
            print("All shared skills already linked.")


def status():
    """Show shared-skills repo status and discovered skills."""
    parser = argparse.ArgumentParser(description="Shared-skills repo status")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    skills = _find_skills()
    commands = _find_commands()

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
        "skill_count": len(skills),
        "command_count": len(commands),
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

    Creates/updates .claude/settings.json with additionalDirectories
    and registers the SessionStart verification hook.
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

    # Create symlinks for skill discovery
    link_result = _sync_symlinks(project)

    result = {
        "project": str(project),
        "settings_path": str(settings_path),
        "shared_skills_dir": shared_path,
        "additionalDirectories_added": shared_path not in add_dirs,
        "hook_added": not already_has,
        "skills_linked": link_result["created"],
        "skills_existing": link_result["existing"],
        "link_errors": link_result["errors"],
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Configured: {project}")
        print(f"  Settings: {settings_path}")
        print(f"  additionalDirectories: {shared_path}")
        print(f"  SessionStart hook: {'added' if not already_has else 'already present'}")
        if link_result["created"]:
            print(f"  Skills linked: {len(link_result['created'])}")
            for s in link_result["created"]:
                print(f"    + {s}")
        else:
            print(f"  Skills: {len(link_result['existing'])} already linked")
        if link_result["errors"]:
            for e in link_result["errors"]:
                print(f"  ! {e['skill']}: {e['error']}")
        print(f"\nRestart Claude Code in {project} to pick up shared skills.")


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
    link_result = {}
    if (project / ".claude" / "skills").exists():
        link_result = _sync_symlinks(project)

    if args.json:
        print(json.dumps({
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
            "returncode": result.returncode,
            "skills": _find_skills(),
            "symlinks": link_result,
        }, indent=2))
    else:
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        skills = _find_skills()
        print(f"\nAvailable skills ({len(skills)}):")
        for s in skills:
            print(f"  {s['name']}")
        if link_result.get("created"):
            print(f"\nNew skills linked: {', '.join(link_result['created'])}")
        if link_result.get("removed"):
            print(f"Stale symlinks removed: {', '.join(link_result['removed'])}")
