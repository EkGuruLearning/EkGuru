#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One romanisation scheme per course file.

Every course states its romanisation twice: in the vocabulary column (`r`, the
"Say it" lane) and again wherever a lesson quotes the language it just taught —
`grammar.examples[].r`, a practice prompt that reads `ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ (sati srī
akāl)`, a worksheet item. When the two disagree, the reader meets two
transliterations of the same word on one page: Punjabi A1 printed
`main ṭhīk hān! te tusīn?` in its practice lane while its own vocabulary column
says `main thik han`, and Gujarati's generated mistake line said `(tamē)` where
the course writes `tame` everywhere else.

This tool makes a course file consistent with itself:

  * it only looks at files whose vocabulary romanisation column is diacritic-free
    (the `pa`, `mr`, `gu`, `ur A2+` convention: ASCII, no marks), and whose own
    words are written in a non-Latin script, so Latin text on the page is
    romanisation and not the language itself;
  * it strips the marks from (a) values under the key `r` — romanisation by
    contract — and (b) Latin groups in parentheses that follow the language's own
    script, e.g. `මෙය (meya)` or `મેજ (mēj)`;
  * it never touches `alphabet`, `pronunciation` or `counting`, the three blocks
    that *define* marks (`ṭa (retroflex)`, `ā (long a)`, low tone), and never
    touches English words that stand on their own (`Café worksheet`).

`--check` reports without writing and exits non-zero when a file is inconsistent,
so a language pass can use it as a gate; `--write` repairs. The rewrite is a
textual substitution inside the existing JSON (escaped exactly as the file holds
it), so the diff is the characters that changed and nothing else — no key
reordering, no re-indentation.

Usage:
    python3 tools/normalise-romanisation.py                 # report every course
    python3 tools/normalise-romanisation.py --lang pa       # one language
    python3 tools/normalise-romanisation.py --lang pa --write
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

LATIN = re.compile(r"[A-Za-z]")
NATIVE = re.compile(
    "[\u0400-\u04ff\u0530-\u058f\u0590-\u05ff\u0600-\u06ff\u0900-\u097f"
    "\u0980-\u09ff\u0a00-\u0a7f\u0a80-\u0aff\u0b00-\u0b7f\u0b80-\u0bff"
    "\u0c00-\u0c7f\u0c80-\u0cff\u0d00-\u0d7f\u0e00-\u0e7f\u0e80-\u0eff"
    "\u0f00-\u0fff\u1000-\u109f\u1780-\u17ff\u3040-\u30ff\u4e00-\u9fff"
    "\uac00-\ud7af]")
SKIP_BLOCKS = ("alphabet", "pronunciation", "counting")

# The three romanisation lanes this repo writes: `r` is a romanisation by
# contract; `say`/`rom` are the same idea in older rows; everything else is
# checked only inside parentheses after the course's own script.
R_KEYS = ("r", "rom", "say")
PARENS = re.compile(r"\(([^()]{1,120})\)")


def accented(s: str) -> str:
    """The Latin letters in `s` that carry a combining mark (ṭ ī ā ū ē …)."""
    out = []
    for ch in s:
        if not unicodedata.category(ch).startswith("L"):
            continue
        if len(unicodedata.normalize("NFD", ch)) <= 1:
            continue
        base = unicodedata.normalize("NFD", ch)[0]
        if base.isascii() and base.isalpha():
            out.append(ch)
    return "".join(out)


def strip_marks(s: str) -> tuple[str, str]:
    """Drop the marks from every Latin letter; return (new, what changed)."""
    changed = accented(s)
    if not changed:
        return s, ""
    out = []
    for ch in s:
        if ch in changed:
            out.append(unicodedata.normalize("NFD", ch)[0])
        else:
            out.append(ch)
    return "".join(out), changed


def fix_string(s: str) -> tuple[str, str]:
    """Fix one string value: `r`-style fields are all romanisation; otherwise
    only a parenthesised group that follows the course's own script."""
    if not s:
        return s, ""
    if not accented(s):
        return s, ""
    out, changed = s, ""
    for m in PARENS.finditer(s):
        inner = m.group(1)
        if NATIVE.search(inner):
            continue
        before = s[:m.start()]
        if not NATIVE.search(before[-60:]):
            continue
        fixed, what = strip_marks(inner)
        if fixed != inner:
            out = out.replace("(" + inner + ")", "(" + fixed + ")")
            changed += what
    return out, changed


