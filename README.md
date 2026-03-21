# shared-skills

Reusable Claude Code skills for diagram generation, skill creation, and evaluation.

## Skills

| Skill | Description |
|-------|-------------|
| `skills/mermaid-diagram` | Generate Mermaid diagrams with mmdc validation loop |
| `skills/excalidraw-diagram` | Generate Excalidraw diagrams with Playwright visual validation |

## Skill Creator

Port of [Anthropic's skill-creator](https://github.com/anthropics/skills) with full eval infrastructure:
- 5-stage workflow (capture intent → interview → write SKILL.md → test → iterate)
- Agent prompts for grading, comparison, and analysis
- Eval scripts for automated testing and benchmarking
- A/B variant testing infrastructure

## Usage as Git Submodule

```bash
# Add to your project
cd your-project
git submodule add https://github.com/petermcalister/shared-skills.git .claude/skills/shared

# Update
cd .claude/skills/shared
git pull origin main
cd ../../..
git add .claude/skills/shared
git commit -m "Update shared-skills submodule"

# Clone with submodules
git clone --recurse-submodules https://github.com/petermcalister/your-project.git
```

## Skill Conventions

Skills follow Pete's YAML frontmatter pattern:

```yaml
---
name: skill-name
description: One-line description for trigger matching
version: 0.1.0
---
```

See `template/SKILL.md` for the full skeleton.
