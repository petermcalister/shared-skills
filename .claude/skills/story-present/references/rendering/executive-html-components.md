# Executive HTML Component Library

> Vendored from obsidian-executive-html. Update both copies in the same commit.

## Page Structure

Every page must include these foundational layers:

### 1. Google Fonts link
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### 2. Noise texture overlay
A fixed pseudo-element on `body` that adds film-grain depth. Uses `var(--noise-opacity)` so light theme gets a subtler grain:
```css
body::before {
  content: '';
  position: fixed;
  inset: 0;
  opacity: var(--noise-opacity, 0.022);
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
}
```

### 3. Custom scrollbar
```css
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border-glow); border-radius: 3px; }
```

### 4. Reset and base body
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 16px; }
body {
  background: var(--bg-deep);
  color: var(--text-primary);
  font-family: var(--font-body);
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}
```

## Component Library

### Hero Section
Full-viewport, vertically centered, with depth layers:
- **Grid overlay**: subtle blue lines at 60–64px spacing
- **Gradient orbs**: 2–3 large blurred radial-gradient circles positioned behind content, using accent-blue and accent-violet at ~15% opacity, with `filter: blur(100–110px)`
- **Badge**: pill-shaped mono label with a pulsing dot (`animation: pulseGlow 2s ease-in-out infinite`)
- **Headline**: Playfair 900, with a `<span class="gradient-text">` on the key phrase
- **Subtitle**: DM Sans 300, `--text-secondary`, max-width 640–780px
- **CTA buttons**: gradient-blue background, dark text, uppercase mono, 8–10px border-radius, hover lifts 2px with box-shadow
- **Stats row** (optional): large gradient-text numbers with mono uppercase labels beneath

### Cards
The universal container:
```css
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.8rem;
  position: relative;
  overflow: hidden;
}
.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: var(--gradient-hero);
}
```
The 2px gradient top-accent is signature. Apply it to cards, callouts, quote-boxes, and any elevated surface.

### Section Headers
```html
<div class="section-label">Part I</div>
<h2>Section Title Here</h2>
<p>Lead paragraph in --text-secondary.</p>
```
The `.section-label` is a mono uppercase marker with a 28px horizontal line before it:
```css
.section-label {
  display: flex; align-items: center; gap: 0.7rem;
  font-family: var(--font-mono); font-size: 0.72rem;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--accent-blue);
}
.section-label::before {
  content: ''; width: 28px; height: 1px;
  background: var(--accent-blue);
}
```

### Tile Grids
For sets of 3–6 items (principles, problems, capabilities):
- Grid: `repeat(3, 1fr)` at 1rem gap
- Each tile: `bg-card`, `border`, 14px radius, 1.4rem padding
- Tile heading: Playfair 1.1rem
- Tile body: `--text-secondary`, 0.92rem
- Hover: `border-glow` + `translateY(-2px)`

### Metric / KPI Cards
For scorecard-style data:
- Mono uppercase label (0.65rem, `--text-muted`)
- Large value: Playfair 900, 1.8rem, colored per accent
- Description: 0.88rem, `--text-secondary`
- Grid: `repeat(auto-fit, minmax(150px, 1fr))` or fixed 4–5 columns

### Data Tables
```css
table {
  width: 100%; border-collapse: separate; border-spacing: 0;
  border: 1px solid var(--border); border-radius: 16px; overflow: hidden;
}
th {
  background: var(--surface); color: var(--text-muted);
  font-family: var(--font-mono); font-size: 0.72rem;
  letter-spacing: 0.12em; text-transform: uppercase;
  padding: 1rem 1.1rem;
}
td {
  background: var(--bg-card); color: var(--text-secondary);
  border-top: 1px solid var(--border); padding: 1rem 1.1rem;
}
td:first-child { color: var(--text-primary); font-weight: 500; }
```

### Callouts
Elevated cards with a gradient background wash for executive statements:
```css
.callout {
  background: linear-gradient(180deg, rgba(91,138,245,0.06), rgba(18,19,26,1));
  border: 1px solid var(--border); border-radius: 16px;
  padding: 1.8rem; position: relative; overflow: hidden;
}
.callout::before { /* 2px gradient bar */ }
```
Include a `.small-label` (mono, cyan, uppercase) above the callout text.

### Quote Boxes
For executive quotes or thesis statements:
- Same card shell as above
- `blockquote`: Playfair italic, `clamp(1.25rem, 2.2vw, 1.65rem)`
- `cite`: block, `--text-muted`, normal font-style

### Tags / Badges
Pill-shaped labels for categorization:
```css
.tag {
  display: inline-flex; align-items: center; gap: 0.5rem;
  font-family: var(--font-mono); font-size: 0.68rem;
  letter-spacing: 0.12em; text-transform: uppercase;
  padding: 0.35em 0.9em; border-radius: 999px;
  border: 1px solid;
}
```
Color variants: `rgba(accent, 0.06)` background, accent foreground, `rgba(accent, 0.25)` border.

### Navigation
Two patterns exist — choose based on page length:
- **Sticky top strip**: `backdrop-filter: blur(16px)`, mono uppercase links, for pages with 5+ sections
- **Fixed side dots**: small circles on the right edge, for long-scroll narratives

### Code Cards
For code snippets and technical content:
- Card container with `overflow: hidden`
- Language label as `.tag` in top-right corner
- `<pre><code>` with `font-family: var(--font-mono)`, `font-size: 0.88rem`
- Background: `var(--bg-elevated)` in light, `var(--bg-card)` in dark
- Syntax highlighting via inline spans with accent colors

### Accordions / Expandable Cards
For detail-heavy content (epic lists, deliverables):
- Card with clickable header row (flex, space-between)
- Chevron icon in a small circle that rotates 180deg on open
- Body: `max-height: 0` → `max-height: 3000px` transition
- JS: simple `classList.toggle('open')`

### Timelines
For roadmaps and phased plans:
- 2-column grid, each item in a card
- Color-coded time label (mono, accent-colored)
- Playfair heading, DM Sans description

### Diagrams (Layered)
For architecture or flow diagrams:
- Container card with flex-column layout
- Each layer: rounded div with color-coded background (`rgba(accent, 0.08)`), border (`rgba(accent, 0.24)`), accent text
- Arrow dividers: centered `▼` character in `--text-muted`

## Animations

Keep these available for scroll-reveal and micro-interactions:
```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
```

**Scroll-reveal** with IntersectionObserver:
```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```
Stagger with `.reveal-delay-1` through `.reveal-delay-4` (transition-delay 0.1s increments).

## Responsive Breakpoints

| Breakpoint | Behavior |
|---|---|
| > 1024px | Full grid layouts (3-col tiles, 4-col pillars, 2-col grids) |
| 720–1024px | 2-col tiles, 2-col pillars, single-col narrative grids |
| < 720px | Single column everything, hide side-dot nav, stack CTAs |

Container padding drops from `0 2rem` to `0 1.2rem` on small screens.

## Separators

Use gradient horizontal rules between content sections:
```css
hr.sep {
  border: none; height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-glow), transparent);
  margin: 2.5rem 0;
}
```

## Theme Toggle

Every page should include a theme toggle button. Place it fixed in the top-right corner:

```html
<button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">
  <span class="toggle-icon">☀️</span>
