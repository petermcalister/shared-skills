# How to write an engineering blog post that people actually read

> **When to load this file.** Load only for **prose outputs** — Option 5 (Conference / Tech Talk) when `output_intent = "docx"`, Option 8 (Design Doc / RFC), and any future internal blog / journey-post output. For slide outputs (Options 1–4, 6, 7, and Option 5 in slide mode), the line-editing rules in `writing-style.md` are sufficient.
>
> **How this differs from `writing-style.md`.** `writing-style.md` is the **line editor** — it governs titles, bullets, captions, and short body blocks at the sentence level (8-word titles, max 5 bullets, no complete-sentence bullets, kill "leverage/utilize", etc.). This file is the **structural editor** — it governs document architecture, section sequencing, paragraph rhythm (ABT, alternating rhythm), opening hooks, conclusion length, internal-audience tone calibration, and the layered-depth model for mixed-seniority readers. Load both for prose; the slide-shaped rules in `writing-style.md` (e.g. "Max 3 sentences per body block", "No complete sentences as bullets") do not apply to flowing prose.

---


**The single most important principle for compelling engineering blog writing is radical specificity.** Dan Luu's seminal research on corporate engineering blogs found that "there's a dearth of real, in-depth, technical writing, which makes any half decent, honest, public writing about technical work interesting." [Danluu](https://danluu.com/corp-eng-blogs/) [danluu](https://danluu.com/corp-eng-blogs/) The blogs engineers love—Stripe, Cloudflare, Netflix—share specific numbers, admit failures, and show real trade-offs. The blogs engineers ignore drown content in corporate hedging and vague claims of success. [danluu](https://danluu.com/corp-eng-blogs/) For a senior enterprise architect writing an internal "journey" post about how your agentic coding harness evolved over three months, the playbook below distills best practices from top engineering blogs, respected technical writers, and enterprise communication experts into a single actionable guide.

---

## The anatomy of posts from Stripe, Netflix, and Cloudflare

