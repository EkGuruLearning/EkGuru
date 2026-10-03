#!/usr/bin/env python3
"""Build per-language flashcard decks from the authored course vocabulary.

PHASE 9 (interactive tools) — Arena command, 2 Oct 2026
--------------------------------------------------------
The course data already carries the raw material: every lesson has a `vocab`
list (target text, romanisation, English, part of speech) and a `flashcards`
marker of "auto:vocab". What was missing is the deck artifact and the surface:
the only flashcards on the site were the ten Hindi toolbox pages, and the
practice engine (js/practice-engine.js) had no card mode.

This tool writes, per language:

    data/flashcards/<code>.json     the deck, for tools, tests and export
    js/flashcards-<code>.js         the same deck as a page-local global,
                                    following the js/course-<code>.js pattern
    data/quality/flashcard-coverage.json   per-language counts and flags

Rules that matter:

  · Cards are copied from authored vocabulary, never invented here. If a
    lesson has no vocab, no card is written — an empty deck is reported, not
    padded.
  · Card ids are stable across rebuilds (language + level + unit + lesson +
    slug of the English gloss) and safe for the journal's SRS store
    ([a-zA-Z0-9_.:-], never a reserved word).
  · A deck is capped at CAP cards — the levels nearest the learner's start
    first — so a page never ships the whole 856-word course. The coverage
    report says how many exist in total, so nothing is hidden.
  · The reported speech tag comes from data/languages/registry.json and is a
    tag, not a promise that a device has that voice.

Run:  python3 tools/build-flashcards.py [--check]
      --check exits 1 when a deck on disk differs (CI/gate use)
"""
import json
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CAP = 300                     # cards shipped per language (PHASE 9 minimum: 200)
LEVEL_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2",
               "A1+", "A2+", "A3", "B1+", "B2+", "B3", "C1+", "C3", "C4", "C5"]

CATEGORY_RULES = [
    ("greetings", r"greet|hello|introduc|salut|привет|courtes"),
    ("numbers", r"number|counting|numer|числ"),
    ("food", r"food|drink|restaurant|meal|kitchen|coffee|tea\b"),
    ("travel", r"travel|airport|hotel|direction|station|ticket|city|trip"),
    ("family", r"family|relative|people|friend"),
    ("time", r"time|day|date|clock|month|week|hour"),
    ("colors", r"color|colour"),
    ("body", r"body|health|doctor|illness|hospital"),
    ("verbs", None),          # by part of speech
    ("adjectives", None),
    ("phrases", None),        # multi-word targets
    ("nouns", None),
    ("other", None),
]

BAD_SLUG = re.compile(r"[^a-z0-9]+")


def esc_js(s):
    return json.dumps(s, ensure_ascii=False)


def slug(s):
    s = BAD_SLUG.sub("-", str(s or "").strip().lower()).strip("-")
    return (s or "card")[:40]


def category(pos, target, title):
    p = (pos or "").lower()
    t = (title or "").lower()
    for name, pattern in CATEGORY_RULES:
        if pattern and re.search(pattern, t):
            return name
    if p in ("greeting", "interjection", "phrase"):
        return "greetings"
    if p in ("number", "numeral", "num"):
        return "numbers"
    if p in ("verb", "verbs"):
        return "verbs"
    if p in ("adj", "adjective", "adj."):
        return "adjectives"
    if " " in str(target or "").strip():
        return "phrases"
    if p in ("noun", "n"):
        return "nouns"
    return "other"


def registry():
    reg = json.load(open("data/languages/registry.json", encoding="utf-8"))
    langs = reg.get("languages") if isinstance(reg, dict) else reg
    return {l["code"]: l for l in (langs or []) if l.get("code")}


def level_index(lv):
    return LEVEL_ORDER.index(lv) if lv in LEVEL_ORDER else 99


