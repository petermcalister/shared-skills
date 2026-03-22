# Addendum: Template Catalogue & Writing Style Guide

This addendum extends the `pptx-report-skill-handoff.md` with two missing layers:
1. A **template catalogue** with 12 presentation archetypes and source references
2. A **technical writing style guide** for slide prose quality, with community skill references

Both should be implemented as `references/` files within the skill and integrated into the SKILL.md workflow.

---

## Part 1: Template Catalogue (`references/template-catalogue.md`)

### Purpose

The skill's workflow should begin with an **interview step** that asks the user about their report's purpose, audience, and content mix, then recommends one of 12 presentation archetypes. Each archetype defines a default slide sequence, palette, and layout style.

### Implementation

The interview should be a simple set of questions:

1. **What is the purpose?** (inform, persuade, review, educate, propose)
2. **Who is the audience?** (technical peers, leadership/execs, mixed, external stakeholders)
3. **What is the content mix?** (mostly diagrams, mostly data/metrics, mostly narrative, balanced)
4. **How many slides?** (short 5-8, medium 10-15, long 15+)

Based on answers, recommend 1-2 archetypes from the catalogue below.

---

### The 12 Presentation Archetypes

#### 1. Executive Summary

- **When to use**: Presenting findings to leadership or non-technical stakeholders who need the headline first
- **Default slides**: Title → Key Takeaway → 3-4 Metrics → Recommendation → Next Steps
- **Palette**: Midnight (dark, authoritative)
- **Layout style**: Large stat callouts, minimal text, one diagram max
- **Slide count**: 5-8
- **Template sources**:
  - SlideModel dark executive templates: https://slidemodel.com/templates/tag/dark/
  - GongRzhe MCP Server built-in `title_slide` + `key_metrics_dashboard` templates: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server (see `slide_layout_templates.json`)
  - PresentationGO executive summary graphics: https://www.presentationgo.com/

#### 2. Technical Deep-Dive

- **When to use**: Presenting architecture, system design, or implementation detail to technical peers
- **Default slides**: Title → Context/Problem → Architecture Diagram (full-bleed) → Component Detail × 3-5 → Trade-offs → Summary
- **Palette**: Ocean (deep blue, technical feel)
- **Layout style**: Diagram-heavy, two-column layouts for component details, minimal bullets
- **Slide count**: 10-15
- **Template sources**:
  - Anthropic's official PPTX skill design ideas (layout patterns, typography): https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md
  - tfriedel/claude-office-skills PPTX workflows: https://github.com/tfriedel/claude-office-skills
  - EasyPPTX grid layouts for component diagrams: https://pypi.org/project/EasyPPTX/
  - tomleelong/PPTX Python toolkit with JSON outlines: https://github.com/tomleelong/PPTX

#### 3. Architecture Review

- **When to use**: Reviewing system architecture with a team, often with multiple Excalidraw diagrams
- **Default slides**: Title → Current State Diagram → Problem Areas → Target State Diagram → Migration Path → Risks → Timeline
- **Palette**: Charcoal (neutral, lets diagrams be the focus)
- **Layout style**: Alternating full-bleed diagrams and commentary slides, before/after comparisons
- **Slide count**: 8-12
- **Template sources**:
  - GongRzhe `before_after_comparison` + `full_image_slide` templates: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server
  - coleam00/excalidraw-diagram-skill for generating the diagrams themselves: https://github.com/coleam00/excalidraw-diagram-skill
  - Ichigo3766/powerpoint-mcp `add-slide-picture-with-caption` pattern: https://github.com/Ichigo3766/powerpoint-mcp

#### 4. Data Analysis Dashboard

