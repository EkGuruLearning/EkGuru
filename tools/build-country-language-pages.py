#!/usr/bin/env python3
"""EkGuru — country language-guide pages from the audited inventory.

    python3 tools/build-country-language-pages.py

Reads data/global/*.json (built by tools/build-inventory.py — run that first)
plus living-language counts from data/language-inventory/core/*.json, and writes:

    world-languages/<slug>/index.html   (one per AUDITED country only)
    world-languages/index.html          (index of audited countries)
    sitemap-world-languages.xml         (+ patch sitemap-index.xml)

Then inserts a "Languages of X" link block into the matching
learn-hindi-from-X page (audited countries only), before the
"Learning Hindi from somewhere else?" section. Idempotent: re-runs
replace the inserted block instead of duplicating it.

Content is data + the inventory's own per-language notes (unique per
country). Template wrapper is kept thin on purpose (de-templating).
Phase-16 safe: reference pages, not learning pages; audited countries only.
"""
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SITE = "https://ekguru.shop"
TODAY = "2026-09-14"

SLUGS = {
    "AF": "afghanistan", "BD": "bangladesh", "BT": "bhutan", "IN": "india",
    "IR": "iran", "LK": "sri-lanka", "MV": "maldives", "NP": "nepal",
    "PK": "pakistan", "KZ": "kazakhstan", "KG": "kyrgyzstan", "TJ": "tajikistan",
    "TM": "turkmenistan", "UZ": "uzbekistan", "AE": "uae", "AM": "armenia",
    "AZ": "azerbaijan", "BH": "bahrain", "GE": "georgia", "IL": "israel",
    "IQ": "iraq", "JO": "jordan", "KW": "kuwait", "LB": "lebanon",
    "OM": "oman", "QA": "qatar", "SA": "saudi-arabia", "SY": "syria",
    "TR": "turkiye", "YE": "yemen",
    "BN": "brunei", "KH": "cambodia", "ID": "indonesia", "LA": "laos",
    "MM": "myanmar", "MY": "malaysia", "PH": "philippines", "SG": "singapore",
    "TH": "thailand", "TL": "timor-leste", "VN": "vietnam",
}
COURSE_URL = {"hin": "learn/hindi/", "ben": "learn/bengali/",
              "tam": "learn/tamil/", "tel": "learn/telugu/",
              "mar": "learn/marathi/", "guj": "learn/gujarati/",
              "kan": "learn/kannada/", "mal": "learn/malayalam/",
              "pan": "learn/punjabi/", "urd": "learn/urdu/"}

GROUPS = [
    ("OFFICIAL", "Official & national languages"),
    ("NATIONAL", None),  # merged into OFFICIAL
    ("WIDELY_SPOKEN", "Widely spoken"),
    ("REGIONAL", "Regional, indigenous & minority languages"),
    ("INDIGENOUS", None),
    ("MINORITY", None),
    ("IMMIGRANT", "Immigrant & expatriate languages"),
    ("SIGN_LANGUAGE", "Sign languages"),
    ("OTHER", "Liturgical, historical & other"),
]
GROUP_OF = {"OFFICIAL": "OFFICIAL", "NATIONAL": "OFFICIAL",
            "WIDELY_SPOKEN": "WIDELY_SPOKEN", "REGIONAL": "REGIONAL",
            "INDIGENOUS": "REGIONAL", "MINORITY": "REGIONAL",
            "IMMIGRANT": "IMMIGRANT", "SIGN_LANGUAGE": "SIGN_LANGUAGE",
            "OTHER": "OTHER"}

BAND_LABEL = {"B0_none": "no L1 community", "B1_under_10k": "under 10,000",
              "B2_10k_100k": "10,000–100,000", "B3_100k_1M": "100,000–1M",
              "B4_1M_10M": "1M–10M", "B5_10M_100M": "10M–100M",
              "B6_over_100M": "over 100M"}


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def esc(x):
    return html.escape(str(x if x is not None else ""), quote=True)


def fmt_num(n):
    if n is None:
        return None
    if n >= 1000000:
        v = n / 1000000
        return ("%gM" % v).replace(".0M", "M") + ""
    if n >= 1000:
        return "%gk" % (n / 1000)
    return str(n)


