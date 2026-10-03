# -*- coding: utf-8 -*-
"""Helpers for the per-language PHASE 1 depth modules (`tools/depth-content/`).

A lesson is authored as a *spec* — a plain dict built by the helpers below — and
`tools/author-depth.py` expands it into the full lesson shape the course schema
requires (`practice` 12 types, `quiz`, `flashcards`, `srs_candidates`,
`srs_policy`). Keeping the authoring surface small is the point: the content
module should read like a phrasebook, not like JSON.

    L(title, learn, vocab, grammar, dialogue, worksheet)

Everything is language-neutral; the renderer knows the language, not the kit.
"""
from __future__ import annotations


def V(t, r, en, pos="phrase"):
    """A vocabulary item: target, romanisation, English, part of speech."""
    return {"t": t, "r": r, "en": en, "pos": pos}


def X(t, r, en):
    """A bare example: target, romanisation, English."""
    return {"t": t, "r": r, "en": en}


def G(title, pattern, explain, examples, mistakes=None):
    """A grammar box. `examples` are X() items; `mistakes` are (wrong, right, why)."""
    return {
        "title": title,
        "pattern": pattern,
        "explain": explain,
        "examples": list(examples),
        "mistakes": [{"wrong": w, "right": r, "why": y} for (w, r, y) in (mistakes or [])],
    }


def D(sp, t, r, en):
    """One dialogue turn by speaker `sp`."""
    return {"sp": sp, "t": t, "r": r, "en": en}


def T(instruction, items, key):
    """One worksheet task: prompt-in-English list, and its answer key."""
    return {"instruction": instruction, "items": list(items), "key": list(key)}


def WS(title, tasks):
    return {"title": title, "tasks": list(tasks)}


def L(title, learn, vocab, grammar, dialogue, worksheet):
    """A full lesson spec (the renderer adds ids, practice, quiz and SRS)."""
    return {
        "title": title,
        "learn": learn,
        "vocab": list(vocab),
        "grammar": grammar,
        "dialogue": list(dialogue),
        "worksheet": worksheet,
    }


def EXTRA(culture, source_url, reading, reading_gloss, listening, listening_gloss,
          voice_tag, idioms, mistakes, task_title, task_instructions):
    """The six-section `extra` block the schema requires on every rung.

    idioms:   (target, literal, meaning) triples, ten of them
    mistakes: (wrong, right, why) triples, at least three
    """
    return {
        "culture": {"text": culture, "source_url": source_url},
        "reading": {"text": reading, "gloss": reading_gloss, "original": True},
        "listening": {"script": listening, "gloss": listening_gloss, "voice_tag": voice_tag},
        "idioms": [{"t": t, "literal": lit, "meaning": m} for (t, lit, m) in idioms],
        "mistakes": [{"wrong": w, "right": r, "why": y} for (w, r, y) in mistakes],
        "task": {"title": task_title, "instructions": task_instructions},
    }
