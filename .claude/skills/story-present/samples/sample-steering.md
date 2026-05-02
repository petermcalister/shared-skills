---
marp: true
theme: status
paginate: true
---

<!-- _class: lead -->

# Programme Atlas steering pack — decision required on go-live date

Steering Committee · 2026-04-15 · Overall 🟡

---

# Programme is 🟡 at risk with schedule and vendor dependency driving amber

| Dimension | RAG | Headline |
|-----------|-----|----------|
| Overall | 🟡 | At risk due to vendor slippage |
| Schedule | 🟡 | 2-week slip on payments integration |
| Budget | 🟢 | On plan at 87% consumed |
| Scope | 🟢 | No change requests |
| Resources | 🟢 | Full capacity |
| Risk | 🟡 | Vendor + regulatory risks elevated |
| Quality | 🟢 | All test gates passing |

---

# Decision required: approve a 2-week push of go-live to Week 24, or absorb the slip via UAT compression

**Ask.** Approve Option A (push go-live to Week 24) or Option B (compress UAT to 1 week and hold Week 22).

**Cost implication.** Option A: +$180K run-rate extension. Option B: $0 but elevated quality risk.

**Timeline implication.** Option A: go-live 2026-07-08. Option B: go-live 2026-06-24.

<!-- speaker: If meeting is cut short, show slides 1, 2, 3, 6, 9, 10 only. This is the survival path. -->

---

# Across three workstreams, payments is red, data is amber, platform is green

| Workstream | Phase | RAG | Key Update |
|------------|-------|-----|------------|
| Payments | Integration | 🔴 | Vendor API delayed 2 weeks |
| Data | UAT prep | 🟡 | Dependent on payments sign-off |
| Platform | Stable | 🟢 | All gates passing |

---

# Financials show $2.1M spent against $2.4M budget with a forecast overrun of $180K under Option A

| Category | Budget | Actual | Variance | Forecast | RAG |
|----------|--------|--------|----------|----------|-----|
| Vendor fees | $1.2M | $1.05M | -$150K | $1.28M | 🟡 |
| Internal labour | $800K | $720K | -$80K | $870K | 🟡 |
| Infrastructure | $400K | $330K | -$70K | $430K | 🟢 |
| **Total** | **$2.4M** | **$2.1M** | **-$300K** | **$2.58M** | 🟡 |

Variance explanation: payments vendor slip triggers 3 weeks of additional internal labour and infra run-rate.

---

# Top risks and issues cluster around the vendor dependency and the architect out-of-office

| Description | Impact | Likelihood | Owner | Mitigation | RAG |
|-------------|--------|------------|-------|------------|-----|
| Vendor API delayed 2 weeks | High | Certain | Priya | Escalated | 🔴 |
| Regulatory approval may slip | High | Medium | Jamal | In flight | 🟡 |
| Lead architect out 3 weeks | Medium | Certain | Pete | Cover identified | 🟡 |
| Staging environment flaky | Medium | Medium | Rob | Fix in progress | 🟡 |

---

# Timeline shows current position at Week 15 with Option A shifting go-live from Week 22 to Week 24

✅ Data migration dry-run (Week 13) · ✅ Security sign-off (Week 14)
🔵 Payments integration (Week 15, slipped)
⏭️ UAT start (Week 17) · Go-live readiness (Week 20) · Production cutover (Week 22 or 24)

---

# Key dependencies include the payments vendor, regulatory approval, and marketing launch date

| Dependency | Owner | Dependent | Status | Date | RAG |
|------------|-------|-----------|--------|------|-----|
| Payments vendor API | Priya | Go-live | Escalated | 2026-05-01 | 🔴 |
| Regulatory sign-off | Jamal | Go-live | In review | 2026-06-01 | 🟡 |
| Marketing launch | Sam | Comms | Confirmed | 2026-07-01 | 🟢 |

---

# We recommend Option A — push go-live to Week 24 — to protect quality and absorb vendor slippage cleanly

| Option | Pros | Cons | Cost | Timeline |
|--------|------|------|------|----------|
| A. Push go-live | Quality protected, UAT full length | $180K overrun | $180K | Week 24 |
| B. Compress UAT | No overrun, holds Week 22 | Quality risk, rollback risk | $0 | Week 22 |

Recommendation: **Option A**. Quality protection outweighs the $180K cost.

---

# Next steering: 2026-05-13 with go-live readiness review and final vendor status

Next 3 milestones: UAT start (Week 17), vendor integration GA (Week 18), go-live readiness review (Week 20).

Key activities for next period: UAT dry-runs, vendor GA test, regulatory final sign-off.
