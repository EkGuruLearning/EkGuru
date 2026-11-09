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
WS_APP = re.compile(r'<div\b(?=[^>]*\bid=["\']ws-app["\'])[^>]*>', re.I)
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
        pm = re.search(r"/learn/([a-z]+)/practice/worksheets/", path)
        slug = pm.group(1) if pm else None
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



LANG_CODE = {"kannada": "kn", "punjabi": "pa", "urdu": "ur", "bengali": "bn", "hindi": "hi",
             "gujarati": "gu", "tamil": "ta", "malayalam": "ml", "marathi": "mr", "telugu": "te"}


def _lang_wrap(code, inner):
    """Bank text is in the target script: say so, or it reads as English.
    The code is the page's own data-learning-language (bn, gu, ur, ...)."""
    return '<div lang="%s">%s</div>' % (code, inner) if code else inner


def _learning_code(html, slug):
    m = re.search(r'data-learning-language="([a-z]+)"', html)
    return m.group(1) if m else LANG_CODE.get(slug)


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



# ---------------------------------------------------------------------------
# Target-script language tagging (a11y). Baked worksheet questions used to
# be pasted in as bare text: a Kannada/Urdu/Punjabi word inside an English
# paragraph had no lang attribute, so a screen reader read it with an
# English voice. Every run of target-script characters is wrapped in
# <span lang="..">, in both freshly baked sheets and ones already in files.
LANG_BY_SLUG = {
    "bengali": "bn", "gujarati": "gu", "kannada": "kn", "malayalam": "ml",
    "marathi": "mr", "punjabi": "pa", "tamil": "ta", "telugu": "te",
    "urdu": "ur", "hindi": "hi",
}
SCRIPT_BLOCKS = [
    ("\u0900-\u097F", "hi"), ("\u0980-\u09FF", "bn"),
    ("\u0A00-\u0A7F", "pa"), ("\u0A80-\u0AFF", "gu"),
    ("\u0B80-\u0BFF", "ta"), ("\u0C00-\u0C7F", "te"),
    ("\u0C80-\u0CFF", "kn"), ("\u0D00-\u0D7F", "ml"),
    ("\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF", None),
]
_SCRIPT_CLASS = "".join(b for b, _ in SCRIPT_BLOCKS)
_RUN = re.compile("[" + _SCRIPT_CLASS + "]+(?:[ \u00a0]+[" + _SCRIPT_CLASS + "]+)*")


def _script_lang(chunk, page_code):
    for block, lang in SCRIPT_BLOCKS:
        if re.search("[" + block + "]", chunk):
            if lang:
                # Devanagari on a Marathi page is Marathi, not Hindi.
                return page_code if (lang == "hi" and page_code == "mr") else lang
            return page_code  # Arabic block: the page's own language (ur/ar)
    return page_code


def wrap_script_runs(escaped, page_code):
    """Wrap target-script runs of an already-escaped text in lang spans."""
    def sub(m):
        chunk = m.group(0)
        lang = _script_lang(chunk, page_code)
        core = chunk.strip()
        lead = chunk[: len(chunk) - len(chunk.lstrip())]
        trail = chunk[len(chunk.rstrip()):]
        return '%s<span lang="%s">%s</span>%s' % (lead, lang, core, trail)
    return _RUN.sub(sub, escaped)


def page_lang_code(path, html):
    m = re.search(r"/learn/([a-z]+)/", path.replace(os.sep, "/"))
    if m and m.group(1) in LANG_BY_SLUG:
        return LANG_BY_SLUG[m.group(1)]
    qs, slug = _bank_questions(path, html)
    return LANG_BY_SLUG.get(slug or "", "hi")


def repair_sheet_langs(path, html):
    """Tag script runs inside already-baked #w-sheet blocks in place."""
    code = page_lang_code(path, html)
    def fix(m):
        block = m.group(0)
        # drop previous wrappers first so re-running stays stable
        block = re.sub(r'<span lang="[a-zA-Z-]+">([^<]*)</span>', r"\1", block)
        parts = re.split(r"(<[^>]+>)", block)
        for i, part in enumerate(parts):
            if part and not part.startswith("<"):
                parts[i] = wrap_script_runs(part, code)
        return "".join(parts)
    return re.sub(r'<div id="w-sheet">[\s\S]*?</div>\s*</div>', fix, html)


