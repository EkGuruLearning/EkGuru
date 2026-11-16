#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hindi C3 / C4 / C5 — the post-C2 extension ladder, authored and published.

Sources (compact Python tuples, one module per level):

    tools/hindi-ext-content/c3.py   Expert : media, satire, regional colour
    tools/hindi-ext-content/c4.py   Scholar: literature, word-craft, academic Hindi
    tools/hindi-ext-content/c5.py   Master : translation, oratory, teaching, classics

Each module exposes TITLE, GOALS, UNITS, TEST, EXTRA. This script expands the
tuples into the course JSON schema used by hi_B3.json (vocab {t,r,en,pos},
grammar {title,explain,pattern,examples[{t,r,en}],mistakes}, dialogue
[{sp,t,r,en}], practice, quiz, flashcards "auto:vocab", worksheet,
srs_candidates, srs_policy), tops each lesson up to ten practice items with
three exercises derived from that lesson's own vocabulary, grammar examples and
dialogue (never templated filler), validates the result against the same
minimums as tools/author-hindi-advanced.py, and writes

    data/courses/phase-2/hi_C3.json
    data/courses/phase-2/hi_C4.json
    data/courses/phase-2/hi_C5.json

with content_status REAL and indexable true. Publication still goes through
tools/audit-course-quality.py (release manifest) and the placeholder scan.

Run:  python3 tools/author-hindi-extension.py           write the three files
      python3 tools/author-hindi-extension.py --check   report drift only
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools" / "hindi-ext-content"
OUT_DIR = ROOT / "data" / "courses" / "phase-2"
sys.path.insert(0, str(ROOT))

from tools.lib.placeholders import is_placeholder  # noqa: E402

LEVELS = ["C3", "C4", "C5"]
LESSON_KEYS = ["id", "title", "learn", "vocab", "grammar", "dialogue", "practice", "quiz", "worksheet"]
MIN_PRACTICE = 10

NOTE = {
    "C3": "EkGuru post-C2 extension (Expert). Not a CEFR level.",
    "C4": "EkGuru post-C2 extension (Scholar). Not a CEFR level.",
    "C5": "EkGuru post-C2 extension (Master). Not a CEFR level.",
}
REASON = {
    "C3": "EkGuru post-C2 extension, labelled Expert in the course index. Not a CEFR level. "
          "Authored 2026-11-16 from tools/hindi-ext-content/c3.py; published as the first rung above C2.",
    "C4": "EkGuru post-C2 extension, labelled Scholar in the course index. Not a CEFR level. "
          "Authored 2026-11-16 from tools/hindi-ext-content/c4.py; published as the second rung above C2.",
    "C5": "EkGuru post-C2 extension, labelled Master in the course index. Not a CEFR level. "
          "Authored 2026-11-16 from tools/hindi-ext-content/c5.py; published as the final rung of the ladder.",
}
SRS_POLICY = ("Only these four high-value terms are preselected; lesson mistakes and productive "
              "patterns may enter personalised review after an actual error.")


