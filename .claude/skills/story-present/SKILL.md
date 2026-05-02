---
name: story-present
description: "Generates structurally sound presentations for high-stakes moments — board meetings, steering committees, investor pitches, conference talks, weekly status, budget escalations, project kickoffs, all-hands updates. Interviews the user about audience and goal, routes to the right framework (McKinsey Pyramid, pitch deck, issue tree, roadmap, conference narrative, RAID/RAG status, or steering board pack), ingests source material from email/calendar/WhatsApp/memory/git if asked, generates Marp markdown, self-scores against a layered rubric (base + output-class overlay) with auto-refine, and renders to HTML/PPTX/DOCX. Use this whenever the user needs to present to an audience and cares that the structure holds up — even if they don't say 'slides' or 'deck'. Triggers include: 'present to the board', 'prep for Thursday's exec review', 'put together a pitch', 'steering update', 'draft a status report deck', 'I'm speaking at PyData', 'budget variance write-up for leadership', 'help me tell this story', 'need to convince the exec team', 'conference talk', 'RAID update', 'board pack'. Prefer this over generic slide-writing skills when the user needs the *structure* to do persuasive work, not just a visual layout."
---

# story-present

## Routing Overview — the eight frameworks

| Option | Framework | Best for | Primary format | Example |
|--------|-----------|----------|----------------|---------|
| 1 | McKinsey Pyramid Principle | Conclusion-first consulting decks for executives | slides | "We should consolidate our 3 data warehouses — here's why" |
| 2 | Market Strategy / Pitch Deck | Investor pitches, fundraising, market positioning | slides | "Series A pitch: $50M TAM in dev-tools" |
| 3 | Internal Problem-Solving / Issue Tree | Root-cause analysis and solution recommendation | slides | "Why deploys fail 15% of the time and 3 fixes" |
| 4 | Project Roadmap / Implementation Plan | Objective → phases → team → success criteria | slides | "H2 migration: 4 phases, 3 teams, 16 weeks" |
| 5 | Conference / Tech Talk | Informing developers/practitioners with a narrative arc | slides | "How we replaced 3 MCP servers with 40 CLI commands" |
| 6 | RAID Log / Weekly Status | Weekly team status, RAG dashboard, RAID register | slides | "Sprint 14: amber on scope, green on the rest" |
| 7 | Steering Committee / Board Pack | Governance decisions, budget variance, escalations | slides | "Data warehouse is 40% over budget — we need a scope decision" |
| 8 | Design Document / RFC | Technical proposal for peer review — problem, design, alternatives, tradeoffs | docx | "Migrate session store from Redis to DynamoDB — design review" |

Full content sequences live in `references/templates/template-*.md`. Load only the one you need.

### Format compatibility

Rendering is decoupled from content generation — every framework produces a canonical Marp `.md` (or section-structured markdown for long-form outputs), and each renderer (html / interactive / pptx / docx / executive-html) consumes that independently. However, some framework × format combinations are natural fits while others are awkward:

| Framework | docx | html | pptx | interactive | executive-html | Notes |
|-----------|------|------|------|-------------|----------------|-------|
| 1 McKinsey Pyramid | ✓ | ✓ | ✓ | ✓ | ✓ | Conclusion-first hero + argument cards |
| 2 Pitch Deck | ✓ | ✓ | ✓ | ✓ | ○ | Investors expect pptx/PDF — flag but allow |
| 3 Issue Tree | ✓ | ✓ | ✓ | ✓ | ✓ | Root-cause cards + solution tiles |
| 4 Roadmap | ✓ | ✓ | ✓ | ✓ | ✓ | Timeline component is a natural match |
| 5 Conference Talk | ✓ | ✓ | ✓ | ✓ | ✓ | Companion article / reading version |
| 6 RAID / Weekly | ✓ | ✓ | ✓ | ○ | ✓ | Dashboard page with RAG metrics — natural fit |
| 7 Steering Pack | ✓ | ✓ | ✓ | ○ | ✓ | Governance pack circulated as URL — strong fit |
| 8 Design Doc / RFC | **✓ primary** | ✓ | ○ | ○ | **✓ primary** | Richest component match for executive-html |

✓ = recommended, ○ = available but the agent should flag it as suboptimal and confirm before rendering.

---

## Process Overview

1. **Level 1 interview** (T0 + Q1–Q6 below, conversational, one at a time). Probe on routing-critical questions (Q2, Q3, Q4) before falling back to defaults.
2. **Depth-mining probes** (D1–D3 after Q4) — extract specific numbers, story arc catalyst, and business bridge. All 8 frameworks.
3. **Understanding Check** — summarise and confirm with the user.
4. **Scope negotiation** — after the user confirms the Understanding Check, play back the proposed scope and actively suggest cuts. Details in §Scope Negotiation below.
5. **Source ingestion** (if Q6 selected any source) — run CLI shortcuts via Bash and capture results into the working notes block. This runs *before* Level 2 because the Level 2 questions reference the ingested data directly ("I see 3 emails about the merger — which one is authoritative?"); asking Level 2 first forces placeholders that later need rework.
6. **Routing** — apply the Q4 (goal) + Q2 (audience) matrix to recommend one of the 8 frameworks. User can override.
7. **Load the matching `references/interview/level2-*.md` and `references/templates/template-*.md`** for the chosen framework.
8. **Level 2 interview** — ask framework-specific questions, referencing ingested data.
9. **Generate Marp markdown** following the chosen template's slide/section sequence and the conventions in `references/generation/marp-conventions.md`. Apply prose-craft directives for Options 5 and 8 (see §Prose-craft directives). Pause at the **mid-generation checkpoint** (after slide 3–4) for user validation before continuing.
10. **Prose refinement** (Options 5 docx + 8 only) — run the mid-generation prose refinement pass: hedging scan, ABT rhythm, alternating rhythm, insight landing, specificity, layered depth. See §Mid-generation prose refinement.
11. **Scoring gate** — self-evaluate against layered rubric in `references/generation/scoring-rubric.md` (base 65 pts + output-class overlay 35 pts = 100). Apply matching hard gate (visual variety for slides, document quality for prose). Refine up to 2 times. Deliver with caveats if still <60 after 2 refines.
12. **Delivery prompt** — ask which formats the user wants delivered (marp / html / pptx / docx / all) and invoke the corresponding CLI shortcut.

