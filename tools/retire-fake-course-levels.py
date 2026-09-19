#!/usr/bin/env python3
"""Retire fabricated course-level data. WHY THIS FILE EXISTS (2026-09-19)

The extended-level generator (tools/generate-extended-courses.py, a one-shot
that is no longer part of the build) wrote placeholder content into
data/courses/phase-*: vocabulary like "af_word_1_1", practice like "Practice
question 1 about food", tests like "Test question 1", and — for one whole
batch of A1 files — a Spanish alphabet and number list pasted onto other
languages. That text was shipped to the public level pages.

This tool makes the retirement deterministic and auditable:

  1. scan every data/courses/phase-*/<code>_<LEVEL>.json for fabrication
     signatures (placeholder vocab/romanisation, "Practice question N",
     "Option A N", thin "Q 0 <theme>"/"why" items, …)
  2. a language whose EVERY level file is fabricated is retired: all of its
     level data, its catalogue entry and its generated level pages are
     removed. Its starter page (languages/<code>/index.html) is kept — that
     content is separate and real.
  3. a language with genuine A1–C2 keeps those six levels; the fabricated
     A3/B3/C3/C4/C5 files and their generated pages are removed and the
     catalogue entry is trimmed to the levels that really exist.
  4. the catalogue (data/courses/index.json) is rewritten from disk truth —
     never from its own previous claims — with an audit trail entry.

Run:  python3 tools/retire-fake-course-levels.py [--dry-run]
      python3 tools/retire-fake-course-levels.py --check   (report only)

It is idempotent: on a clean tree it reports zero and changes nothing.
"""
import collections
import json
import os
import re
import shutil
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CATALOGUE = "data/courses/index.json"
REPORT = "data/audit/retire-fake-courses.json"

LEVELS = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "C4", "C5"]

# A file is fabricated if it carries any of these signatures. The first nine
# come from generate-extended-courses.py's template strings; the last five
# catch the thin "Q 0 food / why / A B C D" variant (the npi batch).
FAKE_PATTERNS = [
    ("placeholder vocab/number token", re.compile(r"_(word|num|letter)_[0-9]+_?[0-9]*")),
    ("placeholder romanisation", re.compile(r"\broman_[0-9]+\b")),
    ("synthetic practice text", re.compile(r"Practice question [0-9]+")),
    ("synthetic quiz text", re.compile(r"Quiz [0-9]+:")),
    ("synthetic example text", re.compile(r"Example [0-9]+ in ")),
    ("synthetic dialogue text", re.compile(r"Dialog(?:ue line|ue) [0-9]+ in ")),
    ("synthetic test text", re.compile(r"Test question [0-9]+")),
    ("synthetic option text", re.compile(r"Option [ABCD] [0-9]+")),
    ("synthetic mistake text", re.compile(r"Common mistake [0-9]+")),
    ("synthetic meaning text", re.compile(r"\bmeaning [0-9]+\b")),
    ("synthetic sentence text", re.compile(r"Sentence [0-9]+ about")),
    ("synthetic translation text", re.compile(r"Translation [0-9]+")),
    ("thin generated question", re.compile(r'"q":\s*"Q \d')),
    ("thin generated why", re.compile(r'"why":\s*"why"')),
    ("bare ABCD options", re.compile(r"\[\s*\"A\"\s*,\s*\"B\"\s*,\s*\"C\"\s*,\s*\"D\"\s*\]")),
]


def scan_file(path):
    s = open(path, encoding="utf-8").read()
    hits = [name for name, p in FAKE_PATTERNS if p.search(s)]
    return hits


