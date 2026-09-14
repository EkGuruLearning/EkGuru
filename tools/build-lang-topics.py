#!/usr/bin/env python3
"""EkGuru — LANGUAGE TOPIC BUILDER (v152 pilot: Bengali).

    python3 tools/build-lang-topics.py [code]

Reads data/topics/<code>.json and emits the "Hindi-level" topic hub:
  /<dir>/                  hub: facts + course links + topic cards
  /<dir>/<slug>/           full topic lesson (Hindi-topic standard)

Generic across languages: the Hindi pages it mirrors are hand-written,
so this builder bakes the SAME shell (SEO head, .pw styles, TTS hint,
phrase tables with speaker buttons, FAQs + JSON-LD, footer) from
per-language JSON content. Unwritten topics render as honest,
unlinked "Coming soon" cards — never fake links, never invented URLs.

After running, run tools/inject-storybook.py for banners + dock.
"""
import html as H
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://ekguru.shop"
MARK = "<!-- ekguru:storybook -->"

# Mirror order of the Hindi topic hub (minus per-language adaptations,
# which live in each JSON's coming_titles).
MIRROR = ["alphabet", "beginners", "bengali-vs-assamese", "bollywood",
          "business", "conversation", "emergency", "family",
          "flashcards-topic", "for-kids", "formal-informal", "grammar",
          "greetings", "heritage", "how-long", "indian-languages",
          "listening", "mistakes", "name-topic", "numbers",
          "phrases-food", "phrases-travel", "pronunciation", "reading",
          "relationships", "sentence-structure", "shopping", "slang",
          "speaking", "time-date", "verbs", "vocabulary", "writing"]

STYLE = """
.pw{max-width:820px;margin:0 auto;padding:0 20px 64px}
.pw h1{font-size:clamp(1.6rem,4.4vw,2.05rem);line-height:1.24;margin:24px 0 14px}
.pw h2{font-size:clamp(1.12rem,3vw,1.3rem);line-height:1.3;margin:34px 0 12px}
.pw h3{font-size:1.02rem;margin:24px 0 8px}
.pw p,.pw li{line-height:1.72;font-size:1rem}
.pw p,.pw ul,.pw ol{max-width:72ch}
.lede{color:var(--ink-2);font-size:1.06rem;line-height:1.7}
.crumb{font-size:.84rem;color:var(--muted);padding:18px 0 0;word-break:break-word}
.crumb a{color:var(--muted)}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:22px 0}
.fact{border:1px solid var(--line);border-radius:12px;padding:13px 15px;background:var(--bg-soft)}
.fact b{display:block;font-size:1.12rem;margin-bottom:2px;color:var(--ink)}
.fact span{font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.faq{border:1px solid var(--line);border-radius:12px;padding:15px 17px;margin:12px 0;background:var(--card,#fff)}
.faq b{display:block;margin-bottom:6px;color:var(--ink)}
.faq p{margin:0;color:var(--ink-2)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
.chips a{font-size:.87rem;border:1px solid var(--line);border-radius:20px;padding:7px 13px;text-decoration:none;background:var(--card,#fff);color:var(--brand);min-height:44px;display:inline-flex;align-items:center}
table.phr{border-collapse:collapse;width:100%;margin:16px 0;max-width:72ch}
table.phr th,table.phr td{border:1px solid var(--line);padding:9px 12px;text-align:left;font-size:.95rem;line-height:1.6}
table.phr th{background:var(--bg-soft)}
table.phr td.bn{font-size:1.08rem}
.ssay{border:1px solid var(--line);background:var(--card,#fff);border-radius:8px;cursor:pointer;font-size:.95rem;padding:2px 8px;margin-left:8px;min-height:34px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin:18px 0}
.card{border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:var(--card,#fff)}
.card b{display:block;margin-bottom:4px}
.card span{font-size:.88rem;color:var(--muted);line-height:1.5}
.card a{text-decoration:none;color:var(--ink)}
.card.soon{opacity:.75;background:var(--bg-soft)}
.soonbadge{display:inline-block;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;border:1px solid var(--line);border-radius:20px;padding:3px 10px;margin-top:8px;color:var(--muted)}
.prevnext{display:flex;justify-content:space-between;gap:12px;margin:36px 0 0;flex-wrap:wrap}
.prevnext a{border:1px solid var(--line);border-radius:12px;padding:12px 16px;text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.pw-ftr{border-top:1px solid var(--line);margin-top:40px;padding:22px 20px 40px;text-align:center;color:var(--muted);font-size:.86rem}
.pw-ftr nav{display:flex;flex-wrap:wrap;gap:6px 18px;justify-content:center;margin-bottom:12px}
.pw-ftr a{color:var(--muted)}
"""


