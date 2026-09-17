#!/usr/bin/env python3
"""Course builder/validator — Phase program (10 languages per phase).

Reads :  data/courses/phase-N/<code>_<LV>.json   (LV = A1 A2 B1 B2 C1 C2)
Writes:  data/courses/index.json                 (manifest grouped by course)

Every course = 6 levels (A1 beginner -> C2 mastery), 6 lessons per level
(3 units x 2 lessons) = 24 lessons. A1 file ALSO holds alphabet + counting.
Every lesson holds: learn, vocab>=8, grammar, dialogue>=4, practice>=5,
quiz==5, flashcards, worksheet(>=3 tasks with keys). Every level: goals>=3
+ test>=10. Romanisation (r) REQUIRED on every target string — a total
beginner (even a child) reads everything through English.

Run:  python3 tools/build-courses.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSES = os.path.join(ROOT, "data", "courses")
LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")
PTYPES = (
    "translate_en", "translate_t", "fill", "choose", "reorder", "speak",
    "multiple_choice", "fill_in_the_blank", "translation", "reverse_translation",
    "matching", "sentence_building", "word_selection", "error_correction",
    "dialogue_completion", "reading_comprehension", "paragraph_comprehension",
    "inference", "main_idea", "detail_identification", "listening_comprehension",
    "dictation", "listen_and_choose", "listen_and_reorder", "listen_and_fill",
    "repeat_after_audio", "pronunciation", "shadowing", "guided_speaking",
    "free_response", "roleplay", "sentence_writing", "short_writing", "paraphrase",
    "summary", "guided_composition", "register_transformation", "tone_identification",
    "semantic_distinction", "contextual_meaning", "argument_construction",
    "discourse_ordering", "style_rewriting", "idiom_interpretation", "implied_meaning",
)
CHOICE_PTYPES = ("multiple_choice", "matching", "word_selection", "listen_and_choose")
AUDIO_PTYPES = ("listening_comprehension", "dictation", "listen_and_choose", "listen_and_reorder", "listen_and_fill", "repeat_after_audio", "pronunciation", "shadowing")
ERRORS = []


def err(path, msg):
    ERRORS.append(f"{path}: {msg}")


def need_str(obj, key, path):
    if not isinstance(obj, dict) or not isinstance(obj.get(key), str) or not obj[key].strip():
        err(path, f"missing/empty '{key}'")
        return False
    return True


def check_vocab(vocab, path, minimum=8):
    if not isinstance(vocab, list) or len(vocab) < minimum:
        err(path, f"vocab needs >={minimum}, got {len(vocab) if isinstance(vocab, list) else '?'}")
        return 0
    n = 0
    for i, v in enumerate(vocab):
        p = f"{path}.vocab[{i}]"
        if not isinstance(v, dict):
            err(p, "not an object"); continue
        if need_str(v, "t", p) & need_str(v, "r", p) & need_str(v, "en", p):
            n += 1
    return n


def check_lesson(les, path):
    if not isinstance(les, dict):
        err(path, "lesson not an object"); return 0
    need_str(les, "id", path); need_str(les, "title", path); need_str(les, "learn", path)
    n = check_vocab(les.get("vocab"), path)
    g = les.get("grammar")
    if not isinstance(g, dict):
        err(path, "missing grammar")
    else:
        gp = path + ".grammar"
        need_str(g, "title", gp); need_str(g, "explain", gp); need_str(g, "pattern", gp)
        ex = g.get("examples", [])
        if not isinstance(ex, list) or len(ex) < 3:
            err(gp, f"needs >=3 examples, got {len(ex) if isinstance(ex, list) else '?'}")
        else:
            for i, e in enumerate(ex):
                if not isinstance(e, dict):
                    err(f"{gp}.examples[{i}]", "not an object"); continue
                need_str(e, "t", gp); need_str(e, "r", gp); need_str(e, "en", gp)
        if not isinstance(g.get("mistakes"), list) or len(g.get("mistakes", [])) < 1:
            err(gp, "needs >=1 mistakes entry")
    d = les.get("dialogue", [])
    if not isinstance(d, list) or len(d) < 4:
        err(path, f"dialogue needs >=4 lines, got {len(d) if isinstance(d, list) else '?'}")
    else:
        for i, line in enumerate(d):
            if not isinstance(line, dict):
                err(f"{path}.dialogue[{i}]", "not an object"); continue
            need_str(line, "t", path); need_str(line, "r", path); need_str(line, "en", path)
    pr = les.get("practice", [])
    if not isinstance(pr, list) or len(pr) < 5:
        err(path, f"practice needs >=5, got {len(pr) if isinstance(pr, list) else '?'}")
    else:
        for i, p in enumerate(pr):
            if not isinstance(p, dict):
                err(f"{path}.practice[{i}]", "not an object"); continue
            if p.get("type") not in PTYPES:
                err(f"{path}.practice[{i}]", f"bad type {p.get('type')!r}")
            need_str(p, "q", path)
            if "answer" not in p or p["answer"] in (None, ""):
                err(f"{path}.practice[{i}]", "missing answer")
            if p.get("type") in CHOICE_PTYPES:
                if not isinstance(p.get("options"), list) or len(p["options"]) < 2:
                    err(f"{path}.practice[{i}]", "choice-style practice needs >=2 options")
                elif not any(str(x).strip() == str(p.get("answer", "")).strip() for x in p["options"]):
                    err(f"{path}.practice[{i}]", "answer must occur in options")
            if p.get("type") in AUDIO_PTYPES and not need_str(p, "audio_source", f"{path}.practice[{i}]"):
                pass
    qz = les.get("quiz", [])
    if not isinstance(qz, list) or len(qz) != 5:
        err(path, f"quiz needs exactly 5, got {len(qz) if isinstance(qz, list) else '?'}")
    else:
        for i, q in enumerate(qz):
            if not isinstance(q, dict):
                err(f"{path}.quiz[{i}]", "not an object"); continue
            need_str(q, "q", path)
            if not isinstance(q.get("options"), list) or len(q.get("options", [])) != 4:
                err(f"{path}.quiz[{i}]", "needs exactly 4 options")
            a = q.get("answer")
            if not isinstance(a, int) or not 0 <= a <= 3:
                err(f"{path}.quiz[{i}]", f"answer must be 0-3, got {a!r}")
    if "flashcards" not in les:
        err(path, "missing flashcards field")
    w = les.get("worksheet")
    if not isinstance(w, dict):
        err(path, "missing worksheet")
    else:
        wp = path + ".worksheet"
        need_str(w, "title", wp)
        tasks = w.get("tasks", [])
        if not isinstance(tasks, list) or len(tasks) < 3:
            err(wp, f"needs >=3 tasks, got {len(tasks) if isinstance(tasks, list) else '?'}")
        else:
            for i, t in enumerate(tasks):
                if not isinstance(t, dict):
                    err(f"{wp}.tasks[{i}]", "not an object"); continue
                need_str(t, "instruction", path)
                if not isinstance(t.get("items"), list) or len(t["items"]) < 2:
                    err(f"{wp}.tasks[{i}]", "needs >=2 items")
                if not isinstance(t.get("key"), list) or len(t["key"]) != len(t.get("items", [])):
                    err(f"{wp}.tasks[{i}]", "key must match items 1:1")
    return n


def check_test(test, path):
    if not isinstance(test, dict):
        err(path, "missing test"); return 0
    need_str(test, "title", path)
    items = test.get("items", [])
    if not isinstance(items, list) or len(items) < 10:
        err(path, f"level test needs >=10 items, got {len(items) if isinstance(items, list) else '?'}")
        return 0
    for i, p in enumerate(items):
        if not isinstance(p, dict):
            err(f"{path}.items[{i}]", "not an object"); continue
        if p.get("type") not in PTYPES:
            err(f"{path}.items[{i}]", f"bad type {p.get('type')!r}")
        need_str(p, "q", path)
        if "answer" not in p or p["answer"] in (None, ""):
            err(f"{path}.items[{i}]", "missing answer")
    return len(items)


def check_alphabet(a, path):
    if not isinstance(a, dict):
        err(path, "A1 needs alphabet{}"); return
    need_str(a, "title", path); need_str(a, "explain", path)
    letters = a.get("letters", [])
    if not isinstance(letters, list) or len(letters) < 10:
        err(path, f"alphabet needs >=10 letters, got {len(letters) if isinstance(letters, list) else '?'}")
        return
    for i, L in enumerate(letters):
        if not isinstance(L, dict):
            err(f"{path}.letters[{i}]", "not an object"); continue
        need_str(L, "t", path); need_str(L, "r", path)


def check_counting(c, path):
    if not isinstance(c, dict):
        err(path, "A1 needs counting{}"); return
    need_str(c, "title", path); need_str(c, "explain", path)
    nums = c.get("numbers", [])
    if not isinstance(nums, list) or len(nums) < 20:
        err(path, f"counting needs >=20 numbers, got {len(nums) if isinstance(nums, list) else '?'}")
    else:
        for i, N in enumerate(nums):
            if not isinstance(N, dict):
                err(f"{path}.numbers[{i}]", "not an object"); continue
            need_str(N, "t", path); need_str(N, "r", path); need_str(N, "en", path)
    if not isinstance(c.get("rules"), list) or len(c.get("rules", [])) < 2:
        err(path, "counting needs >=2 rules")


def main():
    manifest = {"format": "course-per-level", "levels": list(LEVELS), "courses": [],
                "generated_by": "tools/build-courses.py"}
    by_code = {}
    total_lessons = 0
    total_vocab = 0
    if not os.path.isdir(COURSES):
        print("no data/courses dir"); sys.exit(1)
    for phase in sorted(os.listdir(COURSES)):
        pdir = os.path.join(COURSES, phase)
        if not os.path.isdir(pdir) or not phase.startswith("phase-"):
            continue
        for fn in sorted(os.listdir(pdir)):
            if not fn.endswith(".json") or fn.startswith("_"):
                continue
            m = re.match(r"^([a-z]{2,3})_(A1|A2|B1|B2|C1|C2)\.json$", fn)
            fpath = os.path.join(pdir, fn)
            cpath = f"{phase}/{fn}"
            if not m:
                err(cpath, "filename must be <code>_<A1|A2|B1|B2|C1|C2>.json"); continue
            code, lv = m.group(1), m.group(2)
            try:
                with open(fpath, encoding="utf-8") as f:
                    raw = f.read()
                if "�" in raw:
                    err(cpath, "contains U+FFFD")
                course = json.loads(raw)
            except Exception as e:
                err(cpath, f"bad JSON: {e}"); continue
            if course.get("code") != code:
                err(cpath, f"code field {course.get('code')!r} != filename {code}")
            if course.get("file_level") != lv:
                err(cpath, f"file_level {course.get('file_level')!r} != filename {lv}")
            need_str(course, "name", cpath)
            if course.get("medium") != "en":
                err(cpath, "medium must be 'en'")
            if lv == "A1":
                check_alphabet(course.get("alphabet"), cpath + ".alphabet")
                check_counting(course.get("counting"), cpath + ".counting")
            L = course.get("level")
            if not isinstance(L, dict):
                err(cpath, "missing level{}"); continue
            need_str(L, "title", cpath)
            if not isinstance(L.get("goals"), list) or len(L["goals"]) < 3:
                err(cpath, f"needs >=3 goals, got {len(L.get('goals', [])) if isinstance(L.get('goals'), list) else '?'}")
            units = L.get("units", [])
            if not isinstance(units, list) or len(units) != 3:
                err(cpath, f"needs exactly 3 units, got {len(units) if isinstance(units, list) else '?'}")
                continue
            nles = 0
            for u in units:
                if not isinstance(u, dict):
                    err(cpath, "unit not an object"); continue
                need_str(u, "id", cpath); need_str(u, "title", cpath)
                lessons = u.get("lessons", [])
                if not isinstance(lessons, list) or len(lessons) != 2:
                    err(f"{cpath}.{u.get('id')}", "needs exactly 2 lessons"); continue
                for les in lessons:
                    lid = les.get("id") if isinstance(les, dict) else "?"
                    total_vocab += check_lesson(les, f"{cpath}.{u.get('id')}.{lid}")
                    nles += 1
            test_n = check_test(L.get("test"), cpath + ".test")
            total_lessons += nles
            slot = by_code.setdefault(code, {"code": code, "name": course.get("name"),
                                             "phase": phase, "levels": {}, "files": []})
            slot["levels"][lv] = {"lessons": nles, "test_items": test_n}
            slot["files"].append(fn)
    for code in sorted(by_code):
        slot = by_code[code]
        slot["complete"] = all(lv in slot["levels"] for lv in LEVELS)
        slot["files"].sort()
        manifest["courses"].append(slot)
    with open(os.path.join(COURSES, "index.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(f"lessons={total_lessons} vocab={total_vocab} errors={len(ERRORS)}")
    for e in ERRORS[:40]:
        print("ERR", e)
    sys.exit(1 if ERRORS else 0)


if __name__ == "__main__":
    main()
