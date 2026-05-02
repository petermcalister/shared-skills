# Marp Output Conventions

This file is loaded by `SKILL.md` during generation. It defines the exact Marp markdown syntax story-present must produce.

## Frontmatter (required on every deck)

Every generated `.md` file begins with:

```markdown
---
marp: true
theme: default
paginate: true
---
```

Substitute the theme name with the chosen shipped theme (`default`, `consulting`, `conference`, `status`) based on the framework route. When a custom theme CSS is applied at render time, keep the frontmatter `theme:` value matching the asset under `assets/themes/<name>/theme.css`.

## Slide separators

`---` on its own line between slides. No leading or trailing whitespace. One blank line before and after the separator.

```markdown
# Slide A title

Content for A.

---

# Slide B title

Content for B.
```

## Title slides

Use the `_class: lead` directive at the top of the first slide:

```markdown
<!-- _class: lead -->

# Deck title

Subtitle · Author · Date
```

`_class: lead` centres the content and applies the lead-slide variant of the theme.

## Section dividers

Use `<!-- _class: lead -->` with a section heading to mark major section breaks in long decks (conference talks, steering packs):

```markdown
<!-- _class: lead -->

# Part 2: The core argument
```

## Speaker notes

Every slide should carry a speaker note. Use an HTML comment prefixed with `speaker:`:

```markdown
# Slide title

Visible content here.

<!-- speaker: One or two sentences expanding on the slide for the presenter. -->
```

Speaker notes are mandatory for Option 5 (Conference / Tech Talk) per the template rule. For other options they are strongly recommended.

## Chart placeholders

When the source data is not yet available, use a fenced HTML comment block describing the chart:

```markdown
<!-- CHART: Bar chart showing Q1-Q4 revenue by region. Data: [to be provided] -->
```

The render pipelines preserve these as editable text in PPTX/DOCX so the user can substitute the real chart downstream.

## General data placeholders

Use `[DATA NEEDED: brief description]` inline wherever a concrete value is missing. This is the canonical string the user will search-and-replace later. Do not invent data.

```markdown
- Europe market grew [DATA NEEDED: Q4 2025 growth rate]%, outpacing all other regions.
```

## RAG indicators (Options 4 and 5)

Use Unicode emoji:

- 🟢 Green — on track, according to plan
- 🟡 Amber — at risk, mitigation in place or needed
- 🔴 Red — critical, requires immediate attention or escalation

Place the emoji in a dedicated `RAG` column for tables, or inline with the status label for single-line statements.

```markdown
| Workstream | Phase | RAG | Key update |
|------------|-------|-----|------------|
| Platform rebuild | Build | 🟡 | Vendor dependency slipping 2 weeks |
```

## Tables

Use standard GitHub-flavoured markdown tables for most cases. For RAID tables with many columns, use HTML `<table>` tags with `<style scoped>` for font-size reduction so the table fits on a single slide:

```markdown
<style scoped>
table { font-size: 0.72em; }
</style>

| ID | Category | Description | Impact | Owner | Status | RAG |
|----|----------|-------------|--------|-------|--------|-----|
| RS-001 | Risk | Vendor delay | High | J. Smith | Mitigating | 🟡 |
```

## Action titles vs declarative headings

- **Consulting frameworks (Options 1–4, 6–7):** action titles — complete sentences stating findings, not topic labels.
  - BAD: `## Market Analysis`
  - GOOD: `## The European market grew 23% in Q4, outpacing all other regions`
- **Conference talk (Option 5):** declarative topic headings.
  - GOOD: `## How we scaled the ingest pipeline`
- **Design document (Option 8):** descriptive section headings.
  - GOOD: `## Proposed Design`

Never mix styles in the same deck.

## One message per slide

Each slide communicates exactly one idea. If you have two points, you need two slides.

## Citation format

When a slide uses data from an ingested source, append a citation on the last line of that slide:

```markdown
<!-- Source: memory-event-42 -->
<!-- Source: gmail-msg-abc123 -->
<!-- Source: commit 19f61a6 -->
<!-- Source: pete-pa/topics/quarterly-review/q4-review.md -->
```

Keep citations inside HTML comments so they do not render in the main body but are preserved in the Marp source for audit.

## Visual minimums per layout type

Every slide whose template marks a layout type MUST contain the matching visual element. If no real asset is available, use the fallback.

