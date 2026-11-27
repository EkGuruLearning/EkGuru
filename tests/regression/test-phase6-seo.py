#!/usr/bin/env python3
"""Phase 6 §32–34 — local SEO/data/advertising honesty gate.

Retains the original page set and rules: unique nonempty titles/descriptions,
exactly one h1, self-canonical, breadcrumb, no affirmative download CTA or ad
script, and noindex on review/progress. Metadata is parsed, not regex-extracted.
Exactly one nonempty canonical is required; suffix-only URL matches are not
self-canonicals. Duplicate metadata/attributes are ambiguous and fail closed.

No network or generation. --root selects an isolated snapshot. The only write
is reports/phase6-seo.json beneath that root; --no-report disables even that.
Exit 0 = all scoped checks passed; 1 = acceptance failure; 2 = report I/O error.
HTMLParser tolerates recoverable HTML, but this is not an HTML conformance audit.
"""
import argparse
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
PAGES = [
    "learn/hindi/index.html", "learn/hindi/beginner/index.html", "learn/hindi/elementary/index.html",
    "learn/hindi/intermediate/index.html", "learn/hindi/practice/index.html",
    "learn/hindi/practice/typing/index.html", "learn/hindi/practice/quiz/index.html",
    "learn/hindi/practice/worksheets/index.html",
] + ["learn/hindi/%s/index.html" % t for t in
     ["basics", "conversation", "pronunciation", "grammar", "vocabulary",
      "travel", "daily-life", "numbers", "time-dates", "food", "shopping"]]
NOINDEX_PAGES = ["learn/hindi/review/index.html", "learn/hindi/my-progress/index.html"]


class HTMLTextParser(HTMLParser):
    """Small text-context adapter, intentionally identical in both diagnostics.

    Depends on HTMLParser's CPython 3.11/3.12 text-mode hooks: goahead() routes
    text via handle_data while cdata_elem/interesting suppress markup callbacks;
    rawdata retains unfinished input. Regression tests exercise these internals.
    This is not an HTML5 tree builder (nor a full script-escaped-state tokenizer).
    noscript retains the existing scripting-disabled/static interpretation.

    The stdlib calls this mode CDATA, but HTML RCDATA is NOT raw text: only
    title/textarea decode references, exactly once, without retokenizing them.
    """

    RCDATA_ELEMENTS = ("title", "textarea")
    RAWTEXT_ELEMENTS = ("xmp", "iframe", "noembed", "noframes")
    CDATA_CONTENT_ELEMENTS = (HTMLParser.CDATA_CONTENT_ELEMENTS + RCDATA_ELEMENTS
                              + RAWTEXT_ELEMENTS + ("plaintext",))

    def set_cdata_mode(self, elem):
        super().set_cdata_mode(elem)
        if elem == "plaintext":
            self.interesting = re.compile(r"(?!)")  # Nothing, even </plaintext>, ends it.
        elif elem in self.RCDATA_ELEMENTS + self.RAWTEXT_ELEMENTS:
            # Match the exact ASCII tag name, not a prefix or </ title>. Quoted
            # end-tag attributes may contain >; do not resume markup inside them.
            self.interesting = re.compile(
                r"</" + re.escape(elem) + r"(?=[\t\n\f\r />])"
                + r"(?:[^>\"']|\"[^\"]*\"|'[^']*')*>", re.I | re.ASCII)

    def parse_endtag(self, i):
        if self.cdata_elem in self.RCDATA_ELEMENTS + self.RAWTEXT_ELEMENTS:
            match = self.interesting.match(self.rawdata, i)
            if match is None:
                return -1
            self.handle_endtag(self.cdata_elem)
            self.clear_cdata_mode()
            return match.end()
        return super().parse_endtag(i)

    def handle_startendtag(self, tag, attrs):
        if tag in self.CDATA_CONTENT_ELEMENTS:
            # These are non-void HTML elements: <textarea/> still opens textarea.
            self.handle_starttag(tag, attrs)
            self.set_cdata_mode(tag)
        else:
            super().handle_startendtag(tag, attrs)

    def handle_data(self, data):
        if self.cdata_elem in self.RCDATA_ELEMENTS:
            data = unescape(data)
        self.handle_text(data)

    def handle_text(self, data):
        pass

    def close(self):
        super().close()
        if self.cdata_elem and self.rawdata:
            # HTMLParser otherwise leaves unclosed text buffered at EOF. Emit
            # text only: never feed it back as markup or synthesize an end tag.
            self.handle_data(self.rawdata)
            self.rawdata = ""


