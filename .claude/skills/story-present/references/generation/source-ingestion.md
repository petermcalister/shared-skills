# Source Ingestion — CLI orchestration and working notes

**Purpose:** Operational guide for the "Source ingestion" step that runs **between Level 1 confirmation and the Level 2 interview**. Covers the 7 supported source types from PRD Section 4 Q6, the exact Bash invocation pattern for each, the working-notes block format, and the citation format slides must use so every claim links back to a retrieved item.

> **Ordering rule (critical):** Source ingestion runs **after** the Level 1 Understanding Check is confirmed and **before** Level 2 interview questions are asked. Level 2 questions should reference real retrieved data. Do not ingest after Level 2.

> **Topic-folder anchor rule:** Use the topic folder captured in Level 1 T0 as the default root for source (g) markdown evidence (`pete-pa/topics/<topic-folder>/`) unless the user provides a more specific path.

---

## 1. CLI shortcut mapping (verbatim from PRD Section 4)

| Q6 source | CLI shortcut(s) | Notes |
|-----------|----------------|-------|
| (a) Email (keyword) | `gmail-search`, `outlook-search` | Use `--json` and `--weeks` / `--days` derived from Q5 constraints |
| (a) Email (semantic) | `email-finder-search` | Use for "find anything like X" hybrid BM25 + vector retrieval |
| (b) Calendar | `calendar-events`, `outlook-calendar` | Filter by date range derived from Q5 constraints |
| (c) Team messaging (WhatsApp) | `whatsapp-messages --chat cowork-pa` (or named channel) | Channel name from Q6 hint |
| (d) Agent memory | `memory-search`, `memory-context`, `memory-recent` | Cross-tier retrieval (episodic / task / semantic) with FTS5 + optional vector search |
| (e) Saved agent conversations | `Read` / `Grep` on `.claude/` | No CLI — direct file access to prior session transcripts and distilled memories |
| (f) Git work reports | `git log`, `git diff`, `gh pr list` | Summarise via Bash |
| (g) Markdown reports | `Read` / `Grep` on `pete-pa/topics/<topic-folder>/`, `.claude/plans/` | Default paths if no hint |
| (h) None | — | Skip ingestion entirely; proceed straight to Level 2 using only interview answers |

---

## 2. Working notes block structure

Ingested items flow into a single working notes block that the skill carries from Level 1 into Level 2 and into template population. The block is a plain-markdown section the agent keeps in the working conversation — it is not a file — structured as follows:

```markdown
## Working Notes — Ingested Sources

### Source: <Q6 source type, e.g. "Agent memory">
- Query: <verbatim query/hint used>
- Invocation: <exact Bash line>
- Retrieved at: <ISO timestamp>

**Items**
- [<source-tag>] <short summary / subject / first line>
- [<source-tag>] <short summary / subject / first line>
- ...

### Source: <next Q6 source type>
...
```

The `<source-tag>` is the citation identifier used later on slides (see Section 4 below). One working-notes block may contain multiple `### Source:` sub-sections when Q6 selects more than one source type.

---

## 3. Per-source Bash invocation patterns

All shortcuts run inside the Poetry venv (`poetry run <shortcut>`) and emit `--json` where supported, so the agent can parse results and populate the working notes.

### 3.0 Deriving the date-range flag from Q5

Q5 collects constraints including time windows ("last 2 weeks", "this sprint", "last 8 weeks", "since Monday"). Map the phrase to a flag before running any shortcut:

| Q5 phrase | Flag |
|-----------|------|
| "last N weeks" / "past N weeks" | `--weeks N` |
| "last N days" / "past N days" / "this week" | `--days N` (with `this week` → `--days 7`) |
| "this sprint" / no window given | `--weeks 2` (default) |
| "last month" | `--weeks 4` |
| "last quarter" | `--weeks 13` |
| "this week" | `--weeks 1` |

The same flag is reused across `gmail-search`, `outlook-search`, `email-finder-search`, `calendar-events`, `outlook-calendar`, `whatsapp-messages`, and `memory-recent` so the user sees a consistent window regardless of source type.

### 3.1 Email — keyword search (Gmail or Outlook)

```bash
# Q5 constraint "last 8 weeks", Q6 hint "merger approval"
poetry run gmail-search "merger approval" --weeks 8 --json
poetry run outlook-search "merger approval" --weeks 8 --json
```

- `--weeks N` (or `--days N`) is derived from Q5 ("last 8 weeks" → `--weeks 8`).
- Each returned message becomes one working-notes item tagged `gmail-msg-<id>` or `outlook-msg-<entryid-short>`.