</button>
```

```css
.theme-toggle {
  position: fixed;
  top: 1.2rem;
  right: 1.2rem;
  z-index: 200;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: border-color 0.3s, background 0.3s, transform 0.3s;
  backdrop-filter: blur(8px);
}
.theme-toggle:hover {
  border-color: var(--border-glow);
  transform: scale(1.1);
}
```

If the page has a sticky nav strip, position the toggle inside the nav or bump it to `top: 4rem` so they don't overlap.

### Toggle Script

```js
const toggle = document.getElementById('themeToggle');
const icon = toggle.querySelector('.toggle-icon');

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  localStorage.setItem('theme', theme);
}

// Init: respect saved preference, then system preference, default dark
const saved = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
setTheme(saved || (prefersDark ? 'dark' : 'dark'));

toggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  setTheme(current === 'dark' ? 'light' : 'dark');
});
```

This persists the user's choice in `localStorage` and defaults to dark. The `data-theme` attribute on `<html>` drives all CSS variable overrides.

### Light Theme Adjustments

Some components need special handling in light mode:

- **Hero gradient orbs**: reduce opacity via `var(--hero-orb-opacity)` — they're too intense on light backgrounds at full strength
- **Gradient text**: still works on light — the blue→violet→rose gradient has enough saturation to read on white
- **Callout wash**: change to `rgba(91,138,245,0.04)` in light to avoid a grey cast
- **Nav backdrop**: use `var(--nav-bg)` so the blur tints correctly per theme
- **Code blocks**: in light mode, use `--bg-elevated` for code backgrounds rather than `--bg-card` for subtle differentiation
- **Hover shadows**: use `var(--shadow-hover)` — dark uses `rgba(0,0,0,0.3)`, light uses `rgba(0,0,0,0.08)`

## Anti-Patterns

- **Never hardcode background colors.** Always use `var(--bg-*)` tokens so themes switch cleanly.
- **Never use sans-serif for headlines.** Always Playfair Display.
- **Never use color without 6–8% opacity backgrounds.** Colored elements always pair foreground color with a faint tinted background.
- **Never add box-shadows to cards at rest.** Only on hover, and even then, subtle: `0 20px 50px var(--shadow-hover)`.
- **Never use more than one gradient-text span per heading.**
- **No external CSS frameworks.** Everything is self-contained inline CSS.
- **No build tools, no imports, no modules.** A single `.html` file that opens in any browser.
- **Never use raw color values for text or surfaces in component CSS.** Always reference CSS variables — this is what makes the theme toggle work.
