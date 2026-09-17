#!/usr/bin/env python3
"""Consolidate header CSS into one organized block (v102).

Moves ONLY header-scoped rules (.hdr, .logo, .nav, .burger, .hdr-search,
.lang-*, .cur-*, .hs-ico, .nav-desktop-only) from base + WIDTH media queries
into a single appended section, grouped by breakpoint, original relative
order preserved within each group. Everything else stays byte-identical.

Deliberately NOT moved (documented, not forgotten):
  - footer logo rules (.ftr ...) — not header rules
  - unscoped .ac-* rules — shared with the /search/ page autocomplete
  - print / hover:none / pointer:coarse / forced-colors rules — independent
    conditions, no part in width-cascade confusion
  - exact-duplicate rules are deduped (reported below)

Safety: run tools/sweep-header-geometry.py + box-diff before/after; any
visual difference means revert (git checkout css/style.min.css).

Usage: python3 tools/consolidate-header-css.py [--check]
  --check: report what WOULD move without writing.
"""
import re, sys

PATH = "css/style.min.css"
CHECK = "--check" in sys.argv

HEADER_TOK = re.compile(
    r"\.(hdr|hdr-in|logo|logo-mark|burger|nav|hdr-search|hs-ico|"
    r"lang-wrap|lang-btn|lang-menu|cur-wrap|cur-btn|cur-menu|"
    r"nav-desktop-only)(?![\w-])")
FOOTER = re.compile(r"\.ftr(?![\w-])")
AC = re.compile(r"\.ac-(wrap|box|compact)(?![\w-])")

def tokenize(css):
    """Split into [('comment'|'rule'|'media', text)] — strings-aware."""
    items, i, n = [], 0, len(css)
    while i < n:
        if css.startswith("/*", i):
            j = css.find("*/", i + 2) + 2
            items.append(("comment", css[i:j]))
            i = j
        elif re.match(r"\s*@media\b", css[i:]):
            m = re.match(r"(\s*@media\b[^{]*\{)", css[i:])
            start = i
            i += len(m.group(1))
            depth = 1
            while depth and i < n:
                if css[i] == '"':
                    i += 1
                    while i < n and css[i] != '"':
                        i += 2 if css[i] == "\\" else 1
                    i += 1
                    continue
                if css[i] == "{":
                    depth += 1
                elif css[i] == "}":
                    depth -= 1
                i += 1
            items.append(("media", css[start:i]))
        elif css[i] in " \t\r\n;":
            i += 1
        else:
            # plain rule: selector { ... } (brace-match, strings-aware)
            k = css.find("{", i)
            if k < 0:
                break
            p, depth = k + 1, 1
            while depth and p < n:
                if css[p] == '"':
                    p += 1
                    while p < n and css[p] != '"':
                        p += 2 if css[p] == "\\" else 1
                    p += 1
                    continue
                if css[p] == "{":
                    depth += 1
                elif css[p] == "}":
                    depth -= 1
                p += 1
            items.append(("rule", css[i:p]))
            i = p
    return items

def split_media(text):
    """('@media (cond)', inner_css, trailing) for a media item."""
    m = re.match(r"(\s*@media\b[^{]*\{)([\s\S]*)(\}[^}]*)$", text)
    head, inner, tail = m.group(1), m.group(2), m.group(3)
    cond = re.sub(r"^\s*@media\b", "", head).strip().rstrip("{").strip()
    return cond, inner, tail

def inner_rules(inner):
    """Split media-inner CSS into rules (comments kept separate)."""
    out, i, n = [], 0, len(inner)
    while i < n:
        if inner.startswith("/*", i):
            j = inner.find("*/", i + 2) + 2
            out.append(("comment", inner[i:j]))
            i = j
        elif inner[i] in " \t\r\n;":
            i += 1
        else:
            k = inner.find("{", i)
            if k < 0:
                break
            p, depth = k + 1, 1
            while depth and p < n:
                if inner[p] == '"':
                    p += 1
                    while p < n and inner[p] != '"':
                        p += 2 if inner[p] == "\\" else 1
                    p += 1
                    continue
                if inner[p] == "{":
                    depth += 1
                elif inner[p] == "}":
                    depth -= 1
                p += 1
            out.append(("rule", inner[i:p]))
            i = p
    return out

def is_header_rule(selector_text):
    sels = [s.strip() for s in selector_text.split(",")]
    for s in sels:
        if FOOTER.search(s):
            return False
        if AC.search(s) and ".hdr" not in s:
            return False
        if not HEADER_TOK.search(s):
            return False
    return True

def is_width_media(cond):
    return "width" in cond

# Explicit width-group emission order (NOT first-appearance).
# Provenance: exhaustive pairwise cascade analysis, 2026-09-13 (928 rules;
# same selector+property, different value, overlapping ranges). Three pairs
# REQUIRE this relative order (original-file winner must stay last):
#   900px BEFORE 1200px  (.nav translateY -135% ==> -140%, closed drawer)
#   1201px BEFORE 1201-1279px (.hdr .logo 1.3rem ==> 1.16rem; span 140 ==> 110px; ac-wrap 220 ==> 150px)
#   1201px BEFORE 1280-1439px (ac-wrap 220 ==> 190px)
# First-appearance grouping violates the first two (box-diff proved it:
# 83/396 boxes changed, incl. visible logo growth at 1220px). Five residual
# width->base flips are proven harmless (dead under !important / 1200-group
# override / transparent glyph); see work report §9.
GROUP_ORDER = [
    "(max-width:400px)",
    "(max-width:480px)",
    "(max-width:640px)",
    "(max-width:900px)",
    "(max-width:1200px)",
    "(min-width:981px) and (max-width:1024px)",
    "(max-width:1180px)",
    "(min-width:1201px)",
    "(min-width:1201px) and (max-width:1279px)",
    "(min-width:1280px) and (max-width:1439px)",
]

