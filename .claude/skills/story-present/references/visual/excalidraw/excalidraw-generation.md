# Excalidraw Diagram Generation Guide

Progressive-disclosure process for generating Excalidraw JSON from appendix placeholder descriptions.

## When to generate

After all slides pass visual verification and format rendering is complete, during the delivery phase. Generate one `.excalidraw` file per `excalidraw-diagram` entry in the appendix placeholder table.

## Generation loop

For each `excalidraw-diagram` placeholder in the appendix:

1. **Read the description** from the appendix table entry
2. **Load references** (progressive disclosure -- only now, not during slide writing):
   - `references/visual/excalidraw/color-palette.md` for semantic colors
   - `references/visual/excalidraw/element-templates.md` for copy-paste JSON
   - `references/visual/excalidraw/json-schema.md` for property reference
3. **Plan the layout** -- identify elements, pick a design pattern (see below), sketch approximate x/y positions on paper before writing JSON
4. **Generate JSON in sections** -- shapes first, then text labels bound to shapes, then arrows/connections last (arrows reference shape IDs)
5. **Assemble** into a complete `.excalidraw` file:
   ```json
   {"type": "excalidraw", "version": 2, "elements": [...], "appState": {"viewBackgroundColor": "#ffffff"}}
   ```
6. **Save** to `<topic-folder>/assets/<ref>.excalidraw`
7. **Render** via `story-present-render-excalidraw --input <path> --output <path>.png`
8. **Read the PNG** with the Read tool for visual verification
9. **Quality check** -- no text overflow, no overlapping elements, arrows land on targets, readable at slide size (1280x720)
10. **Fix if needed** -- if quality fails, edit JSON and re-render (max 2 iterations per image)

## Design patterns

| Pattern | Shape | When to use |
|---------|-------|-------------|
| Fan-out | Central node with radial spokes | One concept splits into many (capabilities, features) |
| Convergence | Multiple inputs into single output | Many-to-one flows (data aggregation, decision funnels) |
| Tree | Top-down or left-right hierarchy | Org charts, taxonomy, decomposition |
| Timeline | Horizontal sequence with markers | Phases, milestones, historical progression |
| Side-by-side | Two parallel groups | Before/after, comparison, option A vs B |
| Assembly line | Linear pipeline with stages | Data pipelines, CI/CD, processing chains |

## JSON assembly rules

- Start first element at `y: 100`, leave **120px vertical gaps** between rows
- Leave **200px horizontal gaps** between columns
- Use **descriptive IDs** (`auth_rect`, `db_arrow`, not `elem1`, `arrow2`)
- Always set `roughness: 0`, `opacity: 100`, `fontFamily: 3`
- Rectangle width: 160-220px. Height: 70-100px
- Font sizes: 20px for titles, 16px for shape labels, 14px for annotations
- Arrow `points` are relative to the arrow's `x,y` origin
- Every shape with interior text needs `boundElements: [{"id": "<text_id>", "type": "text"}]`
- Every interior text needs `containerId: "<shape_id>"`

## User approval

After all excalidraw images are generated and visually verified, present a summary table:

| # | Placeholder ref | Description | Status |
|---|----------------|-------------|--------|
| 1 | `arch-overview` | System architecture showing 3 services | Verified |
| 2 | `data-flow` | ETL pipeline from source to warehouse | Verified |

Wait for user approval before replacing `placeholder://visual-needed` URLs with actual image paths and removing replaced appendix entries.
