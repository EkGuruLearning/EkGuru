#!/usr/bin/env python3
"""EkGuru — THE PAGE LAYER (the 483 lesson/answer/hub pages join §25).

Prakash:

    "ab remaining all pages ka text and more required thing update kro or
     redesign kro according to future or modern ok every page and every text"

§25 ("the reading layer") put the 974 hand-written `.pw` pages on one
stylesheet. These are the rest of the hand-written site: the language lessons,
the answers, the ask pages, the directories — 555 pages, and every one of them
was still shipping its own copy of the same CSS in a <style> block: the same
crumb, the same lede, the same table, the same cards, 1.4 MB of it in total.

They do not need a second stylesheet. Their container (.art, .qw, .aw) is
given the class §25 already owns — .pw-legacy — and every rule of §25 reaches
them: the reading measure, the crumb, the tables that restack with their
column names on a phone, the cards, the buttons, the support and next bands,
the print rules. css/experience.css §26 ("the page layer") adds only what §25
never had: the cards and widgets these pages are built from.

What this tool does, per page:

  1. MARK IT      <div class="art"> becomes <div class="art pw-legacy">
  2. DROP THE CSS every rule its own <style> block shares with the layer is
                  removed, rule by rule, against a real selector lookup —
                  exactly the way tools/build-legacy-pages.py does it
  3. NAME CELLS   every <td> gets data-h="<its column name>" so the tables
                  can restack instead of hiding a column
  4. TWO BANDS    the support ask, and the next step for that page

IDEMPOTENT, like the reading layer: run it twice and the second run changes
nothing. `--check` exits 1 if anything would change.

Run:  python3 tools/build-page-layer.py [--check] [--report] [--only PATH]
"""
import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# The reading layer owns the rules; this tool reuses its selector lookup, its
# table labelling and its two bands, so the two layers cannot drift apart.
_spec = importlib.util.spec_from_file_location("reading_layer", "tools/build-legacy-pages.py")
blp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(blp)

SKIP_DIRS = {".git", "node_modules", "images", "css", "js", "data", "reports",
             "docs", "templates", "research", "tools"}
CONTAINER = re.compile(r'<div class="(art|qw|aw)(["\s])')
BANDS = re.compile(r"<!-- ekguru:pw-bands:start -->[\s\S]*?<!-- ekguru:pw-bands:end -->")
V200 = re.compile(r'class="xp-')
STYLE = re.compile(r"<style[^>]*>([\s\S]*?)</style>")


# The page's own rules are written against .art / .qw / .aw; after step 1 that
# element IS the .pw-legacy container, so ".art h1" and ".pw-legacy h1" style
# the same element. Without this, the page's copy of a rule would survive the
# strip and, sitting after the bundle, quietly win — the stale style this
# project has shipped five times.
_raw_is_owned = blp.is_owned


def is_owned(sel, family):
    if _raw_is_owned(sel, family):
        return True
    s = blp.norm(sel)
    if s in (".art", ".qw", ".aw"):
        return True                      # §26 owns the container itself
    m = re.match(r"^\.(?:art|qw|aw)\s+(.+)$", s)
    if m:
        return _raw_is_owned(m.group(1), family)
    return False


blp.is_owned = is_owned


def page_files():
    out = []
    for dirpath, dirs, files in os.walk("."):
        parts = [x for x in dirpath.split(os.sep) if x and x != "."]
        if any(p in SKIP_DIRS or p.startswith(".") for p in parts):
            continue
        for f in sorted(files):
            if f.endswith(".html"):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


def has_css(html):
    """CSS left in the page that is not the band block."""
    return bool(re.search(r"\{", BANDS.sub("", "".join(STYLE.findall(html)))))


def on_layer(html):
    """Is this page already on the layer (its container carries .pw-legacy)?"""
    return bool(re.search(r'<div class="[^"]*\bpw-legacy\b', html))


def belongs(html):
    """Is this a page-layer page at all?

    The vocabulary is the test: art/qw/aw containers and none of the v200
    xp-* classes. The v200 pages have their own inline CSS and their own
    system — marking them .pw-legacy would put two designs on one element.
    """
    return bool(CONTAINER.search(html)) and not V200.search(html)


def mark(html):
    """<div class="art"> -> <div class="art pw-legacy">, once."""
    if on_layer(html):
        return html

    def swap(m):
        return '<div class="%s pw-legacy%s' % (m.group(1), m.group(2))
    return CONTAINER.sub(swap, html, count=1)


def band_for(path, countries, by_country):
    """§25's next-step band, with the folders it does not know about."""
    band = blp.next_band(path, countries, by_country)
    if band:
        return band
    segs = path.lstrip("./").split("/")
    for seg in segs:
        course = blp.language_of_folder(seg)
        if course:
            code, data = course
            return blp.lesson_band(data, code)
    # answers/ and ask/ are Hindi pages: point at what they are about.
    if segs[0] in ("answers", "ask", "daily-hindi", "name-in-hindi"):
        courses = blp.course_index()
        if "hi" in courses:
            return blp.lesson_band(courses["hi"], "hi")
    return None


def splice_bands(html, path, countries, by_country):
    """blp.splice_bands, but the band comes from band_for() above."""
    block = (blp.BAND_START + "\n" + (band_for(path, countries, by_country) or "")
             + blp.support_band() + blp.BAND_END + "\n")
    if blp.BAND_START in html:
        start = html.index(blp.BAND_START)
        end = html.index(blp.BAND_END, start) + len(blp.BAND_END)
        tail = html[end:]
        tail = tail[1:] if tail.startswith("\n") else tail
        return html[:start] + block + tail
    i = html.index(blp.SHELL_FOOTER)
    return html[:i] + block + html[i:]


def transform(html, path, countries, by_country, report=None):
    """A page-layer page in, a page on the design system out. Idempotent."""
    out = mark(html)
    changed = out != html

    # 2. the page's own CSS, rule by rule
    def style(m):
        kept, notes = blp.strip_block(m.group(1), "plain", report, path)
        if report is not None and kept.strip():
            report.append("%s  (%d bytes of CSS the layer does not own)" % (path, len(kept)))
        if not kept.strip():
            return ""
        return "<style>%s\n</style>" % kept.strip()
    out = STYLE.sub(style, out)
    out = re.sub(r"\n{3,}", "\n\n", out)

    # 3. column names, so the tables restack
    out, tables = blp.label_rows(out)

    # 4. the two bands
    out = splice_bands(out, path, countries, by_country)

    if report is not None:
        report.append("%s  marked=%s tables=%d css_left=%d"
                      % (path, changed, tables, max(len(b) for b in STYLE.findall(out)) if STYLE.search(out) else 0))
    return out, changed, tables


def main():
    check = "--check" in sys.argv
    report = [] if "--report" in sys.argv else None
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]

    countries = blp.load_countries()
    by_country = blp.course_countries()
    todo, wrote, already, tables_total = [], 0, 0, 0
    for path in page_files():
        if only and only not in path:
            continue
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        if not belongs(html):
            continue
        new, changed, tables = transform(html, path, countries, by_country, report)
        tables_total += tables
        if new == html:
            already += 1
            continue
        if check:
            todo.append(path)
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)
        wrote += 1

    if report is not None:
        print("\n".join(report))
    if check:
        if todo:
            print("STALE %d page(s) not on the page layer:" % len(todo))
            for p in todo[:15]:
                print("  " + p)
            return 1
        print("ok    every page-layer page is on the layer (%d already)" % already)
        return 0
    print("page layer: %d page(s) updated, %d already on it, %d table cells named"
          % (wrote, already, tables_total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
