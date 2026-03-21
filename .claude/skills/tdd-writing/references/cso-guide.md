# Claude Search Optimization (CSO) Guide

How to write skill descriptions and content so Claude can find and correctly trigger your skill.

## The Description Field

The description is the primary trigger mechanism. Claude reads it to decide: "Should I load this skill right now?"

### Format
- Start with "Use when..."
- Write in third person (injected into system prompt)
- Include concrete triggers, symptoms, and situations
- Max 1024 characters total for frontmatter

### The Workflow Trap

When a description summarizes the skill's workflow, Claude may follow the description
instead of reading the full skill content. This was discovered in testing: a description
saying "code review between tasks" caused Claude to do ONE review, even though the
skill's flowchart clearly showed TWO reviews.

When the description was changed to just "Use when executing implementation plans with
independent tasks" (no workflow summary), Claude correctly read and followed the full process.

```yaml
# BAD: Summarizes workflow — Claude follows this shortcut
description: Use when executing plans - dispatches subagent per task with code review between tasks

# BAD: Too much process detail
description: Use for TDD - write test first, watch it fail, write minimal code, refactor

# GOOD: Just triggering conditions
description: Use when executing implementation plans with independent tasks in the current session

# GOOD: Triggering conditions only
description: Use when implementing any feature or bugfix, before writing implementation code
```

## Keyword Coverage

Use words Claude would search for:
- **Error messages**: "Hook timed out", "ENOTEMPTY", "race condition"
- **Symptoms**: "flaky", "hanging", "zombie", "pollution"
- **Synonyms**: "timeout/hang/freeze", "cleanup/teardown/afterEach"
- **Tools**: Actual commands, library names, file types

## Naming

Use active voice, verb-first, gerunds for processes:
- `condition-based-waiting` not `async-test-helpers`
- `creating-skills` not `skill-creation`
- `root-cause-tracing` not `debugging-techniques`

## Token Efficiency

Skills that load frequently need to be lean. Target word counts:
- Getting-started workflows: <150 words
- Frequently-loaded skills: <200 words
- Other skills: <500 words

Techniques:
- Reference `--help` instead of documenting all flags
- Cross-reference other skills instead of repeating content
- One minimal example instead of verbose multi-step demonstrations
- Don't repeat what's in cross-referenced skills

## Cross-Referencing

Use skill name only, with explicit requirement markers:
```markdown
**REQUIRED BACKGROUND:** You must understand tdd-writing before using this skill.
```

Don't use `@` links — they force-load files immediately, consuming context before needed.
