# CLI Tools Reference

The story-present skill delegates all rendering, pre-rendering, and verification to CLI tools invoked via `poetry run`. This reference documents every tool the skill calls, its flags, inputs, outputs, and purpose.

When porting the skill to a new project, each tool listed here must be implemented and wired as a Poetry script shortcut — or replaced with an equivalent that accepts the same flags and produces the same output.

---

## Quick Reference

| Shortcut | Purpose | Required by |
|----------|---------|-------------|
| `story-present-check-deps` | Verify all dependencies are installed | Preflight (before any render) |
| `story-present-prerender-chart` | `chart` YAML fences → SVG + PNG via matplotlib | Pre-render step 1 |
| `story-present-prerender-mermaid` | `mermaid` fences → SVG + PNG via mmdc | Pre-render step 2 |
| `story-present-render-excalidraw` | Excalidraw JSON → PNG via Playwright | Pre-render step 3 |
| `story-present-render-html` | Marp markdown → static HTML via marp-cli | Format: html |
| `story-present-render-interactive` | Marp markdown → interactive HTML (client-side) | Format: interactive |
| `story-present-render-pptx-native` | Marp markdown → native PPTX via manifest pipeline | Format: pptx (primary) |
| `story-present-render-pptx` | Marp markdown → PPTX via AST parsing | Format: pptx (fallback) |
| `story-present-render-docx` | Marp markdown → flowing DOCX via prose adapter + pandoc | Format: docx |
| `story-present-verify-visual` | Screenshot slides as PNGs for visual inspection | Post-review verification |

---

## Tool Details

### story-present-check-deps

Verifies that all Python packages, system binaries, and the Playwright Chromium browser are installed. Run this before any rendering.

```
story-present-check-deps [--json]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--json` | no | (always JSON) | Emit JSON output |

**Output:** JSON array of `{name, present, hint}` objects. Exit 0 if all present, exit 1 if any missing.

**Checks:** python-pptx, markdown-it-py, pyyaml, matplotlib, playwright (Python); marp-cli, pandoc, mmdc (system binaries); Chromium browser (Playwright).

---

### story-present-prerender-chart

Converts ` ```chart ` YAML fences in Marp markdown to SVG and PNG images via matplotlib. This is the **first** pre-render step — run before mermaid.

```
story-present-prerender-chart --input <raw.md> --output <dir> --assets-dir <assets> [--json]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input` | yes | — | Path to the Marp markdown source |
| `--output` | yes | — | Directory to write the rewritten markdown |
| `--assets-dir` | yes | — | Directory for generated SVG + PNG assets |
| `--json` | no | — | Emit JSON result |

**Input:** Marp markdown containing ` ```chart ` fences with YAML chart definitions.
**Output:** Rewritten markdown with chart fences replaced by `![](assets/chart-N.svg)` image references, plus SVG and PNG files in the assets directory.

---

### story-present-prerender-mermaid

Converts ` ```mermaid ` fences to SVG and PNG images via the mmdc (Mermaid CLI) engine. This is the **second** pre-render step — run after chart pre-render.

```
story-present-prerender-mermaid --input <chart-rewritten.md> --output <dir> --assets-dir <assets> [--engine mmdc] [--json]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input` | yes | — | Path to the Marp markdown (post-chart pre-render) |
| `--output` | yes | — | Directory to write the rewritten markdown |
| `--assets-dir` | yes | — | Directory for generated SVG + PNG assets |
| `--engine` | no | `mmdc` | Rendering engine (`mmdc` for local Mermaid CLI) |
| `--json` | no | — | Emit JSON result |

**Input:** Marp markdown containing ` ```mermaid ` fences.
**Output:** Rewritten markdown with mermaid fences replaced by image references, plus SVG and PNG files in the assets directory.

---

### story-present-render-excalidraw

Renders an Excalidraw JSON file to PNG via Playwright + headless Chromium. This is the **third** pre-render step — run after mermaid, for each excalidraw placeholder in the appendix.

```
story-present-render-excalidraw --input <file>.excalidraw --output <file>.png [--scale 2] [--width 1920]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input`, `-i` | yes | — | Path to the `.excalidraw` JSON file |
| `--output`, `-o` | no | input with `.png` suffix | Output PNG path |
| `--scale`, `-s` | no | `2` | Device scale factor |
| `--width`, `-w` | no | `1920` | Maximum viewport width in pixels |

**Input:** A valid Excalidraw JSON file (`{"type": "excalidraw", "elements": [...]}`).
**Output:** PNG file. JSON result printed to stdout with `ok`, `input`, `output`, `scale`, `max_width`, `size_bytes`.

---

### story-present-render-html

Renders pre-rendered Marp markdown to standalone static HTML via marp-cli. The theme CSS is applied via `--theme-set`.

```
story-present-render-html --input <pre-rendered.md> --output <path>.html [--theme <name>]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input` | yes | — | Path to Marp markdown source (post pre-render) |
| `--output` | yes | — | Path to write the HTML file |
| `--theme` | no | `default` | Theme name (looks up `assets/themes/<name>/theme.css`) |

**Requires:** marp-cli (`npm install -g @marp-team/marp-cli`).
**Input:** Marp markdown with all fences already pre-rendered to image references.
**Output:** Self-contained HTML file with inlined CSS.

---

### story-present-render-interactive

Renders raw Marp markdown to a self-contained interactive HTML page with CSS slide transitions, keyboard navigation, progressive bullet builds, client-side mermaid rendering, syntax-highlighted code blocks, and presenter mode (press P).

