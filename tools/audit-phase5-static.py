#!/usr/bin/env python3
"""Phase 5 §3/§9 — static interaction inventory + dead/hidden/unreachable UI sweep.

Walks every HTML page and classifies card-like blocks, finds dead links/buttons,
and flags misleading affordances. Produces:

  reports/phase5-interaction-inventory.json
  reports/hidden-unreachable-ui.json
  reports/phase5-dead-ui-report.json

Static analysis is the INPUT to the browser tests (test-card-interactions.py);
a final PASS requires the browser run. Run: python3 tools/audit-phase5-static.py
"""
import json, os, re, time
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

CARD_CLASSES = re.compile(r'\b(card|faq|tcard|hs-card|mkt|tile|tool-card|mcard|step|slot|'
                          r'panel|grid-item|feature|thumb)\b')
HOVER_TRANSFORM = re.compile(r'\.([a-z0-9 -]+):hover\{[^}]*transform[^}]*\}')

def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return ""

html_files = []
for base, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "reports", "tools", "live-sheets", "uploads")]
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(base, f))

dead_links = []     # href="#" / empty / javascript:
dead_buttons = []   # buttons with no id/type/onclick/data-*/aria-*
hidden_ui = []      # inline display:none / visibility / opacity:0 / pointer-events:none
cards = []          # card inventory
misleading = []     # hover-transform classes not attached to anchors

HOVER_CLASSES = set()
css = read("css/style.min.css")
for m in re.finditer(r'\.((?:[a-z0-9-]+\s*,\s*)*[a-z0-9-]+):hover\{[^}]*transform', css):
    HOVER_CLASSES.update(c.strip().lstrip(".") for c in m.group(1).split(","))

# classes that ARE real interactive controls — never "misleading"
INTERACTIVE = {"btn", "tcard", "pill", "chip", "chips", "slot", "nav", "chip-btn",
               "lang-btn", "cur-btn", "sched-slot", "bk-slot", "bk-x", "fab",
               "share-b", "to-top", "wa-float", "ac-item", "ac-all", "rev-more",
               "tz-toggle", "js-yt", "vid-link", "mkt", "burger", "menu", "close"}

