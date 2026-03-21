---
name: library-management
description: >
  Use this skill when setting up shared skills in a new repo, adding a project to the shared
  library, troubleshooting skill discovery, configuring additionalDirectories, registering
  SessionStart hooks, removing git submodules for skills, or managing the shared-skills repo
  lifecycle (adding skills, pushing changes, syncing across projects). Also trigger when
  the user asks "how do shared skills work", "set up shared skills", "why isn't my skill
  showing up", "add this repo to shared skills", or "connect this project to shared-skills".
version: 0.2.0
---

# Shared Library Management

Manage Pete's shared skill library at `C:/Users/peter/RepoBase/shared-skills`.

## How Shared Skills Work

The shared-skills repo is a **standalone sibling repo**. Consumer projects include it via
`additionalDirectories` in `.claude/settings.json`. Claude Code scans the additional
directory's `.claude/skills/`, `.claude/commands/`, and scripts — making everything
discoverable without submodules or symlinks.

```
C:/Users/peter/RepoBase/
├── shared-skills/                ← the shared library (this repo)
│   ├── .claude/skills/           ← auto-discovered by any consumer
│   ├── .claude/commands/         ← /push-skills, /sync-all
│   ├── scripts/                  ← hook scripts
│   └── tools/library_management/ ← CLI tools
├── cowork/                       ← consumer project
│   └── .claude/settings.json     ← additionalDirectories
└── another-project/              ← another consumer
    └── .claude/settings.json     ← same pattern
```

---

## CLI Tools

All library management is done via CLI shortcuts (registered in pyproject.toml):

| Command | Purpose |
|---------|---------|
| `library-status` | Show repo status, discovered skills, commands |
| `library-status --json` | Same, as JSON |
| `library-setup <project-dir>` | Configure a project to use shared skills |
| `library-verify` | Run the verification script |
| `library-push ["message"]` | Commit + push shared-skills changes |
| `library-sync` | Pull latest from remote |
| `library-list` | List all shared skills with descriptions |

### Quick setup for a new consumer project

```bash
library-setup C:/Users/peter/RepoBase/some-project
```

This creates/merges `.claude/settings.json` in the target project with:
- `additionalDirectories` pointing to shared-skills
- `SessionStart` hook for verification

---

## Setting Up a New Consumer Project (Manual Steps)

When the CLI isn't available or you need to do it manually:

### Step 1: Edit .claude/settings.json

Read the project's `.claude/settings.json`. If it doesn't exist, create it. **Merge** — don't replace — with this structure:

```json
{
  "permissions": {
    "additionalDirectories": [
      "C:/Users/peter/RepoBase/shared-skills"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash C:/Users/peter/RepoBase/shared-skills/scripts/verify-shared-skills.sh"
          }
        ]
      }
    ]
  }
}
```

**IMPORTANT merge rules:**
- If `permissions` exists, add `additionalDirectories` to it — don't overwrite `allow`/`deny`
- If `hooks` exists, add `SessionStart` to it — don't overwrite other hooks
- If `SessionStart` hooks exist, append — don't replace

### Step 2: Remove git submodule (if present)

If the project has a submodule at `.claude/skills/shared`:

```bash
git submodule deinit -f .claude/skills/shared
git rm -f .claude/skills/shared
rm -rf .git/modules/.claude/skills/shared
git commit -m "Remove shared-skills submodule (replaced by additionalDirectories)"
```

### Step 3: Remove duplicate skills

Check for skills that exist in both the project's `.claude/skills/` AND shared-skills:

```bash
for skill in mermaid-diagram excalidraw-diagram skill-creator library-management; do
    [ -d ".claude/skills/$skill" ] && echo "Duplicate: .claude/skills/$skill"
done
```

Remove duplicates — the shared version is discovered via additionalDirectories.

### Step 4: Verify

Restart Claude Code. The SessionStart hook reports:

```
✓ SHARED SKILLS: N skill(s) from C:/Users/peter/RepoBase/shared-skills
  ✓ mermaid-diagram
  ✓ excalidraw-diagram
  ✓ library-management
```

---

## Available Shared Assets

### Skills

| Skill | Trigger |
|-------|---------|
| `mermaid-diagram` | Diagram requests — flowchart, sequence, ER, architecture |
| `excalidraw-diagram` | Visual diagrams — architecture, whiteboard style |
| `skill-creator` | Create, test, or optimize skills |
| `library-management` | This skill — setup, troubleshooting, lifecycle |

### Slash Commands

| Command | Purpose |
|---------|---------|
| `/push-skills` | Commit + push shared-skills without leaving your project |
| `/sync-all` | Pull latest shared skills from remote |

### CLI Tools

| Tool | Purpose |
|------|---------|
| `library-status` | Repo status + skill inventory |
| `library-setup <dir>` | Auto-configure a consumer project |
| `library-verify` | Check skill discovery |
| `library-push` | Commit + push |
| `library-sync` | Pull latest |
| `library-list` | List skills |

---

## Adding a New Skill

1. Create: `mkdir -p .claude/skills/new-skill`
2. Write SKILL.md with frontmatter (`name`, `description`, `version`)
3. Add evals: `mkdir -p .claude/skills/new-skill/evals`
4. Push: `library-push "Added new-skill"` or `/push-skills`

### Skill directory convention

```
.claude/skills/<skill-name>/
├── SKILL.md                    ← required
├── evals/
│   ├── trigger-eval.json       ← eval queries (committed)
│   └── results/                ← eval outputs (gitignored)
├── variants/                   ← A/B testing
│   ├── A/SKILL.md
│   └── B/SKILL.md
├── scripts/                    ← skill-specific scripts
└── references/                 ← skill-specific docs
```

---

## Troubleshooting

### Skills don't appear in /skills
1. Check `additionalDirectories` path is correct and absolute
2. Run: `library-verify`
3. Each skill must be at `.claude/skills/<name>/SKILL.md` (one level deep)

### Duplicate skills
Remove the local copy: `rm -rf .claude/skills/<skill-name>`

### Hook doesn't fire
1. Check `SessionStart` (case-sensitive) in settings.json hooks
2. Verify script exists: `ls C:/Users/peter/RepoBase/shared-skills/scripts/verify-shared-skills.sh`

### Changes not picked up
- Run `library-sync` or `/sync-all` to pull latest
- Consumer projects may need Claude Code restart for new skills
