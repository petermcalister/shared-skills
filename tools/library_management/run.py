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

    result = {
        "project": str(project),
        "settings_path": str(settings_path),
        "shared_skills_dir": shared_path,
        "additionalDirectories_added": shared_path not in add_dirs,
        "hook_added": not already_has,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Configured: {project}")
        print(f"  Settings: {settings_path}")
        print(f"  additionalDirectories: {shared_path}")
        print(f"  SessionStart hook: {'added' if not already_has else 'already present'}")
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
    """Pull latest shared skills from remote."""
    parser = argparse.ArgumentParser(description="Sync shared skills")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    result = subprocess.run(
        ["git", "pull", "--rebase"],
        capture_output=True, text=True, cwd=str(SHARED_SKILLS_DIR),
    )

    if args.json:
        print(json.dumps({
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
            "returncode": result.returncode,
            "skills": _find_skills(),
        }, indent=2))
    else:
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        skills = _find_skills()
        print(f"\nAvailable skills ({len(skills)}):")
        for s in skills:
            print(f"  {s['name']}")