def speakers_cell(r):
    se = r.get("speaker_estimate") or {}
    l1 = se.get("l1")
    if l1:
        return "≈%s L1" % fmt_num(l1)
    band = r.get("estimated_speaker_band", "")
    if band and band != "B0_none":
        return BAND_LABEL.get(band, band)
    if r.get("iso_639_3") == "arb":
        return "no L1 (standard)"
    return "—"


def role_badges(r):
    b = [r["category"].replace("_", " ").title()]
    if r.get("role_detail"):
        b.append(r["role_detail"].replace("-", " "))
    if r.get("status_in_country") not in (None, "LIVING"):
        b.append(r["status_in_country"].title())
    return " · ".join(b)


PAGE_CSS = """
.pw{max-width:860px;margin:0 auto;padding:0 20px 64px}
.pw h1{font-size:clamp(1.6rem,4.4vw,2.05rem);line-height:1.24;margin:24px 0 14px}
.pw h2{font-size:clamp(1.12rem,3vw,1.3rem);line-height:1.3;margin:34px 0 12px}
.pw p,.pw li{line-height:1.72;font-size:1rem}
.pw p,.pw ul{max-width:72ch}
.lede{color:var(--ink-2);font-size:1.06rem;line-height:1.7}
.crumb{font-size:.84rem;color:var(--muted);padding:18px 0 0;word-break:break-word}
.crumb a{color:var(--muted)}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:22px 0}
.fact{border:1px solid var(--line);border-radius:12px;padding:13px 15px;background:var(--bg-soft)}
.fact b{display:block;font-size:1.05rem;margin-bottom:2px;color:var(--ink)}
.fact span{font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
table.lang{width:100%;border-collapse:collapse;margin:6px 0 8px;font-size:.95rem}
table.lang th{text-align:left;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);padding:8px 10px;border-bottom:2px solid var(--line)}
table.lang td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top;line-height:1.6}
table.lang td.nm{font-weight:600;white-space:nowrap}
table.lang td.nt{font-size:.9rem;color:var(--ink-2)}
.badge{display:inline-block;font-size:.72rem;border:1px solid var(--line);border-radius:10px;padding:1px 8px;margin:2px 4px 0 0;color:var(--muted);white-space:nowrap}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
.chips a{font-size:.87rem;border:1px solid var(--line);border-radius:20px;padding:7px 13px;text-decoration:none;background:var(--card,#fff);color:var(--brand);min-height:44px;display:inline-flex;align-items:center}
.research{border:1px dashed var(--line);border-radius:12px;padding:13px 16px;margin:26px 0;font-size:.9rem;color:var(--ink-2);background:var(--bg-soft)}
details.more{margin:10px 0 26px;border:1px solid var(--line);border-radius:12px;padding:12px 16px;background:var(--card,#fff)}
details.more summary{cursor:pointer;font-weight:600}
@media(max-width:640px){table.lang th:nth-child(4),table.lang td:nth-child(4){display:none}}
"""


def page_shell(title, desc, canon_path, crumb_html, body_html, extra_ld=None):
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": SITE + canon_path + "#page",
         "name": title.split(" | ")[0], "description": desc,
         "url": SITE + canon_path, "inLanguage": "en",
         "isPartOf": {"@id": SITE + "/#website"}}]}
    if extra_ld:
        ld["@graph"].extend(extra_ld)
    return """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="%s%s">
<meta name="google-site-verification" content="hFaqyp-9LdUXSKPA9RF011TkO2m_-7AUMasXqm_0dGI" />
<meta property="og:type" content="website">
<meta property="og:site_name" content="EkGuru">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s%s">
<meta property="og:image" content="%s/images/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="%s/images/og-cover.jpg">
<link rel="icon" href="../../images/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="../../images/apple-touch-icon.png">
<link rel="manifest" href="../../manifest.webmanifest">
<meta name="theme-color" content="#4f32d9">
<link rel="stylesheet" href="../../css/style.min.css">
<style>%s
</style>
<script type="application/ld+json">%s</script>
</head>
<body>
<div class="pw">
%s
%s
<footer class="pw-ftr">
  <nav aria-label="Site information">
    <a href="../../">Home</a>
    <a href="../../about/">About</a>
    <a href="../../contact/">Contact</a>
    <a href="../../privacy/">Privacy</a>
    <a href="../../terms/">Terms</a>
    <a href="../../disclaimer/">Disclaimer</a>
  </nav>
  <p>© <span>2026</span> EkGuru — One Student. One Goal. One Guru.<br>
  Written and maintained by Prakash.
  Hindi lessons with native-speaking tutors, one to one.</p>
</footer>
</div>
<script src="../../js/site-config.js" defer></script>
<script defer>
document.addEventListener("DOMContentLoaded",function(){
  function paint(){try{var P=window.EkGuruPrice;if(P&&P.redraw)P.redraw();}catch(e){}}
  paint();window.addEventListener("ekguru:rates",paint);
});
if("serviceWorker" in navigator){window.addEventListener("load",function(){
  navigator.serviceWorker.register("../../sw.js").catch(function(){});
});}
</script>
</body>
</html>
""" % (esc(title), esc(desc), SITE, canon_path,
       esc(title), esc(desc), SITE, canon_path, SITE,
       esc(title), esc(desc), SITE, PAGE_CSS,
       json.dumps(ld, ensure_ascii=False), crumb_html, body_html)


