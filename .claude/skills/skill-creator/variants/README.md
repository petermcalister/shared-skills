# A/B Variant Testing

Test skill variants side-by-side to find the best performing version.

## Workflow

1. **Create variant** — copy the champion skill to `variants/{skill-name}/A/SKILL.md`, create alternative at `variants/{skill-name}/B/SKILL.md`
2. **Run evals** — `python skill-creator/scripts/run_eval.py --variant-a variants/{skill}/A --variant-b variants/{skill}/B`
3. **Compare** — the comparator agent analyzes results and recommends a winner
4. **Promote** — copy the winner back to `skills/{skill-name}/SKILL.md`

## Directory Convention

```
variants/
  {skill-name}/
    A/SKILL.md    # Champion (current best)
    B/SKILL.md    # Challenger (new approach)
```
