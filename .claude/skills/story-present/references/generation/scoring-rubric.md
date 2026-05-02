# Scoring Rubric

Loaded by SKILL.md as the last step before delivery. The agent self-evaluates the generated output against a **layered rubric** — a universal base (65 points) plus an output-class overlay (35 points) — and applies the auto-refine loop below before handing the output to the user.

**Source**: adapted from community ppt-creator self-evaluation rubric (PRD Section 7), extended with prose-craft criteria from tech-writing research.

---

## Architecture — layered scoring

The rubric has three layers. The agent loads **base + one overlay** depending on the chosen framework:

| Output class | When | Overlay loaded | Primary format |
|---|---|---|---|
| **Slides** | output_format is `html`, `interactive`, or `pptx` | Slide overlay (35 pts) | Marp → HTML/PPTX |
| **Prose** | output_format is `docx` | Prose overlay (35 pts) | Markdown → DOCX |
| **Executive HTML** | output_format is `executive-html` | Executive HTML overlay (35 pts) | Structured markdown → obsidian HTML |

**Total is always 100** regardless of output class. Scores are directly comparable across classes.

**Routing rule (format-based, deterministic — no pre-scoring question needed):**

```python
if output_format in ("pptx", "html", "interactive"):
    output_class = "slides"
elif output_format == "docx":
    output_class = "prose"
elif output_format == "executive-html":
    output_class = "executive-html"
```

The user's chosen format determines the scoring class. No framework-based inference needed.

---

## Universal Base Criteria (65 points — all frameworks)

| # | Criterion | Weight | Scoring guide |
|---|-----------|--------|---------------|
| B1 | **Structural compliance** | 20 | Does the output follow the selected template's section/slide sequence exactly? All required sections present in the right order? For executive-html: "template's **section** sequence" — sections can contain multi-paragraph content, subsections, and embedded artifacts. No slide-level atomicity required. |
| B2 | **MECE coverage** | 10 | Are arguments Mutually Exclusive (no overlap) and Collectively Exhaustive (no gaps)? |
| B3 | **Audience alignment** | 10 | Is the language, depth, and tone appropriate for the stated audience from Level 1 Q2? Does the content bridge to the business value surfaced by probe D3? |
| B4 | **Evidence presence** | 5 | Are claims supported by data, examples, or citations? Placeholders marked `[DATA NEEDED]`? Numbers from probe D1 appear where relevant? |
| B5 | **Technical depth** | 5 | When the technical-depth trigger fires (`references/generation/technical-depth-mining.md`): does the output contain architectural decisions, test strategies, or implementation patterns extracted from the source? When the trigger does NOT fire, award 5/5 automatically — this criterion is conditional. See scoring guide below. |
| B6 | **Narrative flow** | 10 | The title-only test: can you read just the slide titles / section headings in sequence and understand the full argument? Does the probe D2 catalyst appear as a tension point in the narrative? For executive-html: "read the **section headings**" — heading hierarchy (h2/h3/h4) must tell a coherent story when read as a table of contents. No action-title format required. |
| B7 | **Constraint compliance** | 5 | Does the output meet the slide count / word count, time limit, and must-include/must-avoid requirements from Level 1 Q5? **Appendix slides** (any slide after `# Appendix`) are excluded from the slide count. |

**Base total**: 20 + 10 + 10 + 5 + 5 + 10 + 5 = **65**.

---

## Slide Overlay Criteria (35 points — Options 1–7, slide output)

Loaded when `output_class == "slides"`. These criteria measure slide-specific craft.

