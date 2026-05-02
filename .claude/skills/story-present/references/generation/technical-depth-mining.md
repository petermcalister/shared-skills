# Technical Depth Mining

Prevents shallow decks when the source material is technically rich. Run this procedure between source ingestion and generation whenever the trigger conditions fire.

---

## Trigger Conditions

Both triggers independently activate this procedure. If either fires, run it.

### Audience trigger

Q2 answer contains any of: `engineers`, `developers`, `technical`, `architecture`, `system design`, `infrastructure`.

### Content trigger

Source material (working notes) contains any of: architecture diagrams, test strategies, design patterns, migration paths, performance data, API designs, database schemas, algorithm choices, framework comparisons.

---

## Extraction Procedure

Scan the source material for these five categories, then rank, map to slides, and flag diagrammable content.

### Step 1 -- Categorised scan

| # | Category | What to look for |
|---|----------|-----------------|
| 1 | **Architectural decisions** | "we chose X over Y because Z", layer separation, dependency direction, integration patterns, service boundaries, data flow direction |
| 2 | **Test strategy** | BDD scenarios, test isolation, mock/capture modes, real vs synthetic data, Playwright/pytest/behave patterns, coverage metrics |
| 3 | **Clever patterns** | Three-tier memory, hybrid search (BM25+vector), plan-and-park, semantic layer, rich placeholder protocol, CLI-first architecture |
| 4 | **Innovation showcase** | Things the audience would find surprising or impressive: autonomous orchestrator, WhatsApp command channel, dual-model LLM pipelines, chart pre-rendering, self-scoring rubric |
| 5 | **Quantitative evidence** | Commit counts, test counts, scenario counts, line counts, coverage metrics, performance numbers, cost savings, latency improvements |

### Step 2 -- Rank by showcase value

For each extracted item, assign a showcase rank:

| Rank | Criteria | Example |
|------|----------|---------|
| **High** | Novel architecture, surprising result, clever solution to a hard problem | "Replaced 3 MCP servers with 40 CLI commands" |
| **Medium** | Solid engineering practice done well | "BDD test suite with 51 scenarios across 2 feature files" |
| **Low** | Standard implementation detail | "CRUD endpoints for task management" |

### Step 3 -- Map to slide slots

For each High and Medium item, identify which template slide it maps to. Rules:

- **Dedicate a full slide** to every High item. Do not bury it in a bullet list.
- Medium items can share a slide if they belong to the same category, but prefer one item per slide when slide count allows.
- Low items appear only as supporting detail within an existing slide, never as the lead content.

### Step 4 -- Identify diagrammable content

Flag any item that describes a flow, pipeline, state machine, timeline, hierarchy, or comparison. These become mermaid fences, not bullet points. Use the situation-to-type mapping in `references/generation/mermaid-diagram-picker.md` to pick the right diagram type.

| Content pattern | Suggested mermaid type |
|----------------|----------------------|
| Data flow / pipeline | `flowchart LR` |
| Service topology | `architecture-beta` or `C4Context` |
| State machine / lifecycle | `stateDiagram-v2` |
| Chronological history | `timeline` |
| Hierarchy / org structure | `flowchart TB` |
| API interaction | `sequenceDiagram` |
| Comparison / prioritisation | `quadrantChart` |
| Project phases | `gantt` |

### Step 5 -- Output

Produce a ranked list in the working notes block, tagged by category and showcase value, with suggested slide mapping and diagram type. Format:

```
## Technical depth extraction

- [HIGH | Architectural decisions] CLI-first architecture replaced 3 MCP servers
  Slide: dedicated slide. Diagram: flowchart LR (data flow from command to CLI to service)
- [HIGH | Innovation showcase] Self-scoring rubric with auto-refine loop
  Slide: dedicated slide. Diagram: stateDiagram-v2 (score -> refine -> deliver)
- [MEDIUM | Test strategy] 51 BDD scenarios across 2 feature files
  Slide: evidence slide with metrics callout
- [LOW | Clever patterns] YAML-based semantic layer
  Slide: supporting detail on architecture slide
```

---

## Integration

This procedure feeds into Generation. After running it:

1. The High items become dedicated slides in the outline.
2. The diagrammable items become mermaid fences (not placeholders) per the rule in SKILL.md Generation section.
3. The quantitative evidence feeds criterion 6a (Evidence presence) in the scoring rubric.
4. The depth of coverage feeds criterion 6b (Technical depth) in the scoring rubric.