**Safe default policy:** For **routing-critical questions** (Q2 audience, Q3 key points, Q4 goal), **probe before defaulting** — ask one clarifying follow-up that surfaces what kind of answer would change the output. Only after the probe is also unanswered, apply the safe default from `references/interview/intake-defaults.md`. For all other questions (T0, Q1, Q5, Q6, all L2), apply the default after 2 unanswered prompts. Log which defaults were applied so the Understanding Check can surface them.

---

## Level 1 Interview — Universal Context

Ask one question at a time, conversationally. For **routing-critical questions** (Q2, Q3, Q4), use the probing follow-ups below before falling back to defaults — these three questions drive framework selection and scope, so vague answers produce bad routing. For other questions (T0, Q1, Q5, Q6), apply the safe default from `references/interview/intake-defaults.md` after 2 unanswered prompts.

### T0 — Topic folder anchor
"Which topic folder under `pete-pa/topics/` should I anchor this run to? I will use `pete-pa/topics/<topic-folder>/` as the default evidence root and `pete-pa/topics/<topic-folder>/story-outputs/<slug>/` for outputs."

If the user is unsure, propose a folder name from Q1 topic language and confirm it in the Understanding Check.

### Q1 — Topic and outcome
"What is this presentation about? What should the audience walk away knowing, feeling, or being able to do?"

### Q2 — Audience
"Who is the audience? (e.g., C-suite executives, engineering team, investors, conference attendees, steering committee)"

**Probing follow-up (if vague or generic):** If the answer is generic ("business people", "my team", "stakeholders"), probe once: *"Help me narrow this — what do they already know about the topic, and what's their stake in the outcome? That changes whether I lead with context or conclusions."* This determines whether the deck needs background slides or can jump straight to recommendations — it directly affects framework selection and slide count.

**Audience → theme mapping.** After Q2, infer a default preview theme from the audience keyword and surface it in the Understanding Check. The user can override by naming any of the 7 themes. Preview CSS snippets live in `references/visual/themes/<name>.css` and are used **only** during the Understanding Check to show the visual register — the actual render uses the existing asset bundles at `assets/themes/<name>/`. The `conference` name collision is intentional: the preview snippet in `references/visual/themes/conference.css` mirrors the asset bundle at a high level but is a separate file (the asset bundle stays authoritative for rendering).

| Audience contains... | Default theme | Register |
|----------------------|---------------|----------|
| C-suite, executives, leadership | `business` | white + navy + top-border accent |
| developers, engineering, tech team | `tech` | GitHub-dark + blue/green |
| keynote, showcase, dark-mode request | `dark` | black + cyan/purple glow |
| board, directors, governance | `editorial` | warm neutrals + serif |
| conference, meetup, PyData, talk | `conference` | slate + cyan, code-friendly |
| internal, standup, weekly, team | `minimal` | white + grey + geometric |
| creative, marketing, launch | `vibrant` | dominant colour + sharp accent |

The picked theme name is passed through at delivery time to `story-present-render-html --theme <name>` (and the pptx/docx shortcuts), which resolves it to `assets/themes/<name>/`.

### Q3 — Key points
"What are the key points or sections you want to cover? List the main ideas, even if rough. If you have an outline from a brainstorming session, paste it here."

**Probing follow-up (always, after Q3 answer):** After the user lists key points, probe for scope boundaries: *"What's explicitly NOT in scope? Anything the audience might expect to see that you deliberately want to leave out?"* This prevents scope creep and gives generation a clear exclusion list. If the user lists more than 6 key points, actively suggest cuts: *"That's [N] topics — a 15-minute deck can land 3–4 well or 7 poorly. Which are must-have vs nice-to-have?"*

### Q4 — Primary goal (routing discriminator)
"What is the primary goal — are you **persuading** (recommending, pitching, selling), **informing** (status update, report, education), or **deciding** (steering committee, board approval)?"

**Probing follow-up (if ambiguous):** If the answer mixes goals ("I want to inform them but also get buy-in"), probe once: *"If this meeting goes perfectly, what happens next — do they approve something, change their mind, or just walk away better informed?"* The answer reveals the true primary goal for routing. Don't accept a dual goal silently — surface the tension: *"Informing and persuading need different opening moves. Which matters more for this specific meeting?"*

### Depth-mining probes (after Q4, before Q5)

