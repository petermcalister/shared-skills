# Template — Option 8: Design Document / RFC

Loaded by SKILL.md when the routing matrix picks Option 8. Defines the section sequence for a flowing technical design document intended for peer review. This is NOT a slide deck — sections are logical divisions, not per-slide breaks.

**Source**: Adapted from Google-style design doc structure (the standalone design-doc skill's Phase 3), integrated into story-present's gated pipeline for scoring, rendering, and delivery.

**Arc pattern**: Problem → Goals → Design → Alternatives → Risks → Implementation → Appendix.

---

## Structural rules (apply to every section)

1. **Section headings, not slide titles.** Headings are descriptive and informative. Use `##` for top-level sections, `###` for subsections. No action titles — this is a document, not a consulting deck.
2. **Technical depth is mandatory.** Every section should contain enough detail for a reviewer to spot problems. Vague descriptions are a scoring-rubric penalty (criterion 6b). Include:
   - Architecture / component breakdowns with mermaid diagrams
   - Data model changes with field-level detail
   - Interface contracts (API signatures, message schemas)
   - Sequence of operations for critical paths
   - Configuration examples, code snippets, CLI invocations
3. **Evidence from source material.** Cite ingested sources (emails, memory, git, reports) with `Source:` markers. Unsourced claims in a design doc invited to peer review will be challenged.
4. **Diagrams over prose for architecture.** Use mermaid fences (not placeholders) for data flows, component topology, sequence diagrams, dependency graphs, and implementation timelines. Reserve placeholders only for photos, screenshots, custom illustrations.
5. **`---` separators between top-level sections.** These maintain Marp compatibility (each section renders as a "slide" in html/pptx if the user requests those formats) while flowing naturally in docx.
6. **Marp frontmatter for pipeline compatibility.** Include standard frontmatter so pre-render and render steps work unchanged:
   ```yaml
   ---
   marp: true
   theme: tech
   paginate: true
   ---
   ```

---

## Section sequence

| # | Section | Heading | Content structure |
|---|---------|---------|-------------------|
| 1 | Title block | `# <Title>: Design Doc` | Author, status (Draft), date, reviewers (or TBD). One-line subtitle describing the proposal in plain language. |
| 2 | TL;DR | `## TL;DR` | 3–5 sentences: what is being proposed, why, and what the key tradeoff is. A reviewer who reads only this should understand the ask. |
| 3 | Context and Problem Statement | `## Context and Problem Statement` | What's the problem? Why now? 2–3 paragraphs of background. Link to prior work, tickets, incidents. A mermaid diagram showing the current state is strongly recommended. |
| 4 | Goals and Non-Goals | `## Goals and Non-Goals` | Bulleted goals (measurable where possible) and explicit non-goals with rationale. Non-goals prevent scope-creep objections during review. |
| 5 | Proposed Design | `## Proposed Design` | The core. Architecture, component breakdown, data model, key interfaces, critical-path sequence. Use subsections (`###`) for each major component. **MUST** contain at least one mermaid diagram (architecture, sequence, or ER). Include code snippets for key interfaces. |
| 6 | Alternatives Considered | `## Alternatives Considered` | For each alternative: what it is, why it was rejected (specific tradeoff), and what would change your mind. Thin alternatives are a scoring penalty. Minimum two genuine alternatives — not strawmen. |
| 7 | Risks and Open Questions | `## Risks and Open Questions` | **Risks**: known risks with proposed mitigations (table format recommended). **Open Questions**: decisions needing reviewer input, with owner/deadline hints where known. |
| 8 | Implementation Plan | `## Implementation Plan` | High-level phasing: what ships first, dependencies, parallelisation. A mermaid gantt or flowchart is recommended for multi-phase plans. |
| 9 | Appendix (optional) | `## Appendix` | Supporting detail that would interrupt the main flow: full API schemas, migration scripts, benchmark data, visual placeholders for future diagrams. |

---

## Section depth calibration

Adapt section depth to proposal complexity. The minimum viable design doc has all nine sections present (even if some are one line). The scaling guidance:

| Proposal complexity | Total length | Proposed Design depth | Alternatives depth |
|--------------------|--------------|-----------------------|-------------------|
| Small (config change, flag flip) | 500–1000 words | 1–2 paragraphs + 1 diagram | 1–2 alternatives, 1 paragraph each |
| Medium (new component, API change) | 1500–3000 words | 3–5 subsections + 2–3 diagrams + code | 2–3 alternatives with tradeoff tables |
| Large (system redesign, migration) | 3000–5000 words | Multiple subsections + diagrams + sequence + data model | 3+ alternatives with decision matrix |

---

## Diagram guidance

| Section | Diagram type | When to include |
|---------|-------------|----------------|
| Context (§3) | flowchart or C4 context | Always — shows the current state the proposal changes |
| Proposed Design (§5) | architecture (flowchart, C4 container, or architecture-beta) | Always — the primary visual artifact |
| Proposed Design (§5) | sequence diagram | When the critical path involves multiple services or async steps |
| Proposed Design (§5) | ER diagram | When data model changes are part of the proposal |
| Alternatives (§6) | quadrant chart or comparison table | When alternatives differ on 2+ measurable axes |
| Implementation (§8) | gantt or flowchart | When implementation has 2+ phases with dependencies |

Use `references/generation/mermaid-diagram-picker.md` for situation → type mapping. Emit real mermaid fences — placeholders are a last resort.

---

## Scoring rubric adaptation for Option 8

The 9-criterion rubric from `references/generation/scoring-rubric.md` applies with these adjustments:

| Criterion | Slide-deck interpretation | Design-doc interpretation |
|-----------|--------------------------|--------------------------|
| 1. Structural compliance | Matches template slide sequence | All 9 sections present and correctly ordered |
| 2. Action titles | Action titles on every slide | Descriptive section headings (action titles are wrong here) |
| 3. One message per slide | One idea per slide | One theme per section (no section covers two unrelated topics) |
| 6b. Technical depth | Conditional on audience | **Always scored** — technical depth is mandatory for design docs |
| 9. Marp syntax | Slide separators, directives | Section separators (`---`), frontmatter, mermaid fences valid |
| 10. Visual variety | Images ≥ ceil(slides/3) | Diagrams ≥ 2, at least 1 distinct mermaid type |

---

## Format delivery defaults

When the delivery prompt asks for formats, the default for Option 8 is:

```
Recommended: docx (primary reading format for design review)
Also available: html (Confluence paste), pptx (presentation to review board), interactive
```

If the user selects pptx or interactive, confirm: "Design docs are flowing documents — slide-format output will chunk sections into slides. Proceed?"
