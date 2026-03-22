# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repo contains **shared reusable Claude Code skills, commands, and CLI tools** consumed by multiple projects under `~/RepoBase/`. Consumer projects discover shared skills via symlinks from their `.claude/skills/` into this repo.

## How Sharing Works

Three types of content are shared: **skills**, **agents**, and **commands**.

Consumer projects connect via two mechanisms:
- **Symlinks/junctions** in `.claude/skills/`, `.claude/agents/`, `.claude/commands/` point here (handles discovery)
- **`additionalDirectories`** in `.claude/settings.json` grants file access (handles references, scripts)

Both are set up automatically by `library-setup <project-dir>`.

On Windows, `os.symlink()` requires elevation. The tools automatically fall back to:
- **Directory junctions** for skills (write-through, no elevation needed)
- **Hardlinks** for agents/commands (write-through, no elevation needed)

All shared content writes through to this repo from any consumer project. Push with `library-push` or `/push-skills`.

## Skills

All skills live at `.claude/skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`, `version`).

| Skill | Purpose |
|-------|---------|
| `mermaid-diagram` | Validated Mermaid diagrams with mmdc + troubleshooting guide |
| `excalidraw-diagram` | Excalidraw JSON with Playwright render-view-fix loop |
| `skill-creator` | Create, test, and optimize skills with eval infrastructure |
| `systematic-debugging` | Root-cause investigation before proposing fixes |
| `test-driven-development` | RED-GREEN-REFACTOR cycle for code |
| `brainstorming` | Collaborative design exploration before implementation |
| `using-git-worktrees` | Isolated workspaces for parallel branch work |
| `plugin-builder` | Build Claude Code plugins |
| `library-management` | Set up and maintain the shared library |

## Shared Agents

Agents live at `.claude/agents/<name>.md`.

| Agent | Purpose |
|-------|---------|
| `reviewer` | Review code changes for production readiness |
| `run-agent` | Execute plan-n-park task batches |

## Shared Commands

Commands live at `.claude/commands/<name>.md`.

| Command | Purpose |
|---------|---------|
| `/checkin` | Git add, commit, and push with concise summary |
| `/plan-n-park` | Create implementation plan for multi-session work |
| `/push-skills` | Commit + push shared-skills from consumer project |
| `/reflect` | Distill and preserve learnings from session |
| `/run-agent` | Execute a plan-n-park |
| `/sync-all` | Pull latest shared skills + list available |

## CLI Tools

Registered in `pyproject.toml` as entry points. Install once as an editable package:

```bash
pip install -e ~/RepoBase/shared-skills
```

This makes all `library-*` commands globally available. Required before `library-setup` can be used on consumer projects.

| Command | Purpose |
|---------|---------|
| `library-setup <dir>` | Full setup: settings.json + hook + symlinks/junctions |
| `library-link [dir]` | Create/refresh symlinks (idempotent) |
| `library-link [dir] --repair` | Replace stale plain copies with proper links |
| `library-status` | Repo status + skill/agent/command inventory |
| `library-list` | List skills with descriptions |
| `library-push ["msg"]` | Commit + push this repo |
| `library-sync` | Git pull + refresh symlinks |
| `library-verify` | Run verification script |

## Conventions

- Skills use YAML frontmatter: `name`, `description` (trigger-focused), `version`
- Descriptions start with "Use when..." — no workflow summaries (causes undertriggering)
- Each skill has `evals/trigger-eval.json` + `evals/implementation-eval.json`
- Heavy reference material goes in `references/`, not inline in SKILL.md
- Keep SKILL.md under 500 lines
- No project-specific references (cowork, pete-pa) — skills must be portable
- All paths relative to the skill directory or use `~/RepoBase/` convention
- Poetry for package management
- Python scripts use `shell=True` on Windows for mmdc subprocess calls

## Consumer Projects

Currently: `cowork`, `EmailEvidenceLocker` (both under `~/RepoBase/`).

To add a new consumer:

```bash
library-setup ~/RepoBase/new-project
```

Then add a "Shared Skills Library" section to the new project's CLAUDE.md — see the library-management skill for the template.
