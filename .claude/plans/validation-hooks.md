# Validation Hooks Plan

> **For execution:** Use `/run-agent` to implement this plan.

## Overview

Add validation tooling that ensures shared skills stay portable, well-structured, and independently deployable. Three new CLI tools plus hook wiring to run them automatically.

## Feature List

See: `.claude/plans/validation-hooks-features.json`

Total features: 6
Passing: 0

## Task Groups

| Batch | Features | Theme |
|-------|----------|-------|
| 1 | F001-F002 | library-lint (skill validation + tool independence) |
| 2 | F003 | library-health (ecosystem scanner) |
| 3 | F004-F006 | Hook wiring + registration |

## Files to Modify

| File | Change |
|------|--------|
| `tools/library_management/lint.py` | New: skill structural linter + tool independence checker |
| `tools/library_management/health.py` | New: ecosystem health scanner for consumer projects |
| `scripts/pre-commit` | New: git pre-commit hook wrapper |
| `pyproject.toml` | Add library-lint and library-health script entries |
| `.claude/settings.json` | Add SessionStart hook for library-health |
| `.claude/skills/library-management/SKILL.md` | Document new tools |

## Architecture

### library-lint (F001 + F002)

A single CLI that runs two check categories:

**Skill checks (F001)** — for every `.claude/skills/*/SKILL.md`:
- Frontmatter has `name`, `description`, `version`
- `description` starts with "Use when" or trigger-focused phrasing
- SKILL.md is under 500 lines
- No project-specific references: `cowork`, `pete-pa`, `EmailEvidenceLocker`
- No `${CLAUDE_PLUGIN_ROOT}` (plugin-specific, not valid in shared skills)
- No hardcoded absolute paths except `~/RepoBase/` convention
- All relative file references (`references/`, `scripts/`, `evals/`) actually exist
- No `@` force-load links

**Tool checks (F002)** — for every `tools/*/`:
- No imports from sibling tool packages (`from tools.other_package import ...`)
- Each tool package is self-contained

**CLI interface:**
```bash
library-lint                    # Lint all skills + tools
library-lint --skills-only      # Only skill checks
library-lint --tools-only       # Only tool independence
library-lint --files FILE...    # Lint specific files (for pre-commit)
library-lint --json             # JSON output
```

**Exit codes:** 0 = clean, 1 = violations found

### library-health (F003)

Scans `~/RepoBase/` for consumer projects and reports ecosystem status.

**Discovery:** Iterates `~/RepoBase/*/` looking for `.claude/settings.json` files
that contain `additionalDirectories` pointing to `shared-skills`. No registry needed —
purely filesystem-based.

**Per-consumer checks:**
- Symlinks exist for each shared skill
- Symlinks point to valid targets (not broken)
- No stale symlinks (pointing to deleted shared skills)
- `.gitignore` managed block is up to date

**Shared-skills repo checks:**
- Uncommitted changes warning
- Unpushed commits warning

**CLI interface:**
```bash
library-health                  # Full ecosystem scan
library-health --json           # JSON output
```

**Exit code:** Always 0 (informational, non-blocking for hooks)

### Pre-commit hook (F004)

Thin bash script that:
1. Gets list of staged `.claude/skills/*/SKILL.md` and `tools/**/*.py` files
2. Runs `library-lint --files <staged-files>`
3. Blocks commit if lint fails

Installed by:
```bash
cp scripts/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Or automatically via `library-setup` when setting up this repo.

### SessionStart hook (F005)

Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "library-health 2>/dev/null || true"
      }]
    }]
  }
}
```

Non-blocking — runs silently if `library-health` isn't installed.

## Test Strategy

- **Unit tests (pytest):** lint rules against known-good and known-bad SKILL.md fixtures
- **Integration:** run `library-lint` on our own skills (should pass), run on a crafted bad skill (should fail)
- **Verification:** `library-health` correctly discovers cowork and EmailEvidenceLocker as consumers

### Test fixtures needed

Create `tests/fixtures/` with:
- `good-skill/SKILL.md` — passes all checks
- `bad-frontmatter/SKILL.md` — missing version
- `bad-refs/SKILL.md` — references cowork, pete-pa
- `bad-paths/SKILL.md` — hardcoded C:/Users/peter paths
- `bad-length/SKILL.md` — over 500 lines

## Debug & Operating Notes

- `~/RepoBase/` is the convention for all repos — hardcoded in health scanner
- Windows paths use forward slashes in Python (`Path` handles this)
- Consumer discovery is dynamic — no registry to maintain
- `library-lint` should be fast (<2s) since it's grep-based, no subprocess spawning
- Pre-commit hook must work in Git Bash on Windows
- The `PYTHONUTF8=1` env var is already set in settings.json for Windows encoding

## Incremental Order

1. **F001** — library-lint skill checks (core linter, everything builds on this)
2. **F002** — library-lint tool independence (extends F001, same CLI)
3. **F003** — library-health ecosystem scanner (independent of F001-F002)
4. **F004** — pre-commit hook (depends on F001)
5. **F005** — SessionStart hook (depends on F003)
6. **F006** — registration + docs (depends on all above)

## Code Review

After all batches complete, `/run-agent` dispatches a `reviewer` agent
to check the full implementation against this plan. The reviewer checks:
- All requirements met (line by line against this plan)
- Code quality and architecture
- Test coverage and results
- No scope creep

Critical and Important issues must be fixed before completion.

## Acceptance Criteria

All features in `validation-hooks-features.json` have `passes: true`
and the final code review assessment is "Ready to merge".