for fp in html_files:
    rel = fp.replace(os.sep, "/")
    h = read(fp)
    if not h:
        continue

    # strip script/style so template strings are never misread as real markup
    h_scan = re.sub(r'<script\b.*?</script>', ' ', h, flags=re.S)
    h_scan = re.sub(r'<style\b.*?</style>', ' ', h_scan, flags=re.S)

    # ---- dead links ----
    for m in re.finditer(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>', h_scan, re.S):
        url, inner = m.group(1), m.group(2)
        if url in ("#", ""):
            tag = m.group(0)
            # JS-wired anti-spam mail links + the contact fab are not dead
            if re.search(r'data-email|data-mail|id="(contact-fab|join-mail)', tag):
                continue
            dead_links.append({"page": rel, "href": url,
                               "text": re.sub(r"<[^>]+>", "", inner).strip()[:40]})
        elif url.startswith("javascript:"):
            dead_links.append({"page": rel, "href": url[:40],
                               "text": re.sub(r"<[^>]+>", "", inner).strip()[:40]})

    # ---- dead buttons (no id, type, onclick, data-* attr) ----
    for m in re.finditer(r'<button\b([^>]*)>', h_scan):
        attrs = m.group(1)
        if not re.search(r'\b(id|type|onclick|data-|aria-)[a-z0-9-]*', attrs):
            dead_buttons.append({"page": rel, "attrs": attrs.strip()[:60]})

    # ---- hidden/unreachable (inline) ----
    for m in re.finditer(r'style="([^"]*)"', h_scan):
        st = m.group(1)
        for prop in ("display:none", "visibility:hidden", "opacity:0", "pointer-events:none"):
            if prop in st.replace(" ", ""):
                hidden_ui.append({"page": rel, "style": st[:80]})
                break

    # ---- card inventory ----
    # find the true extent of each card element via balanced tag counting
    def card_extent(src, start, tag):
        """Return the index just past the matching close tag of the element
        beginning at `start` (the '<' of the opening tag)."""
        i = start
        depth = 0
        open_re = re.compile(r'<' + tag + r'(\s|>)')
        close_re = re.compile(r'</' + tag + r'\s*>')
        for m in re.finditer(r'<(/?)' + tag + r'(\s[^>]*)?>', src[i:]):
            if m.group(1):
                depth -= 1
                if depth == 0:
                    return i + m.end()
            else:
                depth += 1
        return min(len(src), start + 4000)

    for m in re.finditer(r'<(a|div|li|article)\b[^>]*class="([^"]*)"', h_scan):
        tag, cls = m.group(1), m.group(2)
        if not CARD_CLASSES.search(cls):
            continue
        start = m.start()
        end = card_extent(h_scan, start, tag)
        seg = h_scan[start:end]
        anchors = re.findall(r'<a\b[^>]*href="([^"]+)"', seg)
        if tag == "a":
            cards.append({"page": rel, "class": cls, "pattern": "whole-anchor",
                          "anchors": anchors[:2]})
        else:
            stretched = 'tcard-link' in seg
            if stretched:
                cards.append({"page": rel, "class": cls, "pattern": "stretched-link",
                              "anchors": anchors[:2]})
            # FAQ Q&A blocks (<div class="faq"><b>Question</b><p>Answer</p></div>)
            # are informational; an inline reference link in the answer text is
            # correct and must not be treated as a title-only clickable card.
            elif 'faq' in cls and ('<b>' in seg or '<summary' in seg):
                cards.append({"page": rel, "class": cls, "pattern": "informational-faq",
                              "anchors": anchors[:2]})
            # A single action that is JS-wired (mailto etc.) is a control, not
            # a "card with only its title linked".
            elif len(anchors) == 1 and re.search(r'data-email|data-mail|data-mail-main', seg):
                cards.append({"page": rel, "class": cls, "pattern": "js-wired-action",
                              "anchors": anchors[:1]})
            elif len(anchors) == 1:
                cards.append({"page": rel, "class": cls, "pattern": "title-only-link",
                              "anchors": anchors[:1]})
            elif len(anchors) == 0:
                cards.append({"page": rel, "class": cls, "pattern": "no-link",
                              "anchors": []})
            else:
                cards.append({"page": rel, "class": cls, "pattern": "nested-actions",
                              "anchors": anchors[:3]})

    # ---- misleading affordance: hover-lift on a non-interactive element ----
    for cls in HOVER_CLASSES:
        if not cls or cls in INTERACTIVE:
            continue
        for m in re.finditer(r'<(div|li|span)\b[^>]*class="[^"]*\b' + re.escape(cls) + r'\b[^"]*"', h_scan):
            back = h_scan[max(0, m.start()-1500):m.start()]
            opens = len(re.findall(r'<a\b[^>]*>', back))
            closes = len(re.findall(r'</a>', back))
            if opens <= closes:
                misleading.append({"page": rel, "class": cls,
                                   "note": "hover-transform class on a non-interactive element"})

# summarize
from collections import Counter
pattern_count = Counter(c["pattern"] for c in cards)
by_page_pattern = {}
for c in cards:
    if c["pattern"] not in ("whole-anchor",):
        by_page_pattern.setdefault(c["page"], Counter())[c["pattern"]] += 1

inventory = {
    "generated": NOW,
    "totalCardInstances": len(cards),
    "byPattern": dict(pattern_count),
    "cards": cards,
    "misleadingAffordances": misleading,
    "summary": {
        "deadLinks": len(dead_links),
        "deadButtons": len(dead_buttons),
        "hiddenInline": len(hidden_ui),
        "misleadingAffordances": len(misleading),
    },
}
json.dump(inventory, open("reports/phase5-interaction-inventory.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
json.dump({"generated": NOW, "deadLinks": dead_links, "deadButtons": dead_buttons,
           "hiddenInline": hidden_ui},
          open("reports/hidden-unreachable-ui.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
json.dump({"generated": NOW,
           "deadLinks": len(dead_links), "deadButtons": len(dead_buttons),
           "hiddenInline": len(hidden_ui),
           "misleadingAffordances": len(misleading),
           "details": {"deadLinks": dead_links, "deadButtons": dead_buttons,
                       "hiddenInline": hidden_ui, "misleadingAffordances": misleading}},
          open("reports/phase5-dead-ui-report.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

print("cards:", len(cards), dict(pattern_count))
print("deadLinks:", len(dead_links), "| deadButtons:", len(dead_buttons),
      "| hiddenInline:", len(hidden_ui), "| misleading:", len(misleading))
for m in misleading[:10]:
    print("  MISLEADING", m["page"], m["class"])
for d in dead_links[:10]:
    print("  DEADLINK", d["page"], d["href"], d["text"])
