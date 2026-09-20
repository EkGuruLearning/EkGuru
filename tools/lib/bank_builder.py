#!/usr/bin/env python3
"""Turn compact 8-theme rows into lesson objects."""
from tools.lib.extended_banks import V, G, D, lesson

# Shared English theme titles (UI language is English). Target-language
# strings must still be authored in each row.
THEMES = [
    "School and studies",
    "Hobbies and free time",
    "Travel basics",
    "Food and restaurants",
    "Friends and social life",
    "Weather and plans",
    "Shopping and money",
    "Daily routines and future plans",
]


def build_a3(rows):
    """rows: 8 items of (learn, vocab, grammar, dialogue)."""
    out = []
    if len(rows) != 8:
        raise ValueError("A3 needs 8 lessons, got %d" % len(rows))
    for i, row in enumerate(rows, 1):
        learn, vocab, grammar, dialogue = row
        out.append(lesson(i, THEMES[i - 1], learn, vocab, grammar, dialogue))
    return out


def v(rows):
    return [V(*r) if len(r) == 4 else V(r[0], r[1], r[2]) for r in rows]


def g(title, explain, pattern, examples, mistakes):
    return G(title, explain, pattern, examples, mistakes)


def d(lines):
    return D(lines)
