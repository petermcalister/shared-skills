# Level 2 Intake — Options 4 and 5 (RAID Log / Steering Committee)

**Applies to:** Option 6 (RAID Log / Weekly Status) and Option 7 (Steering Committee / Board Pack).

These questions are asked after the Level 1 routing recommendation has been confirmed as Option 6 or Option 7. The questions are novel to story-present — no existing SKILL.md covers this territory — and are sourced verbatim from PRD Section 5.

Ask **one question at a time**, conversationally. After 2 unanswered prompts on any question, apply the safe default for that question from the table below and from `references/interview/intake-defaults.md`, then move on. Safe defaults **differ** between Option 6 (weekly team update, informational) and Option 7 (steering committee, decision-oriented). Apply the column that matches the framework the user picked at the end of Level 1.

---

## Questions

| # | Question | Safe Default — Option 6 (weekly team) | Safe Default — Option 7 (steering committee) |
|---|----------|---------------------------------------|----------------------------------------------|
| **L2-S1** | "Which RAID categories are active for this update? (Risks / Assumptions / Issues / Dependencies — select all that apply)" | All four (RAID) | All four (RAID) |
| **L2-S2** | "What governance level is this? (Weekly team update / Monthly programme review / Steering committee / Board pack)" | Weekly team update | Steering committee |
| **L2-S3** | "How many workstreams or projects does this update cover?" | 1 | 1 |
| **L2-S4** | "Do you need RAG ratings per dimension (schedule, budget, scope, resources, risk) or overall only?" | Overall only | Per-dimension (schedule / budget / scope / resources / risk individually) |
| **L2-S5** | "Any financial data to include? (Budget vs. actual, burn rate, forecast)" | None | Budget vs actual (variance required) |
| **L2-S6** | "What decisions or escalations need to come out of this meeting?" | None (informational only) | Explicit decision slide — what approval, funding, or direction is required |
| **L2-S7** | "Do you have an existing RAID register, data file, or previous report to reference? If so, where is it?" | No — generate from scratch | No — generate from scratch |

---

## Why the defaults diverge

The PRD distinguishes the two governance contexts:

- **Option 6 (weekly team update)** is **informational**. The audience is the delivery team or an immediate manager. They want a fast status read, one RAG, a trimmed RAID register, and the next 3 milestones. No decisions are expected, no financial variance is required, and workstream detail is usually kept to one because most weekly reports cover a single project.

- **Option 7 (steering committee / board pack)** is **decisional**. The audience is a governance body that must approve, fund, or redirect. The PRD requires per-dimension RAG (schedule / budget / scope / resources / risk rated individually, not a single overall colour), an explicit budget-vs-actual variance view, and a dedicated decision slide at position 3 (not 9) so the ask survives any time compression in the meeting.

When a user routes to Option 6 but answers L2-S6 with an actual escalation, the skill should **auto-upgrade to Option 7** and re-ask the divergent questions (L2-S4 per-dimension, L2-S5 variance) — a team update that needs a decision has outgrown Option 6's 5-slide structure.

---

## Working notes capture

Capture each answer into the working-notes block under a `raid_status:` key:

```yaml
raid_status:
  categories: [R, A, I, D]
  governance_level: steering_committee   # or weekly_team | monthly_programme | board
  workstreams: 1
  rag_mode: per_dimension                # or overall
  financials:
    budget_vs_actual: true
    burn_rate: optional
    forecast: optional
  decisions:
    - ask: "Approve €200k additional budget for vendor change"
      cost_implication: "€200k one-off"
      timeline_implication: "+2 weeks slip avoided"
  raid_register_source: none             # or path/url
```

Evidence cited on the generated slides should link back to the ingested source (memory event ID, email subject, report path) per the Level 1 Q6 ingestion step.

---

## After Level 2

Once L2-S1..S7 are answered (or safely defaulted), load the matching template:
- Option 6 → `references/templates/template-raid-status.md`
- Option 7 → `references/templates/template-steering.md`

Walk the slide sequence and populate each slide using the Level 2 answers plus the working-notes block from Level 1 Q6 ingestion.
