# Rendering — PPTX (editable)

`story-present-render-pptx` turns the canonical Marp `.md` into an editable
PowerPoint deck. This reference documents the engine choice, the slide
reconstruction pipeline, and how chart placeholders survive the round trip.

## Engine choice — python-pptx (primary)

PRD Section 8 lists `pptxgenjs` (Node) **or** `python-pptx` (Poetry) as
candidates. OQ6 resolves in favour of **python-pptx** for this skill.

| Option | Why we chose (or didn't) |
|--------|--------------------------|
| **python-pptx** (chosen) | Poetry-native — no Node runtime for the primary path. Full editable shape reconstruction (title, body, notes) via the python API. Reuses the existing `.venv`. Rock-solid for inserting text shapes, notes, and charts. |
| `pptxgenjs` (Node) | Requires a second runtime and an extra npm install step. Better canvas/chart ergonomics, but we only need minimal chart placeholders for now — the editability benefit is the same either way. |
| `marp-cli --pptx` | **Rejected as primary.** Marp's PPTX exporter rasterises slides to images — the output is not editable in PowerPoint, which defeats the goal of the PPTX target. Acceptable only as a fallback if fidelity of a visual layout matters more than editability. |

The chosen engine is wired into `tools/story_present/run.py::render_pptx`.

## Slide reconstruction pipeline

The Marp markdown is parsed by a slide-aware splitter that runs alongside
`markdown-it-py` (imported for token validation and to assert the dep is
installed per PRD Section 15 preflight). The splitter yields one dict per
slide with these fields:

| Field | Source | Destination in PPTX |
|-------|--------|---------------------|
| `title` | First `# ` or `## ` heading in the slide | Top text box (28pt bold) |
| `body_lines` | Non-heading, non-comment lines | Body text box (multi-paragraph) |
| `notes` | `<!-- speaker: ... -->` HTML comments | `slide.notes_slide.notes_text_frame` |
| `chart_placeholders` | Every `[DATA NEEDED: ...]` occurrence | Dedicated italic text box below the body |

Shapes are created on the **blank** layout (`slide_layouts[6]`) so the
renderer owns layout decisions instead of inheriting template placeholder
geometry. No pictures are ever inserted — this is what keeps the output
editable and is what the behave scenario asserts.

## Theme templates

`assets/themes/<name>/template.pptx` is an empty python-pptx deck used as
the starting `Presentation(path)`. We strip any pre-existing slides from
the template before appending our reconstruction, so the template exists
only to carry slide masters and the 16:9 slide size. Replacing a theme's
template swaps branding without touching the reconstruction code.

If the template file is missing at render time, the engine falls back to
`Presentation()` (python-pptx's built-in default) and logs the theme in
the JSON output so the caller can catch the fallback.

## Chart placeholder handling

The `[DATA NEEDED: description]` token is the canonical marker in Marp
(PRD Section 8). The splitter captures every occurrence per slide and
emits each as its own italic text box below the body. Users can then
search-replace the placeholder text or delete the box and drop in a real
chart — PowerPoint sees it as a normal text shape.

## Verification contract

`render_pptx` asserts:

1. Input file exists and is readable.
2. `python-pptx` and `markdown-it-py` import successfully (otherwise the
   preflight check should have caught this — we re-check defensively).
3. Output file exists and is non-empty after `prs.save()`.
4. Returns a JSON payload with `ok=true`, slide count, and byte size.

Per `.claude/rules/verification.md`, callers must still run
`ls -la <output>` and a `Presentation(path)` round-trip to confirm the
file opens before claiming delivery.

## Fidelity trade-offs vs marp-cli --pptx

| Dimension | python-pptx (ours) | marp-cli --pptx |
|-----------|-------------------|-----------------|
| Editability | Full — titles, body, notes are live text | None — every slide is a single image |
| Theme CSS | Not applied (we own shapes directly) | Applied at rasterisation time |
| Speaker notes | Preserved | Preserved |
| Chart placeholders | Editable text boxes | Baked into the image |
| Fidelity to HTML render | Approximate (we own layout) | High (pixel match) |
| Round-trip to user edits | Works | Broken — editing means redrawing in PPT |

Use marp-cli --pptx only if you need a visual snapshot for a read-only
recipient and an HTML file won't do.

## Native PPTX via manifest pipeline (primary path)

`story-present-render-pptx-native` is now the **primary PPTX rendering path**.
It reads Marp markdown, converts it to a JSON manifest via
`manifest_from_slides.py`, then calls `build_deck.py` to produce a native
PPTX with positioned text boxes, themed colour palettes, and proper slide
layouts.

### How it works

1. **Parse** -- `slides_to_manifest()` splits the Marp markdown on `---`
   separators and classifies each slide by type (lead, split-image, diagram,
   bullets/content, numbers/metrics).
2. **Map theme to palette** -- The 7 story-present theme names are mapped to
   pptx_builder's 12 palette names via `references/visual/theme-palette-map.md`.
   For example, `tech` maps to `ocean`.
3. **Build** -- `build_from_manifest()` creates positioned shapes (title box,
   body box, notes) on each slide using the palette colours and layout
   coordinates from `references/visual/slide-types-pptx.md`.

### CLI usage

```bash
poetry run story-present-render-pptx-native --input deck.md --output deck.pptx --theme tech
```

### Fallback: story-present-render-pptx (Marp AST path)

The original `story-present-render-pptx` remains available as a fallback for
quick or draft renders. It uses the simpler slide-aware splitter with
`markdown-it-py` tokenisation and produces editable shapes on blank layouts.
Use the native path for final delivery; use the AST path when speed matters
more than layout precision.

### SVG → PNG auto-conversion

python-pptx cannot embed SVG images directly. The `_add_picture_safe()`
function in `build_deck.py` automatically looks for a `.png` sibling when
given an `.svg` path. The mermaid pre-render step (`MmdcEngine`) generates
both `.svg` and `.png` from each mermaid fence, so PNG siblings are always
available when `mmdc` is the engine. Feed the **pre-rendered markdown** (with
`![w:900 contain](assets/mermaid-*.svg)` refs) to `render_pptx_native` — the
builder resolves the SVG path, finds the PNG sibling, and embeds that instead.

If no PNG sibling exists (e.g. when mmdc was not available), the builder
falls back to a styled placeholder text box describing the diagram.
