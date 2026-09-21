#!/usr/bin/env python3
"""EkGuru — THE AD POLICY: which pages may load the ad script, and which may not.

    python3 tools/inject-ads.py            # apply the policy
    python3 tools/inject-ads.py --check    # CI / build-all (exits 1 if stale)
    python3 tools/inject-ads.py --report   # read-only: the decisions, by class

Auto ads place themselves: once the loader is in the page, Google decides where
a unit goes. So the only reliable way to keep advertising off a page that must
not have it — a quiz a learner is mid-way through, a booking form, the page that
explains the ad cookies — is to not load the loader there at all.

The decision is data, not code. data/monetization/google-monetization.json holds
ad_policy.classes: a page class, the path patterns that belong to it, and which
classes may load the loader. This tool applies that policy to every page:

  · allowed class   -> one marked loader block in <head>, exactly once
  · anything else   -> every ad tag, marker and unit removed

and writes the class the page got onto <html data-ad-class="…">, so the decision
is visible in the page itself and checkable by tools/test-ad-policy.mjs.

History: this file used to inject Auto Ads into everything except a hard-coded
list of directories. The list and the monetization matrix drifted apart, which
is how the legal pages — and then the cookie policy — ended up loading an
advertising script they were supposed to be excluded from.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CONFIG = json.load(open("data/monetization/google-monetization.json", encoding="utf-8"))
POLICY = CONFIG["ad_policy"]
CLASSES = POLICY["classes"]
ALLOWED = set(POLICY["loader_allowed"])
EXCLUDED = list(CONFIG.get("excluded_paths", []))
CLIENT = CONFIG["publisher"]["adsense_client"]

MARK = "<!-- ekguru:adsense:start -->"
END = "<!-- ekguru:adsense:end -->"

SNIPPET = (
    MARK + "\n"
    "<!-- Auto ads: one account loader, and Google places the units. Whether\n"
    "     this block is in the page at all is decided by the page's class\n"
    "     (html[data-ad-class]) and data/monetization/google-monetization.json\n"
    "     -> ad_policy. tools/inject-ads.py enforces it. -->\n"
    '<link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>\n'
    '<link rel="preconnect" href="https://googleads.g.doubleclick.net" crossorigin>\n'
    '<meta name="google-adsense-account" content="' + CLIENT + '">\n'
    '<script async src="https://pagead2.googlesyndication.com/pagead/js/'
    'adsbygoogle.js?client=' + CLIENT + '" crossorigin="anonymous"></script>\n'
    + END
)

SKIP_DIRS = {".git", "node_modules", "images", "css", "js", "docs", "templates",
             "research", "tools", "data", "reports"}

# Every shape an ad block takes in this repository, newest first. A stale unit
# left behind by an older build is exactly what this tool exists to prevent, so
# the scrubber knows all of them and is idempotent.
AD_BLOCK = re.compile(re.escape(MARK) + r"[\s\S]*?" + re.escape(END), re.I)
AD_LEFT = [
    re.compile(r"<!--\s*Google AdSense[\s\S]*?-->", re.I),
    re.compile(r"<!--\s*ekguru:ads(?:ense)?(?::(?:start|end))?\s*-->", re.I),
    re.compile(r'<link[^>]*preconnect[^>]*(?:googlesyndication|doubleclick)[^>]*>', re.I),
    re.compile(r'<meta\s+name="google-adsense-account"[^>]*>', re.I),
    re.compile(r'<script[^>]*adsbygoogle\.js[^>]*>\s*</script>', re.I),
    re.compile(r'<ins[^>]*class="[^"]*adsbygoogle[^"]*"[^>]*>[\s\S]*?</ins>', re.I),
    re.compile(r'<script[^>]*>\s*\(adsbygoogle[\s\S]*?</script>', re.I),
    re.compile(r'<script[^>]*>\s*adsbygoogle\s*=[\s\S]*?</script>', re.I),
]


def pages():
    out = []
    for dirpath, dirs, files in os.walk("."):
        parts = [p for p in dirpath.split(os.sep) if p and p != "."]
        if any(p in SKIP_DIRS or p.startswith(".") for p in parts):
            continue
        for f in sorted(files):
            if f.endswith(".html"):
                out.append(os.path.join(dirpath, f).replace("\\", "/").lstrip("./"))
    return sorted(out)


GLOB_CACHE = {}


def glob_re(pattern):
    if pattern not in GLOB_CACHE:
        rx = re.escape(pattern)
        rx = rx.replace(r"\*\*", "\x00").replace(r"\*", "[^/]*").replace("\x00", ".*")
        GLOB_CACHE[pattern] = re.compile("^" + rx + "/?$")
    return GLOB_CACHE[pattern]


def match(pattern, url):
    """A small glob: ** crosses directories, * stays inside one, and a pattern
    that ends in / also matches that directory's index page."""
    if pattern == "/":
        return url in ("/", "/index.html")
    if glob_re(pattern).match(url):
        return True
    return False


def to_url(rel):
    return "/" + rel.replace(os.sep, "/")


