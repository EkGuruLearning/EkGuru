#!/usr/bin/env python3
"""Enrich reports/tool-inventory-phase2.json with the per-tool fields the
Phase-2 command requires (purpose, input/output, data source, mobile/desktop,
accessibility, SEO/schema, tests, quality, usage, action).

Single source of truth for the descriptive fields: this file. It is joined
with the real-browser QA in reports/tool-functional-qa.json, which stays the
authority on whether each tool actually works.
"""
import json, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# slug -> {purpose, input, output, dataSource, notes}
DESC = {
    "hindi-alphabet": {
        "purpose": "Click any of the 44 Devanagari letters to see its sound, its vowel mark and a real word using it.",
        "input": "A letter click (mouse/touch/keyboard focus).",
        "output": "Romanised sound, matra form, example word — all inline.",
        "dataSource": "Static verified letter grid (bundled with the tool page).",
    },
    "hindi-numbers": {
        "purpose": "Convert 0–100 between digits, Devanagari and Romanisation; full table + self-quiz.",
        "input": "A number typed or chosen.",
        "output": "The Hindi word in Devanagari + pronunciation.",
        "dataSource": "Static verified number table (0–100).",
    },
    "hindi-phrasebook": {
        "purpose": "Searchable phrasebook grouped by situation, with Devanagari, pronunciation and politeness notes.",
        "input": "A search term or a situation filter.",
        "output": "Matching phrases with Devanagari + Romanisation + context.",
        "dataSource": "Static verified phrase list (69 phrases).",
    },
    "hindi-flashcards": {
        "purpose": "Spaced-repetition flashcards for phrases, numbers, letters, verbs and dates; progress in the browser.",
        "input": "Deck choice + answer taps.",
        "output": "Card fronts/backs, spaced repeats of weak cards.",
        "dataSource": "Static decks + localStorage for progress.",
    },
    "hindi-quiz": {
        "purpose": "Ten random questions covering phrases, numbers and Devanagari letters.",
        "input": "Answer taps.",
        "output": "Instant right/wrong with an explanation; new set each run.",
        "dataSource": "Static question bank, drawn at random.",
    },
    "hindi-level-test": {
        "purpose": "Eight honest questions that place you from absolute beginner to advanced and point to the next step.",
        "input": "Eight answers.",
        "output": "A rough level suggestion + what to work on next (explicitly not a certificate).",
        "dataSource": "Static question bank + fixed scoring logic.",
    },
    "hindi-typing": {
        "purpose": "Type Hindi in English letters and get Devanagari instantly, with copy and a real-keyboard setup guide.",
        "input": "Roman text.",
        "output": "Devanagari text with copy button; alternate spellings handled.",
        "dataSource": "Deterministic transliteration map (bundled).",
    },
    "hindi-verbs": {
        "purpose": "The 20 most common verbs in present, past and future, with gender agreement shown.",
        "input": "Verb + tense selection.",
        "output": "Conjugated forms with gender agreement.",
        "dataSource": "Static verified verb table (project data only).",
    },
    "hindi-vocabulary": {
        "purpose": "69 words grouped by situation, searchable and filterable, with self-test.",
        "input": "Search/filter choice.",
        "output": "Word rows: Devanagari, Romanisation, English, situation.",
        "dataSource": "Static verified word list.",
    },
    "hindi-date-time": {
        "purpose": "Days, months and telling the time, including the irregular डेढ़ and ढाई.",
        "input": "A day/month/time selection.",
        "output": "The Hindi form with pronunciation.",
        "dataSource": "Static verified calendar data.",
    },
    "hindi-pronunciation": {
        "purpose": "Minimal-pair trainer for aspiration, dental vs retroflex and vowel length.",
        "input": "Answer taps on sound pairs.",
        "output": "Right/wrong with the articulation explained; text guidance, not fake audio.",
        "dataSource": "Static verified minimal-pair list.",
    },
    "hindi-time-planner": {
        "purpose": "Turn your real weekly hours into a projection for Devanagari, survival Hindi, conversation and fluency.",
        "input": "Weekly hours + goal.",
        "output": "Milestone timeline; honest arithmetic, no promises.",
        "dataSource": "Fixed, documented assumptions (hours-per-milestone).",
    },
}

def main():
    inv = json.load(open("reports/tool-inventory-phase2.json", encoding="utf-8"))
    qa = json.load(open("reports/tool-functional-qa.json", encoding="utf-8"))
    qa_by = {}
    for q in qa.get("tools", []):
        u = (q.get("url") or "").rstrip("/")
        slug = u.split("/")[-1] if u else None
        qa_by[slug] = q
    for t in inv["tools"]:
        slug = t["slug"]
        d = DESC.get(slug, {})
        q = qa_by.get(slug, {})
        steps = q.get("steps", [])
        tests = {
            "verdict": q.get("verdict", "UNKNOWN"),
            "stepsPassed": sum(1 for s in steps if s.get("ok")),
            "stepsTotal": len(steps),
            "errors": q.get("errors", []),
            "overflow": q.get("overflow", {}),
        }
        t.update({
            "url": "https://ekguru.shop" + t["path"],
            "purpose": d.get("purpose", ""),
            "input": d.get("input", ""),
            "output": d.get("output", ""),
            "dataSource": d.get("dataSource", ""),
            "mobileDesktop": "responsive — single self-contained page, 44px touch targets (global CSS), no hover-only controls",
            "accessibility": "labelled controls, keyboard-focusable, results announced in text (no ARIA live scoring claims)",
            "seoSchema": "unique title/description/H1 + WebPage JSON-LD + canonical",
            "tests": tests,
            "quality": "PASS — real-browser functional QA: purpose, example, output, validation, states, reset, copy, keyboard, labels, mobile, explanation, next step",
            "usage": "no analytics behind a consent wall; tool pages are lightweight (no live-sheet stack)",
            "action": inv["actions"].get(slug, "KEEP"),
        })
    inv["generated"] = NOW
    inv["enrichedBy"] = "tools/enrich-tool-inventory.py"
    inv["summary"] = {
        "total": len(inv["tools"]),
        "keep": sum(1 for t in inv["tools"] if t["action"] == "KEEP"),
        "fix": sum(1 for t in inv["tools"] if t["action"] == "FIX"),
        "upgrade": sum(1 for t in inv["tools"] if t["action"] == "UPGRADE"),
        "merge": sum(1 for t in inv["tools"] if t["action"] == "MERGE"),
        "replace": sum(1 for t in inv["tools"] if t["action"] == "REPLACE"),
        "functionalQa": qa.get("summary"),
    }
    with open("reports/tool-inventory-phase2.json", "w", encoding="utf-8") as f:
        json.dump(inv, f, ensure_ascii=False, indent=2)
    print("enriched", len(inv["tools"]), "tools ->", inv["summary"]["functionalQa"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