def head(title, desc, url, pre, ld_json):
    t, d = H.escape(title), H.escape(desc)
    return """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s | EkGuru</title>
<meta name="description" content="%s">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="%s/%s">
<meta name="google-site-verification" content="hFaqyp-9LdUXSKPA9RF011TkO2m_-7AUMasXqm_0dGI" />
<meta property="og:type" content="article">
<meta property="og:site_name" content="EkGuru">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="%s | EkGuru">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s/%s">
<meta property="og:image" content="%s/images/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s | EkGuru">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="%s/images/og-cover.jpg">
<link rel="icon" href="%simages/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="%simages/apple-touch-icon.png">
<link rel="manifest" href="%smanifest.webmanifest">
<meta name="theme-color" content="#4f32d9">
<link rel="stylesheet" href="%scss/style.min.css">
%s
<link rel="stylesheet" href="%scss/storybook.css">
<style>%s
</style>
<script type="application/ld+json">%s</script>
</head>
""" % (t, d, BASE, url, t, d, BASE, url, BASE, t, d, BASE,
       pre, pre, pre, pre, MARK, pre, STYLE, ld_json)


def footer(pre):
    return """<footer class="pw-ftr">
  <nav aria-label="Site information">
    <a href="%s">Home</a>
    <a href="%sabout/">About</a>
    <a href="%scontact/">Contact</a>
    <a href="%sprivacy/">Privacy</a>
    <a href="%sterms/">Terms</a>
    <a href="%sdisclaimer/">Disclaimer</a>
  </nav>
  <p>&copy; <span>2026</span> EkGuru &mdash; One Student. One Goal. One Guru.<br>
  Written and maintained by Prakash.</p>
</footer>
""" % ((pre,) * 6)


def hint(lang_title):
    return ('<p class="sb-hint">\U0001F50A <b>Tap any speaker button to hear '
            '%s spoken.</b> Too fast or slow? Use the <b>speed</b> button at '
            'the bottom-right of the page.</p>') % H.escape(lang_title)


def topic_page(cfg, tp, prev_tp, next_tp):
    d, pre = cfg["dir"], "../../"
    url = "%s/%s/" % (d, tp["slug"])
    rows = []
    for ph in tp["phrases"]:
        rows.append(
            "<tr><td>%s</td><td class=\"bn\" lang=\"%s\">%s"
            "<button class=\"ssay\" data-sb-say=\"%s\" aria-label=\"Hear it in %s\">"
            "\U0001F50A</button></td><td><i>%s</i></td></tr>"
            % (H.escape(ph["en"]), cfg["code"], H.escape(ph["bn"]),
               H.escape(ph["bn"], quote=True), H.escape(cfg["title"]),
               H.escape(ph["say"])))
    faqs = "".join(
        "<div class=\"faq\"><b>%s</b><p>%s</p></div>"
        % (H.escape(f["q"]), H.escape(f["a"])) for f in tp["faqs"])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": "%s/%s#article" % (BASE, url),
         "headline": tp["title"], "description": tp["desc"],
         "inLanguage": "en",
         "about": {"@type": "Language", "name": cfg["title"],
                   "alternateName": cfg["native"]},
         "author": {"@type": "Organization", "name": "EkGuru",
                    "url": BASE + "/"},
         "publisher": {"@type": "Organization", "name": "EkGuru",
                       "url": BASE + "/"},
         "mainEntityOfPage": "%s/%s" % (BASE, url)},
        {"@type": "FAQPage", "@id": "%s/%s#faq" % (BASE, url),
         "mainEntity": [
             {"@type": "Question", "name": f["q"],
              "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
             for f in tp["faqs"]]}]}
    nav = '<nav class="prevnext" aria-label="More %s topics">' % cfg["title"]
    nav += ('<a href="../%s/">&larr; %s</a>' % (prev_tp["slug"], H.escape(prev_tp["title"]))
            if prev_tp else "<span></span>")
    nav += ('<a href="../%s/">%s &rarr;</a>' % (next_tp["slug"], H.escape(next_tp["title"]))
            if next_tp else "<span></span>")
    nav += "</nav>"
    body = ["<div class=\"pw\">",
            "<p class=\"crumb\"><a href=\"%s\">EkGuru</a> \u203a "
            "<a href=\"../\">%s</a> \u203a %s</p>"
            % (pre, H.escape(cfg["hub_title"]), H.escape(tp["title"])),
            "<h1>%s</h1>" % H.escape(tp["h1"]),
            hint(cfg["title"]),
            "<p class=\"lede\">%s</p>" % H.escape(tp["lede"])]
    body += ["<p>%s</p>" % p for p in tp["paras"]]
    body += ["<h2>Words and phrases for this topic</h2>",
             "<table class=\"phr\"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead>"
             "<tbody>%s</tbody></table>" % (tuple(H.escape(x) for x in tp["table_head"]) + ("".join(rows),))]
    body += ["<h2>Questions learners ask</h2>", faqs,
             "<h2>Keep learning %s</h2>" % H.escape(cfg["title"]),
             '<div class="chips"><a href="%s">Full %s course</a>'
             '<a href="%s">%s world course</a>'
             '<a href="%s">Quiz yourself</a></div>'
             % (cfg["course_url"], H.escape(cfg["title"]),
                cfg["world_url"], H.escape(cfg["title"]), cfg["quiz_url"]),
             nav, "</div>"]
    page = (head(tp["title"], tp["desc"], url, pre,
                 json.dumps(ld, ensure_ascii=False))
            + "<body>\n" + "\n".join(body) + "\n" + footer(pre)
            + MARK + "\n" + '<script src="%sjs/storybook.js" defer></script>\n'
            % pre + "</body>\n</html>\n")
    return page


