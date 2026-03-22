---
name: ppt-create
description: >
  Use when the user wants to create a PowerPoint presentation, build a deck, turn markdown into slides,
  or assemble diagrams into a .pptx. Triggers on: "make a deck", "create a presentation", "build a pptx",
  "PowerPoint from these diagrams", "turn this into slides", "present this report".
version: 0.1.0
---

# PowerPoint Creator Skill

Generate professional PowerPoint decks from content, diagrams, and data.

## How This Skill Works

1. **Interview** the user to select an archetype and palette
2. **Generate** a JSON manifest describing every slide
3. **Build** the .pptx with `build_deck.py`
4. **Validate** the output and fix any issues
5. **Deliver** the final file

## Step 1 — Before You Start

Install dependencies (one-time, idempotent):

```bash
cd .claude/skills/ppt-create/references && uv sync
```

All Python commands below must run from the `references/` directory so `uv run` picks up the local venv.

## Step 2 — Interview

Ask the user four questions. Skip any that the context already answers.

1. **Goal** — What is the purpose of this presentation?
   - Inform, persuade, review, educate, or propose

2. **Audience** — Who will see it?
   - Technical peers, leadership, mixed, or external

3. **Content mix** — What kind of content dominates?
   - Diagrams, data/metrics, narrative, or balanced

4. **Length** — How many slides?
   - Short (5-8), medium (10-15), or long (15+)

## Step 3 — Archetype Selection

Based on the interview answers, recommend **two variants** (A and B) from the 12 archetypes.

Load the archetype catalogue:

```
references/archetypes.md
```

Present both options with their default slide sequence, palette, and slide count range. The user picks one, or you generate both for comparison.

## Step 4 — Content Generation

Apply these references while generating slide content:

| Phase | Reference to load |
|-------|-------------------|
| Content writing | `references/writing-style.md` |
| Layout planning | `references/slide-types.md`, `references/design-principles.md` |
| Palette selection | `references/palettes.md` |
| Manifest format | `references/manifest-schema.md` |

### Content workflow

1. Read `references/writing-style.md` and apply its title, bullet, prose, and caption rules.
2. Read `references/design-principles.md` and follow the 10 design rules for layout variety.
3. Read `references/slide-types.md` to understand available slide types and their required fields.
4. Read `references/palettes.md` to confirm the chosen palette's colour values.
5. Read `references/manifest-schema.md` for the JSON structure.
6. Generate the JSON manifest. Every slide must have a `type` field matching one of the registered slide types.

Write the manifest to a `.json` file next to the intended output location.

## Step 5 — Build

Run the build script:

```bash
cd .claude/skills/ppt-create/references && uv run python ../scripts/build_deck.py --manifest <path-to-manifest.json> --output <path-to-output.pptx>
```

If the build fails, read the error output, fix the manifest, and retry.

## Step 6 — Validate and Fix

Run the validation script:

```bash
cd .claude/skills/ppt-create/references && uv run python ../scripts/validate_deck.py --input <path-to-output.pptx> --json
```

Review the JSON output for issues. Common fixes:

- **Missing image**: update the `image_path` to a valid file or switch to a non-image slide type
- **Empty slide**: add body text or bullets
- **Layout violation**: check `references/design-principles.md` rule 6 (vary layouts)
- **Title too long**: apply the 8-word rule from `references/writing-style.md`

Fix the manifest and rebuild. **Always run at least one validate-fix cycle** even if the first build succeeds — validation catches layout and content issues that aren't build errors.

## Step 7 — Deliver

Present the final `.pptx` file path to the user. Include a summary:

- Number of slides
- Archetype used
- Palette applied
- Any notable content decisions

## Intent Routing

Read only the reference you need for the current phase:

| Phase | Reference |
|-------|-----------|
| Interview | (inline questions above) |
| Archetype selection | `references/archetypes.md` |
| Content writing | `references/writing-style.md` |
| Layout planning | `references/slide-types.md`, `references/design-principles.md` |
| Palette selection | `references/palettes.md` |
| Manifest format | `references/manifest-schema.md` |
| Build | `scripts/build_deck.py` |
| Parse markdown | `scripts/parse_report.py` |
| Validate | `scripts/validate_deck.py` |

All paths are relative to this skill's directory (`.claude/skills/ppt-create/`).

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `build_deck.py` | JSON manifest to .pptx | `--manifest <json> --output <pptx>` |
| `parse_report.py` | Markdown to JSON manifest | `--input <md> --images <dir> --archetype <name> --output <json>` |
| `validate_deck.py` | Validate .pptx structure | `--input <pptx> --output-dir <dir> --json` |

## Available Slide Types

Nine types are supported (see `references/slide-types.md` for full layout specs):

| Type | Description |
|------|-------------|
| `title` | Opening slide with title, subtitle, date |
| `section_header` | Section divider |
| `content` | Title + prose + optional bullets |
| `diagram` | Title + image + optional caption |
| `diagram_full` | Full-bleed image with title overlay |
| `metrics` | Large stat callouts |
| `two_column` | Side-by-side content |
| `comparison` | Before/after or pros/cons |
| `closing` | Final slide with summary or CTA |

## Available Palettes

Twelve palettes (see `references/palettes.md` for hex values):

`midnight`, `charcoal`, `ocean`, `sage-calm`, `berry-cream`, `cherry-bold`, `forest-moss`, `coral-energy`, `ocean-gradient`, `midnight-exec`, `warm-terracotta`, `teal-trust`

## Quick Tips

- Always run `uv sync` from `references/` before the first build
- Image paths in the manifest are relative to the manifest file's directory
- Use `diagram` for captioned images, `diagram_full` for full-bleed impact shots
- Keep manifests next to the images they reference for clean relative paths
- The `archetype` metadata field is informational; slide sequence is what matters
