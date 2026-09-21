#!/usr/bin/env python3
"""Audit course data for publication-breaking templated/filler content.

This is intentionally conservative. Structural completeness (six JSON files)
does not make a language course publishable. The scanner records the authored
levels that survive the public-content checks and updates only publication
fields in data/courses/index.json. It never deletes research data.

Run:
  python3 tools/audit-course-quality.py          # write audit + sync index
  python3 tools/audit-course-quality.py --check  # read-only drift check
"""
from __future__ import annotations

import copy
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/courses/index.json"
OUT = ROOT / "data/quality/course-publication-audit.json"
CEFR = ("A1", "A2", "B1", "B2", "C1", "C2")

# These phrases are visible evidence of templated filler rather than useful
# instruction. They caught phase-3 vocabulary whose "meaning" was merely
# "discourse segment 4", repeated question banks that changed only the exercise
# type, and advanced files generated from sentence fragments.
# Phase 3 was created as a broad expansion batch without the editorial/source
# evidence required for publication. Structural success cannot promote it.
UNREVIEWED_PHASES = {"phase-3"}

# Known files with generated/translated advanced fragments that can evade the
# broad phrase scanner. Keep this explicit and reviewable rather than assuming
# that a well-formed JSON document is instructionally sound.
KNOWN_UNPUBLISHABLE = {
    ("ko", "C1"): "known_synthetic_advanced_content",
    ("ko", "C2"): "known_synthetic_advanced_content",
}

