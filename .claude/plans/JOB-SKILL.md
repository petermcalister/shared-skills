---
name: pete-job-search
description: Use this skill whenever Pete asks to search for jobs, find new roles, repeat a job search, or check for engineering leadership opportunities. Triggers include phrases like "find me jobs", "repeat the search", "any new roles", "run the job search again", "what's out there", "refresh the shortlist", or any reference to job hunting, career search, or engineering vacancies. Also trigger when Pete asks to tailor his CV or LinkedIn for a specific role found through this search. This skill contains Pete's complete candidate profile, search criteria, exclusions, commute preferences, and scoring methodology — always consult it before running any job search to ensure consistency.
---

# Pete's Engineering Leadership Job Search

## Purpose

This skill codifies Pete's job search criteria so that any Claude agent can repeat a comprehensive, targeted search for senior engineering leadership roles in London financial services. It should be consulted before every job search to ensure consistency in criteria, exclusions, and scoring.

## Candidate Profile

### Identity
- **Name:** Peter McAlister
- **Current role:** Executive Director, J.P. Morgan, CIB Payments (October 2022 – Present)
- **Location:** Oxted, Surrey
- **Target:** Senior engineering leadership roles in London

### Core Technical Skills
- **Databases:** Oracle, PostgreSQL — deep expertise in schema design, performance tuning, capacity planning, data migration at scale, distributed transaction systems
- **Languages:** Python (primary), SQL, JavaScript
- **Cloud:** AWS (5x certified: DevOps Engineer Professional, Solutions Architect Associate, SysOps Administrator, Developer, Cloud Practitioner)
- **AI/ML:** Agentic AI systems, RAG pipelines (BM25/RRF ranking), LLM integration patterns, MCP tooling, structured feedback loops, guard rails
- **Architecture:** Distributed systems, event-driven architecture, CQRS, microservices, API-first design, CI/CD pipeline design
- **Regulatory:** Basel III, PSD2, GDPR, SOX compliance-adjacent work

### Career History (for alignment scoring)
1. **J.P. Morgan** — Executive Director, CIB Payments (2022–Present)
   - Database standards & policy for ~850 applications
   - Built Operational Meta Store (OMS) for metadata-driven agentic automation
   - Data Management Committee representative, reporting to CIB Head Architect
   - Champions AI-augmented development workflows
2. **Thought Machine** — Client Architect (2020–2022)
   - SaaS core banking (Vault), multi-cloud (AWS, Azure, GCP, Kubernetes, Kafka, CockroachDB)
   - Pre-sales wins in growth markets, architectural leadership
3. **GFT** — Solutions Architect / AWS Practice Lead (2016–2020)
   - Scaled AWS practice from £1M/year to £1M/month
   - 6 major engagements (£300K–£35M) across tier-1 banks
4. **J.P. Morgan** — VP, Information Architect & Analytics Team Lead (2014–2016)
   - Basel III intraday liquidity monitoring platform, cross-asset multi-region
5. **Bank of America Merrill Lynch** — VP, Data Architect (2009–2014)
6. **Barclays Capital** — Senior Developer, Prime Services (earlier career)

### Qualifications
- MSc Computer Science (Commendation) — University of Hertfordshire
- BSc (Hons) Biological Sciences (2:1) — University of Salford
- 5x AWS Certified

## Search Criteria

### Role Requirements (ALL must be met)
- **Seniority:** Director, VP of Engineering, Head of Engineering, Principal Engineer, Staff Engineer, Engineering Manager/Lead
- **Must include BOTH:** delivery accountability AND leadership/mentoring responsibilities
- **Industry:** Financial services, fintech, payments, capital markets, or companies selling technology into financial services
- **Location:** London-based (hybrid acceptable, must have London office presence)
- **Recency:** Posted within last 30 days

### Technical Alignment (prioritise roles matching 3+ of these)
- Python
- Oracle and/or PostgreSQL
- Database engineering / data platform strategy
- Distributed systems / distributed transaction processing
- Cloud infrastructure (AWS preferred)
- Agentic AI / AI engineering / LLM integration
- CI/CD, DevOps practices

### Exclusions (ALWAYS exclude)
- J.P. Morgan (current employer)
- S&P Global Data Engineering role at Ropemaker Place (already applied)
- Pure/dedicated SRE roles (on-call rotation focused, no delivery leadership)
- Pure Enterprise Architect roles (no delivery accountability or team leadership)
- Roles requiring deep ML model training experience (PyTorch/TensorFlow for training, not inference)

