#!/usr/bin/env python3
"""Own the question-api tag on explicit question-rendering pages only.

The check mode is read-only. Generic course bundle consumers are deliberately
not targets: a shared bundle does not prove that a page renders questions.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "reports", "tools", "data", "research", "templates"}
MARK = "<!-- ekguru:questions-api -->"
BLOCK = re.compile(r"\s*<!-- ekguru:questions-api -->\s*<script\b[^>]*\bsrc=[\"'](?:\.\./)*js/question-api\.js[\"'][^>]*>\s*</script>", re.I)
SCRIPT = re.compile(r"<script\b[^>]*>", re.I)
SRC = re.compile(r"\bsrc=[\"']([^\"']+)[\"']", re.I)


def pages() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.html")
                  if not any(part in SKIP or part.startswith(".") for part in p.relative_to(ROOT).parts[:-1]))


def scripts(text: str) -> list[tuple[int, str]]:
    out = []
    for tag in SCRIPT.finditer(text):
        src = SRC.search(tag.group(0))
        if src:
            out.append((tag.start(), src.group(1)))
    return out


def eligible(rel: str, assets: list[str]) -> bool:
    names = {a.rsplit("/", 1)[-1] for a in assets}
    if "hindi-tools.js" in names or "practice-engine.js" in names:
        return True
    if re.fullmatch(r"languages/[^/]+/(?:quiz|review)/index\.html", rel):
        return any(re.fullmatch(r"course-[a-z-]+\.js", name) for name in names)
    return rel == "toolbox/hindi-quiz/index.html"


def desired(path: Path, html: str) -> tuple[str, bool]:
    rel = path.relative_to(ROOT).as_posix()
    clean = BLOCK.sub("", html)
    clean = re.sub(r"\s*<script\b[^>]*\bsrc=[\"'](?:\.\./)*js/question-api\.js[\"'][^>]*>\s*</script>", "", clean, flags=re.I)
    found = scripts(clean)
    assets = [src for _, src in found]
    target = eligible(rel, assets)
    if not target:
        return clean, False

    preferred = ["hindi-tools.js", "practice-engine.js"]
    anchor = None
    prefix = ""
    for wanted in preferred:
        for at, src in found:
            if src.rsplit("/", 1)[-1] == wanted:
                anchor, prefix = at, src[:-len("js/" + wanted)] if src.endswith("js/" + wanted) else ""
                break
        if anchor is not None:
            break
    if anchor is None:
        # World-course quiz/review or the self-contained toolbox quiz: place it
        # beside the first local runtime script near the end of the page.
        candidates = [(at, src) for at, src in found if "/js/" in src or src.startswith("js/")]
        anchor, src = candidates[-1] if candidates else (clean.lower().rfind("</body>"), "")
        m = re.match(r"((?:\.\./)*)js/", src)
        prefix = m.group(1) if m else ""
    tag = f'{MARK}\n<script src="{prefix}js/question-api.js" defer></script>\n'
    return clean[:anchor] + tag + clean[anchor:], True


def main() -> int:
    check = "--check" in sys.argv
    stale, targets, updated = [], 0, 0
    for path in pages():
        old = path.read_text(encoding="utf-8", errors="replace")
        new, target = desired(path, old)
        targets += int(target)
        if new == old:
            continue
        if check:
            stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.write_text(new, encoding="utf-8")
            updated += 1
    if check and stale:
        print(f"STALE {len(stale)} page(s) — run: python3 tools/inject-questions-api.py")
        for path in stale[:10]:
            print("  " + path)
        return 1
    if check:
        print(f"ok    questions API on {targets} question page(s)")
    else:
        print(f"questions api: {updated} page(s) updated, {targets} question page(s) known")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
