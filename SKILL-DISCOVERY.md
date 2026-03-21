# Skill Discovery Problem

## The Problem

Claude Code discovers skills by scanning `.claude/skills/<name>/SKILL.md` — **one level deep** from the skills directory. When this repo is mounted as a git submodule at `.claude/skills/shared/`, the actual skill paths become:

```
.claude/skills/shared/skills/mermaid-diagram/SKILL.md      ← 3 levels deep
.claude/skills/shared/skills/excalidraw-diagram/SKILL.md    ← 3 levels deep
.claude/skills/shared/skill-creator/SKILL.md                ← 2 levels deep
```

**None of these are discovered.** They don't appear in the skill list shown to the agent at session start, can't be triggered by description matching, and are effectively invisible unless the agent already knows to look inside `shared/`.

### Why This Matters

- Skills that aren't discovered can't be triggered naturally by the user
- The agent has no idea these skills exist unless told explicitly
- This defeats the purpose of packaging skills for reuse

## Current Layout

```
shared-skills/                    # This repo (mounted as submodule)
├── skills/                       # Graduated skills
│   ├── mermaid-diagram/SKILL.md
│   └── excalidraw-diagram/SKILL.md
├── skill-creator/SKILL.md        # Skill creation framework
├── template/SKILL.md             # Skeleton template (not a real skill)
└── variants/                     # A/B test variants
```

When consumed at `.claude/skills/shared/`, the `skills/` subfolder adds an extra nesting level that breaks discovery.

## Solutions

### Option A: Symlinks in the Consumer Project

Create symlinks in the consumer's `.claude/skills/` that point into the submodule:

```bash
# In the consumer project (e.g. cowork/)
cd .claude/skills
ln -s shared/skills/mermaid-diagram mermaid-diagram
ln -s shared/skills/excalidraw-diagram excalidraw-diagram
```

**Result:**
```
.claude/skills/
├── mermaid-diagram → shared/skills/mermaid-diagram   ← discovered
├── excalidraw-diagram → shared/skills/excalidraw-diagram  ← discovered
├── shared/                                            ← submodule (unchanged)
│   └── skills/mermaid-diagram/SKILL.md               ← source of truth
└── brainstorming/SKILL.md                            ← local skill
```

| Pros | Cons |
|------|------|
| No changes to this repo | Each consumer must create symlinks |
| Skills discovered natively | Symlinks need setup instructions |
| Edits go through submodule (correct ownership) | Windows symlinks may need admin/dev mode |
| Git tracks symlinks | Consumer must know which skills to link |

**Editability:** Edits through the symlink modify the submodule working tree. Commits still require the two-step submodule flow (commit in submodule, then update pointer in parent). This is the same with or without symlinks — the submodule boundary is what creates the two-step flow, not the symlink.

### Option B: Flatten This Repo's Structure

Move skills to the repo root so that when mounted at `.claude/skills/shared/`, each skill is exactly two levels deep:

```
shared-skills/                    # This repo
├── mermaid-diagram/SKILL.md      ← .claude/skills/shared/mermaid-diagram/SKILL.md
├── excalidraw-diagram/SKILL.md
├── skill-creator/SKILL.md
├── _template/SKILL.md            ← prefixed to avoid discovery
├── _variants/                    ← prefixed to avoid discovery
├── _meta/                        ← repo docs, feature tracking
│   ├── shared-skills.md
│   └── shared-skills-features.json
└── CLAUDE.md
```

**But this still won't work** — Claude Code scans `.claude/skills/` one level deep, so `shared/mermaid-diagram/SKILL.md` is still two levels away from `.claude/skills/`.

The submodule mount point **is** one of those levels. Unless the submodule is mounted directly at `.claude/skills/` (which would conflict with local skills), flattening alone doesn't solve discovery.

### Option C: Mount Submodule at a Different Path + Symlinks

Mount the submodule outside the skills directory (e.g. `.claude/shared-skills/`) and symlink individual skills into `.claude/skills/`:

```
.claude/
├── shared-skills/                 ← submodule (not in skills/)
│   └── skills/mermaid-diagram/SKILL.md
└── skills/
    ├── mermaid-diagram → ../shared-skills/skills/mermaid-diagram  ← discovered
    └── brainstorming/SKILL.md                                     ← local skill
```

| Pros | Cons |
|------|------|
| Clean separation of shared vs local | Still requires symlinks |
| Submodule path doesn't pollute skills dir | Submodule path change needed |
| No accidental discovery of template/variants | More complex setup |

### Option D: Duplicate SKILL.md as Thin Wrappers

Keep the submodule as-is, but create lightweight wrapper skills in the consumer that delegate to the shared skill:

```
.claude/skills/mermaid-diagram/SKILL.md  ← thin wrapper that says "read and follow .claude/skills/shared/skills/mermaid-diagram/SKILL.md"
```

| Pros | Cons |
|------|------|
| No symlinks needed | Wrapper drift — two files to keep in sync |
| Works on all platforms | Indirection adds complexity |
| Consumer controls trigger description | Edits to wrapper don't flow back to shared |

## Recommendation

**Option A (symlinks)** is the pragmatic choice:

1. Zero changes to this repo's structure
2. Consumer creates symlinks once during setup
3. Ownership stays clean — edits flow through the submodule
4. Works with git (symlinks are tracked as path references)

The setup instructions in the consumer project should include a post-submodule-add step:

```bash
# After adding the submodule
cd .claude/skills
for skill in shared/skills/*/; do
    name=$(basename "$skill")
    [ ! -e "$name" ] && ln -s "$skill" "$name"
done
```

### Windows Note

On Windows, symlinks require either:
- **Developer Mode** enabled (Settings > For Developers), or
- Running the terminal as Administrator

Git for Windows supports symlinks if `core.symlinks=true` is set:
```bash
git config --global core.symlinks true
```

Without this, git will create text files containing the target path instead of actual symlinks — which won't work for skill discovery.

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| — | *Pending* | — |
