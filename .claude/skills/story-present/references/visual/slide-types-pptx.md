# Slide Types

All slides use `slide_layouts[6]` (blank layout) and are built programmatically.
Slide dimensions: 10" x 7.5" (standard). Minimum margins: 0.5". Content gap: 0.3-0.5".

## Typography

| Element        | Font    | Size     | Weight  | Notes                  |
|----------------|---------|----------|---------|------------------------|
| Slide title    | Georgia | 36-44pt  | Bold    | palette fg colour      |
| Section header | Georgia | 20-24pt  | Bold    | palette fg colour      |
| Body text      | Calibri | 14-16pt  | Regular | palette fg colour      |
| Captions       | Calibri | 10-12pt  | Italic  | palette muted colour   |

---

## title

**Description:** Opening slide with large title, subtitle, and date.

**Required fields:** `title`
**Optional fields:** `subtitle`, `date`, `image_path` (background image)

**Layout positions:**
- Title: left=0.8", top=2.0", width=8.4", height=1.5" — 44pt Bold Georgia
- Subtitle: left=0.8", top=3.6", width=8.4", height=0.8" — 20pt Regular Calibri
- Date: left=0.8", top=6.5", width=8.4", height=0.5" — 12pt Italic Calibri, muted colour
- Background image (optional): left=0", top=0", width=10" (full bleed)

---

## section_header

**Description:** Section divider with bold heading and optional subtitle line.

**Required fields:** `title`
**Optional fields:** `subtitle`

**Layout positions:**
- Title: left=0.8", top=2.8", width=8.4", height=1.2" — 36pt Bold Georgia, centre-aligned
- Subtitle: left=1.5", top=4.2", width=7.0", height=0.6" — 16pt Regular Calibri, centre-aligned, muted colour

---

## content

**Description:** Title + prose paragraph + optional bullet points.

**Required fields:** `title`, `body`
**Optional fields:** `bullets` (list of strings)

**Layout positions:**
- Title: left=0.8", top=0.4", width=8.4", height=0.8" — 36pt Bold Georgia
- Body: left=0.8", top=1.5", width=8.4", height=2.5" — 16pt Regular Calibri, word-wrap enabled
- Bullets: left=1.0", top=4.2", width=8.0", height=2.8" — 14pt Regular Calibri, 0.3" indent per bullet

---

## diagram

**Description:** Title + prominently placed image + optional caption.

**Required fields:** `title`, `image_path`
**Optional fields:** `caption`

**Layout positions:**
- Title: left=0.8", top=0.4", width=8.4", height=0.8" — 28pt Bold Georgia
- Image: left=0.75", top=1.5", width=8.5" (height auto-scaled)
- Caption: left=0.8", top=6.8", width=8.4", height=0.4" — 10pt Italic Calibri, muted colour, centre-aligned

---

## diagram_full

**Description:** Full-bleed image with minimal title overlay.

**Required fields:** `image_path`
**Optional fields:** `title`

**Layout positions:**
- Image: left=0", top=0", width=10" (height auto-scaled, full bleed)
- Title overlay: left=0.5", top=0.3", width=5.0", height=0.6" — 20pt Bold Georgia, fg colour with semi-transparent background band

---

## metrics

**Description:** Large stat callouts with big numbers (60-72pt) and labels.

**Required fields:** `title`, `metrics` (list of `{value, label}` dicts)
**Optional fields:** none

**Layout positions:**
- Title: left=0.8", top=0.4", width=8.4", height=0.8" — 36pt Bold Georgia
- Metrics grid: evenly distributed across width 0.8"-9.2", top=2.0"
  - Each metric: width = (8.4 / n_metrics)", height=3.0"
  - Value: 60pt Bold Georgia, accent colour, centre-aligned
  - Label: 14pt Regular Calibri, muted colour, centre-aligned, 0.3" below value

---

## two_column

**Description:** Side-by-side content blocks, optional image in one column.

**Required fields:** `title`, `left_body`, `right_body`
**Optional fields:** `left_image`, `right_image`

**Layout positions:**
- Title: left=0.8", top=0.4", width=8.4", height=0.8" — 36pt Bold Georgia
- Left column: left=0.5", top=1.5", width=4.2", height=5.0"
  - Image (if present): top of column, width=4.2" (height auto-scaled)
  - Text: below image or top of column, 14pt Regular Calibri
- Right column: left=5.3", top=1.5", width=4.2", height=5.0"
  - Image (if present): top of column, width=4.2" (height auto-scaled)
  - Text: below image or top of column, 14pt Regular Calibri

---

## comparison

**Description:** Before/after or pros/cons layout with header labels.

**Required fields:** `title`, `left_label`, `left_items`, `right_label`, `right_items`
**Optional fields:** `left_image`, `right_image`

**Layout positions:**
- Title: left=0.8", top=0.4", width=8.4", height=0.8" — 36pt Bold Georgia
- Left header: left=0.5", top=1.5", width=4.2", height=0.5" — 20pt Bold Georgia, accent colour
- Left items: left=0.7", top=2.2", width=4.0", height=4.5" — 14pt Regular Calibri, bulleted
- Left image (optional): left=0.5", top=5.5", width=4.2" (height auto-scaled)
- Right header: left=5.3", top=1.5", width=4.2", height=0.5" — 20pt Bold Georgia, accent2 colour
- Right items: left=5.5", top=2.2", width=4.0", height=4.5" — 14pt Regular Calibri, bulleted
- Right image (optional): left=5.3", top=5.5", width=4.2" (height auto-scaled)

---

## closing

**Description:** Final slide with summary bullets or call to action.

**Required fields:** `title`
**Optional fields:** `bullets`, `call_to_action`

**Layout positions:**
- Title: left=0.8", top=2.0", width=8.4", height=1.2" — 40pt Bold Georgia, centre-aligned
- Bullets: left=1.5", top=3.5", width=7.0", height=2.5" — 16pt Regular Calibri, centre-aligned
- Call to action: left=1.5", top=6.2", width=7.0", height=0.6" — 18pt Bold Calibri, accent colour, centre-aligned
