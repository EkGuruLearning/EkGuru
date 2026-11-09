# -*- coding: utf-8 -*-
"""Hindi B3 ("Advanced") — authored level, merged into its course file.

B3 is the EkGuru bridge between B2 and C1, labelled "Advanced" in the course
index. Until this file existed its course file was an empty stub
(content_status INCOMPLETE, no units). The content lives in three unit files
and one level file under tools/hi-b3-source/ (kept out of tools/lang-data/, which holds the language packs):

    hi-b3-unit1.json   Register and Respect           (3 lessons)
    hi-b3-unit2.json   Linking Ideas                  (3 lessons)
    hi-b3-unit3.json   Telling, Reporting and Arguing (3 lessons)
    hi-b3-level.json   title, goals, test (12 items), extra block

This script validates those files against the T1 schema's minimums and writes
data/courses/phase-2/hi_B3.json. It keeps indexable false: publishing stays a
separate owner decision (the language gate), so authoring does not make the
level public.

Run:  python3 tools/author-hindi-advanced.py           write hi_B3.json
      python3 tools/author-hindi-advanced.py --check   report drift only
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tools" / "hi-b3-source"
COURSE = ROOT / "data" / "courses" / "phase-2" / "hi_B3.json"
UNIT_FILES = ["hi-b3-unit1.json", "hi-b3-unit2.json", "hi-b3-unit3.json"]
LEVEL_FILE = "hi-b3-level.json"

LESSON_KEYS = ["id", "title", "learn", "vocab", "grammar", "dialogue", "practice", "quiz", "worksheet"]


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def validate(units: list[dict], level: dict) -> list[str]:
    problems: list[str] = []
    if not 3 <= len(units) <= 5:
        problems.append(f"units: {len(units)} (schema wants 3-5)")
    for unit in units:
        if not 3 <= len(unit["lessons"]) <= 5:
            problems.append(f"{unit['id']}: {len(unit['lessons'])} lessons (wants 3-5)")
        for lesson in unit["lessons"]:
            missing = [k for k in LESSON_KEYS if k not in lesson]
            if missing:
                problems.append(f"{lesson.get('id')}: missing {missing}")
            if len(lesson.get("practice", [])) < 10:
                problems.append(f"{lesson['id']}: practice {len(lesson.get('practice', []))} (wants 10+)")
            if len(lesson.get("quiz", [])) < 3:
                problems.append(f"{lesson['id']}: quiz < 3")
            if len(lesson.get("dialogue", [])) < 2:
                problems.append(f"{lesson['id']}: dialogue < 2")
            if not lesson.get("grammar", {}).get("examples"):
                problems.append(f"{lesson['id']}: grammar has no examples")
    items = level.get("test", {}).get("items", [])
    if not 10 <= len(items) <= 20:
        problems.append(f"test: {len(items)} items (schema wants 10-20)")
    extra = level.get("extra", {})
    if len(extra.get("idioms", [])) < 10:
        problems.append("extra: idioms < 10")
    if len(extra.get("mistakes", [])) < 3:
        problems.append("extra: mistakes < 3")
    if extra.get("reading", {}).get("original") is not True:
        problems.append("extra: reading must be original: true")
    if not extra.get("listening", {}).get("voice_tag"):
        problems.append("extra: listening voice_tag missing")
    for key in ["culture", "reading", "listening", "idioms", "mistakes", "task"]:
        if key not in extra:
            problems.append(f"extra: {key} missing")
    return problems


def build() -> dict:
    units = [load(name) for name in UNIT_FILES]
    level_src = load(LEVEL_FILE)
    level = {
        "title": level_src["title"],
        "goals": level_src["goals"],
        "units": units,
        "test": level_src["test"],
        "extra": level_src["extra"],
    }
    course = json.loads(COURSE.read_text(encoding="utf-8"))
    course["file_level"] = "B3"
    course["content_status"] = "AUTHORED"
    course["indexable"] = False
    course["reason"] = (
        "EkGuru B2→C1 bridge, labelled Advanced in the course index. Not a CEFR level. "
        "Authored; held unpublished (indexable false) until the owner confirms the language gate."
    )
    course["level"] = level
    return course


def main() -> int:
    check = "--check" in sys.argv
    units = [load(name) for name in UNIT_FILES]
    level = load(LEVEL_FILE)
    problems = validate(units, level)
    if problems:
        for p in problems:
            print("  INVALID:", p)
        return 1
    out_obj = build()
    out = json.dumps(out_obj, ensure_ascii=False, indent=2) + "\n"
    current = COURSE.read_text(encoding="utf-8")
    n_lessons = sum(len(u["lessons"]) for u in units)
    if check:
        if current != out:
            print(f"  hi_B3.json STALE ({n_lessons} lessons not yet written)")
            return 1
        print(f"OK: hi_B3.json current ({len(units)} units, {n_lessons} lessons)")
        return 0
    if current != out:
        COURSE.write_text(out, encoding="utf-8")
        print(f"written: hi_B3.json ({len(units)} units, {n_lessons} lessons, test {len(level['test']['items'])}, idioms {len(level['extra']['idioms'])})")
    else:
        print("already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
