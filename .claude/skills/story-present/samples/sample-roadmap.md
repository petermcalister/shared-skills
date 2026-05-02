---
marp: true
theme: consulting
paginate: true
---

<!-- _class: lead -->

# Story-present skill delivery plan for v1.0

6-phase implementation roadmap

Pete McAlister · 2026-04-11

---

# Our objective is to ship the story-present skill end-to-end by 2026-05-15

One skill, six frameworks, four rendering formats, integrated source ingestion, and a calibrated scoring gate.

---

# The plan has five phases covering scaffolding, templates, ingestion, rendering, and calibration

[DIAGRAM: phase Gantt from Phase 1 through Phase 5 with dependency arrows]

---

# The core team is Pete (lead), plus two implementer agents working batch-at-a-time under the plan-n-park pattern

Pete owns architecture, review, and merges. Implementer agents own batches 1–8 under TDD.

---

# Success means 27+ behave scenarios green, 628+ pytest holding, and all 4 rendering formats produce non-empty files

Plus a ≥50% structural-issue detection rate on the calibration sample set.

---

# The main risk is Phase 6 system dependencies (pandoc, marp-cli) not being present on target machines

Mitigated by the dependency preflight check and clear install hints in the check-deps CLI.
