---
marp: true
theme: conference
paginate: true
---

<!-- _class: lead -->

# Building a plugin OS for personal AI agents

PyCon London 2026

Pete McAlister

---

# Why personal agents fail to collaborate

Today every agent is an island. Shared work needs shared substrate.

---

# A day in the life of five disconnected agents

[DIAGRAM: five agents each doing redundant ingestion of the same email inbox]

---

# What changes when agents share memory and tools

One ingestion path, one memory store, one tool bus — many agents.

---

# The Cowork architecture at 10,000 feet

[DIAGRAM: plugin host, shared memory bus, CLI layer, skill loading]

---

# Plugins as the unit of composition

A plugin is a directory with commands, skills, hooks, and references. No code coupling.

---

# Live demo: loading three plugins into one session

[LIVE DEMO: loading pete-pa, finance, and story-present plugins]

---

# Skills drive the interaction; CLI shortcuts do the work

Skills are markdown. CLI shortcuts are Python. The split keeps prompts short and code testable.

---

# Memory is a three-tier store with FTS5 and optional vector search

Episodic, tasks, semantic. One query surface via memory-search.

---

# Live demo: a morning brief stitching data from five sources

[LIVE DEMO: morning brief pulling Gmail, Outlook, Calendar, WhatsApp, memory]

---

# Lessons from shipping eight skills over twelve weeks

Short prompts win. References beat inline detail. Defaults beat interviews.

---

# What does not work yet

Cross-plugin event routing, plugin versioning, and hot-reload are all still open problems.

---

# What's next on the roadmap

Q3: plugin registry. Q4: multi-host orchestration. 2027: agent-to-agent protocol.

---

# Takeaways

Share memory. Share tools. Keep skills small. Let the CLI do the heavy lifting.

---

# Thank you

github.com/cowork · pete@cowork.dev · @petemc
