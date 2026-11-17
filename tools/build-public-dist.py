#!/usr/bin/env python3
"""
EkGuru — PUBLIC DEPLOY SET  (python3 tools/build-public-dist.py [--out DIR] [--check])

WHY THIS EXISTS (17 Nov 2026)
  GitHub Pages used to publish the repository root as-is, so every file in
  the repo was one URL away on ekguru.shop: tools/, reports/, docs/, the
  Apps Script sources, the Razorpay server, test fixtures, old sheet
  exports (live-sheets/tutors.csv carried email / notification_email /
  formKey columns). None of that is the website.

  This script copies ONLY the website into an output folder. The Pages
  workflow (.github/workflows/pages.yml) uploads that folder, nothing else.

WHAT STAYS PRIVATE (never copied)
  - build + test tooling          tools/ tests/ src/ playwright.config.mjs
                                  package.json package-lock.json node_modules/
  - internal reports and docs     reports/ docs/ research/ *.md at the root
  - server-side code              apps-script/ server/
  - sheet exports / upload packs  csv/ live-sheets/ *.csv at the root
  - repo plumbing                 .github/ .gitignore .git/ Arena notes

WHAT IS PUBLIC (copied verbatim)
  every other file: HTML, css/, js/, data/, images/, sitemaps, robots.txt,
  ads.txt, CNAME, .nojekyll, manifest, sw.js, verification files.

  Browser code is public by nature — a browser can only run what it can
  download, so js/*.js is visible to anyone who asks for it. That is not a
  leak; secrets live in Apps Script Script Properties and the server's
  environment, never in js/.

--check  : build into a temp dir and verify
           (1) every URL in the sitemaps resolves to a copied file,
           (2) every sw.js precache entry is copied,
           (3) nothing copied references a private path,
           (4) no private file slipped in.
           Exit 1 on any failure. Run by tools/test-public-surface.mjs and CI.
"""
import os
import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Top-level names that are NOT the website.
PRIVATE_DIRS = {
    ".git", ".github", ".arena", ".cache", ".local", ".playwright-cli",
    "node_modules", "tools", "tests", "src", "reports", "docs", "research",
    "apps-script", "server", "csv", "live-sheets", "uploads", "audit",
    "playwright-report", "test-results", "Unselected files",
    "Arena latest command  arena",
}
PRIVATE_FILES = {
    ".gitignore", "package.json", "package-lock.json", "playwright.config.mjs",
}
# Root-level files by extension that are never pages.
PRIVATE_ROOT_EXT = {".md", ".csv", ".log", ".py", ".mjs"}
# Anywhere in the tree.
PRIVATE_GLOBS = re.compile(r"(\.local\.(json|csv)$|\.local$|^deploy-secrets)")


def is_private(rel):
    """rel: path relative to ROOT using '/' separators."""
    top = rel.split("/", 1)[0]
    base = rel.rsplit("/", 1)[-1]
    if top in PRIVATE_DIRS:
        return True
    if "/" not in rel:
        if base in PRIVATE_FILES:
            return True
        if os.path.splitext(base)[1].lower() in PRIVATE_ROOT_EXT:
            return True
    if PRIVATE_GLOBS.search(base):
        return True
    return False


def iter_public():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
        if rel_dir == ".":
            rel_dir = ""
        # prune private directories early
        dirnames[:] = [d for d in dirnames if not is_private((rel_dir + "/" if rel_dir else "") + d)]
        for f in filenames:
            rel = (rel_dir + "/" if rel_dir else "") + f
            if is_private(rel):
                continue
            yield rel


def build(out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    n = 0
    for rel in iter_public():
        src = os.path.join(ROOT, rel)
        dst = os.path.join(out, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        n += 1
    return n


PRIVATE_REF = re.compile(
    r"""(?:href|src|action|url)\s*[=(]\s*["']?(?:https?://ekguru\.shop)?/(?:tools|reports|docs|research|apps-script|server|csv|live-sheets|tests|src)/""",
    re.I,
)


def check(out):
    fails = []
    # 1. sitemap URLs -> files
    sitemap_files = [f for f in os.listdir(out) if f.startswith("sitemap") and f.endswith(".xml")]
    urls = set()
    for sm in sitemap_files:
        try:
            tree = ET.parse(os.path.join(out, sm))
        except ET.ParseError as e:
            fails.append("sitemap parse: %s (%s)" % (sm, e))
            continue
        for el in tree.iter():
            # only <loc> of the sitemap namespace — <image:loc> may be off-site
            if el.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc" and el.text:
                urls.add(el.text.strip())
    missing = []
    for u in sorted(urls):
        if u.endswith(".xml") and "/sitemap" in u:
            continue
        p = re.sub(r"^https?://[^/]+", "", u)
        p = p.split("#", 1)[0].split("?", 1)[0]
        if p.endswith("/"):
            p += "index.html"
        if p.startswith("/"):
            p = p[1:]
        if not os.path.isfile(os.path.join(out, p)):
            missing.append(u)
    if missing:
        fails.append("%d sitemap URL(s) have no file in the public set, e.g. %s" % (len(missing), missing[:5]))
    # 2. sw.js precache entries
    sw = os.path.join(out, "sw.js")
    if os.path.isfile(sw):
        body = open(sw, encoding="utf-8").read()
        body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
        body = re.sub(r"//[^\n]*", "", body)
        m = re.search(r"PRECACHE\s*=\s*\[(.*?)\]", body, re.S)
        if m:
            entries = re.findall(r"[\"']([^\"']+)[\"']", m.group(1))
            for e in entries:
                p = e.split("?", 1)[0]
                if p.endswith("/"):
                    p += "index.html"
                p = p.lstrip("/")
                if p and not os.path.isfile(os.path.join(out, p)):
                    fails.append("sw.js precache entry missing from public set: " + e)
    # 3. no public html/js/css references a private path; 4. no private file present
    for dirpath, _, filenames in os.walk(out):
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), out).replace(os.sep, "/")
            if is_private(rel):
                fails.append("private file in public set: " + rel)
            if f == "admin.html" or rel.startswith("js/admin-stats"):
                continue  # owner dashboard talks about the repo layout in prose
            if os.path.splitext(f)[1].lower() in (".html", ".js", ".css", ".webmanifest", ".xml", ".txt"):
                try:
                    txt = open(os.path.join(dirpath, f), encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                if PRIVATE_REF.search(txt):
                    fails.append("public file links a private path: " + rel)
    return fails, len(urls)


def main():
    args = sys.argv[1:]
    out = None
    if "--out" in args:
        out = args[args.index("--out") + 1]
    if "--check" in args:
        tmp = out or tempfile.mkdtemp(prefix="ekguru-public-")
        n = build(tmp)
        fails, nurls = check(tmp)
        if not out:
            shutil.rmtree(tmp, ignore_errors=True)
        if fails:
            for f in fails:
                print("FAIL  " + f)
            print("\npublic deploy set: %d files, %d sitemap URLs — %d problem(s)" % (n, nurls, len(fails)))
            sys.exit(1)
        print("ok    public deploy set: %d files, every one of %d sitemap URLs present, no private path inside" % (n, nurls))
        return
    out = out or os.path.join(ROOT, "_site")
    n = build(out)
    print("wrote %s (%d files)" % (out, n))


if __name__ == "__main__":
    main()