| # | Criterion | Weight | Scoring guide |
|---|-----------|--------|---------------|
| S1 | **Action titles (Options 1–4, 6–7) / Declarative titles (Option 5)** | 15 | Every slide title is a complete sentence stating a finding (consulting) or a clear topic heading (conference)? No topic labels where action titles are required? **Titles must be ≤8 words.** |
| S2 | **One message per slide** | 10 | Does each slide communicate exactly one idea? No slide tries to make two points? |
| S3 | **Marp syntax correctness + content fit** | 5 | Valid Marp frontmatter? Correct `---` separators? **Content-fit check:** split-image slides limit body to ≤5 short lines; diagram slides limit text to ≤3 lines. |
| S4 | **Slide constraint compliance** | 5 | Slide-count ceiling respected? Layout types match template? Appendix excluded from count. |

**Slide overlay total**: 15 + 10 + 5 + 5 = **35**.

**Grand total (base + slide)**: 65 + 35 = **100**.

---

## Prose Overlay Criteria (35 points — Option 8, or Option 5 when docx)

Loaded when `output_class == "prose"`. These criteria measure flowing-document craft, drawing from tech-writing best practices (radical specificity, layered depth, ABT rhythm, minimize caveats).

| # | Criterion | Weight | Scoring guide |
|---|-----------|--------|---------------|
| P1 | **Section headings** | 10 | Descriptive, scannable, parallel structure? Headings enable self-select depth (a reader skimming headings understands the full argument)? No generic labels ("Overview", "Details") where a specific heading would work? **Layered depth test:** each section's first paragraph is a self-contained summary — a reader skimming only first paragraphs understands the full design without reading deeper. First paragraphs that dive straight into implementation detail without a summary sentence score ≤6/10. |
| P2 | **Paragraph discipline** | 10 | One idea per paragraph? Active voice throughout? No hedging language ("it was determined", "could potentially", "in my experience")? ABT rhythm present — at least one complication→resolution beat per section? No 3+ consecutive paragraphs of the same type (all narrative or all technical)? |
| P3 | **Specificity & depth** | 10 | Concrete numbers replace vague quantifiers? Named trade-offs with rejection rationale? Before/after comparisons where applicable? No corporate hedging where the source material has specifics? Every reflective paragraph lands on a concrete insight, not just a narrative beat? |
| P4 | **Prose syntax correctness** | 5 | Valid markdown heading hierarchy (no skipped levels)? No orphaned cross-references? Images and diagrams render correctly? Section breaks are logical (not artificial slide-like fragmentation)? |

**Prose overlay total**: 10 + 10 + 10 + 5 = **35**.

**Grand total (base + prose)**: 65 + 35 = **100**.

---

## Hard Gate — Visual Variety (slides) / Document Quality (prose)

The hard gate is a **mechanical, binary PASS/FAIL** check that runs in addition to the 100-point rubric. It is **NOT** part of the point total. The agent loads the matching gate based on `output_class`.

### Slide output: Criterion 10 — Visual variety (Options 1–7)

Loaded when `output_class == "slides"`.

**Floor rules (ALL must pass):**

| Rule | Check |
|------|-------|
| Image density | `images >= ceil(slides / 3)` |
| Diagram presence | `mermaid_fences + chart_fences >= 1` |
| Directive variety | `distinct_directives >= 2` |

**Implementation.** Mechanics live in `tools/story_present/visual_gate.py` — function `check_visual_variety(markdown_path, slide_count=None)` returns `{passed, reason, counts}`. The regex approach:

- Images: `\!\[[^\]]*\]\([^)]+\)` (all matches).
- Mermaid fences: `^```mermaid\b` with `re.MULTILINE` (start-of-line).
- Chart fences: `^```chart\b` with `re.MULTILINE`.
- Distinct directives: extract `\!\[([^\]]*)\]` bracket content, normalise whitespace + lowercase, count unique strings. `![bg](x)` and `![bg cover](y)` = 2 distinct.
- Slide count: count `^---$` separator lines, excluding the opening frontmatter block.

**Auto-refine behaviour.** Implemented in **F012** (Batch 4). On a criterion-10 fail, the refine loop parses the `reason` string to identify the failing floor and injects the matching fix:

