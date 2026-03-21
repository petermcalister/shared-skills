#!/bin/bash
# verify-shared-skills.sh
# SessionStart hook: confirms shared skills are discoverable.
# Customise SHARED_SKILLS_DIR to match your layout.

SHARED_SKILLS_DIR="C:/Users/peter/RepoBase/shared-skills"
SKILLS_PATH="${SHARED_SKILLS_DIR}/.claude/skills"
ERRORS=0

# ─── Check 1: Does the shared-skills directory exist? ───
if [ ! -d "${SHARED_SKILLS_DIR}" ]; then
    echo "⚠ SHARED SKILLS: directory not found at ${SHARED_SKILLS_DIR}"
    echo "  Clone it:  git clone git@github.com:petermcalister/shared-skills.git ${SHARED_SKILLS_DIR}"
    exit 0
fi

# ─── Check 2: Does the .claude/skills/ directory exist? ───
if [ ! -d "${SKILLS_PATH}" ]; then
    echo "⚠ SHARED SKILLS: ${SKILLS_PATH} not found"
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
    ERRORS=$((ERRORS + 1))
fi

# ─── Check 4: Warn about uncommitted changes ───
DIRTY=""
if [ -d "${SHARED_SKILLS_DIR}/.git" ]; then
    cd "${SHARED_SKILLS_DIR}"
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        DIRTY="  ⚠ Uncommitted changes in shared-skills — run /push-skills"
    fi
    cd - > /dev/null
fi

# ─── Report ───
if [ ${SKILL_COUNT} -gt 0 ]; then
    echo "✓ SHARED SKILLS: ${SKILL_COUNT} skill(s) from ${SHARED_SKILLS_DIR}"
    echo -e "${SKILL_NAMES}"
fi

if [ -n "${DIRTY}" ]; then
    echo "${DIRTY}"
fi

exit 0