After Q4 is answered, ask these three probes **in sequence** to seed generation with specific, honest, business-connected raw material. These apply to **all 8 frameworks** — even slide decks benefit from radical specificity.

**Probe D1 — Concrete evidence:** *"What specific numbers can you share — before/after metrics, percentages, timelines, costs? Even rough estimates are more useful than 'significant improvement'."*
Purpose: extracts the radical specificity that separates compelling content from corporate mush. Numbers anchor every framework: McKinsey conclusions, pitch decks, issue trees, conference demos, status RAGs, and design doc trade-offs.

**Probe D2 — Story arc:** *"What was the catalyst — the thing that forced change or created the opportunity? What didn't work first?"*
Purpose: extracts the "hole" in the Man-in-Hole arc. Creates narrative tension in any format — executives remember the struggle, not the steady state. If the user says "nothing broke, it's a new initiative," that's a valid answer — the probe still surfaces it.

**Probe D3 — Business bridge:** *"What business outcome does this enable for the audience? What happens if they do nothing?"*
Purpose: forces the value bridge. Technical audiences care about enabling outcomes; executive audiences care about risk/opportunity cost. The inaction scenario (do-nothing cost) is often the best opening slide for persuasion frameworks.

If a probe is met with silence or "I don't know," that's fine — log the gap in working notes as `[EVIDENCE GAP: D1/D2/D3]` and move on. Do not default-fill with vague claims.

### Q5 — Constraints
"Any constraints? Target number of slides, time limit, things to avoid, branding requirements, or specific data/diagrams to include?"

### Q6 — Source material
"Where should I pull the source material from? Select any that apply:
- (a) **Email** — Gmail/Outlook via `gmail-search`, `outlook-search`, or `email-finder-search` (hybrid keyword+semantic)
- (b) **Calendar** — `calendar-events`, `outlook-calendar`
- (c) **Team messaging** — `whatsapp-messages` on a named channel
- (d) **Agent memory** — `memory-search`, `memory-context`, `memory-recent` across episodic/task/semantic tiers with FTS5 + optional vector search
- (e) **Saved agent conversations** — prior session transcripts under `.claude/` or distilled memories
- (f) **Git work reports** — commit history, branch diffs, PR descriptions
- (g) **Markdown reports** — files under `pete-pa/topics/<topic-folder>/`, `.claude/plans/`, or a user-specified path
- (h) **None** — I'll work only from what you tell me in this interview

For each selected source, give me a query hint (keywords, date range, channel name, path)."

### Q6a — Image-first sub-step

If the user names an image directory (in Q5 constraints or Q6 hint) — or says "use these pictures", "the images in X", or similar — **scan it before routing to Level 2**. Image inventory shapes the outline (visual-led vs text-led), so it must happen before framework selection locks in a slide count. Full scan pattern, outline adaptation rules by image count, and empty-directory fallback live in **`references/generation/image-ingestion.md`**. Surface the scan results in the Understanding Check so the user can veto specific files before generation.

---

## Understanding Check

After collecting T0 + Q1–Q6 (or applying defaults), present:

```
## Understanding Check

- **Topic**: [summary]
- **Audience**: [summary]
- **Key points**: [bullet list]
- **Goal**: Persuading / Informing / Deciding
- **Constraints**: [summary]
- **Topic folder**: [topic-folder] (`pete-pa/topics/<topic-folder>/`)
- **Source material**: [selected sources + query hints, or "interview answers only"]
- **Theme**: [inferred theme name from audience mapping] (override with any of: business / tech / dark / editorial / vibrant / minimal / conference)

Does this capture your intent? (yes / adjust)
```

If "adjust", re-ask the affected questions. Only proceed to scope negotiation after the user confirms.

---

## Scope Negotiation (between Understanding Check and Source Ingestion)

After the user confirms the Understanding Check, play back a tight scope summary and actively probe for cuts. This step prevents bloated decks built from unfiltered brain-dumps.

**Procedure:**

1. **Summarise the proposed scope** in 2–3 sentences: topic, audience, goal, and the key points from Q3.
2. **Flag scope risks:**
   - If key points exceed slide budget (from Q5), say: *"You have [N] topics for a [M]-slide deck. To land each one properly, I'd suggest cutting to [N−2]. Which topics are essential vs deferrable?"*
   - If key points are vague ("discuss the project"), say: *"This is broad — can you name the 2–3 specific things the audience needs to walk away with?"*
   - If no exclusions were given in Q3 follow-up, say: *"You haven't named anything as out of scope. What might the audience expect to see that you want to deliberately skip?"*
3. **Propose a v1 scope** — a tightened version of the key points that fits the constraints. The user can accept or adjust.
4. **Lock scope** — once confirmed, the locked scope feeds into routing and generation. Any key points the user deferred are logged as "Parked topics" in the working notes for potential follow-up decks.

Only proceed to source ingestion (or routing, if Q6 = None) after scope is locked.

---

## Source Ingestion (between Level 1 and Level 2)

If Q6 selected any source other than (h), run the relevant CLI shortcuts **before** the Level 2 interview, so Level 2 can reference real data rather than placeholders.

