# Template — Option 6: RAID Log / Weekly Status Update

**Source**: Novel — no existing SKILL.md covers this. Structural patterns derived from Tactical Project Manager's 5-slide weekly status template, Expert Programme Management's RAID definitions (Risks / Assumptions / Issues / Dependencies), BestOutcome portfolio RAG practice, and standard PMO reporting conventions.

**Use when**: Level 1 routing lands on Option 4 — the audience is a delivery team, immediate manager, or project sponsor expecting a fast status read rather than a governance decision.

---

## Structural rules

- **Use action titles, not topic labels.** Every slide title is a complete sentence stating status.
  - Topic label (do not use): `Schedule Update`
  - Action title (use): `Schedule is on track for June delivery`
- **RAG indicators are mandatory.** Use the emoji 🟢 🟡 🔴 directly in the markdown — Marp renders these natively and they survive PPTX/DOCX conversion.
- **Filter the RAID register.** Do **not** dump the full register. Show only the top 5–8 escalation-worthy items filtered by impact and status change since last report.
- **One message per slide.** If you need two statuses, use two slides.
- **Consistent structure across weeks.** The same 5 slides in the same order every week so the audience learns where to look.

## RAG standard

| Emoji | Meaning | When to use |
|-------|---------|-------------|
| 🟢 | **Green — on track** | Dimension is progressing to plan. No intervention required. |
| 🟡 | **Amber — at risk** | Mitigation plan in place or needed. Monitoring closely. |
| 🔴 | **Red — critical** | Requires immediate attention or escalation to a higher authority. |

Every RAG dot on the deck must resolve to one of those three states. No blues, no grey, no "TBD" — if you cannot assign a colour, the slide isn't ready.

## RAID category codes

| Code | Category | Definition |
|------|----------|------------|
| **R** | Risk | Uncertain future event that could harm the project if it occurs |
| **A** | Assumption | A belief held to be true that, if invalidated, becomes a risk |
| **I** | Issue | A problem that has already materialised and needs resolution |
| **D** | Dependency | An external item the project relies on (another team, vendor, decision) |

---

## Slide sequence (5 slides)

| # | Slide | Purpose | Content structure |
|---|-------|---------|-------------------|
| 1 | **Title + Overall Health** | Orient the audience and give the headline RAG in one glance | Project name · report date · overall RAG emoji · one-line headline action title (e.g. "Programme remains 🟢 — on track for June delivery") · `<!-- _class: lead -->` |
| 2 | **Project Snapshot** | RAG dashboard grid across all status dimensions | Table with dimension rows. **MUST** also contain a chart skeleton — see **Slide 2 visual mandate** below |
| 3 | **RAID Summary** | The escalation-worthy items from the RAID register | Table with columns **ID, Category, Description, Impact, Owner, Status, RAG**. Max 5–8 rows. Sort by RAG (🔴 first) then impact |
| 4 | **Milestones & Timeline** | Where we are on the plan | Three groups: ✅ Completed (last 2) · 🔵 Current (in-flight) · ⏭️ Upcoming (next 3 with dates) |
| 5 | **Next Steps & Decisions** | What happens now and any escalations needed | Action items with owner + due date. Any decision required from this audience. "No decisions required" is a valid outcome for Option 4 |

---

## Slide-by-slide content templates

### Slide 1 — Title + Overall Health

```markdown
<!-- _class: lead -->

# Programme Atlas is 🟢 on track for June delivery

**Weekly status update — Week 15**
Report date: 2026-04-11 · Owner: Pete McAllister

<!-- Speaker notes: Open with the headline RAG. If the overall colour has changed since last week, call out the change explicitly. -->
```

The title is an action title stating status. The overall RAG emoji appears inline so it renders at the top of the slide before any other content.

### Slide 2 — Project Snapshot

```markdown
# Snapshot: 🟢 overall, 🟡 resources, everything else green

| Dimension | RAG | Status |
|-----------|-----|--------|
| Overall | 🟢 | On track for June delivery |
| Schedule | 🟢 | All milestones on plan |
| Budget | 🟢 | 42% spent of £180k; forecast within £5k of plan |
| Scope | 🟢 | No change requests this week |
| Resources | 🟡 | Contractor onboarding slipped by 1 week |
| Risk | 🟢 | No new risks; top risk mitigated |

<!-- Speaker notes: Walk the table top to bottom. Pause on any 🟡 or 🔴 to explain the mitigation. -->
```