def load_module(level: str):
    path = SRC / f"{level.lower()}.py"
    spec = importlib.util.spec_from_file_location(f"hindi_ext_{level.lower()}", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# expansion
# ---------------------------------------------------------------------------

def expand_vocab(rows):
    return [{"t": t, "r": r, "en": en, "pos": pos} for (t, r, en, pos) in rows]


def expand_grammar(g):
    return {
        "title": g["title"],
        "explain": g["explain"],
        "pattern": g["pattern"],
        "examples": [{"t": t, "r": r, "en": en} for (t, r, en) in g["examples"]],
        "mistakes": list(g.get("mistakes", [])),
    }


def expand_dialogue(rows):
    return [{"sp": sp, "t": t, "r": r, "en": en} for (sp, t, r, en) in rows]


def derived_practice(lesson_id: str, vocab: list[dict], grammar: dict, dialogue: list[dict]) -> list[dict]:
    """Three exercises built from the lesson's own material.

    1. vocabulary meaning (multiple choice, distractors from the same lesson)
    2. reverse translation of the second grammar example
    3. dialogue comprehension (which speaker said it / what did they mean)
    """
    items: list[dict] = []
    if len(vocab) >= 4:
        target = vocab[1]
        distract = [v["en"] for v in vocab if v is not target][:3]
        options = [target["en"]] + distract
        # deterministic, non-alphabetical shuffle keyed on the lesson id
        k = sum(ord(ch) for ch in lesson_id) % 4
        options = options[k:] + options[:k]
        items.append({
            "type": "multiple_choice",
            "q": f"What does ‘{target['t']}’ ({target['r']}) mean in this lesson?",
            "answer": target["en"],
            "skill_target": "vocabulary recall",
            "options": options,
        })
    ex = grammar["examples"]
    if len(ex) >= 2:
        e = ex[1]
        items.append({
            "type": "reverse_translation",
            "q": f"Put into Hindi, using the pattern of this lesson: ‘{e['en']}’",
            "answer": e["t"],
            "skill_target": "pattern production",
        })
    if len(dialogue) >= 3:
        line = dialogue[2]
        speakers = []
        for d in dialogue:
            if d["sp"] not in speakers:
                speakers.append(d["sp"])
        items.append({
            "type": "multiple_choice" if len(speakers) >= 2 else "fill_in_the_blank",
            "q": f"In the dialogue, who says: ‘{line['t']}’?",
            "answer": line["sp"],
            "skill_target": "dialogue comprehension",
            **({"options": speakers[:4]} if len(speakers) >= 2 else {}),
        })
    return items


def expand_lesson(src: dict) -> dict:
    vocab = expand_vocab(src["vocab"])
    grammar = expand_grammar(src["grammar"])
    dialogue = expand_dialogue(src["dialogue"])
    practice = [dict(p) for p in src["practice"]]
    if len(practice) < MIN_PRACTICE:
        practice.extend(derived_practice(src["id"], vocab, grammar, dialogue))
    return {
        "id": src["id"],
        "title": src["title"],
        "learn": src["learn"],
        "vocab": vocab,
        "grammar": grammar,
        "dialogue": dialogue,
        "practice": practice,
        "quiz": [dict(q) for q in src["quiz"]],
        "flashcards": "auto:vocab",
        "worksheet": {
            "title": src["worksheet"]["title"],
            "tasks": [dict(t) for t in src["worksheet"]["tasks"]],
        },
        "srs_candidates": list(src["srs"]),
        "srs_policy": SRS_POLICY,
    }


def expand_units(units):
    return [{"id": u["id"], "title": u["title"], "lessons": [expand_lesson(l) for l in u["lessons"]]}
            for u in units]


# ---------------------------------------------------------------------------
# validation (same minimums as author-hindi-advanced.py)
# ---------------------------------------------------------------------------

def validate(level_code: str, units: list[dict], level: dict) -> list[str]:
    p: list[str] = []
    if not 3 <= len(units) <= 5:
        p.append(f"{level_code} units: {len(units)} (wants 3-5)")
    seen_ids: set[str] = set()
    for unit in units:
        if not 3 <= len(unit["lessons"]) <= 5:
            p.append(f"{unit['id']}: {len(unit['lessons'])} lessons (wants 3-5)")
        for les in unit["lessons"]:
            lid = les.get("id")
            if lid in seen_ids:
                p.append(f"{lid}: duplicate lesson id")
            seen_ids.add(lid)
            missing = [k for k in LESSON_KEYS if k not in les]
            if missing:
                p.append(f"{lid}: missing {missing}")
            if len(les["practice"]) < MIN_PRACTICE:
                p.append(f"{lid}: practice {len(les['practice'])} (wants {MIN_PRACTICE}+)")
            if len(les["quiz"]) < 3:
                p.append(f"{lid}: quiz < 3")
            if len(les["dialogue"]) < 2:
                p.append(f"{lid}: dialogue < 2")
            if len(les["vocab"]) < 6:
                p.append(f"{lid}: vocab < 6")
            if not les["grammar"]["examples"]:
                p.append(f"{lid}: grammar has no examples")
            for i, it in enumerate(les["practice"]):
                for k in ("type", "q", "answer", "skill_target"):
                    if not it.get(k):
                        p.append(f"{lid}: practice[{i}] missing {k}")
                if it.get("type") in ("multiple_choice", "matching") and it.get("options"):
                    if it["answer"] not in it["options"]:
                        p.append(f"{lid}: practice[{i}] answer not among options")
            for i, q in enumerate(les["quiz"]):
                if not isinstance(q.get("answer"), int) or not 0 <= q["answer"] < len(q.get("options", [])):
                    p.append(f"{lid}: quiz[{i}] answer index out of range")
                if not q.get("why"):
                    p.append(f"{lid}: quiz[{i}] missing why")
            for i, t in enumerate(les["worksheet"]["tasks"]):
                if not t.get("instruction") or not t.get("items") or not t.get("key"):
                    p.append(f"{lid}: worksheet task[{i}] incomplete")
            if len(les.get("srs_candidates", [])) != 4:
                p.append(f"{lid}: srs_candidates should be exactly 4")
            vocab_terms = {v["t"] for v in les["vocab"]}
            for term in les.get("srs_candidates", []):
                if term not in vocab_terms:
                    p.append(f"{lid}: srs term ‘{term}’ not in lesson vocab")
    items = level["test"]["items"]
    if not 10 <= len(items) <= 20:
        p.append(f"{level_code} test: {len(items)} items (wants 10-20)")
    for i, it in enumerate(items):
        if it.get("type") not in ("translate_en", "translate_hi", "speak"):
            p.append(f"{level_code} test[{i}] odd type {it.get('type')}")
        if not it.get("q") or not it.get("answer"):
            p.append(f"{level_code} test[{i}] missing q/answer")
    extra = level["extra"]
    for key in ("culture", "reading", "listening", "idioms", "mistakes", "task"):
        if key not in extra:
            p.append(f"{level_code} extra: {key} missing")
    if len(extra.get("idioms", [])) < 10:
        p.append(f"{level_code} extra: idioms < 10")
    if len(extra.get("mistakes", [])) < 3:
        p.append(f"{level_code} extra: mistakes < 3")
    if extra.get("reading", {}).get("original") is not True:
        p.append(f"{level_code} extra: reading must be original: true")
    if not extra.get("listening", {}).get("voice_tag"):
        p.append(f"{level_code} extra: listening voice_tag missing")
    if not extra.get("culture", {}).get("source_url"):
        p.append(f"{level_code} extra: culture source_url missing")
    return p


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

def build(level_code: str) -> tuple[dict, list[str]]:
    mod = load_module(level_code)
    units = expand_units(mod.UNITS)
    level = {
        "id": level_code,
        "title": mod.TITLE,
        "goals": list(mod.GOALS),
        "units": units,
        "test": {"title": mod.TEST["title"], "items": [dict(i) for i in mod.TEST["items"]]},
        "extra": json.loads(json.dumps(mod.EXTRA, ensure_ascii=False)),
    }
    problems = validate(level_code, units, level)
    course = {
        "code": "hi",
        "name": "Hindi",
        "native": "Hindi",
        "phase": "phase-2",
        "medium": "en",
        "file_level": level_code,
        "content_status": "REAL",
        "indexable": True,
        "ekguru_extension": True,
        "cefr_equivalent": None,
        "cefr_note": NOTE[level_code],
        "reason": REASON[level_code],
        "level": level,
    }
    if is_placeholder(course):
        problems.append(f"{level_code}: placeholder scan hit")
    return course, problems


def main() -> int:
    check = "--check" in sys.argv
    rc = 0
    for lv in LEVELS:
        course, problems = build(lv)
        if problems:
            for p in problems:
                print("  INVALID:", p)
            rc = 1
            continue
        out = json.dumps(course, ensure_ascii=False, indent=2) + "\n"
        path = OUT_DIR / f"hi_{lv}.json"
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        units = course["level"]["units"]
        n_lessons = sum(len(u["lessons"]) for u in units)
        n_practice = sum(len(l["practice"]) for u in units for l in u["lessons"])
        if check:
            if current != out:
                print(f"  hi_{lv}.json STALE")
                rc = 1
            else:
                print(f"OK: hi_{lv}.json current ({len(units)} units, {n_lessons} lessons, {n_practice} practice)")
            continue
        if current != out:
            path.write_text(out, encoding="utf-8")
            print(f"written: hi_{lv}.json ({len(units)} units, {n_lessons} lessons, {n_practice} practice, "
                  f"test {len(course['level']['test']['items'])}, idioms {len(course['level']['extra']['idioms'])})")
        else:
            print(f"already current: hi_{lv}.json")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