| Source | CLI shortcut(s) | Notes |
|--------|----------------|-------|
| Email (keyword) | `gmail-search`, `outlook-search` | Use `--json` and `--weeks`/`--days` derived from Q5 |
| Email (semantic) | `email-finder-search` | For "find anything like X" across archives |
| Calendar | `calendar-events`, `outlook-calendar` | Filter by date range from Q5 |
| WhatsApp | `whatsapp-messages --chat <name>` | Channel name from Q6 hint |
| Agent memory | `memory-search`, `memory-context`, `memory-recent` | Cross-tier retrieval, FTS5 + optional vector search |
| Saved conversations | `Read` / `Grep` against `.claude/` | No CLI — direct file access |
| Git | `git log`, `git diff`, `gh pr list` | Summarise via Bash |
| Markdown reports | `Read` / `Grep` against `pete-pa/topics/<topic-folder>/`, `.claude/plans/` | Default paths if no hint |

Full ingestion detail, per-source Bash patterns, the working-notes block structure, and the slide citation format all live in **`references/generation/source-ingestion.md`** — load that file before running the ingestion step.

**Ingest sources step:**
1. For each source selected in Q6 (other than (h) None), run the matching `poetry run <shortcut> ... --json` invocation from `references/generation/source-ingestion.md` §3, passing date-range filters derived from Q5 (`--weeks` / `--days`). For source (g), if no path hint is given, default to `pete-pa/topics/<topic-folder>/` from T0.
2. Capture every returned item into the working-notes block using the structure in `references/generation/source-ingestion.md` §2, with the source tag that §4 requires for citations.
3. If Q6 = (h) None, skip ingestion entirely and proceed directly to Level 2 using only the interview answers.

Every factual claim on a generated slide that comes from an ingested item should carry a `Source: <tag>` marker (e.g. `Source: memory-event-42`, `Source: commit 19f61a6`, `Source: pete-pa/topics/weekly-report/2026-04-weekly.md`). The user needs to audit where each number or quote came from before they put it in front of a board or investor — unsourced claims in a high-stakes deck are the single biggest reason presentations get torn apart in the room.

---

## Level 1 → Framework Routing

After ingestion completes (or immediately if Q6 = None), apply this matrix based on Q4 (goal) and Q2 (audience):

| Q4 Goal | Q2 Audience contains... | Recommended Framework | Option # |
|---------|------------------------|----------------------|----------|
| Persuading | investors, board, VCs, fundraising | Market Strategy / Pitch Deck | 2 |
| Persuading | executives, leadership, C-suite, senior | McKinsey Pyramid Principle | 1 |
| Persuading | internal team, engineering, product | Internal Problem-Solving / Issue Tree | 3 |
| Persuading | engineering peers, architects, reviewers, "design doc", "RFC", "proposal" | Design Document / RFC | 8 |
| Informing | conference, meetup, community, developers | Conference / Tech Talk | 5 |
| Informing | team, weekly, standup, project | RAID Log / Weekly Status | 6 |
| Informing | general, mixed, unknown | McKinsey Pyramid Principle | 1 |
| Deciding | steering committee, programme board, governance | Steering Committee / Board Pack | 7 |
| Deciding | board, directors, investors (approval context) | Steering Committee / Board Pack | 7 |
| Any | mentions "roadmap", "implementation", "plan" | Project Roadmap / Implementation Plan | 4 |

Present the recommendation:

```
Based on your audience ([audience]) and goal ([goal]), I recommend the **[Framework Name]** structure.

Here are all available frameworks:
1. McKinsey Pyramid Principle — conclusion-first, 3–5 supporting arguments, evidence
2. Market Strategy / Pitch Deck — market sizing → positioning → differentiation → growth
3. Internal Problem-Solving / Issue Tree — problem → root causes → solutions → priorities
4. Project Roadmap / Implementation Plan — objective → phases → team → success criteria
5. Conference / Tech Talk — hook → journey → demos → takeaways
6. RAID Log / Weekly Status — RAG dashboard → RAID summary → milestones → next steps
7. Steering Committee / Board Pack — exec summary → decision required → status → financials → risks → recommendation
8. Design Document / RFC — problem → proposed design → alternatives → tradeoffs → open questions (docx primary)

Which would you like? (enter number, or press enter for my recommendation)
```

Once the framework is chosen, load:
- `references/interview/level2-*.md` for framework-specific questions (consulting / conference / raid-status / designdoc)
- `references/templates/template-*.md` for the content sequence (pyramid / storyline-market / storyline-problem / storyline-roadmap / conference / raid-status / steering / designdoc)

---

## Level 2 Interview

Framework-specific questions live in:

| Framework | File |
|-----------|------|
| Options 1, 2, 3, 4 | `references/interview/level2-consulting.md` |
| Option 5 | `references/interview/level2-conference.md` |
| Options 6, 7 | `references/interview/level2-raid-status.md` |
| Option 8 | `references/interview/level2-designdoc.md` |

Safe-default rule for L2: after 2 unanswered prompts, apply the default from `references/interview/intake-defaults.md` and move on. (The probing-first policy applies only to L1 routing-critical questions Q2/Q3/Q4.)

---

## Generation

