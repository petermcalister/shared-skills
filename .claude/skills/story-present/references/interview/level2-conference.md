# Level 2 Interview — Conference / Tech Talk (Option 5)

Loaded by SKILL.md when the Level 1 routing matrix picks Option 5 (Conference / Tech Talk). Contains the five framework-specific questions L2-T1..L2-T5 asked after Level 1 is confirmed and source ingestion (if any) has completed.

**Source**: PRD Section 5 (Level 2 for Option 5, verbatim). Adapted from community frontend-slides purpose detection (pitch / teaching / conference / internal) and community Marp layout rotation patterns. The narrative-arc question (L2-T4) borrows the journey / teaching / research split from community purpose detection research.

Same safe-default rule as Level 1 — after 2 unanswered prompts on any question, apply the safe default from `references/interview/intake-defaults.md` and move on. Track applied defaults in the working-notes block so the Understanding Check can surface them before generation.

---

## Questions — L2-T1..L2-T5

Ask one at a time, conversationally, in order. Do not batch.

| # | Question | Safe Default |
|---|----------|-------------|
| L2-T1 | "What type of talk? (keynote, lightning talk, workshop, panel, tutorial)" | Standard conference talk |
| L2-T2 | "What is the talk duration and any slide count guidance from the conference?" | 30 minutes, no limit |
| L2-T3 | "Will you include live demos, code examples, or interactive elements?" | No demos |
| L2-T4 | "What is the narrative arc — are you telling a journey (problem → discovery → solution), teaching a skill, or presenting research findings?" | Problem → discovery → solution |
| L2-T5 | "Do you want speaker notes generated alongside the slides?" | Yes |

---

## How each answer feeds the template

The answers shape how `references/templates/template-conference.md` is populated:

| Answer | Drives |
|--------|--------|
| **L2-T1** talk type | Overall tone and length calibration. Lightning talks compress to ~6 slides; keynotes extend to ~20. Default 15-slide sequence targets a 30-minute conference talk. |
| **L2-T2** duration + slide count | Final slide count. Rule of thumb: 1 slide per 2 minutes for a conference talk. If the conference hard-caps slide count, the template compresses per its compression rules. |
| **L2-T3** demos / code | Whether slide 8 (Demo) is included or dropped, and whether Section 2 / Section 3 use code-block layouts in the rotation. If "no demos", slide 8 becomes an additional Section 2 detail slide. |
| **L2-T4** narrative arc | Section ordering inside the 15-slide sequence. Journey = problem → discovery → solution (the default). Teaching = concept → example → exercise → recap. Research = question → method → findings → implications. All three route into the same 15-slide skeleton but re-label Sections 1–4. |
| **L2-T5** speaker notes | Whether speaker notes are generated. Default is **yes** and the conference template treats speaker notes as mandatory per PRD Section 6 Option 5. The question exists only so the user can opt out explicitly. |

---

## Narrative arc → section labels

Per the L2-T4 answer, the four section slots in the template (Sections 1–4) are labelled differently but keep the same 15-slide skeleton:

| Arc | Section 1 | Section 2 | Section 3 | Section 4 |
|-----|-----------|-----------|-----------|-----------|
| **Journey** (default) | Context / background | Discovery / turning point | Deep dive into the solution | Practical application |
| **Teaching** | Concept introduction | Worked example | Common pitfalls / deep dive | Exercise / how to apply |
| **Research** | Research question | Method / approach | Findings | Implications / future work |

The agenda slide (slide 3) uses the labels from the chosen arc, and every subsequent content slide's breadcrumb reflects those labels.

---

## Flow summary

1. Ask L2-T1 through L2-T5 one at a time, applying defaults after 2 silent prompts per question.
2. Map L2-T4 onto one of the three section label sets above.
3. Surface any applied defaults in the working-notes block so the user can see them before generation.
4. Proceed to `references/templates/template-conference.md` and walk the 15-slide sequence.
