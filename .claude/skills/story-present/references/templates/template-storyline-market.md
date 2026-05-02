# Template — Option 2: Market Strategy / Pitch Deck

Loaded by SKILL.md when the routing matrix picks Option 2. Defines the 12-slide sequence for investor pitches, fundraising decks, and market-positioning presentations.

**Source**: Community enterprise-ai-skills storyline-builder Template 1 (adapted). Extended with action-title discipline from the McKinsey Pyramid Principle because consulting frameworks — even pitch decks — benefit from titles that state a finding.

**Arc pattern**: **Market → Position → Product → Differentiation → Growth → Roadmap**

---

## Structural rules (apply to every slide)

1. **Action titles.** Every slide title is a complete sentence stating a finding or claim, not a topic label.
   - BAD: `Market Opportunity`
   - GOOD: `The European SaaS market will grow from $8B to $21B by 2028`
2. **One message per slide.** Each slide communicates exactly one idea. If you have two points, you need two slides.
3. **Numbers before adjectives.** Market sizing, growth rates, revenue, ACV — cite the number first, then the qualitative claim.
4. **Source every data point.** Cite via trailing `<!-- Source: ... -->` per `references/generation/marp-conventions.md`.
5. **Title slide uses `_class: lead`.** All other slides use the default layout.

---

## Slide sequence (12 slides)

| # | Purpose | Title style | Content structure |
|---|---------|-------------|-------------------|
| 1 | Title | Company/product name + tagline + date | `<!-- _class: lead -->`; company/product name, one-line tagline, author/presenter, date |
| 2 | Market opportunity | Action title stating the TAM/SAM/SOM finding | TAM / SAM / SOM sizing with growth rate; cite source. **MUST** contain a chart skeleton — see **Slide 2 visual mandate** below |
| 3 | Segment positioning | Action title stating where we play | Which segment within the market, with rationale for that choice |
| 4 | Competitive landscape | Action title stating the competitive shape | Top 3–5 competitors with revenue and growth comparison. **MUST** contain a chart skeleton — see **Slide 4 visual mandate** below |
| 5 | Our position | Action title stating our current rank | Revenue, growth rate, market rank; cite source |
| 6 | Product–market fit | Action title stating the fit claim | Product ↔ use case ↔ target customer mapping; evidence (retention, NPS, logos) |
| 7 | Customer profile | Action title stating who pays us | Top customer segments, enterprise vs SMB split. **MUST** contain a visual — see **Slide 7 visual mandate** below |
| 8 | Pricing model | Action title stating the pricing claim | Pricing structure (tiers, per-seat, usage, ACV) + average contract value |
| 9 | Differentiation | Action title stating the differentiator | Technology/approach vs competitors; what we do they can't |
| 10 | Competitive advantages | Action title stating the advantage set | 3 key advantages with evidence (data, customer quotes, benchmarks) |
| 11 | Growth opportunities | Action title stating the growth bet | 3 identified opportunities, prioritised with rationale |
| 12 | 18-month roadmap | Action title stating the roadmap claim | Priority capabilities mapped to 18-month timeline; investment ask if relevant |

---

## Slide 1 — Title slide template

```markdown
---
marp: true
theme: consulting
paginate: true
---

<!-- _class: lead -->

# [Company or product name]

[One-line tagline stating the positioning]

[Presenter] · [Date]
```

---

## Slide 2 — Market opportunity template

```markdown
# [Action title stating the TAM/SAM/SOM finding — e.g. "The European SaaS market will grow from $8B to $21B by 2028"]

| Layer | Size today | Size in 3 years | CAGR |
|-------|-----------|-----------------|------|
| TAM | $X | $Y | Z% |
| SAM | $X | $Y | Z% |
| SOM | $X | $Y | Z% |

[Chart placeholder: TAM/SAM/SOM stack with growth trajectory]

<!-- Source: [analyst report / primary research / working-notes item] -->
```

---

## Visual mandates (mandatory skeletons per visual slide)

Slides 2, 4, and 7 MUST contain visual skeletons. The generator MUST NOT emit these slides with only text or generic placeholders.

### Slide 2 visual mandate (TAM/market sizing)

Slide 2 MUST contain a chart fence skeleton for market sizing:

````markdown
```chart
{type: bar, data: {labels: ["TAM","SAM","SOM"], values: [100,40,10]}, title: "<infer market name> Market Sizing ($B)"}
```
````

### Slide 4 visual mandate (competitive landscape)

Slide 4 MUST contain a chart fence skeleton for competitor comparison:

````markdown
```chart
{type: bar, data: {labels: ["<competitor 1>","<competitor 2>","<competitor 3>","Us"], values: [80,60,40,25]}, title: "Revenue Comparison ($M)"}
```
````

### Slide 7 visual mandate (customer profile)

Slide 7 MUST contain a split-image visual with a placeholder directive and appendix back-reference:

```markdown
![bg right:40%](placeholder://visual-needed)

*[See Appendix: P<n> — Customer segment profile]*
```

Appendix row: `| P<n> | 7 | **Customer segment profile** — Persona card, segment breakdown, or logo grid. Right 40% composition, customer data flows left. Key elements: <infer from source>. Clean, data-forward pitch register. | excalidraw-diagram |`

---

## Arc and title-only test

After generating all 12 slides, read just the titles in order. The result should read like a coherent pitch:

```
1.  [Company + tagline]
2.  The market is big and growing at X%.
3.  We play in segment Y for reason Z.
4.  The competitive shape looks like [pattern].
5.  We rank Nth today with $X revenue.
6.  Our product fits use-case U for customer C — proven by E.
7.  Our customers are mostly [segment] paying [ACV].
8.  We price at [model] at [$ACV].
9.  We win because [differentiator].
10. Our three advantages are A, B, C — proven by [data].
11. The next wave of growth comes from opportunities G1, G2, G3.
12. Over the next 18 months we will ship [capability roadmap].
```

**Arc**: Market → Position → Product → Differentiation → Growth → Roadmap — the six acts of the deck, each covered in two slides.

---

## Compression rules

If Q5 constrained the deck to fewer than 12 slides:
- First to drop: slide 11 (growth opportunities) — fold into slide 12 roadmap.
- Next to drop: slide 7 (customer profile) — fold into slide 6 product-market fit.
- Minimum: 8 slides — title + market + position + competitive + PMF + pricing + differentiation + roadmap.
- Below 8, refuse and explain the minimum.

---

## Evidence and citation expectations

- Every market-sizing number must cite a source (analyst report, primary research, customer interviews, public filings).
- Every competitor data point must cite a source (10-K, press release, analyst note).
- Every customer metric (retention, NPS, ACV) must link to the working-notes item from ingestion.
- Unsourced numbers in pitch decks are a credibility failure — the scoring-rubric penalises them heavily (criterion 6, weight 10).
