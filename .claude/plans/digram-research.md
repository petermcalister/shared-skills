# Real GitHub repos for Excalidraw and Mermaid Claude Code skills

A thriving open-source ecosystem of Claude Code diagram skills already exists on GitHub, with **at least 9 verified Excalidraw repos and 8+ verified Mermaid repos** implementing the `.claude/skills` directory pattern. The standout repos are **coleam00/excalidraw-diagram-skill** (~1.3k stars, Playwright validation loop) and **SpillwaveSolutions/design-doc-mermaid** (39 stars, full mmdc integration with Python utilities). Every repository listed below was confirmed to exist by directly fetching its GitHub page.

---

## Excalidraw skills: the ecosystem is mature

### 1. coleam00/excalidraw-diagram-skill — the gold standard

**URL:** https://github.com/coleam00/excalidraw-diagram-skill  
**Stars:** ~**1,300** | **Forks:** 222 | **Language:** Python

This is the single best starting point for Excalidraw diagram generation via Claude Code. It installs into `.claude/skills/excalidraw-diagram` and ships with a `SKILL.md` at root plus a `references/` directory containing `color-palette.md`, `element-templates.md`, and `json-schema.md`. The skill teaches Claude the complete Excalidraw JSON schema (x/y coordinates, width, height, seed values) and enforces a design philosophy of "diagrams that argue, not display."

**Visual validation is built in.** The repo includes `render_excalidraw.py` (a Playwright-based renderer) and `render_template.html`. The agent generates JSON, renders it to PNG, reviews its own output for overlapping text, misaligned arrows, or unbalanced spacing, and fixes problems in a loop before delivering. This uses **Playwright**, not Puppeteer, but accomplishes the exact same headless-browser validation pipeline. Large diagrams are built section-by-section to stay under Claude's ~32k token output limit. Brand customization is a single-file swap in `color-palette.md`.

### 2. aref-vc/excalidraw-skill — browser-free rendering

**URL:** https://github.com/aref-vc/excalidraw-skill

A pure CLI approach that explicitly avoids Puppeteer and any browser dependency. It installs to `~/.claude/skills/excalidraw` and uses `scripts/render.mjs` (~350 lines of Node.js) with **roughjs** for hand-drawn shapes, `xmldom` for SVG generation, and `resvg-js` for SVG→PNG conversion. Renders in **200–400ms** with collision avoidance for arrow labels and width-aware text wrapping. The Virgil handwriting font gives outputs the authentic Excalidraw look.

### 3. softaworks/agent-toolkit (excalidraw subagent skill)

**URL:** https://github.com/softaworks/agent-toolkit  
**Stars:** ~575 | **Forks:** ~35  
**Skill path:** `skills/excalidraw/`

A unique architecture: the main agent never directly reads Excalidraw JSON. Instead, it creates task descriptions, a subagent reads/modifies the JSON in isolation, and returns a compact summary. This preserves the main agent's context budget since Excalidraw files run **4k–22k tokens** each. Part of a broader "Softaworks Agent Skills" collection.

### 4. rnjn/cc-excalidraw-skill — minimalist reference

**URL:** https://github.com/rnjn/cc-excalidraw-skill  
**Stars:** 7

A pure markdown-based skill with no scripts or servers. Contains `SKILL.md`, `best-practices.md`, `diagram-patterns.md`, `element-reference.md`, and `examples.md`. Covers flowcharts, sequence diagrams, architecture diagrams, mind maps, ERDs, and wireframes. Color semantics: Blue=info, Green=success, Yellow=decisions, Red=errors. No automated validation — users paste JSON into excalidraw.com manually.

### 5. Additional verified Excalidraw repos

- **edwingao28/excalidraw-skill** (7 stars) — Claude Code skill for live-canvas architecture diagrams. Requires the yctimlin/mcp_excalidraw MCP server running at localhost:3000. Auto-routing arrows, color-coded by role (databases=green, APIs=purple, frontends=blue). A skill-wrapping-MCP hybrid pattern.

- **axtonliu/axton-obsidian-visual-skills** — Multi-skill pack with separate `excalidraw-diagram/SKILL.md`, `mermaid-visualizer/SKILL.md`, and `obsidian-canvas-creator/SKILL.md`. Supports CJK text with Excalifont/Xiaolai font handling. Three output modes for Excalidraw.

- **yctimlin/mcp_excalidraw** (~1,300 stars) — Primarily an MCP server with 26 tools, but includes a portable skill at `skills/excalidraw-skill/` with `SKILL.md` and helper CJS scripts. Canvas screenshot validation, Docker deployment, cloud-specific color palettes (AWS, Azure, GCP, K8s). The most-starred repo in this space, though it's MCP-first.

- **openclaw/skills** — Contains `skills/sairammahadevan/thought-to-excalidraw/SKILL.md`, a PM-focused skill that generates Excalidraw files from structured product thinking (Why, What, How, User Journey) via a Python `layout_diagram.py` script.

