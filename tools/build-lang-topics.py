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
/* Modern-Pro topic system (v158): theme-aware via --sb-accent/--sb-tint. */
.pw{max-width:880px;margin:0 auto;padding:0 20px 64px}
.pw h1{font-size:clamp(1.7rem,4.6vw,2.3rem);line-height:1.2;margin:14px 0;letter-spacing:-.01em}
.pw h2{font-size:clamp(1.15rem,3vw,1.35rem);line-height:1.3;margin:36px 0 12px;letter-spacing:-.005em}
.pw h3{font-size:1.02rem;margin:24px 0 8px}
.pw p,.pw li{line-height:1.72;font-size:1rem}
.pw p,.pw ul,.pw ol{max-width:72ch}
.lede{color:var(--ink-2);font-size:1.08rem;line-height:1.7}
.crumb{font-size:.84rem;color:var(--muted);padding:18px 0 0;word-break:break-word}
.crumb a{color:var(--muted)}
/* hero band */
.hero{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:22px;
  padding:clamp(22px,4.5vw,36px);margin:14px 0 8px;color:var(--ink);
  background:linear-gradient(135deg,var(--sb-tint,#f4f1ff) 0%,var(--card,#fff) 78%);
  box-shadow:var(--sh-1)}
.hero::after{content:"";position:absolute;right:-70px;top:-70px;width:220px;height:220px;border-radius:50%;
  background:radial-gradient(circle,var(--sb-tint,#f4f1ff) 0%,transparent 70%);opacity:.9;pointer-events:none}
.hero h1{margin:10px 0 8px}
.hero .lede{margin:0;max-width:60ch}
.kicker{display:inline-flex;align-items:center;gap:7px;font-size:.74rem;font-weight:800;letter-spacing:.09em;
  text-transform:uppercase;color:var(--sb-accent,#4f32d9);background:rgba(255,255,255,.75);
  border:1px solid var(--line);border-radius:999px;padding:5px 13px}
.statline{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 4px}
.statline span{display:inline-flex;align-items:center;gap:7px;font-size:.85rem;font-weight:600;
  border:1px solid var(--line);border-radius:999px;padding:7px 14px;background:var(--card,#fff);color:var(--ink-2)}
.statline i{width:8px;height:8px;border-radius:50%;background:var(--sb-accent,#4f32d9);font-style:normal}
/* facts */
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:22px 0}
.fact{border:1px solid var(--line);border-radius:14px;padding:14px 16px;background:var(--card,#fff);box-shadow:var(--sh-1)}
.fact b{display:block;font-size:1.25rem;margin-bottom:2px;color:var(--sb-accent,#4f32d9);letter-spacing:-.01em}
.fact span{font-size:.76rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
/* faq */
.faq{position:relative;border:1px solid var(--line);border-radius:14px;padding:16px 18px 16px 20px;margin:12px 0;
  background:var(--card,#fff);box-shadow:var(--sh-1);overflow:hidden}
.faq::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--sb-accent,#4f32d9)}
.faq b{display:block;margin-bottom:6px;color:var(--ink);font-size:1.02rem}
.faq p{margin:0;color:var(--ink-2)}
/* chips */
.chips{display:flex;flex-wrap:wrap;gap:9px;margin:14px 0}
.chips a{font-size:.88rem;font-weight:600;border:1px solid var(--line);border-radius:999px;padding:9px 16px;
  text-decoration:none;background:var(--card,#fff);color:var(--brand);min-height:44px;display:inline-flex;
  align-items:center;transition:all .18s ease;box-shadow:var(--sh-1)}
.chips a:hover{background:var(--sb-accent,#4f32d9);border-color:var(--sb-accent,#4f32d9);color:#fff;
  transform:translateY(-1px)}
/* phrase table */
.twrap{overflow-x:auto;max-width:72ch;border:1px solid var(--line);border-radius:16px;margin:16px 0;
  box-shadow:var(--sh-1);background:var(--card,#fff)}
table.phr{border-collapse:collapse;width:100%;margin:0}
table.phr th,table.phr td{border:0;border-bottom:1px solid var(--line);padding:11px 14px;text-align:left;
  font-size:.95rem;line-height:1.6}
table.phr tbody tr:last-child td{border-bottom:0}
table.phr tbody tr:nth-child(even){background:var(--bg-soft)}
table.phr thead th{position:sticky;top:0;background:var(--sb-tint,#f4f1ff);font-size:.8rem;
  text-transform:uppercase;letter-spacing:.05em;color:var(--ink-2);white-space:nowrap}
table.phr td.bn{font-size:1.1rem}
.ssay{border:1px solid var(--sb-accent,#4f32d9);background:var(--sb-tint,#f4f1ff);color:var(--sb-accent,#4f32d9);
  border-radius:999px;cursor:pointer;font-size:.85rem;padding:4px 12px;margin-left:10px;min-height:36px;
  font-weight:700;transition:all .15s ease;vertical-align:middle}
.ssay:hover{background:var(--sb-accent,#4f32d9);color:#fff}
/* cards */
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px;margin:20px 0}
.card{position:relative;border:1px solid var(--line);border-radius:16px;padding:18px;background:var(--card,#fff);
  overflow:hidden;transition:transform .18s ease,box-shadow .18s ease}
.card::before{content:"";position:absolute;left:0;right:0;top:0;height:4px;
  background:linear-gradient(90deg,var(--sb-accent,#4f32d9),transparent);opacity:.85}
.card b{display:block;margin-bottom:5px;font-size:1.02rem}
.card span{font-size:.88rem;color:var(--muted);line-height:1.55}
.card a{text-decoration:none;color:var(--ink);display:block}
.card a::after{content:"\\2192";display:inline-block;margin-top:10px;font-weight:800;color:var(--sb-accent,#4f32d9);
  transition:transform .18s ease}
.card a:hover b{color:var(--brand)}
.card:hover{transform:translateY(-3px);box-shadow:var(--sh-2)}
.card:hover a::after{transform:translateX(5px)}
.card.soon{opacity:1;background:var(--bg-soft);border-style:dashed}
.card.soon::before{background:var(--line)}
.card.soon:hover{transform:none;box-shadow:none}
.soonbadge{display:inline-block;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;
  border:1px solid var(--line);border-radius:999px;padding:4px 12px;margin-top:10px;color:var(--muted);
  background:var(--card,#fff)}
/* prev/next */
.prevnext{display:flex;justify-content:space-between;gap:12px;margin:40px 0 0;flex-wrap:wrap}
.prevnext a{flex:1 1 220px;border:1px solid var(--line);border-radius:14px;padding:14px 18px;text-decoration:none;
  min-height:44px;display:inline-flex;align-items:center;font-weight:600;background:var(--card,#fff);
  box-shadow:var(--sh-1);transition:all .18s ease}
.prevnext a:hover{border-color:var(--sb-accent,#4f32d9);box-shadow:var(--sh-2);transform:translateY(-2px)}
.prevnext span{flex:1 1 220px}
/* footer */
.pw-ftr{border-top:3px solid var(--sb-accent,#4f32d9);border-radius:18px 18px 0 0;background:linear-gradient(180deg,var(--sb-tint,#f4f1ff),rgba(255,255,255,0) 90%);margin-top:48px;padding:26px 20px 44px;text-align:center;
  color:var(--muted);font-size:.86rem}
.pw-ftr nav{display:flex;flex-wrap:wrap;gap:6px 18px;justify-content:center;margin-bottom:12px}
.pw-ftr a{color:var(--muted)}
/* note + linklist */
.note{background:var(--sb-tint,#f4f1ff);border:1px solid var(--line);border-left:4px solid var(--sb-accent,#4f32d9);
  border-radius:12px;padding:15px 18px;margin:18px 0;font-size:.94rem;color:var(--ink-2);max-width:72ch}
.linklist{list-style:none;padding:0;margin:12px 0 0;max-width:72ch}
.linklist li{padding:12px 14px;border:1px solid var(--line);border-radius:12px;margin-bottom:10px;
  background:var(--card,#fff);transition:all .15s ease}
.linklist li:hover{box-shadow:var(--sh-1);transform:translateX(3px)}
.linklist a{font-weight:700}
.linklist span{display:block;color:var(--muted);font-size:.87rem;margin-top:2px;line-height:1.5}
/* how-it-works steps */
.how{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:16px 0;counter-reset:step}
.howto{position:relative;border:1px solid var(--line);border-radius:14px;padding:16px 16px 16px 58px;background:var(--card,#fff)}
.howto::before{counter-increment:step;content:counter(step);position:absolute;left:16px;top:14px;width:30px;height:30px;
  border-radius:50%;background:var(--sb-accent,#4f32d9);color:#fff;font-weight:800;font-size:.9rem;
  display:flex;align-items:center;justify-content:center}
.howto b{display:block;margin-bottom:4px}
.howto span{font-size:.9rem;color:var(--ink-2);line-height:1.6}
/* CTA band */
.cta{position:relative;overflow:hidden;margin:32px 0 8px;border-radius:20px;padding:clamp(24px,4.5vw,34px);
  background:linear-gradient(135deg,var(--sb-accent,#4f32d9),#6d4de0);color:#fff;text-align:center;box-shadow:var(--sh-2)}
.cta h2{margin:0 0 8px;color:#fff}
.cta p{margin:0 auto 18px;color:rgba(255,255,255,.88);max-width:52ch}
.cta a.cta-btn{display:inline-block;background:#fff;color:var(--sb-accent,#4f32d9);font-weight:800;
  border-radius:999px;padding:12px 30px;text-decoration:none;min-height:48px;transition:transform .15s ease}
.cta a.cta-btn:hover{transform:scale(1.04)}
/* pro touches */
.pw h1,.pw h2{text-wrap:balance}
.pw,.card,.fact{overflow-wrap:break-word}
::selection{background:var(--sb-tint,#f4f1ff)}
a:focus-visible,button:focus-visible{outline:3px solid var(--sb-accent,#4f32d9);outline-offset:2px;border-radius:6px}
@media(prefers-reduced-motion:reduce){.card,.card a::after,.chips a,.prevnext a,.linklist li,.cta a.cta-btn{transition:none}}
@media(max-width:480px){.hero{border-radius:18px}.fact b{font-size:1.1rem}.pw{padding:0 16px 56px}}
@media print{.hero::after,.cta{display:none}.card a::after{content:""}}
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


def topic_page(cfg, tp, prev_tp, next_tp, live):
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
    cta = ('<div class="cta"><h2>Ready to test yourself?</h2>'
           '<p>Turn this topic into lasting memory — quiz, practice and review, all free.</p>'
           '<a class="cta-btn" href="%s">Quiz yourself</a></div>') % cfg["quiz_url"]
    body = ["<div class=\"pw\">",
            "<p class=\"crumb\"><a href=\"%s\">EkGuru</a> \u203a "
            "<a href=\"../\">%s</a> \u203a %s</p>"
            % (pre, H.escape(cfg["hub_title"]), H.escape(tp["title"])),
            '<div class="hero">',
            '<span class="kicker">%s</span>' % H.escape(cfg["title"]),
            "<h1>%s</h1>" % H.escape(tp["h1"]),
            "<p class=\"lede\">%s</p>" % H.escape(tp["lede"]),
            '</div>',
            hint(cfg["title"])]
    body += ["<p>%s</p>" % p for p in tp["paras"]]
    body += ["<h2>Words and phrases for this topic</h2>",
             "<div class=\"twrap\"><table class=\"phr\"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead>"
             "<tbody>%s</tbody></table></div>" % (tuple(H.escape(x) for x in tp["table_head"]) + ("".join(rows),))]
    body += ['<div class="note">%s</div>' % tp["note"]]
    body += ["<h2>Everything on this topic</h2>",
             '<ul class="linklist">' + "".join(
                 '<li><a href="%s">%s</a><span>%s</span></li>'
                 % (l["url"], H.escape(l["label"]), H.escape(l["desc"]))
                 for l in tp["links"]) + "</ul>"]
    body += ["<h2>Questions learners ask</h2>", faqs,
             "<h2>Keep learning %s</h2>" % H.escape(cfg["title"]),
             '<div class="chips"><a href="%s">Full %s course</a>'
             '<a href="%s">%s world course</a>'
             '<a href="%s">Quiz yourself</a></div>'
             % (cfg["course_url"], H.escape(cfg["title"]),
                cfg["world_url"], H.escape(cfg["title"]), cfg["quiz_url"]),
             "<h2>Related topics</h2>",
             '<div class="chips">' + "".join(
                 '<a href="../%s/">%s</a>' % (t["slug"], H.escape(t["title"]))
                 for t in live if t["slug"] != tp["slug"]) + "</div>",
             cta, nav, "</div>"]
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
    nphr = sum(len(t["phrases"]) for t in live)
    stats = '<div class="statline"><span><i></i>%d lessons</span><span><i></i>%d speakable phrases</span><span><i></i>free forever</span></div>' % (len(live), nphr)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "FAQPage", "@id": "%s/%s/#faq" % (BASE, d),
         "mainEntity": [
             {"@type": "Question", "name": f["q"],
              "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
             for f in cfg["hfaqs"]]},
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
            '<div class="hero">',
            '<span class="kicker">Free %s course</span>' % H.escape(cfg["title"]),
            "<h1>%s</h1>" % H.escape(cfg["hub_title"]),
            "<p class=\"lede\">%s</p>" % H.escape(cfg["hub_lede"]),
            stats,
            '</div>',
            hint(cfg["title"]),
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
            "<h2>How this course works</h2>",
            '<div class="how">' + "".join(
                '<div class="howto"><b>%s</b><span>%s</span></div>'
                % (H.escape(s["t"]), H.escape(s["d"])) for s in cfg["how"]) + "</div>",
            "<h2>Questions about this course</h2>",
            "".join('<div class="faq"><b>%s</b><p>%s</p></div>'
                    % (H.escape(f["q"]), H.escape(f["a"])) for f in cfg["hfaqs"]),
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
                               live[i + 1] if i + 1 < len(live) else None,
                               live))
    print("lang-topics [%s]: hub + %d topics, %d coming-soon cards."
          % (code, len(live), len(coming)))


if __name__ == "__main__":
    main()
