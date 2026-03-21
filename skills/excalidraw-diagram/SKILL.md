---
name: excalidraw-diagram
description: >
  Create Excalidraw diagram JSON files that make visual arguments. Use when the user wants to
  visualize workflows, architectures, concepts, system designs, data flows, or any request
  involving diagrams, visual explanations, or technical illustrations. Generates .excalidraw
  files with mandatory Playwright-based visual validation.
version: 0.1.0
---

# Excalidraw Diagram Creator

Generate `.excalidraw` JSON files that **argue visually**, not just display information.

## Customization

**All colors live in one file:** read `${CLAUDE_PLUGIN_ROOT}/skills/excalidraw-diagram/references/color-palette.md` before generating any diagram. It is the single source of truth for all color choices.

---

## Core Philosophy

**Diagrams should ARGUE, not DISPLAY.**

A diagram isn't formatted text. It's a visual argument that shows relationships, causality, and flow that words alone can't express. The shape should BE the meaning.

**The Isomorphism Test**: If you removed all text, would the structure alone communicate the concept? If not, redesign.

**The Education Test**: Could someone learn something concrete from this diagram? A good diagram teaches — it shows actual formats, real event names, concrete examples.

---

## Depth Assessment (Do This First)

### Simple/Conceptual Diagrams
Use abstract shapes when explaining a mental model, the audience doesn't need specifics, or the concept IS the abstraction.

### Comprehensive/Technical Diagrams
Use concrete examples when diagramming a real system, the diagram will teach/explain, or you're showing how technologies integrate. **Include evidence artifacts** (code snippets, JSON examples, real API names).

---

## Design Process (Do This BEFORE Generating JSON)

### Step 0: Assess Depth
Simple/Conceptual vs Comprehensive/Technical. If comprehensive: research actual specs first.

### Step 1: Understand Deeply
For each concept: What does it DO? What relationships exist? What's the core flow?

### Step 2: Map Concepts to Patterns

| If the concept... | Use this pattern |
|-------------------|------------------|
| Spawns multiple outputs | **Fan-out** (radial arrows) |
| Combines inputs into one | **Convergence** (arrows merging) |
| Has hierarchy/nesting | **Tree** (lines + text) |
| Is a sequence of steps | **Timeline** (line + dots + labels) |
| Loops or improves | **Spiral/Cycle** (arrow returning) |
| Is abstract state | **Cloud** (overlapping ellipses) |
| Transforms input→output | **Assembly line** (before→process→after) |
| Compares two things | **Side-by-side** (parallel) |
| Separates into phases | **Gap/Break** (visual separation) |

### Step 3: Ensure Variety
Each major concept must use a **different** visual pattern. No uniform cards or grids.

### Step 4: Sketch the Flow
Mentally trace how the eye moves through the diagram. Clear visual story.

### Step 5: Generate JSON
See element templates: `${CLAUDE_PLUGIN_ROOT}/skills/excalidraw-diagram/references/element-templates.md`

### Step 6: Render & Validate (MANDATORY)
See Render & Validate section below.

---

## Large Diagram Strategy

**Build JSON one section at a time.** Do NOT generate entire file in one pass.

### Section-by-Section Workflow

**Phase 1: Build sections**
1. Create base file with JSON wrapper + first section
2. Add one section per edit — take time with layout and spacing
3. Use descriptive string IDs (e.g., `"trigger_rect"`, `"arrow_fan_left"`)
4. Namespace seeds by section (section 1: 100xxx, section 2: 200xxx)
5. Update cross-section bindings as you go

**Phase 2: Review whole**
Check: cross-section arrows bound correctly? Spacing balanced? All IDs reference existing elements?

**Phase 3: Render & validate**
Run the render-view-fix loop.

---

## Container vs Free-Floating Text

Default to **free-floating text**. Add containers only when they serve a purpose.

| Use Container When... | Use Free-Floating When... |
|----------------------|--------------------------|
| Focal point of section | Label or description |
| Needs visual grouping | Supporting detail |
| Arrows connect to it | Describes something nearby |
| Shape carries meaning | Section title or annotation |

