#!/usr/bin/env python3
"""
EkGuru — Inject Modern JS v300
Injects modern JS files into all HTML pages:
- js/cookie-consent.js (v300 CMP)
- js/monetization.js (v300 5 channels)
- js/print-sheet.js (v300 print-only-worksheet)
- js/level-visuals.js (v300 age progression)
- js/visual-learning.js (v300 dotted tracing)
- js/practice-api.js (v300 shared flags/likes)
- js/refresh-guard.js (v300 refresh bug fix)
- js/course-player.js (v300 responsive)

Ensures each page loads these if not already.
Idempotent.
"""
import os
from pathlib import Path
import re

ROOT = Path(__file__).parent.parent
os.chdir(ROOT)

SKIP_DIRS = {".git", "node_modules", "images", "css", "js", "data", "reports", "docs", "templates", "research", "tools", "csv"}

MODERN_JS = [
    ("js/cookie-consent.js", "cookie-consent"),
    ("js/monetization.js", "monetization"),
    ("js/print-sheet.js", "print-sheet"),
    ("js/level-visuals.js", "level-visuals"),
    ("js/visual-learning.js", "visual-learning"),
    ("js/practice-api.js", "practice-api"),
    ("js/adaptive-practice.js", "adaptive-practice"),
    ("js/global-srs.js", "global-srs"),
    ("js/refresh-guard.js", "refresh-guard"),
    ("js/scroll-restore.js", "scroll-restore"),
    ("js/course-player.js", "course-player"),
]

def prefix_for(file_path):
    # file_path is Path relative to ROOT
    depth = len(file_path.parent.parts)
    return "../" * depth

def inject_into_file(path):
    try:
        content = path.read_text(encoding="utf-8")
    except:
        return False
    if "<html" not in content.lower():
        return False
    
    changed = False
    # Check if already has our markers
    for js_file, name in MODERN_JS:
        if js_file in content:
            continue
        # Determine prefix
        prefix = prefix_for(path.relative_to(ROOT))
        tag = f'<script src="{prefix}{js_file}" defer></script>'
        # Inject before </body> or before existing analytics
        if "</body>" in content:
            # Avoid injecting into pages that are explicitly no-ads or transactional?
            # Inject anyway for visual learning, but respect ad policy for monetization
            # For monetization, only inject if page is not INTERACTIVE_LEARNING? Actually monetization already handles that.
            # We'll inject all modern JS except monetization on INTERACTIVE_LEARNING? But monetization.js itself handles class.
            content = content.replace("</body>", f"{tag}\n</body>")
            changed = True
        else:
            continue
    
    if changed:
        path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    html_files = []
    for root, dirs, files in os.walk(ROOT):
        # Skip
        rel_root = Path(root).relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel_root.parts):
            continue
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if f.endswith(".html"):
                html_files.append(Path(root) / f)
    
    print(f"Found {len(html_files)} HTML files")
    changed = 0
    for p in html_files:
        if inject_into_file(p):
            changed += 1
    print(f"Injected modern JS into {changed} files")

if __name__ == "__main__":
    main()