Load `references/templates/template-<framework>.md` and walk the slide sequence. For each slide:
- Honour the template's title style rule (**action title** for consulting/RAID/steering/pyramid, **declarative heading** for conference).
- **Max 8 words per title.** Shorter titles have more impact — "Three Apps Exceed Cost Thresholds" beats "A Summary of the Three Applications That Have Exceeded Their Cost Thresholds". Full rules in `references/generation/writing-style.md`.
- One message per slide. Two points → two slides.
- Cite evidence from the working notes block. Unsourced claims are risky.
- Mark missing data with `[DATA NEEDED: brief description]`.
- Follow Marp conventions from `references/generation/marp-conventions.md`.
- **Visual minimums per layout type** — every slide whose template marks a layout type MUST contain the matching visual element. Full per-type table in `references/generation/marp-conventions.md` §"Visual minimums per layout type". Summary: `split-image` → MUST have `![bg right/left:40%]`; `diagram` → MUST have a ` ```mermaid ` fence; `code-block` → MUST have a fenced code block; `evidence` → MUST have a ` ```chart ` fence, ` ```mermaid ` fence, or image directive. No real asset? Use a placeholder directive + appendix back-reference (`references/visual/visual-design-principles.md` §"Rich visual placeholder protocol"). All placeholder descriptions collect into a `# Appendix — Visual Placeholders` table after the last numbered slide.
- **Palette application** — after choosing a theme via the audience→theme picker, inject a `<style>` block mapping the theme's CSS variables into the deck. Include explicit table readability rules (body background, header background/text, borders) so markdown tables remain legible in raw Marp preview. Pattern in `references/generation/marp-conventions.md` §"Palette CSS injection".
- **Visual design craft** — apply the 10 rules in `references/visual/visual-design-principles.md` and pick a palette from `references/visual/palettes.md`. These catch common "AI-generated deck" tells.
- **Use `metrics` callout slides** when a number is the story. A 60–72pt stat with a short label lands harder than the same number embedded in a bullet. See `references/visual/slide-types-pptx.md` for layout coordinates.
- **Image directive variety** — pull recipes from `references/generation/marp-image-cookbook.md`; use at least 2 distinct directives across the deck. Prerequisite for the visual variety hard gate (slides output class).
- **Diagram picker** — consult `references/generation/mermaid-diagram-picker.md` and pick the row whose situation matches. Emit ` ```mermaid ` fences; the pre-render step converts them to SVG.
- **Technical depth** — if the audience is technical or the source material is technical, run the extraction procedure in `references/generation/technical-depth-mining.md` before walking the template. High-value items get dedicated slides; diagrammable items become mermaid fences.
- **Mermaid over placeholders** — when source material describes a data flow, service topology, state machine, timeline, hierarchy, API interaction, comparison, or project phase, emit a real ` ```mermaid ` fence (not a placeholder). Use `references/generation/mermaid-diagram-picker.md` for the situation-to-type mapping. Reserve placeholders only for photos, screenshots, custom illustrations, and UI mockups.

### Prose-craft directives (Options 5 and 8)

When generating content for **Option 5 (Conference / Tech Talk)** or **Option 8 (Design Document / RFC)**, inject these craft rules into the generation pass. These are invisible to the user — they shape the first draft's prose quality before the scoring gate runs.

1. **ABT paragraph rhythm** — structure every substantive paragraph as: [context] AND [context], BUT [complication], THEREFORE [resolution]. Not every paragraph needs all three beats, but the complication-to-resolution movement must be present across every section.
2. **Alternating rhythm** — never write more than 2 consecutive paragraphs of the same type (narrative reflection OR technical detail). Alternate between them. The narrative provides the thread; the technical detail provides the credibility.
3. **Active voice, minimal caveats** — say "we decided" not "it was determined." Cut "might", "could potentially", "it appears that", "in my experience." State findings directly.
4. **Radical specificity** — use the concrete numbers from depth-mining probe D1. Name specific systems, teams, and timelines. "3 of 12 applications exceed $10/GB" beats "several applications have elevated costs." If D1 came back empty, flag `[DATA NEEDED]` — do not backfill with vague claims.
5. **Land on insights** — every reflective paragraph must conclude with a concrete insight or lesson, not just a narrative beat. "We tried X" is not a paragraph ending; "We tried X, which taught us Y" is.
6. **Layered depth** — for Option 8, structure sections so readers can self-select depth: section heading conveys the key point, first paragraph gives the 30-second summary, subsequent paragraphs add implementation detail. A reader skimming only first paragraphs should understand the full design.
7. **Connect to business value** — bridge technical work to audience stakes using the material from depth-mining probe D3. Frame the inaction scenario when available: "Without this migration, latency exceeds SLA by Q3."

### Mid-generation checkpoint

After generating slides 1–4 (typically: title, executive summary / hook, first 1–2 content slides), **pause and present them to the user** before continuing. This catches structural misalignment early instead of discovering it at the scoring gate after 15 slides.

Present the checkpoint as:

```
## Mid-generation checkpoint (slides 1–4)

[Show the generated Marp markdown for slides 1–4]

**Structure check:**
- Opening move: [describe — e.g., "conclusion-first per McKinsey" or "hook → tension per conference"]
- Tone register: [e.g., "formal/executive" or "technical/peer"]
- Evidence density: [e.g., "2 sourced claims, 1 placeholder"]

Does this direction look right? (continue / adjust / pivot framework)
```

- **"continue"** — proceed with remaining slides.
- **"adjust"** — user gives feedback; revise slides 1–4 and re-present.
- **"pivot framework"** — user realises the framework choice was wrong; return to routing and re-select. This is cheaper than scoring a full deck at 40/100 and refining twice.

### Mid-generation prose refinement (Options 5 and 8 only)

