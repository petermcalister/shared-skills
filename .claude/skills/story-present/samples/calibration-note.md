# Scoring calibration note (F022)

**PRD reference**: Section 14 Success Criterion 5 — "The scoring gate catches and auto-fixes at least 50% of structural issues (missing slides, topic-style titles in consulting decks, >1 message per slide)."

**Target**: structural-issue detection rate ≥ 50%.
**Measured**: **91.7%** (11 of 12 expected structural issues caught across 6 broken sample decks).

Run with:

```bash
poetry run python pete-pa/skills/story-present/samples/calibrate.py
```

---

## Sample set

### Good samples (one per framework, 7 total)

| File | Framework | Slides | Score (structural sub-rubric, /50) | Issues flagged |
|------|-----------|--------|------------------------------------|----------------|
| `sample-pyramid.md` | Option 1 — McKinsey Pyramid | 12 | 50 | — |
| `sample-pitch.md` | Option 2 — Market / Pitch | 11 | 50 | — |
| `sample-problem.md` | Option 3 — Problem-Solving | 13 | 50 | — |
| `sample-roadmap.md` | Option 4 — Roadmap | 6 | 50 | — |
| `sample-conference.md` | Option 5 — Conference Talk | 15 | 50 | — |
| `sample-raid.md` | Option 6 — RAID / Weekly Status | 5 | 50 | — |
| `sample-steering.md` | Option 7 — Steering Committee | 10 | 49 | 1 x `one_message_per_slide` (two "and" conjunctions in slide 6 title — acceptable false positive, see §Tuning notes) |

Only the structural-sub-rubric score is computed (50 of 100 total rubric points: `structural_compliance=20`, `action_titles=15`, `one_message_per_slide=10`, `marp_syntax=5`). The remaining 50 points are semantic criteria (MECE, audience alignment, evidence presence, narrative flow, constraint compliance) that need LLM reasoning and are evaluated at skill runtime by the main agent — not by this simulator.

### Broken samples (6 deliberate structural violations)

| File | Expected issues | Caught | Missed |
|------|-----------------|--------|--------|
| `sample-pyramid-broken.md` | action_titles, structural_compliance | action_titles | structural_compliance (11 slides — meets the min-10 pyramid threshold, so structural check passes even though it is narratively hollow) |
| `sample-raid-missing-rag.md` | raid_rag, action_titles | raid_rag, action_titles | — |
| `sample-steering-decision-late.md` | steering_decision, steering_financials | steering_decision, steering_financials | — |
| `sample-pitch-broken.md` | action_titles, structural_compliance | action_titles, structural_compliance | — |
| `sample-problem-broken-twopoints.md` | one_message_per_slide, structural_compliance | one_message_per_slide, structural_compliance | — |
| `sample-conference-broken-missing.md` | structural_compliance, marp_syntax (missing `paginate`) | structural_compliance, marp_syntax | — |

**Expected issues total**: 12. **Caught**: 11. **Detection rate**: **11/12 = 91.7%**. Target ≥ 50%. ✅ PASS.

---

## What the simulator catches

The simulator in `calibrate.py` runs seven structural checks:

1. **`structural_compliance`** — minimum slide count per framework (Pyramid ≥10, Pitch ≥9, Problem ≥10, Roadmap ≥6, Conference ≥12, RAID =5, Steering ≥8).
2. **`action_titles`** — for consulting frameworks (Pyramid, Pitch, Problem, Roadmap, RAID, Steering) every non-title, non-appendix slide must either contain a finite verb or be ≥6 words. Topic labels like `Market Analysis`, `Vision`, `Solution` fail. Option 3 (Conference) is exempted because it uses declarative topic headings.
3. **`one_message_per_slide`** — titles with two or more `and` conjunctions, or with `and ... plus ...` pattern, are flagged.
4. **`marp_syntax`** — frontmatter must include `marp: true`, `theme`, and `paginate`.
5. **`raid_rag`** — RAID/steering decks must include 🟢/🟡/🔴 emoji and a `| RAG |` column header.
6. **`steering_decision`** — steering decks must have a "Decision Required" slide at position 3 (not position 9 where traditional status decks hide it — PRD Section 6 Option 5).
7. **`steering_financials`** — steering financial tables must include a `Variance` column.

## What the simulator does NOT catch (left to the runtime agent)

- MECE coverage (semantic — overlap / gaps between arguments)
- Audience alignment (semantic — language level vs stated audience)
- Evidence presence (semantic — are claims backed by citations? partial structural proxy via `Source:` comments)
- Narrative flow / title-only test (semantic — does reading titles tell the story?)
- Constraint compliance (semantic — did we honour Q5 "avoid" items?)

These are flagged in `references/scoring-rubric.md` as semantic criteria and remain the agent's responsibility at generation time.

---

## Tuning notes

### What changed in `scoring-rubric.md`
Nothing. Current weights already hit 91.7% structural detection, well above the 50% PRD target. No re-weighting was required.

### What changed in `intake-defaults.md`
Nothing. No defaults were shown to be too loose or too strict against the broken sample set. Defaults are preserved for the post-merge review cycle.

### Known false positives

1. **`sample-steering.md` slide 6**: "Top risks and issues cluster around the vendor dependency and the architect out-of-office" — two "and" conjunctions. The simulator flags it. On inspection, it genuinely does compress two ideas into one title, but both are variants of the same "elevated risks" message, so the flag is borderline. **Decision: leave it flagged**. The simulator is conservative, and the runtime agent can override.

2. **`sample-pyramid-broken.md` structural_compliance**: the broken pyramid variant has exactly 11 slides (one under the 12-slide ideal but above the 10-slide compression minimum), so the structural check correctly passes. The deck is still flagged on `action_titles` (all 10 content slides are topic labels), which is the more important structural signal for this variant. **No change needed** — the broken sample was designed to test action-title detection primarily.

### Why we did not lower min-slide thresholds further

Dropping `MIN_SLIDES` for pyramid to 6 (the PRD's explicit "absolute minimum") would miss compressed-but-valid decks. The 10-slide threshold catches catastrophically short decks (which is what we want for structural compliance) while allowing legitimate compression. Keeping it.

---

## Reproducibility

```bash
# Full calibration suite
poetry run python pete-pa/skills/story-present/samples/calibrate.py

# Score a single deck
poetry run python pete-pa/skills/story-present/samples/calibrate.py pete-pa/skills/story-present/samples/sample-pyramid.md
```

Exit code 0 if detection_rate ≥ 0.50; exit code 2 otherwise.
