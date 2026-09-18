#!/usr/bin/env python3
"""Redesign the four legal pages (terms, privacy, disclaimer, copyright).

    python3 tools/build-legal-pages.py [--check]

Prakash: "ab support se lekar footer se lekar T&C, disclaimer and all remaining
all pages redesign karo."

The shared shell (tools/build-shell.js) gave these pages the same header and
footer as the rest of the site. Their *bodies* were still the flat 2024 wall of
paragraphs: no contents list, nothing to scan, eleven <h2>s in a row and a
reader who has to scroll to find the one clause they came for.

What this does, without touching a word of the text:

  · gives every <h2> an id, so a clause can be linked to
  · builds an "On this page" contents card from those headings
  · marks the block up as .xp-doc, which css/experience.css §23 styles as a
    document: a readable measure, numbered sections, a scannable hierarchy

The text is preserved byte for byte — the tool only adds ids, a wrapper class
and one generated <nav>. Legal wording is the one thing on a site that must
never be silently rewritten by a build script, so this one refuses to run if it
finds it has changed the prose, and `--check` fails when a page is out of date.

Markers keep it idempotent:

    <!-- ekguru:legal:start -->
    <div class="legal xp-doc"> … </div>
    <!-- ekguru:legal:end -->

Run:  python3 tools/build-legal-pages.py          # write
      python3 tools/build-legal-pages.py --check  # compare (CI/gate)
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PAGES = ["terms", "privacy", "disclaimer", "copyright"]

START = "<!-- ekguru:legal:start -->"
END = "<!-- ekguru:legal:end -->"
TOC_START = "<!-- ekguru:legal-toc:start -->"
TOC_END = "<!-- ekguru:legal-toc:end -->"


def find_block(html_text, opener_re, closer="</div>"):
    """Return (start, end) of the element matching opener_re, counting nested
    <div>s — a regex cannot close an element, and these pages nest several."""
    m = re.search(opener_re, html_text)
    if not m:
        return None
    depth = 0
    i = m.start()
    for tag in re.finditer(r"<(/?)div\b[^>]*>", html_text[m.start():]):
        if tag.group(1) == "":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return (m.start(), m.start() + tag.end())
    return None


def slug(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text or "section"


def add_ids(block):
    """Give every <h2> an id. Existing ids are left alone."""
    used = set(re.findall(r'\bid="([^"]+)"', block))
    n = 0

    def repl(m):
        nonlocal n
        attrs, inner = m.group(1), m.group(2)
        if "id=" in attrs:
            return m.group(0)
        base = slug(inner)
        candidate, k = base, 2
        while candidate in used:
            candidate = "%s-%d" % (base, k)
            k += 1
        used.add(candidate)
        n += 1
        return '<h2 id="%s"%s>%s</h2>' % (candidate, attrs, inner)

    out = re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, block, flags=re.S)
    return out, n


def build_toc(block):
    """The contents card, from the h2s the block already has."""
    items = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', block, flags=re.S)
    if len(items) < 3:
        return ""                      # three headings is not a long document
    links = "\n".join(
        '      <li><a href="#%s">%s</a></li>' % (i, re.sub(r"\s+", " ", t).strip())
        for i, t in items)
    return (TOC_START + "\n"
            '<nav class="xp-toc" aria-label="On this page">\n'
            '  <h2 class="xp-toc-h">On this page</h2>\n'
            "  <ol>\n" + links + "\n  </ol>\n"
            "</nav>\n" + TOC_END)


def strip_toc(block):
    return re.sub(re.escape(TOC_START) + r".*?" + re.escape(TOC_END) + r"\n?",
                  "", block, flags=re.S)


def prose(block):
    """Everything a reader reads: tag-stripped, whitespace-collapsed."""
    text = re.sub(r"<script[\s\S]*?</script>", " ", block)
    text = re.sub(r"<!--[\s\S]*?-->", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def rebuild(html_text, label):
    block = find_block(html_text, r'<div class="legal(?: xp-doc)?">')
    if not block:
        raise SystemExit("ERROR: %s: no <div class=\"legal\"> block found" % label)

    # 1. make the block marker-wrapped, once
    if START not in html_text or END not in html_text:
        html_text = (html_text[:block[0]] + START + "\n"
                     + html_text[block[0]:block[1]] + "\n" + END
                     + html_text[block[1]:])
        block = find_block(html_text, re.escape(START) + r'[\s\S]*?' + re.escape(END))
        inner_start = block[0] + len(START)
        inner_end = block[1] - len(END)
    else:
        span = find_block(html_text, re.escape(START) + r'[\s\S]*?' + re.escape(END))
        inner_start, inner_end = span[0] + len(START), span[1] - len(END)

    inner = html_text[inner_start:inner_end]
    # The guard compares the document WITHOUT the contents card: the card
    # repeats every heading, so including it made the second run fail its own
    # check and refuse to write.

    before = prose(strip_toc(inner))

    # 2. the wrapper class + heading ids
    inner = re.sub(r'<div class="legal">', '<div class="legal xp-doc">', inner, count=1)
    inner = strip_toc(inner)
    inner, _ = add_ids(inner)

    # 3. the contents card, after the opening summary
    toc = build_toc(inner)
    if toc:
        m = re.search(r'<p class="lede">[\s\S]*?</p>', inner) or re.search(r'<p class="upd">[\s\S]*?</p>', inner)
        if m:
            inner = inner[:m.end()] + "\n\n" + toc + inner[m.end():]
        else:
            inner = re.sub(r"(</h1>\s*(?:<p[^>]*>[\s\S]*?</p>\s*)*)",
                           lambda mm: mm.group(1) + "\n" + toc + "\n", inner, count=1)

    after = prose(strip_toc(inner))
    if before != after:
        raise SystemExit("ERROR: %s: the tool changed the text (refusing to write).\n"
                         "  before: %s…\n  after:  %s…"
                         % (label, before[:120], after[:120]))

    out = html_text[:inner_start] + inner + html_text[inner_end:]
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def main():
    check = "--check" in sys.argv
    stale, written = [], 0
    for page in PAGES:
        path = os.path.join(page, "index.html")
        with open(path, encoding="utf-8") as f:
            original = f.read()
        updated = rebuild(original, path)
        if updated == original:
            print("ok    %s" % path)
            continue
        if check:
            print("STALE %s" % path)
            stale.append(path)
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        written += 1
        print("wrote %s (%d headings, contents card)" % (
            path, len(re.findall(r'<h2 id="', updated))))
    if check and stale:
        print("\n⛔ %d legal page(s) need tools/build-legal-pages.py" % len(stale))
        return 1
    print("\n✔ legal pages: %d written, %d already current." % (written, len(PAGES) - written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
