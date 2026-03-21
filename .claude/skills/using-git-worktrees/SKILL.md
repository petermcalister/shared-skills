---
name: using-git-worktrees
description: >
  Use when starting feature work that needs isolation from the current workspace,
  working on multiple branches simultaneously, or before executing an implementation
  plan that shouldn't affect the main working tree. Trigger on: "create a worktree",
  "isolated workspace", "work on a branch without switching", "set up a feature branch",
  "parallel branch work", or when the user wants to implement something without
  disturbing their current working state.
version: 0.1.0
---

# Using Git Worktrees

Create isolated workspaces sharing the same repository — work on multiple branches
simultaneously without switching.

## Directory Selection

Follow this priority:

1. **Check existing directories:** `.worktrees/` (preferred) or `worktrees/`
2. **Check CLAUDE.md** for a worktree directory preference
3. **Ask the user** — suggest `.worktrees/` (project-local, hidden) or a global location

## Safety Verification

For project-local directories, verify the worktree directory is gitignored before
creating anything — unignored worktree contents pollute git status and risk accidental commits.

```bash
git check-ignore -q .worktrees 2>/dev/null
```

If not ignored: add to `.gitignore` and commit before proceeding.

Global directories (outside the project) don't need this check.

## Creation Steps

### 1. Create the worktree

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
git worktree add .worktrees/$BRANCH_NAME -b $BRANCH_NAME
cd .worktrees/$BRANCH_NAME
```

### 2. Run project setup

Auto-detect from project files:

```bash
[ -f package.json ] && npm install
[ -f pyproject.toml ] && poetry install
[ -f Cargo.toml ] && cargo build
[ -f go.mod ] && go mod download
[ -f requirements.txt ] && pip install -r requirements.txt
```

### 3. Verify clean baseline

Run the project's test suite to confirm the worktree starts clean:

```bash
# Use the project-appropriate test command
npm test / pytest / cargo test / go test ./...
```

If tests fail: report the failures and ask whether to proceed or investigate.
If tests pass: report ready.

### 4. Report

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md, then ask user |
| Directory not ignored | Add to .gitignore + commit first |
| Tests fail at baseline | Report failures + ask |
| No package.json etc. | Skip dependency install |

## Common Mistakes

1. **Skipping ignore verification** — worktree contents get tracked, pollute git status. Always `git check-ignore` first.
2. **Assuming directory location** — follow priority: existing > CLAUDE.md > ask.
3. **Proceeding with failing tests** — can't distinguish new bugs from pre-existing. Report and ask.
4. **Hardcoding setup commands** — auto-detect from project files instead.
