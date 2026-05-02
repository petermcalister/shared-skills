# Executive HTML Design Tokens

> Vendored from obsidian-executive-html. Update both copies in the same commit.

## CSS Custom Properties

Always define these CSS custom properties in `:root` (dark theme is the default):

```css
:root, [data-theme="dark"] {
  /* Backgrounds — layered from deepest to most elevated */
  --bg-deep: #0a0b0f;
  --bg-card: #12131a;
  --bg-card-hover: #191b24;
  --bg-elevated: #1a1c27;
  --surface: #222436;

  /* Borders */
  --border: #2a2d3e;
  --border-glow: #3d4167;

  /* Text hierarchy */
  --text-primary: #e4e6f0;
  --text-secondary: #a5aac4;
  --text-muted: #6d7394;

  /* Accent palette — use sparingly, one per element */
  --accent-blue: #5b8af5;
  --accent-cyan: #4cd4c0;
  --accent-amber: #f0a85e;
  --accent-rose: #e86b8a;
  --accent-violet: #9b7cf5;
  --accent-lime: #9ed65c;

  /* Gradients */
  --gradient-hero: linear-gradient(135deg, #5b8af5 0%, #9b7cf5 45%, #e86b8a 100%);
  --gradient-blue: linear-gradient(135deg, #5b8af5, #4cd4c0);
  --gradient-warm: linear-gradient(135deg, #f0a85e, #e86b8a);
  --gradient-cool: linear-gradient(135deg, #9b7cf5, #5b8af5);

  /* Typography stacks */
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'DM Sans', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Theme toggle icon */
  --noise-opacity: 0.022;
  --hero-orb-opacity: 0.9;
  --nav-bg: rgba(10, 11, 15, 0.88);
  --cta-text: #091016;
  --shadow-hover: rgba(0, 0, 0, 0.3);
}
```

## Light Theme Overrides

The light theme preserves the same accent palette and gradients but inverts the surface and text layers. Apply it via `[data-theme="light"]` on `<html>`:

```css
[data-theme="light"] {
  --bg-deep: #f4f5f8;
  --bg-card: #ffffff;
  --bg-card-hover: #f0f1f5;
  --bg-elevated: #e8e9f0;
  --surface: #e2e4ec;

  --border: #d0d3de;
  --border-glow: #b8bcd0;

  --text-primary: #1a1c27;
  --text-secondary: #4a4e6a;
  --text-muted: #7c809a;

  /* Accents stay the same — they read well on light surfaces */
  --accent-blue: #4a78e0;
  --accent-cyan: #2fb8a4;
  --accent-amber: #d99040;
  --accent-rose: #d4567a;
  --accent-violet: #8568e0;
  --accent-lime: #72a840;

  --noise-opacity: 0.012;
  --hero-orb-opacity: 0.5;
  --nav-bg: rgba(244, 245, 248, 0.92);
  --cta-text: #ffffff;
  --shadow-hover: rgba(0, 0, 0, 0.08);
}
```

Light accents are slightly darkened (~10%) from their dark-theme counterparts so they meet WCAG AA contrast on white cards.

## Typography Scale

| Role | Font | Weight | Size | Tracking | Transform |
|---|---|---|---|---|---|
| Hero h1 | Playfair Display | 900 | `clamp(2.8rem, 6vw, 5rem)` | -0.02em | — |
| Section h2 | Playfair Display | 700–900 | `clamp(2rem, 4vw, 3rem)` | -0.02em | — |
| Sub-heading h3 | Playfair Display | 700 | `clamp(1.35rem, 2.5vw, 1.8rem)` | — | — |
| Body text | DM Sans | 300–400 | 1rem–1.15rem | — | — |
| Labels / badges | JetBrains Mono | 500 | 0.65–0.72rem | 0.12–0.18em | uppercase |
| Metric values | Playfair Display | 900 | 1.8–2.4rem | — | — |

**Gradient text** for hero headlines: apply `background: var(--gradient-hero); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;` to a `<span>` wrapping the key phrase — never the entire heading.
