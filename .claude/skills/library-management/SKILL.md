---
name: library-management
description: >
  Use this skill when promoting a skill from cowork into the public shared-skills marketplace,
  installing skills via Claude Code's marketplace machinery, or deciding where a new skill
  belongs in the 2x2 storage grid (private/public x coding/productivity). Trigger on:
  "promote a skill", "publish this skill", "library-promote", "where does this skill live",
  "install pete-pa", "install shared-skills", "marketplace install", "add a marketplace",
  "skill mastery", "where is this skill mastered", "publish to shared-skills", or any
  question about the cowork-private vs petermcalister-shared-skills marketplaces.
version: 0.6.0
---

# Library Management

Manage skill mastery, promotion, and marketplace installation across the cowork repo and
the public `shared-skills` mirror.

The model is dead simple: every skill has **exactly one master location**. Public-staged
copies in `~/RepoBase/shared-skills/.claude/skills/` are produced by `library-promote` and
must never be edited directly.

---

## Storage Model (the 2x2)

|  | **Coding** | **Personal Productivity** |
|---|---|---|
| **Public** | `~/RepoBase/shared-skills/.claude/skills/` (mirror only — see promotion below) → installed via the `petermcalister-shared-skills` marketplace | _(reserved for future)_ |
| **Private** | `cowork/.claude/skills/` — mastered in this repo, no marketplace | `cowork/pete-pa/skills/` — mastered in this repo, distributed via the private `cowork-private` marketplace |

Three rules that follow from the grid:

1. **One master per skill.** A skill is mastered in either `cowork/.claude/skills/` (coding
   tier) or `cowork/pete-pa/skills/` (personal-productivity tier). Never both.
2. **shared-skills is target-only.** It is never a master. Editing files there directly is
   an anti-pattern — the next `library-promote` run will clobber the change.
3. **Marketplace install for consumers.** Other projects (EmailEvidenceLocker, etc.) consume
   skills via Claude Code's `/plugin marketplace add` and `/plugin install`. No symlinks,
   no `additionalDirectories`, no zip drops.

---

## Promotion Lifecycle

`library-promote` copies a master skill from cowork into `~/RepoBase/shared-skills/.claude/skills/<name>/`,
commits the result in shared-skills, and (by default) pushes. Promote a skill **only** when
it is genuinely ready for public consumption — no project-coupled paths, no
`pete-pa/topics/` references, no secrets.

### When to promote

- The skill is portable (no project-specific paths) **or** Pete has explicitly accepted that
  it ships project-coupled.
- The skill has a clear public audience (other Claude Code users, not just Pete).
- Documentation is ready (frontmatter description, examples, troubleshooting).

### When NOT to promote

- The skill references `pete-pa/`, `cowork/`, or other private paths and you haven't
  explicitly decided to ship that coupling.
- The skill is mid-iteration and the public-facing API is unstable.
- The skill is private to Pete's workflow (personal productivity skills generally stay in
  the private `cowork-private` marketplace as part of pete-pa).

### CLI examples

```bash
# Default: detect source, copy, commit, push.
poetry run library-promote story-present --json

# Skip the push (e.g. while iterating, or when shared-skills working tree is dirty).
poetry run library-promote story-present --json --no-push

# Preview what would happen without touching anything.
poetry run library-promote --dry-run mermaid-diagram

# Required when the skill name exists in BOTH cowork/.claude/skills/ and pete-pa/skills/.
poetry run library-promote --source pete-pa <name>
poetry run library-promote --source cowork <name>
```

### Idempotency

Re-running `library-promote` with no master changes is a no-op — zero file changes, zero
new commits. This is the contract pinned by the `@idempotent` behave scenario in
`features/skill_marketplace_restructure.feature`.

### Source detection

Default search order:

1. `cowork/.claude/skills/<name>/`
2. `cowork/pete-pa/skills/<name>/`

If the skill name resolves in both, the tool exits non-zero and demands `--source`.
shared-skills itself is **never** searched as a source — it is target-only.

---

## Anti-patterns

These were all valid in v0.5.0 and earlier. They are dead in v0.6.0:

| Anti-pattern | Why it's dead |
|---|---|
| Symlink/junction skills from shared-skills into a consumer's `.claude/skills/` | The marketplace install does this for you, and symlinks across repos break in CI, on different drives, and inside plugin zips. |
| Add `~/RepoBase/shared-skills` to `permissions.additionalDirectories` for skill discovery | Discovery now happens via plugin install. `additionalDirectories` is for genuine cross-repo file access, not skill plumbing. |
| Package pete-pa as a `.plugin.zip` and drag-and-drop into Claude Code | Replaced by `/plugin marketplace add petermcalister/cowork-pa` + `/plugin install pete-pa@cowork-private`. The retired build script lives only in `scripts/legacy/` for git-blame archaeology. |
| Edit a skill directly in `~/RepoBase/shared-skills/.claude/skills/` | Edits there are clobbered by the next `library-promote`. Edit the master in cowork, then promote. |
| `pip install -e ~/RepoBase/shared-skills` | The shared-skills repo no longer registers any commands via `pyproject.toml`. The new `library-promote` tool is registered by **cowork**'s pyproject.toml. |

---

## CLI Tools

| Command | Purpose |
|---|---|
| `library-promote <name>` | Copy a master skill from cowork into shared-skills, commit, push (idempotent) |

**History note:** `library-link`, `library-push`, `library-sync`, `library-setup`,
`library-verify`, `library-list`, and `library-status` were removed in v0.6.0 (2026-05-02)
as part of the marketplace restructure. They were replaced by Claude Code's built-in
`/plugin marketplace` and `/plugin install` slash commands plus the new `library-promote`
tool. See `.claude/plans/skill-marketplace-restructure.md` for the migration rationale.

---

## Install commands for consumers

The full canonical reference (with expected output, validation checklist, and diagnostic
notes) lives in `.claude/plans/skill-marketplace-restructure-install-commands.md`. The
two install paths a consumer typically needs:

```text
/plugin marketplace add petermcalister/cowork-pa       # Pete's private marketplace
/plugin install pete-pa@cowork-private

/plugin marketplace add petermcalister/shared-skills   # public skills
/plugin install story-present@petermcalister-shared-skills
```

The marketplace `name` in the `<plugin>@<marketplace>` install command comes from the
`name` field in each repo's `.claude-plugin/marketplace.json`, not the GitHub repo name.
For the cowork repo the GitHub name is `cowork-pa` but the marketplace handle is
`cowork-private`.

Currently promoted public skills (as of 2026-05-02): `story-present`, `library-management`.
