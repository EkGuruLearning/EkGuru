#!/usr/bin/env python3
"""Phase 7B §4 — static dependency graph + load-order forensics.

For every HTML page: resolves each <script src> to a real file (404 detection),
records inline scripts, and checks two classes of real defect that bit Phase 6:

  · DOM targets — inline/global code calling getElementById('x') where no
    element id="x" exists on that page (renderer runs, target missing).
  · Missing globals — a page (inline script or dependency) referencing a
    window.X that no loaded script defines.

Output: reports/phase7b-dependency-graph.json
"""
import json, os, re, time
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

SKIP_DIRS = {".git", "node_modules", "reports", "tools", "audit", ".arena", ".cache", "live-sheets"}

def strip_js_comments(code):
    """Remove JS comments so getElementById / window.X inside comment text
    (e.g. a changelog note describing a past bug) are not treated as live
    references. Keeps https:// URLs intact (// preceded by ':')."""
    code = re.sub(r"/\*[\s\S]*?\*/", "", code)
    code = re.sub(r"(?<!:)//[^\n]*", "", code)
    return code

# globals each JS file exports (window.X = ..., or the UMD idiom root.X =
# ... inside (function(root){...})(window|globalThis))
def exports_of(js):
    g = set()
    for m in re.finditer(r"(?:window|root|globalThis|self)\.([A-Za-z_$][\w$]*)\s*=", strip_js_comments(js)):
        g.add(m.group(1))
    return g

js_exports = {}
js_files = {}
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if f.endswith(".js"):
            p = os.path.join(root, f).lstrip("./")
            js_files[p] = open(p, encoding="utf-8").read()
            js_exports[p] = exports_of(js_files[p])

all_globals = set()
for g in js_exports.values():
    all_globals |= g

# built-in-ish globals we will never flag
BUILTIN = {"addEventListener", "localStorage", "document", "window", "navigator", "location",
           "history", "console", "fetch", "SpeechSynthesisUtterance", "speechSynthesis",
           "URL", "Blob", "FileReader", "confirm", "setTimeout", "setInterval", "requestAnimationFrame",
           "requestIdleCallback", "caches", "serviceWorker", "CustomEvent", "Event", "MutationObserver",
           "IntersectionObserver", "getComputedStyle", "matchMedia", "innerWidth", "innerHeight",
           "JSON", "Math", "Date", "Object", "Array", "String", "Number", "parseInt", "parseFloat",
           "isNaN", "encodeURIComponent", "decodeURIComponent", "Promise", "RegExp", "Error", "TypeError",
           "dispatchEvent", "scrollTo", "alert", "atob", "btoa", "performance", "getSelection"}

issues = {"missing_script": [], "missing_dom_target": [], "missing_global": []}
pages_scanned = 0
page_graph = []

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith(".html"):
            continue
        p = os.path.join(root, f).lstrip("./")
        depth = p.count("/")
        base = os.path.dirname(p)
        html = open(p, encoding="utf-8").read()
        pages_scanned += 1

        # script srcs
        srcs = re.findall(r"<script[^>]+src=[\"']([^\"']+)[\"']", html)
        resolved = []
        for s in srcs:
            if s.startswith(("http", "//", "data:")):
                resolved.append(s); continue
            # relative to the page dir
            target = os.path.normpath(os.path.join(base, s)).lstrip("./").replace("\\", "/")
            if target.endswith(".js"):
                ok = target in js_files
                if not ok:
                    issues["missing_script"].append({"page": p, "ref": s, "resolved": target})
                resolved.append({"ref": s, "file": target, "exists": ok})

        # DOM targets referenced in inline scripts
        inline = re.findall(r"<script(?![^>]*src)[^>]*>([\s\S]*?)</script>", html)
        ids_in_page = set(re.findall(r'id=["\']([^"\']+)["\']', html))
        dom_refs = set()
        for code in inline:
            code = strip_js_comments(code)
            dom_refs |= set(re.findall(r"getElementById\([\"']([^\"']+)[\"']\)", code))
            dom_refs |= set(re.findall(r"querySelector\([\"']#([^\"']+)[\"']\)", code))
        for d in dom_refs:
            if d not in ids_in_page:
                issues["missing_dom_target"].append({"page": p, "id": d})

        # globals referenced in inline scripts but never exported by any js
        # (a window.X = ... defined inline in the SAME page counts as defined)
        inline_defined = set()
        for code in inline:
            inline_defined |= set(re.findall(r"window\.([A-Za-z_$][\w$]*)\s*=", strip_js_comments(code)))
        for code in inline:
            for g in re.findall(r"window\.([A-Za-z_$][\w$]*)", strip_js_comments(code)):
                if g in all_globals or g in inline_defined or g in BUILTIN or g == "EKGURU_I18N":
                    continue
                issues["missing_global"].append({"page": p, "global": g})

        page_graph.append({
            "page": p, "depth": depth,
            "scripts": [r if isinstance(r, str) else r["ref"] for r in resolved],
            "inlineBlocks": len(inline),
        })

# aggregate: dedupe missing_global
seen_global = set()
uniq_global = []
for x in issues["missing_global"]:
    k = (x["page"], x["global"])
    if k not in seen_global:
        seen_global.add(k); uniq_global.append(x)
issues["missing_global"] = uniq_global

report = {
    "generated": NOW,
    "pagesScanned": pages_scanned,
    "jsFiles": len(js_files),
    "globalsDefined": sorted(all_globals),
    "issues": issues,
    "summary": {
        "missingScriptRefs": len(issues["missing_script"]),
        "missingDomTargets": len(issues["missing_dom_target"]),
        "missingGlobals": len(issues["missing_global"]),
    },
    "pass": not (issues["missing_script"] or issues["missing_dom_target"] or issues["missing_global"]),
}
with open("reports/phase7b-dependency-graph.json", "w", encoding="utf-8") as fh:
    json.dump(report, fh, ensure_ascii=False, indent=2)
print("pages:", pages_scanned, "| js:", len(js_files), "| globals:", len(all_globals))
print("missing scripts:", len(issues["missing_script"]),
      "| missing dom targets:", len(issues["missing_dom_target"]),
      "| missing globals:", len(issues["missing_global"]))
for x in issues["missing_script"][:10]:
    print("  SCRIPT404", x)
for x in issues["missing_dom_target"][:10]:
    print("  DOM", x)
for x in issues["missing_global"][:10]:
    print("  GLOBAL", x)
