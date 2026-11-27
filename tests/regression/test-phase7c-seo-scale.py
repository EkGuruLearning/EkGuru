#!/usr/bin/env python3
"""Phase 7C §52/§39/§37 — scoped LOCAL static SEO/link-graph gate.

Acceptance contract (not an invented site-wide SEO score):
* tools/seocheck.js defines critical = broken.length and pass = critical == 0;
  tools/gate.js labels that contract "No broken internal links". Apply the same
  zero-broken-target rule to this script's static anchor-link crawl scope.
* A missing/unreadable root, empty crawl or unreadable discovered page is an
  input failure, never a vacuous SEO pass.
* Duplicate titles/descriptions, indexability totals, canonical differences and
  orphan counts remain INFORMATIONAL. There is no supported global threshold
  for this legacy crawl (which excludes tutors and is not the public inventory).
  data/quality/indexing-baseline.json protects existing canonical/noindex policy;
  docs/seo-discovery-followup.md documents deliberate cross-canonical aliases.
  No canonical/robots changes or automatic fixes are authorized by this gate.

HTMLParser reads real tags regardless of attribute order/quoting/case. Metrics
can therefore differ from the historical regex counts. This is not a browser,
HTTP, fragment, JavaScript-link, complete-public-inventory or editorial audit.
The legacy discovery scope is retained; do not infer full SEO quality from PASS.

No network or generation. --root selects an isolated snapshot. The only write
is reports/global-seo-scale-phase7c.json there; --no-report suppresses it.
Exit 0 = scoped criteria pass (informational warnings allowed); 1 = blocking
failure; 2 = report I/O error. Existing report keys and "SEO scale" stdout marker
are retained for tools/run-phase7c-pipeline.py. That caller uses a FAIL marker,
not reliably the process exit code; tools/write-phase7c-reports2.py later
OVERWRITES this report and is not evidence that this gate passed.
"""
import argparse
from collections import Counter
from html import unescape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import time
from urllib.parse import unquote, urljoin, urlparse

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://ekguru.shop"
SKIP_DIRS = {".git", "js", "css", "data", "reports", "images", "uploads", "tools",
             ".github", "node_modules", "tutors", "tests"}
SKIP_FILES = {"googleef0a5b21af26d4ff.html", "404.html", "sitemap.xml", "robots.txt"}


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


class PageInfo(HTMLTextParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.descriptions = []
        self.robots = []
        self.canonicals = []
        self.links = set()
        self._in_title = False
        self._inert = 0
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == "template":
            self._inert += 1
        if self._inert:
            return
        # First attribute wins, as in HTML, rather than silently using the last.
        values = {}
        for name, value in attrs:
            values.setdefault(name, value or "")
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = values.get("name", "").strip().lower()
            content = values.get("content", "").strip()
            if name == "description":
                self.descriptions.append(content)
            elif name == "robots":
                self.robots.append(content)
        elif tag == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonicals.append(values.get("href", "").strip())
        elif tag == "a" and values.get("href", "").strip():
            self.links.add(values["href"].strip())

    def handle_endtag(self, tag):
        if tag == "template":
            self._inert = max(0, self._inert - 1)
        elif not self._inert and tag == "title":
            self._in_title = False

    def handle_text(self, data):
        if self._in_title and not self._inert:
            self.title += data


def pages_on_disk(root):
    """Retain legacy discovery scope: directory indexes + standalone root HTML."""
    root = Path(root)
    pages = []

    def unreadable_directory(exc):
        raise exc

    for dirpath, dirs, files in os.walk(root, onerror=unreadable_directory):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("."))
        rel = Path(dirpath).relative_to(root)
        if "index.html" in files:
            url = "" if rel == Path(".") else rel.as_posix() + "/"
            pages.append((url, Path(dirpath) / "index.html"))
    for file in sorted(root.iterdir()):
        name = file.name
        if name == "index.html" or name in SKIP_FILES:
            continue
        if file.is_file() and name.endswith(".html") and not re.fullmatch(r"google[a-f0-9]+\.html", name):
            pages.append((name, file))
    return pages


def local_file_of_url(root, url_path):
    """Resolve real files or legacy extensionless HTML; never leave the root."""
    root = Path(root).resolve()
    relative = url_path.lstrip("/")
    candidates = [root / relative]
    if not relative or relative.endswith("/"):
        candidates = [root / relative / "index.html"]
    elif not Path(relative).suffix:
        candidates += [root / relative / "index.html", root / (relative + ".html")]
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.is_relative_to(root) and resolved.is_file():
            return resolved
    return None


def resolve(href, page_url):
    """Resolve local anchor targets; external origins and non-HTTP schemes ignored."""
    if href.startswith("#"):
        return None
    url = urlparse(urljoin(BASE + "/" + page_url, href))
    if url.scheme not in {"http", "https"} or url.netloc.lower() != urlparse(BASE).netloc:
        return None
    return unquote(url.path) or "/"


