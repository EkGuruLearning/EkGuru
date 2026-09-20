#!/usr/bin/env python3
"""The country figures: one picture per country, on every page about it.

Prakash: "visuals har subject/language/page pe honi chahiye, country theme ke
hisab se."

The level visuals answer "who is this level for" with a person whose age IS the
level. A country page needs the other half: what the country actually sounds
like. So every country gets one figure — a plate in the page's own colour,
carrying the country's name, its name in its own language, its region, the
official languages written in their own scripts, and two honest numbers: how
many languages are documented for that country on this site, and how many of
them EkGuru can actually teach today.

  · the colour is derived from the country code (the same rule the course cards
    use for their accent). It is NOT presented as the flag: a flag is a
    specific thing and a generated gradient that imitates one would be a lie on
    390 pages.
  · the languages come from data/global/language-country-relations.json — the
    same source the pages themselves are built from, so the picture and the
    text under it cannot disagree.
  · the taught count comes from data/courses/index.json. A country where we
    teach nothing says so in the picture.
  · every figure is a plain SVG (2-4 KB), no fonts, no requests, text stays
    text: it is readable to a screen reader, a crawler and a printer.

Output:  images/vis/country-<cc>.svg          (one per country with a page)
         data/country-visuals.json            (the manifest: alt text, numbers)
         a block on every world-languages/<country>/ and
         learn-hindi-from-<country>/ page

Run:  python3 tools/build-country-visuals.py [--check]
"""

import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT = "images/vis"
MANIFEST = "data/country-visuals.json"
MARK_START = "<!-- ekguru:country-visuals:start -->"
MARK_END = "<!-- ekguru:country-visuals:end -->"

COUNTRIES = "tools/_countries-cache.json"
RELATIONS = "data/global/language-country-relations.json"
COURSES = "data/courses/index.json"

# The catalogue is keyed by ISO 639-1 and most relation rows carry it; six
# languages only appear under their ISO 639-3 id (the same bridge
# tools/build-course-hub.py uses).
ISO3_ALIAS = {"arb": "ar", "cmn": "zh", "fil": "fil", "npi": "npi",
              "uzn": "uzn", "zsm": "zsm"}

RTL_SCRIPTS = {"Arab", "Hebr", "Thaa", "Nkoo", "Syrc", "Adlm"}

# The slug the country pages use. Read from the page itself where possible —
# this is only the fallback for a country whose page has not been built.
SLUGS = {
    "AE": "uae", "GB": "uk", "US": "usa", "TR": "turkiye", "CI": "cote-divoire",
    "CD": "dr-congo", "CG": "congo", "CZ": "czechia", "KR": "south-korea",
    "KP": "north-korea", "LA": "laos", "MD": "moldova", "MK": "north-macedonia",
    "RU": "russia", "SZ": "eswatini", "VA": "vatican-city", "VN": "vietnam",
}


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def text_w(txt, size):
    """Roughly how wide a string will be drawn, in px, at this font size."""
    w = 0.0
    for ch in txt:
        if "\u0590" <= ch <= "\u08ff" or "\u0900" <= ch <= "\u0dff":
            w += size * 0.62          # Arabic, Hebrew, Indic
        elif "\u2e80" <= ch <= "\u9fff" or "\uff00" <= ch <= "\uffef":
            w += size * 1.0           # CJK
        else:
            w += size * 0.58
    return w


def fit_names(names, size, avail, sep=" \u00b7 "):
    """As many language names as fit on one plate line, and how many were left.

    A list truncated by character count runs off the plate when the names are
    wide (CJK) or right-to-left, so the line is measured instead."""
    kept = []
    for name, script in names:
        trial = sep.join([n for n, _ in kept] + [name])
        if kept and text_w(trial + " +99", size) > avail:
            break
        kept.append((name, script))
    if not kept:
        kept = names[:1]
    return kept, max(0, len(names) - len(kept))


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def theme(cc):
    """The country's own colour, from its code — stable, and never a flag."""
    h = int(hashlib.sha1(cc.encode()).hexdigest()[:6], 16)
    hue = h % 360
    return ("hsl(%d 58%% 34%%)" % hue, "hsl(%d 62%% 46%%)" % hue,
            "hsl(%d 70%% 95%%)" % hue)


def slug_of(cc, name):
    if cc in SLUGS:
        return SLUGS[cc]
    return re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")


