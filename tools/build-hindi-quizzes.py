#!/usr/bin/env python3
"""Phase 6 §3 — inject lesson quick quizzes from the canonical bank.

Single source of truth: js/hindi-quiz-bank.js (window.EKGURU_HINDI_QUIZ).
This tool:
  1. parses the bank (the data object is valid JSON),
  2. validates answers / options / duplicate IDs / per-lesson coverage,
  3. injects each lesson's questions into its page as an accessible
     <details>/<summary> self-check (keyboard-toggleable, no JS required),
     idempotently (an existing hand-authored or auto quiz section is
     replaced, guarded by a <!-- quiz:auto --> marker),
  4. writes reports/hindi-quiz-coverage-phase6.json.

Run: python3 tools/build-hindi-quizzes.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BANK = "js/hindi-quiz-bank.js"
LESSON_DIR = "learn"


def load_bank():
    src = open(BANK, encoding="utf-8").read()
    m = re.search(r'window\.EKGURU_HINDI_QUIZ\s*=\s*(\{[\s\S]*?\});?\s*$', src)
    if not m:
        raise SystemExit("could not locate window.EKGURU_HINDI_QUIZ in " + BANK)
    return json.loads(m.group(1))


def lesson_path(slug):
    p = os.path.join(LESSON_DIR, slug, "index.html")
    return p if os.path.exists(p) else None


def quiz_html(questions):
    """Render one <section class="quiz"> for a lesson's questions."""
    items = []
    for q in questions:
        a = q["a"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        e = q["explain"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        qq = q["q"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        items.append(
            '<details style="margin:10px 0;border:1px solid var(--line);border-radius:10px;padding:12px 14px">'
            '<summary style="cursor:pointer;font-weight:600;color:var(--ink)">%s</summary>'
            '<p style="margin:10px 0 0;color:var(--ink-2)">%s — %s</p></details>' % (qq, a, e))
    return ('<!-- quiz:auto:' + ",".join(q["id"] for q in questions) + ' -->\n'
            '    <section class="quiz" aria-label="Quick check" '
            'style="background:var(--bg-soft);border:1px solid #ddd8ff;border-radius:14px;'
            'padding:16px 18px;margin:30px 0"><h2 style="margin:0 0 12px;font-size:1.15rem">Quick check</h2>'
            + "".join(items) + "</section>")


def main():
    bank = load_bank()
    qs = bank["questions"]

    # ---- validation ----
    ids = [q["id"] for q in qs]
    dup_ids = sorted({i for i in ids if ids.count(i) > 1})
    dup_qs = []
    seen = {}
    for q in qs:
        key = re.sub(r"\s+", " ", q["q"]).strip().lower()
        if key in seen:
            dup_qs.append((seen[key], q["id"]))
        seen[key] = q["id"]

    bad_answers = []
    for q in qs:
        if q["a"] not in q["opts"]:
            bad_answers.append(q["id"])
        if len(q["opts"]) != 4:
            bad_answers.append(q["id"] + ":opts")

    lessons = {}
    for q in qs:
        lessons.setdefault(q["lesson"], []).append(q)

    # ---- inject ----
    injected, updated, missing = {}, [], []
    for slug, questions in sorted(lessons.items()):
        path = lesson_path(slug)
        if not path:
            missing.append(slug)
            continue
        html = open(path, encoding="utf-8").read()
        block = quiz_html(questions)
        # 1) remove any previous quiz (hand-authored or auto) inside .rel
        if "<!-- quiz:auto:" in html:
            html = re.sub(r'<!-- quiz:auto:.*?</section>', "", html, count=1, flags=re.S)
            updated.append(slug)
        elif '<section class="quiz"' in html:
            html = re.sub(r'<section class="quiz".*?</section>', "", html, count=1, flags=re.S)
            updated.append(slug)
        # 2) insert before "Keep going" inside .rel (fallback: right after <div class="rel">)
        anchor = '<h2>Keep going</h2>'
        if anchor in html:
            html = html.replace(anchor, block + "\n    " + anchor, 1)
        else:
            rel = '<div class="rel">'
            if rel not in html:
                missing.append(slug + ":no-rel")
                continue
            html = html.replace(rel, rel + "\n    " + block, 1)
        open(path, "w", encoding="utf-8").write(html)
        injected[slug] = len(questions)

    # ---- report ----
    coverage = {
        "generated": None,
        "bank": BANK,
        "version": bank.get("version"),
        "totalQuestions": len(qs),
        "lessonsWithQuiz": len(injected),
        "lessonsTotal": len(lessons),
        "coverage": "%d/%d" % (len(injected), len(lessons)),
        "perLesson": {k: len(v) for k, v in sorted(lessons.items())},
        "answerValidation": "PASS" if not bad_answers else ("FAIL: " + ",".join(bad_answers)),
        "duplicateIds": dup_ids,
        "duplicateQuestions": dup_qs,
        "accessibility": "native <details>/<summary> — keyboard toggle, no JS required",
        "updatedLessons": sorted(updated),
        "missingLessonFiles": missing,
    }
    import datetime, time
    coverage["generated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open("reports/hindi-quiz-coverage-phase6.json", "w", encoding="utf-8") as f:
        json.dump(coverage, f, ensure_ascii=False, indent=2)

    print("quiz bank: %d questions, %d lessons" % (len(qs), len(lessons)))
    print("coverage:", coverage["coverage"], "| answer validation:", coverage["answerValidation"])
    print("duplicate ids:", dup_ids or "none", "| duplicate questions:", dup_qs or "none")
    print("updated:", len(updated), "lessons | missing files:", missing or "none")


if __name__ == "__main__":
    main()