def audit(root):
    root = Path(root).resolve()
    failures = []
    try:
        pages = pages_on_disk(root)
    except OSError as exc:
        pages = []
        failures.append(f"crawl input unreadable: {exc}")
    if not pages:
        failures.append("crawl found no pages; SEO acceptance was not evaluated")
    titles, descs = [], []
    broken, canonical_drift, ambiguous = [], [], []
    link_targets = Counter()
    indexable = noindex = read_count = 0
    for url, file in pages:
        page_url = "/" + url
        try:
            if not file.resolve().is_relative_to(root):
                raise OSError("page symlink leaves crawl root")
            page = PageInfo(file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            failures.append(f"{page_url}: unreadable page ({exc})")
            continue
        read_count += 1
        title = " ".join(page.title.split()) or None
        title = re.sub(r"\s*\|\s*EkGuru$", "", title).strip() if title else None
        desc = page.descriptions[0] if page.descriptions else None
        canon = page.canonicals[0] if page.canonicals else None
        if len(page.descriptions) > 1 or len(page.canonicals) > 1:
            ambiguous.append(page_url)
        titles.append(title or "(none)")
        descs.append(desc or "(none)")
        directives = set(re.split(r"[\s,]+", ",".join(page.robots).lower()))
        if directives & {"noindex", "none"}:
            noindex += 1
        else:
            indexable += 1
        for href in sorted(page.links):
            try:
                target = resolve(href, url)
            except ValueError:
                broken.append((page_url, href))
                continue
            if target is None:
                continue
            link_targets[target] += 1
            # Check anchors to assets too; an extension is not proof of existence.
            if not local_file_of_url(root, target):
                broken.append((page_url, href))
        if canon:
            try:
                canonical_url = urlparse(canon)
                canonical_path = canonical_url.path.rstrip("/") or "/"
                mine = page_url.rstrip("/") or "/"
                if mine == "/index.html":
                    mine = "/"
                if canonical_path != mine or canonical_url.netloc.lower() != urlparse(BASE).netloc:
                    canonical_drift.append((page_url, canon))
            except ValueError:
                canonical_drift.append((page_url, canon))

    duplicate_titles = {title: count for title, count in Counter(titles).items() if count > 1}
    duplicate_descs = {desc: count for desc, count in Counter(descs).items() if count > 1 and desc != "(none)"}
    orphans = ["/" + url for url, _ in pages
               if "/" + url not in {"/", "/index.html", "/admin.html"} and not link_targets.get("/" + url)]
    intentional = [entry for entry in canonical_drift
                   if entry == ("/tutor.html", BASE + "/tutor/")]
    real_drift = [entry for entry in canonical_drift if entry not in intentional]
    if broken:
        failures.append(f"{len(broken)} broken internal anchor target(s); required 0 (tools/seocheck.js)")
    return {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "method": "static crawl of local files (no browser/network); legacy discovery scope",
        "totalPages": len(pages), "pagesRead": read_count,
        "indexable": indexable, "noindex": noindex,
        "duplicateTitles": {"count": len(duplicate_titles), "examples": sorted(duplicate_titles.items(), key=lambda item: (-item[1], item[0]))[:10]},
        "duplicateDescriptions": {"count": len(duplicate_descs), "examples": sorted(duplicate_descs.items(), key=lambda item: (-item[1], item[0]))[:10]},
        "brokenInternalLinks": {"count": len(broken), "examples": broken[:20]},
        "canonicalDrift": {"count": len(real_drift), "examples": real_drift[:20], "intentionalLegacyAliases": intentional},
        "orphanPages": {"count": len(orphans), "examples": orphans[:40]},
        "metadataObservations": {"missingTitles": titles.count("(none)"), "missingDescriptions": descs.count("(none)"),
                                 "ambiguousMetadataPages": ambiguous},
        "pass": not failures, "status": "PASS" if not failures else "FAIL",
        "blockingFailures": failures,
        "acceptanceCriteria": {
            "brokenInternalLinks": "0 required, following tools/seocheck.js and tools/gate.js; static anchor scope only",
            "crawlInput": "nonempty discovery; all discovered pages readable",
        },
        "informationalMetrics": ["totalPages", "indexable", "noindex", "duplicateTitles", "duplicateDescriptions",
                                 "canonicalDrift", "orphanPages", "metadataObservations"],
        "verdictNote": "PASS covers only readable crawl input and zero broken static internal anchor targets. "
                       "Other metrics are informational: no defensible global thresholds or alias-aware baseline "
                       "exist for this discovery scope. No full SEO, publication, browser or live-service approval.",
    }


def write_report(root, result):
    root = Path(root).resolve()
    directory = root / "reports"
    report = directory / "global-seo-scale-phase7c.json"
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
    print("SEO scale (local): %d pages, %d indexable, %d noindex" % (result["totalPages"], result["indexable"], result["noindex"]))
    print("  duplicate titles: %d | duplicate descs: %d | broken links: %d | canonical drift: %d | orphans: %d" %
          tuple(result[key]["count"] for key in ["duplicateTitles", "duplicateDescriptions", "brokenInternalLinks", "canonicalDrift", "orphanPages"]))
    print("SEO scale scoped gate:", result["status"], "(other metrics INFORMATIONAL)")
    for failure in result["blockingFailures"]:
        print("  FAIL:", failure)
    if not args.no_report:
        try:
            write_report(args.root, result)
        except OSError as exc:
            print("FAIL: cannot write private report:", exc)
            return 2
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