- **tenzir/claude-plugins** (2 stars) — Collection of 12+ Claude Code plugins including an Excalidraw plugin ("Create Excalidraw diagrams with proper JSON structure"). Uses the Claude Code plugin architecture rather than `.claude/skills/`.

---

## Mermaid skills: validation loops are the differentiator

### 1. WH-2099/mermaid-skill — confirmed to exist

**URL:** https://github.com/WH-2099/mermaid-skill  
**Stars:** 0 | **License:** MIT | **Commits:** 8

**This specific repo mentioned in the prompt does exist.** It is a full Claude Code skill at `.claude/skills/mermaid/SKILL.md` with a `references/` directory containing per-diagram-type markdown files (flowchart.md, sequenceDiagram.md, classDiagram.md, etc.). Covers **23 Mermaid diagram types** across 6 categories (Flow & Process, Structural, Temporal, Data Visualization, Organization, Technical). A GitHub Action auto-syncs docs from the official mermaid-js/mermaid repo weekly. Invoked with `/mermaid` slash command. However, it does **not** implement a validation loop or mmdc integration — it's purely a syntax reference skill.

### 2. SpillwaveSolutions/design-doc-mermaid — fullest CLI tooling

**URL:** https://github.com/SpillwaveSolutions/design-doc-mermaid  
**Stars:** **39** | **Forks:** 9

The most complete Mermaid CLI skill. The directory structure is well-organized: `mermaid-architect/SKILL.md` as the orchestrator with a decision tree, `CLAUDE.md` for Claude Code integration, and `references/guides/` with specialized guides for activity, deployment, architecture, and sequence diagrams plus a **28-error troubleshooting guide**. 

The `scripts/` directory is the highlight. **`extract_mermaid.py`** extracts and validates diagrams from markdown with flags for `--validate`, `--list-only`, `--output-dir`, and `--replace-with-images`. **`mermaid_to_image.py`** converts diagrams to PNG/SVG with theme and batch support. The repo explicitly documents installing `@mermaid-js/mermaid-cli` globally (`npm install -g @mermaid-js/mermaid-cli`) and verifying with `mmdc --version`. Language-specific code-to-diagram examples cover Spring Boot, FastAPI, React, Python ETL, and Node.js. Available on the Skilz Marketplace.

### 3. mgranberry/mermaid-diagram-skill — the best validation loop

**URL:** https://github.com/mgranberry/mermaid-diagram-skill  
**Stars:** 0 | **Forks:** 0 (forked from coleam00/excalidraw-diagram-skill)

This repo implements the exact validation pattern the prompt describes. It uses **`npx --yes @mermaid-js/mermaid-cli`** to render Mermaid diagrams, and the agent **sees its own output, catches syntax errors from stderr, and fixes layout issues in a loop before delivering**. No global install needed — npx handles ephemeral mmdc downloads. The skill ships with `SKILL.md` at root plus `references/mermaid-theme.md` for theming with `classDef` semantic styles supporting dark/light mode. Compatible with Claude Code, OpenCode, GitHub Copilot, and the Agent Skills Standard (agentskills.io). Installs into `.claude/skills/`, `.github/skills/`, or `.agents/skills/`.

### 4. imxv/Pretty-mermaid-skills — most popular Mermaid skill

**URL:** https://github.com/imxv/Pretty-mermaid-skills  
**Stars:** **244–492** (varying across sources; agentskills.so reports 492) | **Forks:** 12 | **License:** MIT

The most-starred pure Mermaid skill. Offers **15 built-in themes** (tokyo-night, dracula, github-dark, catppuccin-mocha, nord, solarized, etc.) and dual-format output: SVG for web/docs and ASCII/Unicode for terminals. Ships with `SKILL.md`, `references/DIAGRAM_TYPES.md`, and `assets/example_diagrams/` (5 templates). CLI tools in `scripts/`: `render.mjs` for single-diagram rendering, `batch.mjs` for batch processing, and `themes.mjs` for theme management. Listed on skills.sh and LobeHub marketplaces. Auto-installs dependencies on first run.

### 5. awesome-skills/mermaid-syntax-skill — error prevention focus

**URL:** https://github.com/awesome-skills/mermaid-syntax-skill

This skill focuses specifically on preventing the **90% most common Mermaid syntax errors**: special character escaping, reserved word "end" collisions, node IDs with o/x, semicolons in sequence diagrams, and stroke-dasharray comma issues. Contains `SKILL.md` (auto-loaded on trigger), `references/` with complete docs per diagram type, `examples/` with 8 flowchart and 10 sequence diagram patterns, and crucially a **`scripts/validate-mermaid.sh`** bash script for syntax validation. Supports Mermaid v11 features including hand-drawn look and bidirectional arrows.

### 6. Bob2622/beautiful-mermaid-claude-code-skill

**URL:** https://github.com/Bob2622/beautiful-mermaid-claude-code-skill