def collect(files, reg):
    """One deck per language, from every authored level file."""
    decks = {}
    for path in sorted(files):
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        if "level" not in data or "units" not in data.get("level", {}):
            continue
        code = data.get("code") or os.path.basename(path).split("_")[0]
        info = reg.get(code, {})
        deck = decks.setdefault(code, {
            "code": code,
            "name": data.get("name") or info.get("name") or code,
            "native": data.get("native") or info.get("endonym") or "",
            "speech": info.get("speech_tag") or info.get("bcp47") or code,
            "direction": info.get("direction") or "ltr",
            "scripts": info.get("scripts") or [],
            "cards": [],
            "_seen": set(),
        })
        lv = data.get("file_level") or data.get("level", {}).get("title") or ""
        for unit in data["level"].get("units", []):
            utitle = unit.get("title") or unit.get("id") or ""
            for lesson in unit.get("lessons", []):
                ltitle = lesson.get("title") or ""
                for v in lesson.get("vocab") or []:
                    if not isinstance(v, dict):
                        continue
                    target = (v.get("t") or "").strip()
                    english = (v.get("en") or "").strip()
                    if not target or not english:
                        continue
                    # Dedupe on the target itself, not the English gloss: the
                    # expanded decks reuse a gloss across several targets
                    # ("discourse segment in ..."), and a gloss-only id dropped
                    # real vocabulary. The target is what the learner studies.
                    base = "%s.%s.%s" % (code, slug(lv), slug(target))
                    cid = base[:140]
                    if cid in deck["_seen"]:
                        n = 2
                        while ("%s-%d" % (base, n))[:150] in deck["_seen"]:
                            n += 1
                        cid = ("%s-%d" % (base, n))[:150]
                    if cid in deck["_seen"]:
                        continue
                    deck["_seen"].add(cid)
                    deck["cards"].append({
                        "id": cid,
                        "t": target,
                        "r": (v.get("r") or "").strip(),
                        "en": english,
                        "pos": (v.get("pos") or "").strip(),
                        "cat": category(v.get("pos"), target, utitle + " " + ltitle),
                        "level": lv or "A1",
                        "unit": utitle,
                        "lesson": ltitle,
                    })
    for deck in decks.values():
        deck["cards"].sort(key=lambda c: (level_index(c["level"]), c["unit"], c["lesson"], c["en"]))
        deck["total_available"] = len(deck["cards"])
        deck["cards"] = deck["cards"][:CAP]
        deck.pop("_seen", None)
    return decks


def categories_of(cards):
    out = {}
    for c in cards:
        out[c["cat"]] = out.get(c["cat"], 0) + 1
    return dict(sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))


def payload(deck):
    return {
        "code": deck["code"],
        "name": deck["name"],
        "native": deck["native"],
        "speech": deck["speech"],
        "direction": deck["direction"],
        "total_available": deck["total_available"],
        "categories": categories_of(deck["cards"]),
        "cards": deck["cards"],
    }


def main():
    check = "--check" in sys.argv
    reg = registry()
    files = [p for p in glob.glob("data/courses/phase-*/*.json")
             if not os.path.basename(p).startswith(("index", "build-", "_"))]
    decks = collect(files, reg)
    os.makedirs("data/flashcards", exist_ok=True)

    stale, written, report = [], 0, {}
    for code, deck in sorted(decks.items()):
        p = payload(deck)
        if not p["cards"]:
            continue                      # a language with no authored vocab gets no deck
        blob_js = ("/* Generated from the authored course vocabulary by "
                   "tools/build-flashcards.py — do not hand-edit. */\n"
                   "window.EKGURU_FLASHCARDS_%s=%s;\n" % (code.upper(), esc_js(p)))
        # Compact on purpose: the deck is machine-read by tools and tests, and
        # the pretty-printed form cost three megabytes of repo for no reader.
        blob_json = json.dumps(p, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        js_path = "js/flashcards-%s.js" % code
        json_path = "data/flashcards/%s.json" % code
        for path, blob in ((js_path, blob_js), (json_path, blob_json)):
            old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
            if old != blob:
                if check:
                    stale.append(path)
                else:
                    open(path, "w", encoding="utf-8").write(blob)
                    written += 1
        romanised = sum(1 for c in p["cards"] if c["r"])
        report[code] = {
            "name": p["name"], "speech": p["speech"],
            "cards": len(p["cards"]), "available": p["total_available"],
            "meets_minimum": len(p["cards"]) >= 200,
            "romanisation_percent": round(100.0 * romanised / max(1, len(p["cards"])), 1),
            "categories": p["categories"],
        }

    report_blob = json.dumps({
        "generated_by": "tools/build-flashcards.py",
        "cap": CAP,
        "languages": report,
        "totals": {
            "languages": len(report),
            "cards": sum(r["cards"] for r in report.values()),
            "meeting_minimum": sum(1 for r in report.values() if r["meets_minimum"]),
        },
    }, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    rep_path = "data/quality/flashcard-coverage.json"
    old = open(rep_path, encoding="utf-8").read() if os.path.exists(rep_path) else None
    if old != report_blob:
        if check:
            stale.append(rep_path)
        else:
            open(rep_path, "w", encoding="utf-8").write(report_blob)
            written += 1

    if check and stale:
        print("STALE %d flashcard file(s) — run tools/build-flashcards.py" % len(stale))
        for p in stale[:5]:
            print("   ", p)
        return 1

    total = sum(r["cards"] for r in report.values())
    meet = sum(1 for r in report.values() if r["meets_minimum"])
    print("flashcard decks: %d languages · %d cards · %d meet the 200-card minimum"
          % (len(report), total, meet))
    thin = sorted((c for c, r in report.items() if not r["meets_minimum"]))
    if thin:
        print("below 200 (reported, never padded):", ", ".join(thin))
    if not check:
        print("wrote %d file(s)" % written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
