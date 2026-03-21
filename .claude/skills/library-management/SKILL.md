---
name: library-management
description: >
  Use this skill when setting up shared skills in a new repo, connecting a project to the
  shared library, troubleshooting skill discovery, or managing the shared-skills lifecycle.
  Trigger on: "set up shared skills", "connect this project to shared-skills", "why isn't
  my skill showing up", "add this to the shared library", "push skills", "sync skills",
  "how do shared skills work", or any question about additionalDirectories, skill discovery,
  or the shared-skills repo.
version: 0.3.0
---

# Shared Library Management

Manage the shared skill library. All repos live under `~/RepoBase/`.

The shared-skills repo lives at `~/RepoBase/shared-skills/`. Consumer projects include it
via `additionalDirectories` — Claude Code scans the additional directory's `.claude/skills/`
and `.claude/commands/`, making everything discoverable without submodules or symlinks.

This works because `additionalDirectories` tells Claude Code to treat another directory
as if its `.claude/` contents were part of the current project. Skills, commands, and
hooks from the shared repo appear alongside the project's own, with zero duplication.

---

## Setting Up a Consumer Project

### Option A: CLI (preferred)

```bash
library-setup ~/RepoBase/some-project
```

This merges `additionalDirectories` and a `SessionStart` verification hook into the
project's `.claude/settings.json`, preserving any existing settings.

### Option B: Manual

Read the project's `.claude/settings.json` (create if missing). **Merge** these keys
into the existing JSON — don't replace existing `permissions`, `hooks`, or other settings:

```json
{
  "permissions": {
    "additionalDirectories": [
      "~/RepoBase/shared-skills"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/RepoBase/shared-skills/scripts/verify-shared-skills.sh"
          }
        ]
      }
    ]
  }
}
```

Replace `~` with the actual home directory path for the platform (e.g., `C:/Users/peter`
on Windows, `/home/pete` on Linux).

### After setup

Restart Claude Code in the consumer project. The SessionStart hook reports discovered skills.

---

## Removing a Git Submodule (Migration)

If the project previously used a submodule for shared-skills:

```bash
git submodule deinit -f .claude/skills/shared
git rm -f .claude/skills/shared
rm -rf .git/modules/.claude/skills/shared
git commit -m "Remove shared-skills submodule (replaced by additionalDirectories)"
```

Then remove any duplicate skills from `.claude/skills/` that now come from shared-skills.

---

## CLI Tools

Registered in `pyproject.toml` — run with `poetry run <command>` or install the package:

| Command | Purpose |
|---------|---------|
| `library-status [--json]` | Repo status, branch, discovered skills + commands |
| `library-setup <dir>` | Auto-configure a consumer project's settings.json |
| `library-list [--json]` | List all shared skills with descriptions |
| `library-verify` | Run the discovery verification script |
| `library-push ["msg"]` | Git add + commit + push shared-skills |
| `library-sync [--json]` | Git pull + list available skills |

---

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/push-skills` | Commit + push shared-skills without leaving your project |
| `/sync-all` | Pull latest + list skills |

---

## Adding a New Skill

1. Create the directory: `mkdir -p .claude/skills/new-skill`
2. Write `SKILL.md` with YAML frontmatter (`name`, `description`, `version`)
3. Optionally add `evals/trigger-eval.json` and `references/`
4. Push: `library-push "Added new-skill"` or `/push-skills`

### Skill directory convention

```
.claude/skills/<name>/
├── SKILL.md                    ← required
├── evals/
│   ├── trigger-eval.json       ← eval queries (committed)
│   └── results/                ← eval outputs (gitignored)
├── variants/A/ and B/          ← A/B testing
├── scripts/                    ← skill-specific scripts
└── references/                 ← skill-specific docs
```

---

## Troubleshooting

**Skills don't appear in `/skills`:**
- Verify `additionalDirectories` path is correct and absolute in settings.json
- Run `library-verify` to check discovery
- Skills must be at `.claude/skills/<name>/SKILL.md` (exactly one level deep)

**Duplicate skills showing:**
- Remove the local copy from the consumer project's `.claude/skills/`

**Hook doesn't fire:**
- `SessionStart` is case-sensitive in the hooks config
- Verify the script exists at the path specified in the hook

**Changes not picked up:**
- Shared-skills workspace: changes are live (no restart)
- Consumer projects: may need restart for new skills; `/sync-all` pulls latest