class SEOPage(HTMLTextParser):
    """Read actual elements; comments and script/style text cannot supply tags."""

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.titles = []
        self.descriptions = []
        self.canonicals = []
        self.robots = []
        self.h1_count = 0
        self.errors = []
        self._title = None
        self._inert = 0
        self.feed(source)
        self.close()
        if self._title is not None:
            self.errors.append("unclosed title element")

    def handle_starttag(self, tag, attrs):
        if tag == "template":
            self._inert += 1
        if self._inert:
            return
        if self._title is not None and tag != "title":
            self.errors.append("element inside unclosed title")
            return
        attrs_dict = dict(attrs)
        if tag in {"meta", "link", "title"}:
            names = [name for name, _ in attrs]
            if len(names) != len(set(names)):
                self.errors.append("duplicate attribute on " + tag)
        if tag == "title":
            if self._title is not None:
                self.errors.append("nested title element")
            self._title = []
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            name = (attrs_dict.get("name") or "").strip().lower()
            value = (attrs_dict.get("content") or "").strip()
            if name == "description":
                self.descriptions.append(value)
            elif name == "robots":
                self.robots.append(value)
        elif tag == "link" and "canonical" in (attrs_dict.get("rel") or "").lower().split():
            self.canonicals.append((attrs_dict.get("href") or "").strip())

    def handle_endtag(self, tag):
        if tag == "template":
            self._inert = max(0, self._inert - 1)
            return
        if self._inert:
            return
        if tag == "title" and self._title is not None:
            self.titles.append(" ".join("".join(self._title).split()))
            self._title = None

    def handle_text(self, data):
        if self._title is not None and not self._inert:
            self._title.append(data)


def audit(root, pages=PAGES, noindex_pages=NOINDEX_PAGES):
    root = Path(root)
    fails, titles, descs = [], {}, {}

    def read(relative):
        try:
            return (root / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            fails.append(f"{relative}: missing or unreadable ({exc})")
            return None

    for relative in pages:
        source = read(relative)
        if source is None:
            continue
        page = SEOPage(source)
        fails.extend(f"{relative}: {error}" for error in page.errors)
        for values, seen, label in [(page.titles, titles, "title"),
                                    (page.descriptions, descs, "meta description")]:
            if not values or not values[0]:
                fails.append(f"{relative}: no {label}")
            if len(values) > 1:
                fails.append(f"{relative}: multiple {label} elements")
            if len(values) == 1 and values[0]:
                value = values[0]
                if value in seen:
                    fails.append(f"{relative}: duplicate {label} (also {seen[value]})")
                seen[value] = relative
        if page.h1_count != 1:
            fails.append(f"{relative}: {page.h1_count} h1 elements (want 1)")
        if not page.canonicals or not page.canonicals[0]:
            fails.append(relative + ": no canonical")
        if len(page.canonicals) > 1:
            fails.append(relative + ": duplicate canonical elements")
        if len(page.canonicals) == 1 and page.canonicals[0]:
            expected_path = "/" + relative.removesuffix("index.html")
            try:
                canonical = urlsplit(page.canonicals[0])
                is_self = (canonical.scheme.lower() == "https"
                           and canonical.netloc.lower() == "ekguru.shop"
                           and canonical.path.rstrip("/") == expected_path.rstrip("/")
                           and not canonical.query and not canonical.fragment)
            except ValueError:
                is_self = False
            if not is_self:
                fails.append(f"{relative}: canonical mismatch {page.canonicals[0]!r}")
        # Retain the original breadcrumb and honesty rules, not a new content audit.
        if "crumb" not in source:
            fails.append(relative + ": no breadcrumb")
        if re.search(r'>\s*Download\b|\bdownload (now|here|for free)\b', source, re.I):
            fails.append(relative + ": download CTA found")
        if re.search(r"adsbygoogle", source, re.I):
            fails.append(relative + ": ad script found on practice/learning page")

    for relative in noindex_pages:
        source = read(relative)
        if source is None:
            continue
        page = SEOPage(source)
        fails.extend(f"{relative}: {error}" for error in page.errors)
        directives = set(re.split(r"[\s,]+", ",".join(page.robots).lower()))
        if "noindex" not in directives:
            fails.append(relative + ": missing noindex")

    return {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pagesChecked": len(pages) + len(noindex_pages),
        "pass": not fails,
        "fails": fails,
    }


def write_report(root, result):
    """Fixed private report only; do not follow report symlinks into public files."""
    root = Path(root).resolve()
    directory = root / "reports"
    report = directory / "phase6-seo.json"
    if directory.resolve() != directory or report.is_symlink():
        raise OSError("refusing symlinked report destination")
    directory.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--no-report", action="store_true")
    args = parser.parse_args(argv)
    result = audit(args.root)
    print("phase6 seo/data checks:", "PASS" if result["pass"] else "FAIL", "|", result["pagesChecked"], "pages")
    for failure in result["fails"]:
        print("  ", failure)
    if not args.no_report:
        try:
            write_report(args.root, result)
        except OSError as exc:
            print("FAIL: cannot write private report:", exc)
            return 2
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