def _esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def static_sheet(path, html):
    """A printable worksheet that exists in the FILE, not only after a click."""
    if STATIC_MARK in html or 'data-print-target' not in html:
        return html
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
        % (i + 1, wrap_script_runs(_esc(q.get("q", "")), page_lang_code(path, html)))
        for i, q in enumerate(picked))
    answers = "".join(
        '<p style="margin:4px 0">%d. <b>%s</b>%s</p>'
        % (i + 1, wrap_script_runs(_esc(q.get("a", "")), page_lang_code(path, html)),
           " — " + wrap_script_runs(_esc(q.get("explain", "")), page_lang_code(path, html)) if q.get("explain") else "")
        for i, q in enumerate(picked))
    sheet = (
        '\n' + STATIC_MARK + '\n'
        '<div id="w-sheet"><div class="ws-page" style="background:#fff;border:1px solid var(--line);'
        'border-radius:12px;padding:20px;max-width:640px">'
        '<h2 style="margin:0 0 4px">%s practice worksheet</h2>'
        '<p class="muted" style="margin:0 0 12px">Five questions from the free %s course on EkGuru, '
        'with the answers at the foot of the sheet. Press <b>Make worksheet</b> for a fresh set, '
        'or print this one as it is.</p>'
        '<p style="margin:0 0 14px"><b>Name</b> <span style="display:inline-block;width:180px;'
        'border-bottom:1px solid var(--line)"></span> &nbsp; <b>Date</b> '
        '<span style="display:inline-block;width:110px;border-bottom:1px solid var(--line)"></span></p>'
        '%s<h3 style="margin:20px 0 6px">Answers</h3>%s'
        '<p class="muted" style="margin-top:12px;font-size:.78rem">From the EkGuru %s quiz bank — '
        'free to print and share.</p></div></div>' % (name, name, _lang_wrap(_learning_code(html, slug), lines), _lang_wrap(_learning_code(html, slug), answers), name))
    return html[:target.end()] + sheet + html[target.end():]


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def sample_sheet(path, html):
    """Insert the built-in sample sheet inside #ws-app, once."""
    if SAMPLE_MARK in html:
        return html
    qs = sample_questions(path)
    m = WS_APP.search(html)
    if not qs or not m:
        return html
    bm = BANK_NAME.search(html) or re.search(r"/learn/([a-z]+)/practice/worksheets/", path)
    slug = bm.group(1) if bm else ("hindi" if "/hindi/" in path else "")
    topic = qs[0].get("topic") or "basics"
    picked = [q for q in qs if (q.get("topic") or topic) == topic][:5]
    if len(picked) < 3:
        picked = qs[:5]
    name = ""
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if h1:
        name = re.sub(r"\s+", " ", re.sub("<[^>]+>", "", h1.group(1))).split(" — ")[0]
        name = name.replace(" worksheets", "").replace(" Worksheet", "").strip()
    lines = "".join(
        '<p style="font-weight:700;margin:14px 0 0">%d. %s</p>'
        '<div style="border-bottom:1px solid var(--line);height:44px;margin:0 0 12px"></div>'
        % (i + 1, wrap_script_runs(esc(q["q"]), page_lang_code(path, html))) for i, q in enumerate(picked))
    answers = "".join(
        '<p style="margin:4px 0">%d. <b>%s</b>%s</p>'
        % (i + 1, wrap_script_runs(esc(q.get("a", "")), page_lang_code(path, html)),
           " — " + wrap_script_runs(esc(q.get("explain", "")), page_lang_code(path, html)) if q.get("explain") else "")
        for i, q in enumerate(picked))
    sheet = (
        '\n' + SAMPLE_MARK + '\n'
        '<div id="w-sheet"><div class="ws-page" style="background:#fff;border:1px solid var(--line);'
        'border-radius:12px;padding:20px;max-width:640px">'
        '<h2 style="margin:0 0 4px">%s worksheet — sample</h2>'
        '<p class="muted" style="margin:0 0 14px">Five questions from the %s quiz bank on this page&rsquo;s '
        'topic. Pick a topic and press <b>Make worksheet</b> for a fresh sheet, or print this one as it is.</p>'
        '%s<h3 style="margin:18px 0 6px">Answers</h3>%s'
        '<p class="muted" style="margin-top:12px;font-size:.78rem">From the EkGuru %s quiz bank — '
        'free to print and share.</p></div></div>' % (esc(name or "EkGuru"), esc(name or "EkGuru"),
                                                      _lang_wrap(_learning_code(html, slug), lines), _lang_wrap(_learning_code(html, slug), answers), esc(name or "EkGuru")))
    return html[:m.end()] + sheet + html[m.end():]


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
        pass                                        # already on the right tag
    elif m:
        # strip every copy first (the wrong element, if there is one) …
        out = out.replace(" data-print-target", "")
        m = target.search(out)
        # … then put it on the tag this page's kind prints
        out = out[:m.end() - 1] + " data-print-target" + out[m.end() - 1:]

    # Keep one baked sample. A rollback briefly enabled both injectors.
    out = re.sub(re.escape(STATIC_MARK) + r".*?(?=" + re.escape(SAMPLE_MARK) + r")",
                 "", out, count=1, flags=re.S)
    out = static_sheet(path, out)
    out = sample_sheet(path, out)
    if SAMPLE_MARK in out and STATIC_MARK not in out:
        out = out.replace(SAMPLE_MARK, STATIC_MARK + "\n" + SAMPLE_MARK, 1)
    out = repair_sheet_langs(path, out)
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