def countries():
    cache = load(COUNTRIES, []) or []
    out = {}
    for c in cache:
        cc = c.get("cca2")
        if not cc:
            continue
        native = ""
        langs = (c.get("name") or {}).get("native") or {}
        for code, val in sorted(langs.items()):
            cand = (val or {}).get("common") or ""
            if cand and cand.strip() != (c["name"].get("common") or "").strip():
                native = cand
                break
        out[cc] = {
            "cc": cc,
            "name": (c.get("name") or {}).get("common") or cc,
            "native": native,
            "region": c.get("region") or "",
            "subregion": c.get("subregion") or "",
        }
    return out


def relations():
    rows = (load(RELATIONS, {}) or {}).get("relations", [])
    by = {}
    for r in rows:
        cc = r.get("country_id")
        if not cc:
            continue
        by.setdefault(cc, []).append(r)
    return by


def taught_codes():
    data = load(COURSES, {}) or {}
    return {c["code"] for c in data.get("courses", []) if c.get("levels")}


def figure(info, rows, taught):
    """One country, one plate: who it is, what it sounds like, what we teach."""
    a, b, tint = theme(info["cc"])
    official, spoken = [], []
    for r in rows:
        cat = (r.get("category") or "").upper()
        if cat in ("OFFICIAL", "NATIONAL"):
            official.append(r)
        elif cat in ("WIDELY_SPOKEN", "REGIONAL"):
            spoken.append(r)

    def uniq(rs):
        seen, out = set(), []
        for r in rs:
            key = (r.get("native_name") or r.get("language_name") or "").strip()
            if key and key not in seen:
                seen.add(key)
                out.append(r)
        return out

    official, spoken = uniq(official), uniq(spoken)
    headline = official or spoken[:4]

    def code_of(r):
        return r.get("iso_639_1") or ISO3_ALIAS.get(r.get("iso_639_3") or "")

    taught_here = {code_of(r) for r in official + spoken if code_of(r) in taught} - {None}
    documented = len({(r.get("native_name") or r.get("language_name") or "").strip()
                      for r in rows if (r.get("native_name") or r.get("language_name"))})

    # Up to four names in their own scripts, then a count.
    names, used = [], 0
    for r in headline:
        txt = (r.get("native_name") or r.get("language_name") or "").strip()
        if not txt:
            continue
        names.append((txt, r.get("script") or "Latn"))
        used += 1
        if used == 4:
            break
    more = max(0, len(headline) - len(names))

    native_line = " · ".join(esc(n) for n, _ in names) or "—"
    # A list that MIXES scripts (China: 普通话 · 粵語 · ئۇيغۇرچە) has one reading
    # direction, and it is the direction of the language it starts with. Before
    # this, one RTL language anywhere in the list flipped the whole line and the
    # Chinese names ran off the left edge.
    rtl = names[0][1] in RTL_SCRIPTS if names else False
    # A right-to-left string anchored "start" at x=18 runs off the left edge of
    # the plate; a left-to-right string anchored "end" at the right edge would
    # look like a mistake. Each line is anchored on the side it is read from.
    nat_rtl = any("\u0590" <= ch <= "\u08ff" for ch in info["native"])
    nat_x = '302" text-anchor="end' if nat_rtl else '78'
    nat_dir = ' direction="rtl"' if nat_rtl else ""
    region = info["subregion"] or info["region"] or ""

    who = "%s (%s)" % (info["name"], info["cc"])
    verb = "has" if len(taught_here) == 1 else "have"
    alt = ("%s: %s. %d language%s documented for this country, %d of them %s a "
           "course on EkGuru." % (who, ", ".join(n for n, _ in names) or "no official language listed",
                                  documented, "" if documented == 1 else "s",
                                  len(taught_here), verb))
    if not taught_here:
        alt = ("%s: %s. %d languages documented for this country; no course here yet — "
               "the page is the inventory, not the promise."
               % (who, ", ".join(n for n, _ in names) or "no official language listed", documented))

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="320" height="200" '
        'role="img" aria-label="%s" font-family="system-ui,-apple-system,Segoe UI,sans-serif">\n'
        '  <title>%s</title>\n'
        '  <rect width="320" height="200" rx="14" fill="%s" stroke="%s" stroke-width="1"/>\n'
        '  <rect width="320" height="72" rx="14" fill="%s"/>\n'
        '  <rect y="58" width="320" height="14" fill="%s"/>\n'
        '  <circle cx="46" cy="36" r="20" fill="#fff" opacity=".92"/>\n'
        '  <text x="46" y="43" text-anchor="middle" font-size="17" font-weight="700" fill="%s">%s</text>\n'
        '  <text x="78" y="32" font-size="16" font-weight="700" fill="#fff">%s</text>\n'
        '  <text x="%s" y="52" font-size="12" fill="#fff" opacity=".92"%s>%s</text>\n'
        '  <text x="18" y="94" font-size="11" letter-spacing=".08em" fill="%s">%s</text>\n'
        '  <text x="%s" y="122" font-size="%d" fill="#1c1b42"%s>%s</text>\n'
        '  <text x="18" y="150" font-size="11" fill="%s">%s</text>\n'
        '  <text x="18" y="176" font-size="12" font-weight="600" fill="%s">%s</text>\n'
        '</svg>\n')

    label = "OFFICIAL LANGUAGES" if official else "MAIN LANGUAGES"
    nums = ("%d documented · %d taught here" % (documented, len(taught_here))
            if taught_here else
            "%d documented · no course here yet" % documented)
    avail = 320 - 18 - 8
    list_size = 15
    kept = names
    for size in (15, 13, 12, 11, 10):
        kept, dropped = fit_names(names, size, avail)
        list_size = size
        if not dropped:
            break
    more = dropped
    rtl = kept[0][1] in RTL_SCRIPTS if kept else rtl
    lang_x = '302" text-anchor="end' if rtl else '18'
    native_line = " · ".join(esc(n) for n, _ in kept) or "—"

    name_size = 15
    while name_size > 10 and text_w(native_line, name_size) > avail:
        name_size -= 1

    native_avail = 320 - 78 - 10
    native_name = info["native"]
    while len(native_name) > 6 and text_w(native_name, 12) > native_avail:
        native_name = native_name[:-2]
    if native_name != info["native"]:
        native_name = native_name.rstrip() + "…"
    return svg % (
        esc(alt), esc(alt), tint, a,
        b, b,
        a, esc(info["cc"]),
        esc(info["name"][:22]),
        nat_x, nat_dir, esc(native_name),
        a, esc(label),
        lang_x, list_size,
        ' direction="rtl"' if rtl else "",
        native_line + ((" +%d" % more) if more else ""),
        "#5b5876", esc(region + (" · %s" % info["region"] if info["region"] and info["subregion"] and info["region"] != info["subregion"] else "")),
        a, esc(nums),
    )


