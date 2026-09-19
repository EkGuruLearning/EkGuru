#!/usr/bin/env python3
"""EkGuru — Learn/Tools quality baseline (static crawl).

Walks learn/, toolbox/, daily-hindi/, answers/ and scores each page on
the dimensions the ULTRA command lists: title, H1, answer/depth, examples,
practice, tool linkage, internal links, originality signals, metadata,
schema, accessibility, mobile, performance, freshness.

This is STATIC scoring only (an internal quality score, NOT a Google
ranking score). The real-browser half (does each tool actually work) is
tools/test-tools-browser.py. Output: reports/learn-tools-quality-baseline.json
"""
import json
import os
import re
import time
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = ["learn", "toolbox", "daily-hindi", "answers", "materials"]

DEVANAGARI = re.compile(r"[\u0900-\u097F]")
WORD = re.compile(r"[A-Za-z\u0900-\u097F0-9']+")

PRACTICE_HINTS = [
    "practise", "practice", "try it", "exercise", "quick check", "quiz",
    "test yourself", "say it aloud", "write it", "do this", "task",
    "mistake", "check", "complete", "review", "drill",
]
TOOL_HINTS = ["toolbox/", "flashcard", "quiz", "typing", "phrasebook",
              "alphabet explorer", "numbers tool", "level test"]
TUTOR_HINTS = ["tutor", "guru", "trial lesson"]


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta_desc = ""
        self.canonical = ""
        self.h1s = []
        self.h2s = []
        self.headings = 0
        self.links = []
        self.schema = 0
        self.images = 0
        self.img_alt = 0
        self.in_title = False
        self._stack = []
        self.script_depth = 0
        self.style_depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script":
            self.script_depth += 1
            if a.get("type") == "application/ld+json":
                self.schema += 1
        if tag == "style":
            self.style_depth += 1
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1s.append("")
        if tag == "h2":
            self.h2s.append("")
        if tag in ("h1", "h2", "h3", "h4"):
            self.headings += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.images += 1
            if a.get("alt"):
                self.img_alt += 1
        if tag == "meta":
            if a.get("name", "").lower() == "description":
                self.meta_desc = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href", "")
        if tag in ("h1", "h2"):
            self._stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "script" and self.script_depth:
            self.script_depth -= 1
        if tag == "style" and self.style_depth:
            self.style_depth -= 1
        if tag == "title":
            self.in_title = False
        if tag in ("h1", "h2") and self._stack and self._stack[-1] == tag:
            self._stack.pop()

    def handle_data(self, data):
        if self.script_depth or self.style_depth:
            return
        if self.in_title:
            self.title += data
        if self.h1s and self._last_open() == "h1":
            self.h1s[-1] += data
        if self.h2s and self._last_open() == "h2":
            self.h2s[-1] += data

    def _last_open(self):
        return self._stack[-1] if self._stack else ""


def analyze(path):
    try:
        raw = open(path, encoding="utf-8").read()
    except Exception:
        return None
    p = P()
    try:
        p.feed(raw)
    except Exception:
        pass
    # strip tags for body text
    body = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    text = re.sub(r"\s+", " ", body).strip()
    words = len(WORD.findall(text))
    dev = DEVANAGARI.findall(text)
    dev_unique = len(set(dev))

    h1 = p.h1s[0].strip() if p.h1s else ""
    internal = [l for l in p.links if l.startswith("/") or l.startswith(".")]
    external = [l for l in p.links if l.startswith("http") and "ekguru" not in l]
    tool_links = [l for l in p.links if "toolbox/" in l]
    learn_links = [l for l in p.links if "/learn/" in l or l.startswith("../")]
    tutor_links = [l for l in p.links if "tutor" in l and "tutorial" not in l]

    lowered = text.lower()
    practice_hits = sum(1 for h in PRACTICE_HINTS if h in lowered)
    has_audio = "audio" in lowered or "<audio" in raw.lower()
    has_table = "<table" in raw.lower()
    has_code = "<code" in raw.lower() or "<pre" in raw.lower()

    return {
        "title": p.title.strip(),
        "h1": h1,
        "meta_description": p.meta_desc.strip(),
        "canonical": p.canonical,
        "words": words,
        "headings": p.headings,
        "h2_count": len(p.h2s),
        "devanagari_chars": len(dev),
        "devanagari_unique": dev_unique,
        "links_total": len(p.links),
        "links_internal": len(internal),
        "links_external": len(external),
        "links_tool": len(tool_links),
        "links_learn": len(learn_links),
        "links_tutor": len(tutor_links),
        "schema_blocks": p.schema,
        "images": p.images,
        "images_with_alt": p.img_alt,
        "practice_hints": practice_hits,
        "has_audio": has_audio,
        "has_table": has_table,
        "has_code": has_code,
    }


