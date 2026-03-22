# Presentation Archetypes

Twelve archetypes covering the most common presentation scenarios. Each defines a default slide sequence, recommended palette, and slide count range.

Slide type names reference `slide-types.md`. Palette names reference `palettes.md`.

---

## 1. Executive Summary

**When to use:** Presenting results, decisions, or recommendations to senior leadership. Headlines and metrics first, detail on demand.

**Default slide sequence:**
1. `title` — deck title with date
2. `metrics` — 3-4 key numbers that tell the story
3. `content` — executive narrative (the "so what")
4. `diagram` — one supporting visual
5. `content` — recommendations or options
6. `closing` — decision needed / next steps

**Recommended palette:** `midnight-exec`
**Layout style:** Clean, headline-driven. Large metrics. Minimal bullets.
**Slide count:** 5-8

---

## 2. Technical Deep-Dive

**When to use:** Explaining architecture, system design, or technical decisions to engineering peers. Diagrams and detail are welcome.

**Default slide sequence:**
1. `title` — topic and scope
2. `content` — problem statement / context
3. `section_header` — "Architecture"
4. `diagram` — high-level architecture
5. `diagram` — component detail or data flow
6. `content` — key design decisions with bullets
7. `two_column` — trade-offs or alternatives
8. `section_header` — "Implementation"
9. `content` — approach and timeline
10. `metrics` — performance targets or benchmarks
11. `closing` — open questions / next steps

**Recommended palette:** `ocean`
**Layout style:** Diagram-heavy. Alternate between content and diagram slides.
**Slide count:** 10-15

---

## 3. Architecture Review

**When to use:** Reviewing system architecture changes, migration plans, or design proposals with diagrams showing before/after states.

**Default slide sequence:**
1. `title` — review topic
2. `content` — context and goals
3. `section_header` — "Current State"
4. `diagram` — current architecture
5. `section_header` — "Proposed State"
6. `diagram` — target architecture
7. `comparison` — before vs after
8. `content` — migration path with bullets
9. `metrics` — expected improvements
10. `closing` — approval / next steps

**Recommended palette:** `charcoal`
**Layout style:** Diagram-focused with before/after comparisons. Use `diagram_full` for complex visuals.
**Slide count:** 8-12

---

## 4. Data Analysis Dashboard

**When to use:** Presenting metrics, cost analysis, performance data, or any quantitative findings. Numbers drive the narrative.

**Default slide sequence:**
1. `title` — analysis topic and period
2. `metrics` — headline numbers
3. `content` — key findings summary
4. `diagram` — chart or data visualisation
5. `two_column` — segment breakdowns
6. `diagram` — trend or comparison chart
7. `content` — analysis and implications
8. `metrics` — secondary metrics
9. `closing` — recommendations

**Recommended palette:** `midnight`
**Layout style:** Metrics-heavy. Lead each section with numbers, then explain.
**Slide count:** 8-12

---

## 5. Project Status Update

**When to use:** Sprint reviews, project updates, progress reports. Quick, scannable, action-oriented.

**Default slide sequence:**
1. `title` — project name and date
2. `metrics` — status indicators (on-track, at-risk, blocked)
3. `content` — accomplishments this period
4. `content` — upcoming work
5. `comparison` — plan vs actual (if relevant)
6. `closing` — blockers and asks

**Recommended palette:** `sage-calm` or `teal-trust`
**Layout style:** Scannable. Metrics up front. Bullets for status items.
**Slide count:** 5-8

---

## 6. Proposal / Business Case

**When to use:** Persuading decision-makers to approve a project, investment, or initiative. Build the case with evidence and a clear ask.

**Default slide sequence:**
1. `title` — proposal name
2. `content` — the problem / opportunity
3. `metrics` — quantified impact or market size
4. `content` — proposed solution
5. `diagram` — solution architecture or process
6. `two_column` — benefits vs costs
7. `comparison` — option A vs option B
8. `metrics` — ROI / payback projections
9. `content` — implementation timeline
10. `closing` — the ask with call to action

**Recommended palette:** `berry-cream`
**Layout style:** Persuasive flow. Problem-solution-evidence-ask structure.
**Slide count:** 10-15

---

## 7. Incident / Post-Mortem

**When to use:** Reviewing a production incident, outage, or failure. Timeline-driven, blameless, focused on learnings.

**Default slide sequence:**
1. `title` — incident identifier and date
2. `metrics` — impact numbers (duration, users affected, revenue)
3. `content` — incident summary
4. `diagram` — timeline or sequence of events
5. `content` — root cause analysis
6. `comparison` — what happened vs what should have happened
7. `content` — action items with bullets
8. `closing` — follow-up owners and dates

**Recommended palette:** `cherry-bold`
**Layout style:** Timeline-focused. Metrics for impact. Clear action items.
**Slide count:** 8-12

---

## 8. Training / Knowledge Transfer

**When to use:** Onboarding, how-to guides, process walkthroughs. Teach a concept or procedure step by step.

