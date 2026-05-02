# Executive HTML — Content-to-Component Mapping

> Heuristic guide for E2 scoring. The agent selects obsidian components based
> on content patterns in the structured markdown. This is a guide, not a rigid rule.

## Mapping Table

| Content pattern | Obsidian component | When to use |
|---|---|---|
| `# Title` + first paragraph | Hero with gradient-text | Always — page opener |
| `## Section heading` | Section with `.section-label` | Every top-level section |
| Table with RAG emoji (🟢🟡🔴) | Data table with colored status pills | RAID, steering, status |
| Standalone numbers + labels | Metric / KPI cards | Executive summary, snapshot |
| `> blockquote` with attribution | Quote box (Playfair italic) | Key quotes, thesis statements |
| ` ```mermaid ` fence | Card-wrapped rendered diagram | Architecture, flows, timelines |
| ` ```python/yaml/json ` fence | Code card with syntax highlighting | Design docs, cheatsheets |
| Bullet list (3–6 items with bold headings) | Tile grid (3-col) | Principles, capabilities, recommendations |
| Sequential items with dates | Timeline layout | Milestones, implementation phases |
| Emphasis paragraph or `[!callout]` | Gradient callout card | Decision required, key insight |

## Notes

- The agent uses judgment — same approach as standalone obsidian runs
- Multiple components can be nested within a section
- Prefer variety — no 3+ identical consecutive components (scored in E4)
- When content doesn't clearly match a pattern, default to card with body text
- Tables with 3+ columns → data table component; 2-column key/value → tile grid or metric cards
