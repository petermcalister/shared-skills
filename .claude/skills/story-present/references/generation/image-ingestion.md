# Image-First Ingestion

When the user says "use the images in `<dir>`" or when a pre-populated image directory is named in Q5 or Q6, the skill must **scan the directory first** and let what it finds shape the outline — rather than generating an outline and then retrofitting images into it. A slide deck shaped by the imagery available lands more naturally than a deck whose pictures were an afterthought.

---

## Directory-scan CLI pattern

Run this Bash snippet from the skill (requires Pillow, already in `pyproject.toml` via matplotlib's dep chain). The forward slashes in paths are cross-platform safe:

```bash
poetry run python - <<'PY'
from pathlib import Path
from PIL import Image

scan_dir = Path("<user-supplied-dir>")
found = []
for p in sorted(scan_dir.iterdir()):
    if not p.is_file():
        continue
    ext = p.suffix.lower().lstrip(".")
    kind = {
        "png": "photo",
        "jpg": "photo",
        "jpeg": "photo",
        "webp": "photo",
        "svg": "diagram",
        "pdf": "diagram",
    }.get(ext, "other")
    try:
        with Image.open(p) as img:
            w, h = img.size
    except Exception:
        w, h = (None, None)
    found.append({"name": p.name, "kind": kind, "w": w, "h": h})

for f in found:
    print(f)
PY
```

Capture the output into the working-notes block as a table with columns: `filename | kind | dimensions`.

---

## Outline adaptation rules

Once the scan returns, pick an outline shape by **image count N**:

| N found | Outline treatment |
|---|---|
| 0 | Fall back to the normal source ingestion flow in `references/generation/source-ingestion.md`. Image-first ingestion is opt-out here — no images means no adaptation. |
| 1–2 | One "hero image" slide at the opener or closer; the rest of the deck is text + charts. Don't stretch the imagery. |
| 3–5 | One image per major section. The framework's natural sections (e.g. Conference: hook / journey / takeaways) each get one. Remaining slides are text. |
| 6–10 | "Tight visual deck" — aim for an image on ~50% of slides. Group by `kind`: diagrams on structural slides, photos on emotional/contextual slides. |
| 11+ | Image-per-slide is viable. Propose a layout rotation (full-bleed → split → fixed-width inline) so consecutive slides don't look identical. Cite `references/generation/marp-image-cookbook.md` recipes 1, 3, and 6. |

Always surface the scan results in the Understanding Check so the user can veto specific files before generation:

```
## Images found in <dir>
- hero.jpg (photo, 1920x1080) → proposed: opener full-bleed
- architecture.svg (diagram, 1600x900) → proposed: Slide 4 split right
- team-photo.jpg (photo, 2400x1600) → proposed: closer full-bleed
Include all? (yes / drop <name> / skip ingestion)
```

---

## Empty-directory fallback

If the scan dir exists but contains no matching files, or if the user's hint points to a non-existent path:

1. Log the scan attempt and the empty result in the working notes.
2. Do **not** block — continue with whatever other Q6 sources were selected.
3. If Q6 was **only** the image dir (no other sources), fall back to Q6 = (h) None and proceed with interview-only generation.
4. Note in the Understanding Check that image ingestion was skipped so the user can correct the path if it was a typo.

---

## When image-first overrides source-first

Normally `source-ingestion.md` runs *after* L1 and *before* L2. Image-first ingestion is a **sub-step of source ingestion**, not a replacement — it runs at the same point in the flow, but before any CLI source pulls, because the image inventory determines whether the outline should be "visual-led" (N≥6) or "text-led with illustrations" (N≤5). If the user selected both an image dir *and* other Q6 sources, run the image scan first, let it decide the visual-led flag, then pull the other sources normally.