- `"no diagrams"` → inject a **real mermaid fence skeleton** (not a text placeholder) that the LLM fills on the refine pass:

  ````markdown
  ```mermaid
  flowchart LR
    A["<infer from slide topic>"] --> B["<infer>"]
    B --> C["<infer>"]
  ```
  ````

  The skeleton gives the LLM concrete structure to improve instead of starting from scratch. Place it on the slide whose topic most naturally maps to a process or relationship diagram.

- `"images below floor"` → inject **placeholder directives** (the `placeholder://visual-needed` format from `references/visual/visual-design-principles.md` "Rich visual placeholder protocol") on under-imaged slides. Use the Marp directive + appendix back-reference format:

  ```markdown
  ![bg right:40%](placeholder://visual-needed)

  *[See Appendix: P<n> — <brief subject>]*
  ```

  Add a corresponding row to the `# Appendix — Visual Placeholders` table (create the appendix section if it does not yet exist).

- `"distinct"` → vary the directives on existing images. Replace a bare `![](...)` or duplicate directive with a different variant on another slide (e.g. `![bg right:40%](...)`) to increase directive variety.

The refine loop re-runs the **visual gate only** after injection — not the full rubric rescorer — and caps at 2 refinement iterations total (same policy as the weighted loop). If the visual gate still fails after 2 refines, deliver with an explicit caveat naming the missing visuals.

**Delivery gate.** Both the weighted score (≥60) AND the hard gate (PASS) must be satisfied before the output is handed to the user. A deck that passes the weighted rubric but fails the hard gate is NOT delivered until the refine loop above has run; conversely, an output that passes the hard gate but still scores below threshold on the weighted rubric is subject to the weighted auto-refine loop documented below. The two loops are orthogonal — they can each trigger independently on the same output.

### Prose output: Document Quality Gate (Option 8, or Option 5 when docx)

Loaded when `output_class == "prose"`. Replaces the visual variety gate — prose documents have different mechanical floor requirements.

**Floor rules (ALL must pass):**

| Rule | Check |
|------|-------|
| Word count floor | `word_count >= 800` (prevents stubs) |
| Section count | `sections >= 4` (prevents wall-of-text) |
| Evidence density | `data_refs + citations + [DATA NEEDED] markers >= 3` (prevents opinion-only output) |
| Heading hierarchy | No skipped heading levels (h1 → h3 without h2 = FAIL) |
| Specificity floor | Fewer than 3 vague quantifiers ("significant", "several", "many", "various") where a number could be used |

**Implementation.** The prose gate is a text-scan check (analogous to the visual gate regex approach):
- Word count: split on whitespace, count tokens.
- Sections: count `^#{1,3} ` lines with `re.MULTILINE`.
- Evidence density: count `[DATA NEEDED]` markers + `Source:` tags + inline numbers (regex for `\d+[%$KMB]|\d+\.\d+`).
- Heading hierarchy: parse heading levels in order, flag jumps > 1.
- Specificity: count matches for `\b(significant|several|many|various|substantial|numerous|considerable)\b` (case-insensitive).

**Auto-refine behaviour on failure:**
- `"word count below floor"` → expand thin sections with detail from source material or depth-mining probes.
- `"sections below floor"` → split monolithic sections into logical sub-sections.
- `"evidence density below floor"` → inject `[DATA NEEDED]` markers where claims lack support, and mine source material for concrete numbers.
- `"heading hierarchy broken"` → fix heading levels.
- `"specificity below floor"` → replace vague quantifiers with concrete numbers from probe D1 or mark `[DATA NEEDED]`.

The refine loop re-runs the **document quality gate only** after fixes — not the full rubric rescorer — and caps at 2 iterations. If the gate still fails after 2 refines, deliver with an explicit caveat naming the gaps.

---

## Executive HTML Overlay Criteria (35 points — when output_class == "executive-html")

Loaded when `output_class == "executive-html"`. These criteria measure the quality of the obsidian design system rendering. Reference files: `references/rendering/executive-html-tokens.md`, `executive-html-components.md`, `executive-html-component-map.md`.

