#!/usr/bin/env python3
"""Build the time-and-days pages and their generated JS from data/time/*.json.

Same principle as the numbers tool: the visitor types an ENGLISH day, month
or time word and gets the word back in the target language's own script and
real usage. The whole point is that the answer is the *right* word, so the
data is the source of truth and the table + tool are generated from it.

Only the three tables (days, months, time words) are generated, and only
between their own markers. The rest of the page — head, prose, schema,
chrome — is hand-owned, because apply-ultra decorates pages and a generator
that rewrites a whole page fights that decoration on every build.

`--check` fails when the output is stale, so nothing can drift.

  python3 tools/build-time-pages.py
  python3 tools/build-time-pages.py --check
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/time"

PAGES = [
    {
        "slug": "days-and-months-in-punjabi",
        "file": "punjabi.json",
        "title": "Punjabi Days, Months and Time — Days of the Week in Gurmukhi | EkGuru",
        "h1": "Punjabi days, months and time words",
        "desc": ("Every day of the week, month of the year and everyday time word in Punjabi, with "
                 "Gurmukhi writing and pronunciation. Type an English word and get it back in Punjabi."),
        "lede": ("All seven days, all twelve months and the time words you use every day, in Punjabi "
                 "Gurmukhi. Type any English day, month or time word below and it returns the Punjabi "
                 "word in its own script, straight away."),
        "html_lang": "pa",
        "script_name": "Gurmukhi",
    },
    {
        "slug": "days-and-months-in-marathi",
        "file": "marathi.json",
        "title": "Marathi Days, Months and Time — Days of the Week in Devanagari | EkGuru",
        "h1": "Marathi days, months and time words",
        "desc": ("Every day of the week, month of the year and everyday time word in Marathi, with "
                 "Devanagari writing and pronunciation. Type an English word and get it back in Marathi."),
        "lede": ("All seven days, all twelve months and the time words you use every day, in Marathi "
                 "Devanagari. Type any English day, month or time word below and it returns the Marathi "
                 "word in its own script, straight away."),
        "html_lang": "mr",
        "script_name": "Devanagari",
    },
    {
        "slug": "days-and-months-in-gujarati",
        "file": "gujarati.json",
        "title": "Gujarati Days, Months and Time — Days of the Week in Gujarati Script | EkGuru",
        "h1": "Gujarati days, months and time words",
        "desc": ("Every day of the week, month of the year and everyday time word in Gujarati, with "
                 "Gujarati writing and pronunciation. Type an English word and get it back in Gujarati."),
        "lede": ("All seven days, all twelve months and the time words you use every day, in Gujarati "
                 "script. Type any English day, month or time word below and it returns the Gujarati "
                 "word in its own script, straight away."),
        "html_lang": "gu",
        "script_name": "Gujarati",
    },
    {
        "slug": "days-and-months-in-kannada",
        "file": "kannada.json",
        "title": "Kannada Days, Months and Time — Days of the Week in Kannada Script | EkGuru",
        "h1": "Kannada days, months and time words",
        "desc": ("Every day of the week, month of the year and everyday time word in Kannada, with "
                 "Kannada writing and pronunciation. Type an English word and get it back in Kannada."),
        "lede": ("All seven days, all twelve months and the time words you use every day, in Kannada "
                 "script. Type any English day, month or time word below and it returns the Kannada "
                 "word in its own script, straight away."),
        "html_lang": "kn",
        "script_name": "Kannada",
    },
    {
        "slug": "days-and-months-in-telugu",
        "file": "telugu.json",
        "title": "Telugu Days, Months and Time — Days of the Week in Telugu Script | EkGuru",
        "h1": "Telugu days, months and time words",
        "desc": ("Every day of the week, month of the year and everyday time word in Telugu, with "
                 "Telugu writing and pronunciation. Type an English word and get it back in Telugu."),
        "lede": ("All seven days, all twelve months and the time words you use every day, in Telugu "
                 "script. Type any English day, month or time word below and it returns the Telugu "
                 "word in its own script, straight away."),
        "html_lang": "te",
        "script_name": "Telugu",
    },
    {
        "slug": "days-and-months-in-urdu",
        "file": "urdu.json",
        "title": "Urdu Days, Months and Time — Days of the Week in Urdu (Arabic Script) | EkGuru",
        "h1": "Urdu days, months and time words",
        "desc": ("Every day of the week, month of the year and everyday time word in Urdu, with "
                 "Arabic writing and pronunciation. Type an English word and get it back in Urdu."),
        "lede": ("All seven days, all twelve months and the time words you use every day, in Urdu "
                 "Arabic script. Type any English day, month or time word below and it returns the "
                 "Urdu word in its own script, straight away."),
        "html_lang": "ur",
        "script_name": "Arabic",
    },
]


def load(spec) -> dict:
    return json.loads((DATA / spec["file"]).read_text(encoding="utf-8"))


# ----------------------------------------------------------------------
# js/time-data.js — inline, so the answer appears on the first keystroke.
# ----------------------------------------------------------------------
def render_js() -> str:
    langs = {}
    for spec in PAGES:
        d = load(spec)
        langs[d["language"]] = {
            "name": d["languageName"],
            "script": d["script"],
            "days": d["days"],
            "months": d["months"],
            "desi_months": d["desi_months"],
            "time_words": d["time_words"],
            "page": "/" + spec["slug"] + "/",
        }
    body = json.dumps(langs, ensure_ascii=False, indent=1)
    return (
        "/* GENERATED by tools/build-time-pages.py from data/time/*.json.\n"
        "   Do not hand-edit: run the tool. */\n"
        "(function (root) {\n"
        '  "use strict";\n'
        "  var LANGS = " + body + ";\n"
        "\n"
        "  root.EkGuruTime = { langs: LANGS };\n"
        "})(typeof window !== \"undefined\" ? window : globalThis);\n"
    )


# ----------------------------------------------------------------------
# Tables
# ----------------------------------------------------------------------
def rows(items, lang: str) -> str:
    out = []
    for x in items:
        also = ""
        if x.get("also"):
            also = ' <span class="alt">or ' + " / ".join(x["also"]) + "</span>"
        out.append(
            f'<tr><td class="en">{x["en"]}</td>'
            f'<td class="h" lang="{lang}">{x["word"]}</td>'
            f'<td class="rom">{x["roman"]}{also}</td></tr>'
        )
    return "".join(out)


def table(spec: dict, d: dict, kind: str) -> str:
    lang = d["language"]
    if kind == "days":
        head = ("<th>English</th>"
                f'<th>{spec["script_name"]} day</th><th>Say it</th>')
        body = rows(d["days"], lang)
    elif kind == "months":
        head = ("<th>English</th>"
                f'<th>{spec["script_name"]} month</th><th>Say it</th>')
        body = rows(d["months"], lang)
    elif kind == "time_words":
        head = ("<th>English</th>"
                f'<th>{spec["script_name"]} word</th><th>Say it</th>')
        body = rows(d["time_words"], lang)
    elif kind == "desi":
        head = ("<th>English</th>"
                f'<th>{spec["script_name"]} month</th><th>Say it</th>')
        body = rows(d["desi_months"], lang)
    return ('<table class="ex"><thead><tr>' + head + "</tr></thead><tbody>"
            + body + "</tbody></table>")


MARKERS = [("days", "days"), ("months", "months"), ("time", "time_words"), ("desi", "desi")]


def update_page(spec: dict, check: bool) -> str | None:
    d = load(spec)
    path = ROOT / spec["slug"] / "index.html"
    if not path.exists():
        return f"MISSING {spec['slug']}/index.html"
    html = path.read_text(encoding="utf-8")
    for _, kind in MARKERS:
        start = f"<!-- ekguru:time-{spec['slug']}-{kind}:start -->"
        end = f"<!-- ekguru:time-{spec['slug']}-{kind}:end -->"
        if start not in html or end not in html:
            return f"{spec['slug']}/index.html is missing the {kind} markers"
        a = html.index(start) + len(start)
        b = html.index(end)
        want = "\n" + table(spec, d, kind) + "\n"
        if html[a:b] != want:
            if check:
                return (f"STALE {kind} table in {spec['slug']}/index.html — "
                        "run: python3 tools/build-time-pages.py")
            html = html[:a] + want + html[b:]
    path.write_text(html, encoding="utf-8")
    return None


def main() -> int:
    check = "--check" in sys.argv
    problems = []

    js = render_js()
    js_path = ROOT / "js/time-data.js"
    if check:
        if not js_path.exists() or js_path.read_text(encoding="utf-8") != js:
            problems.append("STALE js/time-data.js — run: python3 tools/build-time-pages.py")
    else:
        js_path.write_text(js, encoding="utf-8")

    for spec in PAGES:
        err = update_page(spec, check)
        if err:
            problems.append(err)

    if check:
        if problems:
            print("\n".join(problems))
            return 1
        print("ok    time data and tables are current")
        return 0
    print(f"wrote js/time-data.js and {len(PAGES)} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
