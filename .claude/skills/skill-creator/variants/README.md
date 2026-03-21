# A/B Variant Testing

Test skill variants side-by-side to find the best performing version.

## Convention

Variants live **inside the skill they belong to**, not in a centralized directory:

```
.claude/skills/mermaid-diagram/
├── SKILL.md                    ← active (champion)
├── evals/
│   ├── trigger-eval.json       ← eval queries
│   └── results/                ← eval run outputs (gitignored)
└── variants/
    ├── A/SKILL.md              ← champion copy (for comparison)
    └── B/SKILL.md              ← challenger
```

## Workflow

1. **Create variant** — copy the active SKILL.md to `variants/A/SKILL.md`, write alternative at `variants/B/SKILL.md`
2. **Run evals** — test both variants against the skill's eval set:
   ```bash
   python -m scripts.run_eval --eval-set <skill>/evals/trigger-eval.json --skill-path <skill>/variants/A
   python -m scripts.run_eval --eval-set <skill>/evals/trigger-eval.json --skill-path <skill>/variants/B
   ```
3. **Compare** — the comparator agent (`agents/comparator.md`) analyzes results
4. **Promote** — copy the winner to `<skill>/SKILL.md`
