---
name: brainstorming
description: >
  Use when the user has an idea that needs design exploration before implementation —
  when requirements are ambiguous, multiple approaches exist, or the scope isn't clear.
  Trigger on: "I want to build", "how should we approach", "let's design", "I have an
  idea for", "what's the best way to", "brainstorm", "think through this with me", or
  when the user describes a feature at a high level without specifying how to implement it.
  Do NOT trigger for straightforward implementation tasks where the design is already clear.
version: 0.1.0
---

# Brainstorming — Ideas Into Designs

Turn ambiguous ideas into fully formed designs through collaborative dialogue.

Start by understanding the project context, then ask questions one at a time to refine
the idea. Once you understand what you're building, present the design in small sections,
checking after each whether it looks right.

## The Process

**1. Understand the idea:**
- Check the current project state first (files, docs, recent commits)
- Ask questions one at a time — don't overwhelm with multiple questions
- Prefer multiple choice when possible, open-ended when needed
- Focus on: purpose, constraints, success criteria

**2. Explore approaches:**
- Propose 2-3 different approaches with trade-offs
- Lead with your recommended option and explain why
- Present conversationally, not as a formal document

**3. Present the design:**
- Break into sections of 200-300 words
- Ask after each section: "Does this look right so far?"
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and revise if something doesn't fit

## After the Design

**Documentation:** Write the validated design to a plan file appropriate for the
project (e.g., `.claude/plans/<topic>-design.md` or `docs/plans/`).

**Implementation:** Ask "Ready to start implementing?" If yes, consider whether
the work needs an isolated workspace (git worktree) and create an implementation plan.

## Key Principles

- **One question at a time** — don't overwhelm
- **Multiple choice preferred** — easier to answer than open-ended
- **YAGNI ruthlessly** — cut features that aren't clearly needed
- **Explore alternatives** — always propose 2-3 approaches before settling
- **Incremental validation** — present design in sections, validate each