```
story-present-render-interactive --input <raw.md> --output <path>.html [--theme <name>]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input` | yes | — | Path to Marp markdown source (raw — mermaid runs client-side) |
| `--output` | yes | — | Path to write the HTML file |
| `--theme` | no | `default` | Theme name |

**Input:** Raw Marp markdown — mermaid fences are rendered client-side, no pre-rendering needed.
**Output:** Self-contained HTML file with embedded JavaScript for interactivity.

---

### story-present-render-pptx-native

**Primary PPTX renderer.** Converts pre-rendered Marp markdown to a native editable PowerPoint file using the `pptx_builder` manifest pipeline — positioned text boxes, themed colour palettes, and embedded images.

```
story-present-render-pptx-native --input <pre-rendered.md> --output <path>.pptx [--theme <name>]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input` | yes | — | Path to Marp markdown source (post pre-render) |
| `--output` | yes | — | Path to write the .pptx file |
| `--theme` | no | `tech` | Theme name (mapped to pptx_builder palette) |

**Requires:** python-pptx, Pillow, markdown-it-py.
**Input:** Marp markdown with all fences already pre-rendered to PNG/SVG.
**Output:** Editable .pptx file with positioned layouts.

---

### story-present-render-pptx

**Fallback PPTX renderer.** Uses markdown-it-py AST parsing and a blank slide layout for shape reconstruction. Available for quick draft renders when layout precision matters less.

```
story-present-render-pptx --input <pre-rendered.md> --output <path>.pptx [--theme <name>]
```

Flags are the same as `render-pptx-native`. Use `render-pptx-native` as the default.

---

### story-present-render-docx

Renders pre-rendered Marp markdown to a flowing Word document. The prose adapter (`docx_adapter.slides_to_prose`) restructures slides into headings and paragraphs, then pandoc produces the DOCX using a themed reference document.

```
story-present-render-docx --input <pre-rendered.md> --output <path>.docx [--theme <name>]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input` | yes | — | Path to Marp markdown source (post pre-render) |
| `--output` | yes | — | Path to write the .docx file |
| `--theme` | no | `default` | Theme name (looks up `assets/themes/<name>/reference.docx`) |

**Requires:** pandoc (system binary).
**Input:** Marp markdown with all fences already pre-rendered.
**Output:** Flowing .docx document (not slide-shaped).

---

### story-present-verify-visual

Screenshots every slide as PNG via marp-cli `--images png`. Used for deferred post-review visual verification — run after canonical markdown is persisted and content has been reviewed.

Immediately before this step, prompt the user to switch to a vision-capable model when image inspection is not available. Visual QA should cover all image-bearing slides (including Mermaid/Chart SVG-backed renders and PNG assets), not a sample.

```
story-present-verify-visual --input <pre-rendered.md> --output-dir <slug>/verify [--theme <name>]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input` | yes | — | Path to Marp markdown (pre-rendered with SVG refs) |
| `--output-dir` | yes | — | Directory to write one PNG per slide |
| `--theme` | no | `conference` | Theme name |

**Requires:** marp-cli.
**Output:** One PNG per slide in the output directory (slide-001.png, slide-002.png, ...).

---

## Pipeline Order

```
1. story-present-check-deps          (preflight)
2. story-present-prerender-chart     (chart YAML → SVG/PNG)
3. story-present-prerender-mermaid   (mermaid → SVG/PNG)
4. story-present-render-excalidraw   (excalidraw JSON → PNG, per placeholder)
5. Persist content + user review     (review canonical markdown before visual QA)
6. story-present-render-<format>     (final render to html/interactive/pptx/docx)
7. Model-switch checkpoint           (ask user to switch to vision-capable model if needed)
8. story-present-verify-visual       (screenshot slides for deferred visual check)
```

Steps 2-4 each consume the output of the previous step. Step 6 runs on the fully pre-rendered markdown (except `render-interactive`, which takes raw source). Step 8 runs after rendering and after the review checkpoint.

---

## Porting to a New Project

To use this skill in another project:

1. **Implement** each tool above as a CLI entry point (or adapt the Python modules from `tools/story_present/`)
2. **Wire** each as a Poetry script shortcut in `pyproject.toml`:
   ```toml
   [tool.poetry.scripts]
   story-present-check-deps = "tools.story_present.run:check_deps"
   story-present-prerender-chart = "tools.story_present.chart_prerender.cli:main"
   story-present-prerender-mermaid = "tools.story_present.mermaid_prerender.cli:main"
   story-present-render-excalidraw = "tools.story_present.run:render_excalidraw"
   story-present-render-html = "tools.story_present.run:render_html"
   story-present-render-interactive = "tools.story_present.run:render_interactive"
   story-present-render-pptx-native = "tools.story_present.run:render_pptx_native"
   story-present-render-pptx = "tools.story_present.run:render_pptx"
   story-present-render-docx = "tools.story_present.run:render_docx"
   story-present-verify-visual = "tools.story_present.run:verify_visual"
   ```
3. **Install** Python dependencies: `python-pptx`, `markdown-it-py`, `pyyaml`, `matplotlib`, `Pillow`, `mistune`, `playwright`
4. **Install** system binaries: `marp-cli`, `pandoc`, `mmdc` (optional)
5. **Run** `poetry run playwright install chromium` for excalidraw rendering
6. **Verify** with `poetry run story-present-check-deps`
