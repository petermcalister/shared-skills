# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repo contains **shared reusable Claude Code skills** for a personal assistant system ("pete-pa") hosted in the adjacent `~/RepoBase/cowork` project. Skills are developed here and consumed via git submodule at `cowork/.claude/skills/shared/`.

Current focus: **diagram generation skills** (Mermaid + Excalidraw) and a **skill-creator** eval framework ported from Anthropic.

## Architecture

### Skills

| Skill | Based On | Key Feature |
|-------|----------|-------------|
| `skills/mermaid-diagram` | [SpillwaveSolutions/design-doc-mermaid](https://github.com/SpillwaveSolutions/design-doc-mermaid) | Hierarchical routing, Python utilities, resilient validation workflow, 28-error troubleshooting guide |
| `skills/excalidraw-diagram` | [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) | "Argue not display" philosophy, Playwright render-view-fix loop, section-by-section large diagram strategy |
| `skill-creator` | [anthropics/skills](https://github.com/anthropics/skills) | 5-stage skill creation workflow, eval scripts, A/B variant testing |

### Integration with cowork

```
shared-skills/skills/  ←── git submodule ──→  cowork/.claude/skills/shared/
                                                    ↑
                                          pete-pa/commands/diagram-*.md (launchers)
```

Skills are built first in `cowork/pete-pa/skills/`, then graduated to `shared-skills/skills/` once proven.

### Mermaid Validation Pipeline

```
Claude writes .mmd → validate_mermaid.py runs mmdc →
  IF success: render PNG/SVG → return output path
  IF error: check troubleshooting.md (28 errors) → fix → retry
  NEVER add a diagram to markdown until it passes validation
```

Python scripts: `extract_mermaid.py`, `mermaid_to_image.py`, `validate_mermaid.py`

### Excalidraw Render-View-Fix Loop

```
Agent writes .excalidraw JSON → render_excalidraw.py (Playwright + Chromium) →
  Captures PNG → Agent views PNG → Audits for defects →
  Fixes JSON → Re-renders → Repeats (2-4 iterations typical)
```

Setup: `cd references && uv sync && uv run playwright install chromium`

## Feature Tracking

24 features tracked in `shared-skills-features.json` across 5 phases. Plan details in `shared-skills.md`.

## Tech Stack

- Python 3.12+ with poetry for package management
- mmdc (mermaid-cli) for Mermaid diagram validation/rendering
- Playwright + Chromium for Excalidraw visual validation
- pytest for unit tests
- Skills follow YAML frontmatter convention: `name`, `description`, `version`

## Conventions

- Skills use Pete's YAML frontmatter pattern (see `template/SKILL.md`)
- Commands use `${CLAUDE_PLUGIN_ROOT}` to reference skill paths within pete-pa
- Diagram skills in shared-skills are referenced via project-level path (not plugin-relative)
- Python scripts use `#!/usr/bin/env python3` and support `--json` output where applicable
