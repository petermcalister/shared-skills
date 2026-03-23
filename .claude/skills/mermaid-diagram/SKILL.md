---
name: mermaid-diagram
description: >
  Use this skill ANY time the user wants a diagram, chart, or visual documentation of any kind —
  flowcharts, sequence diagrams, architecture diagrams, ER diagrams, state machines, gantt charts,
  class diagrams, deployment diagrams, mindmaps, or any visual representation of systems, processes,
  or relationships. Trigger on: "diagram", "chart", "visualize", "draw", "map out", "document the
  flow", "show how X connects to Y", or when the user describes states, transitions, timelines, or
  service interactions that imply a visual even without saying "diagram". Also trigger when the user
  mentions "mermaid" by name or asks to convert code to a diagram.
version: 0.2.0
---

# Mermaid Diagram Skill

Generate validated Mermaid diagrams from text descriptions or source code.

## How This Skill Works

1. **Determine diagram type** from the user's request
2. **Load the relevant guide** for that type (only what's needed — saves context)
3. **Generate the .mmd file**
4. **Validate via mmdc** — diagrams with syntax errors are useless to the user
5. **Deliver** the validated .mmd and rendered PNG/SVG

## Intent Routing

Read only the guide you need for this request:

| User's intent | Guide to read |
|---------------|---------------|
| Workflow, process, business logic | `references/guides/diagrams/activity-diagrams.md` |
| Infrastructure, deployment, cloud, K8s | `references/guides/diagrams/deployment-diagrams.md` |
| System architecture, components, microservices | `references/guides/diagrams/architecture-diagrams.md` |
| API flow, service interactions, sequence | `references/guides/diagrams/sequence-diagrams.md` |
| General or unsure which type | `references/mermaid-diagram-guide.md` |

All paths are relative to this skill's directory.

## Validation Workflow

Unvalidated Mermaid diagrams frequently contain syntax errors — broken arrows, reserved word collisions, unescaped characters — that make them useless. Always validate before delivering.

```bash
# Option 1: Use the resilient workflow script
python scripts/validate_mermaid.py --code "$(cat diagram.mmd)" --output diagram.png --json

# Option 2: Direct mmdc validation
mmdc -i diagram.mmd -o diagram.png -b transparent
```

If validation fails, read `references/guides/troubleshooting.md` — it catalogs 28 common errors with fixes. Apply the fix and retry (up to 3 attempts).

## Workspace

Save all intermediate and output artifacts to the skill's workspace directory:

```
.claude/skills/mermaid-diagram/workspace/
```

Use this for `.mmd` source files, rendered `.png`/`.svg` outputs, and validation results. Copy final deliverables to the user's requested location.

## File Naming

```
workspace/<context>_<num>_<type>_<title>.mmd
```

Example: `workspace/api_design_01_sequence_auth_flow.mmd`

## Styling

Apply high-contrast styles for accessibility. Read `references/mermaid-diagram-guide.md` for the classDef templates.

## Unicode Symbols

Enhance clarity with semantic symbols (e.g., `🔐 Auth`, `💾 Database`, `📨 Queue`). Full catalog: `references/guides/unicode-symbols/guide.md`

## Scripts

| Script | When to use |
|--------|-------------|
| `scripts/validate_mermaid.py` | Validate + render with error recovery (`--json` for structured output) |
| `scripts/extract_mermaid.py` | Extract diagrams from existing markdown (`--validate`, `--list-only`) |
| `scripts/mermaid_to_image.py` | Batch render .mmd files to PNG/SVG (`--theme`, `--format`) |

## Quick Tips

- Use `flowchart` not `graph` (modern syntax)
- Wrap labels containing special characters or reserved words in quotes
- The word `end` is reserved — use `"end"` in labels
- Use subgraphs to group related nodes in complex diagrams
- Split very large diagrams into multiple focused diagrams