def country_page(cc, cname, subregion, living, longtail, rels, sibs):
    by_group = {}
    for r in rels:
        by_group.setdefault(GROUP_OF[r["category"]], []).append(r)
    # de-dup: one row per language per group (keep richest roles in badges)
    official = [r for r in rels if r["category"] in ("OFFICIAL", "NATIONAL")]
    off_names = ", ".join(sorted({r["language_name"] for r in official})) or "—"
    off_set = {r["language_name"] for r in official}
    seen, top = set(), []
    for r in sorted((x for x in rels if (x.get("speaker_estimate") or {}).get("l1")),
                    key=lambda x: -(x.get("speaker_estimate") or {}).get("l1", 0)):
        if r["language_id"] in seen:
            continue
        seen.add(r["language_id"])
        top.append(r)
        if len(top) == 6:
            break
    also_names = [r["language_name"] for r in top if r["language_name"] not in off_set][:5]
    top_names = ", ".join(also_names)
    lede = ("The languages of %s at a glance: %s %s the official language%s. "
            % (cname, off_names,
               "is" if len(official) <= 2 else "are among",
               "s" if len({r["language_name"] for r in official}) != 1 else ""))
    if top_names:
        lede += "The largest mother tongues here are %s. " % top_names
    if living and living.get("count"):
        lede += ("Linguists count roughly %s living languages in %s; "
                 "this guide lists the major ones individually." % (living["count"], cname))

    facts = [
        ("Official", off_names),
        ("Largest L1", top[0]["language_name"] + (" ≈" + fmt_num((top[0].get("speaker_estimate") or {}).get("l1")) if top else "")) if top else None,
        ("Living (est.)", "≈%s" % living["count"] if living and living.get("count") else None),
        ("Listed here", "%d" % len({r["language_id"] for r in rels})),
    ]
    facts = [f for f in facts if f and f[1]]
    facts_html = '<div class="facts">' + "".join(
        '<div class="fact"><b>%s</b><span>%s</span></div>' % (esc(v), esc(k))
        for k, v in facts) + "</div>"

    sections = []
    for gkey, gtitle in GROUPS:
        if gtitle is None:
            continue
        rows = by_group.get(gkey, [])
        if not rows:
            continue
        # one row per language: merge roles
        merged = {}
        for r in rows:
            m = merged.setdefault(r["language_id"], {"r": r, "badges": set()})
            m["badges"].add(role_badges(r))
            # keep the relation with speaker numbers for the cell
            if (r.get("speaker_estimate") or {}).get("l1") and not (m["r"].get("speaker_estimate") or {}).get("l1"):
                m["r"] = r
        trs = []
        for lid, m in sorted(merged.items(), key=lambda kv: kv[1]["r"]["language_name"]):
            r = m["r"]
            nm = esc(r["language_name"])
            if r.get("native_name"):
                nm += "<br><span style='font-weight:400;color:var(--muted)'>%s</span>" % esc(r["native_name"])
            badges = "".join('<span class="badge">%s</span>' % esc(b) for b in sorted(m["badges"]))
            note = esc(r.get("country_specific_evidence") or "")
            if r.get("cluster_members"):
                note = ("Covers: %s. " % esc(", ".join(r["cluster_members"]))) + note
            trs.append("<tr><td class='nm'>%s<br>%s</td><td><code>%s</code></td>"
                       "<td>%s</td><td>%s</td><td class='nt'>%s</td></tr>"
                       % (nm, badges, esc(r.get("iso_639_3") or "—"),
                          esc(speakers_cell(r)), esc(r.get("script") or "—"), note))
        sections.append("<h2>%s</h2>\n<table class='lang'>\n<tr><th>Language</th><th>ISO</th>"
                        "<th>Speakers</th><th>Script</th><th>Notes</th></tr>\n%s\n</table>"
                        % (gtitle, "\n".join(trs)))

    more_html = ""
    if longtail:
        more_html = ("<details class='more'><summary>More languages spoken in %s "
                     "(below listing threshold)</summary><p>%s</p></details>"
                     % (esc(cname), esc(longtail)))

    # course cross-links from ekguru_status
    have_course = sorted({r["language_name"]: r["iso_639_3"] for r in rels
                          if r.get("ekguru_status") == "course"}.items())
    chips = []
    for nm, iso in have_course:
        if iso in COURSE_URL:
            chips.append('<a href="../../%s">Learn %s →</a>' % (COURSE_URL[iso], esc(nm)))
    chips.append('<a href="../../learn-hindi-from-%s/">Learn Hindi from %s →</a>'
                 % (SLUGS[cc], esc(cname)))
    chips.append('<a href="../../find-tutors.html">Find a tutor →</a>')
    chips_html = "<h2>Learn with EkGuru</h2>\n<div class='chips'>\n%s\n</div>" % "\n".join(chips)

    sib_links = "".join(
        '\n  <a href="../%s/">%s</a>' % (SLUGS[s], esc(nm))
        for s, nm in sorted(sibs, key=lambda x: x[1]) if s != cc)
    sib_html = ""
    if sib_links:
        sib_html = ("<h2>Languages of neighbouring countries</h2>\n<div class='chips'>%s\n</div>"
                    % sib_links)

    research = ("<div class='research'><b>Research note.</b> This guide is built from EkGuru's "
                "language inventory (pass-1 desk research: constitutions, censuses, Ethnologue 27, "
                "SIL ISO 639-3). Figures are order-of-magnitude estimates; %d of 194 countries "
                "are covered so far and every figure is being re-verified.</div>" % len(SLUGS))

    crumb = ('<p class="crumb"><a href="../../">EkGuru</a> › '
             '<a href="../">World languages</a> › %s</p>\n\n<h1>Languages of %s</h1>\n\n'
             '<p class="lede">%s</p>' % (esc(cname), esc(cname), esc(lede)))
    body = facts_html + "\n" + "\n".join(sections) + "\n" + more_html + "\n" + research + "\n" + chips_html + "\n" + sib_html
    desc = "Languages of %s: %s%s. Official languages, speaker numbers, scripts and notes." % (
        cname, off_names, ("; also " + top_names) if top_names else "")
    return page_shell("Languages of %s | EkGuru" % cname, desc[:300],
                      "/world-languages/%s/" % SLUGS[cc], crumb, body)