| # | Criterion | Weight | Scoring guide |
|---|-----------|--------|---------------|
| E1 | **Section headings + navigation** | 10 | Descriptive headings that build scroll-spy nav? Proper h2/h3 hierarchy? `.section-label` markers present? Logical depth layering (hero → sections → subsections)? |
| E2 | **Component selection** | 10 | Right component per content pattern (see `executive-html-component-map.md`)? KPIs→metric cards, lists→tile grids, quotes→quote boxes, mermaid→card-wrapped diagrams, code→code cards? |
| E3 | **Design token compliance** | 10 | All values use `var(--*)` tokens? Correct font families (Playfair / DM Sans / JetBrains)? `gradient-text` ≤1 per heading? Accent bars on cards? Both dark and light themes defined? Toggle functional? |
| E4 | **Density + visual rhythm** | 5 | No sparse sections (empty visual space without purpose)? No 3+ identical consecutive components? Separators between major sections? Scroll-reveal observers on cards? Responsive at 1024px and 720px breakpoints? |

**Executive HTML overlay total**: 10 + 10 + 10 + 5 = **35**.

**Grand total (base + executive-html)**: 65 + 35 = **100**.

### Executive HTML Hard Gate (binary pass/fail)

Loaded when `output_class == "executive-html"`. Replaces the visual variety and document quality gates.

**Floor rules (ALL must pass):**

| Rule | Check |
|------|-------|
| Self-contained | Single `.html` file, no external dependencies beyond Google Fonts |
| Theme toggle | `data-theme` attribute on `<html>`, toggle button present, localStorage persistence |
| Token coverage | 6 accent colors + 4 bg layers defined in both dark and light themes |
| Noise texture | `body::before` with SVG noise filter (`feTurbulence`) |
| Component minimum | `components >= ceil(sections / 2)` — enough visual variety |

**Implementation.** Text-scan check on the generated HTML:
- Self-contained: `<link` tags only reference `fonts.googleapis.com`.
- Theme toggle: file contains `data-theme=`, `themeToggle`, and `localStorage`.
- Token coverage: check `--accent-blue`, `--accent-cyan`, `--accent-amber`, `--accent-rose`, `--accent-violet`, `--accent-lime`, `--bg-deep`, `--bg-card`, `--bg-elevated`, `--surface` are present. Check `[data-theme="light"]` block exists.
- Noise texture: check for `feTurbulence` in the source.
- Component minimum: count `class="section-label"` occurrences as sections; count card/tile/metric/callout/quote/timeline/table/pre elements as components.

**Auto-refine behaviour on failure:**
- `"not self-contained"` → remove external CSS/JS links, inline everything.
- `"theme toggle missing"` → inject the toggle scaffold from `executive-html-components.md` §Theme Toggle.
- `"token coverage insufficient"` → add missing token definitions from `executive-html-tokens.md`.
- `"noise texture missing"` → inject `body::before` noise overlay from `executive-html-components.md` §Page Structure.
- `"component minimum not met"` → expand thin sections with appropriate components from the component map.

The refine loop re-runs the **executive HTML gate only** after fixes — not the full rubric rescorer — and caps at 2 iterations. If the gate still fails after 2 refines, deliver with an explicit caveat naming the gaps.

---

## Post-render visual verification (DEFERRED after content review)

Text-based scoring cannot catch broken images, clipped diagrams, or layout overflow. Visual verification stays required for final render QA, but it is intentionally delayed until after content is persisted and reviewed.

All image-bearing slides require visual verification for final sign-off.

Order of operations:

1. Generate and score content.
2. Persist canonical markdown and get user content review.
3. Render requested formats.
4. Run visual verification.

For the deferred visual check:

