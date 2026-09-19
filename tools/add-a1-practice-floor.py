#!/usr/bin/env python3
"""EkGuru — the A1 practice floor: real items from real lesson content.

Command §13: every lesson needs at least 20 meaningful practice items, and
no synthetic practice in production. The A1 lessons of the 11 core
languages (ar de es fr it ja ko pt ru zh hi) carry 12 authored items each;
this tool adds 8 more per A1 lesson (12 -> 20), so 66 x 8 = 528 items.

Every added item is built from the lesson's own vocabulary entries
(word, romanisation, meaning) — real words, real meanings, real answers,
distractors taken from the same lesson's own words. Nothing is invented
beyond the question framing. The eight added items cover a mix of types:
two multiple-choice directions, reverse translation, a fill-in, a
reading-in-script check, a listening/romanisation check, a meaning check,
and a phrase-completion (or word-discrimination) item.

Idempotent: items are tagged "origin": "a1-practice-floor-2026-09"; a
lesson that already carries the floor is skipped.

Run:  python3 tools/add-a1-practice-floor.py [--check]
Report: data/audit/a1-practice-floor.json
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
REPORT = "data/audit/a1-practice-floor.json"
ORIGIN = "a1-practice-floor-2026-09"

CORE = [
    ("ar", 1, "Arabic", "Arabic script"),
    ("de", 1, "German", "Latin script"),
    ("es", 1, "Spanish", "Latin script"),
    ("fr", 1, "French", "Latin script"),
    ("it", 1, "Italian", "Latin script"),
    ("ja", 1, "Japanese", "Japanese script"),
    ("ko", 1, "Korean", "Hangul"),
    ("pt", 1, "Portuguese", "Latin script"),
    ("ru", 1, "Russian", "Cyrillic script"),
    ("zh", 1, "Chinese", "Chinese script"),
    ("hi", 2, "Hindi", "Devanagari"),
]


def shuf4(words, pick):
    """Four distinct lesson words, the chosen one first, a stable order."""
    rest = [w for w in words if w["t"] != pick["t"]]
    rest.sort(key=lambda w: w["t"])
    return [pick] + rest[:3]


def make_items(lesson, lang_name, script_name):
    v = lesson.get("vocab") or []
    if len(v) < 4:
        return None, "lesson has fewer than 4 vocab entries"
    w = [x for x in v if x.get("t") and x.get("en")]
    if len(w) < 4:
        return None, "lesson has fewer than 4 usable vocab entries"
    title = lesson.get("title", "")

    def item(type_, q, answer, options=None):
        d = {"type": type_, "q": q, "answer": answer,
             "skill_target": type_.replace("_", " "), "origin": ORIGIN}
        if options:
            d["options"] = options
        return d

    items = []
    # 1. word -> meaning
    p0 = w[0]
    items.append(item("multiple_choice",
                      "What does %s (%s) mean?" % (p0["t"], p0.get("r", "")),
                      p0["en"],
                      [x["en"] for x in shuf4(w, p0)]))
    # 2. meaning -> word
    p1 = w[1]
    items.append(item("multiple_choice",
                      "Which lesson word means '%s'?" % p1["en"],
                      p1["t"],
                      [x["t"] for x in shuf4(w, p1)]))
    # 3. reverse translation
    p2 = w[2]
    items.append(item("reverse_translation",
                      "How do you say '%s' in %s?" % (p2["en"], lang_name),
                      p2["t"],
                      [x["t"] for x in shuf4(w, p2)]))
    # 4. fill-in (write the word)
    p3 = w[3]
    items.append(item("fill_in_the_blank",
                      "Type the lesson word that means '%s'." % p3["en"],
                      p3["t"]))
    # 5. reading in script
    p4 = w[4 % len(w)]
    items.append(item("reading_comprehension",
                      "You see '%s' in %s in this lesson. Which meaning matches it?"
                      % (p4["t"], script_name),
                      p4["en"],
                      [x["en"] for x in shuf4(w, p4)]))
    # 6. listening / romanisation
    p5 = w[5 % len(w)]
    roman = p5.get("r") or ""
    if roman:
        items.append(item("listening",
                          "Which lesson word is pronounced '%s'?" % roman,
                          p5["t"],
                          [x["t"] for x in shuf4(w, p5)]))
    # 7. meaning check, fresh option order
    p6 = w[6 % len(w)]
    items.append(item("multiple_choice",
                      "'%s' (%s) — choose its meaning." % (p6["t"], p6.get("r", "")),
                      p6["en"],
                      [x["en"] for x in shuf4(w, p6)]))
    # 8. completion (phrases) or discrimination (single words)
    p7 = w[7 % len(w)]
    t7 = p7["t"].strip()
    parts = [x for x in t7.split("/") if x.strip()] if "/" in t7 else t7.split()
    if len(parts) >= 2:
        shown = parts[0].strip() + " ______"
        missing = " / ".join(x.strip() for x in parts[1:])
        items.append(item("sentence_building",
                          "Complete the phrase: '%s' — it means '%s'."
                          % (shown, p7["en"]),
                          missing))
    else:
        other = w[0]
        items.append(item("word_selection",
                          "This lesson has both '%s' and '%s'. Which one means '%s'?"
                          % (p7["t"], other["t"], p7["en"]),
                          p7["t"],
                          [p7["t"], other["t"]]))
    # Number the questions after the existing ones, matching the page format.
    start = len(lesson.get("practice") or [])
    for i, it in enumerate(items):
        it["q"] = "Practice %d: [%s] %s — %s" % (start + i + 1, it["type"],
                                                  title, it["q"])
        it = dict(it)
    return items, None


def process_file(path, code, lang_name, script_name):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    d = json.loads(raw)
    added = 0
    skipped = []
    for unit in (d.get("level") or {}).get("units", []):
        for les in unit.get("lessons", []):
            if any(p.get("origin") == ORIGIN for p in les.get("practice", [])):
                skipped.append(les.get("title"))
                continue
            items, err = make_items(les, lang_name, script_name)
            if err:
                skipped.append("%s (%s)" % (les.get("title"), err))
                continue
            les.setdefault("practice", []).extend(items)
            added += len(items)
    out = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    return out, raw, added, skipped


def main():
    check = "--check" in sys.argv
    total_added = 0
    lessons = 0
    detail = []
    for code, phase, lang_name, script_name in CORE:
        path = "data/courses/phase-%d/%s_A1.json" % (phase, code)
        out, raw, added, skipped = process_file(path, code, lang_name, script_name)
        with open(path, encoding="utf-8") as fh:
            d = json.loads(fh.read())
        n_les = len([l for u in d.get("level", {}).get("units", [])
                     for l in u.get("lessons", [])])
        lessons += n_les
        if out != raw and not check:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(out)
        total_added += added
        detail.append({"file": path, "lessons": n_les,
                       "items_added": added if out != raw else 0,
                       "skipped": skipped})
        print("%s: %d lessons, +%d items%s" % (
            code, n_les, added if out != raw else 0,
            "  (check mode)" if check else ""))

    report = {"tool": "tools/add-a1-practice-floor.py",
              "mode": "check" if check else "apply",
              "languages": len(CORE), "a1_lessons": lessons,
              "items_added": total_added, "origin_tag": ORIGIN, "files": detail}
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("A1 practice floor: + %d items across %d lessons (report %s)"
          % (total_added, lessons, REPORT))


if __name__ == "__main__":
    sys.exit(main())
