# Shared Skills: Link Architecture

## Why links?

Claude Code's `additionalDirectories` setting (in `.claude/settings.json`) grants file access to external directories but does **not** trigger skill discovery from those paths. The docs claim it should, but as of v2.1.81 on Windows (and likely all platforms), skills from additional directories do not appear in `/context` or the skill list.

We discovered this on 2026-03-21 and pivoted to symlinks/junctions/hardlinks as the discovery mechanism.

## How it works

Three directories are linked from consumer projects back to shared-skills:

```
Consumer project                            Shared-skills repo
.claude/skills/                             .claude/skills/
├── behave-creator/    (local, real)        ├── brainstorming/SKILL.md
├── brainstorming/ ──> junction ───────────>├── excalidraw-diagram/SKILL.md
├── ...                                     ├── ...
└── .gitignore                              └── using-git-worktrees/SKILL.md

.claude/agents/                             .claude/agents/
├── background-worker.md  (local, real)     ├── reviewer.md
├── reviewer.md ─────> hardlink ───────────>├── run-agent.md
├── run-agent.md ────> hardlink ───────────>
└── .gitignore

.claude/commands/                           .claude/commands/
├── deploy.md          (local, real)        ├── checkin.md
├── checkin.md ──────> hardlink ───────────>├── plan-n-park.md
├── ...                                     ├── ...
└── .gitignore
```

### Windows link strategy

`os.symlink()` requires Developer Mode or elevation on Windows. The tools
try symlinks first, then fall back automatically:

| Content type | Link method | Write-through | Elevation needed |
|-------------|-------------|---------------|-----------------|
| Skills (directories) | Directory junction | Yes | No |
| Agents (files) | Hardlink | Yes | No |
| Commands (files) | Hardlink | Yes | No |

**All link types write through** — edits in any consumer project are immediately
visible in shared-skills and all other consumers.

Hardlinks require same drive (all repos must be under the same drive letter).

### Discovery and access

- **Junctions/hardlinks** make Claude Code discover shared content as if it were local
- **`.gitignore`** in each directory prevents shared content from being tracked in the consumer repo
- **`additionalDirectories`** is still set for file access permissions (reading supporting files, references, scripts)
- **Changes are live** — no restart needed for content edits

## Two-repo model

| Concern | Where it lives | Committed where |
|---------|---------------|-----------------|
| Shared skills/agents/commands | `~/RepoBase/shared-skills/.claude/` | shared-skills repo |
| Links to shared content | Consumer's `.claude/skills/`, `agents/`, `commands/` | Not committed (gitignored) |
| `.gitignore` for links | Consumer's `.claude/{skills,agents,commands}/.gitignore` | Consumer repo |
| Local-only content | Consumer's `.claude/` (real dirs/files) | Consumer repo |
| CLI tools (`library-*`) | `~/RepoBase/shared-skills/tools/library_management/` | shared-skills repo |
| `additionalDirectories` config | Consumer's `.claude/settings.json` | Consumer repo |

## CLI tools

All registered in `shared-skills/pyproject.toml`. Install once as an editable package:

```bash
pip install -e ~/RepoBase/shared-skills
```

This makes all `library-*` commands globally available and is required before
any consumer project can be set up.

| Command | What it does |
|---------|-------------|
| `library-setup <dir>` | Full setup: writes `settings.json`, adds SessionStart hook, creates links, writes `.gitignore` |
| `library-link [dir]` | Creates/refreshes links only. Idempotent. Cleans stale links. Updates `.gitignore`. Default: current dir |
| `library-link [dir] --repair` | Replaces stale plain-directory/file copies with proper junctions/hardlinks |
| `library-sync [--project dir]` | `git pull --rebase` in shared-skills + refreshes links in the consumer project |
| `library-push ["msg"]` | `git add -A && commit && push` in shared-skills |
| `library-status [--json]` | Repo status, branch, discovered skills/agents/commands |
| `library-list [--json]` | List all shared skills with descriptions |
| `library-verify` | Run the SessionStart verification script |

## Key implementation details

### `_sync_location()` in `tools/library_management/run.py`

- Iterates all shared items in a location (skills, agents, or commands)
- For each: if a symlink/junction/hardlink already exists and points correctly, skip. If a real directory/file exists (local content), skip. Otherwise create link.
- With `--repair`: replaces plain copies (from before the junction/hardlink fix) with proper links
- Removes stale links that point into shared-skills but whose target no longer exists
- Calls `_update_gitignore()` to maintain the managed block in `.gitignore`

### `.gitignore` managed blocks

Each linked directory gets a managed block:

```gitignore
# Shared skills (managed by library-link, do not edit)
brainstorming/
excalidraw-diagram/
...
# End shared skills
```

```gitignore
# Shared commands (managed by library-link, do not edit)
checkin.md
plan-n-park.md
...
# End shared commands
```

Blocks are rewritten on every `library-link` run. Lines outside managed blocks are preserved.

### Git index cleanup

When migrating from tracked local copies to links, you must remove the old files from git's index:

```bash
git rm --cached -r .claude/skills/<skill-name>/
```

Otherwise git sees the linked content as modifications to the previously tracked files. The `.gitignore` only affects untracked files.

## Workflows

### Editing shared content

Just edit the file from any consumer project. Junctions and hardlinks mean
you're writing to shared-skills. Commit with:

```bash
library-push "Description of change"
```

### Adding a new shared skill

1. Create `~/RepoBase/shared-skills/.claude/skills/<name>/SKILL.md`
2. `library-push "Added <name> skill"`
3. In each consumer project: `library-link` (creates the new junction)

### Removing a shared skill

1. Delete the directory from shared-skills
2. `library-push "Removed <name> skill"`
3. In each consumer project: `library-link` (removes stale junction, updates `.gitignore`)

### Setting up a new consumer project

```bash
library-setup ~/RepoBase/new-project
```

One command. Creates `.claude/settings.json` entries, junctions/hardlinks, and `.gitignore`.

Then add a "Shared Skills Library" section to the new project's CLAUDE.md — see
the library-management SKILL.md for the template.

### Repairing stale copies

If a consumer project was set up before the junction/hardlink fix and has plain
directory copies instead of proper links:

```bash
library-link ~/RepoBase/project --repair
```

## Known limitations

- `additionalDirectories` skill discovery may be fixed in a future Claude Code release, at which point links become redundant (but harmless)
- Hardlinks require all repos on the same drive (Windows limitation)
- The SessionStart hook (`verify-shared-skills.sh`) reports skill count but is cosmetic — actual discovery relies on links