| Layout type | Required visual element | Fallback if no real asset |
|---|---|---|
| `split-image` | `![bg right:40%](<path>)` or `![bg left:40%](<path>)` | Placeholder directive with `placeholder://visual-needed` URL + `*[See Appendix: P<n>]*` back-reference (see `visual-design-principles.md` §"Rich visual placeholder protocol") |
| `diagram` | ` ```mermaid ` fence (syntactically valid) | Skeleton from template with `<infer>` labels |
| `code-block` | Fenced code block with language hint | — (always producible from source material) |
| `evidence` | ` ```chart ` fence OR ` ```mermaid ` fence OR `![w:700](<path>)` | Placeholder directive + appendix back-reference, or chart skeleton |
| `quote` | Blockquote with attribution | — (text-only, no visual needed) |
| `text-only` | No visual required | — |

## Palette CSS injection

After choosing a theme via the audience→theme picker, inject a `<style>` block into the generated Marp markdown so the palette is visible even in raw preview (VS Code extension, `marp-cli` without `--theme`).

### Procedure

1. Read the chosen theme's preview CSS from `references/visual/themes/<name>.css`.
2. Extract the 9 custom properties: `--bg`, `--fg`, `--accent`, `--accent2`, `--muted`, `--table-bg`, `--table-head-bg`, `--table-head-fg`, `--table-border`.
3. Emit the following `<style>` block **after** the closing `---` of the Marp frontmatter (not inside the YAML):

```markdown
---
marp: true
theme: default
paginate: true
---

<style>
:root {
  --bg: <value>;
  --fg: <value>;
  --accent: <value>;
  --accent2: <value>;
  --muted: <value>;
  --table-bg: <value>;
  --table-head-bg: <value>;
  --table-head-fg: <value>;
  --table-border: <value>;
}
section { background: var(--bg); color: var(--fg); }
section h1, section h2 { color: var(--accent); }
section h6 { color: var(--muted); }
section a { color: var(--accent2); }
section blockquote { border-left-color: var(--accent); color: var(--muted); }
section table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
  background: var(--table-bg);
  color: var(--fg);
}
section th,
section td {
  border: 1px solid var(--table-border);
  padding: 0.35em 0.45em;
  text-align: left;
  vertical-align: top;
}
section th {
  background: var(--table-head-bg);
  color: var(--table-head-fg);
}
section tbody tr:nth-child(even) td {
  background: rgba(127, 127, 127, 0.08);
}
</style>
```

4. The render-time `--theme <name>` flag still applies the full asset bundle CSS, but the inline `<style>` provides a visible palette and readable table defaults even in raw Marp preview.
5. Use `<style>` (global), NOT `<style scoped>`. Scoped styles apply per-slide; the palette must apply to the entire deck.

## Skill-owned rendering

After the deck is generated and scored, SKILL.md asks the user which formats to deliver and invokes the matching CLI shortcut under `tools/story_present/`:

| Target | Engine | CLI shortcut | Theme asset |
|--------|--------|--------------|-------------|
| Marp `.md` | — | (written directly by the skill) | `assets/themes/<name>/theme.css` referenced in frontmatter |
| Rich HTML | `marp-cli` | `story-present-render-html` | `assets/themes/<name>/theme.css` |
| PPTX | `python-pptx` (preferred) or `marp-cli --pptx` | `story-present-render-pptx` | `assets/themes/<name>/template.pptx` |
| Word `.docx` | `pandoc` | `story-present-render-docx` | `assets/themes/<name>/reference.docx` |

The skill must verify the rendered file exists and is non-empty per `.claude/rules/verification.md` before claiming delivery success.

---

## Long-form content rules

These rules apply when `output_format ∈ {docx, executive-html}`. They override the slide-oriented defaults above for content that will be consumed as flowing prose or rich HTML pages.

1. **"One theme per section" replaces "one message per slide."**
   `---` separators mark logical sections. Content within a section may contain multi-paragraph prose, subsections, and embedded artifacts.

2. **Use descriptive section headings, not action titles.**
   Put the action-title insight as the lead sentence of the section body instead. Heading should be a semantic label that works in a table of contents or scroll-spy navigation.

3. **Use h3/h4 freely for subsections within a `---` section.**
   These drive heading hierarchy in docx (ToC generation) and nav structure in executive HTML (scroll-spy anchors). No limit on nesting depth within a section.

**Scope:** Affects generation for Options 5-docx, 6, 7, 8 when output format is `docx` or `executive-html`. No change to slide generation path.