**Rule**: <30% of text elements should be inside containers.

---

## Shape Meaning

| Concept Type | Shape |
|--------------|-------|
| Labels, descriptions | **none** (free-floating text) |
| Timeline markers | small `ellipse` (10-20px) |
| Start, trigger, input | `ellipse` |
| End, output, result | `ellipse` |
| Decision, condition | `diamond` |
| Process, action | `rectangle` |
| Abstract state | overlapping `ellipse` |
| Hierarchy | lines + text (no boxes) |

---

## Layout Principles

- **Hero**: 300×150 — visual anchor
- **Primary**: 180×90
- **Secondary**: 120×60
- **Whitespace = Importance**: Most important element has most space around it (200px+)
- **Flow**: Left→right or top→bottom for sequences, radial for hub-and-spoke
- **Connections**: If A relates to B, there MUST be an arrow

---

## Modern Aesthetics

- `roughness: 0` — Clean edges (default for professional diagrams)
- `strokeWidth: 2` — Standard for shapes and arrows
- `opacity: 100` — Always. Use color/size for hierarchy, not transparency.
- Small marker dots (10-20px ellipses) instead of full shapes for timeline points

---

## Text Rules

**CRITICAL**: The `text` property contains ONLY readable words.

```json
{ "text": "Start", "originalText": "Start" }
```

Settings: `fontSize: 16`, `fontFamily: 3`, `textAlign: "center"`, `verticalAlign: "middle"`

---

## JSON Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": { "viewBackgroundColor": "#ffffff", "gridSize": 20 },
  "files": {}
}
```

---

## Render & Validate (MANDATORY)

You cannot judge a diagram from JSON alone. After generating, you MUST render and visually validate.

### How to Render

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/excalidraw-diagram/references && uv run python render_excalidraw.py <path-to-file.excalidraw>
```

Outputs PNG next to the `.excalidraw` file. View it with the Read tool.

### The Loop

1. **Render & View** — Run script, Read the PNG
2. **Audit vision** — Does structure match your plan? Correct hierarchy? Evidence artifacts readable?
3. **Check defects:**
   - Text clipped or overflowing container
   - Elements overlapping
   - Arrows crossing through elements
   - Arrows pointing to wrong element or empty space
   - Uneven spacing
   - Text too small to read
   - Composition lopsided
4. **Fix** — Edit JSON (widen containers, adjust x/y, add arrow waypoints)
5. **Re-render** — Repeat until clean (typically 2-4 iterations)

### When to Stop

- Diagram matches conceptual design
- No text clipped, overlapping, or unreadable
- Arrows route cleanly
- Spacing consistent, composition balanced

### First-Time Setup

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/excalidraw-diagram/references
uv sync
uv run playwright install chromium
```

---

## Quality Checklist

### Depth & Evidence
1. Research done (for technical diagrams)?
2. Evidence artifacts included?
3. Multi-zoom (summary + sections + detail)?
4. Real content, not just labeled boxes?
5. Educational value?

### Conceptual
6. Isomorphism — structure mirrors concept behavior?
7. Argument — shows something text alone couldn't?
8. Variety — different pattern per concept?
9. No uniform card grids?

### Container Discipline
10. Minimal containers — could any work as free text?
11. Lines as structure for trees/timelines?
12. Typography hierarchy via font size and color?

### Structural
13. Every relationship has an arrow or line?
14. Clear visual flow path?
15. Important elements larger/more isolated?

### Technical
16. `text` contains only readable words?
17. `fontFamily: 3`?
18. `roughness: 0` (unless hand-drawn requested)?
19. `opacity: 100` for all elements?
20. <30% text in containers?

### Visual Validation
21. Rendered to PNG and inspected?
22. No text overflow?
23. No overlapping elements?
24. Even spacing?
25. Arrows land correctly?
26. Readable at export size?
27. Balanced composition?
