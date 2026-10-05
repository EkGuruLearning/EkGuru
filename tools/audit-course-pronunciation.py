#!/usr/bin/env python3
"""Audit source-verified IPA coverage in the published CEFR course data.

This is an evidence report, not an IPA generator. It reads only levels present
in data/courses/index.json's publication manifest and never derives a
transcription from romanisation or browser speech. A course-level research
basis is not a per-word pronunciation citation.

Run: python3 tools/audit-course-pronunciation.py [--check]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "data/courses/index.json"
OUT = ROOT / "data/quality/course-pronunciation-audit.json"
LEVEL_ORDER = ("A1", "A2", "B1", "B2", "C1", "C2")
SOURCE_KEYS = ("ipa_source", "ipa_source_url", "ipa_reference", "ipa_references")
CATEGORIES = ("vocabulary", "grammar_examples", "dialogue")


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def entries_for(data: dict) -> dict[str, list[dict]]:
    """Collect authored target-language entries without inventing a schema."""
    result = {category: [] for category in CATEGORIES}
    for unit in ((data.get("level") or {}).get("units") or []):
        for lesson in (unit.get("lessons") or []):
            result["vocabulary"].extend(x for x in (lesson.get("vocab") or []) if isinstance(x, dict))
            grammar = lesson.get("grammar") or {}
            result["grammar_examples"].extend(
                x for x in (grammar.get("examples") or []) if isinstance(x, dict)
            )
            result["dialogue"].extend(
                x for x in (lesson.get("dialogue") or []) if isinstance(x, dict)
            )
    extra = (data.get("level") or {}).get("extra") or {}
    result["idioms"] = [x for x in (extra.get("idioms") or []) if isinstance(x, dict)]
    if nonempty((extra.get("reading") or {}).get("text")):
        result["reading"] = [{"t": (extra.get("reading") or {}).get("text"), **(extra.get("reading") or {})}]
    if nonempty((extra.get("listening") or {}).get("script")):
        result["listening"] = [{"t": (extra.get("listening") or {}).get("script"), **(extra.get("listening") or {})}]
    return result


def count_group(items: list[dict]) -> dict[str, int]:
    with_ipa = [item for item in items if nonempty(item.get("ipa"))]
    attributed = [item for item in with_ipa if any(nonempty(item.get(k)) for k in SOURCE_KEYS)]
    return {
        "items": len(items),
        "with_ipa": len(with_ipa),
        "with_ipa_source_reference": len(attributed),
    }


def build_report() -> dict:
    catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    published_courses = []
    totals = {category: {"items": 0, "with_ipa": 0, "with_ipa_source_reference": 0}
              for category in (*CATEGORIES, "idioms", "reading", "listening")}
    missing_sources: list[str] = []
    languages_with_research_file = 0
    language_research_source_records = 0
    published_levels = 0

    for course in catalogue.get("courses", []):
        levels_obj = course.get("levels") or {}
        levels = [level for level in LEVEL_ORDER if level in levels_obj]
        if not levels:
            continue
        phase = course.get("phase") or "phase-1"
        course_row = {
            "code": course.get("code", ""),
            "name": course.get("name", ""),
            "published_levels": levels,
            "language_research_file_present": False,
            "language_research_source_records": 0,
            "categories": {category: {"items": 0, "with_ipa": 0,
                                      "with_ipa_source_reference": 0}
                           for category in totals},
        }
        research_path = ROOT / "data/language-research" / f"{course['code']}.json"
        if research_path.is_file():
            research = json.loads(research_path.read_text(encoding="utf-8"))
            sources = research.get("sources") or []
            course_row["language_research_file_present"] = True
            course_row["language_research_source_records"] = len(sources)
            languages_with_research_file += 1
            language_research_source_records += len(sources)
        course_items = 0
        course_ipa = 0
        for level in levels:
            source = ROOT / "data/courses" / phase / f"{course['code']}_{level}.json"
            if not source.is_file():
                missing_sources.append(source.relative_to(ROOT).as_posix())
                continue
            data = json.loads(source.read_text(encoding="utf-8"))
            published_levels += 1
            groups = entries_for(data)
            for category, items in groups.items():
                counts = count_group(items)
                for key, value in counts.items():
                    course_row["categories"][category][key] += value
                    totals[category][key] += value
                course_items += counts["items"]
                course_ipa += counts["with_ipa"]
        course_row["target_entries"] = course_items
        course_row["target_entries_with_ipa"] = course_ipa
        published_courses.append(course_row)

    vocab = totals["vocabulary"]
    status = "SOURCE_COVERAGE_COMPLETE" if vocab["items"] and \
        vocab["with_ipa"] == vocab["items"] and \
        vocab["with_ipa_source_reference"] == vocab["items"] and \
        not missing_sources else "BLOCKED"
    return {
        "schema_version": 1,
        "generated_by": "tools/audit-course-pronunciation.py",
        "scope": "Levels published by data/courses/index.json; non-published drafts are excluded.",
        "status": status,
        "requirement": "Every published vocabulary item has source-verified IPA.",
        "summary": {
            "published_courses": len(published_courses),
            "published_levels": published_levels,
            "published_vocabulary_items": vocab["items"],
            "vocabulary_items_with_ipa": vocab["with_ipa"],
            "vocabulary_items_with_ipa_source_reference": vocab["with_ipa_source_reference"],
            "vocabulary_ipa_coverage_percent": round(100 * vocab["with_ipa"] / vocab["items"], 2)
            if vocab["items"] else 0,
            "vocabulary_ipa_source_reference_coverage_percent":
                round(100 * vocab["with_ipa_source_reference"] / vocab["items"], 2)
                if vocab["items"] else 0,
            "vocabulary_items_missing_ipa": vocab["items"] - vocab["with_ipa"],
            "vocabulary_items_missing_ipa_source_reference":
                vocab["items"] - vocab["with_ipa_source_reference"],
            "all_target_text": totals,
            "languages_with_language_research_file": languages_with_research_file,
            "general_language_research_source_records": language_research_source_records,
            "missing_published_source_files": missing_sources,
        },
        "policy": {
            "ipa": "Render only an author-supplied transcription. Never derive IPA from romanisation, a browser voice, or an unverified model.",
            "source_evidence": "A language-level research_basis is not a citation for an individual IPA transcription.",
            "review": "Coverage is not linguistic verification; qualified native-speaker or phonetics review remains a separate requirement.",
        },
        "courses": published_courses,
    }


def main() -> int:
    report = json.dumps(build_report(), ensure_ascii=False, indent=2) + "\n"
    check = "--check" in sys.argv
    if check:
        current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""
        if current != report:
            print(f"STALE: {OUT.relative_to(ROOT)} needs tools/audit-course-pronunciation.py")
            return 1
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(report, encoding="utf-8")
    data = json.loads(report)
    summary = data["summary"]
    print("course pronunciation audit: %s — %d/%d published vocabulary items have "
          "source-referenced IPA; %d levels, %d languages"
          % (data["status"], summary["vocabulary_items_with_ipa_source_reference"],
             summary["published_vocabulary_items"], summary["published_levels"],
             summary["published_courses"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
