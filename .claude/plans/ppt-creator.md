# PPT Creator Skill Plan

> **For execution:** Use `/run-agent` to implement this plan.

## Overview

Create a `ppt-create` skill that assembles pre-rendered Excalidraw diagram PNGs and markdown content into visually impressive PowerPoint presentations. The skill recommends 2 variants (A and B) from 12 presentation archetypes, applies technical writing principles, and uses a build-validate-fix loop.

Research basis: `.claude/plans/pptx-report-skill-handoff.md` and `.claude/plans/pptx-report-skill-addendum.md`.

## Feature List

See: `.claude/plans/ppt-creator-features.json`

Total features: 13
Passing: 0

## Task Groups

| Batch | Features | Theme |
|-------|----------|-------|
| 1 | F001-F004 | Core deck builder: pyproject.toml, palettes, slide types, build_deck.py |
| 2 | F005-F006 | Markdown parser + manifest schema docs |
| 3 | F007-F010 | SKILL.md + reference docs (archetypes, writing style, design principles) |
| 4 | F011-F012 | Validation script + end-to-end test |
| 5 | F013 | Trigger and implementation evals |

## Files to Create

All files are new — no existing files modified.

```
.claude/skills/ppt-create/
├── SKILL.md                          # F007: Workflow: interview → archetype → build → validate
├── references/
│   ├── pyproject.toml                # F001: uv-managed deps (python-pptx, Pillow, mistune)
│   ├── palettes.md                   # F002: 12 palette definitions with hex values
│   ├── slide-types.md                # F003: 9 slide type specs with layout details
│   ├── manifest-schema.md            # F005: JSON manifest format with examples
│   ├── archetypes.md                 # F008: 12 archetype definitions
│   ├── writing-style.md              # F009: Technical writing guide for slides
│   └── design-principles.md          # F010: Anthropic's design rules + typography
├── scripts/
│   ├── build_deck.py                 # F004: Core JSON manifest → .pptx builder
│   ├── parse_report.py               # F006: Markdown + images → JSON manifest
│   └── validate_deck.py              # F011: Structural + optional visual QA
└── evals/
    ├── trigger-eval.json             # F013: 20 trigger/no-trigger queries
    └── implementation-eval.json      # F013: 5 implementation test cases
```

