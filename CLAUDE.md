# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repo contains **shared reusable Claude Code skills, commands, and CLI tools** consumed by multiple projects under `~/RepoBase/`. Consumer projects discover shared skills via symlinks from their `.claude/skills/` into this repo.

## How Sharing Works

Consumer projects connect via two mechanisms:
- **Symlinks** in `.claude/skills/` point to skills here (handles discovery)
- **`additionalDirectories`** in `.claude/settings.json` grants file access (handles references, scripts)

Both are set up automatically by `library-setup <project-dir>`.

Edits to symlinked skills write directly to this repo. Push with `library-push` or `/push-skills`.

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

## CLI Tools

Registered in `pyproject.toml`. Install with `poetry install`.

| Command | Purpose |
|---------|---------|
| `library-setup <dir>` | Full setup: settings.json + hook + symlinks |
| `library-link [dir]` | Create/refresh symlinks (idempotent) |
| `library-status` | Repo status + skill inventory |
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

To add a new consumer: `library-setup ~/RepoBase/new-project`