def main():
    dry = "--dry-run" in sys.argv
    check = "--check" in sys.argv

    index = json.load(open(CATALOGUE, encoding="utf-8"))
    courses = index.get("courses", [])

    per_code = collections.defaultdict(lambda: {"clean": [], "fake": []})
    for c in courses:
        code, phase = c["code"], c.get("phase") or "phase-1"
        for fname in c.get("files", []):
            path = os.path.join("data/courses", phase, fname)
            if not os.path.exists(path):
                continue
            hits = scan_file(path)
            entry = {"file": path, "signatures": hits}
            (per_code[code]["fake"] if hits else per_code[code]["clean"]).append(entry)

    retire, trim, keep = [], [], []
    for code, buckets in per_code.items():
        if buckets["clean"] and not buckets["fake"]:
            keep.append(code)
        elif not buckets["clean"]:
            retire.append(code)
        else:
            trim.append(code)

    print("KEEP (genuine, all levels present): %d" % len(keep))
    print("RETIRE (every level fabricated):    %d" % len(retire), "—", ", ".join(sorted(retire)))
    print("TRIM  (genuine levels + fake ones): %d" % len(trim))

    deleted_files, deleted_pages, trimmed_levels = [], [], []
    new_courses = []

    for c in courses:
        code, phase = c["code"], c.get("phase") or "phase-1"
        buckets = per_code.get(code)
        if buckets is None:  # defensive: entry with no files on disk
            print("problem: %s has no files on disk; dropped" % code)
            continue

        if code in retire:
            for e in buckets["fake"]:
                if os.path.exists(e["file"]):
                    deleted_files.append(e["file"])
                    if not dry:
                        os.remove(e["file"])
            lvdir = os.path.join("languages", code, "level")
            if os.path.isdir(lvdir):
                deleted_pages.append(lvdir)
                if not dry:
                    shutil.rmtree(lvdir)
            print("retire %s: %d data files, level pages %s"
                  % (code, len(buckets["fake"]), "yes" if os.path.isdir(lvdir) else "none"))
            continue

        # keep or trim: the level map is rebuilt from files that survive.
        surviving = {os.path.basename(e["file"]).split("_")[1][:-5] for e in buckets["clean"]}
        levels = {}
        for lv in LEVELS:
            fname = "%s_%s.json" % (code, lv)
            if lv in surviving:
                d = json.load(open(os.path.join("data/courses", phase, fname), encoding="utf-8"))
                n_units = (d.get("level") or {}).get("units") or []
                levels[lv] = {
                    "lessons": sum(len(u.get("lessons", [])) for u in n_units),
                    "test_items": len(((d.get("level") or {}).get("test") or {}).get("items") or []),
                }
        files = ["%s_%s.json" % (code, lv) for lv in LEVELS if lv in levels]

        if code in trim:
            for lv in [lv for lv in LEVELS if lv not in surviving]:
                trimmed_levels.append("%s %s" % (code, lv))
                fname = "%s_%s.json" % (code, lv)
                p = os.path.join("data/courses", phase, fname)
                if os.path.exists(p):
                    deleted_files.append(p)
                    if not dry:
                        os.remove(p)
                page_dir = os.path.join("languages", code, "level", lv.lower())
                if os.path.isdir(page_dir):
                    deleted_pages.append(page_dir)
                    if not dry:
                        shutil.rmtree(page_dir)

        entry = {
            "code": code,
            "name": c.get("name"),
            "native": c.get("native", c.get("name")),
            "phase": phase,
            "levels": levels,
            "files": files,
            "complete": len(levels) >= 6,
        }
        for extra in ("countries", "family", "script"):
            if extra in c:
                entry[extra] = c[extra]
        new_courses.append(entry)

    if not (dry or check):
        with open(CATALOGUE, "w", encoding="utf-8") as f:
            json.dump({
                "format": "course-per-level",
                "levels": ["A1", "A2", "B1", "B2", "C1", "C2"],
                "note": ("Levels that exist on disk. A3/B3/C3/C4/C5 are EkGuru "
                         "Extended Mastery levels and are published only when a "
                         "level's full content has been authored; the retired "
                         "placeholder data (see data/audit/retire-fake-courses.json) "
                         "must never be regenerated."),
                "courses": new_courses,
            }, f, ensure_ascii=False, indent=1)

    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tool": "tools/retire-fake-course-levels.py",
        "mode": "dry-run" if dry else ("check" if check else "apply"),
        "summary": {
            "catalogue_courses_before": len(courses),
            "catalogue_courses_after": len(new_courses),
            "retired_languages": sorted(retire),
            "trimmed_languages": sorted(trim),
            "kept_languages": sorted(keep),
            "data_files_deleted": len(deleted_files),
            "generated_page_dirs_deleted": len(deleted_pages),
            "levels_removed": len(trimmed_levels),
        },
        "retired_languages_detail": {
            code: [e["file"] for e in per_code[code]["fake"]] for code in sorted(retire)
        },
        "trimmed_levels": sorted(trimmed_levels),
        "kept_languages_detail": {
            code: [e["file"] for e in per_code[code]["clean"]] for code in sorted(keep)
        },
        "status": "PASS" if (deleted_files or deleted_pages or not (retire or trim)) else "REVIEW_REQUIRED",
    }
    if not (dry or check):
        os.makedirs("data/audit", exist_ok=True)
        with open(REPORT, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=1)
        print("\nreport: %s" % REPORT)

    print("\nfiles to delete: %d · level page dirs to delete: %d · levels removed: %d"
          % (len(deleted_files), len(deleted_pages), len(trimmed_levels)))
    if dry or check:
        print("(dry run — nothing changed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
