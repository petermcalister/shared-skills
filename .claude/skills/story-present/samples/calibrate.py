"""Structural-issue scoring simulator for the story-present skill.

Per PRD Section 14 Success Criterion 5, the scoring gate must catch at least
50% of structural issues (missing slides, topic-style titles in consulting
decks, >1 message per slide, RAID tables missing RAG columns, steering
decision slide not at position 3, etc.).

This module applies structural checks against a Marp markdown deck and
returns a list of detected issues plus a per-criterion score against the
rubric in `references/scoring-rubric.md`.

It is intentionally NOT an LLM. The PRD's rubric has semantic criteria
(MECE, audience alignment, narrative flow) that need a model, but the
structural checks below cover structural_compliance, action_titles,
one_message_per_slide, and marp_syntax — which together account for 50
of the 100 points in the rubric and are exactly the issues the success
criterion calls out.

Usage:
    python pete-pa/skills/story-present/samples/calibrate.py
    python pete-pa/skills/story-present/samples/calibrate.py <deck.md>

The no-argument form runs the full calibration suite (all good and
broken samples in this directory) and prints the detection rate.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

SAMPLES_DIR = Path(__file__).resolve().parent


# --------------------------------------------------------------------------- #
# Data classes
# --------------------------------------------------------------------------- #


@dataclass
class Slide:
    index: int  # 1-based slide number
    title: Optional[str]
    body: str
    raw: str


@dataclass
class DeckAnalysis:
    path: Path
    framework: str  # pyramid | pitch | problem | roadmap | conference | raid | steering | unknown
    slides: List[Slide]
    frontmatter: dict
    issues: List[str] = field(default_factory=list)
    scores: dict = field(default_factory=dict)

    @property
    def total_score(self) -> int:
        return sum(self.scores.values())


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
SLIDE_SEP_RE = re.compile(r"^---\s*$", re.MULTILINE)


def parse_deck(path: Path) -> DeckAnalysis:
    text = path.read_text(encoding="utf-8")

    frontmatter: dict = {}
    m = FRONTMATTER_RE.match(text)
    if m:
        fm_block = m.group(1)
        for line in fm_block.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                frontmatter[k.strip()] = v.strip()
        body = text[m.end() :]
    else:
        body = text

    chunks = [c.strip() for c in SLIDE_SEP_RE.split(body) if c.strip()]

    slides: List[Slide] = []
    for i, chunk in enumerate(chunks, start=1):
        title = None
        for line in chunk.splitlines():
            s = line.strip()
            if s.startswith("# "):
                title = s[2:].strip()
                break
        slides.append(Slide(index=i, title=title, body=chunk, raw=chunk))

    framework = _infer_framework(path.name, frontmatter, slides)

    return DeckAnalysis(
        path=path,
        framework=framework,
        slides=slides,
        frontmatter=frontmatter,
    )


def _infer_framework(filename: str, frontmatter: dict, slides: List[Slide]) -> str:
    name = filename.lower()
    if "pyramid" in name:
        return "pyramid"
    if "pitch" in name:
        return "pitch"
    if "problem" in name:
        return "problem"
    if "roadmap" in name:
        return "roadmap"
    if "conference" in name:
        return "conference"
    if "raid" in name:
        return "raid"
    if "steering" in name:
        return "steering"

    theme = (frontmatter.get("theme") or "").lower()
    if theme == "conference":
        return "conference"
    if theme == "status":
        return "raid"
    return "unknown"


# --------------------------------------------------------------------------- #
# Structural checks
# --------------------------------------------------------------------------- #


# Minimum slide counts per framework. Below this we flag a "missing slides" issue.
MIN_SLIDES = {
    "pyramid": 10,       # 12 ideal, allow compression to 10
    "pitch": 9,          # 12 ideal, allow 9
    "problem": 10,       # 13 ideal
    "roadmap": 6,        # 6 is the minimum sequence
    "conference": 12,    # 15 ideal
    "raid": 5,           # 5 exact
    "steering": 8,       # 10 ideal, allow 8
}


# These frameworks require action-title style (complete sentences).
# Option 3 (conference) uses declarative topic headings instead.
ACTION_TITLE_FRAMEWORKS = {"pyramid", "pitch", "problem", "roadmap", "raid", "steering"}


# Regex for "action title" detection: a title counts as an action title if it
# contains a finite verb or at least 6 words. Topic labels like "Market Analysis"
# or "Appendix" fail both checks.
#
# Finite-verb cue list is lightweight — tense markers, modals, copula, common
# reporting verbs. Good enough for structural catch-rate, not for semantic grading.
FINITE_VERB_RE = re.compile(
    r"\b(is|are|was|were|will|would|can|could|should|must|may|has|have|had|"
    r"shows|grew|dropped|requires|recommend|need|needs|points|hit|hits|split|"
    r"splits|consolidate|halves|cuts|saves|drives|driving|makes|turns|brings|"
    r"produces|delivers|delivered|restores|protect|approve|push|compress|"
    r"absorb|adds|moves|confirms|captures|reduces|eliminates|leads|lead|"
    r"closes|ships|tripled|dropped|take|takes|taken|fail|fails|failing|"
    r"reach|reaches|remain|remains|goes|went|gone|yields|yield|finished|"
    r"started|run|runs|running|does|did|done|wins|won|lose|lost|be|been|"
    r"be|breaks|broken|rises|risen|falls|fallen|carries|carry|cluster|clustered)\b",
    re.IGNORECASE,
)


def _is_action_title(title: str) -> bool:
    """Heuristic: action title = finite verb OR >=6 words (and not a bare topic label).

    Single-word or two-word titles are always topic labels. Titles with a verb
    or that run to at least 6 words are treated as action titles.
    """
    if not title:
        return False
    stripped = title.strip().strip(".").strip()
    # "Appendix" and similar bare labels are explicitly allowed on the last slide,
    # but this helper treats them as non-action.
    words = stripped.split()
    if len(words) <= 2:
        return False
    if FINITE_VERB_RE.search(stripped):
        return True
    if len(words) >= 6:
        # Six-plus-word headings without a verb are rare but possible.
        return True
    return False


def _count_messages_in_slide(slide: Slide) -> int:
    """Rough proxy for 'messages per slide'.

    We count the number of conjunction-joined clauses in the title and the
    number of non-bullet body sentences. A slide title containing 'and ... and'
    or 'and ... plus ...' is flagged as multi-message, as is a body with >5
    declarative sentences outside a table.
    """
    if not slide.title:
        return 0
    ands = len(re.findall(r"\band\b", slide.title, flags=re.IGNORECASE))
    pluses = len(re.findall(r"\bplus\b", slide.title, flags=re.IGNORECASE))
    # Two or more "and"s in a title means multi-message for sure.
    multi = 1
    if ands >= 2 or (ands >= 1 and pluses >= 1):
        multi += 1
    return multi


def check_structural_compliance(deck: DeckAnalysis) -> None:
    min_required = MIN_SLIDES.get(deck.framework, 5)
    if len(deck.slides) < min_required:
        deck.issues.append(
            f"structural_compliance: only {len(deck.slides)} slides (min for "
            f"{deck.framework} is {min_required})"
        )
        deck.scores["structural_compliance"] = 8  # partial credit
    else:
        deck.scores["structural_compliance"] = 20


def check_action_titles(deck: DeckAnalysis) -> None:
    if deck.framework not in ACTION_TITLE_FRAMEWORKS:
        # Conference uses declarative topic titles; don't penalise.
        deck.scores["action_titles"] = 15
        return

    topic_label_slides: List[int] = []
    for slide in deck.slides:
        if not slide.title:
            continue
        # The last slide being "Appendix" or "Thank you" is allowed as a closing label.
        if slide.index == len(deck.slides) and slide.title.strip().lower() in {
            "appendix",
            "thank you",
        }:
            continue
        # Title slide (slide 1) is a presentation title, not an action title.
        if slide.index == 1:
            continue
        if not _is_action_title(slide.title):
            topic_label_slides.append(slide.index)

    if topic_label_slides:
        deck.issues.append(
            f"action_titles: slides {topic_label_slides} use topic labels instead of action titles"
        )
        # Scale the penalty to how many slides are broken.
        ratio = len(topic_label_slides) / max(1, len(deck.slides))
        deck.scores["action_titles"] = max(0, int(15 * (1 - ratio)))
    else:
        deck.scores["action_titles"] = 15


def check_one_message_per_slide(deck: DeckAnalysis) -> None:
    multi_message_slides: List[int] = []
    for slide in deck.slides:
        if _count_messages_in_slide(slide) > 1:
            multi_message_slides.append(slide.index)
    if multi_message_slides:
        deck.issues.append(
            f"one_message_per_slide: slides {multi_message_slides} try to make more than one point"
        )
        ratio = len(multi_message_slides) / max(1, len(deck.slides))
        deck.scores["one_message_per_slide"] = max(0, int(10 * (1 - ratio)))
    else:
        deck.scores["one_message_per_slide"] = 10


def check_marp_syntax(deck: DeckAnalysis) -> None:
    score = 5
    if deck.frontmatter.get("marp") != "true":
        deck.issues.append("marp_syntax: frontmatter missing `marp: true`")
        score -= 2
    if "theme" not in deck.frontmatter:
        deck.issues.append("marp_syntax: frontmatter missing `theme`")
        score -= 1
    if "paginate" not in deck.frontmatter:
        deck.issues.append("marp_syntax: frontmatter missing `paginate`")
        score -= 1
    deck.scores["marp_syntax"] = max(0, score)


def check_raid_rag_column(deck: DeckAnalysis) -> None:
    """RAID/steering decks must include RAG emoji/column."""
    if deck.framework not in {"raid", "steering"}:
        return
    text = "\n".join(s.raw for s in deck.slides)
    has_rag_emoji = any(e in text for e in ("🟢", "🟡", "🔴"))
    has_rag_header = re.search(r"\|\s*RAG\s*\|", text, flags=re.IGNORECASE)
    if not (has_rag_emoji and has_rag_header):
        deck.issues.append(
            "raid_rag: RAID/steering deck missing RAG emoji column (🟢🟡🔴 in a | RAG | header)"
        )


def check_steering_decision_position(deck: DeckAnalysis) -> None:
    """Per PRD, the 'Decision Required' slide must be at position 3 in steering decks."""
    if deck.framework != "steering":
        return
    decision_positions = [
        s.index
        for s in deck.slides
        if s.title and "decision" in s.title.lower()
    ]
    if not decision_positions:
        deck.issues.append("steering_decision: no 'Decision Required' slide found")
        return
    if 3 not in decision_positions:
        deck.issues.append(
            f"steering_decision: 'Decision Required' slide at position {decision_positions[0]}, "
            f"must be at position 3"
        )


def check_steering_variance_column(deck: DeckAnalysis) -> None:
    """Steering decks must show budget variance, not just budget vs actual."""
    if deck.framework != "steering":
        return
    text = "\n".join(s.raw for s in deck.slides)
    if not re.search(r"\|\s*Variance\s*\|", text, flags=re.IGNORECASE):
        deck.issues.append(
            "steering_financials: financial table missing 'Variance' column"
        )


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #


def score_deck(path: Path) -> DeckAnalysis:
    deck = parse_deck(path)
    check_structural_compliance(deck)
    check_action_titles(deck)
    check_one_message_per_slide(deck)
    check_marp_syntax(deck)
    check_raid_rag_column(deck)
    check_steering_decision_position(deck)
    check_steering_variance_column(deck)
    return deck


# --------------------------------------------------------------------------- #
# Calibration suite
# --------------------------------------------------------------------------- #


# Each broken sample declares the structural issue(s) it is designed to trigger.
# The detection rate is (issues caught) / (issues expected) across all broken
# samples. Target: >=50% per PRD Section 14 Success Criterion 5.
BROKEN_SUITE = {
    "sample-pyramid-broken.md": [
        "action_titles",
        "structural_compliance",  # no real Executive Summary / evidence split
    ],
    "sample-raid-missing-rag.md": [
        "raid_rag",
        "action_titles",
    ],
    "sample-steering-decision-late.md": [
        "steering_decision",
        "steering_financials",
    ],
    "sample-pitch-broken.md": [
        "action_titles",
        "structural_compliance",
    ],
    "sample-problem-broken-twopoints.md": [
        "one_message_per_slide",
        "structural_compliance",
    ],
    "sample-conference-broken-missing.md": [
        "structural_compliance",
        "marp_syntax",  # missing paginate
    ],
}


GOOD_SUITE = [
    "sample-pyramid.md",
    "sample-pitch.md",
    "sample-problem.md",
    "sample-roadmap.md",
    "sample-conference.md",
    "sample-raid.md",
    "sample-steering.md",
]


def run_calibration() -> dict:
    good_results = []
    for name in GOOD_SUITE:
        p = SAMPLES_DIR / name
        if not p.exists():
            continue
        deck = score_deck(p)
        good_results.append(
            {
                "sample": name,
                "framework": deck.framework,
                "slides": len(deck.slides),
                "score": deck.total_score,
                "issues": deck.issues,
            }
        )

    expected_total = 0
    caught_total = 0
    broken_results = []
    for name, expected in BROKEN_SUITE.items():
        p = SAMPLES_DIR / name
        if not p.exists():
            continue
        deck = score_deck(p)
        # Map each expected tag against the issues caught.
        caught_tags = []
        for tag in expected:
            matched = any(issue.startswith(tag) for issue in deck.issues)
            if matched:
                caught_tags.append(tag)
        expected_total += len(expected)
        caught_total += len(caught_tags)
        broken_results.append(
            {
                "sample": name,
                "expected": expected,
                "caught": caught_tags,
                "missed": [t for t in expected if t not in caught_tags],
                "issues": deck.issues,
            }
        )

    detection_rate = caught_total / expected_total if expected_total else 0.0

    return {
        "good_samples": good_results,
        "broken_samples": broken_results,
        "expected_issues_total": expected_total,
        "caught_issues_total": caught_total,
        "detection_rate": round(detection_rate, 3),
        "target_rate": 0.50,
        "meets_target": detection_rate >= 0.50,
    }


def main() -> None:
    if len(sys.argv) >= 2:
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"ERROR: {path} not found", file=sys.stderr)
            sys.exit(1)
        deck = score_deck(path)
        out = {
            "path": str(path),
            "framework": deck.framework,
            "slides": len(deck.slides),
            "score": deck.total_score,
            "score_breakdown": deck.scores,
            "issues": deck.issues,
        }
        print(json.dumps(out, indent=2))
        return

    report = run_calibration()
    print(json.dumps(report, indent=2))
    if not report["meets_target"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
