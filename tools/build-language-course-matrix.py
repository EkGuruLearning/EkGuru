#!/usr/bin/env python3
"""EkGuru — language/course matrix (master audit §7).

Joins the canonical registries with what is actually published:

  data/global/languages.json                      700-entry registry
  data/global/language-support-readiness.json     733 readiness records
  data/global/language-priority.json              700 priority records
  data/global/language-country-relations.json     1,983 relations
  data/courses/index.json                         89 course entries
  languages/<code>/…, learn/<slug>/… on disk        published surfaces
  sitemap-*.xml                                    sitemap membership

Writes data/quality/language-course-matrix.json with one record per
language that has any course surface, plus the full-registry status
counts used by reports/EKGURU-GLOBAL-LANGUAGE-STATUS.md.

Run: python3 tools/build-language-course-matrix.py
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT = "data/quality/language-course-matrix.json"
CEFR = ["A1", "A2", "B1", "B2", "C1", "C2"]
EXT = ["A3", "B3", "C3", "C4", "C5"]


def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as fh:
        return json.load(fh)


def count_ids(lst, key):
    return {x.get(key): x for x in lst}


def page_state(code):
    """What exists on disk for languages/<code>/: course page, level pages,
    robots of the level ladder, and whether any of it is in a sitemap."""
    base = os.path.join(ROOT, "languages", code)
    state = {"course_dir": False, "level_pages": [], "noindex": True,
             "course_page": False, "in_sitemap": False}
    if not os.path.isdir(base):
        return state
    state["course_dir"] = True
    state["course_page"] = os.path.exists(os.path.join(base, "course", "index.html"))
    for lvl in ["a1", "a2", "b1", "b2", "c1", "c2", "a3", "b3", "c3", "c4", "c5"]:
        p = os.path.join(base, "level", lvl, "index.html")
        if os.path.exists(p):
            src = open(p, encoding="utf-8", errors="ignore").read()
            state["level_pages"].append(lvl.upper())
            if "noindex" not in src.lower():
                state["noindex"] = False
    return state


def main():
    langs = load("data/global/languages.json")["languages"]
    readiness = count_ids(load("data/global/language-support-readiness.json")["readiness"], "language_id")
    readiness_all = load("data/global/language-support-readiness.json")["readiness"]
    priority = count_ids(load("data/global/language-priority.json")["priorities"], "language_id")
    relations = load("data/global/language-country-relations.json")["relations"]
    courses = load("data/courses/index.json")["courses"]
    code_map = load("data/global/language-code-map.json")["canonical_course_codes"]

    # join a course code to its registry entry via the canonical code map
    def registry_for(c):
        code, iso3c = c["code"], c.get("iso_639_3") or ""
        cm = code_map.get(code) or {}
        iso3 = cm.get("iso_639_3") or iso3c
        cands = {"lang:" + iso3} if iso3 else set()
        cands |= {"lang:" + a for a in (cm.get("aliases") or [])}
        hits = [l for l in langs if l.get("language_id") in cands]
        if hits:
            # prefer CANONICAL_LANGUAGE over MACROLANGUAGE cluster entries
            canon = [h for h in hits if h.get("language_type") == "CANONICAL_LANGUAGE"]
            return canon[0] if canon else hits[0]
        return next((l for l in langs if l.get("iso_639_1") == code), {})

    rel_by_lang = {}
    for r in relations:
        rel_by_lang.setdefault(r["language_id"], []).append(r)

    # sitemap membership for language URLs
    sm = set()
    for f in os.listdir(ROOT):
        if f.startswith("sitemap") and f.endswith(".xml"):
            for u in re.findall(r"<loc>(https://ekguru\.shop/[^<]*)</loc>",
                                open(f, encoding="utf-8", errors="ignore").read()):
                sm.add(u)

    # measurable content counts from course files
    def course_counts(code):
        total = {"lesson_count": 0, "word_count": 0, "dialogue_line_count": 0,
                 "question_count": 0, "test_items": 0}
        for dirpath, _dirs, files in os.walk(os.path.join(ROOT, "data", "courses")):
            for fn in files:
                if not fn.startswith(code + "_") or not fn.endswith(".json"):
                    continue
                try:
                    d = json.load(open(os.path.join(dirpath, fn), encoding="utf-8"))
                except Exception:
                    continue
                lv = d.get("level") or {}
                for u in (lv.get("units") or []):
                    lessons = u.get("lessons") or []
                    total["lesson_count"] += len(lessons)
                    for le in lessons:
                        total["word_count"] += len(le.get("vocab") or le.get("vocabulary") or le.get("words") or [])
                        dlg = le.get("dialogue") or []
                        total["dialogue_line_count"] += len(dlg.get("lines") if isinstance(dlg, dict) else dlg)
                        total["question_count"] += len(le.get("practice") or []) + len(le.get("quiz") or [])
                t = lv.get("test") or {}
                total["test_items"] += len(t.get("items") or (t if isinstance(t, list) else []))
        return total

    rows = []
    for c in courses:
        code = c["code"]
        lang = registry_for(c)
        lid = lang.get("language_id") or c.get("language_id") or ("lang:" + code)
        cm = code_map.get(code) or {}
        rd = (readiness.get(lid) or {})
        pr = (priority.get(lid) or {})
        rels = rel_by_lang.get(lid, [])
        state = page_state(code)
        levels = c.get("levels", {})
        counts = course_counts(code)
        rows.append({
            "code": code,
            "language_id": lid,
            "name": c.get("name") or cm.get("name") or lang.get("canonical_name"),
            "native_name": lang.get("native_name") or c.get("native"),
            "aliases": sorted(set(cm.get("aliases") or []) | set(lang.get("aliases") or [])),
            "iso_639_1": cm.get("iso_639_1") or lang.get("iso_639_1"),
            "iso_639_3": cm.get("iso_639_3") or lang.get("iso_639_3"),
            "bcp47": lang.get("iso_639_1") or (lang.get("iso_639_3") or code),
            "script": lang.get("script"),
            "writing_system": lang.get("script"),
            "language_family": lang.get("language_family"),
            "countries": sorted({r.get("country_id") for r in rels if r.get("country_id")}),
            "country_count": len({r.get("country_id") for r in rels if r.get("country_id")}),
            "readiness": rd.get("readiness"),
            "priority": pr.get("priority"),
            "priority_score": pr.get("score"),
            "course_exists": bool(c.get("levels")) or state["course_dir"],
            "complete": bool(c.get("complete")),
            "levels": {lv: bool((levels or {}).get(lv)) for lv in CEFR + EXT},
            "levels_on_disk": state["level_pages"],
            "public_indexable": not state["noindex"] and state["course_dir"],
            "noindex": state["noindex"],
            "in_sitemap": any(u.startswith("https://ekguru.shop/languages/" + code + "/") for u in sm),
            "lesson_count": counts["lesson_count"],
            "vocabulary_count": counts["word_count"],
            "dialogue_line_count": counts["dialogue_line_count"],
            "question_count": counts["question_count"],
            "test_items": counts["test_items"],
            "phase": c.get("phase"),
            "quality_status": "COMPLETE" if c.get("complete") else ("PUBLISHED_PARTIAL" if c.get("levels") else "NOT_PUBLISHED"),
        })

    # registry-wide status counts
    from collections import Counter
    rd_dist = Counter(r.get("readiness", "NO_RECORD") for r in readiness_all)
    pri_dist = Counter((priority.get(l["language_id"]) or {}).get("priority", "NO_RECORD")
                       for l in langs)
    dup_native = Counter((l.get("canonical_name") or "").lower() for l in langs)
    duplicates = {k: v for k, v in dup_native.items() if v > 1 and k}
    alias_count = sum(len(l.get("aliases") or []) for l in langs)

    out = {
        "schema_version": 1,
        "generated_note": "Language/course matrix joining the canonical registries with published surfaces. Deterministic; no network.",
        "registry": {
            "total_languages": len(langs),
            "readiness_distribution": dict(rd_dist),
            "priority_distribution": dict(pri_dist),
            "duplicate_canonical_names": duplicates,
            "alias_total": alias_count,
            "relation_count": len(relations),
        },
        "course_languages": len(rows),
        "courses": sorted(rows, key=lambda r: (r["name"] or "")),
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("registry=%d courses=%d complete=%d" % (
        len(langs), len(rows), sum(1 for r in rows if r["complete"])))
    print("readiness:", dict(rd_dist))
    print("wrote", OUT)


if __name__ == "__main__":
    sys.exit(main())