1. Immediately before visual QA, ask the user: `Switch to a vision-capable model now for visual verification?`
2. Run `story-present-verify-visual --input <pre-rendered.md> --output-dir <slug>/verify --theme <name>` to screenshot every slide as PNG.
3. Inspect **all slides that contain any image asset** (mermaid/chart SVG render, PNG asset, screenshot, photo, excalidraw output) and confirm assets are present, readable, and not clipped.
4. If the current model cannot inspect images, pause and request model switch before continuing.
5. If switching is unavailable or declined, publish the verify folder for human review, set status to `visual-review-pending`, and do not mark final QA complete.
6. Apply the following failure criteria:
   - **Clipped diagram** (any node or label cut off) = FAIL -- simplify mermaid source (reduce node count, switch from LR to TB) and re-render.
   - **Missing image** (broken ref or empty space where image should be) = FAIL -- check asset paths and re-render.
   - **Text overflow** (bullets pushed off slide by large image) = FAIL -- reduce image size or split slide.
7. This check applies to ALL output formats, not just HTML. For interactive HTML, open the file and verify client-side Mermaid renders correctly. For PPTX, open the file and verify diagrams are embedded (not placeholder text). For DOCX, verify images appear in the document.
8. This step runs AFTER scoring and AFTER rendering because it verifies rendered output, not markdown source.

---

### Excalidraw visual verification (deferred, capability-aware)

When the deck contains excalidraw-rendered PNGs (placeholders replaced via the appendix pipeline), verify each generated image against these checks:

| Check | What to look for | Failure action |
|-------|-----------------|----------------|
| No text overflow | All text is fully visible within element bounds; no clipping at edges | Regenerate with smaller font or larger container elements |
| No overlapping elements | Elements do not stack on each other unintentionally; deliberate overlaps (e.g. grouped labels) are acceptable | Regenerate with adjusted positions or spacing |
| Arrows land correctly | Arrowheads touch or connect to their target elements; no floating arrow endpoints | Regenerate with corrected binding points |
| Readable at slide size | Text is at least 12px equivalent when rendered at 1280px viewport width; thin strokes remain visible | Regenerate with increased font size or stroke width |

If model-side image inspection is unavailable, request model switch first. If switching is unavailable or declined, hand off PNGs for human review and mark `visual-review-pending` until confirmed.

**2-iteration regeneration cap.** If an excalidraw image fails any of the checks above, regenerate the JSON and re-render the PNG. A maximum of 2 regeneration attempts per image is allowed. After 2 failed attempts, deliver the best version with an explicit caveat naming the quality issue (e.g. "P3 arrow endpoints do not connect cleanly -- manual adjustment recommended").

**Quality checklist reference.** If the excalidraw skill provides a quality checklist at `references/visual/excalidraw/quality-checklist.md`, consult it for additional rendering guidance. The checks above are the minimum required gate; the quality checklist may include additional best practices for element sizing, colour contrast, and hand-drawn style consistency.

---

## Auto-refine loop

After generating the deck, score it against the rubric above, then apply the threshold rules:

| Score | Action |
|-------|--------|
| **≥ 75** | Deliver to the user. No refinement needed. |
| **60 – 74** | Auto-refine once, re-score, deliver the refined version. |
| **< 60** | Auto-refine once, re-score. If still <60, refine again (second refine). Then deliver the final version with an explicit caveat listing the criteria that remained low-scoring. |

**Iteration cap**: no more than **2** refinement iterations total, regardless of starting score. Never loop indefinitely.

### Procedure

1. Generate the output per `references/templates/template-<framework>.md`. For prose output (Options 5 docx + 8), run the mid-generation prose refinement pass first (see SKILL.md §Mid-generation prose refinement).
2. **Iteration 0 — first scoring pass.**
   - Walk each base criterion (B1–B7) and each overlay criterion (S1–S4 or P1–P4), assign a 0..max-weight score, record the rationale.
   - Sum to a total out of 100.
   - Run the matching hard gate (visual variety or document quality).
3. **Decision:**
   - `total >= 75` → deliver. Done.
   - `60 <= total < 75` → go to Iteration 1 (refine once).
   - `total < 60` → go to Iteration 1 (refine once).
