# Shared Skills + Diagram Skills Plan

## Overview

Create a `shared-skills` GitHub repo at `~/RepoBase/shared-skills` for reusable Claude Code skills, port Anthropic's skill-creator with full eval infrastructure, build Mermaid and Excalidraw diagram skills in pete-pa, then graduate them to the shared repo via git submodule.

**Reference repos** (base our diagram skills on these):
- **Mermaid**: [SpillwaveSolutions/design-doc-mermaid](https://github.com/SpillwaveSolutions/design-doc-mermaid) — hierarchical routing, Python utilities, 28-error troubleshooting guide, resilient workflow
- **Excalidraw**: [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) — "argue not display" philosophy, Playwright render-view-fix loop, section-by-section large diagram strategy

## Feature List

See: `shared-skills-features.json`

Total features: 24
Passing: 0

## Prerequisites

Before starting ANY features:

1. **Fix GitHub auth**: `gh auth login -h github.com` — current token is invalid
2. **Verify npm works**: `npm install -g @mermaid-js/mermaid-cli` (F003)
3. **Verify git submodule support**: `git submodule` should be available (it is — standard Git for Windows)

## Repo Structure: shared-skills

```
~/RepoBase/shared-skills/          # Adjacent to ~/RepoBase/cowork/
├── README.md                      # Setup instructions (incl. submodule usage)
├── .gitignore                     # evals/results/, __pycache__, .env
├── skills/                        # Graduated, proven skills
│   ├── mermaid-diagram/           # (F022 — after proving in pete-pa)
│   │   ├── SKILL.md              # Hierarchical routing + decision tree
│   │   ├── scripts/              # Python utilities
│   │   │   ├── extract_mermaid.py
│   │   │   ├── mermaid_to_image.py
│   │   │   └── validate_mermaid.py
│   │   └── references/
│   │       ├── guides/
│   │       │   ├── diagrams/     # Per-type guides (activity, sequence, etc.)
│   │       │   ├── troubleshooting.md  # 28-error catalog
│   │       │   └── unicode-symbols/guide.md
│   │       └── mermaid-diagram-guide.md
│   └── excalidraw-diagram/        # (F022 — after proving in pete-pa)
│       ├── SKILL.md              # "Argue not display" philosophy
│       └── references/
│           ├── json-schema.md
│           ├── color-palette.md
│           ├── element-templates.md
│           ├── render_excalidraw.py
│           ├── render_template.html
│           └── pyproject.toml
├── skill-creator/                 # Ported from anthropics/skills
│   ├── SKILL.md                   # 5-stage workflow (adapted)
│   ├── agents/                    # grader.md, comparator.md, analyzer.md
│   ├── scripts/                   # 9 Python scripts (eval, benchmark, package)
│   ├── eval-viewer/               # viewer.html + generate_review.py
│   └── references/                # schemas.md
├── template/                      # Skeleton for new skills
│   └── SKILL.md                   # Pete's YAML frontmatter conventions
├── evals/                         # Shared eval results (gitignored)
│   └── results/                   # Per-skill eval output
└── variants/                      # A/B testing infrastructure
    ├── registry.json              # Active variant registry
    └── README.md                  # A/B workflow docs
```

## Repo Structure: cowork (submodule wiring)

```
~/RepoBase/cowork/
├── .gitmodules                    # → petermcalister/shared-skills
├── .claude/skills/shared/         # Submodule checkout of shared-skills/skills/
│   ├── mermaid-diagram/           # Available project-wide
│   └── excalidraw-diagram/        # Available project-wide
└── pete-pa/
    ├── skills/
    │   ├── mermaid-diagram/       # Built here first (F004-F009)
    │   └── excalidraw-diagram/    # Built here first (F010-F013)
    └── commands/
        ├── diagram-mermaid.md     # Thin launcher
        └── diagram-excalidraw.md  # Thin launcher
```

## Files to Create/Modify

### Phase 1: Foundation (F001-F003)

| File | Change |
|------|--------|
| `~/RepoBase/shared-skills/` (new repo) | Create via `gh repo create petermcalister/shared-skills --public --clone` |
| `~/RepoBase/shared-skills/README.md` | Repo purpose, submodule usage, skill conventions |
| `~/RepoBase/shared-skills/.gitignore` | `evals/results/`, `__pycache__/`, `.env`, `*.pyc` |
| Global npm | `npm install -g @mermaid-js/mermaid-cli` |

### Phase 2: Mermaid Skill in pete-pa (F004-F009)

Based on **SpillwaveSolutions/design-doc-mermaid**.

| File | Change |
|------|--------|
| `pete-pa/skills/mermaid-diagram/SKILL.md` | Hierarchical routing with decision tree, resilient workflow, on-demand guide loading |
| `pete-pa/skills/mermaid-diagram/scripts/extract_mermaid.py` | Extract + validate diagrams from markdown (ported from SpillwaveSolutions) |
| `pete-pa/skills/mermaid-diagram/scripts/mermaid_to_image.py` | Render .mmd to PNG/SVG with themes + batch support (ported from SpillwaveSolutions) |
| `pete-pa/skills/mermaid-diagram/scripts/validate_mermaid.py` | Resilient workflow: save .mmd, generate image, validate, error recovery |
| `pete-pa/skills/mermaid-diagram/references/mermaid-diagram-guide.md` | Comprehensive diagram type reference (flowchart, sequence, ER, C4, class, state, gantt) |
| `pete-pa/skills/mermaid-diagram/references/guides/troubleshooting.md` | 28-error troubleshooting catalog with severity + fixes |
| `pete-pa/skills/mermaid-diagram/references/guides/diagrams/*.md` | Per-type guides: activity, deployment, architecture, sequence diagrams |
| `pete-pa/skills/mermaid-diagram/references/guides/unicode-symbols/guide.md` | Unicode semantic symbols for diagram enhancement |
| `pete-pa/commands/diagram-mermaid.md` | Command launcher |

### Phase 3: Excalidraw Skill in pete-pa (F010-F013)

Based on **coleam00/excalidraw-diagram-skill**.

| File | Change |
|------|--------|
| `pete-pa/skills/excalidraw-diagram/SKILL.md` | "Argue not display" philosophy, depth assessment, visual pattern library, section-by-section strategy, mandatory render-view-fix loop |
| `pete-pa/skills/excalidraw-diagram/references/json-schema.md` | Excalidraw element types, common properties, binding format |
| `pete-pa/skills/excalidraw-diagram/references/color-palette.md` | Semantic color system (single customization point for branding) |
| `pete-pa/skills/excalidraw-diagram/references/element-templates.md` | Copy-paste JSON templates for every element type |
| `pete-pa/skills/excalidraw-diagram/references/render_excalidraw.py` | Playwright-based renderer (JSON → PNG via headless Chromium) |
| `pete-pa/skills/excalidraw-diagram/references/render_template.html` | HTML template loading @excalidraw/excalidraw from esm.sh |
| `pete-pa/skills/excalidraw-diagram/references/pyproject.toml` | Dependencies (playwright) for uv-based setup |
| `pete-pa/commands/diagram-excalidraw.md` | Command launcher |

### Phase 4: Skill Creator Port (F014-F020)

| File | Change |
|------|--------|
| `~/RepoBase/shared-skills/skill-creator/SKILL.md` | Adapted from anthropics/skills |
| `~/RepoBase/shared-skills/skill-creator/agents/grader.md` | Eval grading agent |
| `~/RepoBase/shared-skills/skill-creator/agents/comparator.md` | A/B comparison agent |
| `~/RepoBase/shared-skills/skill-creator/agents/analyzer.md` | Benchmark analysis agent |
| `~/RepoBase/shared-skills/skill-creator/scripts/*.py` | 9 Python scripts (eval, benchmark, improve, package, validate, loop, utils) |
| `~/RepoBase/shared-skills/skill-creator/eval-viewer/viewer.html` | Interactive eval viewer |
| `~/RepoBase/shared-skills/skill-creator/eval-viewer/generate_review.py` | Review data generator |
| `~/RepoBase/shared-skills/skill-creator/references/schemas.md` | JSON schemas |
| `~/RepoBase/shared-skills/template/SKILL.md` | Pete's skill template |
| `~/RepoBase/shared-skills/variants/registry.json` | Empty A/B registry |
| `~/RepoBase/shared-skills/variants/README.md` | A/B workflow docs |

### Phase 5: Integration (F021-F024)

| File | Change |
|------|--------|
| `cowork/.gitmodules` | Add shared-skills submodule |
| `cowork/.claude/skills/shared/` | Submodule checkout |
| `shared-skills/skills/mermaid-diagram/` | Graduated from pete-pa |
| `shared-skills/skills/excalidraw-diagram/` | Graduated from pete-pa |
| `pete-pa/.claude-plugin/plugin.json` | Version bump |
| `CLAUDE.md` | Add diagram + shared-skills docs |

## Incremental Order

Work on features in this order (grouped by phase):

### Phase 1: Foundation (do first — everything depends on this)
1. **F001** — Create shared-skills repo on GitHub + clone locally (BLOCKING)
2. **F002** — Scaffold repo structure (depends on F001)
3. **F003** — Install mmdc (independent, can parallel with F002)

### Phase 2: Mermaid Skill (build in pete-pa — based on SpillwaveSolutions)
4. **F004** — Mermaid SKILL.md with hierarchical routing + decision tree
5. **F005** — Mermaid Python scripts (extract, render, validate with resilient workflow)
6. **F006** — Mermaid reference guides (diagram-type guides, troubleshooting, unicode symbols)
7. **F007** — Mermaid command launcher + test (depends on F004-F006)

### Phase 3: Excalidraw Skill (build in pete-pa — based on coleam00)
8. **F008** — Excalidraw reference files (json-schema, color-palette, element-templates)
9. **F009** — Excalidraw Playwright renderer (render_excalidraw.py + render_template.html + pyproject.toml)
10. **F010** — Excalidraw SKILL.md with full philosophy + render-view-fix loop (depends on F008-F009)
11. **F011** — Excalidraw command launcher + test (depends on F010)

### Phase 4: Skill Creator (port from Anthropic — independent of Phase 2-3)
12. **F012** — Port skill-creator SKILL.md (independent)
13. **F013** — Port agent prompts (depends on F012)
14. **F014** — Port core eval scripts (depends on F012)
15. **F015** — Port helper scripts (depends on F014)
16. **F016** — Port eval viewer (depends on F014)
17. **F017** — Port schemas + create template (depends on F012)
18. **F018** — A/B variant infrastructure (independent)

### Phase 5: Integration (wire it all together)
19. **F019** — Git submodule wiring (depends on F001)
20. **F020** — Graduate diagram skills to shared-skills (depends on F007 + F011 + F019)
21. **F021** — Run skill-creator evals on diagram skills (depends on F014 + F020)
22. **F022** — Version bump + docs update (depends on all above)

## Key Technical Decisions

### Mermaid Skill: Hierarchical On-Demand Guide Loading (from SpillwaveSolutions)

The skill uses a **decision tree** to route requests to specialized guides:

```
User Request → Analyze Intent →
  "workflow, process" → Load activity-diagrams.md
  "infrastructure, cloud" → Load deployment-diagrams.md
  "system architecture" → Load architecture-diagrams.md
  "API flow, interactions" → Load sequence-diagrams.md
  "code to diagram" → Load code-to-diagram guide + examples
  "extract, validate" → Use Python scripts
```

This is token-efficient — only the relevant guide is loaded, not all documentation.

### Mermaid Skill: Resilient Workflow with Error Recovery

The critical pattern from SpillwaveSolutions:

```
1. Identify diagram type → Load appropriate guide
2. Generate .mmd → Save file
3. Validate via mmdc (Python script wraps subprocess)
   IF success → Generate image → Add to markdown
   IF error → Check troubleshooting.md (28 documented errors)
           → If still failing, search external sources
           → Retry with fixes
4. NEVER add a diagram to markdown until it passes validation
```

Three Python scripts work together:
- `extract_mermaid.py` — Extract diagrams from markdown, validate, replace with images
- `mermaid_to_image.py` — Render .mmd to PNG/SVG with theme + batch support
- `validate_mermaid.py` — Full resilient workflow (save, render, validate, error recovery)

### Excalidraw Skill: "Argue Not Display" Philosophy (from coleam00)

The skill enforces a design methodology, not just JSON generation:

1. **Depth Assessment** — Simple/conceptual vs comprehensive/technical routing
2. **Research Mandate** — For technical diagrams, look up actual specs before drawing
3. **Visual Pattern Library** — Fan-out, convergence, tree, spiral, assembly line, side-by-side, gap/break
4. **Container Discipline** — Default to free-floating text, <30% of text in containers
5. **Section-by-Section Build** — Large diagrams MUST be built one section at a time (Claude's ~32k token limit)
6. **Mandatory Render-View-Fix Loop** — Playwright renders PNG, agent views it, fixes issues, re-renders

### Excalidraw Skill: Playwright Render-View-Fix Loop (from coleam00)

```
Agent writes .excalidraw JSON
  → render_excalidraw.py launches headless Chromium via Playwright
  → Loads render_template.html (imports @excalidraw/excalidraw from esm.sh)
  → Captures PNG screenshot of rendered SVG
  → Agent views PNG via Read tool
  → Audits against original vision + checks for visual defects
  → Fixes JSON (widen containers, adjust coordinates, reroute arrows)
  → Re-renders → Repeats (typically 2-4 iterations)
```

First-time setup: `uv sync && uv run playwright install chromium`

### Excalidraw Skill: Color Palette as Single Customization Point (from coleam00)

All colors live in `references/color-palette.md`:
- **Semantic shape colors** — fill/stroke pairs for start, end, decision, AI, error, etc.
- **Text hierarchy colors** — title, subtitle, body/detail levels
- **Evidence artifact colors** — dark backgrounds for code snippets, JSON examples
- To rebrand: edit only `color-palette.md`, everything else is universal

### Skill Creator Port: Adaptation Points

When porting from Anthropic's repo, adapt these:
- **SKILL.md frontmatter**: Add `version` field (Pete's convention)
- **Script paths**: Anthropic assumes `.claude/commands/` — adapt to Pete's `commands/` and `skills/` structure
- **Eval runner**: Anthropic uses `claude -p` CLI — verify this works on Windows with Pete's setup
- **Package script**: Adapt to produce `.plugin.zip` format matching `deploy-plugin.sh`
- **Eval viewer**: Should work as-is (static HTML) — just verify paths

### Git Submodule: How It Works

```bash
# One-time setup in cowork repo:
cd ~/RepoBase/cowork
git submodule add https://github.com/petermcalister/shared-skills.git .claude/skills/shared

# Cloning cowork on a new machine:
git clone --recurse-submodules https://github.com/petermcalister/cowork-pa.git

# Updating shared-skills in cowork:
cd .claude/skills/shared
git pull origin main
cd ../../../
git add .claude/skills/shared
git commit -m "Update shared-skills submodule"
```

**Important for plugin packaging**: The submodule is at `.claude/skills/shared/` (project level), NOT inside `pete-pa/`. Plugin commands that need diagram skills will reference the project-level path, not `${CLAUDE_PLUGIN_ROOT}`. This is correct — diagram skills are general-purpose, not Pete-specific.

### Diagram Skill Graduation Strategy

When graduating from pete-pa → shared-skills (F020):
1. **Copy** the skill to shared-skills/skills/ (not move)
2. **Remove** from pete-pa/skills/ (avoid duplication)
3. **Update** pete-pa commands to reference via project-level path
4. If plugin needs to be self-contained (portable ZIP), keep a copy in pete-pa too — agent should test whether the plugin still works after moving

## Test Strategy

### Mermaid
- Generate flowchart, sequence, ER, architecture diagram — verify mmdc compiles all
- Run `extract_mermaid.py --validate` on a markdown file with multiple diagram types
- Intentionally break syntax — verify resilient workflow catches errors and recovers using troubleshooting guide
- Generate complex diagram (>20 nodes) — verify readability
- Test batch conversion with `mermaid_to_image.py` across themes

### Excalidraw
- Generate architecture diagram — render via Playwright, verify PNG output
- Run render-view-fix loop — verify agent catches overlapping text and fixes it
- Generate large diagram (>15 elements) — verify section-by-section build strategy works
- Verify color palette customization — change `color-palette.md`, regenerate, confirm new colors
- Check no overlapping elements in rendered PNG
- Generate diagram with arrows between containers — verify bindings are correct
- Test first-time setup: `uv sync && uv run playwright install chromium`

### Skill Creator
- Run quick_validate.py on both diagram skills
- Run run_eval.py with trigger queries for mermaid-diagram
- Open eval viewer in browser — verify it displays results

### Submodule
- Clone cowork fresh with --recurse-submodules — verify shared skills populate
- Modify a skill in shared-skills, update submodule in cowork — verify update propagates

## Acceptance Criteria

All 24 features in `shared-skills-features.json` have `passes: true`

## Notes for the Building Agent

1. **Fix `gh auth` first** — `gh auth login -h github.com` — nothing works without this
2. **Work in two repos** — `~/RepoBase/cowork` and `~/RepoBase/shared-skills`. Keep commits separate.
3. **Port from reference repos, don't rewrite from scratch** — Adapt SpillwaveSolutions and coleam00 code to Pete's conventions (YAML frontmatter, `${CLAUDE_PLUGIN_ROOT}` paths, poetry for package management). The source material is proven and battle-tested.
4. **Test diagram skills manually** — generate a real diagram with each skill before marking done
5. **The Excalidraw render pipeline needs Playwright** — run `uv sync && uv run playwright install chromium` in the references/ directory during setup
6. **Windows paths** — use forward slashes in bash, backslashes in Python paths. mmdc should work on Windows via npm global install.
7. **Phase 2 and Phase 3 are independent** — if you have capacity, work them in parallel
8. **The troubleshooting guide is critical for Mermaid** — it prevents 90% of syntax errors. Port it faithfully from SpillwaveSolutions.
9. **Excalidraw render-view-fix loop is MANDATORY** — the SKILL.md must enforce this, not suggest it. Diagrams are not delivered without visual validation.
10. **Poetry for package management** — Pete prefers poetry over pip/pipenv.
