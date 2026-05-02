# story-present

A framework-routed presentation and document generator. Interviews the user about audience and goal, routes to the right framework, ingests source material, generates Marp markdown, self-scores against a rubric, and renders to multiple output formats.

## Dependencies

### Python (managed via Poetry)

| Package | Purpose |
|---------|---------|
| `python-pptx` | Native PPTX rendering with positioned layouts |
| `markdown-it-py` | Markdown tokenisation for slide parsing |
| `pyyaml` | Chart fence YAML parsing |
| `matplotlib` | Chart pre-rendering (bar, line, pie, scatter to SVG + PNG) |
| `Pillow` | Image processing for PPTX embedding |
| `mistune` | Markdown parsing for the interactive HTML renderer |
| `playwright` | Headless Chromium for excalidraw JSON to PNG rendering |

Install all with:

```bash
poetry install
poetry run playwright install chromium
```

> **Note:** `playwright install chromium` downloads the Chromium browser binary. This is a one-time step after installing the `playwright` Python package.

### System binaries

| Binary | Install | Purpose |
|--------|---------|---------|
| `marp-cli` | `npm install -g @marp-team/marp-cli` | Static HTML rendering, slide screenshots for visual verification |
| `pandoc` | [pandoc.org/installing](https://pandoc.org/installing.html) | DOCX rendering via the prose adapter |
| `mmdc` (optional) | `npm install -g @mermaid-js/mermaid-cli` | Local Mermaid diagram pre-rendering to SVG + PNG |

Run the dependency check to verify everything is installed:

```bash
poetry run story-present-check-deps
```

## Frameworks

The skill routes to one of eight frameworks based on the user's audience and goal:

| Option | Framework | Best for | Primary format |
|--------|-----------|----------|----------------|
| 1 | McKinsey Pyramid Principle | Conclusion-first executive decks | slides |
| 2 | Market Strategy / Pitch Deck | Investor pitches, fundraising | slides |
| 3 | Internal Problem-Solving / Issue Tree | Root-cause analysis, solution recommendation | slides |
| 4 | Project Roadmap / Implementation Plan | Phased delivery plans | slides |
| 5 | Conference / Tech Talk | Developer-facing narrative talks | slides |
| 6 | RAID Log / Weekly Status | Sprint status, RAG dashboards | slides |
| 7 | Steering Committee / Board Pack | Governance decisions, budget escalations | slides |
| 8 | Design Document / RFC | Technical proposals for peer review | docx |

Each framework has its own content template (`references/template-*.md`) and interview questions (`references/level2-*.md`).

### Format compatibility

Rendering is decoupled from content generation. Every framework produces a canonical Marp `.md` (or section-structured markdown for long-form outputs), and each renderer consumes that independently. Some framework × format combinations are more natural than others:

| Framework | docx | html | pptx | interactive | executive-html | Notes |
|-----------|------|------|------|-------------|----------------|-------|
| 1 McKinsey Pyramid | ✓ | ✓ | ✓ | ✓ | ✓ | Conclusion-first hero + argument cards |
| 2 Pitch Deck | ✓ | ✓ | ✓ | ✓ | ○ | Investors expect pptx/PDF — flag but allow |
| 3 Issue Tree | ✓ | ✓ | ✓ | ✓ | ✓ | Root-cause cards + solution tiles |
| 4 Roadmap | ✓ | ✓ | ✓ | ✓ | ✓ | Timeline component is a natural match |
| 5 Conference Talk | ✓ | ✓ | ✓ | ✓ | ✓ | Companion article / reading version |
| 6 RAID / Weekly | ✓ | ✓ | ✓ | ○ | ✓ | Dashboard page with RAG metrics — natural fit |
| 7 Steering Pack | ✓ | ✓ | ✓ | ○ | ✓ | Governance pack circulated as URL — strong fit |
| 8 Design Doc / RFC | **✓ primary** | ✓ | ○ | ○ | **✓ primary** | Richest component match for executive-html |

✓ = recommended, ○ = available but flagged as suboptimal before rendering.

## Output Formats

| Format | Description | Engine |
|--------|-------------|--------|
| **html** | Static Marp presentation with pre-rendered SVG diagrams | `marp-cli` |
| **interactive** | Self-contained HTML with CSS slide transitions, keyboard navigation, progressive bullet builds, client-side mermaid diagrams, syntax-highlighted code blocks, and presenter mode (press P) | `interactive_renderer.py` (pure Python) |
| **pptx** | Native editable PowerPoint with positioned text boxes, themed colour palettes, and embedded PNG diagrams | `pptx_builder` manifest pipeline via `python-pptx` |
| **docx** | Flowing Word document — the prose adapter restructures slides into headings and paragraphs suited for reading, then pandoc produces the DOCX | Prose adapter + `pandoc` |
| **executive-html** | Premium single-page dark-luxury reading artifact using the obsidian design system — self-contained HTML with theme toggle, scroll-reveal animations, and component-driven layout (hero, cards, tiles, metrics, tables, timelines) | Agent-generated from vendored design system |

All formats start from the same canonical Marp markdown source (slide-structured for html/interactive/pptx, section-structured for docx/executive-html).

## Rendering Pipeline

The rendering pipeline has three stages: pre-render, render, verify.

### 1. Pre-render (charts, mermaid, then excalidraw)

```bash
# Step 1: Convert ```chart YAML fences to SVG + PNG via matplotlib
poetry run story-present-prerender-chart \
    --input <raw.md> \
    --output <dir> \
    --assets-dir <assets>

# Step 2: Convert ```mermaid fences to SVG + PNG via mmdc
poetry run story-present-prerender-mermaid \
    --input <chart-rewritten.md> \
    --output <dir> \
    --engine mmdc \
    --assets-dir <assets>
```

```bash
# Step 3: Render excalidraw JSON to PNG via Playwright + Chromium
poetry run story-present-render-excalidraw \
    --input <file>.excalidraw \
    --output <file>.png \
    --scale 2 \
    --width 1920
```

All three steps produce SVG (for HTML) and/or PNG siblings (for PPTX/DOCX). Order matters: chart pre-render runs first, mermaid second, excalidraw last — each consumes the output of the previous step.

### 2. Render to output format

```bash
# Static HTML
poetry run story-present-render-html \
    --input <pre-rendered.md> --output <path>.html --theme <name>

# Interactive HTML (uses raw source — client-side mermaid)
poetry run story-present-render-interactive \
    --input <raw.md> --output <path>.html --theme <name>

# Native PPTX
poetry run story-present-render-pptx-native \
    --input <pre-rendered.md> --output <path>.pptx --theme <name>

# Flowing DOCX
poetry run story-present-render-docx \
    --input <pre-rendered.md> --output <path>.docx --theme <name>
```

### 3. Visual verification (deferred post-review)

```bash
poetry run story-present-verify-visual \
    --input <pre-rendered.md> --output-dir <slug>/verify --theme <name>
```

Screenshots every slide as PNG via `marp --images png`. Run this after the canonical markdown is persisted and reviewed. If the current model cannot inspect images, prompt the user to switch to a vision-capable model before visual QA; only if switching is unavailable or declined, keep the generated PNGs for human review and mark the output `visual-review-pending`.

Immediately before this step, prompt the user to switch to a vision-capable model for visual QA. Verify all image-bearing slides (not a sample): Mermaid/Chart SVG-backed renders, PNG assets, screenshots, photos, and excalidraw outputs.

## Themes

Seven themes mapped to audience type:

| Theme | Register | Audience |
|-------|----------|----------|
| `business` | White + navy + top-border accent | C-suite, executives |
| `tech` | GitHub-dark + blue/green | Developers, engineering |
| `dark` | Black + cyan/purple glow | Keynote, showcase |
| `editorial` | Warm neutrals + serif | Board, directors |
| `conference` | Slate + cyan, code-friendly | Conference, meetup |
| `minimal` | White + grey + geometric | Internal, weekly, team |
| `vibrant` | Dominant colour + sharp accent | Creative, marketing |

Theme CSS previews live in `references/themes/<name>.css`. Rendering asset bundles live in `assets/themes/<name>/`.

## Scoring

Every generated output is self-evaluated against a **layered rubric** — a universal base (65 points) plus an output-class overlay (35 points), always totalling 100.

### Scoring route (format-based)

The user's chosen output format determines which overlay is loaded — no framework-based inference needed:

```python
if output_format in ("pptx", "html", "interactive"):
    output_class = "slides"
elif output_format == "docx":
    output_class = "prose"
elif output_format == "executive-html":
    output_class = "executive-html"
```

### Universal base (65 pts — all frameworks)

| Criterion | Weight |
|-----------|--------|
| Structural compliance | 20 |
| MECE coverage | 10 |
| Audience alignment | 10 |
| Evidence presence | 5 |
| Technical depth (conditional) | 5 |
| Narrative flow | 10 |
| Constraint compliance | 5 |

### Slide overlay (35 pts — when output_format is html/interactive/pptx)

| Criterion | Weight |
|-----------|--------|
| Action / declarative titles | 15 |
| One message per slide | 10 |
| Marp syntax + content fit | 5 |
| Slide constraint compliance | 5 |

### Prose overlay (35 pts — when output_format is docx)

| Criterion | Weight |
|-----------|--------|
| Section headings | 10 |
| Paragraph discipline | 10 |
| Specificity & depth | 10 |
| Prose syntax correctness | 5 |

### Executive HTML overlay (35 pts — when output_format is executive-html)

| Criterion | Weight |
|-----------|--------|
| Section headings + navigation | 10 |
| Component selection | 10 |
| Design token compliance | 10 |
| Density + visual rhythm | 5 |

### Hard gates (binary PASS/FAIL, separate from 100-point score)

- **Slides:** Visual variety gate — images >= ceil(slides/3), at least 1 diagram, at least 2 distinct image directives.
- **Prose:** Document quality gate — word count >= 800, sections >= 4, evidence density >= 3, valid heading hierarchy, specificity floor.
- **Executive HTML:** Self-contained (single .html, no external deps beyond Google Fonts), theme toggle with localStorage, 6 accent + 4 bg tokens in both themes, noise texture, component minimum >= ceil(sections/2).

### Quality pipeline for prose (Options 5 docx + 8)

Prose outputs run an additional **mid-generation prose refinement pass** (hedging scan, ABT rhythm, alternating rhythm, insight landing, specificity, layered depth) between generation and scoring. This is a deliberate +1 LLM pass — quality first.

Outputs scoring below 75 are automatically refined (up to 2 iterations). Outputs below 60 after refinement are delivered with explicit caveats.

## Directory Structure

```
story-present/
  SKILL.md              # Full skill definition and process
  README.md             # This file
  assets/
    themes/<name>/      # Rendering asset bundles (theme.css, template.pptx, reference.docx)
  references/           # Templates, rubrics, conventions, interview guides
  evals/                # Skill evaluation framework
  samples/              # Example decks
```

## CLI Shortcuts

All tools are invoked via `poetry run <shortcut>`. See `references/cli-tools.md` for full flag documentation and porting instructions.

| Shortcut | Purpose | Pipeline stage |
|----------|---------|----------------|
| `story-present-check-deps` | Verify all dependencies installed | Preflight |
| `story-present-prerender-chart` | `chart` YAML fences → SVG + PNG | Pre-render 1 |
| `story-present-prerender-mermaid` | `mermaid` fences → SVG + PNG | Pre-render 2 |
| `story-present-render-excalidraw` | Excalidraw JSON → PNG | Pre-render 3 |
| `story-present-render-html` | Marp → static HTML | Render |
| `story-present-render-interactive` | Marp → interactive HTML (client-side mermaid, presenter mode) | Render |
| `story-present-render-pptx-native` | Marp → native editable PPTX (primary) | Render |
| `story-present-render-pptx` | Marp → PPTX (fallback) | Render |
| `story-present-render-docx` | Marp → flowing DOCX via pandoc | Render |
| `story-present-verify-visual` | Screenshot slides as PNGs for visual check | Post-review |

## Quick Start

1. Install dependencies: `poetry install` and the system binaries above
2. Run `poetry run story-present-check-deps` to verify
3. Ask the skill to create a presentation — it will interview you (with probing on audience/scope/goal), negotiate scope, route to a framework, generate with a mid-point checkpoint, score, and persist canonical markdown for review
4. Review/approve the persisted content, then choose output format(s): `html`, `interactive`, `pptx`, `docx`, `executive-html`, or `all`
5. Run deferred visual verification (`story-present-verify-visual`) for final render QA