**Why scripts/ not tools/**: Pete said tools/ is for CLI-type support. These are skill-internal helpers Claude invokes, matching the mermaid-diagram pattern (`.claude/skills/mermaid-diagram/scripts/`). No new entry points in root `pyproject.toml`.

**Why uv not poetry**: Follows excalidraw-diagram's pattern (`.claude/skills/excalidraw-diagram/references/pyproject.toml`) — skill-local deps isolated from the repo's poetry package.

## Test Strategy

- **Unit tests:** Each script tested individually via CLI invocation with test fixtures
- **Integration test (F012):** Full workflow — create test manifest + test PNG → build_deck.py → validate_deck.py → verify .pptx structure
- **Trigger eval (F013):** 10 should-trigger, 10 should-not queries
- **Implementation eval (F013):** 5 scenarios with assertions on output
- **Test isolation:** Each test creates temp dirs, cleans up after. No shared state between tests.

## Debug & Operating Notes

- **Pattern to follow**: mermaid-diagram skill structure for scripts, excalidraw-diagram for uv/pyproject.toml in references/
- **Scripts run via**: `cd .claude/skills/ppt-create/references && uv run python ../scripts/build_deck.py --manifest <path> --output <path>`
- **python-pptx quirk**: Use `slide_layouts[6]` (blank layout) for all slides — build everything programmatically
- **Windows**: `shell=True` for any subprocess calls (consistent with codebase convention)
- **Image handling**: `add_picture()` auto-scales height when only width is specified — use this for aspect ratio preservation
- **Font availability**: Georgia and Calibri are standard Windows fonts. On other OS, python-pptx will substitute — this is acceptable
- **Pete's exception pattern**: Every function wraps in try/except with `inspect.currentframe().f_code.co_name` + logger.warning + re-raise

## Incremental Order

### Batch 1: Core deck builder (F001-F004)

1. **F001** — `references/pyproject.toml` (blocking — needed for `uv sync` before any script runs)
   - deps: python-pptx>=1.0.0, Pillow>=10.0.0, mistune>=3.0.0
   - Run `uv sync` to generate `uv.lock`

2. **F002** — `references/palettes.md` (independent, referenced by F004)
   - 12 palettes, each with: bg, fg, accent, accent2, muted, highlight, error
   - midnight (1E1E2E), charcoal (36454F), ocean (0D1B2A) from handoff
   - 9 additional: sage-calm, berry-cream, cherry-bold, forest-moss, coral-energy, ocean-gradient, midnight-exec, warm-terracotta, teal-trust
   - Each palette maps to 1-2 archetypes

3. **F003** — `references/slide-types.md` (independent, referenced by F004)
   - 9 slide types: title, section_header, content, diagram, diagram_full, metrics, two_column, comparison, closing
   - Each type: description, required fields, optional fields, layout specs (positions in Inches), typography

4. **F004** — `scripts/build_deck.py` (depends on F001-F003)
   - ~400 lines, argparse CLI: `--manifest <json>` `--output <pptx>`
   - Load JSON manifest → iterate slides → dispatch to type-specific renderer function
   - 9 renderer functions matching slide-types.md
   - Palette dict loaded from manifest metadata, passed to each renderer
   - Typography: Georgia headings 36-44pt bold, Calibri body 14-16pt, captions 10-12pt italic muted
   - Acceptance: create a 3-slide test manifest (title + diagram + closing), run build_deck.py, verify .pptx opens with correct slides

### Batch 2: Markdown parser + manifest docs (F005-F006)

5. **F005** — `references/manifest-schema.md` (independent)
   - Full JSON schema documentation with examples for each slide type
   - metadata block: title, subtitle, author, date, archetype, palette
   - slides array: type-specific field definitions

6. **F006** — `scripts/parse_report.py` (depends on F005)
   - ~200 lines, argparse CLI: `--input <md>` `--images <dir>` `--archetype <name>` `--output <json>`
   - Uses mistune 3.x AST parsing
   - Mapping: H1→title/section_header, H2→section_header, H3→content, bullets→bullets, images→diagram/diagram_full, bold-colon→metrics
   - Scans --images dir, matches filenames from markdown
   - Acceptance: parse test markdown with 3 sections + 1 image ref, verify JSON output has correct slide types

### Batch 3: SKILL.md + reference docs (F007-F010)

7. **F007** — `SKILL.md` (~350 lines, depends on all references existing)
   - YAML frontmatter: name=ppt-create, trigger description, version=0.1.0
   - Workflow: Before You Start → Interview → Archetype Selection → Content Generation → Build → Validate & Fix → Deliver
   - Intent routing table (phase → which reference to load)
   - Interview: 4 questions (goal, audience, content mix, length) — skip if context provides answers
   - Variant A/B: present 2 archetype recommendations, user picks or gets both
   - Scripts table documenting when to use each script

8. **F008** — `references/archetypes.md` (~300 lines)
   - 12 archetypes from addendum: Executive Summary, Technical Deep-Dive, Architecture Review, Data Analysis Dashboard, Project Status Update, Proposal/Business Case, Incident/Post-Mortem, Training/Knowledge Transfer, Sprint/Demo Day, Comparison/Evaluation, Quarterly Review, Research/Investigation
   - Each: when to use, default slide sequence, recommended palette, layout style, slide count range
   - Decision matrix: goal × audience → recommended archetypes

9. **F009** — `references/writing-style.md` (~150 lines)
   - Title rules: action-oriented, lead with conclusion, max 8 words
   - Bullet rules: parallel structure, front-load data, max 5/slide, max 2 lines each
   - Prose: active voice, concrete > abstract, data-first
   - Captions: describe what to notice, under 15 words
   - Anti-patterns: generic agendas, AI prose, filler phrases

10. **F010** — `references/design-principles.md` (~100 lines)
    - 10 Anthropic design rules (no boring slides, colour dominance 60-70%, vary layouts, breathing room, etc.)
    - Typography table (sizes, weights per element type)
    - Layout constraints (0.5" margins, 0.3-0.5" between blocks)
    - Never use accent lines under titles

### Batch 4: Validation + end-to-end test (F011-F012)

11. **F011** — `scripts/validate_deck.py` (~150 lines)
    - argparse CLI: `--input <pptx>` `--output-dir <dir>` `--json`
    - Structural validation (always): slide count, no empty slides, images embedded, title/closing present, text lengths
    - Visual validation (when soffice available): render to PNG, report dimensions
    - Graceful degradation: warn + structural-only if LibreOffice absent
    - Acceptance: validate the test .pptx from F004, verify JSON report is correct

12. **F012** — End-to-end integration test
    - Create test markdown + test PNG image
    - Run parse_report.py → manifest JSON
    - Run build_deck.py → .pptx
    - Run validate_deck.py → verify passes
    - Open .pptx with python-pptx and assert: slide count, background colors match palette, images embedded

### Batch 5: Evals (F013)

13. **F013** — `evals/trigger-eval.json` + `evals/implementation-eval.json`
    - Trigger: 10 should-trigger ("make a deck", "create a presentation", "build a pptx", "PowerPoint from these diagrams", "turn this into slides"), 10 should-not ("mermaid diagram", "excalidraw diagram", "markdown report", "review PR", "fix bug")
    - Implementation: 5 scenarios (executive summary, architecture review with PNGs, incident post-mortem, comparison deck, training deck)

## Code Review

After all batches complete, `/run-agent` dispatches a `reviewer` agent to check:
- All requirements met (line by line against this plan)
- Code quality: type hints, docstrings, Pete's exception pattern
- Reference docs complete and internally consistent
- No scope creep

## Documentation Sweep

| File | Check for |
|------|-----------|
| `CLAUDE.md` | Add ppt-create to Skills table |
| Root `pyproject.toml` | No changes needed (skill uses own uv-managed deps) |

## Acceptance Criteria

- All 13 features in `ppt-creator-features.json` have `passes: true`
- `uv sync` succeeds in `references/`
- `build_deck.py` produces valid .pptx from test manifest
- `parse_report.py` converts markdown to correct JSON manifest
- `validate_deck.py` reports no structural issues on generated .pptx
- Generated .pptx opens in PowerPoint with correct dark palette, fonts, and embedded images
- SKILL.md follows mermaid-diagram pattern (frontmatter, intent routing, scripts table)
- Trigger eval has 20 queries with correct expected outcomes
