---
marp: true
theme: consulting
paginate: true
---

<!-- _class: lead -->

# Morning brief latency has tripled and needs a two-part fix

Internal problem-solving review

Pete McAlister · 2026-04-11

---

# Morning brief generation now takes 4.2 minutes, up from 1.3 minutes in January

Users are disengaging: open-rate on the 7am brief dropped from 94% to 71% over the same window.

<!-- Source: memory-event-201 -->

---

# The root cause splits into two issues: sequential CLI fan-out and memory-search table scans

Both are independent, both are fixable, and neither blocks the other.

---

# Issue 1: CLI shortcuts run sequentially instead of in parallel, wasting 2.1 minutes per brief

[DIAGRAM: current sequential pipeline vs proposed parallel fan-out]

<!-- Source: profiler trace 2026-04-08 -->

---

# Issue 2: memory-search does a full FTS5 table scan on every query, costing 0.8 minutes per brief

No covering index on (subject, created_at). Query planner falls back to full scan once the episodic table exceeds 10K rows.

<!-- Source: explain-query-plan output -->

---

# The fix for issue 1 is to wrap all CLI fan-out in asyncio.gather with a 90-second shared timeout

One code change in build_briefing_context. Estimated effort: half a day. Estimated saving: 2.1 minutes per brief.

---

# The fix for issue 2 is to add a composite index on (subject, created_at) and run ANALYZE

Two-line migration. Estimated effort: one hour. Estimated saving: 0.8 minutes per brief.

---

# Combined, the two fixes bring brief latency back to 1.3 minutes and restore the 94% open-rate target

[CHART: projected latency before/after both fixes]

---

# We prioritise issue 2 first (one-hour fix, immediate impact) and ship issue 1 the same week

Issue 2 ships Monday. Issue 1 ships Wednesday after review. Full restoration by Friday.

---

# The risk is that the parallel fan-out uncovers a rate-limit on one of the upstream CLIs

Mitigated by a per-source semaphore capping concurrent calls at 4.

---

# Recommended next step: merge PR #142 (issue 2) today and open the draft PR for issue 1 by EOD

Owner: Pete. Review: platform team. Rollback: revert the migration and disable the async gather flag.

---

# Success criteria: brief latency <90 seconds at p95 and open-rate back above 90% within 2 weeks

Measured via the existing brief_metrics table.

---

# Appendix

Full profiler traces, query plans, and the rejected alternative fixes (caching layer, separate service) with rationale.