The highest-rated engineering blogs—scored by Draft.dev across writing quality, technical depth, consistency, and broad usefulness—share a remarkably consistent structure. **Meta Engineering, GitHub Engineering, Stripe Engineering, and Cloudflare** [Draft.dev](https://draft.dev/learn/engineering-blogs) all score 4.8/5.0 or higher, and their posts follow a pattern worth emulating.

The universal template begins with **1–2 paragraphs establishing the business problem and why it matters**, not the technology. Next comes background context: the technical landscape, constraints, and scale requirements that shaped decisions. The body walks through design decisions with explicit trade-offs—not just what was chosen, but what was rejected and why. Implementation details follow, with concrete code, diagrams, and architecture specifics. Results come with measurable outcomes. Finally, honest lessons learned close the piece.

Stripe's writing culture, documented by their documentation manager Dave Nunez, defaults to **narrative memos over slide decks**. [slab](https://slab.com/blog/stripe-writing-culture/) Their CEO uses footnotes in emails. [slab](https://slab.com/blog/stripe-writing-culture/) Engineers review each other's writing the way they review code. [Slab](https://slab.com/blog/stripe-writing-culture/) Cloudflare's CTO reads every blog post personally, and their legal review has a **one-hour SLO**—so lightweight some people don't think of it as an approval step. [danluu](https://danluu.com/corp-eng-blogs/) [Danluu](https://danluu.com/corp-eng-blogs/) This speed enables Cloudflare to publish analysis of a BGP outage just eight hours after the incident, while readers still care. [danluu](https://danluu.com/corp-eng-blogs/) Segment made blogging an explicit criterion in performance reviews and held "blogging retreats" to build the habit. [Danluu](https://danluu.com/corp-eng-blogs/) [danluu](https://danluu.com/corp-eng-blogs/)

What makes these blogs boring is equally instructive. Dan Luu found that companies with **14 stakeholders who must sign off** produce infrequent, watered-down content. [danluu](https://danluu.com/corp-eng-blogs/) Non-engineering approvals "mainly de-risk posts, remove references to specifics, make posts vaguer and less interesting to engineers." [Danluu](https://danluu.com/corp-eng-blogs/) [danluu](https://danluu.com/corp-eng-blogs/) The natural state of a lightly edited engineering blog is interesting. Companies have to actively make them boring. [Danluu](https://danluu.com/corp-eng-blogs/) [danluu](https://danluu.com/corp-eng-blogs/)

**Voice and tone** across top blogs converge on a shared principle: conversational but technically precise. Google's Developer Documentation Style Guide—originally internal since 2005, made public in 2017—recommends sounding like "a knowledgeable friend who understands what the developer wants to do." [ACES](https://aceseditors.org/news/2021/googles-style-guide-for-software-developers) Use active voice, present tense, second person when instructing, [Google Developers](https://developers.googleblog.com/making-the-google-developers-documentation-style-guide-public/) and sentence case for headings. Sean Goedecke, whose writing advice is widely cited in the engineering community, puts it more directly: minimize caveats. Say "companies reward pragmatic engineers" instead of "in my experience, I've seen companies reward pragmatic engineers, but every company operates differently so it's hard to say anything for sure." [Sean Goedecke](https://www.seangoedecke.com/on-writing/)

---

## How to structure a "then versus now" journey post

Your post—comparing what you described three months ago to where you are now—maps perfectly onto what storytelling experts call the **"Man in Hole" arc**, identified by Kurt Vonnegut as the most commercially successful story shape. The character starts in an okay state, falls into trouble, struggles, climbs out, and ends up better than where they started. [WXO](https://worldxo.org/the-heros-journey-in-modern-narratives-how-to-design-narratives-for-experiences/) In engineering terms: things were working, a problem or new requirement emerged, you tried approaches that didn't fully work, you found a better path, and now the system is improved. This shape triggers what Harvard Business Review research links to oxytocin release, improving both comprehension and recall.

The most actionable framework comes from Anvil's engineering team, who adapted Pixar's **Story Spine** for technical blog posts: [Anvil](https://www.useanvil.com/blog/engineering/writing-technical-blog-posts-with-the-story-spine/)

- Here's what we were doing (the status quo three months ago)
- But then we faced this challenge (what broke, scaled poorly, or needed to change)
- The problem was painful in these specific ways (establishing stakes with metrics)
- We went looking for solutions—here's what we needed and why (the quest)
- We considered approaches that didn't work—here's why (false starts and learning)
- We arrived at our current approach—here's why, and how it works (resolution with technical depth)
- Now the world is better and here's the proof (the new normal, with before/after data)

For your specific "what changed in three months" format, a purpose-built template works best. **Open with a snapshot of where you were three months ago**—specific metrics, the stack as it existed, the process you followed. Name the catalyst that forced change. Walk through key milestones chronologically, using "because of that" chains to show causality rather than just listing events. Present the current state using parallel metrics to section one, enabling direct comparison. Include an explicit before/after table or visualization. Close with lessons learned and what surprised you.

The **ABT (And-But-Therefore) framework** works beautifully at the paragraph level throughout journey posts. "[Context] AND [more context], BUT [complication], THEREFORE [action/resolution]." This three-beat structure creates natural forward momentum. [First AI Movers](https://www.firstaimovers.com/p/storytelling-frameworks-writers-2025) Herbert Lui's research on engineering blog archetypes notes that "more often than not, you've actually already written the words in memos or Slack or Threads—you just need to compile it together." [Herbert Lui](https://herbertlui.net/6-types-of-posts-for-corporate-engineering-blogs/) Your earlier blog post is itself raw material for the "before" section.

---

## Balancing personal reflection with technical rigor

The tension between storytelling and technical depth is the central craft challenge of engineering blog writing. The best posts resolve it through **alternating rhythm**: narrative context, then technical detail, then reflection, then the next technical block. The narrative provides the thread that pulls readers forward. The technical detail provides the credibility that earns their trust.

Paul Graham identifies four components of useful writing, which multiply together: **correctness** (true claims), **importance** (matters to readers), **novelty** (says something they didn't know), and **strength** (bold claims, skillfully qualified). [paulgraham](https://paulgraham.com/useful.html) His editing philosophy is ruthless: "If you write a bad sentence, you don't publish it. You delete it and try again." [paulgraham](https://paulgraham.com/useful.html) He rereads sentences over a hundred times before publishing. [paulgraham](https://paulgraham.com/useful.html)

Julia Evans, whose blog is among the most admired in the engineering community, models a different but complementary approach. Her process is to struggle with something, figure out how to solve it, and write about what helped. The blog posts aren't about the struggle for its own sake—she wouldn't write "I find Rust hard" because that wouldn't help anyone. Instead, she writes about the specific thing she learned that made the struggle end. [Jvns.ca](https://jvns.ca/blog/2021/05/24/blog-about-what-you-ve-struggled-with/) **For your post, this means each section should land on a concrete insight, not just a narrative beat.**

The ratio rule synthesized from multiple expert sources: for each reflective or contextual section, include at least one concrete technical detail—a metric, a code pattern, a before/after comparison. For each deep technical section, include at least one sentence of context or reflection. This prevents the post from becoming either a diary entry or a dry specification.

Charity Majors offers the most practical advice on length: "Keep it short, keep it snappy. Edit twice as much as you write. Short, pithy posts tend to be more memorable, get wider traction, and stick in people's minds more. Do NOT write 5000–8000 word monstrosities." [Substack](https://writethatblog.substack.com/p/charity-majors-on-technical-blogging) The consensus across sources is a **5–10 minute read** (roughly 1,000–2,500 words), [freeCodeCamp](https://www.freecodecamp.org/news/how-to-write-a-great-technical-blog-post-414c414b67f6/) with Criteo Engineering targeting seven minutes specifically. [Medium](https://medium.com/criteo-engineering/writing-a-tech-blog-post-tips-and-tricks-from-the-criteo-engineers-27682ffee1c) For longer content, split into a series.

---

## Writing for colleagues inside a tier-1 investment bank

Internal engineering blog posts have a superpower that external posts lack: **you can be radically specific and honest**. [Substack](https://writethatblog.substack.com/p/technical-blogging-lessons-learned) You can write "our legacy settlement system takes 47 seconds to process a batch that should take 2 seconds"—something no external blog would publish. This specificity is exactly what makes internal posts genuinely useful. The biggest mistake internal authors make is writing as if they're external, hedging everything into meaninglessness.

The tone calibration for internal audiences is straightforward: **write like a person, not a corporation**. [Medium](https://medium.com/collaborne-engineering/how-to-write-an-engineering-blog-4e20280c0aa6) Brian Crawford's widely cited advice for internal blogging is blunt: "Be yourself, and write as if you were speaking to your audience in person. There's no need for stuffy language. We already know you're smart—you work here." [LinkedIn](https://www.linkedin.com/pulse/ten-tips-writing-perfect-internal-blog-post-brian-crawford) Avoid "it was determined that the optimal approach would be" when "we decided to" works better. Kill corporate jargon. Say who did what. [Intranet Connections](https://intranetconnections.com/blog/internal-blog/) First person is not just appropriate—it's preferred.

For a mixed audience of senior leaders, fellow architects, and developers, use **layered depth**. The structure that serves all three: [Lumen Learning](https://courses.lumenlearning.com/suny-esc-technicalwriting/chapter/audience/)

- **Layer 1 (30 seconds):** Title plus a TL;DR of 2–3 sentences stating what, why, and impact. Serves everyone, especially executives.
- **Layer 2 (2 minutes):** Problem statement and business context. Accessible to senior leaders.
- **Layer 3 (5 minutes):** Solution overview and decision rationale. Serves architects and senior developers.
- **Layer 4 (10+ minutes):** Implementation details and lessons. Serves practitioners who want specifics.

Clear section headings let readers self-select their depth. [Lumen Learning](https://courses.lumenlearning.com/suny-esc-technicalwriting/chapter/audience/) Include explicit skip-ahead guidance: "If you just want the outcome, see Section 3."

**Handling proprietary constraints** in a regulated financial institution requires a simple pre-publication checklist rather than a paralysing review committee. [Pressbooks](https://pressbooks.pub/coccoer/chapter/audience-analysis/) Check that the post contains no material non-public information, no client names or identifying details, no specific trading positions or strategies, no unpatched security vulnerabilities, and respects information barriers between departments. [Theta Lake](https://thetalake.com/blog/modern-approaches-to-information-barriers-for-finance/) This checklist, maintained by the author plus one compliance-aware reviewer, covers 95% of posts. When you need to generalize sensitive numbers, say so explicitly: "We process millions of events per day through our messaging layer (details generalized)" is better than vague claims about "handling a lot of data."

**Connect engineering work to business value**—this is where financial services engineering posts often fall short. Always bridge the gap: "This optimization reduced our options pricing calculation from 200ms to 15ms, which means traders can quote clients faster in volatile markets." Frame the regulated environment as a feature, not a constraint. Engineering for compliance, auditability, disaster recovery, and data governance presents genuinely interesting challenges that are unique to the industry.

---

## Hooks, pacing, diagrams, code, and conclusions

**Opening hooks** are where most engineering posts fail. Paul Graham's test is devastating: "Useful writing tells people something true and important that they didn't already know, and tells them as unequivocally as possible." [paulgraham](https://paulgraham.com/useful.html) For your journey post, consider opening with the most surprising metric or change: "Three months ago, our agentic coding harness took X minutes to do Y. Today it takes Z." Or open with a mistake: "In my last post, I recommended approach A. I was wrong." The loop-and-callback technique—opening with a provocative outcome, telling the full story, then returning to the opening with full context—creates especially satisfying reads.

**Pacing** follows Paul Graham's advice: "Write in spoken language." Read your draft out loud. Where you stumble, rewrite. Where you dread reading, cut. His editing process is "loose, then tight"—write the first draft fast, trying all kinds of ideas, then spend days rewriting carefully. [paulgraham](https://paulgraham.com/useful.html) He expects **80% of the ideas in an essay to emerge after writing begins**, and 50% of starting ideas to be wrong. [paulgraham](https://paulgraham.com/writing44.html)

**Code examples** should be runnable, production-worthy, and annotated with comments explaining the "why," not the "what." [DevRel Bridge Agency](https://devrelbridge.com/blog/developer-friendly-blog-post-structure) MDN Web Docs' guidelines note that readers copy and paste code directly into production, so examples must follow best practices. [MDN Web Docs](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide) Keep lines short enough to avoid horizontal scrolling. Show good and bad patterns side by side when illustrating what changed. For a journey post specifically, showing the old code approach next to the new one—with a brief annotation of what changed and why—is extremely effective.

**Diagrams** are essential for architecture posts. [Google](https://www.hireawriter.us/technical-content/diagramming-in-technical-blog-posts) Draft.dev's guidance prioritizes clarity over completeness: "Include only the components essential to understanding your article's main point." [Draft.dev](https://draft.dev/learn/how-to-create-diagrams-for-technical-blog-posts) Use consistent symbols and color schemes. [SCIMUS](https://thescimus.com/blog/writing-better-technical-design-documents-for-development-teams/) Write descriptive captions ("Figure 2 illustrates the authentication flow between services") instead of "as shown below." [SCIMUS](https://thescimus.com/blog/writing-better-technical-design-documents-for-development-teams/) Tools like Excalidraw produce a hand-drawn aesthetic that feels approachable; [Black Girl Bytes](https://blackgirlbytes.dev/the-ultimate-guide-to-writing-technical-blog-posts) Mermaid diagrams can be version-controlled alongside text. [Google](https://www.hireawriter.us/technical-content/diagramming-in-technical-blog-posts) For your before/after post, **parallel architecture diagrams showing the old and new system side by side** will be the single most valuable visual element.

**Conclusions** should be **3–5 sentences** that connect back to the opening without merely repeating it. [Medium](https://medium.com/quark-works/tips-on-how-to-write-your-first-successful-technical-blog-4cb65e5b4ce4) Include a next step for the reader—try the technique, implement the pattern, explore a related topic. Paul Graham's advice: "Learn to recognize the approach of an ending, and when one appears, grab it." [paulgraham](https://paulgraham.com/writing44.html) Don't force a conclusion; recognize the natural stopping point.

---

## A practical blueprint for your post

Given your specific situation—a senior enterprise architect writing an internal follow-up post about how your agentic coding harness evolved over three months—here is a concrete structural blueprint synthesized from all the research above.

**Title:** Make it specific and searchable internally. Something like "Building our agentic coding harness: what changed in three months" rather than "Agentic coding harness update." [Medium](https://medium.com/collaborne-engineering/how-to-write-an-engineering-blog-4e20280c0aa6)

**TL;DR (2–3 sentences):** State the biggest change, the most important metric, and why colleagues should care. Bottom line up front.

**Section 1 — Where we were.** Reference your earlier post explicitly. Summarize the original approach in 2–3 paragraphs with the key metrics and architecture diagram from three months ago. Be honest about what you got right and what assumptions have since proven wrong. This is your "ordinary world."

**Section 2 — What forced us to change.** Identify the specific catalyst—a scaling problem, user feedback, a failed experiment, a new requirement. Use the ABT framework: we had X, AND it worked for Y, BUT then Z happened, THEREFORE we had to rethink.

**Section 3 — The messy middle.** This is where the story lives. Walk through what you tried, including dead ends. Use "because of that" chains to show how one discovery led to the next. Include code comparisons (old pattern versus new) and an updated architecture diagram. Alternate between narrative reflection and technical specifics.

**Section 4 — Where we are now.** Present the current state using parallel metrics to Section 1, enabling direct comparison. A before/after table with specific numbers is powerful here. Show what's better and what trade-offs you accepted.

**Section 5 — What surprised us.** The non-obvious lessons. What would you tell your three-months-ago self? This section is often the most valuable for readers and the most memorable.

**Closing (3–5 sentences):** What's next for the harness, and what question you're still wrestling with. End with an open thread, not a period.

Throughout, bold key numbers and insights for scannability. [Horizonpeakconsulting](https://www.horizonpeakconsulting.com/write-technical-complex-blogs/) Use first person. Be specific about internal systems by name. Keep it under 2,500 words. Have one trusted colleague review before publishing—not a committee. [Medium +2](https://medium.com/quark-works/tips-on-how-to-write-your-first-successful-technical-blog-4cb65e5b4ce4) And remember Charity Majors' advice: "Pull on the threads of whatever is deeply interesting to you, and try to put something out there. If it's interesting to you, it's going to be interesting to someone else." [Substack](https://writethatblog.substack.com/p/charity-majors-on-technical-blogging)