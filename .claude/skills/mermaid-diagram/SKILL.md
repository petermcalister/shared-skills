---
name: mermaid-diagram
description: >
  Create Mermaid diagrams (activity, deployment, sequence, architecture, flowchart, ER, class,
  state, gantt, mindmap) from text descriptions or source code. Use when asked to "create a diagram",
  "generate mermaid", "document architecture", "code to diagram", "visualize workflow",
  "create design doc", "convert code to diagram", or any request involving technical diagrams.
  Supports hierarchical on-demand guide loading, Unicode semantic symbols, and Python utilities
  for diagram extraction, validation, and image conversion.
version: 0.1.0
---

# Mermaid Architect — Hierarchical Diagram Skill

Mermaid diagram system with specialized guides, resilient validation, and code-to-diagram capabilities.

## Decision Tree

1. **User makes a request** → Analyze intent
2. **Determine diagram/document type** → Load appropriate guide(s)
3. **Generate diagram** using guide patterns
4. **Validate via resilient workflow** → NEVER deliver unvalidated diagrams

### Intent Routing

| User says... | Load guide |
|-------------|-----------|
| "workflow", "process", "business logic", "user flow" | `.claude/skills/mermaid-diagram/references/guides/diagrams/activity-diagrams.md` |
| "infrastructure", "deployment", "cloud", "K8s" | `.claude/skills/mermaid-diagram/references/guides/diagrams/deployment-diagrams.md` |
| "system architecture", "components", "microservices" | `.claude/skills/mermaid-diagram/references/guides/diagrams/architecture-diagrams.md` |
| "API flow", "interactions", "sequence" | `.claude/skills/mermaid-diagram/references/guides/diagrams/sequence-diagrams.md` |
| General diagram or unsure | `.claude/skills/mermaid-diagram/references/mermaid-diagram-guide.md` |

For troubleshooting syntax errors, read: `.claude/skills/mermaid-diagram/references/guides/troubleshooting.md`

## Resilient Workflow (MANDATORY)

**NEVER add a diagram to markdown until it passes validation.**

```
1. Identify diagram type → Load appropriate guide
2. Write .mmd file with naming convention
3. Validate via mmdc:
   python .claude/skills/mermaid-diagram/scripts/validate_mermaid.py \
     --code "$(cat diagram.mmd)" --output diagram.png --json
4. IF success → Deliver diagram
   IF error → Read troubleshooting.md → Fix syntax → Retry (max 3 attempts)
```

### Quick Validation Commands

```bash
# Validate a single .mmd file
mmdc -i diagram.mmd -o diagram.png -b transparent

# Extract and validate all diagrams in a markdown file
python .claude/skills/mermaid-diagram/scripts/extract_mermaid.py doc.md --validate

# Batch convert all .mmd files to PNG
python .claude/skills/mermaid-diagram/scripts/mermaid_to_image.py diagrams/ output/ --format png
```

### File Naming Convention

```
./diagrams/<context>_<num>_<type>_<title>.mmd
./diagrams/<context>_<num>_<type>_<title>.png
```

Example: `./diagrams/api_design_01_sequence_auth_flow.mmd`

## High-Contrast Styling (Required)

Always add high-contrast classDef styles for accessibility:

```mermaid
%% High-contrast styles
classDef default fill:#E8F4FD,stroke:#1B4F72,stroke-width:2px,color:#1B4F72
classDef highlight fill:#D4EFDF,stroke:#1E8449,stroke-width:2px,color:#1E8449
classDef warning fill:#FDEBD0,stroke:#B9770E,stroke-width:2px,color:#B9770E
classDef error fill:#FADBD8,stroke:#C0392B,stroke-width:2px,color:#C0392B
classDef info fill:#D6EAF8,stroke:#2471A3,stroke-width:2px,color:#2471A3
```

## Unicode Semantic Symbols (Quick Reference)

Enhance diagram clarity with Unicode symbols:

| Category | Symbols |
|----------|---------|
| Infrastructure | ☁️ 🌐 🔌 📡 🗄️ |
| Compute | ⚙️ ⚡ 🔄 ♻️ 🚀 |
| Data | 💾 📦 📊 📈 🗃️ |
| Security | 🔐 🔑 🛡️ 🚪 👤 |
| Monitoring | 📝 📊 🚨 ⚠️ ✅ ❌ |

Full reference: `.claude/skills/mermaid-diagram/references/guides/unicode-symbols/guide.md`

## Python Utilities

| Script | Purpose |
|--------|---------|
| `scripts/extract_mermaid.py` | Extract diagrams from markdown, validate, replace with images |
| `scripts/mermaid_to_image.py` | Convert .mmd to PNG/SVG with themes and batch support |
| `scripts/validate_mermaid.py` | Resilient workflow: validate, render, error recovery |

## Best Practices

1. **Wrap labels in quotes** when they contain special characters or reserved words
2. **Use `flowchart` not `graph`** for modern Mermaid syntax
3. **Avoid reserved word `end`** as a node name — use `"end"` instead
4. **Add `classDef` styles** for every diagram (accessibility)
5. **Validate before delivering** — always run mmdc
6. **Use subgraphs** to group related nodes in complex diagrams
7. **Keep diagrams focused** — split large diagrams into multiple smaller ones