**Default slide sequence:**
1. `title` — training topic
2. `content` — learning objectives
3. `section_header` — "Concepts"
4. `content` — core concept 1
5. `diagram` — supporting visual
6. `content` — core concept 2
7. `diagram` — supporting visual
8. `section_header` — "Hands-On"
9. `content` — step-by-step procedure
10. `two_column` — do vs don't
11. `content` — common pitfalls
12. `diagram` — reference architecture or cheat sheet
13. `closing` — resources and contacts

**Recommended palette:** `forest-moss`
**Layout style:** Progressive disclosure. Alternate concept and visual slides.
**Slide count:** 12-20

---

## 9. Sprint / Demo Day

**When to use:** Showcasing completed work at a sprint demo, hackathon, or show-and-tell. Visual and energetic.

**Default slide sequence:**
1. `title` — sprint number or demo title
2. `metrics` — sprint velocity or key results
3. `content` — feature 1 with description
4. `diagram` — screenshot or demo capture
5. `content` — feature 2 with description
6. `diagram_full` — full-bleed screenshot
7. `closing` — what's next

**Recommended palette:** `coral-energy`
**Layout style:** Visual-first. Screenshots and demos dominate. Keep text minimal.
**Slide count:** 5-10

---

## 10. Comparison / Evaluation

**When to use:** Side-by-side analysis of tools, vendors, approaches, or options. Structured evaluation with clear criteria.

**Default slide sequence:**
1. `title` — evaluation topic
2. `content` — evaluation criteria and methodology
3. `comparison` — option A vs option B (overview)
4. `two_column` — detailed feature comparison
5. `comparison` — option A vs option B (technical)
6. `metrics` — scoring or ranking
7. `two_column` — cost comparison
8. `diagram` — decision matrix or scoring chart
9. `content` — recommendation with rationale
10. `closing` — next steps

**Recommended palette:** `ocean-gradient`
**Layout style:** Symmetrical comparisons. Use `comparison` and `two_column` types heavily.
**Slide count:** 8-12

---

## 11. Quarterly Review

**When to use:** QBRs, periodic business reviews, board updates. Structured around time periods with metrics and trends.

**Default slide sequence:**
1. `title` — quarter and year
2. `metrics` — headline KPIs
3. `section_header` — "Performance"
4. `content` — highlights and lowlights
5. `diagram` — trend chart or dashboard screenshot
6. `metrics` — department or product metrics
7. `section_header` — "Outlook"
8. `content` — next quarter priorities
9. `comparison` — plan vs actual
10. `two_column` — risks and mitigations
11. `closing` — key decisions needed

**Recommended palette:** `midnight-exec`
**Layout style:** Metrics-first. Period-over-period comparisons. Executive-friendly.
**Slide count:** 10-15

---

## 12. Research / Investigation

**When to use:** Presenting research findings, competitive analysis, or investigation results. Evidence-based with supporting data.

**Default slide sequence:**
1. `title` — research topic
2. `content` — research question and methodology
3. `section_header` — "Findings"
4. `content` — finding 1 with evidence
5. `diagram` — supporting data or visualisation
6. `content` — finding 2 with evidence
7. `diagram` — supporting data or visualisation
8. `content` — finding 3 with evidence
9. `two_column` — implications and limitations
10. `metrics` — key quantitative findings
11. `closing` — conclusions and recommended actions

**Recommended palette:** `warm-terracotta`
**Layout style:** Evidence-driven. Each finding backed by data or a visual. Progressive build-up to conclusions.
**Slide count:** 10-15

---

## Decision Matrix

Use this matrix to narrow from 12 archetypes to 2 recommendations based on goal and audience.

### By Goal

| Goal | Primary archetype | Secondary archetype |
|------|-------------------|---------------------|
| Inform | Executive Summary | Data Analysis Dashboard |
| Persuade | Proposal / Business Case | Comparison / Evaluation |
| Review | Quarterly Review | Project Status Update |
| Educate | Training / Knowledge Transfer | Technical Deep-Dive |
| Propose | Proposal / Business Case | Architecture Review |

### By Audience

| Audience | Best archetypes |
|----------|-----------------|
| Technical peers | Technical Deep-Dive, Architecture Review, Incident / Post-Mortem |
| Leadership | Executive Summary, Quarterly Review, Proposal / Business Case |
| Mixed | Data Analysis Dashboard, Project Status Update, Comparison / Evaluation |
| External | Proposal / Business Case, Research / Investigation, Executive Summary |

### Goal x Audience

| | Technical peers | Leadership | Mixed | External |
|---|---|---|---|---|
| **Inform** | Technical Deep-Dive | Executive Summary | Data Analysis Dashboard | Executive Summary |
| **Persuade** | Architecture Review | Proposal / Business Case | Comparison / Evaluation | Proposal / Business Case |
| **Review** | Sprint / Demo Day | Quarterly Review | Project Status Update | Quarterly Review |
| **Educate** | Training / Knowledge Transfer | Executive Summary | Training / Knowledge Transfer | Research / Investigation |
| **Propose** | Architecture Review | Proposal / Business Case | Proposal / Business Case | Proposal / Business Case |
