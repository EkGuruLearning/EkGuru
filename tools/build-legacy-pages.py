#!/usr/bin/env python3
"""EkGuru — THE READING LAYER (974 hand-written pages move onto the design system).

Prakash:

    "ab remaining all pages ka text and more required thing update kro or
     redesign kro according to future or modern ok every page and every text"

WHAT THIS TOUCHES

  974 pages carry their own copy of the same body CSS in a <style> block:
  13 template variants of it, ~3 KB each, 239 distinct selectors across them.
  Every copy has drifted a little further from the others, and the project has
  paid for that five separate times — the note still sitting in the tool pages
  says it best:

      "two copies of the same rule in two files is how this project has
       shipped a stale style five separate times. One class, one place."

  css/experience.css §25 ("the reading layer") is now that one place: it owns
  the whole vocabulary these pages use, expressed in the v200 language. This
  tool does the three things a stylesheet cannot do by itself.

  1. MARK THE PAGES.  <div class="pw"> becomes <div class="pw pw-legacy">
     (and "pw-tool" on the tool pages, whose .card is a flashcard and not a
     link card). Every §25 rule is scoped to those classes, so the modern xp-*
     pages are unreachable from it, whatever the two systems name alike.

  2. DROP THE DUPLICATED CSS.  Every rule in the page's own <style> block that
     §25 now owns is removed — rule by rule, including inside @media blocks —
     and the block itself is removed when nothing is left. A rule is only
     dropped when it is provably owned: the check is a real selector lookup
     against css/experience.css, not a guess. Anything unowned stays exactly
     where it is, and `--report` prints what stayed and why.

  3. GIVE EVERY CELL ITS COLUMN NAME.  The old tables hid a column below 640px.
     That is not responsive design, it is deleted information. Every <td> gets
     data-h="<its column's <th>>", so §25 can restack each row as a labelled
     block on a phone — same data, readable, no sideways scrolling.

  Then it writes the two bands the site was missing:

    .pw-support  — current free/advertising status, with the
                   two ways to keep it that way. Not one of these 974 pages
                   said this before: 0/974 carried any support ask at all.
    .pw-next     — the next step, learned from the page itself: a country page
                   ("Languages of Japan") points at the courses for the
                   languages of that country; a language page points at its own
                   course. This is the same country question the course search
                   now answers, put where a reader of that page already is.

  Both bands are <footer>/<nav> on purpose: they are page chrome, not the
  page's prose, so the copy index (tools/build-copy-index.js strips
  header/footer/nav) does not fingerprint the same 40 words 974 times.

IDEMPOTENT.  Run it twice: the second run changes nothing. Markers
(ekguru:pw-bands) make the bands replaceable rather than additive, the class
swap is a one-way rename, and a table that already has data-h is left alone.

Run:  python3 tools/build-legacy-pages.py [--check] [--report] [--only PATH]
      --check  exits 1 if any page would change (CI / build-all.py check)
      --report prints why each kept rule is kept, and writes nothing
"""
import json
import os
import re
import sys
import unicodedata
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CSS = "css/experience.css"
BAND_START = "<!-- ekguru:pw-bands:start -->"
BAND_END = "<!-- ekguru:pw-bands:end -->"
SHELL_FOOTER = "<!-- ekguru:shell-footer:start -->"

# Selectors dropped although §25 does not style them, with the reason.
DEAD = {
    # tools/build-shell.js deletes the in-page <footer class="pw-ftr"> when it
    # stamps the one real footer; this styling outlived its element.
    ".pw-ftr", ".pw-ftr nav", ".pw-ftr a",
    # The pre-shell footer's own rules. They still win on cascade order today
    # (a page's <style> comes after the bundle), which is exactly the stale
    # style the project keeps re-shipping. The footer is the shell's now.
    ".ftr a", ".ftr-in a", ".ftr-bot a",
    # The old way of fitting a 5-column table on a phone: hide a column. §25
    # restacks the row with its column names instead, so nothing is lost.
    "table.lang th:nth-child(4)", "table.lang td:nth-child(4)",
    "table.lang th:nth-child(3)", "table.lang td:nth-child(3)",
}

