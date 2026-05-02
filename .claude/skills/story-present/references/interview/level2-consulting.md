# Level 2 Interview — Consulting Frameworks (Options 1, 2, 3, 4)

Loaded by SKILL.md when the Level 1 routing matrix picks one of the four consulting frameworks. Contains the **base** questions (L2-C1..C6) asked for **all four** options, plus the **add-on** question sets asked only when the specific option is chosen.

**Source**: PRD Section 5 (verbatim), adapted from community ppt-creator INTAKE.md questionnaire pattern. Same safe-default rule as Level 1 — after 2 unanswered prompts on any question, apply the safe default from `references/interview/intake-defaults.md` and move on.

---

## When to ask which add-on set

The Level 1 routing matrix (PRD Section 4) determines which add-on block to layer on top of the base questions:

| Option chosen at Level 1 | Base L2-C1..C6 | + L2-M1..M3 (market) | + L2-P1..P3 (problem) | + L2-R1..R3 (roadmap) |
|--------------------------|----------------|-----------------------|-----------------------|-----------------------|
| **Option 1 — McKinsey Pyramid** | yes | no | no | no |
| **Option 2 — Market Strategy / Pitch Deck** | yes | **yes** | no | no |
| **Option 3 — Internal Problem-Solving / Issue Tree** | yes | no | **yes** | no |
| **Option 4 — Project Roadmap / Implementation Plan** | yes | no | no | **yes** |

Ask the six base questions first, in order, then append the matching add-on block. Do not ask add-on questions for options they do not apply to.

---

## Base questions — L2-C1..C6

Asked for Options 1, 2, 3, and 4.

| # | Question | Safe Default |
|---|----------|-------------|
| L2-C1 | "What is the core conclusion or recommendation you want the audience to accept?" | Derive from Level 1 Q1 |
| L2-C2 | "What specific decision or action do you want from the audience after this presentation?" | "Agree to move to next step" |
| L2-C3 | "What tone and style? (e.g., data-heavy and formal, narrative and visual, minimal text)" | Professional, clear, balanced |
| L2-C4 | "What are the 3–5 strongest supporting arguments or evidence points for your conclusion?" | Derive from Level 1 Q3 |
| L2-C5 | "Any must-include data, charts, tables, or specific facts? Any topics to explicitly avoid?" | None; generate placeholders |
| L2-C6 | "What is the scope boundary — what is IN scope and what is explicitly OUT of scope?" | Topic + 1 layer of related context |

---

## Option 2 add-on — Market Strategy L2-M1..M3

Ask only when the chosen option is **2 (Market Strategy / Pitch Deck)**.

| # | Question | Safe Default |
|---|----------|-------------|
| L2-M1 | "What is the total addressable market size and growth rate?" | "[To be researched]" placeholder |
| L2-M2 | "Who are the top 3 competitors and what is your differentiation?" | Placeholder |
| L2-M3 | "What is your pricing model and average contract value?" | Placeholder |

These answers feed the Market opportunity, Competitive landscape, Differentiation, and Pricing slides in `references/templates/template-storyline-market.md`.

---

## Option 3 add-on — Problem-Solving L2-P1..P3

Ask only when the chosen option is **3 (Internal Problem-Solving / Issue Tree)**.

| # | Question | Safe Default |
|---|----------|-------------|
| L2-P1 | "What is the current state vs. target state? Quantify the gap if possible." | Qualitative description |
| L2-P2 | "What are the 2–4 contributing factors or root causes you've identified?" | Derive from Q3 |
| L2-P3 | "For each solution option, what is the estimated impact, investment, and timeline?" | Placeholder table |

These answers feed the Problem statement, Contributing factors (×3), Root cause insight, and Solution options slides in `references/templates/template-storyline-problem.md`.

---

## Option 4 add-on — Roadmap L2-R1..R3

Ask only when the chosen option is **4 (Project Roadmap / Implementation Plan)**.

| # | Question | Safe Default |
|---|----------|-------------|
| L2-R1 | "What is the measurable objective this roadmap delivers?" | Derive from Q1 |
| L2-R2 | "How many phases, and what is the total duration in weeks?" | 4 phases, 12 weeks |
| L2-R3 | "What are the key roles on the team, and are there any resource gaps?" | PM, Design, Engineering |

These answers feed the Objective, Approach overview, Detailed roadmap, and Team composition slides in `references/templates/template-storyline-roadmap.md`.

---

## Flow summary

1. Ask L2-C1 through L2-C6 one at a time, applying defaults after 2 silent prompts per question.
2. If the chosen option is 2a, append L2-M1..M3. If 2b, append L2-P1..P3. If 2c, append L2-R1..R3.
3. Surface any applied defaults in the working notes block so the user can see them before generation.
4. Proceed to the matching `references/templates/template-*.md` and walk the slide sequence.
