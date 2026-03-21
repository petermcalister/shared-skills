# Sharing Claude Code Skills Across Repos — Complete Setup Guide

## The problem

Claude Code discovers skills by scanning `.claude/skills/<name>/SKILL.md` only **one level deep**. Git submodules and nested directories create extra depth that breaks discovery silently. Symlinks are fragile and have broken across multiple Claude Code versions (issues #764, #10573, #14836, #25367). Neither approach lets you edit a skill in your working repo and push changes back to a shared source.

## The solution: `--add-dir` with a standalone shared-skills repo

Instead of embedding skills inside each project via submodules or symlinks, keep them in a **standalone sibling repo** and tell Claude Code to include it via `--add-dir`.

This gives you:

- **Reliable skill discovery** — skills sit at the exact depth Claude Code expects
- **Full git workflow** — edit, commit, push from the shared repo directly
- **No symlinks** — avoids all documented fragility
- **No duplication** — one source of truth, many consumers
- **Live reload** — changes to skills are picked up mid-session without restarting

---

## Directory layout

```
~/projects/
├── shared-skills/                    ← standalone git repo (the shared source)
│   ├── .claude/
│   │   └── skills/
│   │       ├── job-search/
│   │       │   └── SKILL.md          ← your job search skill
│   │       ├── cv-tailor/
│   │       │   └── SKILL.md          ← CV tailoring skill
│   │       └── interview-prep/
│   │           └── SKILL.md          ← interview preparation skill
│   └── README.md
│
├── peter-pa/                         ← your cowork/project repo
│   ├── .claude/
│   │   ├── settings.json             ← persists --add-dir config
│   │   ├── hooks.json                ← PostStart hook for verification
│   │   └── skills/
│   │       └── local-only-skill/     ← project-specific skills still work
│   │           └── SKILL.md
│   ├── scripts/
│   │   └── verify-shared-skills.sh   ← hook script (git tracked)
│   └── CLAUDE.md
│
└── another-project/                  ← any other repo can also use shared-skills
    └── .claude/
        └── settings.json             ← same additionalDirectories entry
```

---

## Setup steps

### Step 1: Create the shared-skills repo

```bash
mkdir -p ~/projects/shared-skills/.claude/skills
cd ~/projects/shared-skills
git init

# Copy your SKILL.md files into .claude/skills/<skill-name>/SKILL.md
# Each skill must be in its own subdirectory with a SKILL.md file

git add -A
git commit -m "Initial shared skills"
git remote add origin git@github.com:you/shared-skills.git
git push -u origin main
```

### Step 2: Configure your cowork repo to use it

**Option A — Launch with the flag:**

```bash
cd ~/projects/peter-pa
claude --add-dir ~/projects/shared-skills
```

**Option B — Persist it in settings (recommended):**

Create or edit `.claude/settings.json` in your cowork repo:

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  },
  "additionalDirectories": [
    "~/projects/shared-skills"
  ]
}
```

This means every time you launch Claude Code from this repo, the shared skills are automatically included without needing to remember the `--add-dir` flag.

### Step 3: Add the verification hook

This is optional but recommended. It confirms shared skills are discoverable on every session start.

**Create `.claude/hooks.json`:**

```json
{
  "hooks": [
    {
      "matcher": "PostStart",
      "hooks": [
        {
          "type": "command",
          "command": "bash ./scripts/verify-shared-skills.sh"
        }
      ]
    }
  ]
}
```

**Create `scripts/verify-shared-skills.sh`:**

```bash
#!/bin/bash
# verify-shared-skills.sh
# PostStart hook: confirms shared skills from --add-dir are discoverable
# Git track this file so all team members get the verification automatically.
#
# Customise SHARED_SKILLS_DIR to match your layout.

SHARED_SKILLS_DIR="${HOME}/projects/shared-skills"
SKILLS_PATH="${SHARED_SKILLS_DIR}/.claude/skills"
ERRORS=0

# ─── Check 1: Does the shared-skills directory exist? ───
if [ ! -d "${SHARED_SKILLS_DIR}" ]; then
    echo "⚠ SHARED SKILLS: directory not found at ${SHARED_SKILLS_DIR}"
    echo "  Clone it:  git clone git@github.com:you/shared-skills.git ${SHARED_SKILLS_DIR}"
    echo "  Or update SHARED_SKILLS_DIR in this script to match your layout."
    exit 0  # exit 0 so hook doesn't block the session
fi

# ─── Check 2: Does the .claude/skills/ directory exist with content? ───
if [ ! -d "${SKILLS_PATH}" ]; then
    echo "⚠ SHARED SKILLS: ${SKILLS_PATH} not found"
    echo "  The repo exists but has no .claude/skills/ directory."
    ERRORS=$((ERRORS + 1))
fi