def index_page(countries):
    items = []
    by_sub = {}
    for cc, cname, sub, n in countries:
        by_sub.setdefault(sub, []).append((cc, cname, n))
    for sub in sorted(by_sub):
        lis = "".join(
            '\n  <li><a href="%s/">Languages of %s</a> — %d listed</li>' % (SLUGS[cc], esc(cname), n)
            for cc, cname, n in sorted(by_sub[sub], key=lambda x: x[1]))
        items.append("<h2>%s</h2>\n<ul>%s\n</ul>" % (esc(sub), lis))
    crumb = ('<p class="crumb"><a href="../">EkGuru</a> › World languages</p>\n\n'
             '<h1>Languages of the world, country by country</h1>\n\n'
             '<p class="lede">Which languages are spoken where — official languages, speaker '
             'numbers, scripts and honest notes, from EkGuru\'s ongoing language inventory. '
             '%d of 194 countries are covered so far; new countries are added as research '
             'completes.</p>' % len(countries))
    body = "\n".join(items) + ("\n<div class='research'><b>Research note.</b> Pass-1 desk research "
        "(constitutions, censuses, Ethnologue 27, SIL ISO 639-3); figures are "
        "order-of-magnitude estimates being re-verified.</div>")
    # index lives one level up: fix relative depths
    html_out = page_shell("World languages by country | EkGuru",
                          "Languages spoken in each country: official languages, speaker numbers, scripts and notes. %d countries covered so far."
                          % len(countries),
                          "/world-languages/", crumb, body)
    return html_out.replace("../../", "../")


