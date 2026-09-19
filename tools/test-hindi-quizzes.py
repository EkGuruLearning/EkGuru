#!/usr/bin/env python3
"""Phase 6 §29 — validate the Hindi quiz bank + injected lesson quizzes.

Checks (no duplicate framework — reuses the bank parser):
  · data schema (id/lesson/q/a/opts/explain/topic/level/type)
  · answer validity (exactly one correct option, a ∈ opts, 4 options)
  · duplicate question IDs and near-duplicate question text
  · 15/15 lesson coverage
  · accessibility (native <details>/<summary> in every lesson)
  · no "native/recorded/AI" claims in quiz content
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BANK = "js/hindi-quiz-bank.js"
LESSONS = ["hindi-alphabet-for-beginners", "how-to-say-hello-in-hindi", "hindi-sentence-structure",
           "aap-tum-tu-hindi", "common-hindi-mistakes", "hindi-days-months-time",
           "hindi-family-words", "hindi-gender-masculine-feminine", "hindi-numbers-1-to-100",
           "hindi-or-urdu-difference", "hindi-phrases-for-travel", "hindi-verbs-present-past-future",
           "learn-hindi-from-bollywood", "learn-hindi-online-guide", "write-your-name-in-hindi"]


def load_bank():
    src = open(BANK, encoding="utf-8").read()
    m = re.search(r'window\.EKGURU_HINDI_QUIZ\s*=\s*(\{[\s\S]*?\});?\s*$', src)
    return json.loads(m.group(1))


def main():
    bank = load_bank()
    qs = bank["questions"]
    fails = []

    # schema
    required = {"id", "lesson", "type", "topic", "level", "q", "a", "opts", "explain"}
    for q in qs:
        missing = required - set(q)
        if missing:
            fails.append("%s missing %s" % (q.get("id", "?"), missing))

    # answer validity
    for q in qs:
        if q["a"] not in q["opts"]:
            fails.append("%s: answer not among options" % q["id"])
        if len(q["opts"]) != 4 or len(set(q["opts"])) != 4:
            fails.append("%s: options not 4 unique" % q["id"])

    # duplicates
    ids = [q["id"] for q in qs]
    dup_ids = sorted({i for i in ids if ids.count(i) > 1})
    if dup_ids:
        fails.append("duplicate ids: %s" % dup_ids)
    seen, dup_q = {}, []
    for q in qs:
        k = re.sub(r"\s+", " ", q["q"]).strip().lower()
        if k in seen:
            dup_q.append((seen[k], q["id"]))
        seen[k] = q["id"]
    if dup_q:
        fails.append("near-duplicate questions: %s" % dup_q)

    # coverage
    by_lesson = {}
    for q in qs:
        by_lesson.setdefault(q["lesson"], []).append(q)
    missing_lessons = [l for l in LESSONS if l not in by_lesson]
    if missing_lessons:
        fails.append("lessons without quiz: %s" % missing_lessons)
    thin = [l for l, v in by_lesson.items() if len(v) < 3]
    if thin:
        fails.append("lessons with <3 questions: %s" % thin)

    # accessibility + injection
    for l in LESSONS:
        p = os.path.join("learn", l, "index.html")
        if not os.path.exists(p):
            fails.append("missing lesson file: " + l)
            continue
        html = open(p, encoding="utf-8").read()
        if "<details" not in html or "<summary" not in html:
            fails.append("%s: no <details>/<summary> quiz" % l)

    # no false claims
    for q in qs:
        txt = (q["q"] + " " + q["explain"]).lower()
        for bad in ("native recording", "native audio", "recorded by", "ai "):
            if bad in txt:
                fails.append("%s: false claim '%s'" % (q["id"], bad))

    res = {
        "generated": "tbd", "bank": BANK, "totalQuestions": len(qs),
        "lessonsCovered": len(by_lesson), "lessonsTotal": len(LESSONS),
        "coverage": "%d/%d" % (len(by_lesson), len(LESSONS)),
        "pass": not fails, "fails": fails,
    }
    import time
    res["generated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open("reports/hindi-quiz-tests.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("quiz tests:", "PASS" if not fails else "FAIL")
    for x in fails[:20]:
        print("  ", x)
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
