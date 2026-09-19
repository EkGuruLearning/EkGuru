#!/usr/bin/env python3
"""Replace placeholder extra-level (and unpublished-language) JSON.

Writes either:
  · content_status=REAL extra levels from tools/lib/extended_banks.py
  · content_status=INCOMPLETE stubs with empty units (never placeholder tokens)

Never invents {code}_word_n_i. Never marks a language complete without units.
Alias codes in data/global/language-code-map.json are not new courses.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from tools.lib.placeholders import (  # noqa: E402
    ALL_LEVELS,
    CEFR_LEVELS,
    EXTRA_LEVELS,
    content_status,
    is_placeholder,
    placeholder_hits,
    walk_course_json,
)
from tools.lib.extended_banks import load_all_packs  # noqa: E402

CATALOGUE = "data/courses/index.json"
ALIAS_MAP = "data/global/language-code-map.json"
STATUS_OUT = "data/quality/course-repair-status.json"

EXTENSION_NOTE = {
    "A3": "EkGuru A2→B1 bridge. Not a CEFR level.",
    "B3": "EkGuru B2→C1 bridge. Not a CEFR level.",
    "C3": "EkGuru post-C2 extension. Not a CEFR level. Unpublished until authored.",
    "C4": "EkGuru post-C2 extension. Not a CEFR level. Unpublished until authored.",
    "C5": "EkGuru post-C2 extension. Not a CEFR level. Unpublished until authored.",
}


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def dump(path, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def distractors(vocab, keep_en, n=3):
    out = []
    for w in vocab:
        en = (w.get("en") or "").strip()
        if en and en != keep_en and en not in out:
            out.append(en)
        if len(out) >= n:
            break
    return out


def practice_from(lesson, name):
    vocab = lesson.get("vocab") or []
    gram = lesson.get("grammar") or {}
    dlg = lesson.get("dialogue") or []
    items = []
    for w in vocab:
        en = w.get("en") or ""
        t = w.get("t") or ""
        if not t or not en:
            continue
        opts = [en] + distractors(vocab, en)
        if len(opts) < 2:
            continue
        items.append({
            "type": "multiple_choice",
            "q": "What does “%s” mean?" % t,
            "options": opts[:4],
            "answer": en,
            "why": "“%s” means “%s”." % (t, en),
            "skill_target": "vocabulary recognition",
        })
        items.append({
            "type": "translate_t",
            "q": "How do you say “%s” in %s?" % (en, name),
            "answer": t,
            "why": "The course word for “%s” is “%s”." % (en, t),
            "skill_target": "vocabulary production",
        })
    examples = gram.get("examples") or []
    if examples:
        ex = examples[0]
        items.append({
            "type": "error_correction",
            "q": "Which sentence matches this pattern: %s" % (gram.get("pattern") or gram.get("title") or ""),
            "options": [ex.get("t")] + [e.get("t") for e in examples[1:4] if e.get("t") != ex.get("t")],
            "answer": ex.get("t"),
            "why": gram.get("explain") or "",
            "skill_target": "grammar recognition",
        })
    if dlg:
        line = dlg[0]
        items.append({
            "type": "dialogue_completion",
            "q": "Who says: “%s”" % (line.get("t") or ""),
            "options": [line.get("sp")] + [x.get("sp") for x in dlg[1:] if x.get("sp") != line.get("sp")],
            "answer": line.get("sp"),
            "why": "%s says this line." % (line.get("sp") or "The speaker"),
            "skill_target": "listening/dialogue",
        })
    # Cap at 12; never pad with invented questions.
    return items[:12]


def quiz_from(lesson):
    items = []
    for w in (lesson.get("vocab") or [])[:5]:
        if not w.get("t") or not w.get("en"):
            continue
        items.append({
            "q": "“%s” means:" % w["t"],
            "options": [w["en"]] + distractors(lesson.get("vocab") or [], w["en"]),
            "answer": 0,
            "why": "“%s” = “%s”." % (w["t"], w["en"]),
        })
    return items[:5]


def worksheet_from(lesson, name):
    vocab = [w for w in (lesson.get("vocab") or []) if w.get("t") and w.get("en")]
    if len(vocab) < 3:
        return {}
    return {
        "title": "Write the %s word" % name,
        "tasks": [{
            "instruction": "Write the word that matches each English gloss. Use this lesson’s list, nothing else.",
            "items": [w["en"] for w in vocab[:6]],
            "key": [w["t"] for w in vocab[:6]],
        }],
    }


def test_from(lessons, name, level):
    items = []
    for les in lessons:
        for w in (les.get("vocab") or [])[:2]:
            if not w.get("t") or not w.get("en"):
                continue
            items.append({
                "type": "multiple_choice",
                "q": "What does “%s” mean?" % w["t"],
                "options": [w["en"]] + distractors(les.get("vocab") or [], w["en"]),
                "answer": w["en"],
                "why": "From this %s lesson: “%s” means “%s”." % (level, w["t"], w["en"]),
            })
        if len(items) >= 10:
            break
    return {"title": "%s test" % level, "items": items[:10]}


def goals_from(lessons, name, level):
    out = []
    for les in lessons:
        title = (les.get("title") or "").strip()
        if title:
            out.append("Handle a short %s exchange about %s." % (name, title.lower()))
    if not out:
        out = ["Use authored %s %s vocabulary in short exchanges." % (name, level)]
    return out[:8]


def real_course(meta, level, lessons, name):
    packed = []
    for les in lessons:
        row = dict(les)
        row["practice"] = practice_from(les, name)
        row["quiz"] = quiz_from(les)
        row["worksheet"] = worksheet_from(les, name)
        row["srs_candidates"] = [w.get("t") for w in (les.get("vocab") or []) if w.get("t")][:8]
        packed.append(row)
    mid = max(1, len(packed) // 2)
    units = [
        {"id": "Unit 1", "title": "%s %s — first half" % (name, level), "lessons": packed[:mid]},
        {"id": "Unit 2", "title": "%s %s — second half" % (name, level), "lessons": packed[mid:]},
    ]
    return {
        "code": meta["code"],
        "name": name,
        "native": meta.get("native") or name,
        "phase": meta.get("phase"),
        "medium": "en",
        "file_level": level,
        "content_status": "REAL",
        "indexable": True,
        "ekguru_extension": level in EXTRA_LEVELS,
        "cefr_equivalent": None if level in EXTRA_LEVELS else level,
        "cefr_note": EXTENSION_NOTE.get(level, ""),
        "level": {
            "id": level,
            "title": "%s %s" % (name, level),
            "goals": goals_from(packed, name, level),
            "units": units,
            "test": test_from(packed, name, level),
        },
    }


def incomplete_course(meta, level, reason):
    name = meta.get("name") or meta.get("code")
    return {
        "code": meta["code"],
        "name": name,
        "native": meta.get("native") or name,
        "phase": meta.get("phase"),
        "medium": "en",
        "file_level": level,
        "content_status": "INCOMPLETE",
        "indexable": False,
        "ekguru_extension": level in EXTRA_LEVELS,
        "cefr_equivalent": None if level in EXTRA_LEVELS else level,
        "cefr_note": EXTENSION_NOTE.get(level, ""),
        "reason": reason,
        "level": {
            "id": level,
            "title": "%s %s — not published" % (name, level),
            "goals": [],
            "units": [],
        },
    }


def course_path(phase, code, level):
    return "data/courses/%s/%s_%s.json" % (phase, code, level)


def rewrite_index(courses, packs):
    cat = load(CATALOGUE, {}) or {}
    for c in courses:
        code = c["code"]
        phase = c.get("phase") or "phase-1"
        published = []
        extra_published = []
        for lv in list(CEFR_LEVELS) + list(EXTRA_LEVELS):
            path = course_path(phase, code, lv)
            data = load(path)
            st = content_status(data) if data else "INCOMPLETE"
            if st == "REAL" and not is_placeholder(data):
                published.append(lv)
                if lv in EXTRA_LEVELS:
                    extra_published.append(lv)
        # Catalogue levels: CEFR if REAL, plus authored extras only.
        level_map = {}
        old_levels = c.get("levels") or {}
        for lv in published:
            path = course_path(phase, code, lv)
            data = load(path) or {}
            lessons = [l for u in ((data.get("level") or {}).get("units") or [])
                       for l in (u.get("lessons") or [])]
            test_n = len((((data.get("level") or {}).get("test") or {}).get("items") or []))
            level_map[lv] = {
                "lessons": len(lessons),
                "test_items": test_n,
                "hours": None,
                "note": EXTENSION_NOTE.get(lv, "CEFR " + lv if lv in CEFR_LEVELS else ""),
            }
        c["levels"] = level_map
        cefr_ok = all(lv in published for lv in CEFR_LEVELS)
        c["complete"] = bool(cefr_ok)
        c["extra_levels_published"] = extra_published
        if not cefr_ok:
            c["complete_reason"] = "CEFR A1–C2 not fully authored; unpublished levels are INCOMPLETE stubs."
        elif extra_published:
            c["complete_reason"] = "CEFR A1–C2 authored. Extra tracks published: %s." % ", ".join(extra_published)
        else:
            c["complete_reason"] = "CEFR A1–C2 authored. Extra tracks A3/B3/C3–C5 unpublished."
    cat["courses"] = courses
    cat["levels"] = list(CEFR_LEVELS)
    cat["extension_tracks"] = list(EXTRA_LEVELS)
    cat["updated"] = "2026-09-19"
    cat["note"] = (
        "complete=true means CEFR A1–C2 are authored. "
        "A3/B3/C3/C4/C5 are EkGuru extension tracks, listed in levels only when REAL."
    )
    dump(CATALOGUE, cat)
    return cat


def scan(fail=False):
    hits = []
    for path in walk_course_json("data/courses"):
        if path.endswith("/index.json") or "/authored/" in path:
            continue
        raw = open(path, encoding="utf-8").read()
        found = placeholder_hits(raw)
        if found:
            hits.append((path, found[:3]))
    print("placeholder scan: %d file(s)" % len(hits))
    for path, found in hits[:20]:
        print("  %s  %s" % (path, found))
    if fail and hits:
        return 1
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--scan" in argv:
        return scan(fail="--fail" in argv)

    packs = load_all_packs()
    cat = load(CATALOGUE, {}) or {}
    courses = cat.get("courses") or []
    aliases = load(ALIAS_MAP, {}) or {}
    blocked = set(aliases.get("blocked_new_course_codes") or [])

    wrote_real, wrote_stub, skipped, blocked_hit = 0, 0, 0, []
    reasons = {}

    for c in courses:
        code = c["code"]
        if code in blocked:
            blocked_hit.append(code)
        phase = c.get("phase") or "phase-1"
        name = c.get("name") or code
        complete_flag = bool(c.get("complete"))
        meta = {"code": code, "name": name, "native": c.get("native") or name, "phase": phase}

        for lv in ALL_LEVELS:
            path = course_path(phase, code, lv)
            existing = load(path) if os.path.exists(path) else None
            st = content_status(existing) if existing else "MISSING"

            # Never overwrite authored CEFR of a complete course.
            if lv in CEFR_LEVELS and complete_flag and st == "REAL":
                skipped += 1
                continue

            pack = (packs.get(code) or {}).get(lv)
            if pack:
                dump(path, real_course(meta, lv, pack, name))
                wrote_real += 1
                continue

            if lv in EXTRA_LEVELS or st in ("PLACEHOLDER", "MISSING", "INCOMPLETE"):
                if lv in CEFR_LEVELS and complete_flag and st == "REAL":
                    skipped += 1
                    continue
                why = EXTENSION_NOTE.get(lv) or (
                    "No authored bank; refusing to publish placeholder lessons."
                )
                if lv in CEFR_LEVELS and not complete_flag:
                    why = "Catalogue marks this language incomplete; A1–C2 were placeholder and are unpublished."
                dump(path, incomplete_course(meta, lv, why))
                wrote_stub += 1
                reasons.setdefault(code, []).append(lv)
            else:
                skipped += 1

    rewrite_index(courses, packs)

    report = {
        "updated": "2026-09-19",
        "wrote_real": wrote_real,
        "wrote_incomplete_stubs": wrote_stub,
        "skipped_existing_real": skipped,
        "blocked_alias_codes_in_catalogue": blocked_hit,
        "authored_pack_codes": sorted(packs.keys()),
        "authored_pack_levels": {k: sorted(v.keys()) for k, v in packs.items()},
        "stubbed_levels_by_code": reasons,
        "note": (
            "REAL extra levels come only from tools/lib/extended_banks.py. "
            "C3–C5 are unpublished unless a pack exists. "
            "Placeholder generator tools/generate-extended-courses.py now refuses to write."
        ),
        "npi_note": (
            "Nepali catalogue code is npi (aliases ne, nep). Phase-11 npi was placeholder; "
            "it is INCOMPLETE until an authored bank exists. Do not emit /languages/ne/."
        ),
        "kannada_note": "Kannada course code remains kn. Do not invent a second Kannada course.",
    }
    dump(STATUS_OUT, report)
    print("repair: real=%d stub=%d skipped=%d packs=%s" % (
        wrote_real, wrote_stub, skipped, ",".join(sorted(packs.keys()))))
    print("status: %s" % STATUS_OUT)
    return scan(fail="--fail" in argv)


if __name__ == "__main__":
    sys.exit(main())
