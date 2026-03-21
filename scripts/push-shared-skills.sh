#!/bin/bash
# push-shared-skills.sh
# Commit and push shared-skills changes from anywhere.
# Usage: bash C:/Users/peter/RepoBase/shared-skills/scripts/push-shared-skills.sh "commit message"

SHARED_SKILLS_DIR="C:/Users/peter/RepoBase/shared-skills"

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
echo "✓ Shared skills pushed: ${MSG}"