### Previously Searched Companies (check for new roles)
Barclays, Goldman Sachs, Morgan Stanley, Citi, HSBC, Deutsche Bank, UBS, Standard Chartered, NatWest, Lloyds, Mastercard, Visa, Wise, Revolut, Monzo, Starling, OakNorth, Checkout.com, ClearBank, 10x Banking, Thought Machine, Bloomberg, ICE, LSEG, Broadridge, Finastra, Temenos, Murex, Stripe, Adyen, WorldPay/FIS, GoCardless, Quantexa, Capital One UK

### Job Board Sources
LinkedIn Jobs, Indeed UK, CityJobs, eFinancialCareers, Glassdoor UK, TotalJobs, Technojobs, plus direct career pages of companies listed above.

## Commute Preferences

Pete commutes from **Oxted, Surrey** via Southern Rail and Thameslink.

### Optimal Stations (Thameslink direct or single train)
| Station | Route | Approx. Door-to-Door |
|---------|-------|---------------------|
| City Thameslink | Oxted → East Croydon → Thameslink | ~50 min |
| Blackfriars | Oxted → East Croydon → Thameslink | ~50 min |
| Farringdon | Oxted → East Croydon → Thameslink | ~52 min |
| Moorgate | Oxted → East Croydon → Thameslink | ~55 min |
| Barbican | Oxted → East Croydon → Thameslink | ~56 min |
| London Bridge | Oxted → Southern Rail direct | ~40 min |

### Acceptable with Interchange
| Station | Route | Approx. Door-to-Door |
|---------|-------|---------------------|
| Liverpool Street | London Bridge + Northern/Elizabeth line | ~55 min |
| Old Street | London Bridge + Northern line | ~48 min |
| Canary Wharf | London Bridge + Jubilee line | ~50 min |
| Bank/Monument | London Bridge + Northern line | ~45 min |

### Commute Scoring
- **Thameslink direct (no interchange):** +5 points
- **Single interchange from London Bridge:** +3 points
- **Under 50 min total:** +3 points
- **50–60 min total:** +1 point
- **Over 60 min total:** -2 points

## Alignment Scoring Methodology

Score each role out of 100 across these dimensions:

| Dimension | Weight | Scoring Guidance |
|-----------|--------|-----------------|
| **Technical overlap** | 30% | How many core skills match (Python, Oracle/PostgreSQL, distributed systems, AWS, AI/agentic)? |
| **Seniority fit** | 20% | Does the title/scope match ED-level? Step-up, lateral, or step-down? |
| **Delivery + leadership** | 20% | Does the role include both delivery accountability AND team mentoring? Exclude pure architecture or pure SRE. |
| **Domain alignment** | 15% | Financial services, payments, capital markets overlap? Regulatory familiarity? |
| **Commute** | 10% | Use commute scoring table above |
| **AI/Innovation signal** | 5% | Does the role mention AI, ML, agentic systems, or innovation? |

### Red Flag Checklist (note any that apply)
- [ ] Role posted >6 weeks ago (may be filled or hard-to-fill)
- [ ] No Python, SQL, or database mention (poor technical alignment)
- [ ] Pure people management with no technical depth
- [ ] Requires niche skills Pete lacks (e.g., C++, Scala, Rust, deep ML training)
- [ ] Consumer-facing domain with no FS crossover
- [ ] Contract/interim role (Pete seeks permanent)

## Output Format

For each role found, provide:

1. **Job title** and company
2. **Direct application URL** (verified working)
3. **London office location** and nearest rail/tube station
4. **Commute estimate** from Oxted with route
5. **Key requirements and tech stack**
6. **Salary** (published or market estimate)
7. **Date posted**
8. **Alignment score** (out of 100) with brief narrative covering database, distributed systems, AI/agentic, delivery leadership, and mentoring overlap
9. **Red flags or gaps**

Rank roles by alignment score descending. Include a brief market commentary section at the end covering demand trends, salary movements, and any notable patterns.

## Tips for Effective Searching

- Senior roles at tier-1 banks fill within days — speed matters
- Many Director+ roles are filled via headhunters (Selby Jennings, Huxley, Oliver Wyman) and never posted publicly — mention this to Pete
- Include year/date in search queries for recency (e.g., "2026")
- Search both job title variations: "Director of Engineering", "Head of Engineering", "VP Engineering", "Principal Engineer", "Engineering Director"
- Cross-reference multiple job boards — the same role often appears with different detail levels
- Verify application URLs are live before including in results
- Use web_fetch to read full job descriptions rather than relying on search snippets
