# Intake Defaults

Safe default values for every Level 1 and Level 2 interview question. If the user does not answer a question after 2 prompts, apply the default and move on. Log which defaults were applied so the Understanding Check can surface them.

Defaults are copied verbatim from PRD Sections 4 and 5.

---

## Level 1 — Universal (PRD Section 4)

| # | Question | Safe Default |
|---|----------|-------------|
| T0 | Topic folder anchor under `pete-pa/topics/` | Derive `<topic-folder>` from Q1 topic slug and confirm in Understanding Check |
| Q1 | Topic and outcome | Use whatever topic context is available |
| Q2 | Audience | General professional audience — **probe first:** "What do they already know, and what's their stake?" |
| Q3 | Key points / outline | Derive from Q1 topic — **always probe:** "What's explicitly NOT in scope?" |
| Q4 | Primary goal (persuading / informing / deciding) | Informing — **probe first if ambiguous:** "If the meeting goes perfectly, what happens next?" |
| Q5 | Constraints (slide count, time, must-include, must-avoid) | 12–15 slides, 15–20 minutes, no constraints |
| Q6 | Source material | (h) None — use only interview answers |

When Q4 defaults to Informing and Q2 defaults to "general professional audience", the routing matrix lands on **Option 1 (McKinsey Pyramid Principle)** as the default framework — the "Informing + general/mixed/unknown" row.

---

## Depth-mining probes (D1–D3, after Q4)

These three probes fire for **all 8 frameworks** between Q4 and Q5. They extract specific, honest, business-connected raw material that dramatically improves generation quality. If unanswered, log the gap — do not default-fill with vague claims.

| # | Probe | Safe Default |
|---|-------|-------------|
| D1 | "What specific numbers can you share — before/after, %, timelines, costs?" | Log `[EVIDENCE GAP: D1]` in working notes — no vague backfill |
| D2 | "What was the catalyst that forced change? What didn't work first?" | Log `[EVIDENCE GAP: D2]` — if genuinely new initiative, log "no prior state" |
| D3 | "What business outcome does this enable? What happens if they do nothing?" | Log `[EVIDENCE GAP: D3]` — no vague backfill |

---

## Level 2 — Consulting frameworks (Options 1, 2, 3, 4)

Base questions from PRD Section 5. Stored here and used by `references/interview/level2-consulting.md` (batch 2).

### Base questions L2-C1..C6

| # | Question | Safe Default |
|---|----------|-------------|
| L2-C1 | Core conclusion / recommendation | Derive from Level 1 Q1 |
| L2-C2 | Specific decision or action wanted from audience | "Agree to move to next step" |
| L2-C3 | Tone and style | Professional, clear, balanced |
| L2-C4 | 3–5 strongest supporting arguments / evidence | Derive from Level 1 Q3 |
| L2-C5 | Must-include data / charts / tables; topics to avoid | None; generate placeholders |
| L2-C6 | Scope boundary (in scope / out of scope) | Topic + 1 layer of related context |

### Option 2 additions — Market Strategy L2-M1..M3

| # | Question | Safe Default |
|---|----------|-------------|
| L2-M1 | TAM size and growth rate | "[To be researched]" placeholder |
| L2-M2 | Top 3 competitors and differentiation | Placeholder |
| L2-M3 | Pricing model and average contract value | Placeholder |

### Option 3 additions — Problem-Solving L2-P1..P3

| # | Question | Safe Default |
|---|----------|-------------|
| L2-P1 | Current state vs target state, quantify the gap | Qualitative description |
| L2-P2 | 2–4 contributing factors / root causes | Derive from Q3 |
| L2-P3 | For each solution option: impact, investment, timeline | Placeholder table |

### Option 4 additions — Roadmap L2-R1..R3

| # | Question | Safe Default |
|---|----------|-------------|
| L2-R1 | Measurable objective this roadmap delivers | Derive from Q1 |
| L2-R2 | Number of phases and total duration in weeks | 4 phases, 12 weeks |
| L2-R3 | Key team roles and resource gaps | PM, Design, Engineering |

---

## Level 2 — Option 5 Conference / Tech Talk L2-T1..T5

| # | Question | Safe Default |
|---|----------|-------------|
| L2-T1 | Type of talk (keynote / lightning / workshop / panel / tutorial) | Standard conference talk |
| L2-T2 | Talk duration and slide count guidance | 30 minutes, no limit |
| L2-T3 | Live demos / code examples / interactive elements | No demos |
| L2-T4 | Narrative arc (journey / teaching / research) | Problem → discovery → solution |
| L2-T5 | Speaker notes alongside slides | Yes |

---

## Level 2 — Options 6 and 7 RAID / Steering L2-S1..S7

Defaults differ between Option 6 (weekly team) and Option 7 (steering committee) per PRD Section 5.

| # | Question | Default (Option 6) | Default (Option 7) |
|---|----------|-------------------|--------------------|
| L2-S1 | Active RAID categories | All four (RAID) | All four (RAID) |
| L2-S2 | Governance level | Weekly team update | Steering committee |
| L2-S3 | Number of workstreams / projects | 1 | 1 |
| L2-S4 | RAG per dimension or overall only | Overall only | Per-dimension |
| L2-S5 | Financial data (budget vs actual, burn, forecast) | None | Budget vs actual |
| L2-S6 | Decisions / escalations needed from meeting | None (informational) | Explicit decision slide |
| L2-S7 | Existing RAID register / data file / previous report | No — generate from scratch | No — generate from scratch |

---

## Default application policy

1. Ask each question once.
2. **For routing-critical questions (Q2, Q3, Q4):** if the answer is vague or missing, ask the probing follow-up from SKILL.md before applying a default. Only default after the probe is also unanswered. These three questions drive framework selection and scope — bad defaults here cascade into bad decks.
3. **For other questions (Q1, Q5, Q6, all L2):** if silent, re-prompt once with a brief clarification. After 2 unanswered prompts, apply the default and move on.
4. Track which defaults were applied in the working notes block.
5. Surface all applied defaults in the Understanding Check so the user sees them before generation.
6. The user can override any applied default by replying "adjust" at the Understanding Check.

---

## Level 2 — Option 8 Design Document / RFC L2-D1..D6

| # | Question | Safe Default |
|---|----------|-------------|
| L2-D1 | Proposed design (architecture, components, interfaces) | Infer from ingested source; flag `[DESIGN NEEDED]` if empty |
| L2-D2 | Alternatives considered + rejection rationale | 2 alternatives inferred from source; flag `[ALTERNATIVES THIN]` |
| L2-D3 | Goals and non-goals | Goals from L1 Q1; non-goals omitted with flag `[NON-GOALS NEEDED]` |
| L2-D4 | Key risks, failure modes, open questions | 1–2 obvious risks from design; flag `[RISKS INCOMPLETE]` |
| L2-D5 | Implementation sequence (phases, dependencies) | Single-phase rollout |
| L2-D6 | Devil's advocate pass before writing | Yes |
