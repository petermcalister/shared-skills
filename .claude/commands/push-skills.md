Commit and push any changes in the shared-skills repo.

1. Run: `cd C:/Users/peter/RepoBase/shared-skills && git status --short`
2. If there are no changes, tell me "No changes to push in shared-skills"
3. If there are changes, show me what changed and ask for a commit message
4. Once I provide a message (or say "go ahead"), run:
   ```
   cd C:/Users/peter/RepoBase/shared-skills && git add -A && git commit -m "<message>" && git push
   ```
5. Report what was committed and pushed
