#!/usr/bin/env python3
"""Idempotent removal of 'Learn' and 'Become a Tutor' from ALL header
variants (desktop, sticky, mobile drawer, tablet, responsive duplicates).

Implements PHASE 23 / Phase 3 of the master command:
  - REMOVE the "Become a Tutor" (nav.join) link from every header nav
  - REMOVE the "Learn" dropdown (nav-more) from every header
  - KEEP the underlying learn/ and join.html pages reachable via footer
    links (untouched).

Line-based edits (no fragile regex over nested HTML).
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

EN_HEADER_FILES = ["index.html", "find-tutors.html", "join.html", "tutor.html"]
LOCALIZED = [(d, f) for d in ["ar", "de", "es", "fr", "ja", "pt"]
             for f in ["index.html", "find-tutors.html", "join.html"]]
TUTOR_PROFILES = [
    "tutor/hemlata/index.html",
    "tutor/shikha-dutta/index.html",
    "tutor/sushila-g/index.html",
    "tutor/tara/index.html",
]

changes = []

def edit(rel, mutate_lines):
    p = ROOT / rel
    lines = p.read_text(encoding="utf-8").split("\n")
    out = mutate_lines(lines)
    new = "\n".join(out)
    if new == "\n".join(lines):
        return
    p.write_text(new, encoding="utf-8")
    changes.append(rel)

def remove_en_header(lines):
    """Remove nav.join link (first occurrence = header) and the nav-more group."""
    out = lines[:]
    # 1) 'Become a Tutor' header link — first occurrence in file is the header.
    for i, ln in enumerate(out):
        if 'data-i18n="nav.join"' in ln and 'data-navlink="join.html"' in ln:
            del out[i]
            break
    # 2) 'Learn' dropdown: from the 'Three long labels' comment through the
    #    closing </div> of .nav-more (div-depth balanced).
    start = None
    for i, ln in enumerate(out):
        if "Three long labels" in ln:
            start = i
            break
    if start is not None:
        depth = 0
        opened = False
        end = None
        for j in range(start, len(out)):
            line = out[j]
            if "<div" in line:
                # count every <div ...> on the line (nav-more open + menu open)
                depth += line.count("<div")
                opened = True
            if "</div>" in line:
                depth -= line.count("</div>")
            if opened and depth <= 0:
                end = j
                break
        if end is not None:
            del out[start:end + 1]
    return out

def remove_localized_header(lines):
    """Remove the localized join link — first <a href="join.html"> is the header."""
    out = lines[:]
    for i, ln in enumerate(out):
        if '<a href="join.html">' in ln:
            del out[i]
            break
    return out

def remove_tutor_profile_header(lines):
    """Remove 'Become a Tutor' — first occurrence is the header."""
    out = lines[:]
    for i, ln in enumerate(out):
        if '<a href="../../join.html">Become a Tutor</a>' in ln:
            del out[i]
            break
    return out

for f in EN_HEADER_FILES:
    edit(f, remove_en_header)
for d, f in LOCALIZED:
    edit(f"{d}/{f}", remove_localized_header)
for f in TUTOR_PROFILES:
    edit(f, remove_tutor_profile_header)

print("Files changed:", len(changes))
for c in changes:
    print("  -", c)
