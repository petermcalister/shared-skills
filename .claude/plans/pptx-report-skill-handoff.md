# Cowork Report Presenter Skill — Implementation Handoff

## Context & Goal

Pete is a data engineer building a personal AI assistant called **Cowork**. He produces technical reports and architecture documentation that combine markdown prose with pre-rendered Excalidraw diagram images (PNG). He needs a Claude Code skill and supporting Python scripts/CLI that can assemble these into a **visually impressive PowerPoint presentation**.

The user will supply:
- Markdown content (headings, paragraphs, bullet points, key metrics)
- Pre-rendered PNG images (Excalidraw architecture diagrams, flowcharts, etc.)
- Optionally: a theme/palette preference

The skill must produce:
- A polished `.pptx` file with professional design (not generic white-background bullet slides)
- Diagrams embedded as full-bleed or prominently placed images
- A dark theme aesthetic consistent with Pete's dashboard work (`assets/style.css` uses a dark palette)

---

## Architecture Overview

```
report-presenter/
├── SKILL.md                    # Required: skill instructions + YAML frontmatter
├── references/
│   ├── design-guide.md         # Colour palettes, typography, layout patterns
│   └── slide-types.md          # Catalogue of slide type templates (title, diagram, metrics, etc.)
├── scripts/
│   ├── build_deck.py           # Core CLI: markdown + images → .pptx
│   ├── parse_report.py         # Markdown parser → structured section list
│   └── validate_deck.py        # QA: convert to images, check for issues
└── assets/
    └── template.pptx           # Optional: base template with master slides/fonts
```

---

## SKILL.md Requirements

The SKILL.md frontmatter must include:

```yaml
---
name: report-presenter
description: >
  Create visually impressive PowerPoint presentations from markdown content and
  pre-rendered diagram images (PNG/JPG). Use this skill whenever the user wants to
  turn a report, architecture doc, analysis, or any markdown content with diagrams
  into a presentation. Triggers on: "make a deck", "create a presentation from",
  "turn this into slides", "present this report", "build a pptx", or any request
  combining text content with images into a .pptx output. Also use when the user
  provides Excalidraw PNGs alongside markdown and wants a polished visual output.
---
```

The body should define a clear workflow:

1. **Parse** — Read the markdown input and catalogue available images
2. **Plan** — Decide slide count, assign content to slide types, select palette
3. **Build** — Run `build_deck.py` to generate the `.pptx`
4. **Validate** — Convert to images and visually inspect (subagent if available)
5. **Fix & Re-validate** — At least one fix cycle before declaring success

---

## Core Script: `build_deck.py`

### Purpose

CLI tool that takes a structured JSON manifest (or markdown file + image directory) and produces a `.pptx` using `python-pptx`.

### Interface

```bash
python scripts/build_deck.py \
    --input report.md \
    --images ./diagrams/ \
    --output ./outputs/report-deck/final.pptx \
    --palette dark \
    --title "Database Cost Analysis Q4"
```

Alternatively, accept a JSON manifest for full control:

```bash
python scripts/build_deck.py \
    --manifest slides.json \
    --output ./outputs/report-deck/final.pptx
```

### JSON Manifest Schema

```json
{
    "title": "Database Cost Analysis Q4",
    "subtitle": "Cost per GB by Application Workload",
    "author": "Pete",
    "palette": "midnight",
    "font_heading": "Georgia",
    "font_body": "Calibri",
    "slides": [
        {
            "type": "title",
            "title": "Database Cost Analysis Q4",
            "subtitle": "Architecture Efficiency Review"
        },
        {
            "type": "section_header",
            "title": "Storage Spend Overview"
        },
        {
            "type": "content",
            "title": "Key Findings",
            "body": "Total database spend increased 12% QoQ...",
            "bullets": [
                "PostgreSQL clusters account for 45% of total spend",
                "Cost-per-GB ranges from £2.10 to £18.40 across applications",
                "Three applications exceed the £10/GB efficiency threshold"
            ]
        },
        {
            "type": "diagram",
            "title": "System Architecture",
            "image_path": "./diagrams/architecture.png",
            "caption": "Figure 1: Current database topology"
        },
        {
            "type": "metrics",
            "title": "Cost per GB by Application",
            "metrics": [
                {"label": "App Alpha", "value": "£2.10/GB", "trend": "down"},
                {"label": "App Beta", "value": "£8.50/GB", "trend": "flat"},
                {"label": "App Gamma", "value": "£18.40/GB", "trend": "up"}
            ]
        },
        {
            "type": "two_column",
            "title": "Before vs After Migration",
            "left": {"heading": "Legacy Stack", "body": "Oracle RAC on bare metal..."},
            "right": {"heading": "Target State", "body": "PostgreSQL on K8s..."},
            "image_path": "./diagrams/migration_flow.png"
        },
        {
            "type": "diagram_full",
            "title": "Cost Breakdown by Service",
            "image_path": "./diagrams/cost_breakdown.png"
        },
        {
            "type": "closing",
            "title": "Next Steps",
            "bullets": [
                "Migrate App Gamma to shared PostgreSQL cluster",
                "Implement storage tiering for cold data",
                "Review Q1 targets with platform team"
            ]
        }
    ]
}
```

