# Sharing Claude Code Skills, Commands & Scripts Across Repos

## The problem

Claude Code discovers skills by scanning `.claude/skills/<n>/SKILL.md` only **one level deep**. Git submodules and nested directories create extra depth that breaks discovery silently. Symlinks are fragile and have broken across multiple Claude Code versions (issues #764, #10573, #14836, #25367). Neither approach lets you edit a skill in your working repo and push changes back to a shared source without leaving your project.

## The solution: `--add-dir` with a standalone shared-tools repo

Instead of embedding skills inside each project via submodules or symlinks, keep them in a **standalone sibling repo** and tell Claude Code to include it via `--add-dir`. This works for skills, slash commands, and scripts — anything Claude Code discovers from `.claude/`.

This gives you:

- **Reliable discovery** — skills, commands, and scripts sit at the exact depth Claude Code expects
- **Full git workflow** — edit, commit, push from the shared repo directly
- **No symlinks** — avoids all documented fragility
- **No duplication** — one source of truth, many consumers
- **Live reload** — changes are picked up mid-session without restarting
- **Push without leaving your project** — a `/push-skills` slash command handles it

---

## Directory layout

```
~/projects/
├── shared-skills/                        ← standalone git repo (the shared source)
│   ├── .claude/
│   │   ├── skills/                       ← auto-discovered skills
│   │   │   ├── job-search/
│   │   │   │   └── SKILL.md
│   │   │   └── cv-tailor/
│   │   │       └── SKILL.md
│   │   └── commands/                     ← shared slash commands
│   │       ├── push-skills.md            ← commit & push without leaving cowork
│   │       └── sync-all.md              ← pull latest shared skills
│   ├── scripts/                          ← shared utility scripts
│   │   ├── verify-shared-skills.sh       ← PostStart hook verification
│   │   └── push-shared-skills.sh         ← git add/commit/push helper
│   └── README.md
│
├── peter-pa/                             ← your cowork/project repo
│   ├── .claude/
│   │   ├── settings.json                 ← persists --add-dir config
│   │   ├── hooks.json                    ← PostStart hook for verification
│   │   └── skills/                       ← project-specific skills (optional)
│   │       └── local-only/
│   │           └── SKILL.md
│   ├── src/                              ← your actual project code
│   └── CLAUDE.md
│
└── another-project/                      ← any other repo can also use shared-skills
    └── .claude/
        └── settings.json                 ← same additionalDirectories entry
```

---

## Setup steps

### Step 1: Create the shared-skills repo

```bash
mkdir -p ~/projects/shared-skills/.claude/skills
mkdir -p ~/projects/shared-skills/.claude/commands
mkdir -p ~/projects/shared-skills/scripts
cd ~/projects/shared-skills
git init
```

### Step 2: Add your skills

Each skill needs its own subdirectory with a `SKILL.md` file:

```bash
mkdir -p .claude/skills/job-search
# Copy or create your SKILL.md
cat > .claude/skills/job-search/SKILL.md << 'EOF'
---
name: job-search
description: "Use this skill whenever Pete asks to search for jobs, find new roles,
  repeat a job search, or check for engineering leadership opportunities."
---

# Pete's Engineering Leadership Job Search

Your full skill content here...
EOF
```

### Step 3: Add the push-skills slash command

This is the key piece — it lets you commit and push shared skill changes **without leaving your cowork repo**.

Create `.claude/commands/push-skills.md`:

```markdown
Commit and push any changes in the shared-skills repo.

1. Run: `cd ~/projects/shared-skills && git status --short`
2. If there are no changes, tell me "No changes to push in shared-skills"
3. If there are changes, show me what changed and ask for a commit message
4. Once I provide a message (or say "go ahead"), run:
   ```
   cd ~/projects/shared-skills && git add -A && git commit -m "<message>" && git push
   ```
5. Report what was committed and pushed
```

Create `.claude/commands/sync-all.md`:

```markdown
Pull the latest shared skills from the remote.

1. Run: `cd ~/projects/shared-skills && git pull --rebase`
2. Report what changed (if anything)
3. Run: `cd ~/projects/shared-skills && find .claude/skills -name "SKILL.md" | sort`
4. List all available shared skills
```

### Step 4: Add the utility scripts

Create `scripts/verify-shared-skills.sh`:

```bash
#!/bin/bash
# verify-shared-skills.sh
# PostStart hook: confirms shared skills are discoverable.
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
        DIRTY="  ⚠ Uncommitted changes in shared-skills repo — run /push-skills"
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

Create `scripts/push-shared-skills.sh` (standalone version for use outside Claude Code):

```bash
#!/bin/bash
# push-shared-skills.sh
# Commit and push shared-skills changes from anywhere.
# Usage: bash ~/projects/shared-skills/scripts/push-shared-skills.sh "commit message"

SHARED_SKILLS_DIR="${HOME}/projects/shared-skills"

cd "${SHARED_SKILLS_DIR}" || { echo "Cannot find ${SHARED_SKILLS_DIR}"; exit 1; }

if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to push in shared-skills"
    exit 0
fi

echo "Changes found:"
git status --short
echo ""

MSG="${1:-Update shared skills}"
git add -A
git commit -m "${MSG}"
git push

echo ""
echo "✓ Shared skills pushed with message: ${MSG}"
```

Make both executable:

```bash
chmod +x scripts/verify-shared-skills.sh
chmod +x scripts/push-shared-skills.sh
```

### Step 5: Commit the shared-skills repo

```bash
cd ~/projects/shared-skills
git add -A
git commit -m "Initial shared skills, commands, and scripts"
git remote add origin git@github.com:you/shared-skills.git
git push -u origin main
```

### Step 6: Configure your cowork repo

Create `.claude/settings.json` in your cowork repo (e.g. `~/projects/peter-pa/`):

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

Create `.claude/hooks.json` in your cowork repo:

```json
{
  "hooks": [
    {
      "matcher": "PostStart",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/projects/shared-skills/scripts/verify-shared-skills.sh"
        }
      ]
    }
  ]
}
```

Note: the hook script path points to the **shared-skills repo** — so the verification logic itself is shared and updatable from one place. If you prefer the hook script to be local to the cowork repo, copy it to `./scripts/verify-shared-skills.sh` and update the path accordingly.

### Step 7: Verify it works

Launch Claude Code from your cowork repo:

```bash
cd ~/projects/peter-pa
claude
```

On session start, the hook should report:

```
✓ SHARED SKILLS: 2 skill(s) discovered from ~/projects/shared-skills
  ✓ job-search
  ✓ cv-tailor