def vocab_is_ascii(level: dict) -> bool:
    """True when the course's own romanisation column carries no marks."""
    for u in level.get("units") or []:
        for l in (u or {}).get("lessons") or []:
            for v in (l or {}).get("vocab") or []:
                if accented(str((v or {}).get("r") or "")):
                    return False
    return True


def native_words(level: dict) -> str:
    return "".join(str((v or {}).get("t") or "")
                   for u in (level.get("units") or [])
                   for l in ((u or {}).get("lessons") or [])
                   for v in ((l or {}).get("vocab") or []))


def course_in_scope(path: str) -> tuple[bool, str]:
    data = json.load(open(path, encoding="utf-8"))
    level = data.get("level") or {}
    words = native_words(level)
    if not words:
        return False, "no vocabulary"
    if LATIN.search(words[:400]):
        return False, "Latin-script course"
    if not vocab_is_ascii(level):
        return False, "this course's romanisation already uses marks"
    return True, ""


def walk(node, path="", key="", out=None):
    """Yield (path, key, value) for every string, skipping the mark-defining
    blocks — collected in `out` to keep the caller simple."""
    if out is None:
        out = []
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, "%s.%s" % (path, k), k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, "%s[%d]" % (path, i), key, out)
    elif isinstance(node, str):
        out.append((path, key, node))
    return out


def in_skipped_block(path: str) -> bool:
    head = path.lstrip(".").split("[")[0].split(".")[0]
    return head in SKIP_BLOCKS


def plan(path: str):
    """Every string in one course file that needs fixing."""
    data = json.load(open(path, encoding="utf-8"))
    rows = []
    for p, key, value in walk(data.get("level") or {}):
        if in_skipped_block(p):
            continue
        if key in R_KEYS:
            fixed, what = strip_marks(value)
        else:
            fixed, what = fix_string(value)
        if fixed != value:
            rows.append((p, value, fixed, what))
    return rows


def json_literal_forms(value: str):
    """The exact substrings a JSON file may hold for `value` (escaped or not)."""
    out = [value]
    escaped = json.dumps(value, ensure_ascii=False)[1:-1]
    if escaped != value:
        out.append(escaped)
    ascii_form = json.dumps(value)[1:-1]
    if ascii_form not in out:
        out.append(ascii_form)
    return out


def apply_to_file(path: str, rows) -> int:
    """Rewrite the file in place, then re-plan it: 0 means the file is clean.

    Rows repeat — Gujarati's generated mistake line is the same sentence in every
    unit — so identical rewrites are applied once and counted once; the check that
    matters is that the file no longer plans anything.
    """
    text = open(path, encoding="utf-8").read()
    pairs = []
    for _p, old, new, _what in rows:
        for old_form in json_literal_forms(old):
            if old_form not in text:
                continue
            new_form = old_form
            for a in accented(old):
                new_form = new_form.replace(a, unicodedata.normalize("NFD", a)[0])
            if new_form != old_form:
                pairs.append((old_form, new_form))
            break
    for old_form, new_form in dict.fromkeys(pairs):
        text = text.replace(old_form, new_form)
    open(path, "w", encoding="utf-8").write(text)
    return len(plan(path))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lang", action="append", default=[], help="limit to these course codes")
    ap.add_argument("--write", action="store_true", help="repair; without it, report only")
    args = ap.parse_args()

    files = sorted(glob.glob("data/courses/*/*.json"))
    checked = skipped = repaired = 0
    failures = []
    for path in files:
        stem = os.path.basename(path)[:-5]
        code = stem.partition("_")[0]
        if args.lang and code not in args.lang:
            continue
        ok, why = course_in_scope(path)
        if not ok:
            skipped += 1
            continue
        checked += 1
        rows = plan(path)
        if not rows:
            continue
        repaired += len(rows)
        print("%s  %d string(s)" % (path, len(rows)))
        for p, old, new, what in rows[:6]:
            print("    %s  [%s]" % (p, what))
            print("      - %s" % old[:120])
            if args.write:
                print("      + %s" % new[:120])
        if len(rows) > 6:
            print("    … %d more" % (len(rows) - 6))
        if args.write:
            left = apply_to_file(path, rows)
            print("    → written%s" % ("" if not left else
                                       "; !! %d string(s) still planned" % left))
            if left:
                failures.append(path)

    print("\n%d course file(s) in scope (%d skipped: another scheme or script), "
          "%d string(s) %s" % (checked, skipped, repaired,
                               "repaired" if args.write else "to repair"))
    if failures:
        print("!! still inconsistent after writing: %s" % ", ".join(failures))
        return 2
    if repaired and not args.write:
        print("run again with --write to apply")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