BACKLINK = """
<h2>Languages spoken in {cname}</h2>
<p>Wondering what people actually speak in {cname} — official languages, regional
languages, and the languages of visitors and expats? Our research guide lists
them with speaker numbers and scripts.</p>
<div class="chips">
  <a href="../world-languages/{slug}/">Languages of {cname} →</a>
</div>

<h2>Learning Hindi from somewhere else?</h2>"""


def insert_backlinks(audited):
    missing = []
    for cc, cname in audited:
        p = "learn-hindi-from-%s/index.html" % SLUGS[cc]
        if not os.path.exists(p):
            missing.append((cc, "no page"))
            continue
        h = open(p, encoding="utf-8").read()
        anchor = "<h2>Learning Hindi from somewhere else?</h2>"
        marker = "world-languages/%s/" % SLUGS[cc]
        if marker in h:
            # idempotent: replace old block if present
            h = re.sub(r"\n<h2>Languages spoken in .*?</div>\n\n<h2>Learning Hindi from somewhere else\?></h2>",
                       "\n" + BACKLINK.strip() + "", h, count=1)
            open(p, "w", encoding="utf-8").write(h)
            continue
        if anchor not in h:
            missing.append((cc, "no anchor"))
            continue
        h = h.replace(anchor, BACKLINK.strip().format(cname=cname, slug=SLUGS[cc]), 1)
        open(p, "w", encoding="utf-8").write(h)
    return missing


def build():
    rels_data = load("data/global/language-country-relations.json")
    rels = rels_data if isinstance(rels_data, list) else rels_data.get("relations", rels_data.get("relationships", []))
    sov = {c["cca2"]: c for c in load("data/language-inventory/sovereign-194.json")["countries"]}
    living, longtail = {}, {}
    for fp in sorted(glob.glob("data/language-inventory/core/*.json")):
        d = load(fp)
        for e in d.get("countries", []) if isinstance(d, dict) else []:
            living[e["cca2"]] = e.get("livingLanguages", {})
            longtail[e["cca2"]] = e.get("notesLongTail", "")

    by_country = {}
    for r in rels:
        by_country.setdefault(r["country_id"], []).append(r)

    audited = sorted((cc for cc in by_country if cc in SLUGS and cc in sov),
                     key=lambda cc: sov[cc]["name"])
    assert audited, "no audited countries found — run tools/build-inventory.py first"
    countries_meta = []
    for cc in audited:
        c = sov[cc]
        sibs = [(s, sov[s]["name"]) for s in audited if sov[s].get("subregion") == c.get("subregion")]
        out = country_page(cc, c["name"], c.get("subregion", ""),
                           living.get(cc, {}), longtail.get(cc, ""),
                           by_country[cc], sibs)
        d = "world-languages/%s" % SLUGS[cc]
        os.makedirs(d, exist_ok=True)
        open(d + "/index.html", "w", encoding="utf-8").write(out)
        countries_meta.append((cc, c["name"], c.get("subregion", ""),
                               len({r["language_id"] for r in by_country[cc]})))

    os.makedirs("world-languages", exist_ok=True)
    open("world-languages/index.html", "w", encoding="utf-8").write(index_page(countries_meta))

    urls = ["  <url>\n    <loc>%s/world-languages/</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>" % (SITE, TODAY)]
    for cc, cname, sub, n in sorted(countries_meta, key=lambda x: x[1]):
        urls.append("  <url>\n    <loc>%s/world-languages/%s/</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>" % (SITE, SLUGS[cc], TODAY))
    open("sitemap-world-languages.xml", "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n")

    idx = open("sitemap-index.xml", encoding="utf-8").read()
    if "sitemap-world-languages.xml" not in idx:
        idx = idx.replace("</sitemapindex>",
                          '  <sitemap>\n    <loc>%s/sitemap-world-languages.xml</loc>\n    <lastmod>%s</lastmod>\n  </sitemap>\n</sitemapindex>'
                          % (SITE, TODAY))
        open("sitemap-index.xml", "w", encoding="utf-8").write(idx)

    missing = insert_backlinks([(cc, sov[cc]["name"]) for cc in audited])
    print("pages: %d | backlinks ok: %d | missing: %s"
          % (len(audited), len(audited) - len(missing), missing or "none"))


if __name__ == "__main__":
    build()