After generating the **full first draft** (all sections / slides complete), run a mechanical prose-quality check **before** the scoring gate. This is Option B — a dedicated refinement pass that catches craft issues the scoring rubric measures but cannot fix surgically.

**Trigger:** Fires only for Option 5 (Conference / Tech Talk) and Option 8 (Design Document / RFC), where prose craft materially affects quality. Options 1–4, 6–7 skip this step — their content is bullet-heavy and the scoring rubric + refine loop is sufficient.

**Procedure — scan then rewrite:**

1. **Hedging scan** — flag paragraphs containing: "it was determined", "in my experience", "it's hard to say", "could potentially", "might be", "it appears that", "to some extent". Rewrite each to direct voice.

2. **ABT rhythm check** — for each section, verify at least one paragraph contains a clear complication→resolution beat. Flag sections that are pure description with no tension. Inject a "BUT" beat where the source material supports one.

3. **Alternating rhythm check** — flag any sequence of 3+ consecutive paragraphs of the same type (all narrative or all technical). Break the sequence by injecting a paragraph of the other type — a concrete metric after narrative, or a reflective transition after technical detail.

4. **Insight landing check** — flag reflective paragraphs that end on narrative beats without a concrete insight ("We tried X." → should be "We tried X, which revealed Y."). Append the missing insight from source material or from depth-mining probes.

5. **Specificity check** — flag sentences that use vague quantifiers ("significant", "several", "many", "substantial") where depth-mining probe D1 provided concrete numbers. Replace with the specific number. If no number exists, replace with `[DATA NEEDED]`.

6. **Layered depth check** (Option 8 only) — verify each section's first paragraph is a self-contained summary. A reader skimming only first paragraphs should understand the full design. If a first paragraph dives straight into detail, prepend a 1–2 sentence summary.

**Output:** The refined draft replaces the original in the working file. Log which fixes were applied and how many in the working notes block under `prose_refinement:`. Then proceed to the scoring gate.

**Cost:** +1 LLM self-review pass. This is deliberate — we prefer quality over speed.

### Image sourcing

Before generating, check for diagrams the user (or an earlier skill session) has already rendered:

1. `.claude/skills/excalidraw-diagram/workspace/` — excalidraw PNGs
2. `.claude/skills/mermaid-diagram/workspace/` — mermaid PNGs
3. Any user-specified directory

List what you find and confirm with the user which images to embed before writing the deck. This avoids regenerating diagrams the user already has.

### Optional: A/B variant generation

For ambiguous routing (e.g., a steering committee about a funding decision — is this a Pitch Deck or a Steering Pack?), offer to build both variants so the user can compare. Two genuinely different structures, not minor tweaks — different frameworks, different opening moves, different title discipline. The comparison is often faster than a 3rd round of interview questions.

---

## Scoring Gate (last step before delivery)

Before delivering the output, self-evaluate against the **layered rubric** in `references/generation/scoring-rubric.md`:

### Rubric architecture — base + overlay (total always 100)

| Layer | What it measures | Points |
|---|---|---|
| **Universal base (B1–B7)** | Structural compliance, MECE, audience alignment, evidence, technical depth, narrative flow, constraints | 65 |
| **Slide overlay (S1–S4)** — Options 1–7 | Action/declarative titles, one-message-per-slide, Marp syntax, slide constraints | 35 |
| **Prose overlay (P1–P4)** — Option 8 (or Option 5 docx) | Section headings, paragraph discipline, specificity & depth, prose syntax | 35 |

**Routing:** use `output_intent` for Option 5 and load base + the matching overlay.

For **Option 5**, determine `output_intent` **before** scoring:
- If the prompt or Q5 constraints already specify docx, set `output_intent = "docx"`.
- If unspecified, ask one quick pre-scoring question: `Should I score this as slides or as a prose docx?`.
- If still unanswered, default to `output_intent = "slides"`.

Use: `output_class = "prose" if framework == 8 else "prose" if framework == 5 and output_intent == "docx" else "slides"`.

### Hard gate (separate from 100-point total)

| Output class | Gate | What it checks |
|---|---|---|
| **Slides** | Visual variety | images ≥ ceil(slides/3), ≥1 diagram fence, ≥2 distinct directives |
| **Prose** | Document quality | word count ≥ 800, sections ≥ 4, evidence density ≥ 3, heading hierarchy valid, specificity floor |

### Pipeline for prose (Options 5 docx + 8)

For prose output, the pipeline adds a **mid-generation prose refinement** step between generation and scoring (see §Mid-generation prose refinement above). The full pipeline is:

1. Generate first draft (all sections)
2. **Prose refinement pass** — hedging scan, ABT check, alternating rhythm, insight landing, specificity, layered depth
3. Scoring gate (base B1–B7 + prose overlay P1–P4)
4. Hard gate (document quality)
5. Auto-refine loop if needed (up to 2 iterations)
6. Delivery

### Thresholds (same for both output classes)

- **≥75** — Deliver to user.
- **60–74** — Auto-refine once, re-score, deliver.
- **<60** — Auto-refine once, re-score; if still <60, refine again; then deliver with an explicit caveat listing low-scoring criteria. Cap refinements at 2 total iterations.

Full rubric, scoring guides, hard gate mechanics, and auto-refine procedure in `references/generation/scoring-rubric.md`.

---