def block(info, fig, taught_names, documented):
    """The figure on the page, with the sentence that explains what it means.

    The counts are also written into the markup as data attributes: a caption is
    prose and prose can drift, so the test compares the attributes against the
    manifest and the manifest against the source data."""
    if taught_names:
        visible = ", ".join(taught_names)
        said = ("Published course levels are currently available for %s%s; check the course "
                "catalogue for each exact range."
                % (visible,
                   (" and %d other documented language%s" %
                    (fig["taught"] - len(taught_names), "" if fig["taught"] - len(taught_names) == 1 else "s"))
                   if fig["taught"] > len(taught_names) else ""))
    else:
        said = ("No published course level is linked from this research record yet.")
    return (
        MARK_START + "\n"
        '<section class="ct-visual" data-documented="%d" data-taught="%d" '
        'aria-labelledby="ct-visual-h">\n'
        '<h2 id="ct-visual-h">%s, in one picture</h2>\n'
        "<p>The panel below is generated from the same data as the list under it: the "
        "official languages in their own scripts, how many languages are documented for "
        "%s, and how many of them can be learned here today. The colour is the page’s own — "
        "this site gives every country a colour from its code, and it is not meant to be "
        "the flag.</p>\n"
        '<figure class="ct-fig"><img src="/%s" width="320" height="200" '
        'loading="lazy" decoding="async" alt="%s"><figcaption><b>%s</b> · %s — '
        "%d language%s documented, %s "
        '<a href="/courses/by-country/#country-%s">Courses for %s →</a></figcaption></figure>\n'
        "</section>\n" % (
            documented, fig["taught"],
            esc(info["name"]), esc(info["name"]),
            fig["path"], esc(fig["alt"]),
            esc(info["name"]),
            esc(info["subregion"] or info["region"] or "world"),
            documented, "" if documented == 1 else "s",
            said, info["cc"].lower(), esc(info["name"]))
        + MARK_END + "\n")