### Slide Types to Implement

Each slide type maps to a python-pptx construction function:

| Type | Description | Image Support |
|------|-------------|---------------|
| `title` | Opening slide: large title, subtitle, date | Optional background image |
| `section_header` | Section divider with bold heading | No |
| `content` | Title + prose paragraph + optional bullet points | No |
| `diagram` | Title + prominently placed image + optional caption | **Yes — primary use case** |
| `diagram_full` | Full-bleed image with minimal title overlay | **Yes — hero image** |
| `metrics` | Large stat callouts (big numbers 60-72pt) | No |
| `two_column` | Side-by-side content blocks, optional image | Optional |
| `comparison` | Before/after or pros/cons layout | Optional |
| `closing` | Final slide with summary bullets or call to action | No |

### Image Handling

This is critical — the whole point of the skill is embedding pre-rendered diagrams beautifully.

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def add_diagram_slide(
    prs: Presentation,
    title: str,
    image_path: str,
    caption: str = None,
    palette: dict = None
) -> None:
    """Add a slide with a prominently placed diagram image.

    Args:
        prs: The Presentation object.
        title: Slide title text.
        image_path: Path to the PNG/JPG image file.
        caption: Optional caption below the image.
        palette: Colour palette dict with keys: bg, fg, accent, muted.

    Raises:
        FileNotFoundError: If image_path does not exist.
    """
    try:
        slide_layout = prs.slide_layouts[6]  # blank layout
        slide = prs.slides.add_slide(slide_layout)

        # Set background colour
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor.from_string(palette["bg"])

        # Add title
        from pptx.util import Inches, Pt
        txBox = slide.shapes.add_textbox(
            Inches(0.8), Inches(0.4), Inches(8.4), Inches(0.8)
        )
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(palette["fg"])

        # Add image — centred, max width 8.5 inches, auto-scale height
        slide.shapes.add_picture(
            image_path,
            left=Inches(0.75),
            top=Inches(1.5),
            width=Inches(8.5)
            # height auto-calculated to preserve aspect ratio
        )

        # Optional caption
        if caption:
            cap_box = slide.shapes.add_textbox(
                Inches(0.8), Inches(6.8), Inches(8.4), Inches(0.4)
            )
            cap_tf = cap_box.text_frame
            cap_p = cap_tf.paragraphs[0]
            cap_p.text = caption
            cap_p.font.size = Pt(10)
            cap_p.font.italic = True
            cap_p.font.color.rgb = RGBColor.from_string(palette["muted"])
            cap_p.alignment = PP_ALIGN.CENTER

    except Exception as e:
        import inspect
        import logging
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e
```

For the `diagram_full` type (hero/full-bleed image), the image should span nearly the entire slide:

```python
def add_diagram_full_slide(
    prs: Presentation,
    title: str,
    image_path: str,
    palette: dict = None
) -> None:
    """Add a full-bleed diagram slide with title overlay.

    The image spans the full slide width. The title appears as a
    semi-transparent overlay bar at the top.
    """
    try:
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # Full-bleed image
        slide.shapes.add_picture(
            image_path,
            left=Inches(0),
            top=Inches(0.8),
            width=Inches(10),
            # height auto-scaled
        )

        # Title overlay bar
        txBox = slide.shapes.add_textbox(
            Inches(0), Inches(0), Inches(10), Inches(0.7)
        )
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(palette["fg"])

    except Exception as e:
        import inspect
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e
```

---

## Colour Palettes

Implement at least these palettes (Pete prefers dark themes):

```python
PALETTES: dict[str, dict[str, str]] = {
    "midnight": {
        "bg": "1E1E2E",
        "fg": "CDD6F4",
        "accent": "89B4FA",
        "accent2": "A6E3A1",
        "muted": "6C7086",
        "highlight": "F9E2AF",
        "error": "F38BA8",
    },
    "charcoal": {
        "bg": "36454F",
        "fg": "F2F2F2",
        "accent": "4FC3F7",
        "accent2": "81C784",
        "muted": "90A4AE",
        "highlight": "FFD54F",
        "error": "EF5350",
    },
    "ocean": {
        "bg": "0D1B2A",
        "fg": "E0E1DD",
        "accent": "1B9AAA",
        "accent2": "06D6A0",
        "muted": "415A77",
        "highlight": "FFD166",
        "error": "EF476F",
    },
}
```

The `midnight` palette matches Pete's existing dashboard dark theme from `assets/style.css`.

---

## Markdown Parser: `parse_report.py`

### Purpose

Parse a markdown file into the structured JSON manifest that `build_deck.py` consumes. This bridges the gap between authoring in markdown and producing slides.

### Behaviour

```bash
python scripts/parse_report.py \
    --input report.md \
    --images ./diagrams/ \
    --output slides.json