## Delivery — slug + format prompt (topic folder anchored in T0)

After the scoring gate passes, use the topic folder captured in T0 (ask only if the user wants to override it):

1. Derive a slug from the deck title (e.g. `ai-personal-assistant-talk` from "Building Your Own AI Personal Assistant").
2. Confirm the T0 topic folder (or ask for override).
3. Create `pete-pa/topics/<topic-folder>/story-outputs/<slug>/` and an `assets/` subdirectory inside it.
4. All outputs go into that folder: `<slug>.md` (canonical Marp source), `<slug>.html`, `<slug>.pptx` (native PPTX), `<slug>.docx` (flowing DOCX), `assets/` (pre-rendered SVGs).
5. Persist `<slug>.md` first and ask the user to review content before any image-level verification. Rendering and visual checks happen only after this review checkpoint.

Then ask for format:

```
Which format(s) do you want delivered? (html / interactive / pptx / docx / executive-html / all)
```

- **html** — Rich Marp presentation with pre-rendered SVG diagrams
- **interactive** — Rich HTML with slide transitions, progressive builds, client-side mermaid diagrams, code highlighting, and presenter mode (P key)
- **pptx** — Native PowerPoint with positioned layouts and themed shapes (via `story-present-render-pptx-native`). When PPTX is selected, ask: *"Which visual palette? Options: midnight (dark blue), charcoal (warm grey), ocean (navy/teal), midnight-exec (navy/purple), coral-energy (terracotta/orange), warm-terracotta (earthy), ocean-gradient (teal/cyan), or 'infer from audience' (default)."* Pass via `--palette <name>`. If 'infer', omit `--palette` and let the theme→palette map decide.
- **docx** — Flowing Word document adapted for reading, not slide-shaped blocks (via `story-present-render-docx`, uses the prose adapter before pandoc)
- **executive-html** — Premium single-page dark-luxury reading artifact using the obsidian design system. Agent loads `references/rendering/executive-html-tokens.md` and `executive-html-components.md`, consults `executive-html-component-map.md` for content-to-component mapping, and produces a single self-contained `.html` file. Scored against base + E1–E4 overlay + executive HTML hard gate.
- **all** — All five formats rendered after the content review checkpoint

**Key rules:**
- The Marp `.md` is always written as the canonical intermediate regardless of format choice.
- **Pre-render charts first** via `story-present-prerender-chart --input <raw.md> --output <dir> --assets-dir <assets>`. This produces SVGs + PNGs and a rewritten `.md` with `![w:700 contain]` image refs.
- **Then pre-render mermaid** via `story-present-prerender-mermaid --input <chart-rewritten.md> --output <dir> --engine mmdc --assets-dir <assets>`. This produces SVGs + PNGs and rewrites remaining mermaid fences.
- **Mermaid engine fallback (Edge workaround):** On corporate machines where Puppeteer's bundled Chrome is blocked (AppLocker), the rendering pipeline auto-falls back to `engine=playwright` which uses `src/output_format/playwright_mermaid.py`. That module tries system Edge (`msedge` channel) first, then Chrome, then Playwright-bundled Chromium. The `--engine playwright` flag also works explicitly: `story-present-prerender-mermaid --input <md> --output <dir> --engine playwright --assets-dir <assets>`. The auto-fallback happens inside `_select_mermaid_engine()` in `tools/rendering/run.py` — callers (html/pptx/docx/verify-visual renderers) do not need to specify the engine manually.
- **All renderers consume the fully pre-rendered `.md`**, not the raw source. HTML uses SVGs; PPTX/DOCX auto-select PNG siblings (`_add_picture_safe` and docx SVG→PNG swap).

| Step | CLI shortcut | Notes |
|------|-------------|-------|
| Pre-render charts | `story-present-prerender-chart --input <raw.md> --output <dir> --assets-dir <assets>` | Run first; produces SVGs + PNGs |
| Pre-render mermaid | `story-present-prerender-mermaid --input <chart-rewritten.md> --output <dir> --engine mmdc --assets-dir <assets>` | Run second; consumes chart-rewritten markdown |

| Format | CLI shortcut | Input |
|--------|--------------|-------|
| html | `story-present-render-html --input <pre-rendered.md> --output <path> --theme <name>` | Pre-rendered (SVG refs) |
| interactive | `story-present-render-interactive --input <md> --output <path> --theme <name>` | Raw source (client-side mermaid) |
| pptx | `story-present-render-pptx-native --input <pre-rendered.md> --output <path> --theme <name> [--palette <name>]` | Pre-rendered (auto PNG) |
| docx | `story-present-render-docx --input <pre-rendered.md> --output <path> --theme <name>` | Pre-rendered (auto PNG) |

**PPTX quality gate (new):** Immediately after rendering PPTX and before human visual QA, run:
`story-present-qa-pptx-visual --input <deck>.pptx`.
This checks three common regressions automatically: low effective DPI (blurry diagrams), image upscaling,
and image placement issues (overflow/edge-touch). Use `--strict` to fail on edge-touch warnings.

**Post-review visual verification (DEFERRED, mandatory for final QA):** After content is persisted and user-reviewed, run `story-present-verify-visual --input <pre-rendered.md> --output-dir <slug>/verify --theme <name>`.

