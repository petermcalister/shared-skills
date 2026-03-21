---
description: Execute a plan-n-park by dispatching run-agent subagents per task batch with operational context
---

# Run Agent

Execute a plan created by `/plan-n-park` by dispatching `run-agent` subagents for batches of 3-4 related tasks. Each subagent arrives pre-loaded with debugging and behave skills via the agent definition — the command only needs to inject the task-specific context.

**Core principles:**
- Subagents protect the main context window — all implementation happens there
- Each subagent gets 3-4 logically related tasks, not one at a time
- Standing rules (bug discipline, git discipline, verification) live in the agent definition
- The command injects operational context from the plan

---

## Step 1: Load and Parse Plan

Read the plan file and extract:
- **Task groups** (batches of 3-4 related features from the plan's Task Groups table)
- **Operational context** (Debug & Operating Notes, Test Strategy, test isolation patterns)
- **Feature JSON** (current pass/fail state)
- **Progress file** (where the last session left off)

If the plan doesn't define task groups, create them: group features by logical dependency or theme, 3-4 per batch.

## Step 2: Resume from Last Session

Read `.claude/plans/claude-progress.txt`. Start from where it says "Next session should:". Don't repeat completed work.

## Step 3: Per Batch — Dispatch run-agent

For each batch, dispatch using the `run-agent` agent definition:

```
Agent tool:
  subagent_type: "run-agent"
  description: "Implement batch N: [theme]"
  prompt: |
    ## Your Tasks

    [FULL TEXT of 3-4 tasks from plan — paste everything, don't make subagent read files]

    ## Operational Context

    [Paste the plan's "Debug & Operating Notes" section]
    [Paste the plan's "Test Strategy" section]
    [Paste any test isolation patterns]
```

The agent definition handles skills (TDD, debugging, behave), standing rules (bug-fixing, git discipline, verification), and report format. The command only injects what's unique to this batch.

## Step 4: Review Subagent Output

When the subagent returns, review its report:

**Check:**
- Did it complete all tasks in the batch?
- Did it run tests and show actual output (not just claims)?
- Did it commit (not push)?
- Did it mention any bugs found and fixed?

**If issues found:** Dispatch a fix subagent (same `run-agent` type) with specific instructions. Don't fix manually (protects main context).

**After review:**
- Update feature JSON: flip `passes: false` to `true` for completed features
- Update progress file with session state

## Step 5: Checkpoint — Report to User

After each batch, pause and report:

```
Batch N complete: [theme]
- Features completed: F001, F002, F003
- Tests: all passing
- Bugs fixed: [any found along the way]
- Commits: [list SHAs]

Next batch: [theme] (F004-F006)
Ready to continue?
```

Wait for user confirmation before proceeding. If user says "run them all", proceed without pausing between batches — but still report at the end.

## Step 6: Final Code Review

After all batches complete, get the git range and dispatch the `reviewer` agent:

```bash
BASE_SHA=$(git log --oneline | grep -m1 "before plan started" | awk '{print $1}')
# or use the SHA from the progress file / first batch
HEAD_SHA=$(git rev-parse HEAD)
```

```
Agent tool:
  subagent_type: "reviewer"
  description: "Code review: [plan-name]"
  prompt: |
    Review the complete implementation of [plan-name].

    ## What Was Implemented
    [Summary of all features from all batches]

    ## Requirements
    [Paste the plan's acceptance criteria and feature list]

    ## Git Range
    Base: [BASE_SHA]
    Head: [HEAD_SHA]

    Run `git diff --stat BASE..HEAD` and `git diff BASE..HEAD` to see all changes.
    Run the full test suite to verify everything passes.
    Compare implementation against requirements line by line.
```

**Act on the review:**
- **Critical issues:** Dispatch `run-agent` to fix immediately
- **Important issues:** Dispatch `run-agent` to fix before completion
- **Minor issues:** Note for user, don't block completion

After fixes, re-run the reviewer to confirm. Final commit (not push). Update progress file and feature JSON.

## Step 7: Finish

- Present summary to user with all commits, features completed, and any remaining work
- User decides next steps (push, PR, further work)

---

## Parallel Dispatch

When batches are independent (no shared files, no sequential dependencies), dispatch multiple `run-agent` subagents simultaneously in a single message. This runs them concurrently.

**Use parallel when:**
- Batches touch different subsystems or files
- No batch depends on another's output
- Fixing one area won't affect another

**Use sequential (default) when:**
- Later batches depend on earlier ones
- Batches modify the same files
- You're unsure — sequential is always safe

After parallel agents return, review all reports together. Check for conflicts (agents editing the same files), then run the full test suite before proceeding.

---

## Controller Role

The main agent's job is orchestration only:

- **Do:** Parse plan, dispatch `run-agent` subagents, review reports, update progress, report to user
- **Don't:** Read implementation files, write code, run tests, debug failures

If something needs fixing, dispatch a subagent. Keep the main context clean.

## Red Flags

- Subagent reports "all done" suspiciously fast — dispatch reviewer to verify
- Subagent skips tests — reject the report, redispatch with explicit test instructions
- Subagent claims success without showing output — reject, redispatch
- Subagent says "found a bug but didn't fix it" — reject, redispatch
- Subagent ran `git push` — flag to user immediately
- Subagent asks questions — answer them clearly before letting it proceed