COUNTRIES = "tools/_countries-cache.json"
CARDS = ".cards>.card"


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def norm(sel):
    """One spelling of a selector, so two files can be compared."""
    sel = re.sub(r"\s+", " ", sel.strip())
    sel = re.sub(r"\s*([>+~])\s*", r"\1", sel)
    # [type="text"] and [type=text] are the same selector; the old pages write
    # them unquoted, §25 writes them quoted.
    sel = re.sub(r"""\[([a-zA-Z-]+)=["']([^"']*)["']\]""", r"[\1=\2]", sel)
    return sel


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", " ", css, flags=re.S)


# Folder names that are not the country's name: the three the site writes the
# way readers say them. Everything else matches on the name (apostrophes and
# accents dropped, so "Côte d'Ivoire" finds cote-divoire).
SHORT_NAMES = {"uae": "AE", "uk": "GB", "usa": "US"}
# The country's own name, where the folder and the data disagree: the site calls
# Côte d'Ivoire by its French name, the country data calls it Ivory Coast.
FOLDER_ALIASES = {"cote-divoire": ("CI", "Côte d'Ivoire")}


def slugify(s):
    """A country name to the folder the site files it under.

    Accents are decomposed and dropped, not turned into separators: "Türkiye"
    is turkiye, not t-rkiye, and "Côte d'Ivoire" is cote-divoire.
    """
    s = unicodedata.normalize("NFKD", s.lower().replace("&", " and "))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("'", "").replace("\u2019", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# ---------------------------------------------------------------------------
# what the shared layer owns
# ---------------------------------------------------------------------------
def owned_selectors():
    """Every selector in §25 of css/experience.css."""
    with open(CSS, encoding="utf-8") as f:
        css = f.read()
    i = css.find("25. THE READING LAYER")
    if i < 0:
        raise SystemExit("ERROR: css/experience.css has no §25 — the reading layer is missing")
    section = css[css.rfind("/*", 0, i):]
    out = set()
    for m in re.finditer(r"([^{}]+)\{", strip_comments(section)):
        head = m.group(1).strip()
        if not head or head.startswith("@") or ";" in head:
            continue
        for part in head.split(","):
            part = part.strip()
            if part:
                out.add(norm(part))
    return out


OWNED = None
_CACHE = {}


def aliases(sel):
    """Further spellings of `sel` that §25 may own."""
    out = [re.sub(r"^\.pw(?=\s|$)", ".pw-legacy", sel)]
    m = re.match(r"^(\.cards?)([\s\S]*)$", sel)
    if m:
        # §25 styles a link card as .cards > .card, because a bare .card inside
        # a tool is a flashcard — the two cannot share one rule.
        out.append(CARDS + m.group(2))
        # …and the old "hovering the card lifts its title" rule, same idea.
        if m.group(2).strip() == "a:hover b":
            out.append(CARDS + " a:hover b")
    m = re.match(r"^(?:table\.lang|table\.phr|\.tbl)\s+(.+)$", sel)
    if m:
        out.append(m.group(1))          # §25 styles the cell, not the table
    if norm(sel) == ".row .btn":
        out.append(".btn")
    m = re.match(r"^(?:\.tool|\.cf-f)\s+(input|select|textarea)(:focus)?$", sel)
    if m:
        out.append(m.group(1) + (m.group(2) or ""))
    m = re.match(r"^\.row\s+(.+)$", sel)
    if m:
        out.append(m.group(1))          # a .row is a flex wrapper; the item is the thing
    return [o for o in out if o and o != sel]


def is_owned(sel, family):
    """Can §25 style this selector?

    Exact match first, then a prefix match for the cases where the layer styles
    the same thing but spells it more precisely — .pw-legacy
    input:not([type=checkbox])… still owns a bare `input`.
    """
    global OWNED
    if OWNED is None:
        OWNED = owned_selectors()
    key = (sel, family)
    if key in _CACHE:
        return _CACHE[key]
    s = norm(sel)
    hit = s in DEAD
    if not hit:
        cands = set()
        for f in {s} | set(aliases(s)):
            cands.add(f)
            for pre in (".pw-legacy ", ".pw-tool "):
                cands.add(pre + f)
        if family != "tool":
            cands = {c for c in cands if not c.startswith(".pw-tool ")}
        for c in cands:
            if c in OWNED:
                hit = True
                break
            n = len(c)
            for o in OWNED:
                if len(o) > n and o.startswith(c) and o[n] in ":.[# >":
                    hit = True
                    break
            if hit:
                break
    _CACHE[key] = hit
    return hit


# ---------------------------------------------------------------------------
# the page's own <style>, rule by rule
# ---------------------------------------------------------------------------
def parse_blocks(css):
    """Top level of a stylesheet: ('rule', selectors, body) | ('at', head, inner)."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        head = css[i:j].strip()
        if head.startswith("@"):
            depth, k = 1, j + 1
            while k < n and depth:
                if css[k] == "{":
                    depth += 1
                elif css[k] == "}":
                    depth -= 1
                k += 1
            out.append(("at", head, css[j + 1:k - 1]))
            i = k
            continue
        k = css.find("}", j)
        if k < 0:
            break
        out.append(("rule", head, css[j + 1:k]))
        i = k + 1
    return out


def strip_block(css, family, report=None, where=""):
    """Returns (kept_css, dropped_rules). Unattributable rules are kept."""
    kept, dropped = [], 0
    for kind, head, body in parse_blocks(css):
        if kind == "at":
            inner, inner_dropped = strip_block(body, family, report, where + head + " ")
            dropped += inner_dropped
            if inner.strip():
                kept.append(head + "{" + inner.strip() + "}")
            continue
        head = strip_comments(head).strip()
        sels = [s.strip() for s in head.split(",") if s.strip()]
        if sels and all(is_owned(s, family) for s in sels):
            dropped += 1
            continue
        if report is not None and sels:
            unowned = [s for s in sels if not is_owned(s, family)]
            report.append("%s  %s" % (where or "·", " | ".join(unowned)))
        kept.append(head + "{" + body.strip() + "}")
    return "\n".join(kept), dropped


# ---------------------------------------------------------------------------
# data-h: every cell gets its column's name
# ---------------------------------------------------------------------------
TAG = re.compile(r"<[^>]+>")


def cell_text(s):
    return unescape(TAG.sub("", s)).replace("\u200b", "").strip()


def escape_attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def label_rows(html):
    """Give each <td> the text of its column's <th>. Returns (html, tables)."""
    out, touched, pos = [], 0, 0
    for m in re.finditer(r"<table\b[\s\S]*?</table>", html):
        table = m.group(0)
        out.append(html[pos:m.start()])
        pos = m.end()
        if "data-h=" in table:
            out.append(table)
            continue
        rows = list(re.finditer(r"<tr\b[^>]*>[\s\S]*?</tr>", table))
        heads = None
        for r in rows:
            if "<th" in r.group(0):
                heads = [cell_text(c) for c in
                         re.findall(r"<th\b[^>]*>[\s\S]*?</th>", r.group(0))]
                break
        if not heads or not any(heads):
            out.append(table)
            continue
        new_rows = []
        for r in rows:
            row = r.group(0)
            if "<th" in row:
                new_rows.append(row)
                continue
            cells = list(re.finditer(r"<td\b([^>]*)>", row))
            if not cells or len(cells) != len(heads):
                new_rows.append(row)
                continue
            pieces, last = [], 0
            for i, c in enumerate(cells):
                label = heads[i]
                if len(label) > 28:
                    label = label[:27].rstrip() + "\u2026"
                pieces.append(row[last:c.start()])
                pieces.append('<td data-h="%s"%s>' % (escape_attr(label), c.group(1)))
                last = c.end()
            pieces.append(row[last:])
            new_rows.append("".join(pieces))
        new_table = table
        for old, new in zip((r.group(0) for r in rows), new_rows):
            if old != new:
                new_table = new_table.replace(old, new, 1)
        if new_table != table:
            touched += 1
            table = new_table
        out.append(table)
    out.append(html[pos:])
    return "".join(out), touched


# ---------------------------------------------------------------------------
# the two bands
# ---------------------------------------------------------------------------
def course_index():
    try:
        with open("data/courses/index.json", encoding="utf-8") as f:
            return {c["code"]: c for c in json.load(f).get("courses", [])}
    except (OSError, ValueError):
        return {}


def course_countries():
    """ISO country code -> [(course name, course code)] for every course we have.

    The same relation the country index is built from, so the band on a country
    page cannot promise something /courses/by-country/ does not show.
    """
    try:
        with open("data/global/language-country-relations.json", encoding="utf-8") as f:
            rel = json.load(f)
        rel = rel.get("relations", rel)
    except (OSError, ValueError):
        return {}
    iso3 = {"arb": "ar", "cmn": "zh", "fil": "fil", "npi": "npi", "uzn": "uzn", "zsm": "zsm"}
    courses = course_index()
    out = {}
    for r in rel:
        if not isinstance(r, dict):
            continue
        code = r.get("iso_639_1") or iso3.get(r.get("iso_639_3")) or r.get("iso_639_3")
        country = (r.get("country_id") or "").upper()
        course = courses.get(code)
        if not course or not country:
            continue
        out.setdefault(country, {})[code] = course["name"]
    return {k: sorted(v.items(), key=lambda kv: kv[1]) for k, v in out.items()}


def load_countries():
    try:
        with open(COUNTRIES, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    rows = data if isinstance(data, list) else data.get("countries", data)
    if isinstance(rows, dict):
        rows = list(rows.values())
    out = {}
    for r in rows:
        if not isinstance(r, dict):
            continue
        raw = r.get("name")
        if isinstance(raw, dict):
            raw = raw.get("common") or raw.get("official") or ""
        name = str(raw or r.get("country") or "").strip()
        code = str(r.get("code") or r.get("iso2") or r.get("cca2") or "").strip().upper()
        if name and code:
            out[slugify(name)] = (code, name)
    by_code = {c: (c, n) for c, n in out.values()}
    for slug, code in SHORT_NAMES.items():
        if code in by_code:
            out[slug] = by_code[code]
    out.update(FOLDER_ALIASES)
    return out


# The reusable support band in the page's own language (v3 hardening, Gate 14).
# Page language decides; English is the fallback. Reusable CTA strings only —
# never lesson content. Keys: (title, paragraph, cta, trial).
# One factual support band is used in every language tree; it avoids
# unreviewed translations of commercial or permanence claims.

def page_lang(html):
    match = re.search(r'<html\b[^>]*\blang=["\']([^"\']+)', html, re.I)
    return (match.group(1).split("-")[0].lower() if match else "en")


def support_band(lang="en"):
    # Keep this factual and language-neutral. The former translated variants
    # promised that every lesson would remain free forever and claimed ads were
    # active on surrounding pages; neither statement is valid in this release.
    return (
        '<footer class="pw-support">\n'
        '  <p>Published lessons are currently free. Advertising is disabled in this release.</p>\n'
        '  <a class="pw-support-cta" href="/support/">Support EkGuru</a>\n'
        '  <a href="/find-tutors.html">Tutor profiles</a>\n'
        '</footer>\n'
    )

def lesson_band(course, code, tool=False):
    """One shape for "here is the course for this language", from real data."""
    levels = course.get("levels") or {}
    if isinstance(levels, dict) and levels:
        keys = sorted(levels)
        lessons = sum((l or {}).get("lessons", 0) for l in levels.values())
        shape = "%s to %s, %d lessons" % (keys[0], keys[-1], lessons)
    else:
        shape = "not published yet"
    if tool:
        return (
            '<nav class="pw-next" aria-label="Next step">\n'
            '  <b>Turn a tool on, then learn around it</b>\n'
            '  <p>The free %s course is what these tools belong to — %s, and it works\n'
            '  without an account.</p>\n'
            '  <p><a class="btn btn-primary" href="/courses/#/%s">Open the %s course</a></p>\n'
            '</nav>\n' % (course["name"], shape, code, course["name"])
        )
    return (
        '<nav class="pw-next" aria-label="Next step">\n'
        '  <b>Learn %s properly</b>\n'
        '  <p>The free course takes it in order — %s, from the first letter to real\n'
        '  conversation, and it works without an account.</p>\n'
        '  <p><a class="btn btn-primary" href="/courses/#/%s">Open the %s course</a></p>\n'
        '</nav>\n' % (course["name"], shape, code, course["name"])
    )


def language_of_folder(folder):
    """The language a page's own folder names, or None.

    Leftmost match, not first found: `learn-hindi-for-arabic-speakers/grammar/`
    is about Hindi — Arabic is the language the reader already speaks, and the
    first version of this pointed that page at the Arabic course.
    """
    words = folder.replace("_", "-").split("-")
    best = None
    for code, course in course_index().items():
        for name in {slugify(course.get("name", "")), course.get("slug") or "", code}:
            if not name:
                continue
            if name in words:
                at = words.index(name)
            elif name == folder:
                at = 0
            else:
                continue
            if best is None or at < best[0] or (at == best[0] and len(name) > best[2]):
                best = (at, (code, course), len(name))
    return best[1] if best else None


def next_band(path, countries, by_country):
    """The next step for this exact page, or nothing when we have nothing real to say."""
    segs = path.lstrip("./").split("/")
    if len(segs) >= 3 and segs[0] == "world-languages":
        hit = countries.get(segs[1])
        if hit:
            code, name = hit
            names = [n for _, n in by_country.get(code, [])]
            if len(names) == 1:
                taught = "EkGuru teaches <b>%s</b> over video, one to one, with a tutor who speaks it." % names[0]
            elif 2 <= len(names) <= 4:
                taught = ("EkGuru teaches <b>%s</b> over video, one to one, with tutors who speak them."
                          % " and ".join([", ".join(names[:-1]), names[-1]] if len(names) > 2 else names))
            elif names:
                taught = ("EkGuru teaches <b>%d of these languages</b> over video, one to one — %s, %s, %s and %d more."
                          % (len(names), names[0], names[1], names[2], len(names) - 3))
            else:
                taught = ("No course exists for the languages listed here yet — this page is the "
                          "inventory, not the promise.")
            return (
                '<nav class="pw-next" aria-label="Next step">\n'
                '  <b>Learn a language of %s with a tutor</b>\n'
                '  <p>%s The first lesson costs nothing.</p>\n'
                '  <p><a class="btn btn-primary" href="/courses/?country=%s">Courses for %s</a>\n'
                '  <a class="btn btn-ghost" href="/courses/by-country/#country-%s">Every language of %s</a></p>\n'
                '</nav>\n' % (name, taught, code, name, code, name)
            )
    if len(segs) >= 2 and segs[0] not in ("", "courses", "learn", "languages", "world-languages"):
        course = language_of_folder(segs[0])
        if course:
            code, c = course
            return lesson_band(c, code)
        if "toolbox" in segs[0].replace("_", "-").split("-"):
            courses = course_index()
            if "hi" in courses:
                return lesson_band(courses["hi"], "hi", tool=True)
    return None


# Where the bands go when the page has no bands yet. The shell footer is the
# right answer on a built page, but a page freshly written by a generator has
# no shell markers at all (tools/build-shell.js runs last, on purpose), and an
# earlier version of this function refused to build such a page at all:
# "ERROR: <page> has neither the bands nor the shell footer marker". The bands
# still belong inside the page — before its own footer, or at the end of main,
# or at the end of the body — so that is where they go.
BAND_ANCHORS = ('<div class="pw-ftr', "<footer", "</main>", "</body>")


def band_anchor(html, path):
    if SHELL_FOOTER in html:
        return html.index(SHELL_FOOTER)
    for anchor in BAND_ANCHORS:
        if anchor in html:
            return html.index(anchor)
    raise SystemExit("ERROR: %s has neither the bands nor any place to put them" % path)


def splice_bands(html, path, countries, by_country):
    block = (BAND_START + "\n" + (next_band(path, countries, by_country) or "")
             + support_band(page_lang(html)) + BAND_END + "\n")
    if BAND_START in html:
        start = html.index(BAND_START)
        end = html.index(BAND_END, start) + len(BAND_END)
        tail = html[end:]
        tail = tail[1:] if tail.startswith("\n") else tail
        return html[:start] + block + tail
    i = band_anchor(html, path)
    return html[:i] + block + html[i:]


# ---------------------------------------------------------------------------
# the whole transform
# ---------------------------------------------------------------------------
def transform(html, path, countries, by_country, report=None):
    """A legacy page in, a page on the design system out. Idempotent."""
    is_tool = 'class="tool"' in html
    family = "tool" if is_tool else "plain"
    changed = []

    # 1. the classes
    def swap(m):
        cls = m.group(1).split()
        if "pw-legacy" not in cls:
            cls.append("pw-legacy")
        if is_tool and "pw-tool" not in cls:
            cls.append("pw-tool")
        return 'class="%s"' % " ".join(cls)
    new = re.sub(r'class="([^"]*\bpw\b[^"]*)"', swap, html, count=1)
    if new != html:
        changed.append("classes")
        html = new

    # 2. the duplicated css
    def style(m):
        kept, dropped = strip_block(m.group(2), family, report,
                                    ("%s  " % path) if report is not None else "")
        if dropped:
            changed.append("css")
        if not kept.strip():
            return ""
        return m.group(1) + "\n" + kept.strip() + "\n</style>"
    new = re.sub(r"(<style[^>]*>)([\s\S]*?)</style>", style, html)
    html = re.sub(r"\n{3,}", "\n\n", new)

    # 3. column names for every cell
    html, tables = label_rows(html)
    if tables:
        changed.append("data-h")

    # 4. the bands
    new = splice_bands(html, path, countries, by_country)
    if new != html:
        changed.append("bands")
        html = new

    return html, changed


def pages():
    out = []
    for dirpath, dirs, files in os.walk("."):
        if ".git" in dirpath or "node_modules" in dirpath:
            continue
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            p = os.path.join(dirpath, f)
            with open(p, encoding="utf-8") as fh:
                html = fh.read()
            # Token match, not \bpw\b: the page layer marks its own pages
            # .pw-legacy, and a substring test would claim all 555 of them
            # (and then try to put the reading layer on them a second time).
            classes = set()
            for m in re.finditer(r'class="([^"]*)"', html):
                classes.update(m.group(1).split())
            if "pw" not in classes:
                continue
            # Five pages carry .pw and are already on the v200 system (the four
            # legal documents and /support/). Their CSS is the design, not a
            # copy of it — the reading layer has nothing to say to them.
            if re.search(r'class="[^"]*\bxp-(page|main|sec|hero|doc|support-hero|freeband)\b', html):
                continue
            out.append(p)
    return sorted(out)


def main():
    check = "--check" in sys.argv
    do_report = "--report" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    countries = load_countries()
    by_country = course_countries()
    if not countries:
        print("! tools/_countries-cache.json unreadable — country next-steps skipped")
    todo = [only] if only else pages()
    report = [] if do_report else None
    stale, touched, counters = [], 0, {}
    for p in todo:
        with open(p, encoding="utf-8") as fh:
            html = fh.read()
        new, changed = transform(html, p, countries, by_country, report)
        if new == html:
            continue
        stale.append((p, ",".join(changed)))
        for c in changed:
            counters[c] = counters.get(c, 0) + 1
        if not check and not do_report:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(new)
            touched += 1
    if do_report:
        print("--- kept, because §25 does not own them (%d rule(s)) ---" % len(report))
        for line in sorted(set(report)):
            print("  " + line)
        print("\n%d page(s) would change." % len(stale))
        return 0
    if check:
        if stale:
            print("STALE %d page(s) — run: python3 tools/build-legacy-pages.py" % len(stale))
            for p, why in stale[:10]:
                print("  %s  (%s)" % (p, why))
            return 1
        print("ok    all %d page(s) are on the reading layer" % len(todo))
        return 0
    print("reading layer: %d page(s) updated%s" % (
        touched,
        ("  —  " + ", ".join("%s×%d" % (k, v) for k, v in sorted(counters.items()))) if counters else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