```

### Parsing Rules

1. `# H1` headings become `title` slides (first H1 only) or `section_header` slides
2. `## H2` headings become `section_header` slides
3. `### H3` headings become the title of a `content` slide
4. Paragraph text under a heading becomes the `body` of that content slide
5. Bullet lists (`- ` or `* `) become the `bullets` array of the current content slide
6. Image references (`![caption](path.png)`) become `diagram` slides:
   - If the image is the only content under a heading → `diagram_full`
   - If the image accompanies text → `diagram` with caption from the alt text
7. Lines matching `**Key Metric:** value` or similar bold-colon patterns get collected into `metrics` slides
8. The parser should scan the `--images` directory and match filenames referenced in the markdown

### Return Type

The parser must return `list[dict]` — a list of slide definition dicts matching the manifest schema above.

---

## Validation Script: `validate_deck.py`

### Purpose

Convert the generated `.pptx` to per-slide images and report any issues.

### Interface

```bash
python scripts/validate_deck.py \
    --input ./outputs/report-deck/final.pptx \
    --output-dir ./outputs/report-deck/qa/
```

### Behaviour

1. Convert `.pptx` → PDF via LibreOffice headless (`soffice --headless --convert-to pdf`)
2. Convert PDF → per-slide JPGs via `pdftoppm -jpeg -r 150`
3. Output a summary: slide count, any slides with no content, image dimensions
4. If LibreOffice is not available, log a warning and skip (don't fail)

This enables the visual QA loop described in the SKILL.md workflow.

---

## Coding Conventions (MUST follow)

Pete has specific coding standards that must be applied throughout:

### Python Style
- 4 spaces for indentation, PEP8 compliant
- Lines under 120 characters
- Meaningful variable names, preferably Hungarian notation
- Type hints on all function definitions
- Docstrings on all functions and classes

### Exception Handling

Every function must use this pattern:

```python
import inspect
import logging

# At module level:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=common.log_file,
    filemode='a'
)
logger = common.getLogger(__name__)

# In every function:
try:
    # ... function logic ...
except Exception as e:
    current_function = inspect.currentframe().f_code.co_name
    print(f"An error occurred in {current_function}: {e}")
    logger.warning(f"An error occurred in {current_function}: {e}")
    raise e
```

### File Organisation
- Scripts go in the `scripts/` directory
- Reference docs go in `references/`
- Output files go in `files/` or `outputs/` directory
- All CLI scripts should use `argparse` for argument parsing

### SQL Conventions (if any DuckDB/Postgres queries are needed)
- Table names UPPERCASE with underscores, no plurals
- Column names lowercase with underscores (camelCase acceptable)
- Major SQL keywords on new lines
- Column selections on separate lines with leading commas

---

## Dependencies

The skill should use only these Python packages:

```
python-pptx>=1.0.0    # Core PPTX creation
Pillow>=10.0.0         # Image handling and resizing
mistune>=3.0.0         # Markdown parsing (lightweight, no heavy deps)
```

System tools (for validation only, not required for generation):
- LibreOffice (`soffice`) — PDF conversion
- Poppler (`pdftoppm`) — PDF to images

---

## Design Principles (from Anthropic's own PPTX skill)

These are proven best practices from the official Anthropic PPTX skill. The skill MUST enforce them:

1. **No boring slides** — every slide needs a visual element (image, shape, icon, or chart)
2. **Bold, content-informed palettes** — colours should feel designed for THIS topic
3. **Dominance over equality** — one colour dominates (60-70%), 1-2 supporting, one accent
4. **Dark/light contrast** — dark backgrounds for title + conclusion, or dark throughout
5. **Commit to a visual motif** — one distinctive element repeated across slides
6. **Vary layouts** — don't repeat the same layout on consecutive slides
7. **Left-align body text** — centre only titles
8. **Size contrast** — titles 36pt+, body 14-16pt
9. **NEVER use accent lines under titles** — hallmark of AI-generated slides
10. **Breathing room** — 0.5" minimum margins, 0.3-0.5" between content blocks

### Typography

| Element | Size | Weight |
|---------|------|--------|
| Slide title | 36-44pt | Bold |
| Section header | 20-24pt | Bold |
| Body text | 14-16pt | Regular |
| Captions | 10-12pt | Italic, muted colour |

### Font Pairing (default)

- **Heading**: Georgia (serif, professional)
- **Body**: Calibri (clean, readable)

---

## Example Usage

### From Markdown

Given `report.md`:

```markdown
# Database Cost Analysis Q4

## Storage Spend Overview

### Key Findings

Total database spend increased 12% quarter-on-quarter, driven primarily
by the expansion of PostgreSQL clusters supporting App Alpha and App Beta.

- PostgreSQL clusters account for 45% of total spend
- Cost-per-GB ranges from £2.10 to £18.40 across applications
- Three applications exceed the £10/GB efficiency threshold

![System Architecture](./diagrams/architecture.png)

## Efficiency Analysis

![Cost Breakdown](./diagrams/cost_breakdown.png)

### Recommendations

- Migrate App Gamma to shared PostgreSQL cluster
- Implement storage tiering for cold data
- Review Q1 targets with platform team
```

And a `./diagrams/` folder containing `architecture.png` and `cost_breakdown.png`.

The expected output is a 6-7 slide presentation:
1. Title slide: "Database Cost Analysis Q4"
2. Section header: "Storage Spend Overview"
3. Content slide: "Key Findings" with bullets
4. Diagram slide: "System Architecture" with `architecture.png` prominently placed
5. Section header: "Efficiency Analysis"
6. Full-bleed diagram: "Cost Breakdown" with `cost_breakdown.png`
7. Content/closing slide: "Recommendations" with bullets

### From JSON Manifest

```bash
python scripts/build_deck.py --manifest slides.json --output final.pptx
```

Where `slides.json` follows the schema defined above.

---

## Testing

Use behave step definitions in `features/steps/`:

### Feature File

```gherkin
Feature: Report Presenter builds PPTX from markdown and images

  Scenario: Generate a basic report deck
    Given a markdown file "test_report.md" with 3 sections
    And a diagrams directory with 2 PNG files
    When I run the parse_report script
    Then the manifest JSON contains 7 slides
    And 2 slides have type "diagram" or "diagram_full"

  Scenario: Images are embedded in the PPTX
    Given a manifest with a diagram slide referencing "arch.png"
    When I run the build_deck script
    Then the output PPTX contains an embedded image
    And the image dimensions are within the slide bounds

  Scenario: Dark palette is applied correctly
    Given a manifest with palette "midnight"
    When I run the build_deck script
    Then slide backgrounds use colour "1E1E2E"
    And title text uses colour "CDD6F4"

  Scenario: Missing image fails gracefully
    Given a manifest referencing a non-existent image "missing.png"
    When I run the build_deck script
    Then the script logs a warning
    And the slide is created with a placeholder message
```

### Test Data

- Create mock markdown files in `files/temp/mock/data/`
- Create small test PNG images (solid colour rectangles are fine)
- Use `context` to share data between steps
- Clean up in `after_scenario` hook

---

## Stretch Goals (not required for v1)

- **Speaker notes**: Add notes from markdown content that didn't fit on the slide
- **Chart generation**: Use matplotlib or plotly to render data charts as PNGs, then embed
- **Template inheritance**: Load a corporate `.pptx` template and use its master slides
- **PDF export**: Convert final `.pptx` to PDF via LibreOffice as a secondary output
- **Batch mode**: Process multiple reports in a single run

---

## Key Research References

These repos were evaluated during design and informed the approach:

| Repository | What We Learned |
|------------|-----------------|
| `anthropics/skills` (official PPTX skill) | Design principles, QA validation loop, slide type patterns |
| `tfriedel/claude-office-skills` | OOXML editing workflow, thumbnail validation, template-based creation |
| `coleam00/excalidraw-diagram-skill` | Playwright render-view-fix loop pattern for visual validation |
| `SpillwaveSolutions/design-doc-mermaid` | Python CLI tooling patterns, mmdc validation integration |
| `Skillsmp pptx-generator` | 6-phase pipeline (Gather→Design→Generate→Convert→QA→Output), subagent QA |

---

## Summary

Build a Claude Code skill called `report-presenter` that:
1. Parses markdown reports into a structured slide manifest
2. Uses `python-pptx` to build visually impressive presentations with embedded images
3. Applies dark-themed colour palettes with professional typography
4. Supports multiple slide types (title, content, diagram, metrics, two-column, closing)
5. Includes a validation script for visual QA
6. Follows Pete's coding conventions (type hints, docstrings, inspect-based exception handling)
7. Works as a CLI tool AND as a Claude Code skill via SKILL.md
