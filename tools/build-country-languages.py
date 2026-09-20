#!/usr/bin/env python3
"""Compact country → language list for the homepage marquee.

Source of truth: data/global/language-country-relations.json
Country names: tools/_countries-cache.json
"""
import json
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

rel = json.loads(open("data/global/language-country-relations.json", encoding="utf-8").read())["relations"]
cache = json.loads(open("tools/_countries-cache.json", encoding="utf-8").read())
names = {c["cca2"]: (c.get("name") or {}).get("common") or c["cca2"]
         for c in cache if c.get("cca2")}

lang_name = {}
for row in rel:
    code = row.get("iso_639_1") or row.get("iso_639_3")
    n = row.get("language_name") or row.get("native_name")
    if code and n and code not in lang_name:
        lang_name[code] = n

by = defaultdict(lambda: {"name": "", "langs": []})
seen = defaultdict(set)
for row in rel:
    cc = row.get("country_id")
    if not cc or len(cc) != 2:
        continue
    code = row.get("iso_639_1") or row.get("iso_639_3") or ""
    label = lang_name.get(code) or row.get("language_name") or code
    if not label or label in seen[cc]:
        continue
    seen[cc].add(label)
    by[cc]["langs"].append(label)
    by[cc]["name"] = names.get(cc, cc)

items = []
for cc, info in sorted(by.items(), key=lambda kv: kv[1]["name"]):
    langs = info["langs"][:12]
    if not langs:
        continue
    items.append({"cc": cc, "name": info["name"], "langs": langs})

src = (
    "/* Generated from data/global/language-country-relations.json — do not hand-edit. */\n"
    "(function () {\n"
    '  "use strict";\n'
    "  window.EKGURU_COUNTRY_LANGS = %s;\n"
    "})();\n"
) % json.dumps(items, ensure_ascii=False, separators=(",", ":"))

path = "js/country-languages.js"
open(path, "w", encoding="utf-8").write(src)
print("wrote %s (%d countries, %d bytes)" % (path, len(items), len(src)))