```

Check with `/skills` to see both local and shared skills listed.

---

## Daily workflow

### Editing a shared skill

You're working in `peter-pa/` and want to update the job search skill. Just ask Claude to edit it — because `--add-dir` makes the shared repo's files visible, Claude can read and write to `~/projects/shared-skills/.claude/skills/job-search/SKILL.md` directly.

The change takes effect immediately (live reload).

### Pushing changes back (without leaving your project)

Type `/push-skills` in Claude Code. The slash command:

1. Checks the shared-skills repo for uncommitted changes
2. Shows you what changed
3. Asks for a commit message
4. Commits and pushes

You never leave your cowork repo.

Alternatively, from a terminal (without Claude Code):

```bash
bash ~/projects/shared-skills/scripts/push-shared-skills.sh "Updated scoring criteria"
```

### Pulling latest on another machine

```bash
cd ~/projects/shared-skills
git pull
```

Any Claude Code session with `additionalDirectories` pointing here picks up the changes automatically.

---

## What gets git tracked where

| File | Lives in | Purpose |
|------|----------|---------|
| `.claude/skills/*/SKILL.md` | shared-skills | The actual skill definitions |
| `.claude/commands/push-skills.md` | shared-skills | Slash command to push without leaving cowork |
| `.claude/commands/sync-all.md` | shared-skills | Slash command to pull latest |
| `scripts/verify-shared-skills.sh` | shared-skills | PostStart hook verification |
| `scripts/push-shared-skills.sh` | shared-skills | Standalone push helper |
| `.claude/settings.json` | cowork repo | Persists `additionalDirectories` |
| `.claude/hooks.json` | cowork repo | Registers the PostStart hook |

The key insight: **almost everything lives in the shared-skills repo**. The cowork repo only needs two small config files (`settings.json` and `hooks.json`) to wire it all up.

---

## Adding a new skill

```bash
cd ~/projects/shared-skills
mkdir -p .claude/skills/new-skill
cat > .claude/skills/new-skill/SKILL.md << 'EOF'
---
name: new-skill
description: "When to trigger this skill"
---

# Skill content here
EOF
```

Or just ask Claude to create it — since the shared-skills directory is visible via `--add-dir`, Claude can create files there directly.

Then `/push-skills` to commit and push.

---

## Adding a new slash command

```bash
cat > ~/projects/shared-skills/.claude/commands/my-command.md << 'EOF'
Description of what this command does.

Steps Claude should follow when /my-command is invoked.
EOF
```

The command becomes available as `/my-command` in any Claude Code session that includes the shared-skills repo via `--add-dir`.

---

## Sharing across multiple projects

Every project that wants access to the shared tools just needs one file:

`.claude/settings.json`:
```json
{
  "additionalDirectories": [
    "~/projects/shared-skills"
  ]
}
```

And optionally the hooks.json for verification. That's it.

---

## Troubleshooting

**Skills don't appear in `/skills` output:**
- Confirm `additionalDirectories` in `.claude/settings.json` points to the correct path
- Check that each skill is at `.claude/skills/<n>/SKILL.md` (exactly one level deep)
- Run the verification script manually: `bash ~/projects/shared-skills/scripts/verify-shared-skills.sh`

**Hook doesn't fire:**
- Ensure `hooks.json` is at `.claude/hooks.json` (not `.claude/hooks/hooks.json`)
- Check the script path is correct and the script is executable
- `PostStart` is case-sensitive

**Context window budget exceeded:**
- Claude Code caps skill metadata at ~2% of the context window (~52 skills with typical descriptions)
- If you have many skills, less-used ones may be silently hidden
- Check with `/context` and consider splitting into multiple shared repos by domain

**`/push-skills` fails:**
- Ensure the shared-skills repo has a remote configured: `cd ~/projects/shared-skills && git remote -v`
- Check you have push access to the remote

---

## Why not submodules or symlinks?

| Approach | Discovery | Edit & push | Fragility | Shared commands |
|----------|-----------|-------------|-----------|-----------------|
| Git submodule | Breaks (extra nesting) | Awkward | Medium | No |
| Directory symlink | Often breaks | Works if resolves | High | No |
| Per-skill symlinks | Sometimes works | Works | Medium-high | No |
| **--add-dir** | **Reliable** | **Native git** | **Low** | **Yes** |

The `--add-dir` approach is the only one that reliably discovers skills, provides a clean git workflow for contributing changes, avoids symlink fragility, and shares slash commands and scripts alongside skills.
