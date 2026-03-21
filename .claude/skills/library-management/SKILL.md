---
name: library-management
description: >
  Use this skill when setting up shared skills in a new repo, adding a project to the shared
  library, troubleshooting skill discovery, configuring additionalDirectories, registering
  SessionStart hooks, removing git submodules for skills, or managing the shared-skills repo
  lifecycle (adding skills, pushing changes, syncing across projects). Also trigger when
  the user asks "how do shared skills work", "set up shared skills", "why isn't my skill
  showing up", "add this repo to shared skills", or "connect this project to shared-skills".
version: 0.1.0
---

# Shared Library Management

This skill teaches you how to set up, consume, and maintain Pete's shared skill library
at `C:/Users/peter/RepoBase/shared-skills`.

## How Shared Skills Work

The shared-skills repo is a **standalone sibling repo** that any project includes via
`additionalDirectories` in its `.claude/settings.json`. Claude Code scans the additional
directory's `.claude/skills/`, `.claude/commands/`, and scripts — making everything
discoverable without submodules or symlinks.

```
C:/Users/peter/RepoBase/
├── shared-skills/                ← the shared library
│   ├── .claude/skills/           ← auto-discovered by any consumer
│   ├── .claude/commands/         ← /push-skills, /sync-all
│   └── scripts/                  ← hook scripts
├── cowork/                       ← consumer project
│   └── .claude/settings.json     ← additionalDirectories → shared-skills
└── another-project/              ← another consumer
    └── .claude/settings.json     ← same pattern
```

---

## Setting Up a New Consumer Project

When the user asks to connect a project to shared skills, follow these steps:

### Step 1: Add additionalDirectories

Read the project's `.claude/settings.json` (create if it doesn't exist). Add or merge:

```json
{
  "permissions": {
    "additionalDirectories": [
      "C:/Users/peter/RepoBase/shared-skills"
    ]
  }
}
```

If `settings.json` already has `permissions`, merge `additionalDirectories` into the
existing `permissions` object. Don't overwrite other settings.

### Step 2: Add the SessionStart verification hook

Add to the project's `.claude/settings.json` (merge with existing hooks if any):

```json
{
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

### Step 3: Remove git submodule (if present)

If the project has a git submodule pointing to shared-skills, remove it:

```bash
git submodule deinit -f .claude/skills/shared
git rm -f .claude/skills/shared
rm -rf .git/modules/.claude/skills/shared
git commit -m "Remove shared-skills submodule (replaced by additionalDirectories)"
```

### Step 4: Remove duplicate skills

If the project has copies of shared skills in `.claude/skills/`, remove them to
avoid duplicates. Check for:

```bash
# Skills that exist in both the project AND shared-skills
for skill in mermaid-diagram excalidraw-diagram skill-creator; do
    if [ -d ".claude/skills/$skill" ]; then
        echo "Duplicate: .claude/skills/$skill (also in shared-skills)"
    fi
done
```

Remove duplicates — the shared version will be discovered via additionalDirectories.

### Step 5: Verify

Restart Claude Code. On session start, the hook should report:

```
✓ SHARED SKILLS: N skill(s) from C:/Users/peter/RepoBase/shared-skills
  ✓ mermaid-diagram
  ✓ excalidraw-diagram
  ✓ library-management
  ...
```

Run `/skills` to confirm both local and shared skills appear.

---

## Available Shared Assets

### Skills (auto-discovered)

| Skill | Trigger |
|-------|---------|
| `mermaid-diagram` | Diagram requests — flowchart, sequence, ER, architecture |
| `excalidraw-diagram` | Visual diagram requests — architecture, whiteboard style |
| `skill-creator` | Create, test, or optimize skills |
| `library-management` | This skill — setup, troubleshooting, lifecycle |

### Commands (auto-discovered)

| Command | Purpose |
|---------|---------|
| `/push-skills` | Commit + push shared-skills changes without leaving your project |
| `/sync-all` | Pull latest shared skills from remote |

### Scripts (used by hooks)

| Script | Purpose |
|--------|---------|
| `scripts/verify-shared-skills.sh` | SessionStart hook — reports discovered skills |
| `scripts/push-shared-skills.sh` | Standalone push helper (use from terminal) |

---

## Adding a New Skill to the Shared Library

1. Create the skill directory and SKILL.md:
   ```bash
   mkdir -p C:/Users/peter/RepoBase/shared-skills/.claude/skills/new-skill
   ```

2. Write the SKILL.md with YAML frontmatter:
   ```yaml
   ---
   name: new-skill
   description: "When to trigger this skill..."
   version: 0.1.0
   ---
   ```

3. Add evals (optional but recommended):
   ```
   .claude/skills/new-skill/
   ├── SKILL.md
   ├── evals/
   │   └── trigger-eval.json
   └── references/        (if needed)
   ```

4. Push: run `/push-skills` or `bash scripts/push-shared-skills.sh "Added new-skill"`

5. The skill is immediately available in all consumer projects (no restart needed
   for the shared-skills workspace; consumer projects may need restart).

---

## Eval Convention

Evals live inside each skill, not in a centralized directory:

```
.claude/skills/<skill-name>/
├── SKILL.md
├── evals/
│   ├── trigger-eval.json       ← eval queries (committed)
│   └── results/                ← eval outputs (gitignored)
├── variants/                   ← A/B testing
│   ├── A/SKILL.md
│   └── B/SKILL.md
├── scripts/                    ← skill-specific scripts
└── references/                 ← skill-specific docs
```

Run evals from the skill-creator:
```bash
PYTHONUTF8=1 python -c "
import sys; sys.path.insert(0, '.claude/skills/skill-creator')
from scripts.run_eval import main; sys.argv = [
    'run_eval',
    '--eval-set', '.claude/skills/<skill>/evals/trigger-eval.json',
    '--skill-path', '.claude/skills/<skill>',
    '--runs-per-query', '1',
    '--verbose',
]; main()
"
```

---

## Troubleshooting

### Skills don't appear in /skills
1. Check `additionalDirectories` path is correct and absolute
2. Verify skills are at `.claude/skills/<name>/SKILL.md` (one level deep)
3. Run: `bash C:/Users/peter/RepoBase/shared-skills/scripts/verify-shared-skills.sh`

### Duplicate skills showing
Remove the local copy — the shared version is discovered via additionalDirectories:
```bash
rm -rf .claude/skills/<duplicate-skill-name>
```

### Hook doesn't fire
1. Check `SessionStart` (case-sensitive) in settings.json hooks
2. Verify script is executable: `chmod +x scripts/verify-shared-skills.sh`
3. Check script path is absolute

### Changes not picked up
- Shared-skills workspace: changes are live (no restart needed)
- Consumer projects: may need Claude Code restart to pick up new skills
- Run `/sync-all` to pull latest from remote
