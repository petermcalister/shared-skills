# Migration Plan: Git Submodules → additionalDirectories

## Overview

Replace the git submodule approach for sharing skills with the `additionalDirectories` pattern from `shared-skills-setup-guide.md`. Create a `library-management` skill that teaches agents in any repo how to set up, consume, and maintain the shared library.

## Current State

- `cowork/.gitmodules` points `.claude/skills/shared` → `petermcalister/shared-skills`
- `cowork/.claude/skills/` has **duplicate** copies of mermaid-diagram and excalidraw-diagram (both as local skills AND inside the submodule)
- `shared-skills/` has skills at `.claude/skills/*` (correct for discovery when used as `additionalDirectories`)
- No `additionalDirectories` configured in cowork yet
- No shared commands (`/push-skills`, `/sync-all`) exist yet
- No verification hook exists in cowork

## Target State

- Submodule **removed** from cowork
- `cowork/.claude/settings.json` has `additionalDirectories: ["C:/Users/peter/RepoBase/shared-skills"]`
- Duplicate skills removed from `cowork/.claude/skills/` (mermaid-diagram, excalidraw-diagram, skill-creator — now discovered via additionalDirectories)
- Shared commands `/push-skills` and `/sync-all` available in all sessions
- PostStart hook verifies shared skills on every session start
- `library-management` skill teaches agents in any repo how to set up this pattern

## Features

### F001: Create shared commands and scripts
- `.claude/commands/push-skills.md` — commit + push shared-skills without leaving consumer repo
- `.claude/commands/sync-all.md` — pull latest shared skills
- `scripts/verify-shared-skills.sh` — PostStart hook script
- `scripts/push-shared-skills.sh` — standalone push helper

### F002: Create library-management skill
- `.claude/skills/library-management/SKILL.md` — teaches agents how to:
  - Set up `additionalDirectories` in a new repo
  - Register the PostStart verification hook
  - Know which skills/commands/scripts are shared vs local
  - Add new skills to the shared library
  - Run evals on shared skills
  - Push changes back to the shared repo
  - Understand the colocated eval convention (evals under each skill)

### F003: Configure cowork to use additionalDirectories
- Create `cowork/.claude/settings.json` with `additionalDirectories`
- Add PostStart hook to cowork's settings
- Remove git submodule from cowork
- Remove duplicate skills from `cowork/.claude/skills/` (mermaid-diagram, excalidraw-diagram)
- Keep cowork-only skills (brainstorming, debug-skill, etc.) in place

### F004: Update CLAUDE.md and documentation
- Update shared-skills CLAUDE.md to reflect new structure
- Document the additionalDirectories approach
- Remove references to git submodules

## Build Order

1. **F001** — shared commands + scripts (in shared-skills repo)
2. **F002** — library-management skill (in shared-skills repo)
3. **F003** — cowork migration (in cowork repo)
4. **F004** — documentation update (both repos)
