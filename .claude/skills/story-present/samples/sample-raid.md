---
marp: true
theme: status
paginate: true
---

<!-- _class: lead -->

# Programme Atlas is 🟡 at risk on schedule due to vendor delays

Weekly status · Week 15 · 2026-04-11 · Pete McAlister

---

# Programme snapshot shows schedule amber but everything else is green

| Dimension | RAG | Status |
|-----------|-----|--------|
| Overall | 🟡 | At risk due to schedule slippage on vendor integration |
| Schedule | 🟡 | Two-week slip on the payments vendor integration |
| Budget | 🟢 | $2.1M of $2.4M consumed, on plan |
| Scope | 🟢 | No change requests this week |
| Resources | 🟢 | Team at full capacity |
| Risk | 🟡 | Vendor risk elevated; mitigation in flight |

---

# The top RAID items this week include one red dependency and two amber risks

| ID | Category | Description | Impact | Owner | Status | RAG |
|----|----------|-------------|--------|-------|--------|-----|
| D-14 | Dependency | Payments vendor API delayed by 2 weeks | High | Priya | Escalated | 🔴 |
| R-07 | Risk | Regulatory approval may slip to June | High | Jamal | Mitigating | 🟡 |
| R-09 | Risk | Key architect out 3 weeks from May 1 | Medium | Pete | Planning cover | 🟡 |
| I-03 | Issue | Staging environment flaky | Medium | Rob | In progress | 🟡 |
| A-02 | Assumption | Marketing launch date holds at July 1 | Low | Sam | Confirmed | 🟢 |

---

# Milestones show two completed, one in-flight, three upcoming

✅ **Completed**
- Week 13: Data migration dry-run passed
- Week 14: Security review signed off

🔵 **Current**
- Week 15: Payments vendor integration (slipped 2 weeks)

⏭️ **Upcoming**
- Week 17: UAT start (was Week 16)
- Week 20: Go-live readiness review
- Week 22: Production cutover

---

# Next steps require a decision on whether to absorb the slip or push go-live

Action items this week:
- Priya to escalate vendor slip to the steering committee by Friday — **decision needed**
- Pete to draft two go-live options (absorb vs push) for the Monday review
- Rob to stabilise staging by Wednesday

**Decision required**: absorb the 2-week slip by compressing UAT, or push go-live to Week 24?
