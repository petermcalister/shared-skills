---
name: library-management
description: >
  Use this skill when setting up shared skills in a new repo, connecting a project to the
  shared library, troubleshooting skill discovery, or managing the shared-skills lifecycle.
  Trigger on: "set up shared skills", "connect this project to shared-skills", "why isn't
  my skill showing up", "add this to the shared library", "push skills", "sync skills",
  "how do shared skills work", or any question about additionalDirectories, skill discovery,
  or the shared-skills repo.
version: 0.4.0
---

# Shared Library Management

Manage the shared skill library. All repos live under `~/RepoBase/`.

The shared-skills repo lives at `~/RepoBase/shared-skills/`. Consumer projects use
symlinks from their `.claude/skills/` to the shared repo's skills, making them
discoverable by Claude Code's skill scanner.

The `additionalDirectories` setting in `settings.json` grants file access to the
shared-skills directory. Symlinks handle skill discovery. Both are set up automatically
by `library-setup`.

---

## Setting Up a Consumer Project

### Option A: CLI (preferred)

```bash
library-setup ~/RepoBase/some-project
```

This does three things:
1. Merges `additionalDirectories` into the project's `.claude/settings.json`
2. Adds a `SessionStart` verification hook
3. Creates symlinks from `.claude/skills/` to each shared skill

### Option B: Manual

1. Add `additionalDirectories` and the SessionStart hook to `.claude/settings.json`:

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

Replace `~` with the actual home directory path for the platform.

2. Create symlinks for each shared skill:

```bash
library-link ~/RepoBase/some-project
```

### After setup

Restart Claude Code in the consumer project. The SessionStart hook reports discovered
skills, and `/context` shows them in the skill list.

---

## Refreshing Symlinks

When skills are added or removed in the shared repo, consumer projects need their
symlinks updated. Two ways to do this:

```bash
library-link ~/RepoBase/some-project    # Just refresh symlinks
library-sync --project ~/RepoBase/some-project  # Git pull + refresh symlinks
```

Both commands are idempotent — they create missing symlinks, skip existing ones,
and remove stale symlinks pointing to deleted shared skills.

---

## Removing a Git Submodule (Migration)

If the project previously used a submodule for shared-skills:

```bash
git submodule deinit -f .claude/skills/shared
git rm -f .claude/skills/shared
rm -rf .git/modules/.claude/skills/shared
git commit -m "Remove shared-skills submodule (replaced by symlinks)"
```

Then run `library-link` to create symlinks for all shared skills.

---

## CLI Tools

Install: `pip install -e ~/RepoBase/shared-skills`

| Command | Purpose |
|---------|---------|
| `library-status [--json]` | Repo status, branch, discovered skills + commands |
| `library-setup <dir>` | Full setup: settings.json + hook + symlinks |
| `library-link [dir] [--json]` | Create/refresh symlinks only (default: current dir) |
| `library-list [--json]` | List all shared skills with descriptions |
| `library-verify` | Run the discovery verification script |
| `library-push ["msg"]` | Git add + commit + push shared-skills |
| `library-sync [--project dir] [--json]` | Git pull + refresh symlinks |

---

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/push-skills` | Commit + push shared-skills without leaving your project |
| `/sync-all` | Pull latest + list skills |

---

## Adding a New Skill

1. Create the directory in shared-skills: `mkdir -p .claude/skills/new-skill`
2. Write `SKILL.md` with YAML frontmatter (`name`, `description`, `version`)
3. Optionally add `evals/trigger-eval.json` and `references/`
4. Push: `library-push "Added new-skill"` or `/push-skills`
5. In consumer projects: `library-link` to pick up the new skill

### Skill directory convention

```
.claude/skills/<name>/
├── SKILL.md                    <- required
├── evals/
│   ├── trigger-eval.json       <- eval queries (committed)
│   └── results/                <- eval outputs (gitignored)
├── variants/A/ and B/          <- A/B testing
├── scripts/                    <- skill-specific scripts
└── references/                 <- skill-specific docs
```

---

## Troubleshooting

**Skills don't appear in `/context`:**
- Run `library-link` to create/refresh symlinks
- Skills must be at `.claude/skills/<name>/SKILL.md` (exactly one level deep)
- Symlinks must point to valid shared-skills directories

**Duplicate skills showing:**
- If a local skill has the same name as a shared one, the local copy takes precedence
- Remove the local copy if you want the shared version

**Hook doesn't fire:**
- `SessionStart` is case-sensitive in the hooks config
- Verify the script exists at the path specified in the hook

**Changes not picked up:**
- Shared-skills edits are live (symlinks follow the source files)
- New shared skills need `library-link` to create the symlink
- Removed shared skills: `library-link` cleans up stale symlinks

**Symlink errors on Windows:**
- Git Bash `ln -s` works on Windows 10+ with Developer Mode enabled
- If symlinks fail, check Windows Settings > Developer Mode is ON
