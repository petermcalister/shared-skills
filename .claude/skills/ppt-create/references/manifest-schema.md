# Manifest Schema

The JSON manifest drives `build_deck.py` to produce a styled PowerPoint deck. It has two parts: a **metadata block** (top-level keys) and a **slides array**.

---

## Metadata Block

| Field          | Type   | Required | Default     | Description                                         |
|----------------|--------|----------|-------------|-----------------------------------------------------|
| `title`        | string | no       | —           | Deck title (informational, not rendered directly)    |
| `subtitle`     | string | no       | —           | Deck subtitle                                       |
| `author`       | string | no       | —           | Author name                                         |
| `date`         | string | no       | —           | Date string                                         |
| `archetype`    | string | no       | —           | Presentation archetype (e.g. "executive-briefing")   |
| `palette`      | string | no       | `"midnight"` | Colour palette key from palettes.md                 |
| `font_heading` | string | no       | `"Georgia"`  | Heading font family                                 |
| `font_body`    | string | no       | `"Calibri"`  | Body font family                                    |
| `slides`       | array  | **yes**  | —           | Array of slide objects (see below)                  |

### Available palettes

`midnight`, `charcoal`, `ocean`, `sage-calm`, `berry-cream`, `cherry-bold`, `forest-moss`, `coral-energy`, `ocean-gradient`, `midnight-exec`, `warm-terracotta`, `teal-trust`

---

## Slides Array

Each slide object must have a `type` field. Additional fields depend on the type.

---

### `title`

Opening slide with large title, subtitle, and date.

| Field        | Type   | Required | Description                |
|--------------|--------|----------|----------------------------|
| `type`       | string | **yes**  | `"title"`                  |
| `title`      | string | **yes**  | Main title text            |
| `subtitle`   | string | no       | Subtitle text              |
| `date`       | string | no       | Date line                  |
| `image_path` | string | no       | Background image file path |

```json
{
  "type": "title",
  "title": "Q4 Strategy Review",
  "subtitle": "Building the Next Growth Engine",
  "date": "March 2026"
}
```

---

### `section_header`

Section divider with bold heading and optional subtitle.

| Field      | Type   | Required | Description       |
|------------|--------|----------|-------------------|
| `type`     | string | **yes**  | `"section_header"` |
| `title`    | string | **yes**  | Section title     |
| `subtitle` | string | no       | Subtitle text     |

```json
{
  "type": "section_header",
  "title": "Market Analysis"
}
```

---

### `content`

Title + prose paragraph + optional bullet points.

| Field     | Type     | Required | Description              |
|-----------|----------|----------|--------------------------|
| `type`    | string   | **yes**  | `"content"`              |
| `title`   | string   | **yes**  | Slide title              |
| `body`    | string   | **yes**  | Paragraph body text      |
| `bullets` | string[] | no       | List of bullet strings   |

```json
{
  "type": "content",
  "title": "Key Findings",
  "body": "Our research identified three critical growth areas that align with the current market trajectory.",
  "bullets": [
    "Cloud adoption accelerating 40% YoY",
    "Enterprise segment showing strongest demand",
    "Partner channel driving 60% of new leads"
  ]
}
```

---

### `diagram`

Title + prominently placed image + optional caption.

| Field        | Type   | Required | Description          |
|--------------|--------|----------|----------------------|
| `type`       | string | **yes**  | `"diagram"`          |
| `title`      | string | **yes**  | Slide title          |
| `image_path` | string | **yes**  | Path to image file   |
| `caption`    | string | no       | Caption below image  |

```json
{
  "type": "diagram",
  "title": "System Architecture",
  "image_path": "images/architecture.png",
  "caption": "Figure 1: High-level system architecture"
}
```

---

### `diagram_full`

Full-bleed image with minimal title overlay.

| Field        | Type   | Required | Description             |
|--------------|--------|----------|-------------------------|
| `type`       | string | **yes**  | `"diagram_full"`        |
| `title`      | string | no       | Overlay title           |
| `image_path` | string | **yes**  | Path to image file      |

```json
{
  "type": "diagram_full",
  "title": "Network Topology",
  "image_path": "images/topology.png"
}
```

---

### `metrics`

Large stat callouts with big numbers and labels.

| Field     | Type     | Required | Description                        |
|-----------|----------|----------|------------------------------------|
| `type`    | string   | **yes**  | `"metrics"`                        |
| `title`   | string   | **yes**  | Slide title                        |
| `metrics` | object[] | **yes**  | Array of metric objects (see below)|

Each metric object:

| Field   | Type   | Required | Description                              |
|---------|--------|----------|------------------------------------------|
| `label` | string | **yes**  | Metric label                             |
| `value` | string | **yes**  | Display value (e.g. "42%", "$1.2M")      |
| `trend` | string | no       | Trend indicator (e.g. "up", "down", "flat") |

```json
{
  "type": "metrics",
  "title": "Q4 Performance",
  "metrics": [
    {"label": "Revenue", "value": "$4.2M", "trend": "up"},
    {"label": "Customers", "value": "1,247", "trend": "up"},
    {"label": "Churn Rate", "value": "2.1%", "trend": "down"}
  ]
}
```

