---
name: tdd-writing
description: >
  Use when creating, editing, or testing Claude Code skills using a Test-Driven Development
  approach. Trigger on: "create a skill", "write a skill", "test this skill", "the skill
  isn't working", "improve this skill", "skill needs testing", "verify skill works", or
  when the user wants to iterate on a SKILL.md with baseline testing and rationalization
  hardening. This is the TDD approach — for eval/benchmark-based skill development, use
  skill-creator instead.
version: 0.2.0
---

# TDD Writing — Test-Driven Skill Development

Writing skills IS Test-Driven Development applied to process documentation. You write test
cases (pressure scenarios), watch them fail (baseline), write the skill, watch tests pass,
and refactor (close loopholes).

If you didn't watch an agent fail without the skill, you don't know if the skill teaches
the right thing.

**For eval/benchmark-based skill development**, use `skill-creator` instead. This skill
focuses on the RED-GREEN-REFACTOR cycle with subagent pressure testing.

---

## The RED-GREEN-REFACTOR Cycle

### RED: Baseline (Write Failing Test)

Run a pressure scenario with a subagent WITHOUT the skill. Document:
- What choices did the agent make?
- What rationalizations did it use (verbatim)?
- Which pressures triggered violations?

This is "watch the test fail." You must see natural behavior before writing the skill.

### GREEN: Write Minimal Skill

Write a skill that addresses the specific rationalizations from baseline.
Don't add content for hypothetical cases — only address observed failures.

Run the same scenarios WITH the skill. The agent should now comply.

### REFACTOR: Close Loopholes

Agent found a new rationalization? Add an explicit counter. Re-test until bulletproof.
Build a rationalization table from all test iterations.

For detailed testing methodology, read `testing-skills-with-subagents.md`.

---

## Skill Structure

```
skill-name/
├── SKILL.md              # Main reference (required, <500 lines)
├── evals/                # Trigger + implementation evals
├── references/           # Heavy docs (>100 lines)
└── scripts/              # Reusable tools
```

### SKILL.md Frontmatter

```yaml
---
name: kebab-case-name
description: >
  Use when [specific triggers, symptoms, contexts]. Include concrete phrases
  users would say. Write in third person. Do NOT summarize the skill's workflow.
version: 0.1.0
---
```

The description is the primary trigger mechanism. A description that summarizes the
workflow creates a shortcut Claude will take — the skill body becomes documentation
Claude skips. Describe WHEN to use, not HOW it works.

For full description optimization guidance, read `references/cso-guide.md`.

### Body Structure

1. **Overview** — what is this, core principle in 1-2 sentences
2. **When to Use** — symptoms, use cases, when NOT to use
3. **Core Pattern** — before/after comparison or step-by-step
4. **Quick Reference** — table or bullets for scanning
5. **Common Mistakes** — what goes wrong + fixes

Keep SKILL.md under 500 lines. Move heavy reference material to `references/`.

---

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)

**Don't create for:**
- One-off solutions (put in commit message)
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)
- Mechanical constraints (automate with validation instead)

---

## Skill Types and How to Test Each

| Type | Examples | Test approach |
|------|----------|---------------|
| **Discipline** (rules) | TDD, designing-before-coding | Pressure scenarios: time + sunk cost + exhaustion |
| **Technique** (how-to) | condition-based-waiting | Application scenarios: can agent apply correctly? |
| **Pattern** (mental model) | reducing-complexity | Recognition: does agent know when to apply? |
| **Reference** (docs) | API guides | Retrieval: can agent find and use the right info? |

---

## Writing Patterns

- Use **imperative form** in instructions ("Check the code", not "You should check")
- **One excellent example** beats many mediocre ones
- Use **flowcharts only for non-obvious decisions** (not linear steps or reference)
- **Explain why** things matter rather than demanding compliance
- Don't use `@` links (force-loads files, burns context) — use "read X when needed"

---

## Bulletproofing Discipline Skills

When a skill enforces rules, agents will rationalize around them under pressure.

1. **Close every loophole explicitly** — don't just state the rule, forbid specific workarounds
2. **Build a rationalization table** from baseline testing — every excuse gets a counter
3. **Create a red flags list** — self-check items for the agent
4. **Add foundational principle early**: "Violating the letter of the rules IS violating the spirit"

For persuasion psychology research behind these techniques, read `persuasion-principles.md`.

---

## Checklist

**RED Phase:**
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run WITHOUT skill — document baseline behavior verbatim
- [ ] Identify rationalization patterns

**GREEN Phase:**
- [ ] Name: letters, numbers, hyphens only
- [ ] Description: starts with "Use when...", third person, no workflow summary
- [ ] Keywords throughout for discovery
- [ ] Address specific baseline failures
- [ ] Run WITH skill — verify compliance

**REFACTOR Phase:**
- [ ] Identify new rationalizations
- [ ] Add explicit counters
- [ ] Build rationalization table
- [ ] Re-test until bulletproof

**Quality:**
- [ ] Under 500 lines (move excess to references/)
- [ ] Quick reference table for scanning
- [ ] Common mistakes section
- [ ] No narrative storytelling
