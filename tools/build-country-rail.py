#!/usr/bin/env python3
"""The homepage country rail — 194 countries, two rows, opposite directions.

Prakash's requirement: every country is on the home page, each item a plain
anchor to that country's real page, with its actual languages under the name
(two lines per item). Two rows run in opposite directions continuously;
hover and focus pause them, prefers-reduced-motion stops them, and the pace
is slow enough to read.

Source of truth (no invented facts):
  data/language-inventory/sovereign-194.json   the 194 sovereign countries
  data/global/language-country-relations.json  the researched language links
  world-languages/<slug>/                      the pages that must exist

The summary is at most two language names: the country's national language
first, then a widely spoken one (or the next national). If a country has
relations of no usable kind, the item shows the country name only — an empty
second line is not filler.

The rail is static: each row's track carries its items twice (the duplicate
is aria-hidden), so the loop is seamless with zero JavaScript and works with
scripting off. Idempotent: run twice, second run changes nothing.

Run:  python3 tools/build-country-rail.py [--check]
"""
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# The cca2 -> slug table belongs to tools/build-country-language-pages.py,
# which owns the country pages; import it so the rail can never drift from
# the pages it links to.
_spec = importlib.util.spec_from_file_location(
    "bclp", os.path.join(ROOT, "tools", "build-country-language-pages.py"))
_bclp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bclp)
SLUGS = _bclp.SLUGS

HOME = "index.html"
START = "<!-- ekguru:countries-rail:start -->"
END = "<!-- ekguru:countries-rail:end -->"

# Relationship types, most to least representative of a country's everyday
# languages. Anything else (INDIGENOUS, MIGRANT, ...) is a fallback.
PREF = {"NATIONAL": 0, "WIDELY_SPOKEN": 1}


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def load(p, default=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def summary_for(rels):
    """Up to two language names, by relationship type."""
    if not rels:
        return ""
    ranked = sorted(rels, key=lambda r: (PREF.get(r.get("kind"), 9),
                                         r.get("language_name") or ""))
    picked = []
    for r in ranked:
        name = (r.get("language_name") or "").strip()
        if name and name not in picked:
            picked.append(name)
        if len(picked) == 2:
            break
    return " · ".join(picked)


def build_rows():
    sov = (load("data/language-inventory/sovereign-194.json") or {}).get("countries") or []
    rels = (load("data/global/language-country-relations.json") or {}).get("relations") or []

    by_country = {}
    for r in rels:
        cc = r.get("country_id")
        if cc:
            by_country.setdefault(cc, []).append(
                {"kind": (r.get("relationship_id") or "").split(":")[-1],
                 "language_name": r.get("language_name")})

    items = []
    for c in sov:
        cc = c.get("cca2")
        slug = SLUGS.get(cc)
        if not slug or not os.path.exists("world-languages/%s/index.html" % slug):
            continue                      # never a link to a page that is not there
        name = esc(c.get("name") or "")
        if not name:
            continue
        summ = summary_for(by_country.get(cc))
        items.append((name, summ, "world-languages/%s/" % slug))

    if not items:
        raise SystemExit("ERROR: no country items could be built")
    return items


def rail_html(items):
    half = (len(items) + 1) // 2
    rows = [items[:half], items[half:]]
    out = [START, '\n<section class="ct-rail" aria-label="Courses by country — the 194 countries we cover">']
    for i, row in enumerate(rows):
        direction = "left" if i == 0 else "right"
        block = "".join(
            '<a class="ct-item" href="%s"><b>%s</b>%s</a>'
            % (href, name,
               ('<small>%s</small>' % esc(s)) if s else "")
            for name, s, href in row)
        out.append('  <div class="ct-rail-row" data-dir="%s"><div class="ct-rail-track">'
                   % direction)
        out.append(block)
        # The seam: the same cards again, hidden from readers and crawlers,
        # so the -50% loop joins with no jump.
        out.append('<div class="ct-dup" aria-hidden="true">%s</div>' % block)
        out.append('</div></div>')
    out.append('</section>')
    out.append(END)
    return "\n".join(out)


def main():
    check = "--check" in sys.argv
    items = build_rows()
    new = rail_html(items)

    with open(HOME, encoding="utf-8") as f:
        html = f.read()

    if START in html and END in html:
        i, j = html.index(START), html.index(END) + len(END)
        old = html[i:j]
        out = html[:i] + new + html[j:]
    else:
        anchor = "<!-- ekguru:languages-home:start"
        pos = html.find(anchor)
        if pos < 0:
            raise SystemExit("ERROR: %s: no rail markers and no anchor" % HOME)
        out = html[:pos] + new + "\n" + html[pos:]

    if out == html:
        print("country rail: current (%d countries, two rows)" % len(items))
        return 0
    if check:
        print("STALE: %s needs tools/build-country-rail.py" % HOME)
        return 1
    with open(HOME, "w", encoding="utf-8") as f:
        f.write(out)
    print("country rail: %d countries written to %s (rows of %d/%d)"
          % (len(items), HOME, (len(items) + 1) // 2, len(items) - (len(items) + 1) // 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