Every row has a colour. Every colour has a one-line justification. The title restates the table's headline so someone scanning the deck catches it.

#### Slide 2 visual mandate (project snapshot)

In addition to the RAG table, slide 2 MUST contain a chart fence skeleton representing the dashboard dimensions as a horizontal bar:

````markdown
```chart
{type: bar, data: {labels: ["Overall","Schedule","Budget","Scope","Resources","Risk"], values: [3,3,3,3,2,3]}, title: "RAG Dashboard (3=Green, 2=Amber, 1=Red)"}
```
````

Values MUST be inferred from the actual RAG statuses: 3 for green, 2 for amber, 1 for red.

### Slide 3 — RAID Summary

```markdown
# Three RAID items require attention this week

| ID | Cat | Description | Impact | Owner | Status | RAG |
|----|-----|-------------|--------|-------|--------|-----|
| R-17 | R | Vendor X may miss integration window | H | Pete | Mitigation in progress | 🟡 |
| I-04 | I | Staging environment outage blocking QA | H | Ops | Resolved today | 🟢 |
| D-09 | D | Awaiting security sign-off from Infosec | M | Laura | On track for Fri | 🟢 |

<!-- Speaker notes: Only show items that changed status this week or are 🔴. Do not dump the full RAID register — that lives in the appendix or the register tool. -->
```

**Column definition (mandatory):** `ID, Category, Description, Impact, Owner, Status, RAG`. The scenario `RAID table has the required columns` asserts this exact header.

Filter rules:
- **Maximum 5–8 rows.** Beyond that the audience stops reading.
- **Escalation-worthy only.** Include items that (a) are 🔴 or 🟡, or (b) changed RAG since last report, or (c) are 🟢 but previously escalated and need closure.
- **Sort order:** 🔴 first, then 🟡, then 🟢 closures, then by Impact (H > M > L).
- **Impact** is H / M / L. If you need more granularity you are writing a steering pack (Option 5), not a weekly status.

### Slide 4 — Milestones & Timeline

```markdown
# Three milestones completed, two in flight, database cutover next

**✅ Completed (last 2 weeks)**
- 2026-04-04 — API v2 deployed to staging
- 2026-04-08 — Security review passed

**🔵 Current (in flight)**
- Frontend redesign — Laura — due 2026-04-18
- Contractor onboarding — Ops — due 2026-04-15

**⏭️ Upcoming (next 3)**
- 2026-04-22 — Database cutover
- 2026-05-01 — UAT kick-off
- 2026-06-14 — Go-live

<!-- Speaker notes: This is where a picture is worth more than a table — consider a Gantt-style visual when generating for HTML/PPTX. -->
```

### Slide 5 — Next Steps & Decisions

```markdown
# Next steps are owned; no decisions required from this audience

**Actions this week**
| Action | Owner | Due |
|--------|-------|-----|
| Finalise contractor onboarding | Ops | 2026-04-15 |
| Sign off staging QA | Laura | 2026-04-16 |
| Submit database cutover runbook | Pete | 2026-04-18 |

**Decisions requested from this audience**
None — informational update only.

<!-- Speaker notes: If the answer to "decisions" is anything other than None, the update has outgrown Option 4 and should be regenerated as Option 5 (Steering Committee). -->
```

If the team answers L2-S6 with an actual decision, the skill should prompt: "You've identified a decision — would you like to regenerate this as a Steering Committee deck (Option 5) instead?" and auto-upgrade on confirmation.

---

## Arc pattern

`Headline RAG → Snapshot → RAID → Timeline → Next steps`

Read just the titles and you should understand the week: "Programme is 🟢 on track → Snapshot shows 🟡 resources → Three RAID items need attention → Milestones on plan → Next steps owned, no decisions needed."

## What this template deliberately omits

- **Per-dimension deep dives.** That's Option 5's job.
- **Budget variance tables.** Option 4 gets a single budget RAG in the snapshot; the steering pack gets the full variance view.
- **Financial forecasts.** Same reason.
- **Workstream sub-slides.** Option 4 assumes 1 workstream (L2-S3 default). Multi-workstream reporting belongs in Option 5.
- **Dependency maps across programmes.** Option 5's slide 8.

If the user needs any of these, the routing should send them to Option 5 instead.