Renders Mermaid as **pure ASCII/Unicode text** (default) or themed SVGs using the beautiful-mermaid package. Uses `bun run scripts/render-mermaid.ts` for rendering. Supports stdin/stdout piping for composable CLI workflows. Themes include tokyo-night and others. Claude Code automatically triggers this skill when diagram generation is requested.

### 7. Additional verified Mermaid-adjacent repos

- **daymade/claude-code-skills** (636 stars) — A skills marketplace repo containing 43+ skills including `mermaid-tools`, which extracts Mermaid diagrams from markdown and generates PNG images using bundled scripts (`extract-and-generate.sh`, `extract_diagrams.py`, `puppeteer-config.json`).

- **alexanderop/walkthrough** — A Claude Code skill that generates interactive HTML walkthroughs with clickable Mermaid diagrams. Has `skill.md` + `references/html-patterns.md`. Pan/zoom, dark mode, Shiki syntax highlighting. Uses Mermaid as a visualization component within broader walkthrough generation.

- **johnlarkin1/claude-code-extensions** — Personal skill collection containing dedicated `mermaid` and `excalidraw` skills with SKILL.md files for each. Also includes a `diagram-code` skill that generates Mermaid, GraphViz DOT, and Excalidraw from natural language.

---

## How the validation loop pattern works across these repos

The repos implement three distinct validation strategies, each worth understanding:

**Playwright render-view-fix (Excalidraw).** Used by coleam00/excalidraw-diagram-skill. The agent writes Excalidraw JSON → `render_excalidraw.py` launches a headless Chromium via Playwright → loads the JSON into an HTML template → captures a PNG screenshot → the agent views the PNG, checks for bounding box overlaps and layout issues → edits the JSON → re-renders until clean. This is the most robust visual validation approach.

**mmdc stderr capture (Mermaid).** Used by mgranberry/mermaid-diagram-skill and documented in SpillwaveSolutions/design-doc-mermaid. The agent writes a `.mmd` file → runs `npx --yes @mermaid-js/mermaid-cli -i file.mmd -o output.svg 2>&1` → if mmdc exits with errors, stderr is captured and fed back to Claude → Claude reads the error message, fixes the syntax, and re-runs until compilation succeeds. A blog post at zolkos.com documents this canonical pattern explicitly.

**Bash/Python validation scripts (Mermaid).** Used by awesome-skills/mermaid-syntax-skill (`validate-mermaid.sh`) and SpillwaveSolutions/design-doc-mermaid (`extract_mermaid.py --validate`). These run syntax checks without necessarily rendering, catching structural errors before the full render pipeline.

---

## What was not found

The user-mentioned repo name **"excalidraw-diagram-skill"** was found exactly as described at `coleam00/excalidraw-diagram-skill`. The user-mentioned **"WH-2099/mermaid-skill"** was also confirmed to exist. The name **"design-doc-mermaid"** was found at `SpillwaveSolutions/design-doc-mermaid`. No repos matching exactly "excalidraw-agent-skill" as a standalone repo name were found, though `aref-vc/excalidraw-skill` and `edwingao28/excalidraw-skill` are close matches. The Puppeteer-specific validation pipeline the user described exists in spirit via Playwright (coleam00) and via the mmdc stderr capture pattern (mgranberry, SpillwaveSolutions) — no repo uses Puppeteer specifically for Excalidraw validation, but Playwright serves the identical purpose.

## Quick reference table

| Repository | Category | Stars | SKILL.md | Validation loop | Key differentiator |
|---|---|---|---|---|---|
| coleam00/excalidraw-diagram-skill | Excalidraw | ~1,300 | ✅ | ✅ Playwright | Gold standard, render-view-fix loop |
| aref-vc/excalidraw-skill | Excalidraw | Small | ✅ | ✅ roughjs CLI | No browser needed, 200ms renders |
| softaworks/agent-toolkit | Excalidraw | ~575 | ✅ | ❌ | Subagent delegation for token savings |
| rnjn/cc-excalidraw-skill | Excalidraw | 7 | ✅ | ❌ | Pure markdown, zero dependencies |
| WH-2099/mermaid-skill | Mermaid | 0 | ✅ | ❌ | 23 diagram types, auto-synced docs |
| SpillwaveSolutions/design-doc-mermaid | Mermaid | 39 | ✅ | ✅ Python+mmdc | Fullest CLI tooling, 28-error guide |
| mgranberry/mermaid-diagram-skill | Mermaid | 0 | ✅ | ✅ npx mmdc | Best stderr→fix loop implementation |
| imxv/Pretty-mermaid-skills | Mermaid | ~244–492 | ✅ | ✅ Render scripts | 15 themes, SVG+ASCII dual output |
| awesome-skills/mermaid-syntax-skill | Mermaid | Small | ✅ | ✅ Bash script | Error prevention, v11 support |
| Bob2622/beautiful-mermaid-claude-code-skill | Mermaid | Small | ✅ | ✅ Bun render | ASCII/Unicode terminal output |