CLASS_ORDER = ("ADMIN", "RESEARCH_REQUIRED", "TRANSACTIONAL", "UTILITY",
               "INTERACTIVE_LEARNING", "HIGH_CONTENT", "MEDIUM_CONTENT")


def is_excluded(url):
    for path in EXCLUDED:
        if path.endswith("/") and (url == path or url.startswith(path)):
            return True
        if url == path:
            return True
    return False


def classify(rel, page_html=None):
    """The page's class — what kind of page it is.

    Noindex is a publication state, not a content-length shortcut. Draft and
    research pages remain ad-ineligible even if a path later moves or acquires
    enough prose to resemble an article.
    """
    if page_html is None:
        try:
            with open(rel, encoding="utf-8") as f:
                page_html = f.read()
        except (OSError, UnicodeDecodeError):
            page_html = ""
    url = to_url(rel)
    # Owner-only consoles remain ADMIN even though they also carry noindex.
    if any(match(pattern, url) for pattern in CLASSES["ADMIN"]["match"]):
        return "ADMIN"
    head = page_html.split("</head>", 1)[0]
    if re.search(r'<meta\b(?=[^>]*\bname=["\']robots["\'])(?=[^>]*\bcontent=["\'][^"\']*noindex)', head, re.I):
        return "RESEARCH_REQUIRED"
    if "research-notice" in page_html or 'data-publication-state="research-required"' in page_html:
        return "RESEARCH_REQUIRED"

    for name in CLASS_ORDER:
        for pattern in CLASSES[name]["match"]:
            if match(pattern, url):
                return name
    return "MEDIUM_CONTENT"


def may_load(rel, page_html=None):
    """(class, allowed, why) — the policy decision, in one place."""
    url = to_url(rel)
    cls = classify(rel, page_html)
    if is_excluded(url):
        return cls, False, "excluded_paths"
    if cls not in ALLOWED:
        return cls, False, "class " + cls
    return cls, True, "class " + cls


def set_class_attr(html, cls):
    m = re.search(r"<html\b([^>]*)>", html)
    if not m:
        return html
    attrs = re.sub(r'\s+data-ad-class="[^"]*"', "", m.group(1))
    return html[:m.start()] + "<html" + attrs + ' data-ad-class="%s">' % cls + html[m.end():]


def scrub(html):
    """Every ad tag, marker and unit out of a page. Idempotent."""
    out = AD_BLOCK.sub("", html)
    for rx in AD_LEFT:
        out = rx.sub("", out)
    if out != html:
        out = re.sub(r"[ \t]+\n", "\n", out)
        out = re.sub(r"\n{3,}", "\n\n", out)
        out = out.replace("\n\n</head>", "\n</head>")
    return out


def apply_policy(rel, html):
    """(new_html, what happened). Idempotent: a second run writes nothing."""
    cls, allowed, _why = may_load(rel, html)
    html = set_class_attr(html, cls)

    if not allowed:
        had_ads = "adsbygoogle" in html or "ekguru:ads" in html
        out = scrub(html)
        return out, ("stripped" if had_ads else "kept-clean")

    if html.count(MARK) == 1 and html.count(END) == 1 and "adsbygoogle.js" in html:
        return html, "have"
    html = scrub(html)
    if "</head>" not in html:
        return html, "nohead"
    html = html.replace("</head>", SNIPPET + "\n</head>", 1)
    return html, "added"


def main():
    check = "--check" in sys.argv
    report = "--report" in sys.argv
    if report:
        check = True                     # --report is a report: it must not write

    counts, changes, stale = {}, {}, []
    for rel in pages():
        with open(rel, encoding="utf-8") as f:
            html = f.read()
        new, what = apply_policy(rel, html)
        counts[what] = counts.get(what, 0) + 1
        if report:
            changes.setdefault((classify(rel, html), what), []).append(rel)
        if new == html:
            continue
        if check:
            stale.append((rel, what))
            continue
        with open(rel, "w", encoding="utf-8") as f:
            f.write(new)

    if report:
        for (cls, what), paths in sorted(changes.items()):
            print("%-22s %-11s %4d  e.g. %s" % (cls, what, len(paths), paths[0]))

    if check:
        if stale:
            print("STALE %d page(s) disagree with the ad policy — run: "
                  "python3 tools/inject-ads.py" % len(stale))
            for rel, what in stale[:12]:
                print("  %-11s %s" % (what, rel))
            return 1
        print("ok    ad policy: %d page(s) match the matrix (%s)"
              % (sum(counts.values()),
                 ", ".join("%s %d" % kv for kv in sorted(counts.items()))))
        return 0

    print("ad policy: %d page(s) — %d tagged, %d already correct, "
          "%d ad-free by policy, %d with no head"
          % (sum(counts.values()), counts.get("added", 0) + counts.get("stripped", 0),
             counts.get("have", 0) + counts.get("kept-clean", 0),
             counts.get("stripped", 0) + counts.get("kept-clean", 0),
             counts.get("nohead", 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
