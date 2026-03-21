# Shared Skills: Symlink Architecture

## Why symlinks?

Claude Code's `additionalDirectories` setting (in `.claude/settings.json`) grants file access to external directories but does **not** trigger skill discovery from those paths. The docs claim it should, but as of v2.1.81 on Windows (and likely all platforms), skills from additional directories do not appear in `/context` or the skill list.

We discovered this on 2026-03-21 and pivoted to symlinks as the discovery mechanism.

## How it works

```
Consumer project (.claude/skills/)          Shared-skills repo (.claude/skills/)
├── behave-creator/        (local, real)    ├── brainstorming/SKILL.md
├── brainstorming/ ──────> symlink ────────>├── excalidraw-diagram/SKILL.md
├── excalidraw-diagram/ ─> symlink ────────>├── library-management/SKILL.md
├── library-management/ ─> symlink ────────>├── mermaid-diagram/SKILL.md
├── mermaid-diagram/ ────> symlink ────────>├── plugin-builder/SKILL.md
├── ...                                     ├── ...
└── .gitignore  (ignores all symlinked dirs)
```

- **Symlinks** make Claude Code discover shared skills as if they were local
- **`.gitignore`** in `.claude/skills/` prevents symlinked content from being tracked in the consumer repo
- **`additionalDirectories`** is still set for file access permissions (reading supporting files, references, scripts)
- **Edits** to symlinked skills write through to the shared-skills repo
- **Changes are live** — no restart needed for content edits

## Two-repo model

| Concern | Where it lives | Committed where |
|---------|---------------|-----------------|
| Shared skill content | `~/RepoBase/shared-skills/.claude/skills/` | shared-skills repo |
| Symlinks to shared skills | Consumer's `.claude/skills/<name>` | Not committed (gitignored) |
| `.gitignore` for symlinks | Consumer's `.claude/skills/.gitignore` | Consumer repo |
| Local-only skills | Consumer's `.claude/skills/<name>/` (real dirs) | Consumer repo |
| CLI tools (`library-*`) | `~/RepoBase/shared-skills/tools/library_management/` | shared-skills repo |
| `additionalDirectories` config | Consumer's `.claude/settings.json` | Consumer repo |

## CLI tools

All registered in `shared-skills/pyproject.toml`. Install with `pip install -e ~/RepoBase/shared-skills`.

| Command | What it does |
|---------|-------------|
| `library-setup <dir>` | Full setup: writes `settings.json`, adds SessionStart hook, creates symlinks, writes `.gitignore` |
| `library-link [dir]` | Creates/refreshes symlinks only. Idempotent. Cleans stale symlinks. Updates `.gitignore`. Default: current dir |
| `library-sync [--project dir]` | `git pull --rebase` in shared-skills + refreshes symlinks in the consumer project |
| `library-push ["msg"]` | `git add -A && commit && push` in shared-skills |
| `library-status [--json]` | Repo status, branch, discovered skills and commands |
| `library-list [--json]` | List all shared skills with descriptions |
| `library-verify` | Run the SessionStart verification script |

## Key implementation details

### `_sync_symlinks()` in `tools/library_management/run.py`

- Iterates all skill dirs in shared-skills that contain a `SKILL.md`
- For each: if a symlink already exists and points correctly, skip. If a real directory exists (local skill), skip. Otherwise create symlink.
- Removes stale symlinks that point into shared-skills but whose target no longer exists
- Calls `_update_skills_gitignore()` to maintain the managed block in `.gitignore`

### `.gitignore` managed block

```gitignore
# Symlinked shared skills (managed by library-link, do not edit)
brainstorming/
excalidraw-diagram/
...
# End shared skills
```

The block is rewritten on every `library-link` run. Lines outside the managed block are preserved.

### Git index cleanup

When migrating from tracked local copies to symlinks, you must remove the old files from git's index:

```bash
git rm --cached -r .claude/skills/<skill-name>/
```

Otherwise git sees the symlinked content as modifications to the previously tracked files. The `.gitignore` only affects untracked files.

## Workflow for agents

### Editing a shared skill

Just edit the file. The symlink means you're writing to shared-skills. Commit with:

```bash
library-push "Description of change"
```

### Adding a new shared skill

1. Create `~/RepoBase/shared-skills/.claude/skills/<name>/SKILL.md`
2. `library-push "Added <name> skill"`
3. In each consumer project: `library-link` (creates the new symlink)

### Removing a shared skill

1. Delete the directory from shared-skills
2. `library-push "Removed <name> skill"`
3. In each consumer projects: `library-link` (removes stale symlink, updates `.gitignore`)

### Setting up a new consumer project

```bash
library-setup ~/RepoBase/new-project
```

One command. Creates `.claude/settings.json` entries, symlinks, and `.gitignore`.

## Known limitations

- `additionalDirectories` skill discovery may be fixed in a future Claude Code release, at which point symlinks become redundant (but harmless)
- Windows requires Developer Mode enabled for `ln -s` to work in Git Bash
- The SessionStart hook (`verify-shared-skills.sh`) reports skill count but is cosmetic — actual discovery relies on symlinks
