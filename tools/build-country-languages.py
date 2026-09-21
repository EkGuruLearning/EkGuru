#!/usr/bin/env python3
"""Build the quality-labelled country → language list for the homepage.

Only VERIFIED and explicitly labelled PROVISIONAL relationships are emitted.
Agent-compiled/unsourced records stay in the internal research inventory.
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from lib.country_quality import RANK, classify  # noqa: E402

relations = json.loads(open("data/global/language-country-relations.json", encoding="utf-8").read())["relations"]
cache = json.loads(open("tools/_countries-cache.json", encoding="utf-8").read())
names = {
    c["cca2"]: (c.get("name") or {}).get("common") or c["cca2"]
    for c in cache
    if c.get("cca2")
}

# Deduplicate repeated relationship categories for the same country/language.
# Keep the strongest evidence state; a language can be both OFFICIAL and
# WIDELY_SPOKEN without appearing twice in the homepage panel.
strongest = {}
for row in relations:
    cc, language_id = row.get("country_id"), row.get("language_id")
    if not cc or len(cc) != 2 or not language_id:
        continue
    state = classify(row)
    if state == "RESEARCH_REQUIRED":
        continue
    key = (cc, language_id)
    current = strongest.get(key)
    if current is None or RANK[state] > RANK[current[0]]:
        strongest[key] = (state, row)

by = defaultdict(list)
for (cc, _language_id), (state, row) in strongest.items():
    label = row.get("language_name") or row.get("native_name")
    if not label:
        continue
    by[cc].append({
        "name": label,
        "native": row.get("native_name") or "",
        "code": row.get("iso_639_1") or row.get("iso_639_3") or "",
        "quality": state,
    })

items = []
for cc, langs in sorted(by.items(), key=lambda item: names.get(item[0], item[0])):
    langs.sort(key=lambda row: (-RANK[row["quality"]], row["name"]))
    if not langs:
        continue
    items.append({"cc": cc, "name": names.get(cc, cc), "langs": langs[:30]})

src = (
    "/* Generated from quality-gated country-language relations — do not hand-edit. */\n"
    "(function () {\n"
    '  "use strict";\n'
    "  window.EKGURU_COUNTRY_LANGS = %s;\n"
    "})();\n"
) % json.dumps(items, ensure_ascii=False, separators=(",", ":"))

path = "js/country-languages.js"
open(path, "w", encoding="utf-8").write(src)
print("wrote %s (%d sourced countries, %d bytes)" % (path, len(items), len(src)))
