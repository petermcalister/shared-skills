# Design Principles

Ten rules for slide layout and visual design. Apply these when planning slide types and generating the manifest.

---

## The 10 Rules

### 1. No boring slides
Every slide needs a visual element -- a diagram, a metric callout, a coloured text block, or a shaped container. A wall of text is never acceptable. If a slide has only prose, add bullets, a metric, or split into two slides.

### 2. Bold, content-informed palettes
Colours should feel designed for THIS topic, not a generic corporate template. Select the palette that matches the archetype and subject matter. See `palettes.md` for the full set.

### 3. Dominance over equality
One colour dominates 60-70% of the visual space (usually the background). One or two supporting colours fill 20-30%. One accent colour is used sparingly for emphasis. Never give equal weight to more than two colours.

### 4. Dark/light contrast
Use dark backgrounds for title and closing slides to create visual bookends. The body slides can stay dark (for a bold feel) or shift to a lighter treatment. Either way, maintain strong contrast between text and background.

### 5. Commit to a visual motif
Pick one distinctive element and repeat it across the deck: a rounded rectangle container, a diagonal divider, a colour bar along the left edge. Consistency builds professionalism. Do not mix multiple decorative motifs.

### 6. Vary layouts
Never repeat the same slide type on consecutive slides. Alternate between content, diagram, metrics, and two-column types to maintain visual rhythm. If you must place two content slides back to back, vary the number of bullets or add an image to one.

### 7. Left-align body text
Body text and bullets are always left-aligned. Centre alignment is reserved for titles, section headers, and metric values only. Mixed alignment within a single text block is never acceptable.

### 8. Size contrast
Create hierarchy through size differences. Titles at 36-44pt should be noticeably larger than body text at 14-16pt. Metric values at 60-72pt should dominate their slides. Subtle size differences (e.g. 16pt vs 18pt) create visual confusion rather than hierarchy.

### 9. No accent lines under titles
Horizontal lines or bars placed directly under slide titles are a hallmark of AI-generated presentations. Do not add them. Let whitespace and font weight create the separation between title and body content.

### 10. Breathing room
White space is not wasted space. Maintain minimum margins and spacing to prevent the deck from feeling cramped.

---

## Typography

| Element | Font | Size | Weight | Notes |
|---------|------|------|--------|-------|
| Slide title | Georgia | 36-44pt | Bold | Palette fg colour |
| Section header | Georgia | 20-24pt | Bold | Palette fg colour, centre-aligned |
| Body text | Calibri | 14-16pt | Regular | Palette fg colour, left-aligned |
| Captions | Calibri | 10-12pt | Italic | Palette muted colour |
| Metric values | Georgia | 60-72pt | Bold | Palette accent colour, centre-aligned |
| Metric labels | Calibri | 14pt | Regular | Palette muted colour, centre-aligned |

---

## Layout Constraints

| Constraint | Value |
|------------|-------|
| Slide dimensions | 10" x 7.5" (standard widescreen) |
| Minimum margins (all sides) | 0.5" |
| Gap between content blocks | 0.3-0.5" |
| Image max width (centred) | 8.5" |
| Image max width (full-bleed) | 9.5" (or 10" for `diagram_full`) |
| Max bullets per slide | 5 |
| Max lines per bullet | 2 |
| Title max words | 8 |

---

## Rich visual placeholder protocol

When a slide's template mandates a visual element but no real image, diagram,
or chart is available from the source material, emit a **placeholder directive**
on the slide and collect the full description in an **appendix table** after
the last numbered slide. This keeps slides clean while preserving enough detail
for a human to create the visual later (e.g., using the excalidraw-diagram skill).

### On-slide format

```markdown
![bg right:40%](placeholder://visual-needed)

*[See Appendix: P1 — Architecture diagram]*
```

The slide keeps the Marp image directive (reserves layout space) and a short
back-reference to the appendix row. No blockquote, no full description on the slide.

### Appendix section

After the last numbered slide (e.g. after Q&A), emit the appendix:

```markdown
---

<!-- _class: lead -->

# Appendix — Visual Placeholders

---

<style scoped>
table { font-size: 0.65em; }
</style>

| Ref | Slide | Description | Tool |
|-----|-------|-------------|------|
| P1 | 4 | **Architecture diagram** — Left-to-right flow: Skill box, CLI box, tools/ box, Data sources box. Hand-drawn whiteboard style, dark tech theme. | excalidraw-diagram |
| P2 | 8 | **WhatsApp briefing screenshot** — Mobile phone frame, chat bubble, formatted brief. Dark tech theme. | excalidraw-diagram |
```

If more than 6 placeholders, split across multiple table slides (one `---` separator per 6 rows).

### Rules

1. The `![...]` directive is REAL Marp syntax — it renders as a broken-image
   icon in preview but keeps the slide layout correct (the split-image region
   is reserved, not collapsed).
2. The `placeholder://` URL scheme signals "not a real file" to both humans
   and the visual gate. The gate counts `placeholder://` refs as images for
   the image-density floor but flags them in a `placeholders_remaining` count.
3. The appendix table carries the full description: Subject, Composition,
   Key elements, Style, Purpose, and Suggested tool — collapsed into the
   Description column. The on-slide text is only `*[See Appendix: P<n> — <brief subject>]*`.
4. Appendix slides use `<!-- _class: lead -->` for the section header.
   Appendix slides are NOT counted by criterion 8 (constraint compliance)
   for the slide-count limit.
5. Mermaid/chart fences are ALWAYS preferred over placeholders when the
   content is diagrammable. Only use placeholders for photos, screenshots,
   custom illustrations, or complex visuals that need a human artist.
6. When the user later creates an excalidraw image, they replace the
   `placeholder://` URL with the real path AND remove the appendix row.
7. If a slide already has a real mermaid fence or SVG, it does not get a
   placeholder or appendix entry.