def hub_page(cfg, live, coming):
    d, pre = cfg["dir"], "../"
    facts = "".join(
        '<div class="fact"><b>%s</b><span>%s</span></div>'
        % (H.escape(f["v"]), H.escape(f["k"])) for f in cfg["facts"])
    cards = "".join(
        '<div class="card"><a href="%s/"><b>%s</b><span>%s</span></a></div>'
        % (t["slug"], H.escape(t["title"]), H.escape(t["lede"][:90] + "…"))
        for t in live)
    cards += "".join(
        '<div class="card soon"><b>%s</b><br><span class="soonbadge">Coming soon</span></div>'
        % H.escape(title) for _, title in coming)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": "%s/%s/#hub" % (BASE, d),
         "name": cfg["hub_title"], "description": cfg["hub_lede"],
         "inLanguage": "en",
         "about": {"@type": "Language", "name": cfg["title"],
                   "alternateName": cfg["native"]}},
        {"@type": "ItemList", "@id": "%s/%s/#list" % (BASE, d),
         "name": "%s lessons" % cfg["title"], "numberOfItems": len(live),
         "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": t["title"],
              "url": "%s/%s/%s/" % (BASE, d, t["slug"])}
             for i, t in enumerate(live)]}]}
    body = ["<div class=\"pw\">",
            "<p class=\"crumb\"><a href=\"%s\">EkGuru</a> \u203a %s</p>"
            % (pre, H.escape(cfg["hub_title"])),
            "<h1>%s</h1>" % H.escape(cfg["hub_title"]),
            hint(cfg["title"]),
            "<p class=\"lede\">%s</p>" % H.escape(cfg["hub_lede"]),
            '<div class="facts">%s</div>' % facts,
            "<h2>Start here</h2>",
            '<div class="chips"><a href="%s">Full %s course (29 lessons)</a>'
            '<a href="%s">%s world course</a>'
            '<a href="%s">Quiz yourself</a></div>'
            % (cfg["course_url"], H.escape(cfg["title"]),
               cfg["world_url"], H.escape(cfg["title"]), cfg["quiz_url"]),
            "<h2>Topics (%d ready, %d coming soon)</h2>"
            % (len(live), len(coming)),
            '<div class="cards">%s</div>' % cards,
            "<h2>New lessons every week</h2>",
            "<p>Each topic is written fresh for this course — real explanations, "
            "real phrases, every word speakable. Bookmark this page; the "
            "coming-soon cards turn into lessons week by week.</p>",
            "</div>"]
    return (head(cfg["hub_title"], cfg["lede"], d + "/", pre,
                 json.dumps(ld, ensure_ascii=False))
            + "<body>\n" + "\n".join(body) + "\n" + footer(pre)
            + MARK + "\n" + '<script src="%sjs/storybook.js" defer></script>\n'
            % pre + "</body>\n</html>\n")


def main():
    code = sys.argv[1] if len(sys.argv) > 1 else "bn"
    with open("data/topics/%s.json" % code, encoding="utf-8") as f:
        cfg = json.load(f)
    live = cfg["topics"]
    live_slugs = {t["slug"] for t in live}
    coming = [(s, cfg["coming_titles"].get(s, s.replace("-", " ").title()))
              for s in MIRROR if s not in live_slugs]
    os.makedirs(cfg["dir"], exist_ok=True)
    with open("%s/index.html" % cfg["dir"], "w", encoding="utf-8") as f:
        f.write(hub_page(cfg, live, coming))
    for i, tp in enumerate(live):
        os.makedirs("%s/%s" % (cfg["dir"], tp["slug"]), exist_ok=True)
        with open("%s/%s/index.html" % (cfg["dir"], tp["slug"]), "w",
                  encoding="utf-8") as f:
            f.write(topic_page(cfg, tp,
                               live[i - 1] if i > 0 else None,
                               live[i + 1] if i + 1 < len(live) else None))
    print("lang-topics [%s]: hub + %d topics, %d coming-soon cards."
          % (code, len(live), len(coming)))


if __name__ == "__main__":
    main()
