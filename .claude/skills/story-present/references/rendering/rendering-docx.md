# Rendering — DOCX (pandoc pipeline)

`story-present-render-docx` turns the canonical Marp `.md` into a Word
`.docx` via pandoc. This reference documents the pipeline, the
reference-doc theme strategy, and heading/table conventions.

## Engine — pandoc

Pandoc is the single tool for this target. It reads GitHub-flavoured
Markdown (which Marp is a superset of), maps headings and tables to Word
styles, and emits a `.docx`. The skill shells out via the CLI wrapper
rather than calling pandoc's API directly — this is the thin-wrapper
convention from `CLAUDE.md` "Adding a New CLI Action".

Install hint (Windows): `winget install --id JohnMacFarlane.Pandoc`. The
preflight check (`story-present-check-deps`) verifies it's on PATH.

## Invocation

```
pandoc <input>.md -o <output>.docx --reference-doc=<theme>/reference.docx
```

- `--reference-doc` points to the committed `reference.docx` for the
  theme the skill was asked to render. If the file is missing the
  renderer omits the flag and falls back to pandoc's built-in styles.
- The same `_resolve_binary` helper used by `render_html` resolves the
  pandoc executable on Windows (prefers `.exe`/`.cmd` shims).
- stderr from pandoc is surfaced verbatim on failure so users see the
  exact pandoc error.

## Reference docs

`assets/themes/<name>/reference.docx` is a minimal Word document
containing only the Word styles pandoc needs. We seed each theme from
pandoc's own default reference (`pandoc --print-default-data-file
reference.docx`) via `scripts/build_story_present_themes.py`. To rebrand
a theme:

1. Open the theme's `reference.docx` in Word.
2. Edit the **Heading 1**, **Heading 2**, **Heading 3**, **Normal**,
   **Table Grid**, and **List Paragraph** styles.
3. Save and commit — pandoc will pick up the new styles next render.

Do not add content to the reference doc — pandoc ignores content and
only reads styles.

## Heading mapping

Marp markdown headings map to Word styles as follows (pandoc default):

| Marp markdown | Word style |
|---------------|------------|
| `# Title` | Heading 1 |
| `## Subtitle` | Heading 2 |
| `### Detail` | Heading 3 |
| paragraph text | Normal |
| `- bullet` | List Paragraph |
| `\| table \|` | Table Grid |

Because Marp uses `---` as a slide separator, pandoc treats it as a
horizontal rule. The resulting `.docx` reads as a running document with
section breaks where slides end — intentional, so the docx target
behaves as "flat report" rather than "one page per slide". Teams asking
for "a presentation as a Word doc" almost always want the running-doc
form.

## Table styling

RAID and steering decks use markdown tables heavily. Pandoc maps these
to the **Table Grid** style in the reference doc. Adjust table fonts,
borders, and header colouring in `reference.docx` to propagate across
all decks.

## Verification contract

`render_docx` asserts:

1. Input file exists.
2. `pandoc` resolves on PATH.
3. `pandoc` exits zero (stderr surfaced on failure).
4. Output file exists and is non-empty after pandoc returns.
5. Returns JSON with `ok=true`, theme, `reference_doc` path (or null),
   and byte size.

## Prose adapter (slides_to_prose)

`render_docx` now runs `slides_to_prose()` from `tools/story_present/docx_adapter.py`
before passing the markdown to pandoc. This adapter restructures the Marp slide
deck into a flowing document that reads as a report, not slide-shaped blocks.

### What the adapter does

| Input element | Output |
|---------------|--------|
| Marp frontmatter (`---` YAML block) | Stripped |
| `<style>` blocks | Stripped |
| Slide separators (`---`) | Stripped |
| Speaker notes (`<!-- speaker: ... -->`) | Stripped |
| `<!-- _class: ... -->` directives | Stripped |
| Title slide heading (`# Title`) | H1 heading (document title) |
| Section breadcrumbs (`###### Section N`) | H2 heading |
| Slide titles (`# Title`) | H3 heading |
| Placeholder images (`placeholder://...`) | Italicised description text |
| Source citations (`<!-- Source: ... -->`) | Inline parenthetical text |
| Marp image alt-text directives | Simplified to plain `![](path)` |

### Result

The output reads as a flowing document with proper heading hierarchy:
- H1 for the document title
- H2 for major sections
- H3 for individual slide topics
- Bullet lists, tables, and code blocks preserved as-is

No slide separators, no Marp-specific syntax, no speaker notes visible in
the final Word document. Teams asking for "a presentation as a Word doc"
get a clean running-document form.
