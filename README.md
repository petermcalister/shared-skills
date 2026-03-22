# shared-skills

Reusable Claude Code skills, commands, and CLI tools shared across projects via symlinks.

## Skills

| Skill | Purpose |
|-------|---------|
| `mermaid-diagram` | Generate validated Mermaid diagrams (flowchart, sequence, ER, architecture) |
| `excalidraw-diagram` | Generate Excalidraw diagrams with Playwright render-view-fix loop |
| `skill-creator` | Create, test, and optimize skills with eval infrastructure |
| `systematic-debugging` | Root-cause investigation before proposing fixes |
| `test-driven-development` | RED-GREEN-REFACTOR cycle for code |
| `brainstorming` | Collaborative design exploration before implementation |
| `using-git-worktrees` | Isolated workspaces for parallel branch work |
| `plugin-builder` | Build Claude Code plugins (commands, skills, agents, hooks) |
| `library-management` | Set up and maintain the shared library in consumer projects |

## How It Works

This repo is a standalone sibling to your project repos. Consumer projects discover
shared skills via **symlinks** from their `.claude/skills/` into this repo. The
`additionalDirectories` setting grants file access to supporting references and scripts.

```
~/RepoBase/
├── shared-skills/                    <- this repo
│   ├── .claude/skills/               <- shared skills live here
│   ├── .claude/commands/             <- shared slash commands
│   └── tools/library_management/     <- CLI tools
├── cowork/                           <- consumer project
│   └── .claude/skills/
│       ├── local-skill/              <- project-specific (real dir)
│       └── mermaid-diagram/ -> symlink to shared-skills
└── another-project/                  <- another consumer
    └── .claude/skills/
        └── mermaid-diagram/ -> symlink to shared-skills
```

## Setup

### New consumer project

```bash
pip install -e ~/RepoBase/shared-skills
library-setup ~/RepoBase/your-project
```

This creates symlinks, configures `additionalDirectories`, and registers a
SessionStart verification hook — all in one command.

### Refresh after adding/removing skills

```bash
library-link ~/RepoBase/your-project
```

## CLI Tools

Install with `pip install -e ~/RepoBase/shared-skills` (or `poetry install` in this repo).

| Command | Purpose |
|---------|---------|
| `library-setup <dir>` | Full setup: settings.json + hook + symlinks |
| `library-link [dir]` | Create/refresh symlinks (idempotent) |
| `library-status` | Repo status, skills, commands |
| `library-list` | List skills with descriptions |
| `library-push ["msg"]` | Commit + push shared-skills |
| `library-sync` | Git pull + refresh symlinks |
| `library-verify` | Run verification script |

## Shared Commands

Available in any consumer project via symlinks:

| Command | Purpose |
|---------|---------|
| `/push-skills` | Commit + push shared-skills without leaving your project |
| `/sync-all` | Pull latest + list skills |
| `/checkin` | Git add, commit, push with concise summary |
| `/plan-n-park` | Create structured implementation plan for multi-session work |
| `/run-agent` | Execute plan batches via subagents |
| `/reflect` | Distill and preserve session learnings |

## Adding a Skill

```bash
mkdir -p .claude/skills/new-skill
# Write SKILL.md with name, description, version frontmatter
library-push "Added new-skill"
# In consumer projects:
library-link
```

## Skill Conventions

```yaml
---
name: kebab-case-name
description: >
  Use when [triggers]. Trigger on: "phrase1", "phrase2".
version: 0.1.0
---
```

Each skill can include `evals/`, `references/`, `scripts/`, and `variants/` subdirectories.

## Windows Note

Symlinks require Developer Mode enabled (Settings > For Developers).
Ensure `git config --global core.symlinks true` is set.