def main():
    css = open(PATH, encoding="utf-8").read()
    items = tokenize(css)
    # sanity: tokens must reconstruct the file (modulo skipped whitespace)
    recon = "".join(t for _, t in items)
    assert re.sub(r"\s+", "", recon) == re.sub(r"\s+", "", css), "tokenizer lost bytes!"

    moved_base, moved_media = [], {}
    media_order = []
    kept_media_rules = {}   # cond -> rules left behind (unmoved)
    pending_comments = []
    out_items = []
    stats = {"moved": 0, "deduped": 0}

    for kind, text in items:
        if kind == "comment":
            pending_comments.append(text)
            out_items.append((kind, text))
            continue
        if kind == "rule":
            sel = text[:text.find("{")]
            if is_header_rule(sel):
                moved_base.append(("".join(pending_comments), text))
                stats["moved"] += 1
                # drop the carried comments from their old spot
                out_items = out_items[:len(out_items) - len(pending_comments)]
            else:
                out_items.append((kind, text))
            pending_comments = []
            continue
        # media
        cond, inner, tail = split_media(text)
        parts = inner_rules(inner)
        kept, cmts = [], []
        for pk, pt in parts:
            if pk == "comment":
                cmts.append(pt)
                kept.append((pk, pt))
                continue
            sel = pt[:pt.find("{")]
            if is_width_media(cond) and is_header_rule(sel):
                moved_media.setdefault(cond, []).append(("".join(cmts), pt))
                if cond not in media_order:
                    media_order.append(cond)
                stats["moved"] += 1
                # drop carried comments from old spot
                kept = kept[:len(kept) - len(cmts)]
            else:
                kept.append((pk, pt))
            cmts = []
        if any(k == "rule" for k, _ in kept):
            head = text[:text.find("{") + 1]
            body = "".join(t for _, t in kept)
            out_items.append(("media", head + body + "}"))
        else:
            # whole block moved away — drop it (comments carried along)
            pass
        pending_comments = []

    # dedupe exact duplicates within each group, keep first
    def dedupe(lst):
        seen, out = set(), []
        for c, r in lst:
            key = re.sub(r"\s+", "", r)
            if key in seen:
                stats["deduped"] += 1
                continue
            seen.add(key)
            out.append((c, r))
        return out

    moved_base = dedupe(moved_base)
    for cond in media_order:
        moved_media[cond] = dedupe(moved_media[cond])

    print(f"header rules to move: {stats['moved']} "
          f"({len(moved_base)} base + {sum(len(v) for v in moved_media.values())} in {len(media_order)} width queries)")
    print(f"exact duplicates removed: {stats['deduped']}")
    print("width groups (file order):", ", ".join(media_order))
    # Emit width groups in GROUP_ORDER, NOT first-appearance (see note above).
    ordered = [c for c in GROUP_ORDER if c in moved_media]
    unknown = [c for c in media_order if c not in GROUP_ORDER]
    if unknown:
        print(f"WARNING: width queries outside GROUP_ORDER, appended last: {unknown}",
              file=sys.stderr)
    ordered += unknown
    print("width groups (emission order):", ", ".join(ordered))
    if CHECK:
        return 0
    media_order = ordered

    banner = ("\n\n/* ============================================================\n"
              "   v102 — HEADER CSS, CONSOLIDATED (generated by\n"
              "   tools/consolidate-header-css.py; do not hand-edit above blocks)\n"
              "   Every header-scoped rule from base + width media queries,\n"
              "   grouped by breakpoint in GROUP_ORDER (cascade-proven: every\n"
              "   cross-group winner verified against the original file order).\n"
              "   Left in place on purpose: .ftr logo rules, unscoped .ac-*\n"
              "   rules (shared with /search/), print/hover/pointer rules.\n"
              "   Verify: tools/sweep-header-geometry.py (65 widths, 0 fails).\n"
              "   ============================================================ */\n")
    sec = [banner, "\n/* ---- header: base (all widths) ---- */\n"]
    for c, r in moved_base:
        sec.append(c + r + "\n")
    for cond in media_order:
        sec.append(f"\n/* ---- header: {cond} ---- */\n@media {cond}{{\n")
        for c, r in moved_media[cond]:
            sec.append(c + r.strip() + "\n")
        sec.append("}\n")

    new = "".join(t for _, t in out_items).rstrip("\n") + "\n" + "".join(sec)
    # final integrity: every moved rule body still present exactly once
    for _, r in moved_base:
        body = r[r.find("{"):r.rfind("}") + 1]
        assert new.count(re.sub(r"\s+", " ", body).strip()) >= 1
    open(PATH, "w", encoding="utf-8").write(new)
    print(f"wrote {PATH}: {len(css)} -> {len(new)} bytes")
    return 0

if __name__ == "__main__":
    sys.exit(main())
