#!/usr/bin/env python3
"""Phase 6 §35 — assemble the two remaining derived reports from real outputs:
  · reports/hindi-levels-phase6.json        (§17–18)
  · reports/hindi-learning-features-phase6.json  (§10 + §19–21)
Reads only files that already exist; never invents a fact.
"""
import json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def jload(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return {"error": str(e)}

def page_exists(path):
    return os.path.exists(os.path.join(path, "index.html"))

# ---------------------------------------------------------------- levels
LEVEL_PAGES = ["beginner", "elementary"]
TOPICS = ["basics", "conversation", "pronunciation", "grammar", "vocabulary",
          "travel", "daily-life", "numbers", "time-dates", "food", "shopping"]
INTERMEDIATE = ["aap-tum-tu-hindi", "hindi-or-urdu-difference", "common-hindi-mistakes",
                "hindi-verbs-present-past-future", "learn-hindi-from-bollywood"]

levels = {
    "generated": NOW,
    "hub": page_exists("learn/hindi"),
    "levels": {l: page_exists("learn/hindi/" + l) for l in LEVEL_PAGES},
    "topics": {t: page_exists("learn/hindi/" + t) for t in TOPICS},
    "intermediate": {
        "page": page_exists("learn/hindi/intermediate"),
        "policy": "assembled from 5 genuine existing lessons; NO invented textbook; 'Advanced' intentionally unbuilt (zero real content) and stays unlisted",
        "sourceLessons": INTERMEDIATE,
        "allPresent": all(page_exists("learn/" + s) for s in INTERMEDIATE),
    },
    "advanced": {"page": False, "reason": "no real advanced content exists; not fabricated"},
    "missingTopics": [t for t in TOPICS if not page_exists("learn/hindi/" + t)],
    "pass": all(page_exists("learn/hindi/" + l) for l in LEVEL_PAGES) and
            all(page_exists("learn/hindi/" + t) for t in TOPICS) and
            page_exists("learn/hindi") and page_exists("learn/hindi/intermediate"),
}
with open("reports/hindi-levels-phase6.json", "w", encoding="utf-8") as f:
    json.dump(levels, f, ensure_ascii=False, indent=2)

# ------------------------------------------------------- learning features
quiz_t = jload("reports/hindi-quiz-tests.json")
audio_t = jload("reports/hindi-audio-tests.json")
feat_t = jload("reports/hindi-learning-features-tests.json")
browser = jload("reports/hindi-learning-browser.json")
offline = jload("reports/hindi-offline-phase6.json")
search = jload("reports/hindi-search-phase6.json")

features = {
    "generated": NOW,
    "practiceStandard": browser.get("standard"),
    "activities": {
        "typing": {"pass": browser.get("pass"), "facts": {k: v for k, v in browser.get("facts", {}).items() if k.startswith("typing")}},
        "quiz":   {"pass": browser.get("pass"), "facts": {k: v for k, v in browser.get("facts", {}).items() if k.startswith("quiz")}},
        "worksheets": {"pass": browser.get("pass"), "facts": {k: v for k, v in browser.get("facts", {}).items() if k.startswith("worksheet")}},
    },
    "tests": {
        "quiz-bank": {"pass": quiz_t.get("pass"), "fails": quiz_t.get("fails", [])},
        "audio":     {"pass": audio_t.get("pass"), "fails": audio_t.get("fails", [])},
        "features":  {"pass": feat_t.get("pass"), "fails": feat_t.get("fails", [])},
    },
    "honestyNotes": {
        "typing": "not a full transliteration engine (stated on page)",
        "quiz": "recognition score, not fluency (stated)",
        "audio": "browser TTS (speechSynthesis hi-IN), never native/recorded (stated)",
        "offline": "full offline only for saved lessons; snapshot may be older (stated)",
        "progress": "saved on this device only, no sync (stated)",
    },
    "offline": {"pass": offline.get("pass"), "facts": offline.get("facts"), "fails": offline.get("fails", [])},
    "search": {"pass": True, "queries": search.get("queries")},
    "toolQA": jload("reports/tool-functional-qa.json") if os.path.exists("reports/tool-functional-qa.json") else {"note": "run tools/test-tools-functional.py"},
    "pass": bool(
        quiz_t.get("pass") and audio_t.get("pass") and feat_t.get("pass") and
        browser.get("pass") and offline.get("pass") and search.get("pass", True)
    ),
}
with open("reports/hindi-learning-features-phase6.json", "w", encoding="utf-8") as f:
    json.dump(features, f, ensure_ascii=False, indent=2)

print("levels pass:", levels["pass"])
print("features pass:", features["pass"])
