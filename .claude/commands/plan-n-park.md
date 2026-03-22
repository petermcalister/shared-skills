---
description: Create a comprehensive implementation plan with structured artifacts for multi-session work
---

# Super Plan Command

Create a plan in `.claude/plans/{plan-name}.md` with structured artifacts for multi-session work.

---

## Phase 1: Get Your Bearings (REQUIRED)

Before doing anything, orient yourself:

```bash
# 1. Where am I?
pwd

# 2. What happened recently?
git log --oneline -10

# 3. Read progress file (if exists)
cat .claude/plans/claude-progress.txt

# 4. Check for existing plans
ls .claude/plans/*.md
```

**If previous session left bugs:** Fix them BEFORE planning new work.

---

## Phase 2: Clarify Until 90% Confident (REQUIRED)

**Ask clarifying questions until you reach 90% confidence** on:

| Area | Questions to Consider |
|------|----------------------|
| **Requirements** | What exactly should this feature do? What are the acceptance criteria? |
| **Scope** | What's in scope vs out of scope? Are there related features to avoid touching? |
| **Technical Approach** | Which existing patterns should we follow? Any architectural constraints? |
| **Edge Cases** | What happens with empty data? Nulls? Large datasets? Concurrent access? |
| **Dependencies** | What must exist before this can work? What depends on this? |
| **Testing** | How will we verify this works? What test scenarios cover it? |

**Process:**
1. Explore the codebase to understand current state
2. Identify ambiguities or gaps in understanding
3. Use `AskUserQuestion` tool to clarify before writing the plan
4. Only proceed to write the plan when confidence >= 90%

**Do NOT write the plan if:**
- Requirements could be interpreted multiple ways
- You're unsure which existing code to modify
- The scope feels unclear or unbounded
- You're guessing at the user's intent

---

## Phase 3: Create Structured Artifacts

### 3.1 Feature List (JSON) - CRITICAL

Create `.claude/plans/{plan-name}-features.json` with pass/fail tracking:

```json
{
  "plan_name": "{plan-name}",
  "created": "YYYY-MM-DD",
  "features": [
    {
      "id": "F001",
      "description": "Short description of feature",
      "acceptance": "How to verify this is done",
      "passes": false
    }
  ]
}
```

**CRITICAL RULES:**
- Use JSON, not Markdown (harder to accidentally corrupt)
- Only change `passes` field - NEVER remove or edit feature descriptions
- Each feature must be independently testable
- Features should be small enough to complete in one session

### 3.2 Plan File (Markdown)

Create `.claude/plans/{plan-name}.md` using template below.

### 3.3 Progress File

Create/update `.claude/plans/claude-progress.txt`:

```text
=== Session: YYYY-MM-DD HH:MM ===
Plan: {plan-name}
Worked on: F001, F002
Completed: F001
Blocked: None
Next session should: Start with F002, then F003
Environment state: Clean, all tests pass
```

---

## Phase 4: Pre-Implementation Verification

Before finalising the plan, verify these areas are addressed:

### Test Isolation

| Question | Why It Matters |
|----------|----------------|
| How will tests filter data from previous runs? | Old data without new fields causes false failures |
| What identifier links test data to the current run? | e.g., `run_id`, `created_by`, `created_at` |
| Do step definitions query ALL records or filtered records? | Querying all records includes stale data |

**Pattern:** Filter by run identifier in verification steps:
```python
# Filter findings by current analysis run, not all historical findings
current_run_id = context.analysis_result.get('run_id')
for evidence in evidence_list:
    if str(evidence.get('analysis_run_id')) != str(current_run_id):
        continue  # Skip findings from previous runs
```

### Existing Data Impact

| Question | Action Required |
|----------|-----------------|
| What if database has records without new fields? | Plan migration + handle NULL values |
| Will new constraints break existing data? | Test migration on copy of prod data |
| Do old records need backfilling? | Add migration step or mark as N/A |

### Test Step Dependencies

Document what context/state each test step requires:

```markdown
| Step | Requires in Context |
|------|---------------------|
| `Then each finding has explanation` | `context.analysis_result['run_id']` |
| `Then findings are persisted` | `context.thread_emails` list |
```

### Explicit Acceptance Criteria

**Don't write:** "All tests pass"

**Do write:**
```markdown
## Acceptance Criteria
- [ ] `@explanation` scenario passes: "Output includes explanation field"
- [ ] `@confidence` scenario passes: "Low-confidence results are filtered"
- [ ] UI displays results correctly
```

---

## Phase 5: Work Incrementally

Pick the highest-priority feature with `passes: false`, implement it completely, test it, mark `passes: true`, commit. If time remains, pick next feature.

### Clean State Rule

End every session with:
- [ ] All changes committed to git (commit only — never push)
- [ ] Tests passing (or documented why not)
- [ ] Progress file updated
- [ ] No half-implemented features

---

## Phase 6: End-of-Session Protocol

Before ending work:

