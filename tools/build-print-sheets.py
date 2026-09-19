#!/usr/bin/env python3
"""EkGuru — WHICH PAGES PRINT AS A SHEET (and what exactly prints).

Prakash: "print worksheet pura page hi print karti hai, par humein sirf
worksheet hi print karni hai."

css/experience.css §27 does the printing. It cannot know, by itself, which
element on a page IS the sheet — that depends on the page. This tool marks it:

  · <body data-print="sheet">        this page prints as a sheet, not a page
  · the sheet element gets           data-print-target

Marked automatically, from what the page actually contains:

  · a worksheet builder (#ws-app) — the ten languages' worksheet pages. The
    sheet inside it is #w-sheet, which js/hindi-tools.js fills; the controls
    that build it are not printed.
  · a printable guide (.art on the /materials/ pages) — 40-odd charts and
    revision sheets whose whole point is a piece of paper.

and it loads js/print-sheet.js on those pages. As of this round it also bakes
a real SAMPLE SHEET into every worksheet page: `#ws-app` used to be empty until
a script filled it, so a reader with JavaScript off — or a browser that had not
finished booting — had nothing inside the print target and the print fell back
to the whole page. The sample is five questions from that language's own quiz
bank, marked with <!-- ekguru:sample-sheet -->, replaced in place when the
reader builds their own. A stylesheet can only hide what
is in the file; a worksheet is assembled in the browser when the reader clicks
"Make worksheet", so nothing in the file can be marked as the paper. The script
clones the finished sheet into #ekguru-print-root on beforeprint, which is the
one thing that makes "print only the worksheet" true even when the page around
it is a full page of navigation, controls and notes.

Everything else keeps normal printing: §27 still turns the chrome off, so a
lesson or an answer prints its content and nothing else either.

IDEMPOTENT: the body attribute and the target are set once. Run it twice and
the second run writes nothing.

Run:  python3 tools/build-print-sheets.py [--check]
      --check exits 1 listing pages that are not marked yet (CI / build-all)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SKIP_DIRS = {".git", "node_modules", "images", "css", "js", "data", "reports",
             "docs", "templates", "research", "tools"}
MARK = "data-print"

# The sheet, per page kind. A page is only a sheet when printing it is the
# point of the page: the ten worksheet builders, and the printed guides under
# /materials/ that carry their own Print button. Lessons, answers and hubs
# print as content with the chrome off — they are not sheets.
# Attribute-order independent: some pages carry data-print-target before id,
# and the old regex silently skipped those pages.
WS_APP = re.compile(r'<div (?=[^>]*\bid="ws-app")[^>]*>')
ART = re.compile(r'<div\b[^>]*\bclass="[^"]*\bart\b[^"]*"[^>]*>')


def judge(path, html):
    """(the target tag, kind) for this page, or None.

    The target depends on the KIND of page, not on what happens to come first
    in the file: a worksheet page prints the worksheet builder (its controls
    are hidden and #w-sheet prints), a printable guide prints the article.
    """
    if WS_APP.search(html):
        return WS_APP, "worksheet builder"
    if "materials/" in path and re.search(r"window\.print\s*\(\s*\)", html):
        m = ART.search(html)   # class="art", or "art pw-legacy" once layered
        if m:
            return ART, "printed guide"
    return None


SAMPLE_MARK = "<!-- ekguru:sample-sheet -->"
BANK_OF = {"hindi": "hindi"}          # js/<slug>-quiz-bank.js

# Which languages have a worksheet page, and which bank file holds the
# questions. The page names the language in data-topic="lang-<slug>"; the
# Hindi page is the original and its bank is not named after a slug.
BANK_NAME = re.compile(r'data-topic="lang-([a-z]+)"')


def json_object(src, marker):
    """The JS object assigned to `marker`, without eval.

    The generated banks are `window.EKGURU_X_QUIZ = {json};` followed by two
    more statements, so a regex to the end of the file does not work and a
    brace matcher does. Strings are skipped so a `}` inside a question — and
    there are plenty — cannot end the object early.
    """
    i = src.find(marker)
    if i < 0:
        return None
    i = src.find("{", i)
    if i < 0:
        return None
    depth, j, in_str, esc = 0, i, False, False
    while j < len(src):
        c = src[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                try:
                    import json
                    return json.loads(src[i:j + 1])
                except Exception:
                    return None
        j += 1
    return None


def sample_questions(path):
    """Five questions from the page's own quiz bank, or None.

    A worksheet page prints `[data-print-target]` = #ws-app. With scripting
    off, that element held nothing at all, so the browser had no sheet to
    print and fell back to the page. Baking a real sample sheet into the page
    at build time is what makes "print only the worksheet" true before any
    script runs — and it is the same sheet a reader sees on arrival.
    """
    m = BANK_NAME.search(open(path, encoding="utf-8").read())
    slug = m.group(1) if m else ("hindi" if "/hindi/" in path else None)
    if not slug:
        return None
    bank = "js/%s-quiz-bank.js" % slug
    if not os.path.exists(bank):
        return None
    src = open(bank, encoding="utf-8").read()
    for marker in ("window.EKGURU_%s_QUIZ" % slug.upper(),
                   "window.EKGURU_HINDI_QUIZ", "window.EKGURU_QUIZ"):
        d = json_object(src, marker)
        if d and d.get("questions"):
            return d["questions"]
    return None


CHAIN = "data-print-chain"
CHAIN_RE = re.compile(r"\s+" + CHAIN + r'(="[^"]*")?')

SAMPLE_END = "<!-- /ekguru:sample-sheet -->"
STATIC_END = "<!-- /ekguru:static-sheet -->"


def strip_baked(html, mark, endmark):
    """Remove a previously baked sheet block. Legacy blocks have no end
    marker; they end at the first </div></div> after the start mark (the
    sheet is one #w-sheet div holding one .ws-page div, and no inner
    element closes two divs in a row)."""
    i = html.find(mark)
    if i < 0:
        return html, False
    if i > 0 and html[i - 1] == "\n":
        i -= 1                       # take the leading newline with the block
    j = html.find(endmark, i)
    if j >= 0:
        return html[:i] + html[j + len(endmark):], True
    j = html.find("</div></div>", i)
    if j < 0:
        return html, False
    return html[:i] + html[j + len("</div></div>"):], True


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

# A tolerant tokenizer: comments and script/style BODIES are skipped whole, so
# a `<` inside a quiz string cannot be mistaken for a tag. Everything else is
# matched as an open tag, a close tag, or nothing.
TAGRE = re.compile(
    r"<!--.*?-->|<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>"
    r"|</?([a-zA-Z][a-zA-Z0-9-]*)(?:\"[^\"]*\"|'[^']*'|[^>\"'])*>",
    re.S | re.I)


def ancestors(html, pos):
    """The open elements around offset `pos`, outermost first."""
    stack = []
    for m in TAGRE.finditer(html):
        if m.start() >= pos:
            break
        tag = m.group(0)
        name = m.group(1)
        if name is None:                      # comment / script / style body
            continue
        name = name.lower()
        if tag.startswith("</"):
            for k in range(len(stack) - 1, -1, -1):
                if stack[k][0] == name:
                    del stack[k:]
                    break
        elif not (tag.rstrip().endswith("/>") or name in VOID):
            stack.append([name, m.start(), m.end()])
    return stack


def mark_chain(html, target):
    """Mark every wrapper between <body> and the sheet.

    Idempotent by construction: the previous marks are dropped first, then the
    chain is recomputed from the markup in front of us.
    """
    out = CHAIN_RE.sub("", html)
    m = target.search(out)
    if not m:
        return out
    chain = [x for x in ancestors(out, m.start()) if x[0] not in ("html", "body")]
    for _name, _s, end in reversed(chain):    # right to left, so offsets hold
        out = out[:end - 1] + " " + CHAIN + out[end - 1:]
    return out



STATIC_MARK = "<!-- ekguru:static-sheet -->"

BANK_FOR = {
    "hindi": "js/hindi-quiz-bank.js",
}


def _bank_questions(path, html):
    """The quiz bank behind a worksheet page, parsed without eval()."""
    slug = None
    m = re.search(r'data-topic="lang-([a-z]+)"', html)
    if m:
        slug = m.group(1)
    if not slug:
        m = re.search(r"/learn/([a-z]+)/practice/worksheets/", path)
        slug = m.group(1) if m else None
    if not slug:
        return None, None
    bank = BANK_FOR.get(slug, "js/%s-quiz-bank.js" % slug)
    if not os.path.exists(bank):
        return None, None
    src = open(bank, encoding="utf-8").read()
    i = src.find('"questions"')
    if i < 0:
        i = src.find("'questions'")
    if i < 0:
        return None, None
    i = src.find("[", i)
    if i < 0:
        return None, None
    # A brace/bracket matcher that skips string contents, so a `]` inside a
    # question ("opts": [ ... ]) cannot end the array early.
    depth, j, in_str, esc = 0, i, False, False
    while j < len(src):
        c = src[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                try:
                    import json
                    return json.loads(src[i:j + 1]), slug
                except Exception:
                    return None, slug
        j += 1
    return None, slug


def _esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def static_sheet(path, html):
    """A printable worksheet that exists in the FILE, not only after a click."""
    if 'data-print-target' not in html:
        return html
    html, _had = strip_baked(html, STATIC_MARK, STATIC_END)
    target = WS_APP.search(html)
    if not target:
        return html
    qs, slug = _bank_questions(path, html)
    if not qs:
        return html
    name = slug.capitalize()
    picked = qs[:5]
    # Five questions on one topic read better than five at random: use the
    # first question's topic when the bank has five of them.
    topic = picked[0].get("topic") if picked else None
    if topic:
        same = [q for q in qs if q.get("topic") == topic][:5]
        if len(same) == 5:
            picked = same
    lines = "".join(
        '<p style="font-weight:700;margin:16px 0 0">%d. %s</p>\n'
        '<div style="border-bottom:1px solid var(--line);height:46px;margin:0 0 10px"></div>\n'
        % (i + 1, _esc(q.get("q", "")))
        for i, q in enumerate(picked))
    answers = "".join(
        '<p style="margin:4px 0">%d. <b>%s</b>%s</p>'
        % (i + 1, _esc(q.get("a", "")),
           " — " + _esc(q.get("explain", "")) if q.get("explain") else "")
        for i, q in enumerate(picked))
    sheet = (
        '\n' + STATIC_MARK + '\n'
        '<div id="w-sheet"><div class="ws-page" style="background:#fff;border:1px solid var(--line);'
        'border-radius:12px;padding:20px;max-width:640px">'
        '<h2 style="margin:0 0 4px">%s practice worksheet</h2>'
        '<p class="muted" style="margin:0 0 12px">Five questions from the free %s course on EkGuru. '
        'The answers stay on screen below — the printed sheet never carries the answer key. '
        'Press <b>Make worksheet</b> for a fresh set, or print this one as it is.</p>'
        '<p style="margin:0 0 14px"><b>Name</b> <span style="display:inline-block;width:180px;'
        'border-bottom:1px solid var(--line)"></span> &nbsp; <b>Date</b> '
        '<span style="display:inline-block;width:110px;border-bottom:1px solid var(--line)"></span></p>'
        '%s<div class="no-print ws-answers" style="margin-top:20px">'
        '<h3 style="margin:0 0 6px">Answers (on screen only — never printed)</h3>%s</div>'
        '<p class="muted" style="margin-top:12px;font-size:.78rem">From the EkGuru %s quiz bank — '
        'free to print and share.</p></div></div>'
        % (name, name, lines, answers, name)) + STATIC_END
    return html[:target.end()] + sheet + html[target.end():]


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def sample_sheet(path, html):
    """Remove the legacy SAMPLE sheet from a worksheet page.

    A worksheet page carries exactly ONE baked worksheet — the static sheet
    (static_sheet, below). An earlier tool version baked a second, marked
    sample sheet into the same #ws-app: dead weight at runtime (the builder
    keeps only the first #w-sheet) and a duplicate on paper without
    JavaScript. This pass strips it forever; it no longer re-injects."""
    return strip_baked(html, SAMPLE_MARK, SAMPLE_END)[0]
def pages():
    out = []
    for dirpath, dirs, files in os.walk("."):
        parts = [x for x in dirpath.split(os.sep) if x and x != "."]
        if any(part in SKIP_DIRS or part.startswith(".") for part in parts):
            continue
        for f in sorted(files):
            if f.endswith(".html"):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


SCRIPT_MARK = "<!-- ekguru:print-sheet -->"
SCRIPT_TAG = '<script src="%sjs/print-sheet.js" defer></script>'


def depth_prefix(path):
    """../ per directory, so the script resolves from any depth."""
    parts = [p for p in path.replace("\\", "/").split("/") if p and p != "."]
    # the last part is the file itself; every directory before it is one level
    return "../" * (len(parts) - 1)


def insert_script(html, path):
    """Load js/print-sheet.js on this page, once."""
    # Older runs emitted a defer-first, two-line tag; normalize to the
    # canonical form so the file (and the tests) see one shape.
    html = re.sub(
        r'<script defer="" src="((?:\.\./)+)js/print-sheet\.js">\s*</script>',
        r'<script src="\1js/print-sheet.js" defer></script>',
        html)
    if SCRIPT_MARK in html or "js/print-sheet.js" in html:
        return html
    tag = SCRIPT_MARK + "\n" + SCRIPT_TAG % depth_prefix(path)
    anchor = "<!-- ekguru:shell-header:end -->"
    if anchor in html:
        return html.replace(anchor, anchor + "\n" + tag, 1)
    i = html.find("</head>")
    if i >= 0:
        return html[:i] + tag + "\n" + html[i:]
    return html


def mark(path, html):
    """Returns (new_html, kind|None). Moves the target if it is on the wrong
    element — the attribute is a statement about the page, so it has one home.
    """
    found = judge(path, html)
    if not found:
        return html, None
    target, kind = found
    out = html

    if not re.search(r"<body[^>]*\b%s=" % MARK, out):
        out = re.sub(r"<body([^>]*)>", r'<body\1 %s="sheet">' % MARK, out, count=1)

    m = target.search(out)
    if m and "data-print-target" in m.group(0):
        # already on the right tag — normalize the attribute (older runs
        # wrote it with an empty value and before the id)
        tag = m.group(0)
        clean = re.sub(r'\s*data-print-target(?:=""|="[^"]*")?', "", tag)
        if clean != tag:
            # id stays first, the print attribute rides behind it; tags
            # without an id (the .art guides) carry it right after the name
            if re.search(r'id="[^"]+"', clean):
                clean = re.sub(r'(id="[^"]+")', r"\1 data-print-target", clean, count=1)
            else:
                clean = re.sub(r"^<(\w+)", r"<\1 data-print-target", clean, count=1)
            out = out[:m.start()] + clean + out[m.end():]
    elif m:
        # strip every copy first (the wrong element, if there is one) …
        out = out.replace(" data-print-target", "")
        m = target.search(out)
        # … then put it on the tag this page's kind prints
        out = out[:m.end() - 1] + " data-print-target" + out[m.end() - 1:]

    out = sample_sheet(path, out)
    out = static_sheet(path, out)
    out = insert_script(out, path)
    out = mark_chain(out, target)
    return out, kind


def main():
    check = "--check" in sys.argv
    unmarked, marked, written = [], 0, 0
    for p in pages():
        with open(p, encoding="utf-8") as fh:
            html = fh.read()
        new, kind = mark(p, html)
        if kind:
            marked += 1
            if new == html:
                continue
        if new == html:
            continue
        if check:
            unmarked.append(p)
            continue
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(new)
        written += 1
    if check:
        if unmarked:
            print("STALE %d page(s) — run: python3 tools/build-print-sheets.py" % len(unmarked))
            for p in unmarked[:12]:
                print("  " + p)
            return 1
        print("ok    %d printable page(s) marked, nothing else to do" % marked)
        return 0
    print("print sheets: %d written, %d printable page(s) known" % (written, marked))
    return 0


if __name__ == "__main__":
    sys.exit(main())