---

### `two_column`

Side-by-side content blocks with optional images.

| Field        | Type   | Required | Description              |
|--------------|--------|----------|--------------------------|
| `type`       | string | **yes**  | `"two_column"`           |
| `title`      | string | **yes**  | Slide title              |
| `left_body`  | string | **yes**  | Left column text         |
| `right_body` | string | **yes**  | Right column text        |
| `left_image` | string | no       | Left column image path   |
| `right_image`| string | no       | Right column image path  |

```json
{
  "type": "two_column",
  "title": "Regional Comparison",
  "left_body": "North America saw 35% growth driven by enterprise adoption and partner expansion across all verticals.",
  "right_body": "EMEA grew 28% with strong traction in financial services and a new partnership with Deutsche Telekom."
}
```

---

### `comparison`

Before/after or pros/cons layout with header labels and bulleted items.

| Field         | Type     | Required | Description                   |
|---------------|----------|----------|-------------------------------|
| `type`        | string   | **yes**  | `"comparison"`                |
| `title`       | string   | **yes**  | Slide title                   |
| `left_label`  | string   | **yes**  | Left column header            |
| `left_items`  | string[] | **yes**  | Left column bullet items      |
| `right_label` | string   | **yes**  | Right column header           |
| `right_items` | string[] | **yes**  | Right column bullet items     |
| `left_image`  | string   | no       | Left column image path        |
| `right_image` | string   | no       | Right column image path       |

```json
{
  "type": "comparison",
  "title": "Before vs After Migration",
  "left_label": "Before",
  "left_items": [
    "Manual deployments taking 4 hours",
    "Frequent rollback incidents",
    "No automated testing"
  ],
  "right_label": "After",
  "right_items": [
    "CI/CD pipeline deploys in 12 minutes",
    "Zero-downtime blue/green deployments",
    "95% test coverage with automated gates"
  ]
}
```

---

### `closing`

Final slide with summary bullets or call to action.

| Field            | Type     | Required | Description                  |
|------------------|----------|----------|------------------------------|
| `type`           | string   | **yes**  | `"closing"`                  |
| `title`          | string   | **yes**  | Closing title                |
| `bullets`        | string[] | no       | Summary bullet points        |
| `call_to_action` | string   | no       | Call-to-action text          |

```json
{
  "type": "closing",
  "title": "Next Steps",
  "bullets": [
    "Finalise vendor selection by April 15",
    "Begin pilot programme in Q2",
    "Full rollout targeted for Q3"
  ],
  "call_to_action": "Let's schedule the kickoff meeting this week."
}
```

---

## Complete Example Manifest

```json
{
  "title": "Q4 Strategy Review",
  "subtitle": "Building the Next Growth Engine",
  "author": "Strategy Team",
  "date": "March 2026",
  "archetype": "executive-briefing",
  "palette": "midnight",
  "font_heading": "Georgia",
  "font_body": "Calibri",
  "slides": [
    {
      "type": "title",
      "title": "Q4 Strategy Review",
      "subtitle": "Building the Next Growth Engine",
      "date": "March 2026"
    },
    {
      "type": "section_header",
      "title": "Market Analysis"
    },
    {
      "type": "content",
      "title": "Key Findings",
      "body": "Our research identified three critical growth areas that align with the current market trajectory.",
      "bullets": [
        "Cloud adoption accelerating 40% YoY",
        "Enterprise segment showing strongest demand",
        "Partner channel driving 60% of new leads"
      ]
    },
    {
      "type": "metrics",
      "title": "Q4 Performance",
      "metrics": [
        {"label": "Revenue", "value": "$4.2M", "trend": "up"},
        {"label": "Customers", "value": "1,247", "trend": "up"},
        {"label": "Churn Rate", "value": "2.1%", "trend": "down"}
      ]
    },
    {
      "type": "diagram",
      "title": "System Architecture",
      "image_path": "images/architecture.png",
      "caption": "Figure 1: High-level system architecture"
    },
    {
      "type": "two_column",
      "title": "Regional Comparison",
      "left_body": "North America saw 35% growth driven by enterprise adoption.",
      "right_body": "EMEA grew 28% with strong traction in financial services."
    },
    {
      "type": "comparison",
      "title": "Before vs After Migration",
      "left_label": "Before",
      "left_items": [
        "Manual deployments taking 4 hours",
        "Frequent rollback incidents"
      ],
      "right_label": "After",
      "right_items": [
        "CI/CD pipeline deploys in 12 minutes",
        "Zero-downtime deployments"
      ]
    },
    {
      "type": "closing",
      "title": "Next Steps",
      "bullets": [
        "Finalise vendor selection by April 15",
        "Begin pilot programme in Q2"
      ],
      "call_to_action": "Let's schedule the kickoff meeting this week."
    }
  ]
}
```

## Notes

- Image paths can be absolute or relative to the manifest file's directory.
- The `palette` key must match one of the registered palettes in `build_deck.py`.
- The `trend` field on metrics is stored in the manifest for semantic use but is not currently rendered visually by `build_deck.py`.
- The `font_heading` and `font_body` metadata fields are informational; `build_deck.py` currently uses hardcoded font names per element.