PUBLIC_BUGS = {
    "generic_level_instruction": re.compile(r"\bControl .{0,180}?level-appropriate", re.I | re.S),
    "sentence_fragment_as_definition": re.compile(r"discourse segment(?:\s+\d+)?\s+in", re.I),
    "templated_question_bank": re.compile(r"analyse or produce .{0,240}?model", re.I | re.S),
    "templated_question_bank_fil": re.compile(r"suriin o buuin ang modelo", re.I),
    "placeholder_token": re.compile(
        r"(?:language_word(?:_\d+)?|\bword_\d+\b|\blesson_\d+\b|\broman_\d+\b|translation pending|theme related word)",
        re.I,
    ),
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def lesson_count(data: dict) -> int:
    return sum(
        len(unit.get("lessons") or [])
        for unit in ((data.get("level") or {}).get("units") or [])
        if isinstance(unit, dict)
    )


def test_count(data: dict) -> int:
    obj = (data.get("level") or {}).get("test") or data.get("test") or {}
    return len(obj.get("items") or []) if isinstance(obj, dict) else 0


def locate(course: dict, level: str) -> Path | None:
    phase = course.get("phase") or "phase-1"
    preferred = ROOT / "data/courses" / phase / f"{course['code']}_{level}.json"
    if preferred.exists():
        return preferred
    matches = sorted((ROOT / "data/courses").glob(f"phase-*/{course['code']}_{level}.json"))
    return matches[0] if matches else None


def audit_level(course: dict, level: str) -> dict:
    path = locate(course, level)
    if not path:
        return {"level": level, "state": "NOT_AUTHORED", "file": None, "issues": []}
    try:
        data = load(path)
    except Exception:
        return {
            "level": level,
            "state": "PUBLIC_CONTENT_BUG",
            "file": str(path.relative_to(ROOT)),
            "issues": ["invalid_json"],
        }
    text = json.dumps(data, ensure_ascii=False)
    issues = [name for name, pattern in PUBLIC_BUGS.items() if pattern.search(text)]
    if (course.get("phase") or "phase-1") in UNREVIEWED_PHASES:
        issues.append("unreviewed_expansion_batch")
    explicit_block = KNOWN_UNPUBLISHABLE.get((course["code"], level))
    if explicit_block:
        issues.append(explicit_block)
    if str(data.get("content_status") or "").upper() in {"INCOMPLETE", "RESEARCH_REQUIRED"}:
        issues.append("explicitly_unpublished")
    if data.get("indexable") is False:
        issues.append("explicitly_noindex")
    lessons = lesson_count(data)
    tests = test_count(data)
    if lessons <= 0:
        issues.append("no_lessons")
    if tests <= 0:
        issues.append("no_level_test")
    return {
        "level": level,
        "state": "PUBLIC_CONTENT_BUG" if issues else "PUBLISHABLE_EXISTING",
        "file": str(path.relative_to(ROOT)),
        "lessons": lessons,
        "test_items": tests,
        "issues": sorted(set(issues)),
    }


def build() -> tuple[dict, dict]:
    index = load(INDEX)
    updated = copy.deepcopy(index)
    records = []
    by_code = {c["code"]: c for c in updated.get("courses", [])}
    for original in index.get("courses", []):
        checks = [audit_level(original, level) for level in CEFR]
        publishable = [row["level"] for row in checks if row["state"] == "PUBLISHABLE_EXISTING"]
        target = by_code[original["code"]]
        old_levels = original.get("levels") or {}
        target["levels"] = {
            level: {
                "lessons": next(row["lessons"] for row in checks if row["level"] == level),
                "test_items": next(row["test_items"] for row in checks if row["level"] == level),
                **({"hours": old_levels[level].get("hours")} if level in old_levels and "hours" in old_levels[level] else {}),
                **({"note": old_levels[level].get("note")} if level in old_levels and old_levels[level].get("note") else {}),
            }
            for level in publishable
        }
        target["complete"] = publishable == list(CEFR)
        target["quality_status"] = (
            "PUBLISHABLE_COMPLETE" if target["complete"]
            else "PUBLISHABLE_PARTIAL" if publishable
            else "RESEARCH_REQUIRED"
        )
        blocked = [row for row in checks if row["state"] == "PUBLIC_CONTENT_BUG"]
        if target["complete"]:
            target["complete_reason"] = "CEFR A1–C2 pass structural and public filler checks. Editorial/source review remains required."
        elif publishable:
            target["complete_reason"] = (
                f"Only {', '.join(publishable)} may be public; "
                f"{', '.join(row['level'] for row in blocked) or 'remaining levels'} are blocked or unauthored."
            )
        else:
            target["complete_reason"] = "No CEFR level currently passes the public-content quality gate."
        records.append({
            "code": original["code"],
            "name": original.get("name"),
            "phase": original.get("phase"),
            "publishable_levels": publishable,
            "complete": target["complete"],
            "quality_status": target["quality_status"],
            "levels": checks,
        })

    audit = {
        "schema_version": 1,
        "generated_on": "2026-09-20",
        "method": "Conservative publication gate: blocks the unreviewed phase-3 expansion and known synthetic advanced files, then applies deterministic filler/placeholder, lesson and level-test checks. This does not substitute for native-speaker editorial review.",
        "states": {
            "PUBLISHABLE_EXISTING": "No deterministic blocker found; existing content only, not a claim of independent linguistic verification.",
            "PUBLIC_CONTENT_BUG": "Must remain unpublished/noindex.",
            "NOT_AUTHORED": "No level file exists.",
        },
        "summary": {
            "course_records": len(records),
            "complete": sum(r["complete"] for r in records),
            "partial": sum(r["quality_status"] == "PUBLISHABLE_PARTIAL" for r in records),
            "research_required": sum(r["quality_status"] == "RESEARCH_REQUIRED" for r in records),
            "level_states": dict(sorted(Counter(row["state"] for r in records for row in r["levels"]).items())),
        },
        "courses": records,
    }
    return updated, audit


def canonical_json(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def main() -> int:
    check = "--check" in sys.argv
    updated, audit = build()
    expected_index = canonical_json(updated)
    expected_audit = json.dumps(audit, ensure_ascii=False, indent=2) + "\n"
    stale = []
    if INDEX.read_text(encoding="utf-8") != expected_index:
        stale.append(str(INDEX.relative_to(ROOT)))
    if not OUT.exists() or OUT.read_text(encoding="utf-8") != expected_audit:
        stale.append(str(OUT.relative_to(ROOT)))
    if check:
        if stale:
            print("STALE: " + ", ".join(stale))
            return 1
        print("PASS: course publication audit is current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(expected_index, encoding="utf-8")
    OUT.write_text(expected_audit, encoding="utf-8")
    print(
        "course quality: %d complete, %d partial, %d research-required"
        % (audit["summary"]["complete"], audit["summary"]["partial"], audit["summary"]["research_required"])
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
