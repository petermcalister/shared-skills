# Mermaid Diagram Picker

Situation → diagram-type mapping. When a slide needs a diagram, pick the row whose *Situation* best matches what you're trying to say, then paste the minimal example into a `` ```mermaid `` fence. The F007/F008 pre-render engines will convert it to SVG at delivery time.

Mermaid docs: https://mermaid.js.org/intro/

---

| # | Situation | Diagram type | Minimal example | When to pick this over alternatives |
|---|---|---|---|---|
| 1 | Show a linear pipeline with a decision point | `flowchart LR` | `flowchart LR`<br>`  A[Ingest] --> B{Valid?}`<br>`  B -->|yes| C[Store]`<br>`  B -->|no| D[Reject]` | Pick over `sequenceDiagram` when the focus is on *data flow through stages*, not who-talks-to-whom over time |
| 2 | Show who calls who in an API interaction | `sequenceDiagram` | `sequenceDiagram`<br>`  Client->>API: POST /order`<br>`  API->>DB: INSERT`<br>`  DB-->>API: ok`<br>`  API-->>Client: 201` | Pick over `flowchart` when the audience needs to see request/response timing and actor boundaries |
| 3 | Explain database relationships | `erDiagram` | `erDiagram`<br>`  USER ||--o{ ORDER : places`<br>`  ORDER ||--|{ ITEM : contains` | Pick over `classDiagram` when the focus is data cardinality, not object-oriented inheritance |
| 4 | Show a chronological project history | `timeline` | `timeline`<br>`  title Project`<br>`  2024 : Idea`<br>`  2025 : Build`<br>`  2026 : Ship` | Pick over `gantt` when the audience only needs *ordering*, not overlapping durations or dependencies |
| 5 | Position options on a 2×2 framework | `quadrantChart` | `quadrantChart`<br>`  title Effort vs Impact`<br>`  x-axis Low --> High`<br>`  y-axis Low --> High`<br>`  "Fix typos": [0.1, 0.1]`<br>`  "Rewrite core": [0.9, 0.8]` | Pick over `flowchart` when the framing *is* the message (McKinsey-style prioritisation) |
| 6 | Show system context at C4 level 1 | `C4Context` | `C4Context`<br>`  Person(user, "User")`<br>`  System(app, "App")`<br>`  Rel(user, app, "uses")` | Pick over `architecture-beta` when the audience wants formal C4 notation and the slide is about external actors, not internal services |
| 7 | Show internal service topology | `architecture-beta` | `architecture-beta`<br>`  group api(cloud)[API]`<br>`  service db(database)[DB] in api`<br>`  service web(server)[Web] in api`<br>`  web:R --> L:db` | Pick over `C4Context` when the audience is engineering and the slide is about cloud/service layout, not user interactions |
| 8 | Show a state machine (order lifecycle) | `stateDiagram-v2` | `stateDiagram-v2`<br>`  [*] --> Pending`<br>`  Pending --> Paid`<br>`  Paid --> Shipped`<br>`  Shipped --> [*]` | Pick over `flowchart` when the same entity moves through named states — the diagram reads as "what can happen next" |
| 9 | Compare sequential phases with parallel swimlanes | `gantt` | `gantt`<br>`  title Migration`<br>`  section Discovery`<br>`  Audit :a1, 2026-01-01, 14d`<br>`  section Build`<br>`  Refactor :after a1, 30d` | Pick over `timeline` when you need to show overlapping work or dependencies between tracks |
| 10 | Explain a hierarchy or org tree | `flowchart TB` | `flowchart TB`<br>`  CEO --> CTO`<br>`  CEO --> CFO`<br>`  CTO --> EngA`<br>`  CTO --> EngB` | Pick over `classDiagram` when the relationship is pure containment/reporting, not OO composition |
| 11 | Visualise an issue tree for root-cause analysis | `flowchart TB` | `flowchart TB`<br>`  Problem --> Cause1[Infra cost]`<br>`  Problem --> Cause2[Team velocity]`<br>`  Cause1 --> Fix1[Rightsize VMs]`<br>`  Cause2 --> Fix2[Pair rotation]` | The Option 3 "Internal Problem-Solving" framework pairs naturally with this shape |
| 12 | Mind-map of a brainstorm | `mindmap` | `mindmap`<br>`  root((Launch))`<br>`    Marketing`<br>`      Blog`<br>`      Demos`<br>`    Engineering`<br>`      API`<br>`      UI` | Pick over `flowchart` when the output of a Q3 key-points question is genuinely non-linear and radial framing helps |

---

## Pre-render contract

When a fence like `` ```mermaid `` appears in the generated Marp markdown, the `story-present-prerender-mermaid` CLI (F009) rewrites it to:

```markdown
![w:900 contain](out/mmdc/assets/<sha1>.svg)
```

This means hand-authored fences and engine-rewritten fences render identically via the recipe 7 directive in `marp-image-cookbook.md`. The engine choice (mmdc) is set at delivery time via the prompt documented in `SKILL.md` §Delivery. The interactive HTML renderer uses client-side mermaid instead of pre-rendering.

## Further reading

- Mermaid documentation: https://mermaid.js.org/intro/
- C4 model: https://c4model.com/
