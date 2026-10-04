#!/usr/bin/env python3
"""Reject generated segmentation labels as published vocabulary or flashcards."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(r"contextual segment\s+\d+\s*:", re.IGNORECASE)


def main() -> int:
    publication = json.loads(
        (ROOT / "data/quality/course-publication-audit.json").read_text(encoding="utf-8")
    )
    errors: list[str] = []
    levels_checked = 0

    for course in publication.get("courses", []):
        code = course.get("code", "")
        phase = course.get("phase") or "phase-1"
        for level in course.get("publishable_levels", []):
            source = ROOT / "data/courses" / phase / f"{code}_{level}.json"
            if not source.is_file():
                errors.append(f"{source.relative_to(ROOT)}: published level source is missing")
                continue
            data = json.loads(source.read_text(encoding="utf-8"))
            levels_checked += 1
            for unit in (data.get("level") or {}).get("units", []):
                for lesson in unit.get("lessons", []):
                    for item in lesson.get("vocab", []):
                        if isinstance(item, dict) and PLACEHOLDER.match(str(item.get("en", "")).strip()):
                            errors.append(
                                f"{source.relative_to(ROOT)} · {lesson.get('title', 'lesson')}: "
                                f"placeholder gloss for {item.get('t', '[empty target]')}"
                            )

            page = ROOT / "languages" / code / "level" / level.lower() / "index.html"
            if not page.is_file():
                errors.append(f"{page.relative_to(ROOT)}: published level page is missing")
            elif PLACEHOLDER.search(page.read_text(encoding="utf-8")):
                errors.append(f"{page.relative_to(ROOT)}: generated segmentation label is public")

    decks_checked = 0
    for deck_path in sorted((ROOT / "data/flashcards").glob("*.json")):
        deck = json.loads(deck_path.read_text(encoding="utf-8"))
        decks_checked += 1
        for card in deck.get("cards", []):
            if PLACEHOLDER.match(str(card.get("en", "")).strip()):
                errors.append(
                    f"{deck_path.relative_to(ROOT)} · {card.get('id', 'card')}: placeholder gloss"
                )

    if errors:
        for error in errors[:40]:
            print("FAIL", error)
        if len(errors) > 40:
            print(f"… {len(errors) - 40} more")
        return 1
    print(
        f"PASS: no generated contextual-segment glosses in {levels_checked} "
        f"published level sources/pages or {decks_checked} flashcard decks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
