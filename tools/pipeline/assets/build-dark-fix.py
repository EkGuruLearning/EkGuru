#!/usr/bin/env python3
"""Dark-mode safety net — generated overrides for hard-coded light colours.

WHY
---
The theme is token-driven ([data-theme="dark"] swaps --bg/--card/--ink…), but
~200 rules across the stylesheets still say `background:#fff` or `color:#222`
literally. In dark mode those boxes keep a white background while the text
inside inherits the light --ink, so a real person sees a white box with
white text (owner report, 17 Nov 2026: "dark mode me text/box visible nahi").

WHAT IT DOES
------------
Walks every stylesheet, and for every rule outside an existing dark-theme
scope that hard-codes
  · a LIGHT background (white, #fff, #f5f5f5, rgba(255,255,255,.9), a
    light gradient)  → emits  [data-theme="dark"] SEL { background: var(--card) }
  · a DARK text colour (#000…#3xx, black)
                     → emits  [data-theme="dark"] SEL { color: var(--ink) }
  · a LIGHT border colour → border-color: var(--line)
inside the same @media / @supports context, and writes the result between
    /* EKGURU_DARK_FIX */ … /* /EKGURU_DARK_FIX */
at the end of css/style.min.css — the one stylesheet every page loads. The
attribute prefix adds specificity, so the override wins regardless of which
page-specific stylesheet declared the literal.

Rules that set BOTH a dark background and a light text colour (a real dark
badge) are left alone; rules already scoped to a dark theme are skipped.

Idempotent. `--check` exits 1 when the block is stale. Run:
    python3 tools/build-dark-fix.py [--check]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BUNDLE = ROOT / "css" / "style.min.css"
START = "/* EKGURU_DARK_FIX */"
END = "/* /EKGURU_DARK_FIX */"
SOURCES = [
    "css/style.min.css", "css/modern-fix.css", "css/storybook.css", "css/book-mode.css",
    "css/foundation.css", "css/world-redesign.css", "css/home-future.css", "css/ultra.css",
    "css/support-razorpay.css",
    # JS that injects its own <style> text (the course player, print sheets…)
    "js/course-player.js", "js/hindi-tools.js", "js/level-visuals.js", "js/cookie-consent.js",
    "js/monetization.js", "js/copywatch.js",
]


def css_from_js(src: str) -> str:
    """CSS carried in JS string literals: every quoted string that looks like
    `selector{prop:value}` is concatenated. Good enough for the injected
    stylesheets this repo writes (one rule block per literal)."""
    out = []
    for m in re.finditer(r'"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'', src):
        lit = m.group(1) if m.group(1) is not None else m.group(2)
        if "{" in lit and "}" in lit and ":" in lit and not lit.lstrip().startswith("<"):
            out.append(lit.replace('\\"', '"').replace("\\'", "'"))
    return "\n".join(out)

DARK_SCOPE = re.compile(r'data-theme=\\?["\']?(dark|contrast)|\.theme-dark|prefers-color-scheme:\s*dark', re.I)


def strip_comments(css: str) -> str:
    return re.sub(r"/\*[\s\S]*?\*/", "", css)


def parse_rules(css: str):
    """Yield (context_stack, selector, declarations) for every style rule."""
    i, n = 0, len(css)
    stack: list[str] = []
    buf = ""
    while i < n:
        ch = css[i]
        if ch == "{":
            head = buf.strip()
            buf = ""
            if head.startswith("@"):
                name = head.split("(")[0].split()[0].lower()
                if name in ("@media", "@supports", "@container", "@layer"):
                    stack.append(head)
                    i += 1
                    continue
                # @keyframes / @font-face / @page: skip the whole block
                depth = 1
                i += 1
                while i < n and depth:
                    if css[i] == "{":
                        depth += 1
                    elif css[i] == "}":
                        depth -= 1
                    i += 1
                continue
            # style rule: read until the matching close brace
            j = css.find("}", i + 1)
            if j == -1:
                break
            decls = css[i + 1:j]
            yield list(stack), head, decls
            i = j + 1
            continue
        if ch == "}":
            if stack:
                stack.pop()
            buf = ""
            i += 1
            continue
        buf += ch
        i += 1


HEX = re.compile(r"#([0-9a-f]{3}|[0-9a-f]{6})\b", re.I)


def luminance_of_hex(h: str) -> float:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[k:k + 2], 16) / 255 for k in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def colour_lum(value: str):
    """Perceived luminance of the FIRST solid colour in a value, or None."""
    v = value.strip().lower()
    if "gradient(" in v:
        # a gradient is "light" when every solid stop in it is pale
        # (linear-gradient(180deg,#fff,color-mix(… var(--x) 65%,#fff))):
        # the var() stops are tints of white, so the box reads white.
        lums = [luminance_of_hex(m.group(0)) for m in HEX.finditer(v)]
        for m in re.finditer(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([0-9.]+))?\s*\)", v):
            if not m.group(4) or float(m.group(4)) >= 0.55:
                lums.append(sum(c * int(m.group(k)) / 255 for c, k in ((0.2126, 1), (0.7152, 2), (0.0722, 3))))
        if lums and min(lums) >= 0.82:
            return max(lums)
        return None
    if re.search(r"\bvar\(", v):
        return None
    if re.match(r"^(white|#fff\b|#ffffff\b)", v):
        return 1.0
    if re.match(r"^(black|#000\b|#000000\b)", v):
        return 0.0
    m = re.search(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([0-9.]+))?\s*\)", v)
    if m:
        a = float(m.group(4)) if m.group(4) else 1.0
        if a < 0.55:
            return None
        r, g, b = (int(m.group(k)) / 255 for k in (1, 2, 3))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    m = HEX.search(v)
    if m:
        return luminance_of_hex(m.group(0))
    return None


def colour_sat(value: str):
    """Rough HSL saturation of the first solid colour (0 = neutral grey/white)."""
    v = value.strip().lower()
    m = re.search(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", v)
    if m:
        r, g, b = (int(m.group(k)) / 255 for k in (1, 2, 3))
    else:
        m = HEX.search(v)
        if v.startswith("white"):
            return 0.0
        if not m:
            return 0.0
        h = m.group(0).lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        r, g, b = (int(h[k:k + 2], 16) / 255 for k in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    if mx == mn:
        return 0.0
    l = (mx + mn) / 2
    return (mx - mn) / (1 - abs(2 * l - 1)) if l not in (0, 1) else 0.0


SKIP_SEL = re.compile(r"::?(before|after|selection|placeholder|-webkit-|-moz-)|print|-dot\b|\.dot\b|-knob|-thumb|toggle|-loading|\bi:nth-child|\.sb-scene\b", re.I)  # .sb-scene = illustrated sky, keep the artwork
PAGE_SEL = re.compile(r"^(html|body|main|\.wrap|\.pw|\.pw-legacy|\.pw-tool|\.art|\.xp-page|\.xp-main|\.courses-page|\.country-theme)(\[[^\]]*\]|\.[a-z0-9_-]+)*$")
LINK_SEL = re.compile(r"(^|[\s>+~])a(:[a-z-]+)?$")


def declarations(decls: str):
    out = {}
    for part in decls.split(";"):
        if ":" not in part:
            continue
        k, _, val = part.partition(":")
        k = k.strip().lower()
        val = val.strip()
        if val.endswith("!important"):
            val = val[:-10].strip()
        out[k] = val
    return out


def scope_one(selector: str, theme: str) -> str:
    s = selector.strip()
    if s.startswith(":root"):
        return ':root[data-theme="%s"]' % theme + s[5:]
    if re.match(r"^html\b", s):
        return 'html[data-theme="%s"]' % theme + s[4:]
    return '[data-theme="%s"] ' % theme + s


def scope(selector: str) -> str:
    """Prefix one selector with the dark AND the contrast theme attribute:
    the contrast theme is black-on-black-surface and needs every light-box
    override the dark theme needs (the 17 Nov 2026 real-browser audit found
    white cards under white ink on /contact/, /support/ and the worksheet
    sample in contrast mode)."""
    return scope_one(selector, "dark") + "," + scope_one(selector, "contrast")


def build_block(sources) -> str:
    seen = set()
    by_context: dict[str, list[str]] = {}
    texts = []
    for src in sources:
        p = ROOT / src
        if not p.exists():
            continue
        css = p.read_text(encoding="utf-8")
        if src.endswith(".js"):
            css = css_from_js(css)
        if src.endswith("style.min.css") and START in css:
            css = css.split(START)[0] + css.split(END, 1)[-1] if END in css else css.split(START)[0]
        texts.append(strip_comments(css))

    # Deliberate dark-theme rules already in the sources win: remember which
    # (selector, property) pairs they cover so no generated rule out-ranks them.
    covered = set()
    for css in texts:
        for ctx, sel, decls in parse_rules(css):
            if not (DARK_SCOPE.search(sel) or any(DARK_SCOPE.search(c) for c in ctx)):
                continue
            d = declarations(decls)
            for one in sel.split(","):
                base = re.sub(r'^\s*(html|:root)?\[data-theme=\\?["\']?(dark|contrast)\\?["\']?\]\s*', "", one.strip())
                base = re.sub(r"\s+", " ", base).strip()
                for prop in d:
                    covered.add((base, "background" if prop.startswith("background") else prop))

    for css in texts:
        for ctx, sel, decls in parse_rules(css):
            if DARK_SCOPE.search(sel) or any(DARK_SCOPE.search(c) for c in ctx):
                continue
            if any("print" in c for c in ctx):
                continue
            if sel.startswith("@") or "%" in sel and not sel.strip().startswith("."):
                continue
            if SKIP_SEL.search(sel):
                continue
            d = declarations(decls)
            bg = d.get("background-color") or d.get("background")
            bg_lum = colour_lum(bg) if bg else None
            fg = d.get("color")
            fg_lum = colour_lum(fg) if fg else None
            bd = d.get("border-color") or (d.get("border") if d.get("border") and HEX.search(d.get("border")) else None)
            bd_lum = colour_lum(HEX.search(bd).group(0)) if bd and HEX.search(bd) else None
            fixes = []
            light_bg = bg_lum is not None and bg_lum >= 0.82
            # a pale near-white tint (#f5f2ff, #e7f6ec…) reads as "white box"
            # in dark mode; only a clearly coloured pale box keeps its tint
            tinted_bg = light_bg and colour_sat(bg) >= 0.18 and bg_lum <= 0.9
            dark_bg = bg_lum is not None and bg_lum <= 0.35
            dark_fg = fg_lum is not None and fg_lum <= 0.35
            light_fg = fg_lum is not None and fg_lum >= 0.82
            first = re.sub(r"\s+", " ", sel.split(",")[0].strip())
            is_page = bool(PAGE_SEL.match(first))
            is_link = bool(LINK_SEL.search(first))
            bg_covered = (first, "background") in covered
            fg_covered = (first, "color") in covered
            if light_bg and not bg_covered:
                if tinted_bg:
                    # a pale green/red/yellow box carries meaning (quiz right/
                    # wrong, warnings): keep the tint, force readable dark text
                    if not fg_covered:
                        fixes.append("color:var(--eg-accent-contrast,#171020)")
                else:
                    fixes.append("background:var(--bg,#131020)" if is_page else "background:var(--card,#211b32)")
                    if "background-image" in d and "gradient" in d["background-image"]:
                        fixes.append("background-image:none")
                    if light_fg and not fg_covered:
                        fixes.append("color:var(--ink,#f8f5ff)")
            if dark_fg and not dark_bg and not tinted_bg and not fg_covered:
                fixes.append("color:var(--brand,#c4b5fd)" if is_link else "color:var(--ink,#f8f5ff)")
            if bd_lum is not None and bd_lum >= 0.82 and not dark_bg and (first, "border-color") not in covered:
                fixes.append("border-color:var(--line,#9887ad)")
            if not fixes:
                continue
            sels = [scope(x) for x in sel.split(",") if x.strip()]
            key = (tuple(ctx), ",".join(sels), ";".join(fixes))
            if key in seen:
                continue
            seen.add(key)
            ctx_key = "".join(c + "{" for c in ctx)
            by_context.setdefault(ctx_key, []).append(",".join(sels) + "{" + ";".join(fixes) + "}")
    # Inline styles (generated worksheets, admin panels) cannot be reached by
    # a class rule; attribute selectors + !important are the only handle.
    INLINE = [
        ('[style*="background:#fff"]', "background:var(--card,#211b32)!important"),
        ('[style*="background:#f6f4ff"]', "background:var(--bg,#131020)!important"),
        ('[style*="background:#eef0f6"]', "background:var(--card,#211b32)!important"),
        ('[style*="background:#f5f6f8"]', "background:var(--card,#211b32)!important"),
        ('[style*="color:#10131f"]', "color:var(--ink,#f8f5ff)!important"),
        ('[style*="color:#5f6577"]', "color:var(--muted,#c5b8d7)!important"),
    ]
    by_context.setdefault("", []).extend(scope(a) + "{" + b + "}" for a, b in INLINE)
    parts = []
    for ctx_key, rules in by_context.items():
        body = "".join(rules)
        parts.append(ctx_key + body + "}" * ctx_key.count("{"))
    return START + "\n" + "\n".join(parts) + "\n" + END + "\n"


def main() -> int:
    check = "--check" in sys.argv
    current = BUNDLE.read_text(encoding="utf-8")
    block = build_block(SOURCES)
    if START in current:
        if END not in current:
            raise SystemExit("ERROR: dark-fix start marker without end marker")
        head = current.split(START, 1)[0]
        tail = current.split(END, 1)[1].lstrip("\n")
        new = head + block + tail
    else:
        new = current + ("" if current.endswith("\n") else "\n") + block
    n_rules = block.count("{") - block.count("@media") - block.count("@supports")
    if new == current:
        print("dark-fix: current (%d override rules)" % n_rules)
        return 0
    if check:
        print("STALE css/style.min.css dark-fix block — run tools/build-dark-fix.py")
        return 1
    BUNDLE.write_text(new, encoding="utf-8")
    print("dark-fix: wrote %d override rules into css/style.min.css" % n_rules)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
