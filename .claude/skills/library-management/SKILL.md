---
name: library-management
description: >
  Use this skill when setting up shared skills in a new repo, connecting a project to the
  shared library, troubleshooting skill discovery, or managing the shared-skills lifecycle.
  Trigger on: "set up shared skills", "connect this project to shared-skills", "why isn't
  my skill showing up", "add this to the shared library", "push skills", "sync skills",
  "how do shared skills work", or any question about additionalDirectories, skill discovery,
  or the shared-skills repo.
version: 0.5.0
---

# Shared Library Management

Manage the shared skill library. All repos live under `~/RepoBase/`.

The shared-skills repo lives at `~/RepoBase/shared-skills/`. Three types of content
are shared: **skills** (directories), **agents** (.md files), and **commands** (.md files).

Consumer projects use symlinks/junctions from their `.claude/skills/`, `.claude/agents/`,
and `.claude/commands/` to the shared repo, making content discoverable by Claude Code.

The `additionalDirectories` setting in `settings.json` grants file access to the
shared-skills directory. Symlinks/junctions handle discovery. Both are set up
automatically by `library-setup`.

### Prerequisites

The CLI tools must be installed once as a global editable package:

```bash
pip install -e ~/RepoBase/shared-skills
```

This makes all `library-*` commands available system-wide. This is required before
`library-setup` or `library-link` can be used.

### Windows behavior

On Windows, `os.symlink()` requires Developer Mode or elevation. The tools
automatically fall back to:
- **Directory junctions** for skills — write-through, no elevation needed
- **Hardlinks** for agents/commands — write-through, no elevation needed

All shared content writes through to the shared-skills repo from any consumer
project. Edits made anywhere are immediately visible everywhere.

---

## Setting Up a Consumer Project

### Option A: CLI (preferred)

```bash
library-setup ~/RepoBase/some-project
```

This does four things:
1. Merges `additionalDirectories` into the project's `.claude/settings.json`
2. Adds a `SessionStart` verification hook
3. Creates symlinks/junctions for all shared content (skills, agents, commands)
4. **You must then** add a "Shared Skills Library" section to the project's CLAUDE.md (see template below)

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

### After setup: Update the consumer project's CLAUDE.md

After running `library-setup` or `library-link`, **always** add or update a
"Shared Skills Library" section in the consumer project's CLAUDE.md. Without this,
future Claude Code sessions won't understand the shared content architecture.

Run `library-status --json` to get current counts, then add a section like this
(adapt counts/names to what's actually linked):

~~~markdown
## Shared Skills Library

This project uses a shared-skills repo at `~/RepoBase/shared-skills/` for reusable
skills, agents, commands, and tools. Content is symlinked/junctioned into:

| Local path | Shared source | What's shared |
|------------|--------------|---------------|
| `.claude/skills/` | `shared-skills/.claude/skills/` | N skills (list key ones) |
| `.claude/agents/` | `shared-skills/.claude/agents/` | N agents |
| `.claude/commands/` | `shared-skills/.claude/commands/` | N commands |

### How it works

- **Symlinks/junctions** make shared content discoverable as if it were local
- **`.gitignore`** files in each directory (managed by `library-link`) prevent
  symlinked content from being tracked in this repo
- **`additionalDirectories`** in `.claude/settings.json` grants file read access
  to the shared-skills repo
- **Edits** write through to the shared-skills repo (junctions for skills, hardlinks for agents/commands)

### Key commands

```bash
library-link .                        # Create/refresh all symlinks
library-link . --repair               # Replace stale copies with proper links
library-push "description"            # Commit + push shared-skills changes
library-sync --project .              # Git pull shared-skills + refresh symlinks
library-status                        # Show shared repo status
```

### Commit workflow

Shared content lives in the shared-skills repo. Edits made via symlinks/junctions
are committed there, not here:

```bash
# After editing a shared skill/agent/command:
library-push "Improved systematic-debugging triggers"
```

Local-only content (e.g. project-specific commands or skills) is committed to
this repo normally.
~~~

Then restart Claude Code in the consumer project. The SessionStart hook reports
discovered skills, and `/context` shows them in the skill list.

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

| Command | Purpose |
|---------|---------|
| `library-status [--json]` | Repo status, branch, discovered skills/agents/commands |
| `library-setup <dir>` | Full setup: settings.json + hook + symlinks/junctions |
| `library-link [dir] [--json]` | Create/refresh symlinks only (default: current dir) |
| `library-link [dir] --repair` | Replace stale plain copies with proper links |
| `library-list [--json]` | List all shared skills with descriptions |
| `library-verify` | Run the discovery verification script |
| `library-push ["msg"]` | Git add + commit + push shared-skills |
| `library-sync [--project dir] [--json]` | Git pull + refresh symlinks |

---

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/push-skills` | Commit + push shared-skills without leaving your project |
| `/sync-skills` | Pull latest + list skills |

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
- `library-link` automatically falls back to directory junctions (skills) and
  file copies (agents/commands) — no elevation or Developer Mode needed
- If junctions fail, check that PowerShell is available on PATH
- Stale plain-directory copies from before the junction fix: run `library-link --repair`

**Agent/command edits not writing through:**
- Run `library-link --repair` to replace stale file copies with hardlinks
- Hardlinks share the same file data — edits anywhere are visible everywhere
- If repos are on different drives, hardlinks won't work (same-drive requirement)