def splice(path, html_block, check):
    if not os.path.exists(path):
        return "missing"
    original = open(path, encoding="utf-8").read()
    html = original
    if MARK_START in html:
        start = html.index(MARK_START)
        end = html.index(MARK_END) + len(MARK_END)
        html = html[:start] + html[end:]
    if "<!-- ekguru:pw-bands:start -->" in html:
        anchor = html.index("<!-- ekguru:pw-bands:start -->")
    else:
        anchor = html.rfind("</main>")
    if anchor < 0:
        anchor = html.find("<!-- ekguru:shell-footer:start -->")
    if anchor < 0:
        return "no anchor"
    new = html[:anchor].rstrip("\n") + "\n" + html_block + html[anchor:]
    if new != original:
        if check:
            print("STALE %s — run tools/build-country-visuals.py" % path)
            return "stale"
        open(path, "w", encoding="utf-8").write(new)
        return "wrote"
    return "ok"


def main():
    check = "--check" in sys.argv
    info_map = countries()
    rel = relations()
    taught = taught_codes()
    os.makedirs(OUT, exist_ok=True)

    manifest = {"version": 1, "generated_note": "generated by tools/build-country-visuals.py",
                "countries": {}, "figures": {}}
    written = pages = 0
    stale = 0
    for cc in sorted(info_map):
        info = info_map[cc]
        rows = rel.get(cc) or []
        if not rows:
            continue
        slug = slug_of(cc, info["name"])
        page = "world-languages/%s/index.html" % slug
        sibling = "learn-hindi-from-%s/index.html" % slug
        if not (os.path.exists(page) or os.path.exists(sibling)):
            continue

        fig = {"path": "%s/country-%s.svg" % (OUT, cc.lower()), "country": cc,
               "name": info["name"], "region": info["region"],
               "subregion": info["subregion"], "slug": slug,
               "alt": "", "documented": 0, "taught": 0}
        svg = figure(info, rows, taught)
        alt = re.search(r'aria-label="([^"]*)"', svg)
        fig["alt"] = alt.group(1) if alt else info["name"]
        official = [r for r in rows if (r.get("category") or "").upper() in ("OFFICIAL", "NATIONAL")]
        spoken = [r for r in rows if (r.get("category") or "").upper() in ("WIDELY_SPOKEN", "REGIONAL")]
        seen = set()
        documented = 0
        for r in rows:
            key = (r.get("native_name") or r.get("language_name") or "").strip()
            if key and key not in seen:
                seen.add(key)
                documented += 1
        code_of = lambda r: r.get("iso_639_1") or ISO3_ALIAS.get(r.get("iso_639_3") or "")
        fig["documented"] = documented
        taught_rows = [r for r in official + spoken if code_of(r) in taught]
        seen_t, names = set(), []
        for r in taught_rows:
            code = code_of(r)
            if code in seen_t:
                continue
            seen_t.add(code)
            names.append((r.get("language_name") or code).strip())
        fig["taught"] = len(seen_t)
        fig["taught_names"] = names[:3]
        manifest["countries"][cc] = {"name": info["name"], "slug": slug,
                                     "region": info["region"], "subregion": info["subregion"]}
        manifest["figures"][cc] = fig

        if os.path.exists(fig["path"]) and open(fig["path"], encoding="utf-8").read() == svg:
            pass
        elif check:
            print("STALE %s — run tools/build-country-visuals.py" % fig["path"])
            stale += 1
        else:
            with open(fig["path"], "w", encoding="utf-8") as f:
                f.write(svg)
            written += 1

        page_block = block(info, fig, fig["taught_names"], documented)
        for p in (page, sibling):
            res = splice(p, page_block, check)
            if res == "wrote":
                pages += 1
            elif res == "stale":
                stale += 1

    body = json.dumps(manifest, indent=1, ensure_ascii=False, sort_keys=True) + "\n"
    if os.path.exists(MANIFEST) and open(MANIFEST, encoding="utf-8").read() == body:
        pass
    elif check:
        print("STALE %s — run tools/build-country-visuals.py" % MANIFEST)
        stale += 1
    else:
        with open(MANIFEST, "w", encoding="utf-8") as f:
            f.write(body)
        written += 1

    if check:
        print("ok    country visuals: %d figure(s), %d page(s) %s"
              % (len(manifest["figures"]), pages, "(stale: %d)" % stale if stale else ""))
        return 1 if stale else 0
    print("country visuals: %d svg file(s) + manifest, %d page block(s) written — %d country(ies)"
          % (written, pages, len(manifest["figures"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