### 3.2 Email — semantic hybrid search

```bash
# Q6 hint "anything about the Q3 merger"
poetry run email-finder-search "anything about the Q3 merger" --top-k 10 --json
# Read full body for the most relevant hit
poetry run email-finder-read <email-uuid> --json
```

- Use `--top-k` ≥ 5 (default 10) so Level 2 has enough material to reference.
- Tag items as `email-<uuid-short>`.

### 3.3 Calendar

```bash
# Q5 constraint "this week"
poetry run calendar-events --weeks 1 --json
poetry run outlook-calendar --weeks 1 --json
```

- Tag items as `cal-event-<id>` or `outlook-cal-<entryid-short>`.

### 3.4 Team messaging (WhatsApp)

```bash
# Q6 hint "cowork-pa, last 7 days"
poetry run whatsapp-messages --chat cowork-pa --days 7 --json
```

- Tag items as `wa-<chat>-<msgid>`.

### 3.5 Agent memory

```bash
# Q6 hint "Q1 shipping"
poetry run memory-search "Q1 shipping" --json
poetry run memory-recent --days 30 --json
poetry run memory-context --json
```

- `memory-search` runs across all three tiers (episodic / task / semantic) with FTS5 and optional vector search.
- Tag episodic items `memory-event-<id>`, tasks `memory-task-<id>`, semantic facts `memory-fact-<id>`.

### 3.6 Saved agent conversations

```bash
# Direct file access — no CLI shortcut
# Prefer Grep for keyword search over Read for targeted extraction
```

Use the `Grep` tool against `.claude/` (plans, distilled memories, session transcripts). Tag items `claude-<relative-path>#<line>`.

### 3.7 Git work reports

```bash
# Q6 "sprint 24 summary"
git log --since="2 weeks ago" --oneline
git log --since="2 weeks ago" --format="%h %s" -- <path>
git diff <base>..HEAD --stat
gh pr list --state merged --limit 20
```

- Tag commits as `commit <short-sha>`, PRs as `pr-<number>`.

### 3.8 Markdown reports

```bash
# Default paths if Q6 gives no hint
# Use Grep to find candidate files, Read to pull full paragraphs
```

Search `pete-pa/topics/<topic-folder>/` and `.claude/plans/` (and any user-specified path). Tag items with their relative path, e.g. `pete-pa/topics/weekly-report/2026-04-weekly.md`.

---

## 4. Slide citation format

Every factual claim on a generated slide that comes from an ingested item **must** carry a `Source:` marker whose value is the `<source-tag>` recorded in the working notes. The agent should format it inline at the end of the bullet, or as a smaller line beneath a chart/quote, so the user can audit the source.

| Source type | Example citation |
|-------------|------------------|
| Gmail / Outlook keyword | `Source: gmail-msg-abc123` / `Source: outlook-msg-0000AB12` |
| Email semantic | `Source: email-<uuid-short>` |
| Calendar | `Source: cal-event-12345` |
| WhatsApp | `Source: wa-cowork-pa-987` |
| Memory — episodic | `Source: memory-event-42` |
| Memory — task | `Source: memory-task-7` |
| Memory — semantic fact | `Source: memory-fact-15` |
| Saved conversation | `Source: claude-.claude/plans/story-present.md#L42` |
| Git commit | `Source: commit 19f61a6` |
| Git PR | `Source: pr-123` |
| Markdown report | `Source: pete-pa/topics/weekly-report/2026-04-weekly.md` |

Claims without a source are allowed only for material the user gave directly in the interview — and even then should be marked `Source: interview` if the audience is executive / governance. If data is missing entirely, use the `[DATA NEEDED: ...]` placeholder from `marp-conventions.md` instead of fabricating a citation.

---

## 5. Q6 = None path

If Q6 selects (h) None, the skill **skips the ingestion step entirely** — no CLI shortcut is invoked, the working notes block is not created, and Level 2 proceeds using only the interview answers. The Understanding Check should record `Source material: interview answers only` in that case.

---

## 6. Order of operations checklist

1. Level 1 T0 + Q1–Q6 answered (or defaulted).
2. Understanding Check shown, user confirms.
3. **Source ingestion runs here** — per Q6 selections, one Bash invocation per source type from the table above.
4. Results captured into the working notes block (Section 2 format).
5. Level 2 interview begins, referencing the working notes.
6. Template population reads the working notes and emits slides with `Source: <tag>` citations (Section 4).