- Immediately before visual verification, prompt the user: `Switch to a vision-capable model now for visual QA?`
- Verify **every slide that contains any image asset** (mermaid/chart SVG renders, PNG assets, excalidraw PNGs, photos, screenshots). Do not sample.
- If the current model cannot inspect images, pause and ask for model switch before continuing visual QA.
- If switching is unavailable or declined, keep status as `visual-review-pending` and do not mark final QA complete.
- Mark final output status explicitly as either `visually-verified` or `visual-review-pending`.

### Excalidraw diagram generation

After the review checkpoint and render step, generate excalidraw diagrams for appendix placeholders:

1. Parse the appendix to find `excalidraw-diagram` entries
2. For each entry, read `references/visual/excalidraw/excalidraw-generation.md` and follow the generation loop
3. Render each `.excalidraw` to PNG via `story-present-render-excalidraw --input <path> --output <path>`
4. Verify each PNG: no text overflow, no overlapping elements, arrows land correctly, readable at slide size
5. If image inspection is unavailable in the current model, prompt user to switch models before continuing
6. If switching is unavailable or declined, present generated PNG paths for human review and mark the run `visual-review-pending`
7. If verification fails, fix and re-render (max 2 iterations per image)
8. Present all generated images to the user for approval
9. Replace `placeholder://visual-needed` URLs with actual image paths and remove replaced appendix entries

---

## Reference file index

| File | Purpose |
|------|---------|
| `references/generation/marp-conventions.md` | Marp syntax, separators, directives, placeholders, RAG emoji, speaker notes |
| `references/interview/intake-defaults.md` | Safe defaults for every L1 and L2 question |
| `references/generation/scoring-rubric.md` | Layered rubric (base 65 + overlay 35 = 100), hard gates, auto-refine loop |
| `references/templates/template-pyramid.md` | Option 1 — 12-slide McKinsey Pyramid sequence |
| `references/interview/level2-consulting.md` | L2 for Options 1, 2, 3, 4 |
| `references/templates/template-storyline-market.md` | Option 2 — 12 slides |
| `references/templates/template-storyline-problem.md` | Option 3 — 13 slides |
| `references/templates/template-storyline-roadmap.md` | Option 4 — 6 slides |
| `references/interview/level2-conference.md` | L2 for Option 5 |
| `references/templates/template-conference.md` | Option 5 — 15 slides, layout rotation, speaker notes |
| `references/interview/level2-raid-status.md` | L2 for Options 6, 7 |
| `references/templates/template-raid-status.md` | Option 6 — 5 slides, RAG indicators |
| `references/templates/template-steering.md` | Option 7 — 10 slides, decision-first |
| `references/interview/level2-designdoc.md` | L2 for Option 8 |
| `references/templates/template-designdoc.md` | Option 8 — flowing document, problem → design → alternatives → tradeoffs |
| `references/generation/source-ingestion.md` | Source ingestion CLI orchestration and working-notes format |
| `references/rendering/rendering-html.md` | marp-cli invocation, theme CSS |
| `references/rendering/rendering-pptx.md` | python-pptx engine, AST parsing, chart placeholders |
| `references/rendering/rendering-docx.md` | pandoc pipeline, reference.docx styles |
| `references/visual/visual-design-principles.md` | 10 design rules + typography table (ex-ppt-create) |
| `references/visual/palettes.md` | 12 named palettes with hex values (ex-ppt-create) |
| `references/visual/slide-types-pptx.md` | 9 pptx slide types with pixel positions (ex-ppt-create) |
| `references/generation/writing-style.md` | Title/bullet/prose rules incl. 8-word title limit (ex-ppt-create) |
| `references/generation/marp-image-cookbook.md` | 9 Marp image-directive recipes with when-to-use guidance (bg, cover, split, filters, contain, drop-shadow) |
| `references/generation/mermaid-diagram-picker.md` | Situation → Mermaid diagram-type table (flowchart, sequence, ER, timeline, quadrant, C4, architecture-beta, etc.) |
| `references/generation/image-ingestion.md` | Image-first directory scan, outline adaptation rules, empty-dir fallback |
| `references/generation/technical-depth-mining.md` | Technical depth extraction procedure — trigger conditions, 5 categories, ranking, slide mapping, diagram flagging |
| `references/visual/excalidraw/excalidraw-generation.md` | Excalidraw JSON generation process (progressive disclosure) |
| `references/visual/excalidraw/color-palette.md` | Excalidraw semantic color palette |
| `references/visual/excalidraw/element-templates.md` | Copy-paste JSON element templates |
| `references/visual/excalidraw/json-schema.md` | Excalidraw element type reference |
| `references/rendering/cli-tools.md` | Full CLI tool reference — flags, inputs, outputs, pipeline order, porting guide |
| `references/rendering/executive-html-tokens.md` | Obsidian design tokens (CSS custom properties, dark/light themes, typography scale) — vendored from obsidian-executive-html |
| `references/rendering/executive-html-components.md` | Obsidian component library (hero, cards, tiles, metrics, tables, callouts, quotes, tags, nav, accordions, timelines, diagrams, animations, breakpoints, toggle, anti-patterns) — vendored from obsidian-executive-html |
| `references/rendering/executive-html-template.html` | Working reference HTML template implementing the full obsidian design system — vendored from obsidian-executive-html |
| `references/rendering/executive-html-component-map.md` | Content-to-component mapping heuristic for E2 scoring — which markdown patterns map to which obsidian components |