# ─── Check 3: Count discoverable skills ───
SKILL_COUNT=0
SKILL_NAMES=""
if [ -d "${SKILLS_PATH}" ]; then
    for skill_dir in "${SKILLS_PATH}"/*/; do
        if [ -f "${skill_dir}SKILL.md" ]; then
            SKILL_COUNT=$((SKILL_COUNT + 1))
            skill_name=$(basename "${skill_dir}")
            SKILL_NAMES="${SKILL_NAMES}  ✓ ${skill_name}\n"
        fi
    done
fi

if [ ${SKILL_COUNT} -eq 0 ] && [ -d "${SKILLS_PATH}" ]; then
    echo "⚠ SHARED SKILLS: no SKILL.md files found in ${SKILLS_PATH}"
    echo "  Each skill needs: ${SKILLS_PATH}/<skill-name>/SKILL.md"
    ERRORS=$((ERRORS + 1))
fi

# ─── Check 4: Warn about uncommitted changes ───
DIRTY=""
if [ -d "${SHARED_SKILLS_DIR}/.git" ]; then
    cd "${SHARED_SKILLS_DIR}"
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        DIRTY="  ⚠ Uncommitted changes in shared-skills repo"
    fi
    cd - > /dev/null
fi

# ─── Report ───
if [ ${SKILL_COUNT} -gt 0 ]; then
    echo "✓ SHARED SKILLS: ${SKILL_COUNT} skill(s) discovered from ${SHARED_SKILLS_DIR}"
    echo -e "${SKILL_NAMES}"
fi

if [ -n "${DIRTY}" ]; then
    echo "${DIRTY}"
fi

if [ ${ERRORS} -gt 0 ]; then
    echo ""
    echo "  Shared skills may not trigger correctly. Check the setup."
fi

exit 0
```

Make it executable:

```bash
chmod +x scripts/verify-shared-skills.sh
```

### Step 4: Verify it works

Inside Claude Code, run:

```
/skills
```

You should see both your local skills AND the shared skills listed. The hook output on session start will show:

```
✓ SHARED SKILLS: 2 skill(s) discovered from ~/projects/shared-skills
  ✓ job-search
  ✓ cv-tailor
```

Or if something's wrong:

```
⚠ SHARED SKILLS: directory not found at ~/projects/shared-skills
  Clone it: git clone git@github.com:you/shared-skills.git ~/projects/shared-skills
```

---

## Contributing changes back

This is the key advantage over submodules and symlinks — **you edit the actual repo files**.

```bash
# 1. Edit the skill directly in the shared repo
cd ~/projects/shared-skills
vim .claude/skills/job-search/SKILL.md

# 2. The change is immediately visible in your Claude Code session
#    (--add-dir supports live reload — no restart needed)

# 3. When happy, commit and push
git add -A
git commit -m "Updated job search scoring criteria"
git push

# 4. Other repos/machines pull the latest
cd ~/projects/another-project
# Skills auto-update when shared-skills repo is pulled
```

The workflow is: **edit → test live → commit → push → pull on other machines**. No symlink recreation, no submodule update, no copy step.

---

## What gets git tracked where

| File | Repo | Purpose |
|------|------|---------|
| `.claude/skills/*/SKILL.md` | shared-skills | The actual skill definitions |
| `.claude/settings.json` | cowork repo (peter-pa) | Persists `additionalDirectories` |
| `.claude/hooks.json` | cowork repo (peter-pa) | Registers the PostStart verification hook |
| `scripts/verify-shared-skills.sh` | cowork repo (peter-pa) | The verification script itself |

The hook files (`hooks.json` and the script) are git tracked in your cowork repo, so anyone who clones it gets the verification automatically — they just need to clone the shared-skills repo to the expected path.

---

## Adding a new skill to the shared repo

```bash
cd ~/projects/shared-skills
mkdir -p .claude/skills/new-skill-name
cat > .claude/skills/new-skill-name/SKILL.md << 'EOF'
---
name: new-skill-name
description: "Trigger description — when should Claude invoke this skill"
---

# Skill Title

Your skill content here.
EOF

git add -A
git commit -m "Added new-skill-name skill"
git push
```

The new skill will be immediately discoverable in any Claude Code session that has `additionalDirectories` pointing to this repo.

---

## Troubleshooting

**Skills don't appear in `/skills` output:**
- Confirm `additionalDirectories` in `.claude/settings.json` points to the correct absolute path
- Check that each skill is at `.claude/skills/<name>/SKILL.md` (exactly one level deep)
- Run the verification script manually: `bash scripts/verify-shared-skills.sh`

**Hook doesn't fire:**
- Ensure `hooks.json` is in `.claude/hooks.json` (not `.claude/hooks/hooks.json`)
- Check the script is executable: `chmod +x scripts/verify-shared-skills.sh`
- The `matcher: "PostStart"` is case-sensitive

**Skills trigger in one repo but not another:**
- Each consuming repo needs its own `.claude/settings.json` with the `additionalDirectories` entry
- The shared-skills repo path must be consistent across machines (or use `${HOME}` in the verify script)

**Context window budget exceeded:**
- Claude Code caps skill metadata at ~2% of the context window
- If you have many skills, less-used ones may be silently hidden
- Check with `/context` and consider splitting into multiple shared repos by domain

---

## Why not submodules or symlinks?

| Approach | Discovery | Edit & push back | Fragility |
|----------|-----------|-------------------|-----------|
| Git submodule | Breaks (extra nesting depth) | Awkward (submodule commit dance) | Medium |
| Directory symlink | Often breaks (issues #764, #14836) | Works if symlink resolves | High |
| Per-skill symlinks | Sometimes works | Works | Medium-high |
| **--add-dir (this approach)** | **Reliable** | **Native git workflow** | **Low** |

The `--add-dir` approach is the only one that gives you reliable discovery, a clean edit-and-push workflow, and avoids the documented fragility of symlinks in Claude Code's skill scanner.