4. **Iteration 1 — refinement.**
   - Focus refinement on the lowest-scoring criteria from Iteration 0.
   - Re-score.
5. **Decision after Iteration 1:**
   - `total >= 75` → deliver. Done.
   - `total >= 60` → deliver the refined version. Done.
   - `total < 60` → go to Iteration 2 (second refine).
6. **Iteration 2 — second refinement.**
   - Again target the lowest-scoring criteria.
   - Re-score.
7. **Decision after Iteration 2:** regardless of score, deliver the final version. If `total < 60`, prepend an explicit caveat block:

   ```
   ## Quality caveat

   This output was generated and refined twice but still scored below the 60/100 threshold on the following criteria:
   - <criterion name>: <score>/<weight>
   - <criterion name>: <score>/<weight>

   Recommended next steps: <what the user should manually fix>.
   ```

8. Hand off to the delivery prompt.

---

## Criterion B5 -- Technical depth scoring guide

This criterion is **conditional**. It only applies when the technical-depth trigger fires (see `references/generation/technical-depth-mining.md`). When the trigger does NOT fire, award 5/5 automatically.

| Score | Description |
|-------|-------------|
| **5/5** | At least 3 distinct technical innovations from source material have dedicated slides/sections (not just bullets). Architectural decisions show the trade-off, not just the choice. |
| **3-4/5** | Technical content present but shallow -- bullet summaries where a diagram or code example would be more effective. |
| **1-2/5** | Source material has rich technical content but the output reads like an executive summary. |
| **0/5** | Technical source material completely ignored. |

### Auto-refine for B5

When B5 scores <=2 and a refine iteration is triggered, the refine pass must:

1. Re-run the extraction procedure from `references/generation/technical-depth-mining.md`.
2. Identify the top 3 unrepresented High-value items.
3. Replace the weakest slides with dedicated slides for those items.
4. Add mermaid fences for any diagrammable items (per the diagram picker in `references/generation/mermaid-diagram-picker.md`).

---

## Anti-inflation rules

To keep self-scoring honest (adapted from creative-director-skill):

- Never award full weight on a criterion the agent has not explicitly checked. Default to a conservative mid-range score if unsure.
- The agent must cite specific slide numbers in its rationale. "Slide 5 uses a topic label instead of an action title" is valid. "Titles look OK" is not.
- If the rationale is only one sentence, the score is probably inflated. Aim for one sentence per criterion minimum, plus cited slide numbers for any deduction.

---

## Recording results

Store the scoring result in the working notes block so the delivery prompt can reference it and the behave scenarios can assert on it. Use the matching output class template:

**Slide output (Options 1–7):**

```
scoring_result:
  output_class: slides
  iteration: 0
  total: 82
  base:
    structural_compliance: 20/20
    mece_coverage: 8/10
    audience_alignment: 9/10
    evidence_presence: 4/5
    technical_depth: 5/5
    narrative_flow: 9/10
    constraint_compliance: 5/5
  overlay:
    action_titles: 13/15
    one_message_per_slide: 9/10
    marp_syntax: 5/5
    slide_constraints: 5/5
  hard_gate: PASS
  caveat: null
```

**Prose output (Option 8, or Option 5 docx):**

```
scoring_result:
  output_class: prose
  iteration: 0
  total: 87
  base:
    structural_compliance: 18/20
    mece_coverage: 9/10
    audience_alignment: 10/10
    evidence_presence: 5/5
    technical_depth: 5/5
    narrative_flow: 10/10
    constraint_compliance: 5/5
  overlay:
    section_headings: 8/10
    paragraph_discipline: 9/10
    specificity_depth: 8/10
    prose_syntax: 5/5
  hard_gate: PASS
  prose_refinement:
    hedging_fixes: 3
    abt_injections: 1
    alternating_fixes: 0
    insight_landings: 2
    specificity_replacements: 4
    layered_depth_fixes: 1
  caveat: null
```