- **When to use**: Presenting cost analysis, metrics, trends — Pete's primary use case for database spend reporting
- **Default slides**: Title → KPI Overview (metrics grid) → Trend Chart → Breakdown by Category → Comparison Table → Outliers → Recommendations
- **Palette**: Midnight (matches Pete's existing dashboard theme from `assets/style.css`)
- **Layout style**: Large numbers (60-72pt), metric cards, tables, chart images
- **Slide count**: 8-12
- **Template sources**:
  - GongRzhe `key_metrics_dashboard` + `data_visualization` templates: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server
  - Anthropic PPTX skill "Large stat callouts" pattern: https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md
  - SlidesCarnival dark data templates: https://www.slidescarnival.com/tag/dark
  - python-pptx table examples: https://pbpython.com/creating-powerpoint.html

#### 5. Project Status Update

- **When to use**: Sprint reviews, weekly/monthly status, progress tracking
- **Default slides**: Title → Achievements This Period → Metrics vs Target → Risks & Blockers → Plan for Next Period → Dependencies
- **Palette**: Sage Calm or Teal Trust
- **Layout style**: Traffic-light status indicators, progress bars, timeline graphics
- **Slide count**: 5-8
- **Template sources**:
  - GongRzhe `timeline_slide` + `process_flow` templates: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server
  - SlideModel project status templates: https://slidemodel.com/templates/tag/dark/
  - PresentationGO timeline and Gantt infographics: https://www.presentationgo.com/

#### 6. Proposal / Business Case

- **When to use**: Proposing a new initiative, migration, or investment to decision-makers
- **Default slides**: Title → Problem Statement → Proposed Solution → Architecture (diagram) → Cost-Benefit → Timeline → Risk Mitigation → Ask/Decision Required
- **Palette**: Berry & Cream (distinctive, persuasive)
- **Layout style**: Two-column pros/cons, cost tables, single persuasive diagram
- **Slide count**: 10-15
- **Template sources**:
  - GongRzhe `two_column_text` + `comparison_slide` templates: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server
  - Envato Elements dark pitch deck templates (premium): https://elements.envato.com/presentation-templates/dark/compatible-with-powerpoint
  - SlideNest dark business templates (free): https://slidenest.com/dark

#### 7. Incident / Post-Mortem

- **When to use**: Reviewing a production incident, outage, or security event
- **Default slides**: Title → Timeline of Events → Root Cause Diagram → Impact Assessment → What Went Well → What Went Wrong → Action Items
- **Palette**: Cherry Bold (urgency without alarm)
- **Layout style**: Timeline-centric, single cause diagram, action item table
- **Slide count**: 8-12
- **Template sources**:
  - GongRzhe `timeline_slide` template: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server
  - Anthropic PPTX skill "Timeline or process flow" pattern: https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md
  - SlideEgg dark timeline templates: https://www.slideegg.com/powerpoint/dark-powerpoint-templates

#### 8. Training / Knowledge Transfer

- **When to use**: Onboarding, team training, explaining a system to new joiners
- **Default slides**: Title → Learning Objectives → Concept Overview → Diagram Walk-through × 3-5 → Hands-on Exercise → Key Takeaways → Resources
- **Palette**: Forest & Moss (approachable, educational)
- **Layout style**: Concept + diagram pairs, numbered steps, callout boxes for key terms
- **Slide count**: 12-20
- **Template sources**:
  - GongRzhe `chapter_intro` + `text_with_image` templates: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server
  - Slidesgo dark educational templates: https://slidesgo.com/dark
  - EasyPPTX grid layouts for multi-concept slides: https://pypi.org/project/EasyPPTX/

#### 9. Sprint / Demo Day

- **When to use**: Demonstrating completed work, showing screenshots, live walkthroughs
- **Default slides**: Title → Sprint Goal → Feature 1 (screenshot + description) → Feature 2 → Feature 3 → Metrics Impact → What's Next
- **Palette**: Coral Energy (energetic, celebratory)
- **Layout style**: Large screenshots/diagrams with brief annotations, minimal text
- **Slide count**: 5-10
- **Template sources**:
  - GongRzhe `full_image_slide` + `text_with_image` templates: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server
  - python-pptx image + textbox positioning: https://python-pptx.readthedocs.io/en/latest/user/shapes.html
  - tomleelong/PPTX JSON outline with image support: https://github.com/tomleelong/PPTX

#### 10. Comparison / Evaluation

- **When to use**: Comparing technologies, vendors, approaches, or architectures side by side
- **Default slides**: Title → Evaluation Criteria → Option A → Option B → Option C → Side-by-Side Matrix → Recommendation → Next Steps
- **Palette**: Ocean Gradient (neutral, analytical)
- **Layout style**: Two-column and three-column comparisons, scoring tables, radar/matrix layouts
- **Slide count**: 8-12
- **Template sources**:
  - GongRzhe `before_after_comparison` + `three_column_layout` templates: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server
  - python-pptx table creation for scoring matrices: https://github.com/scanny/python-pptx/blob/master/docs/user/quickstart.rst
  - SlideModel comparison templates: https://slidemodel.com/templates/tag/dark/

#### 11. Quarterly / Periodic Review

- **When to use**: QBRs, annual reviews, periodic reporting cycles
- **Default slides**: Title → Period Highlights → KPI Dashboard → Trend Over Time → Deep-Dive Topic × 2-3 → Outlook → Actions
- **Palette**: Midnight Executive (formal, recurring)
- **Layout style**: Metric grids, trend charts, consistent recurring structure
- **Slide count**: 10-15
- **Template sources**:
  - GongRzhe `key_metrics_dashboard` template: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server
  - m3dev/pptx-template for recurring report automation via JSON/Excel data: https://github.com/m3dev/pptx-template
  - kwlo/python-pptx-templater for Jinja-style placeholder replacement: https://github.com/kwlo/python-pptx-templater
  - PoweredTemplate dark business templates: https://poweredtemplate.com/powerpoint-templates/dark.html

#### 12. Research / Investigation Findings

- **When to use**: Presenting research results, investigation outcomes, proof-of-concept findings
- **Default slides**: Title → Hypothesis / Question → Methodology → Key Finding 1 (with evidence diagram) → Key Finding 2 → Key Finding 3 → Implications → Recommendations
- **Palette**: Warm Terracotta (academic, thoughtful)
- **Layout style**: Evidence-first (diagram then interpretation), quote callouts for key findings
- **Slide count**: 10-15
- **Template sources**:
  - GongRzhe `quote_slide` + `text_with_image` templates: https://github.com/GongRzhe/Office-PowerPoint-MCP-Server
  - Anthropic PPTX skill design ideas for visual polish: https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md
  - natter1/python_pptx_interface for matplotlib figure integration: https://github.com/natter1/python_pptx_interface

---

### Key Reference Repositories for Templates

| Repository | URL | What It Provides |
|---|---|---|
| GongRzhe/Office-PowerPoint-MCP-Server | https://github.com/GongRzhe/Office-PowerPoint-MCP-Server | 25 slide templates in `slide_layout_templates.json`, 4 colour schemes, python-pptx based |
| anthropics/skills (PPTX) | https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md | Design principles, layout patterns, typography, QA validation loop |
| tfriedel/claude-office-skills | https://github.com/tfriedel/claude-office-skills | OOXML editing workflow, template-based creation, thumbnail validation |
| tomleelong/PPTX | https://github.com/tomleelong/PPTX | Python CLI toolkit with JSON outlines, template directory, Claude Code integration |
| EasyPPTX | https://pypi.org/project/EasyPPTX/ | Percentage-based positioning, grid layouts, dark theme support, TOML templates |
| m3dev/pptx-template | https://github.com/m3dev/pptx-template | Jinja-style DSL for template placeholders, JSON/Excel data injection |
| kwlo/python-pptx-templater | https://github.com/kwlo/python-pptx-templater | Jinja template language for PPTX, layout-based slide generation |
| natter1/python_pptx_interface | https://github.com/natter1/python_pptx_interface | Stylesheet-based formatting, matplotlib integration, PDF/PNG export |
| Ichigo3766/powerpoint-mcp | https://github.com/Ichigo3766/powerpoint-mcp | Picture-with-caption slide type, image handling patterns |

### Free Template Download Sites

| Site | URL | Notes |
|---|---|---|
| SlideModel | https://slidemodel.com/templates/tag/dark/ | Professional dark templates, free + premium |
| SlidesCarnival | https://www.slidescarnival.com/tag/dark | Free, creative commons, dark themes |
| Slidesgo | https://slidesgo.com/dark | Free dark academia and tech themes |
| SlideEgg | https://www.slideegg.com/powerpoint/dark-powerpoint-templates | 160+ free dark templates |
| SlideNest | https://slidenest.com/dark | Free dark templates for PowerPoint/Keynote/Slides |
| PresentationGO | https://www.presentationgo.com/ | 3,200+ free templates and infographic elements |
| PoweredTemplate | https://poweredtemplate.com/powerpoint-templates/dark.html | Free + premium dark templates |
| Envato Elements | https://elements.envato.com/presentation-templates/dark/compatible-with-powerpoint | Premium subscription, highest quality |

---

## Part 2: Writing Style Guide (`references/writing-style.md`)

### Purpose

The skill needs a companion reference that guides the **prose quality** of slide content — not just layout and formatting, but the actual words. Technical presentations fail when the content reads like a document dump onto slides. This reference teaches the agent how to write for a slide context: concise, action-oriented, data-first, jargon-free.

### Community Skills and Resources to Draw From

The following existing Claude Code skills and resources provide battle-tested writing guidance. The coding agent should review these and distil the relevant principles into the `references/writing-style.md` file.

#### Foundation: Elements of Style for AI Agents

**obra/the-elements-of-style**
- URL: https://github.com/obra/the-elements-of-style
- Install: `/plugin install elements-of-style@superpowers-marketplace`
- What it provides: Strunk's 18 core writing rules packaged as a Claude Code plugin. The `writing-clearly-and-concisely` skill loads ~12k tokens of the 1918 text. Key rules: omit needless words, use active voice, put statements in positive form, use definite specific concrete language.
- Why it matters: The foundational layer — every slide title and bullet should pass Strunk's test.

**MCP Market: Concise Writing Style Guide**
- URL: https://mcpmarket.com/tools/skills/concise-writing-style-guide
- What it provides: Enforces active voice, positive framing, elimination of redundant phrasing. Specifically targets READMEs, API docs, and technical wikis.
- Why it matters: Directly applicable to the kind of terse, impactful prose needed on slides.

#### Technical Documentation Skills

**MCP Market: Technical Writing Expert**
- URL: https://mcpmarket.com/tools/skills/technical-writing-expert
- What it provides: Transforms Claude into a documentation specialist. Automatically activates on markdown files and documentation directories. Ensures clarity, accessibility, and actionability.

**MCP Market: Technical Documentation Writing**
- URL: https://mcpmarket.com/tools/skills/technical-documentation-writing
- What it provides: Standardised templates for READMEs, API documentation (JSDoc, Python docstrings), and lifecycle documentation.

**MCP Market: Documentation Standards**
- URL: https://mcpmarket.com/tools/skills/documentation-standards-5
- What it provides: Framework for distinguishing user-facing vs internal documentation. Establishes protocols for each audience type.

**MCP Market: Technical Writer**
- URL: https://mcpmarket.com/tools/skills/technical-writer-1
- What it provides: Information architecture audits, gap identification, task-based content creation (API refs, tutorials, migration guides).

#### Technical Blogging and Narrative Skills

**MCP Market: Technical Blog Writer**
- URL: https://mcpmarket.com/tools/skills/technical-blog-writer
- What it provides: Concept-first methodology (explain "why" before "how"), progressive explanation layers, Mermaid diagram integration, citation verification for benchmarks/metrics. Prevents fabrication of quantitative data.
- Why it matters: The "why before how" principle is critical for technical slide narratives.

**MCP Market: Technical Writing (AI Blogging)**
- URL: https://mcpmarket.com/tools/skills/technical-writing-2
- What it provides: Anti-AI voice control (filters out robotic phrasing and AI clichés using custom reference guides), context-aware code analysis, structured drafting with hooks and technical deep-dives.
- Why it matters: Prevents the generic AI tone that makes slide content feel hollow.

#### Co-Authoring and Review Skills

**MCP Market: Doc Co-Authoring**
- URL: https://mcpmarket.com/tools/skills/document-co-authoring-workflow-1
- What it provides: Three-stage co-authoring process for technical documentation and proposals. Structured review workflow.

**dhruvbaldawa/ccconfigs: writing-documentation skill**
- URL: https://claude-plugins.dev/skills/@dhruvbaldawa/ccconfigs/writing-documentation
- What it provides: Applies Elements of Style principles specifically to technical documentation types (README, API docs, architecture docs, CLI docs). Includes a `reference/doc-types.md` with per-type guidelines.

#### Real-World Workflows

**Mintlify's Claude Code Writing Standards**
- URL: https://www.mintlify.com/blog/how-mintlify-uses-claude-code-as-a-technical-writing-assistant
- What it provides: Practical guidance on putting writing standards in CLAUDE.md, requiring verification of code examples and links, using Claude for maintenance-style writing, and the importance of planning before writing.

**Kaz Sato's Multi-Agent Technical Writing**
- URL: https://medium.com/google-cloud/supercharge-tech-writing-with-claude-code-subagents-and-agent-skills-44eb43e5a9b7
- What it provides: Multi-specialist review pattern — one agent for professional editing (style, grammar, structure) and another as a subject matter expert for technical accuracy. Found 31 issues across 2 review passes.

---

### Slide-Specific Writing Principles

The `references/writing-style.md` file should distil these principles from the sources above, adapted specifically for presentation slide content:

#### Titles
- **Action-oriented, not descriptive**: "PostgreSQL Drives 45% of Total Spend" not "Database Cost Overview"
- **Lead with the conclusion**: The title should tell the audience what to think, not what to look at
- **One idea per title**: If you need "and" in the title, split into two slides
- **Max 8 words**: Shorter titles have more visual impact at 36-44pt

#### Bullets
- **Parallel structure**: Every bullet should start with the same grammatical form (all verbs, all nouns, etc.)
- **Front-load the key information**: "£18.40/GB — App Gamma exceeds threshold by 84%" not "App Gamma has a cost per GB of £18.40 which is 84% over our threshold"
- **No more than 5 bullets per slide**: If you have more, split or summarise
- **Each bullet ≤ 2 lines**: If it wraps beyond 2 lines, it's a paragraph disguised as a bullet

#### Prose
- **Active voice always**: "The migration reduced costs by 30%" not "Costs were reduced by 30% through the migration"
- **Concrete over abstract**: "3 of 12 applications exceed £10/GB" not "Several applications have elevated cost profiles"
- **Define jargon on first use**: If the audience might not know a term, add a parenthetical
- **Data-first phrasing for metrics**: Lead with the number, not the label: "£2.10/GB — lowest cost per GB across all applications" not "The lowest cost application has a cost per GB of £2.10"

#### Captions (for diagrams)
- **Describe what the audience should notice**: "Arrows show the hot path from API gateway to PostgreSQL — the most cost-intensive route" not "Figure 1: System Architecture"
- **Keep under 15 words**: Captions compete with the image for attention

#### Anti-Patterns to Reject
- Generic opening slides ("Agenda", "Table of Contents") — jump straight to content
- Slide titles that repeat the section header verbatim
- Bullet points that are complete sentences with full punctuation
- "In conclusion" / "To summarise" — the closing slide should be actionable, not reflective
- Filler phrases: "It is important to note that", "As we can see from the data", "Going forward"
- AI-sounding prose: "leverage", "utilize", "streamline", "cutting-edge", "game-changer"

---

### Integration Into the Skill Workflow

The SKILL.md workflow should reference this writing guide at two points:

1. **During content generation** (Step 2: Plan): When deciding what text goes on each slide, consult `references/writing-style.md` for title and bullet conventions
2. **During QA** (Step 4: Validate): After visual QA, run a content QA pass checking slide titles against the action-oriented rule and bullets against the parallel structure rule

The coding agent building this skill should review at minimum:
- `obra/the-elements-of-style` SKILL.md: https://github.com/obra/the-elements-of-style/blob/main/skills/writing-clearly-and-concisely/SKILL.md
- Anthropic's PPTX skill design ideas: https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md
- The MCP Market Technical Blog Writer: https://mcpmarket.com/tools/skills/technical-blog-writer

These three sources together cover clear writing fundamentals, slide-specific design principles, and technical narrative structure.
