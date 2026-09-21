#!/usr/bin/env python3
"""Write /courses/by-country/ — every country, and the languages we can teach for it.

    python3 tools/build-course-countries.py [--check]

Prakash: "course mai search fix kro course mai language ko country wise bi
search kr ske jo abhi work nahi kar raha."

The interactive hub (/courses/) answers that with a dropdown and a search box.
This page answers the same question for everyone else: a crawler, a reader with
JavaScript off, and a reader who wants to scan the whole map instead of typing
into a box. It is generated from the two files the rest of the course system
already uses —

    data/courses/index.json                  which courses exist
    data/global/language-country-relations.json   which countries they are for

— so a course added tomorrow appears here with its countries, and a country the
inventory documents but we have not written a course for is listed honestly in
its own section, with the request link. That second list is the build queue;
it is the answer to "aur course add karenge" that stays true by itself.

The page also carries a tiny client-side filter (type a country) that upgrades
the list without being required for it.

Run:  python3 tools/build-course-countries.py           # write
      python3 tools/build-course-countries.py --check   # compare (CI/gate)
"""
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

PAGE = "courses/by-country/index.html"
MARK = "<!-- ekguru:course-countries:start -->"
MARK_END = "<!-- ekguru:course-countries:end -->"

# Standard Arabic ships as "arb", Mandarin as "cmn" — the same bridge the
# player and the hub use, so all three agree on which language a course is.
ISO3_ALIAS = {"arb": "ar", "cmn": "zh", "fil": "fil", "npi": "npi",
              "uzn": "uzn", "zsm": "zsm"}


