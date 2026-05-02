# Level 2 Interview — Design Document / RFC (Option 8)

Loaded by SKILL.md when the Level 1 routing matrix picks Option 8 (Design Document / RFC). Contains the six framework-specific questions L2-D1..L2-D6 asked after Level 1 is confirmed and source ingestion (if any) has completed.

**Source**: Adapted from the standalone design-doc skill's Phase 1 extraction flow. The standalone skill runs its own interview + devil's advocate + generation pipeline. This Level 2 captures the same extraction needs within story-present's gated pipeline so that scoring, rendering, and delivery run consistently.

Same safe-default rule as Level 1 — after 2 unanswered prompts on any question, apply the safe default from `references/interview/intake-defaults.md` and move on. Track applied defaults in the working-notes block so the user can see them before generation.

---

## Questions — L2-D1..L2-D6

Ask one at a time, conversationally, in order. Do not batch.

| # | Question | Safe Default |
|---|----------|-------------|
| L2-D1 | "What is the proposed design? Describe the solution — architecture, key components, data model changes, interfaces. Paste from notes if you have them." | Infer from ingested source material; flag `[DESIGN NEEDED]` if nothing available |
| L2-D2 | "What alternatives did you consider? For each, why was it rejected — what specific tradeoff ruled it out?" | Two alternatives inferred from source material with generic tradeoffs; flag `[ALTERNATIVES THIN — strengthen before review]` |
| L2-D3 | "What are the goals and non-goals? What does this design explicitly NOT address?" | Goals inferred from L1 Q1; non-goals omitted with flag `[NON-GOALS NEEDED]` |
| L2-D4 | "What are the key risks, failure modes, or open questions you want reviewers to weigh in on?" | Infer 1–2 obvious risks from design; flag `[RISKS INCOMPLETE]` |
| L2-D5 | "What is the implementation sequence — what ships first, what depends on what, what can be parallelised?" | Single-phase rollout |
| L2-D6 | "Do you want a devil's advocate pass before the document is written? (I'll pressure-test alternatives, failure modes, scale, and complexity cost.)" | Yes |

---

## How each answer feeds the template

| Answer | Drives |
|--------|--------|
| **L2-D1** proposed design | Populates Section 4 (Proposed Design) — the core of the document. If technical detail is rich, multiple subsections are generated with diagrams. |
| **L2-D2** alternatives | Populates Section 5 (Alternatives Considered). Each alternative gets a heading, description, and explicit rejection rationale. Thin alternatives get a scoring-rubric penalty (criterion 6b). |
| **L2-D3** goals / non-goals | Populates Section 3. Non-goals are critical for peer review — they prevent scope creep objections. |
| **L2-D4** risks / open questions | Populates Section 6 (Risks and Open Questions). Each risk gets a mitigation row. Each open question gets an owner/deadline hint. |
| **L2-D5** implementation sequence | Populates Section 7 (Implementation Plan). If multi-phase, a mermaid gantt or flowchart is generated. |
| **L2-D6** devil's advocate | If yes, the agent runs a pressure-test pass (challenge alternatives, failure modes, scale assumptions, complexity cost) before generation. Challenges that reveal genuine weaknesses are folded into the document. |

---

## Devil's advocate pass (if L2-D6 = yes)

Before generation, challenge the design conversationally:

1. **Alternatives**: "You chose X over Y — have you considered Z? What specifically rules out Y?"
2. **Failure modes**: "What happens when [component] is unavailable? What's the blast radius?"
3. **Scale**: "Does this hold at 10x current load? Where does it break first?"
4. **Complexity cost**: "Is there a simpler version that gets 80% of the value?"
5. **Dependencies**: "What changes in other systems does this require?"

Present challenges as "One thing reviewers will probably push on..." not as an interrogation. If a challenge reveals a genuine weakness, help address it in the document.

---

## Format guidance

Option 8 produces a **flowing document**, not a slide deck. The canonical Marp `.md` is still generated (for pipeline consistency), but:

- **Primary output is docx** — rendered via `story-present-render-docx`
- **html is a secondary option** — useful for Confluence paste
- **pptx and interactive are suboptimal** — the agent should flag this and confirm before rendering

The template uses `---` separators for logical sections (not per-slide breaks), and the scoring rubric adapts criterion 3 (one message per slide) to "one theme per section."

---

## Flow summary

1. Ask L2-D1 through L2-D6 one at a time, applying defaults after 2 silent prompts per question.
2. If L2-D6 = yes, run devil's advocate pass and fold improvements.
3. Surface applied defaults and devil's advocate findings in the working-notes block.
4. Proceed to `references/templates/template-designdoc.md` and walk the section sequence.
