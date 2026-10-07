#!/usr/bin/env python3
"""Replace generated C1/C2 phrase-fragment labels with contextual glosses.

The advanced CEFR batch split six complete target-language sentences into
short collocations, but labelled each item "discourse segment N in ...".  This
repair keeps the authored target phrases and replaces only the generated label
with a concise, contextual English gloss.  It does not claim native review.

Run `--check` to report drift or `--write` to apply the deterministic mapping.
"""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("ar", "bn", "de", "it", "ja", "ko", "pt", "ru", "zh")
LEVELS = ("C1", "C2")
PLACEHOLDER = re.compile(r"^discourse segment\s+\d+\s*(?:in|:)\s*", re.I)

# Six lesson-level sentence frames in each course.  The same conceptual
# sequence is intentional: the multilingual advanced courses teach comparable
# rhetorical moves, while every target-language phrase remains independently
# authored in its own course file.
GLOSSES = {
    "C1": (
        ("according to the report", "the report indicates", "it appears that",
         "that implementation", "implementation has", "has improved",
         "improved, although", "although it remains uneven"),
        ("although", "the evidence is", "the evidence is limited", "limited; neither",
         "neither should be", "should be ignored", "ignored, nor", "nor presented as final"),
        ("critical evaluation", "evaluation of changes", "changes affecting",
         "affecting", "society", "society requires analysis", "critical analysis",
         "analysis of context and method"),
        ("the data were", "the data were incomplete", "incomplete; therefore",
         "therefore postponed", "the committee postponed", "the decision",
         "the decision until", "until the causal link became clearer"),
        ("with full", "full respect", "respect for this", "this proposal",
         "this proposal; I would", "I would like", "like to offer",
         "to offer an alternative perspective"),
        ("reading both studies", "the two studies", "the studies together",
         "together reveals", "that contextual", "contextual difference",
         "difference explains", "explains part of the variation"),
    ),
    "C2": (
        ("the decision alone", "alone was not", "the decision itself",
         "itself was not the source", "the source of the flaw", "the flaw; rather",
         "rather, the manner", "the manner of implementation changed the outcome"),
        ("his silence", "silence indicated", "suggested less than", "agreement",
         "agreement rather than", "rather than agreement", "it suggested",
         "a calculated distance preserving room to retreat"),
        ("we need speed", "speed is necessary", "yes; but", "but speed without",
         "speed without accountability", "without accountability", "is not progress",
         "only a postponement of crisis"),
        ("the phrase was", "was not spoken", "not uttered", "in the hall",
         "the hall; yet", "yet its echo", "its echo", "changed every later decision"),
        ("I do not intend", "to refute", "your view", "your objection; but",
         "but rather to", "define its scope", "so that", "the claim is not overstated"),
        ("in light of", "the available evidence", "evidence currently available",
         "this remains", "a plausible interpretation", "plausible rather than certain",
         "not a categorical judgment", "not a final verdict"),
    ),
}

# The Chinese advanced batch also split complete clauses into overlapping
# character windows. These glosses name each window's contribution in the
# authored sentence rather than presenting the repeated whole-sentence summary.
ZH_GLOSSES = {
    "C1": (
        ("according to the report", "the report indicates that", "although regional",
         "regional differences", "differences still", "still persist", "persist, while",
         "while implementation"),
        ("even if the evidence", "the evidence is limited", "limited, it should not",
         "it should not", "should not be ignored", "ignored as a result", "that result; nor",
         "nor can it be treated as final"),
        ("critical evaluation", "evaluation of effects", "effects on society", "social change",
         "change calls for", "calls for examining", "examining context", "context and method"),
        ("while respecting your", "respecting your proposal", "the proposal's premise", "on that premise",
         "I would like", "would like to offer", "offer an alternative", "an alternative that accounts for constraints"),
        ("considering the two studies", "the two studies together", "the studies make visible", "this makes clear",
         "contextual differences", "these differences at least", "at least explain", "explain part of the divergence"),
        ("because the data", "the data are incomplete", "incomplete, the committee", "the committee decided",
         "the committee decided to defer", "decided to defer", "defer the decision", "until causality is clearer"),
    ),
    "C2": (
        ("the problem was not only", "not only the decision", "the decision itself", "the decision itself; rather",
         "rather, precisely", "precisely in", "in the way the decision", "the decision was implemented"),
        ("his silence and", "silence, rather than", "rather than indicating", "indicating agreement",
         "agreement, instead", "instead it may", "may imply", "imply a calculated distance"),
        ("speed is indeed necessary", "although necessary", "necessary, but", "but without accountability",
         "without accountability", "accountability, speed", "speed is not", "not progress"),
        ("that phrase was never", "never spoken", "spoken in the meeting hall", "in the hall",
         "spoken aloud; yet", "yet its echo", "its echo", "rewrote later decisions"),
        ("I do not intend", "not intend to reject", "to reject your", "your objection",
         "your objection; rather", "rather, I intend", "intend to clarify", "clarify its scope"),
        ("on the evidence currently available", "the evidence available", "available evidence; this",
         "this is", "a plausible interpretation", "plausible, not definitive", "not a final verdict",
         "a final verdict"),
    ),
}


def expected(path: Path) -> tuple[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    rung = path.stem.rsplit("_", 1)[-1]
    gloss_bank = ZH_GLOSSES if path.stem.startswith("zh_") else GLOSSES
    for unit in data.get("level", {}).get("units", []):
        for lesson in unit.get("lessons", []):
            match = re.search(r"-l([1-6])$", str(lesson.get("id", "")), re.I)
            if not match:
                continue
            glosses = gloss_bank[rung][int(match.group(1)) - 1]
            vocab = lesson.get("vocab", [])
            if len(vocab) != 8:
                raise ValueError(f"{path.name}:{lesson.get('id')}: expected eight authored phrase items")
            for item, gloss in zip(vocab, glosses):
                old = str(item.get("en", ""))
                if PLACEHOLDER.match(old):
                    item["en"] = gloss
                    changed += 1
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n", changed


def main() -> int:
    write = "--write" in sys.argv
    check = "--check" in sys.argv or not write
    stale: list[str] = []
    updated = 0
    for code in LANGS:
        for rung in LEVELS:
            path = ROOT / f"data/courses/phase-1/{code}_{rung}.json"
            old = path.read_text(encoding="utf-8")
            body, changed = expected(path)
            # Only placeholder presence is this tool's contract. Other authors
            # may legitimately extend the same course file (extra blocks,
            # lessons, tests), so do not treat unrelated JSON drift as stale.
            if changed == 0 or old == body:
                continue
            updated += changed
            if check:
                stale.append(f"{path.relative_to(ROOT)}: {changed} placeholder gloss(es)")
            else:
                path.write_text(body, encoding="utf-8")
                print(f"updated {path.relative_to(ROOT)}: {changed} contextual glosses")
    if stale:
        print("\n".join(stale))
        return 1 if check else 2
    print(f"advanced C1/C2 glosses current ({updated} glosses checked in write mode)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