def esc(s):
    return (str(s if s is not None else "")
            .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def load():
    with open("data/courses/index.json", encoding="utf-8") as f:
        courses = json.load(f)["courses"]
    with open("data/global/language-country-relations.json", encoding="utf-8") as f:
        relations = json.load(f).get("relations", [])
    names = {}
    try:
        with open("tools/_countries-cache.json", encoding="utf-8") as f:
            for c in json.load(f):
                code = c.get("cca2")
                if code:
                    names[code] = (c.get("name") or {}).get("common") or code
    except Exception:
        pass
    return courses, relations, names


def index(relations, courses):
    """Return only published courses with reviewed A/B source relationships."""
    have = {c["code"]: c for c in courses if c.get("levels")}
    by_country = {}
    for r in relations:
        code = r.get("iso_639_1") or ISO3_ALIAS.get(r.get("iso_639_3") or "") or r.get("iso_639_3")
        country = r.get("country_id")
        sourced = any(isinstance(x, dict) and x.get("source_url") and x.get("evidence_type") != "agent-compiled"
                      and str(x.get("priority") or "").split("-")[0] in {"A", "B"}
                      for x in (r.get("sources") or []))
        if not code or not country or code not in have or r.get("confidence") != "high" or r.get("needs_human_review") or not sourced:
            continue
        by_country.setdefault(country, {})[code] = {"code": code, "name": have[code]["name"], "native": r.get("native_name") or ""}
    return by_country, have


def course_href(code):
    """The page a reader should land on, relative to /courses/by-country/."""
    if os.path.isdir(os.path.join("languages", code, "course")):
        return "../../languages/%s/course/" % code
    if os.path.isdir(os.path.join("learn", code)):
        return "../../learn/%s/" % code
    return "../../courses/#/%s" % code


def build():
    courses, relations, names = load()
    by_country, have = index(relations, courses)
    name = lambda c: names.get(c, c)

    total_countries = len(by_country)
    total_langs = len({c for v in by_country.values() for c in v})

    total_published = len(have)

    out = [MARK]
    out.append(
        '<div class="course-static xp-country-page">'
        '<section class="course-hero">'
        '<img class="xp-world xp-world-herochip" data-xp-world="multi" '
        'src="../../images/xp/world-multi.svg" alt="" aria-hidden="true" '
        'width="430" height="430" loading="lazy" decoding="async">'
        '<span class="pill">%d sourced country contexts · %d published courses</span>'
        '<h1>Published courses by country</h1>'
        '<p>Browse country relationships that have high-confidence, reviewed A/B source evidence and point to a course with published levels. Research inventory and unpublished course shells are omitted.</p>'
        '<div class="course-hero-stats">'
        '<span><b>%d</b> sourced country contexts</span>'
        '<span><b>%d</b> represented course languages</span>'
        '<span><b>%d</b> published courses sitewide</span>'
        '</div>'
        '<div class="course-orbit" aria-hidden="true"><i>अ</i><i>Α</i><i>ع</i><i>あ</i><i>മ</i></div>'
        '</section>' % (total_countries, total_published, total_countries, total_langs, total_published))

    # The filter is an upgrade, not a requirement: without it the list below is
    # complete and every link works.
    out.append(
        '<div class="course-tools country-tools">'
        '<label>Find your country'
        '<input id="country-search" type="search" autocomplete="off" '
        'placeholder="e.g. Japan, Nigeria, Brazil" aria-describedby="country-count"></label>'
        '<span id="country-count" role="status"></span>'
        '</div>')

    rows = []
    for country in sorted(by_country, key=lambda c: (-len(by_country[c]), name(c))):
        langs = by_country[country]
        chips = "".join(
            '<a class="country-course" href="%s"><b>%s</b>%s</a>'
            % (course_href(code), esc(langs[code]["name"]),
               ('<small>%s</small>' % esc(langs[code]["native"])) if langs[code]["native"] else "")
            for code in sorted(langs, key=lambda k: langs[k]["name"]))
        rows.append(
            '<article class="country-card" id="country-%s" data-country="%s" data-search="%s">'
            '<h3><span class="country-code" aria-hidden="true">%s</span>%s'
            '<small>%d %s</small></h3>'
            '<div class="country-courses">%s</div></article>'
            % (esc(country), esc(country), esc((name(country) + " " + country).lower()), esc(country),
               esc(name(country)), len(langs), "language" if len(langs) == 1 else "languages",
               chips))

    out.append('<section class="xp-sec" id="countries"><div class="xp-head" style="text-align:start;margin-inline:0">'
               '<h2>Pick a sourced country context</h2><p>The number is how many published course languages have a qualifying relationship for that country.</p>'
               '</div><div class="country-grid">%s</div>'
               '<p class="country-empty" id="country-empty" hidden>No country matches that. '
               'Try the language name instead on the <a href="../">course hub</a>.</p></section>'
               % "".join(rows))

    out.append(
        '<section class="xp-sec"><div class="xp-head" style="text-align:start;margin-inline:0">'
        '<h2>How to use a country page</h2></div>'
        '<div class="xp-grid xp-grid-3 xp-stagger">'
        '<a class="xp-card" href="../"><div class="xp-card-ico" aria-hidden="true">🧭</div>'
        '<h3>Search the whole hub</h3><p>The course hub filters by language, by country and by '
        'the country you type — with a count for each.</p>'
        '<span class="xp-card-link">Open the course hub</span></a>'
        '<a class="xp-card" href="../../learn-hindi-by-country/"><div class="xp-card-ico" aria-hidden="true">🌍</div>'
        '<h3>Hindi, country by country</h3><p>The other half of this map: what learning Hindi '
        'means in 196 countries — times, prices, scripts and how much English is around.</p>'
        '<span class="xp-card-link">See the Hindi funnels</span></a>'
        '<a class="xp-card" href="../../contact/?topic=Course%20request"><div class="xp-card-ico" aria-hidden="true">✉️</div>'
        '<h3>Ask for a language</h3><p>A request is a vote. It is also how the queue above gets '
        'reordered — nothing is added for show.</p>'
        '<span class="xp-card-link">Write to us</span></a>'
        '</div></section>')

    # ItemList of countries with the languages available for each.
    items = []
    for i, country in enumerate(sorted(by_country), 1):
        items.append({
            "@type": "ListItem", "position": i,
            "name": "Language courses for %s" % name(country),
            "url": "https://ekguru.shop/courses/by-country/#country-%s" % country,
        })
    out.append('<script type="application/ld+json">%s</script>' % json.dumps(
        {"@context": "https://schema.org", "@type": "ItemList",
         "name": "EkGuru language courses by country",
         "numberOfItems": len(items), "itemListElement": items},
        ensure_ascii=False, separators=(",", ":")))

    out.append(
        '<script>(function(){var box=document.getElementById("country-search");'
        'if(!box)return;var cards=[].slice.call(document.querySelectorAll(".country-card"));'
        'var count=document.getElementById("country-count"),empty=document.getElementById("country-empty");'
        'box.addEventListener("input",function(){var q=box.value.toLowerCase().trim(),n=0;'
        'cards.forEach(function(c){var hit=!q||c.getAttribute("data-search").indexOf(q)>=0;'
        'c.hidden=!hit;if(hit)n++;});'
        'if(count)count.textContent=n+(n===1?" country":" countries");'
        'if(empty)empty.hidden=n>0;});'
        'if(count)count.textContent=cards.length+" countries";})();</script>')
    out.append(MARK_END)
    return "\n".join(out)


def splice(path, block, start, end, check):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            html = f.read()
    else:
        html = ""
    if start in html and end in html:
        import re
        body = re.sub(r"[ \t]*\n", "\n", block.strip("\n"))
        updated = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: body, html,
                         count=1, flags=re.S)
    elif start in html or end in html:
        raise SystemExit("ERROR: %s has one marker of the %s pair" % (path, start))
    else:
        updated = new_page(html, block)
    canonical = "https://ekguru.shop/courses/by-country/"
    updated = re.sub(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>', '<link rel="canonical" href="%s">' % canonical, updated, count=1, flags=re.I)
    updated = re.sub(r'<meta\b(?=[^>]*\bproperty=["\']og:url["\'])[^>]*>', '<meta property="og:url" content="%s">' % canonical, updated, count=1, flags=re.I)
    return html, updated


def new_page(existing, block):
    """A page with the site's head, breadcrumb and script tags — the same
    helpers the other generated families use, so it is indistinguishable from
    a hand-written page once the shell has run."""
    if existing and "<html" in existing:
        return existing
    import importlib.util
    import io
    import contextlib
    # build-hindi-pages.py has a hyphen in its name, so it is imported by path
    # — the same trick tools/build-world-course.py uses.
    spec = importlib.util.spec_from_file_location(
        "build_hindi_pages", os.path.join(ROOT, "tools", "build-hindi-pages.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    write_page = mod.write_page
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        write_page(PAGE, "../../", "Language Courses by Country — Every Language, Every Country | EkGuru",
                   "Every country EkGuru teaches a language for, the languages available for it "
                   "today, and the ones documented but not built yet.",
                   "courses/by-country/", '<a href="../../">EkGuru</a> › <a href="../">Courses</a> › '
                   'By country', block + "\n")
    with open(PAGE, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# the sitemaps
# ---------------------------------------------------------------------------
# /courses/ was in no declared sitemap: sitemap-courses-hub.xml exists with 85
# course URLs but sitemap-index.xml never listed it, so the only sitemaps Google
# was told about were the ones without the course hub in them. Both the hub and
# this page are linked from the nav, so they get crawled — but a page the site
# never declares is a page the site is not asking to have indexed.
SITEMAP = "sitemap-courses-hub.xml"
INDEX = "sitemap-index.xml"
HUBS = ["https://ekguru.shop/courses/", "https://ekguru.shop/courses/by-country/"]


def sitemap_block(loc):
    return "  <url>\n    <loc>%s</loc>\n  </url>\n" % loc


def update_sitemaps(check):
    """Returns True when something needed changing (or is stale in check mode)."""
    changed = []

    # 1. the URLs
    if os.path.exists(SITEMAP):
        with open(SITEMAP, encoding="utf-8") as f:
            xml = f.read()
    else:
        xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n')
    out = xml
    for loc in HUBS:
        if "<loc>%s</loc>" % loc in out:
            continue
        if out.rstrip().endswith("</urlset>"):
            out = out.replace("</urlset>", sitemap_block(loc) + "</urlset>", 1)
        else:
            raise SystemExit("ERROR: %s has no </urlset>" % SITEMAP)
    if out != xml:
        changed.append(SITEMAP)
        if not check:
            with open(SITEMAP, "w", encoding="utf-8") as f:
                f.write(out)

    # 2. declaring it
    with open(INDEX, encoding="utf-8") as f:
        idx = f.read()
    if "<loc>https://ekguru.shop/%s</loc>" % SITEMAP not in idx:
        stamp = time.strftime("%Y-%m-%d", time.gmtime())
        entry = ("  <sitemap>\n    <loc>https://ekguru.shop/%s</loc>\n"
                 "    <lastmod>%s</lastmod>\n  </sitemap>\n" % (SITEMAP, stamp))
        out = idx.replace("</sitemapindex>", entry + "</sitemapindex>", 1)
        changed.append(INDEX)
        if not check:
            with open(INDEX, "w", encoding="utf-8") as f:
                f.write(out)
    return changed


def main():
    check = "--check" in sys.argv
    block = build()
    html, updated = splice(PAGE, block, MARK, MARK_END, check)
    maps = update_sitemaps(check)
    if updated == html and not maps:
        print("ok    %s is current" % PAGE)
        return 0
    if check:
        for m in maps:
            print("STALE %s — run: python3 tools/build-course-countries.py" % m)
        if updated != html:
            print("STALE %s — run: python3 tools/build-course-countries.py" % PAGE)
        return 1
    if updated != html:
        os.makedirs(os.path.dirname(PAGE), exist_ok=True)
        with open(PAGE, "w", encoding="utf-8") as f:
            f.write(updated)
        print("wrote %s (%d bytes)" % (PAGE, len(updated)))
    for m in maps:
        print("updated %s" % m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
