# Marp Image Cookbook

Canonical recipes for Marp image directives. Pick one per slide situation. Marp syntax reference: https://marpit.marp.app/image-syntax

Every directive below is a real Marpit keyword — they compose (e.g. `bg right:40% brightness:.4`). When in doubt, prefer `contain` over `cover` for diagrams, and `cover` over raw embeds for hero photography.

---

## 1. Full-bleed background

```markdown
![bg](assets/hero.jpg)
```

**When to use:** Section-opener slide, title slide, or any "feel before read" moment. Image fills the entire slide; put title text on top via normal markdown (readable only if the image is dark or you add a brightness filter — see recipe 5).

---

## 2. Background with cover fit

```markdown
![bg cover](assets/city-skyline.jpg)
```

**When to use:** Hero photography where the subject is centred and cropping the edges is safe. `cover` scales to fill without distortion; `contain` (its sibling) letterboxes to show the whole image. Default is `cover` when dimensions match slide aspect, but being explicit prevents surprise cropping.

---

## 3. Right-side split background

```markdown
![bg right:40%](assets/chart.png)

# Revenue grew 3x
- Q1 baseline
- Q4 result
```

**When to use:** The classic "visual + bullets" layout. Image occupies the right 40% of the slide; text flows into the remaining 60%. Use `bg left:40%` for the mirror.

---

## 4. Multi-background split (vertical stack on left)

```markdown
![bg left:50% vertical](assets/before.png)
![bg left:50% vertical](assets/after.png)

# Before vs after
One pane each, no label noise.
```

**When to use:** Comparison shots where two images each earn half of a split panel. The `vertical` keyword stacks multiple backgrounds in the named region instead of overlaying them. Add a third `![bg left:50% vertical](...)` to stack three.

---

## 5. Brightness filter on background

```markdown
![bg brightness:.4](assets/crowd.jpg)

# Community first
White text sits legibly over the darkened image.
```

**When to use:** You want hero imagery *and* readable text on top. `brightness:.4` drops the image to 40% brightness; combine with white text. Other filters: `blur:5px`, `sepia:1`, `hue-rotate:90deg`. See the Marpit docs link above for the full list.

---

## 6. Fixed-width inline image

```markdown
![w:600](assets/logo.png)
```

**When to use:** Inline embed where you know the exact width you want (pixels). Good for logos, screenshots, and anything where the slide flow is: heading → image → caption. Use `![h:400](...)` for height-constrained. Combine as `![w:600 h:400](...)`.

---

## 7. `contain` for SVG diagrams

```markdown
![w:900 contain](assets/architecture.svg)
```

**When to use:** Pre-rendered Mermaid or Excalidraw SVGs. `contain` preserves the whole diagram (no cropping) while `w:900` caps the width so it never overflows the slide margins. This is the directive the F007/F008 mermaid pre-render engines emit by default — matching it here means hand-authored fences and engine-rewritten fences look identical.

### Content-fit: charts vs diagrams

- **Diagrams** (mermaid, excalidraw): use `![w:900 contain]` -- diagrams are the primary content and need full width
- **Charts** (matplotlib bar/line/pie/scatter): use `![w:700 contain]` -- charts share the slide with bullets; the smaller directive leaves room for 3 lines of text below
- **General rule:** if a slide has BOTH an image AND bullets, the image directive width should be <=700px. If the image is the only content (no bullets), use up to w:900.

---

## 8. Drop-shadow filter

```markdown
![w:700 drop-shadow](assets/screenshot.png)
```

**When to use:** UI screenshots or product shots that need to "lift" off the slide background. `drop-shadow` adds a subtle shadow; pairs well with a neutral background theme.

---

## 9. Grayscale + opacity (muted reference image)

```markdown
![bg grayscale:1 opacity:.5](assets/old-design.png)

# Old → new
The faded background is context; the foreground is the story.
```

**When to use:** Before/after or context-setting slides where you want an image present but visually subordinate to the text. Stack with a foreground image (recipe 2) for a full "reference vs current" layout.

---

## Further reading

- Marpit image syntax: https://marpit.marp.app/image-syntax
- CSS filters (everything after `brightness:`, `blur:`, etc.): https://developer.mozilla.org/en-US/docs/Web/CSS/filter
