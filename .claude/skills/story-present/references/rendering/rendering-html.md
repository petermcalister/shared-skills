# Rendering to rich HTML

**Feature:** F019
**PRD sections:** 2 Goal 3, 3 (architecture), 8 (rendering ownership table), 15 (dependencies)

This reference documents how the `story-present` skill renders a Marp markdown deck to a standalone, themed HTML file. The skill owns *orchestration* (which theme, which engine, which flags); the actual `marp-cli` invocation is handled by the thin plumbing shortcut `story-present-render-html` under `tools/story_present/run.py`.

---

## CLI shortcut

```bash
poetry run story-present-render-html \
    --input  /path/to/deck.md       \
    --output /path/to/out.html      \
    --theme  consulting
```

The shortcut is a thin argparse wrapper. It:

1. Verifies the input file exists.
2. Resolves the theme CSS at `pete-pa/skills/story-present/assets/themes/<theme>/theme.css` and aborts with an actionable error if missing.
3. Creates the parent directory of `--output` if necessary.
4. Resolves the `marp` binary via `shutil.which` (preferring `marp.cmd` / `marp.exe` on Windows so npm shims execute correctly under `subprocess`).
5. Shells out to marp-cli with the invocation below.
6. Verifies the output file exists and is non-empty on return.
7. Emits a JSON status object (`{ok, input, output, theme, size_bytes}`).

Exit codes: `0` on success, `1` on any failure (missing input, missing theme, marp-cli not installed, marp-cli non-zero exit, empty output file).

---

## marp-cli invocation

```bash
marp <input.md> --html --theme-set <theme.css> --output <out.html>
```

| Flag | Purpose |
|------|---------|
| `<input.md>` | Positional argument — the canonical Marp markdown file the skill produced. |
| `--html` | Enables HTML passthrough (allows Marp directive comments and inline markup). Required for the consulting/conference/status themes, which use `<span class="rag-*">` utility classes in tables. |
| `--theme-set <theme.css>` | Registers the theme CSS with marp-cli for this invocation. The `theme:` directive inside the deck's frontmatter must match the theme name declared in the CSS's `@theme` comment (e.g. `theme: consulting`). |
| `--output <out.html>` | Destination HTML file. marp-cli infers the output format from the file extension. |

No other flags are set. `marp-cli` bundles its CSS inline into the output, so the HTML file is self-contained for CSS. However, image references (`<img src="assets/...">`) are external — the shortcut automatically copies SVG and PNG assets from the input markdown's `assets/` directory to the output HTML's `assets/` directory so relative paths resolve in the browser.

---

## Theme assets

Each shipped theme lives under `pete-pa/skills/story-present/assets/themes/<name>/theme.css` and is a valid Marp theme starting with `/* @theme <name> */`, then `@import 'default';`, then overrides.

| Theme | Intended for | Look & feel |
|-------|--------------|-------------|
| `default` | Any deck that hasn't picked something more opinionated | Clean sans-serif, light background, neutral palette |
| `consulting` | Options 1, 2, 3, 4 (pyramid, storyline) | Serif Georgia body, navy (`#0b1f3a`) accents, bordered headings, disciplined whitespace — McKinsey/BCG tradition |
| `conference` | Option 5 (conference / tech talk) | Dark mode (`#0f172a` background), cyan accents, monospace code blocks — optimised for code-heavy talks |
| `status` | Options 6, 7 (RAID, steering committee) | Dense tables, compact padding, RAG utility classes (`.rag-red`, `.rag-amber`, `.rag-green`) for risk indicators |
| `tech` | Option 8 (design doc / RFC) | GitHub-dark + blue/green, code-friendly — natural register for technical documents |

---

## Theme selection in the skill

Per PRD Open Question 1 (OQ1) default, the skill applies a fixed default theme per framework, overridable via an explicit user request:

| Framework | Default theme |
|-----------|---------------|
| Option 1 (Pyramid) | `consulting` |
| Option 2 (Market Strategy) | `consulting` |
| Option 3 (Problem-Solving) | `consulting` |
| Option 4 (Roadmap) | `consulting` |
| Option 5 (Conference) | `conference` |
| Option 6 (RAID / Weekly Status) | `status` |
| Option 7 (Steering Committee) | `status` |
| Option 8 (Design Doc / RFC) | `tech` |

The skill passes the resolved theme name to `story-present-render-html --theme <name>` and makes sure the deck's frontmatter `theme:` directive matches.

---

## Verification (post-render)

Per `.claude/rules/verification.md`, the skill must verify the claim "HTML rendered" before declaring success. The shortcut already asserts non-zero file size internally, but the skill should additionally:

