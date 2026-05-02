---
marp: true
theme: consulting
paginate: true
---

<!-- _class: lead -->

# We should consolidate to a single cloud vendor by Q3 2026

A $4.2M annual saving through AWS-only consolidation

Pete McAlister · 2026-04-11

---

# We should consolidate to AWS because cost, operability, and risk all point the same way

**Situation.** We currently run production workloads across AWS, Azure, and GCP, with roughly equal spend across all three.

**Complication.** Multi-cloud overhead has risen to 18% of total infra cost and our on-call burden has doubled year-over-year.

**Resolution.** Consolidate to AWS over Q2–Q3 2026, capturing $4.2M annual savings, halving on-call load, and reducing vendor risk through a single strong contractual relationship.

<!-- speaker: Lead with the recommendation. The three arguments follow. -->

---

# Consolidating to AWS saves $4.2M annually through committed-use discounts

Three-year reserved instance pricing on AWS yields 52% savings versus our current on-demand spend mix, and unified egress eliminates cross-cloud transfer fees entirely.

<!-- Source: finance-ingest 2026-Q1 -->

---

# Cloud spend breakdown shows AWS already carries 41% of workloads at lowest unit cost

[CHART: stacked bar of AWS / Azure / GCP spend by workload class, annotated with $/vCPU-hour]

<!-- Source: memory-event-142 -->

---

# Unifying on AWS halves the on-call surface area and cuts MTTR by 40%

One runbook, one console, one IAM model. Current pager load shows 63% of incidents are cross-cloud routing or auth issues that disappear under a single vendor.

<!-- Source: memory-recent 30d -->

---

# Incident data shows 63% of Sev-2 pages in Q1 were multi-cloud integration failures

[CHART: pareto of incident root causes over 90 days]

<!-- Source: pagerduty export 2026-Q1 -->

---

# Single-vendor risk is lower than multi-vendor risk when contracts include exit clauses

An EDP with a 90-day termination clause and contractual data portability gives us real leverage while removing the 3x coordination tax of multi-vendor operations.

<!-- Source: legal review 2026-03 -->

---

# Vendor comparison shows AWS leads on regional coverage and committed-use flexibility

[TABLE: AWS vs Azure vs GCP across 8 criteria with weighted scores]

<!-- Source: vendor scorecard 2026-Q1 -->

---

# Taken together, the cost, operability, and risk arguments all point to AWS

Cost saves $4.2M. Operability halves on-call. Risk is mitigated by the EDP exit clause. No argument pulls toward a different vendor or toward maintaining the status quo.

---

# We recommend migrating Azure and GCP workloads to AWS over Q2–Q3 2026, led by the Platform team

Phase 1 (Apr–May): Azure workloads. Phase 2 (Jun–Jul): GCP workloads. Phase 3 (Aug–Sep): decommission and contract closeout. Budget: $380K one-time migration cost.

---

# The main risk is migration-induced downtime, mitigated by a blue/green rollout with automated rollback

Every service migrates behind a feature flag with a 2-week bake period. Any SLA regression triggers automatic rollback to the source cloud.

---

# Appendix

Detailed spend tables, vendor scorecards, migration runbooks, and the full incident root-cause analysis.
