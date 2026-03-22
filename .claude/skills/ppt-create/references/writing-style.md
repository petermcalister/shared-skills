# Writing Style Guide

Rules for writing slide content. Apply these when generating text for the JSON manifest.

---

## Title Rules

Slide titles carry the message. A reader skimming only titles should understand the full narrative.

1. **Action-oriented** — Lead with the conclusion, not the topic.
   - Good: "PostgreSQL Drives 45% of Total Spend"
   - Bad: "Database Cost Overview"

2. **Lead with the conclusion** — The title IS the takeaway.
   - Good: "Migration Cuts Latency by 60%"
   - Bad: "Latency Results After Migration"

3. **One idea per title** — If you need "and", split into two slides.
   - Good: "Redis Caching Eliminates Hot Spots"
   - Bad: "Redis Caching and Database Sharding Results"

4. **Max 8 words** — Shorter titles have more impact. Cut filler words.
   - Good: "Three Apps Exceed Cost Thresholds"
   - Bad: "A Summary of the Three Applications That Have Exceeded Their Cost Thresholds"

5. **Never repeat section headers** — A slide title must add information beyond its section name.
   - Good (section "Performance"): "Response Times Drop Below 200ms Target"
   - Bad (section "Performance"): "Performance Overview"

---

## Bullet Rules

Bullets are for scanning, not reading. Each one should stand alone.

1. **Parallel structure** — Every bullet in a list must use the same grammatical form.
   - Good: "Reduced latency by 40%", "Eliminated cold starts", "Cut costs by $12K/month"
   - Bad: "Reduced latency by 40%", "Cold starts are now eliminated", "We cut costs by $12K/month"

2. **Front-load key info** — Put the number or conclusion first.
   - Good: "18.40/GB -- App Gamma exceeds threshold by 84%"
   - Bad: "App Gamma has a cost per GB of 18.40 which exceeds the threshold by 84%"

3. **Max 5 bullets per slide** — More than 5 means the slide needs splitting.

4. **Max 2 lines per bullet** — If a bullet wraps beyond 2 lines, it belongs in body text.

5. **No complete sentences** — Bullets are fragments. Drop "We", "The team", "It is".
   - Good: "Deployed to 3 regions in Q3"
   - Bad: "We deployed the solution to 3 regions in Q3."

---

## Prose Rules

Body text on slides should be concise and direct.

1. **Active voice always** — The subject acts.
   - Good: "The platform processes 2M requests daily"
   - Bad: "2M requests are processed daily by the platform"

2. **Concrete over abstract** — Use specific numbers and names.
   - Good: "3 of 12 applications exceed 10/GB"
   - Bad: "Several applications have elevated costs"

3. **Data-first phrasing** — For metrics slides, lead with the number.
   - Good: "42% of traffic originates from the API gateway"
   - Bad: "The API gateway is responsible for a significant portion of traffic"

4. **Short paragraphs** — Max 3 sentences per body text block. If you need more, add bullets.

5. **No hedging** — Cut "might", "could potentially", "it appears that". State the finding.

---

## Caption Rules

Captions describe what to notice in a diagram or image.

1. **Describe the insight, not the figure** — The reader can see it is a figure.
   - Good: "Latency spikes correlate with deployment windows"
   - Bad: "Figure 1: Latency Chart"

2. **Under 15 words** — Captions are signposts, not explanations.

3. **No figure numbering** — Slides are not papers. Drop "Figure 1:", "Chart 2:".

4. **Point to the specific detail** — Guide the eye.
   - Good: "Red cluster shows the three over-threshold applications"
   - Bad: "Application cost distribution"

---

## Anti-Patterns

Reject these patterns during content generation. If any appear, rewrite.

### Generic agenda slides
Do not create slides titled "Agenda" or "Overview" that just list section names. The title slide and section headers serve this purpose.

### Repeating section headers as titles
Every slide title must add information. "Performance" as both a section header and a slide title wastes the reader's attention.

### Complete sentences as bullets
Bullets are fragments. If you wrote a period at the end, it is too long.

### Filler phrases
Remove on sight:
- "It is important to note that"
- "As we can see from the data"
- "In this section we will discuss"
- "Let's take a look at"
- "Moving on to the next topic"

### Closing cliches
Do not use:
- "In conclusion"
- "To summarise"
- "Thank you for your time"
- "Any questions?"

### AI-sounding language
These words signal generated content. Replace with plain English:
- "leverage" -> "use"
- "utilize" -> "use"
- "streamline" -> "simplify" or "speed up"
- "cutting-edge" -> name the specific technology
- "game-changer" -> describe the actual impact
- "synergy" -> "combined effect" or just cut it
- "paradigm shift" -> describe what changed
- "holistic approach" -> "full scope" or just cut it
