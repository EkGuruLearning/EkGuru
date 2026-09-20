#!/usr/bin/env python3
"""Detect manufactured course placeholders.

The extended-course generator used to write tokens such as `hi_word_1_1`,
`roman_1_1`, and English stubs like `theme related word`. Those strings are
not lessons. Any file that still contains them is unpublished material.
"""
from __future__ import annotations

import json
import os
import re

PLACEHOLDER_RES = [
    re.compile(r"\b[a-z]{2,3}_word_\d+_\d+\b", re.I),
    re.compile(r"\broman_\d+(?:_\d+)?\b", re.I),
    re.compile(r"related word \d+", re.I),
    re.compile(r"Example \d+ in ", re.I),
    re.compile(r"Dialogue line \d+", re.I),
    re.compile(r"English translation \d+ about", re.I),
    re.compile(r"Common mistake \d+ for ", re.I),
    re.compile(r"Practice question \d+ about ", re.I),
    re.compile(r"Test question \d+ for ", re.I),
    re.compile(r"Correct \{?theme\}? \d+", re.I),
    re.compile(r"\bword_\d+_\d+\b"),
    re.compile(r"\bnum_\d+\b"),
    re.compile(r"Trace: [a-z]{2,3}_word_", re.I),
]

EXTRA_LEVELS = ("A3", "B3", "C3", "C4", "C5")
CEFR_LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")
ALL_LEVELS = CEFR_LEVELS + EXTRA_LEVELS


def blob_of(obj) -> str:
    if isinstance(obj, str):
        return obj
    return json.dumps(obj, ensure_ascii=False)


def placeholder_hits(text: str) -> list[str]:
    hits = []
    for rx in PLACEHOLDER_RES:
        m = rx.search(text)
        if m:
            hits.append(m.group(0))
    return hits


def is_placeholder(obj) -> bool:
    return bool(placeholder_hits(blob_of(obj)))


def content_status(obj) -> str:
    if not isinstance(obj, dict):
        return "UNKNOWN"
    stated = (obj.get("content_status") or "").upper()
    if stated in ("INCOMPLETE", "REAL", "PLACEHOLDER"):
        if stated == "REAL" and is_placeholder(obj):
            return "PLACEHOLDER"
        return stated
    if is_placeholder(obj):
        return "PLACEHOLDER"
    units = ((obj.get("level") or {}).get("units") or [])
    lessons = [l for u in units for l in (u.get("lessons") or [])]
    if not lessons:
        return "INCOMPLETE"
    return "REAL"


def walk_course_json(root: str = "data/courses"):
    for dirpath, _dirs, files in os.walk(root):
        if os.path.basename(dirpath) == "index.json":
            continue
        for f in files:
            if not f.endswith(".json") or f == "index.json":
                continue
            path = os.path.join(dirpath, f).replace("\\", "/")
            yield path