1. Run relevant tests
2. Check `git status`
3. Commit with descriptive message referencing the feature ID (never push)
4. Update progress file with session summary
5. Update feature list — change `passes: false` to `passes: true` for completed features

---

## Plan Template

```markdown
# {Feature Name} Plan

> **For execution:** Use `/run-agent` to implement this plan.

## Overview
{Brief description - 1-2 sentences}

## Feature List
See: `.claude/plans/{plan-name}-features.json`

Total features: {N}
Passing: {0}

## Task Groups

Group features into batches of 3-4 logically related tasks. Each batch is
assigned to one subagent session during execution.

| Batch | Features | Theme |
|-------|----------|-------|
| 1 | F001-F003 | {description} |
| 2 | F004-F007 | {description} |

## Files to Modify
| File | Change |
|------|--------|
| `path/to/file` | Description of change |

## Test Strategy
- **Unit tests (pytest):** {list of modules needing unit tests}
- **Integration tests (behave):** {list of scenarios — see Behave Feature below}
- **Verification:** {how to confirm}
- **Test isolation:** {how tests avoid stale data}

## Behave Feature

For significant new features, write the `.feature` file as part of the plan.
This defines acceptance criteria in executable Gherkin before any code is written.

```gherkin
Feature: {Feature name}
  As {persona}
  I want {capability}
  So that {benefit}

  Scenario: {Happy path}
    Given {precondition}
    When {action}
    Then {expected outcome}

  Scenario: {Edge case or error}
    Given {precondition}
    When {action}
    Then {expected outcome}
```

**Save to:** `features/{feature-name}.feature`

**When to include:** Any feature that introduces new user-facing behaviour,
new CLI commands, new data flows, or integration points. Skip for pure
refactoring, config changes, or internal-only restructuring.

**Step definitions:** `features/steps/{feature_name}_steps.py` — one of the
first implementation tasks should be writing the step stubs so the feature
file runs (and fails) before implementation begins.

## Debug & Operating Notes

Document anything an implementing agent needs to know:
- Known quirks in the codebase
- Common failure modes and how to diagnose them
- Environment setup or prerequisites
- Patterns to follow (or avoid)

## Incremental Order
Work on features in this order:
1. F001 - {description} (blocking)
2. F002 - {description} (depends on F001)
3. F003 - {description} (independent)

## Code Review

After all batches complete, `/run-agent` dispatches a `reviewer` agent
to check the full implementation against this plan. The reviewer checks:
- All requirements met (line by line against this plan)
- Code quality and architecture
- Test coverage and results
- No scope creep

Critical and Important issues must be fixed before completion.

## Documentation Sweep

After code review passes, check whether these files need updating to
reflect the new work. Only update what has actually changed — don't
rewrite sections that are still accurate.

| File | Check for |
|------|-----------|
| `CLAUDE.md` | CLI shortcuts table, current actions table, current state, tool structure tree, version number |
| `README.md` | CLI reference examples, architecture descriptions, feature lists |
| `pyproject.toml` | Already handled by implementation — verify only |
| Plugin manifests (`plugin.json`) | Version bump if plugin-packaged features changed |
| Startup tool description (`__main__.py`) | If startup gained new responsibilities |

**Skip this section** for pure refactoring, test-only changes, or
internal restructuring that doesn't affect the user-facing surface.

## Acceptance Criteria
All features in `{plan-name}-features.json` have `passes: true`,
the final code review assessment is "Ready to merge",
and documentation is up to date.
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| Implement entire plan in one session | Runs out of context mid-feature | One feature at a time |
| Skip testing before marking done | Bugs accumulate | Always verify with tests |
| Edit feature descriptions in JSON | Loses requirements | Only change `passes` field |
| Leave uncommitted changes | Next session starts broken | Commit before ending |
| Skip progress file | Next session has no context | Always update progress |
| `git push` during planning/execution | Only the human decides when to push | Commit only |
| Vague acceptance criteria | Untestable outcomes | Name specific scenarios and expected results |
| Ignoring existing data state | NULL handling surprises | Plan for migrations and backfill |

---

## Quick Checklist

### Before Planning
- [ ] Ran `git log` and read progress file
- [ ] Verified project runs
- [ ] Asked clarifying questions (90% confidence)

### Plan Created
- [ ] Feature list JSON created
- [ ] Plan markdown created
- [ ] Features are small, independently testable
- [ ] Task groups defined (3-4 related features per batch)
- [ ] Behave `.feature` file written (if significant new behaviour)
- [ ] Debug & operating notes section populated
- [ ] Test isolation strategy documented
- [ ] Acceptance criteria are specific and verifiable

### After Each Feature
- [ ] Feature tested and verified
- [ ] `passes: true` in feature JSON
- [ ] Changes committed with descriptive message
- [ ] Progress file updated

### After All Features
- [ ] Documentation sweep: CLAUDE.md, README.md, plugin manifests updated if needed

### End of Session
- [ ] No uncommitted changes
- [ ] Tests passing
- [ ] Progress file has "Next session should:" guidance
