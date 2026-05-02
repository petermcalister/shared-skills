---
marp: true
theme: consulting
paginate: true
---

<!-- _class: lead -->

# Morning brief is slow and users are unhappy and costs are up and we need to fix many things

Multiple issues, multiple fixes, one deck

Pete · 2026-04-11

---

# Brief latency is 4.2 minutes, open-rate dropped to 71%, and CLI fan-out is sequential, plus memory-search is doing full table scans, and also the staging environment is flaky

All of these things are problems. We will address them all. Some are related, some are not. This slide is trying to make six points at once.

<!-- This slide intentionally violates one-message-per-slide -->

---

# The fix

Do everything at once. Parallelise and index and also repair staging and maybe also rewrite the brief format.

---

# Results

Latency better. Users happy. Costs down.

---

# Appendix