def score(a):
    """Internal quality score 0-100. NOT a Google ranking score."""
    s = 0
    if a["title"] and a["title"] != a["h1"]:
        s += 5
    if a["h1"]:
        s += 5
    if a["meta_description"]:
        s += 5
    if a["canonical"]:
        s += 3
    if a["words"] >= 1200:
        s += 10
    elif a["words"] >= 500:
        s += 6
    elif a["words"] >= 250:
        s += 3
    if a["devanagari_unique"] >= 20:
        s += 10
    elif a["devanagari_unique"] >= 5:
        s += 6
    if a["headings"] >= 4:
        s += 8
    elif a["headings"] >= 2:
        s += 4
    if a["practice_hints"] >= 3:
        s += 10
    elif a["practice_hints"] >= 1:
        s += 6
    if a["links_tool"] >= 1:
        s += 8
    if a["links_learn"] >= 1:
        s += 5
    if a["links_tutor"] >= 1:
        s += 4
    if a["links_internal"] >= 5:
        s += 7
    elif a["links_internal"] >= 2:
        s += 4
    if a["schema_blocks"] >= 1:
        s += 5
    if a["images_with_alt"] >= a["images"] and a["images"] > 0:
        s += 4
    if a["has_table"]:
        s += 4
    if a["has_audio"]:
        s += 3
    if a["has_code"]:
        s += 2
    return min(100, s)


def grade(score, words):
    if score >= 75 and words >= 800:
        return "A"
    if score >= 55:
        return "B"
    if score >= 35:
        return "C"
    if words < 120 and score < 30:
        return "D"
    return "C"


def kind_of(rel):
    if rel.startswith("toolbox/"):
        return "tool"
    if rel.startswith("learn/paths/"):
        return "path"
    if rel.startswith("learn/practice/"):
        return "practice"
    if rel.startswith("learn/"):
        return "learn"
    if rel.startswith("daily-hindi/"):
        return "daily"
    if rel.startswith("answers/"):
        return "answer"
    return "other"


def main():
    out = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": "Static internal quality baseline only — not a Google ranking score. "
                "Real-browser tool tests live in reports/tool-qa.json.",
        "pages": [],
        "summary": {},
    }
    for d in SCAN_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for dirpath, dirs, files in os.walk(base):
            if "index.html" not in files:
                continue
            rel = os.path.relpath(os.path.join(dirpath, "index.html"), ROOT)
            a = analyze(os.path.join(dirpath, "index.html"))
            if not a:
                continue
            sc = score(a)
            rec = {
                "url": "/" + rel.replace("index.html", ""),
                "kind": kind_of(rel),
                "grade": grade(sc, a["words"]),
                "score": sc,
                **a,
            }
            out["pages"].append(rec)

    by_kind = {}
    for p in out["pages"]:
        by_kind.setdefault(p["kind"], {"count": 0, "grades": {}, "total_words": 0, "avg_score": 0})
        by_kind[p["kind"]]["count"] += 1
        by_kind[p["kind"]]["grades"][p["grade"]] = by_kind[p["kind"]]["grades"].get(p["grade"], 0) + 1
        by_kind[p["kind"]]["total_words"] += p["words"]
        by_kind[p["kind"]]["avg_score"] += p["score"]
    for k, v in by_kind.items():
        if v["count"]:
            v["avg_score"] = round(v["avg_score"] / v["count"], 1)

    grades = {}
    for p in out["pages"]:
        grades[p["grade"]] = grades.get(p["grade"], 0) + 1
    out["summary"] = {
        "pages": len(out["pages"]),
        "grades": grades,
        "by_kind": by_kind,
        "weakest": sorted(out["pages"], key=lambda x: x["score"])[:20],
        "thinnest_by_words": sorted(out["pages"], key=lambda x: x["words"])[:15],
    }
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    with open(os.path.join(ROOT, "reports", "learn-tools-quality-baseline.json"), "w") as f:
        json.dump(out, f, indent=2)
    # admin-consumable single source of truth: window.EKGURU_QUALITY
    js = ("/* Generated by tools/learn-tools-audit.py — do not hand-edit.\n"
          "   Internal content-quality data consumed by admin Learn Ops. */\n"
          "window.EKGURU_QUALITY = " + json.dumps(out, ensure_ascii=False) + ";\n")
    with open(os.path.join(ROOT, "js", "learn-quality.js"), "w", encoding="utf-8") as f:
        f.write(js)
    print("wrote js/learn-quality.js (%d pages)" % len(out["pages"]))
    print(json.dumps(out["summary"], indent=2))


if __name__ == "__main__":
    main()