1. `ls -la <out.html>` — confirm non-zero byte size.
2. Open the file (or `head -20`) — confirm the first line is `<!DOCTYPE html>`.
3. Grep for the theme class — `grep -c 'consulting\|conference\|status' <out.html>` should return >0 when the matching theme is used.

---

## Failure modes

| Failure | Cause | Fix |
|---------|-------|-----|
| `ERROR: marp-cli not installed` | `marp` shim not on PATH | `npm install -g @marp-team/marp-cli` (run `story-present-check-deps` to confirm) |
| `ERROR: theme '<name>' not found` | Theme directory missing or typo | Check `pete-pa/skills/story-present/assets/themes/` — only `default`, `consulting`, `conference`, `status` ship |
| `ERROR: output not produced or empty` | marp-cli succeeded but wrote a zero-byte file (usually means input Marp was malformed) | Re-read the Marp file, check frontmatter, ensure slide separators are `---` on their own lines |
| `OSError: %1 is not a valid Win32 application` | Subprocess tried to exec the bare `marp` shell script on Windows | Already handled by `_resolve_binary` — report as a bug if seen |

---

## Two HTML output types

The skill offers two distinct HTML renderers:

| | Static HTML (`render-html`) | Interactive HTML (`render-interactive`) |
|---|---|---|
| **Engine** | marp-cli (external binary) | `interactive_renderer.py` (pure Python) |
| **Mermaid** | Pre-rendered to SVG via mmdc before marp-cli runs | Client-side rendering via embedded mermaid.min.js |
| **Code highlighting** | Marp's built-in code blocks | Embedded highlight.js with theme-matched stylesheet |
| **Navigation** | Static slides (scroll or PgDn) | Arrow keys, space, swipe; CSS transitions (fade + lead zoom) |
| **Progressive builds** | Not supported | Bullet-by-bullet reveal on advance |
| **Presenter mode** | Not supported | Press **P** to open a presenter window with notes and slide preview |
| **Overview grid** | Not supported | Press **Escape** to see all slides in a grid |
| **Deep linking** | Not supported | URL hash (`#3`) jumps to slide 3 |
| **Self-contained** | CSS inlined; images may be external | Fully self-contained -- no external URLs in `<script src>` or `<link href>` |
| **Input** | Marp markdown (after mermaid pre-rendering) | Raw Marp markdown source (mermaid runs client-side) |

### Chart, Mermaid, and Excalidraw pre-render pipeline

Charts use `story-present-prerender-chart` to convert `` ```chart `` YAML fences to SVGs + PNGs via matplotlib. Run chart pre-render BEFORE mermaid pre-render; the mermaid step consumes the chart-rewritten markdown. Excalidraw pre-rendering runs last, converting appendix-referenced `.excalidraw` JSON files to PNGs via Playwright + headless Chromium and replacing `placeholder://visual-needed` URLs with real image paths.

```
deck.md  -->  story-present-prerender-chart  -->  deck-charts.md  -->  story-present-prerender-mermaid  -->  deck-mermaid.md  -->  story-present-render-excalidraw  -->  deck-final.md
```

1. **Chart pre-render**: convert `` ```chart `` YAML fences to SVG + PNG via matplotlib.
2. **Mermaid pre-render**: convert `` ```mermaid `` fences to SVG + PNG via mmdc.
3. **Excalidraw pre-render** (if appendix has excalidraw placeholders):
   ```bash
   story-present-render-excalidraw --input <file>.excalidraw --output <file>.png
   ```
   Renders each Excalidraw JSON to PNG, then `replace_placeholders` rewrites `placeholder://visual-needed` URLs to real image paths and removes fulfilled appendix table rows.

The chart pre-render emits `![w:700 contain]` directives (smaller than the `![w:900 contain]` used for diagrams) because charts typically share the slide with bullet text.

### When to use which

- **Static HTML** -- best for email attachments, archival, or environments where JavaScript is blocked.
- **Interactive HTML** -- best for live presenting, screen sharing, or any scenario where navigation, transitions, and presenter mode add value.

### Interactive renderer CLI shortcut

```bash
poetry run story-present-render-interactive \
    --input  /path/to/deck.md       \
    --output /path/to/out.html      \
    --theme  tech
```

The shortcut verifies the input file exists, resolves the theme CSS for colour variables, invokes the Python renderer, and verifies the output is non-empty. The interactive renderer reads the raw Marp source directly (no mermaid pre-rendering step needed) because mermaid diagrams are rendered client-side by the embedded mermaid.min.js library.

---

## Related references

- `references/generation/marp-conventions.md` — Marp syntax, slide separators, directives
- `references/rendering/rendering-pptx.md` — PPTX rendering
- `references/rendering/rendering-docx.md` — DOCX rendering
- `tools/story_present/run.py::render_html` — the static HTML implementation
- `tools/story_present/interactive_renderer.py` — the interactive HTML implementation
