#!/usr/bin/env python3
"""EkGuru — LANGUAGE TOPIC BUILDER (Phase 2: all nine Indian languages).

    python3 tools/build-lang-topics.py [code ...] [--check]

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
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "https://ekguru.shop"
MARK = "<!-- ekguru:storybook -->"
TOPIC_VOICE_MARKER = "<!-- ekguru:topic-voice-controls:v1 -->"
TOPIC_HUB_VOICE_MARKER = "<!-- ekguru:topic-hub-voice-controls:v2 -->"
TOPIC_BUILDER_VERSION = "phase2-topic-depth-1"
with open(__file__, "rb") as _source_file:
    TOPIC_BUILDER_SOURCE_FINGERPRINT = hashlib.sha256(_source_file.read()).hexdigest()[:16]
with open(os.path.join(ROOT, "data", "quality", "indexing-baseline.json"), encoding="utf-8") as _baseline_file:
    INDEXING_BASELINE = json.load(_baseline_file).get("pages", {})


def publication_for(url):
    """Preserve the immutable robots/canonical decision for this route.

    A newly added route has no owner-approved publication decision and stays
    noindex. Existing pages inherit their exact baseline canonical and index
    state rather than being promoted by a content rebuild.
    """
    route = str(url).strip("/")
    rel = (route + "/index.html") if route else "index.html"
    baseline = INDEXING_BASELINE.get(rel)
    default_canonical = BASE + "/" + (str(url).lstrip("/"))
    if baseline is None:
        return "noindex, follow", default_canonical
    robots = ("index, follow, max-snippet:-1, max-image-preview:large"
              if baseline.get("indexable") else "noindex, follow")
    return robots, baseline.get("canonical") or default_canonical


def content_fingerprint(cfg, topic=None):
    """Fingerprint generator source and language data without touching chrome."""
    payload = {
        "builder_version": TOPIC_BUILDER_VERSION,
        "builder_source": TOPIC_BUILDER_SOURCE_FINGERPRINT,
        "config": cfg,
        "topic": topic,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:20]

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



def localised(text, lang):
    lang = re.sub(r"^Learn\s+", "", lang or "")
    """A per-language page gets its own title.

    The topic titles come from per-language JSON and the good ones already name
    the language ("Bengali vs Assamese"). The rest — "Family words", "Shopping
    and bargaining", "Speaking practice" — were the same words on nine pages,
    which is exactly the template pattern AdSense flagged. Naming the language
    in the title (and the h1) makes each page say what it is.
    """
    if not lang or lang.lower() in text.lower() or text.lower() in lang.lower():
        return text
    return "%s in %s" % (text, lang)


def head(title, desc, url, pre, ld_json):
    t, d = H.escape(title), H.escape(desc)
    robots, canonical = publication_for(url)
    return """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s | EkGuru</title>
<meta name="description" content="%s">
<meta name="robots" content="%s">
<link rel="canonical" href="%s">
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
""" % (t, d, robots, H.escape(canonical, quote=True), t, d, BASE, url, BASE,
       t, d, BASE, pre, pre, pre, pre, MARK, pre, STYLE, ld_json)


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


# Every live topic page gets one real retrieval exercise, tied to its own
# phrase table. These short prompts are deliberately topic-specific: they give
# learners a safe next action without claiming that every browser has a native
# voice or that one regional usage is universal.
PRACTICE_FOCUS = {
    "greetings": "Choose a relationship and setting before you speak: a greeting to a close friend need not be the greeting you choose for an elder or a first meeting. Practise opening and replying, then listen for the form your conversation partner uses. Mirror it politely instead of assuming one greeting fits every community.",
    "alphabet": "Pick one letter or sign from the examples, trace it slowly, and name its sound before you read a whole word containing it. Then cover the chart and identify the same shape in a new example. This separates visual recognition from pronunciation and helps prevent guessing from a familiar-looking script.",
    "numbers": "Choose a practical setting—a price, a quantity, an age, or an appointment time—and use the number in a complete request. Say the number once, pause, and repeat it at a natural pace. Check the script form as well as the romanisation; a familiar Arabic numeral is not a substitute for recognising the local form.",
    "conversation": "Turn two rows into a brief exchange: open, answer, and add one follow-up question of your own. Keep the turns short enough to say without reading. In a real conversation, listen for the other person’s pace and leave room for a reply rather than delivering a memorised speech.",
    "verbs": "Choose one verb from the examples and build two short sentences around it. Change one detail at a time—who is acting, when it happens, or whether the sentence is a question—then compare the result with the page. Do not invent an ending from English; learn the pattern from attested examples.",
    "vocabulary": "Group the words by the company they keep: notice which word belongs with a person, action, place, or polite reply. Make one short sentence using a pair from the table, then recall the pair tomorrow without looking. Remembering a usable phrase is more valuable than reciting an isolated translation.",
    "phrases-food": "Imagine ordering one item, checking a detail, and thanking the person serving you. Practise the request as a complete turn, not as a bare noun. Menus and regional food names vary; point to an item or ask what it contains when a translation or dietary detail matters.",
    "pronunciation": "Listen to one phrase from the table, wait a beat, and repeat it at an easy pace. Try once more without the romanisation, then compare what you said with the written form. The spelling guide is approximate; focus on a clear, comfortable rhythm rather than forcing an accent you do not have.",
    "grammar": "Return to one complete example and mark the words that carry the relationship between its parts. Change only one word, read the new version aloud, and check whether the meaning still follows. This small contrast is safer than memorising a rule without seeing the language used in context.",
    "beginners": "Select three forms you can use this week and attach each to a real routine: greeting someone, asking a simple question, or describing what you need. Practise for a few minutes on separate days. If recall fails, reveal the answer, say it once, and try again later rather than copying it repeatedly.",
    "family": "Choose one real relationship and practise the matching term in a short introduction. Family titles can carry age, affection, respect, and local habit, so they do not always map neatly onto English labels. When unsure, listen to how the family addresses one another and ask before using an intimate form.",
    "time-date": "Use the examples to arrange a real meeting: ask for a day, confirm a time, and repeat the answer back. Write the date in the script shown on the page, then read it aloud. Calendar conventions and everyday time expressions can vary, so confirm the details rather than relying on a guess.",
    "phrases-travel": "Picture one journey and ask for a destination, a direction, or a stop. Practise the request slowly enough to be understood, then repeat the place name back to check it. If the route is important, combine the spoken phrase with a map or written address rather than relying on one phrase alone.",
    "shopping": "Role-play a small purchase: ask the price, confirm the quantity, and respond courteously. Say the amount back before paying. Bargaining is not expected in every shop or situation, so read the setting and accept a clear answer; the aim is a respectful exchange, not a memorised performance.",
    "emergency": "Practise a short, direct request for help and add the most important detail—your location, the person affected, or what is needed. Speak clearly and repeat the key noun if necessary. In a real emergency, use local emergency services and gestures or a written address as well as these phrases.",
    "formal-informal": "Choose two listeners with different relationships to you and practise the same message for each. Keep the meaning steady while adjusting the form of address or level of politeness shown on the page. A common trap is switching one familiar word while leaving the rest of a formal sentence unchanged.",
    "mistakes": "Take one incorrect form discussed on this page and explain why it sounds wrong in its example, not just which answer replaces it. Then make a new sentence that avoids the same trap. Keep a short personal error log; correcting a recurring habit is more useful than collecting a long list of rules.",
    "speaking": "Record yourself giving a short answer using two phrases from the table. Listen once for whether the words are understandable and once for pauses or missing endings. Re-record only one improvement at a time. If you have a partner, ask for one specific correction instead of a vague judgement of your accent.",
    "listening": "Read the three cues, hide the table, and listen to the speaker control once if a matching voice is available. Try to identify the phrase before reading it. On a second listen, notice where one word ends and the next begins; do not mistake a regional accent for an error.",
    "reading": "Choose a short item in the script from this guide and read it aloud before checking the romanisation. Point to each written unit as you say it, then return to the beginning and read for meaning. If a sign or printed form differs regionally, use the surrounding context and ask a fluent reader.",
    "writing": "Write three examples from memory, then compare each with the page one character at a time. Correct the shape or mark that changed the meaning instead of rewriting the whole row. A photograph of a real label or notebook can become a useful review prompt, provided you have permission to keep it.",
    "sentence-structure": "Build a new sentence by keeping the pattern from one model and replacing only one meaningful part. Read it aloud and translate the whole idea back into English. Avoid moving every word into English order; compare how the example itself marks who did what and when.",
    "name-topic": "Write your name in the script as a pronunciation guide, not as a claim that every sound has an exact one-letter match. Say it aloud for a fluent speaker and invite them to adjust the spelling. Names deserve care: follow the person’s own preferred spelling when they already use one.",
    "slang": "Before repeating a slang expression, identify who said it, to whom, and in what mood. Practise recognising the phrase before trying it yourself. Slang can sound friendly in one group and rude in another; avoid using it with elders, customers, or strangers until a trusted speaker confirms the setting.",
    "for-kids": "Make a picture card for one word, say it together, and let the learner point to the matching picture before speaking. Keep the activity short and playful, with a chance to stop. Do not turn pronunciation into a test; encouragement and repeated exposure work better than correcting every sound.",
    "business": "Practise one workplace request as a complete message: name the task, make the request, and confirm the next step. Keep a respectful opening and closing. Office conventions differ by team and region, so use the examples as a starting point and observe the register your colleagues prefer.",
    "heritage": "Choose one phrase connected to a relative, place, or family routine and ask a speaker how they say it at home. Record any regional form beside the printed version without treating either as the only correct one. A heritage learner can connect written study with oral knowledge while respecting family variation.",
    "how-long": "Turn the goal into a small, repeatable routine: choose one phrase, recall it tomorrow, and use it later in a new example. Track practice time rather than promising a fluency date. Progress depends on prior experience, access to speakers, and consistency; a calendar is a planning aid, not a guarantee.",
    "indian-languages": "Compare one form on this page with a language you already know: note a real similarity and one difference in sound, script, or usage. Shared words do not prove that pronunciation or grammar is interchangeable. Keep both examples visible so a helpful comparison does not become a false shortcut.",
    "relationships": "Practise a respectful way to introduce a person or describe a relationship, then check whether the form suits the setting. Terms of affection and respect are personal as well as linguistic. Avoid assuming that a phrase that works among close friends belongs in every family or public conversation.",
    "flashcards-topic": "Use the three cues as active-recall cards: try each answer before turning to the key, then revisit the ones you missed after a short break. Shuffle the order on the next pass. Do not count a card as learned just because the answer looks familiar while it is visible.",
}


def topic_source_word_count(tp):
    """Count authored topic text, excluding JSON keys and navigation metadata."""
    def values(item):
        if isinstance(item, dict):
            for value in item.values():
                yield from values(value)
        elif isinstance(item, list):
            for value in item:
                yield from values(value)
        elif isinstance(item, str):
            yield item

    fields = [tp.get(key, "") for key in
              ("h1", "lede", "paras", "table_head", "phrases", "note", "faqs")]
    text = H.unescape(re.sub(r"<[^>]*>", " ", " ".join(values(fields))))
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def practice_section(cfg, tp):
    """Render a no-JS recall drill from this topic's own phrases and usage note."""
    phrases = tp["phrases"]
    positions = sorted({0, len(phrases) // 2, len(phrases) - 1})
    samples = [phrases[i] for i in positions]
    cues = "".join("<li>%s</li>" % H.escape(ph["en"]) for ph in samples)
    key = "".join(
        '<li><span lang="%s" dir="auto">%s</span> '
        '<i>%s</i> — %s</li>'
        % (H.escape(cfg["code"], quote=True), H.escape(ph["bn"]),
           H.escape(ph["say"]), H.escape(ph["en"])) for ph in samples)
    language = re.sub(r"^Learn\s+", "", cfg["title"])
    focus = PRACTICE_FOCUS.get(tp["slug"])
    if focus is None and "-vs-" in tp["slug"]:
        focus = ("Write down one useful similarity and one difference between the two languages. "
                 "Check each claim against the examples rather than guessing from a shared word. "
                 "Keep the forms in their own scripts and practise saying both before deciding "
                 "which one belongs in the situation described on this page.")
    if focus is None and ("cinema" in tp["slug"] or tp["slug"] in ("bollywood", "sandalwood", "mollywood", "pollywood", "kollywood", "tollywood", "lollywood")):
        focus = ("Choose a short line you can understand from a film or programme in the language. "
                 "Listen once for the situation, then replay it with subtitles and compare one "
                 "expression with this page. Screen dialogue is written for characters and can "
                 "be dramatic or region-specific; do not treat it as a universal everyday script.")
    if topic_source_word_count(tp) < 400 and focus is None:
        raise ValueError("No topic-specific practice focus for %s" % tp["slug"])
    parts = [
        '<section class="topic-practice" aria-labelledby="topic-practice-title">',
        '<h2 id="topic-practice-title">Practice: recall, then use</h2>',
        '<p>Use this quick recall drill for <b>%s</b>. Hide the script and romanisation columns; say the %s form for each cue before revealing its row, then check spelling and sound. The phrase-table speaker buttons provide a model when a matching browser voice is available.</p>'
        % (H.escape(tp["title"]), H.escape(language)),
        '<ol class="practice-cues">%s</ol>' % cues,
    ]
    if topic_source_word_count(tp) < 400:
        anchor = samples[0]
        parts.append(
            '<p class="practice-focus"><b>Transfer practice.</b> %s Start from '
            '<span lang="%s" dir="auto">%s</span> (<i>%s</i>) and decide whether '
            'it fits the situation before using it elsewhere.</p>'
            % (H.escape(focus), H.escape(cfg["code"], quote=True),
               H.escape(anchor["bn"]), H.escape(anchor["say"]))
        )
    contrast = samples[-1]
    parts += [
        '<p class="practice-context"><b>Context check.</b> For %s, “%s” belongs to a particular setting. A common mistake is to treat an English gloss as universal; read the language-specific note above and ask a fluent speaker when local usage differs.</p>'
        % (H.escape(tp["title"]), H.escape(contrast["en"])),
        '<details class="practice-key"><summary>Check your recall: answer key</summary><ol>%s</ol></details>' % key,
        '</section>'
    ]
    return "\n".join(parts)


_TOPIC_SCRIPT_BLOCKS = {
    "bn": r"\u0980-\u09FF", "gu": r"\u0A80-\u0AFF",
    "kn": r"\u0C80-\u0CFF", "ml": r"\u0D00-\u0D7F",
    "mr": r"\u0900-\u097F", "pa": r"\u0A00-\u0A7F",
    "ta": r"\u0B80-\u0BFF", "te": r"\u0C00-\u0C7F",
    "ur": r"\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF",
}
_TOPIC_SCRIPT_PATTERNS = {}


def _topic_script_pattern(code):
    block = _TOPIC_SCRIPT_BLOCKS.get(code)
    if not block:
        return None
    if code not in _TOPIC_SCRIPT_PATTERNS:
        char = "[" + block + "]"
        joined = char + r"+(?:[\u200c\u200d]*" + char + r"+)*(?:[\s\u00a0]+" + char + r"+(?:[\u200c\u200d]*" + char + r"+)*)*"
        _TOPIC_SCRIPT_PATTERNS[code] = re.compile(joined)
    return _TOPIC_SCRIPT_PATTERNS[code]


def _topic_speaker(text, code, language_name):
    spoken = H.escape(text)
    quoted = H.escape(text, quote=True)
    label = H.escape("Play %s in %s" % (text, language_name), quote=True)
    return ('<span lang="%s" dir="auto">%s</span>'
            '<button type="button" class="ssay" data-sb-say="%s" data-voice-lang="%s" '
            'aria-label="%s" aria-pressed="false"><span aria-hidden="true">🔊</span></button>') % (
                H.escape(code, quote=True), spoken, quoted, H.escape(code, quote=True), label)


def _topic_language_span(text, code):
    return '<span lang="%s" dir="auto">%s</span>' % (
        H.escape(code, quote=True), H.escape(text))


def _foreign_topic_language(text, start, end, code, topic_slug):
    """Use explicit Hindi comparison labels; otherwise shared Devanagari stays contextual."""
    if code != "mr":
        return None
    value = str(text or "")
    before = value[max(0, start - 120):start]
    after = value[end:end + 80]
    labels = list(re.finditer(r"\b(Hindi|Marathi)\s*[:=]\s*", before, re.I))
    if labels and labels[-1].group(1).casefold() == "hindi":
        return ("hi", "Hindi")
    if re.search(r"\bHindi\s+$", before, re.I) or re.match(r"\s*\(\s*Hindi\s*\)", after, re.I):
        return ("hi", "Hindi")
    if topic_slug == "marathi-vs-hindi":
        run = value[start:end].strip()
        if run == "हिंदी" or re.search(r"(?:/|\bagainst(?:\s+Hindi)?)\s*$", before, re.I):
            return ("hi", "Hindi")
        if re.match(r"\s+stands\s+Hindi-classic\b", after, re.I):
            return ("hi", "Hindi")
    return None


def _speaker_controls_in_text_nodes(page, code, language_name, topic_slug=""):
    """Tag visible target prose and add controls only outside existing links."""
    pattern = _topic_script_pattern(code)
    if not pattern:
        return page
    chunks = re.split(r"(<[^>]+>)", page)
    output, skipped = [], []
    language_context = []
    anchor_depth = 0
    void = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    for chunk in chunks:
        if chunk.startswith("<"):
            match = re.match(r"<\s*(/?)\s*([a-zA-Z0-9]+)\b", chunk)
            if match:
                closing, tag = match.groups(); tag = tag.lower()
                if closing:
                    if tag == "a" and anchor_depth and not skipped:
                        anchor_depth -= 1
                    if skipped and skipped[-1] == tag:
                        skipped.pop()
                    for index in range(len(language_context) - 1, -1, -1):
                        if language_context[index][0] == tag:
                            language_context = language_context[:index]
                            break
                elif not skipped and tag not in void:
                    classes = re.search(r"\bclass\s*=\s*(['\"])(.*?)\1", chunk, re.I)
                    class_names = set(classes.group(2).split()) if classes else set()
                    hidden = re.search(r"\baria-hidden\s*=\s*(['\"])true\1", chunk, re.I)
                    lang = re.search(r"\blang\s*=\s*(['\"])(.*?)\1", chunk, re.I)
                    lang_value = lang.group(2) if lang else ""
                    explicitly_hindi = lang and lang_value.lower().split("-", 1)[0] == "hi"
                    if lang:
                        language_context.append((tag, lang_value))
                    if tag == "a":
                        anchor_depth += 1
                    if tag in {"script", "style", "noscript", "button"} or hidden or explicitly_hindi or (tag == "td" and "bn" in class_names):
                        skipped.append(tag)
            output.append(chunk)
        elif skipped:
            output.append(chunk)
        else:
            nearest = language_context[-1][1].lower().split("-", 1)[0] if language_context else ""

            def speak(match):
                foreign = _foreign_topic_language(chunk, match.start(), match.end(), code, topic_slug)
                route = foreign or (code, language_name)
                if anchor_depth:
                    # Link text is already a keyboard-operable link. Keep its
                    # BCP-47 attribution without placing a second control inside.
                    return match.group(0) if nearest == route[0] else _topic_language_span(match.group(0), route[0])
                return _topic_speaker(match.group(0), *route)

            output.append(pattern.sub(speak, chunk))
    return "".join(output)


def _speaker_controls_in_body(page, code, language_name, topic_slug=""):
    """Limit language additions to visible body content, never head metadata."""
    body = re.search(r"(<body\b[^>]*>)([\s\S]*?)(</body\s*>)", page, re.I)
    if not body:
        return page
    content = _speaker_controls_in_text_nodes(
        body.group(2), code, language_name, topic_slug)
    return (page[:body.start()] + body.group(1) + content
            + body.group(3) + page[body.end():])


def topic_page(cfg, tp, prev_tp, next_tp, live):
    d, pre = cfg["dir"], "../../"
    url = "%s/%s/" % (d, tp["slug"])
    language_name = re.sub(r"^Learn\s+", "", cfg["title"])
    rows = []
    for ph in tp["phrases"]:
        spoken = H.escape(ph["bn"])
        label = H.escape("Play %s in %s" % (ph["bn"], language_name), quote=True)
        rows.append(
            '<tr><td>%s</td><td class="bn" lang="%s" dir="auto">%s'
            '<button type="button" class="ssay" data-sb-say="%s" data-voice-lang="%s" '
            'aria-label="%s" aria-pressed="false"><span aria-hidden="true">🔊</span></button>'
            '</td><td><i>%s</i></td></tr>'
            % (H.escape(ph["en"]), H.escape(cfg["code"], quote=True), spoken,
               H.escape(ph["bn"], quote=True), H.escape(cfg["code"], quote=True),
               label, H.escape(ph["say"]))
        )
    faqs = "".join(
        "<div class=\"faq\"><b>%s</b><p>%s</p></div>"
        % (H.escape(f["q"]), H.escape(f["a"])) for f in tp["faqs"])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": "%s/%s#article" % (BASE, url),
         "headline": localised(tp["title"], cfg["title"]),
         "description": tp["desc"],
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
    cta = ('<aside class="cta" aria-label="Next step"><h2>Ready to test yourself?</h2>'
           '<p>Turn this topic into lasting memory — quiz, practice and review, all free.</p>'
           '<a class="cta-btn" href="%s">Quiz yourself</a></aside>') % cfg["quiz_url"]
    seo_title = localised(tp["title"], cfg["title"])
    seo_desc = tp["desc"] if cfg["title"].lower() in tp["desc"].lower() else \
        "%s: %s" % (cfg["title"], tp["desc"])
    body = ["<div class=\"pw\">",
            "<p class=\"crumb\"><a href=\"%s\">EkGuru</a> \u203a "
            "<a href=\"../\">%s</a> \u203a %s</p>"
            % (pre, H.escape(cfg["hub_title"]), H.escape(tp["title"])),
            '<article class="topic-core" data-topic-core="true" data-language="%s" data-topic="%s" data-topic-fingerprint="%s">'
            % (H.escape(cfg["code"], quote=True), H.escape(tp["slug"], quote=True),
               content_fingerprint(cfg, tp)),
            '<div class="hero">',
            '<span class="kicker">%s</span>' % H.escape(cfg["title"]),
            "<h1>%s</h1>" % H.escape(localised(tp["h1"], cfg["title"])),
            "<p class=\"lede\">%s</p>" % H.escape(tp["lede"]),
            '</div>',
            hint(cfg["title"])]
    body += ["<p>%s</p>" % p for p in tp["paras"]]
    body += ["<h2>Words and phrases for this topic</h2>",
             "<div class=\"twrap\"><table class=\"phr\"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead>"
             "<tbody>%s</tbody></table></div>" % (tuple(H.escape(x) for x in tp["table_head"]) + ("".join(rows),))]
    body += ["<h2>Language, culture, and common traps</h2>",
             '<div class="note">%s</div>' % tp["note"],
             practice_section(cfg, tp),
             "<h2>Questions learners ask</h2>", faqs,
             "</article>",
             '<section class="topic-navigation" aria-label="Continue learning">',
             "<h2>Everything on this topic</h2>",
             '<ul class="linklist">' + "".join(
                 '<li><a href="%s">%s</a><span>%s</span></li>'
                 % (l["url"], H.escape(l["label"]), H.escape(l["desc"]))
                 for l in tp["links"]) + "</ul>"]
    body += ["<h2>Keep learning %s</h2>" % H.escape(cfg["title"]),
             '<div class="chips"><a href="%s">Full %s course</a>'
             '<a href="%s">%s world course</a>'
             '<a href="%s">Quiz yourself</a></div>'
             % (cfg["course_url"], H.escape(cfg["title"]),
                cfg["world_url"], H.escape(cfg["title"]), cfg["quiz_url"]),
             "<h2>Related topics</h2>",
             '<div class="chips">' + "".join(
                 '<a href="../%s/">%s</a>' % (t["slug"], H.escape(t["title"]))
                 for t in live if t["slug"] != tp["slug"]) + "</div>",
             cta, nav, "</section>", "</div>"]
    page = (head(seo_title, seo_desc, url, pre,
                 json.dumps(ld, ensure_ascii=False))
            + "<body>\n" + "\n".join(body) + "\n" + footer(pre)
            + MARK + "\n" + '<script src="%sjs/storybook.js" defer></script>\n'
            % pre + "</body>\n</html>\n")
    page = _speaker_controls_in_body(page, cfg["code"], language_name, tp["slug"])
    return page.replace("</body>", TOPIC_VOICE_MARKER + "\n</body>", 1)


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
    body = [TOPIC_HUB_VOICE_MARKER,
            "<div class=\"pw\" data-topic-hub-fingerprint=\"%s\">" % content_fingerprint(cfg),
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
    hub_desc = cfg["lede"] if cfg["title"].lower() in cfg["lede"].lower() else \
        "%s: %s" % (cfg["title"], cfg["lede"])
    page = (head(cfg["hub_title"], hub_desc, d + "/", pre,
                 json.dumps(ld, ensure_ascii=False))
            + "<body>\n" + "\n".join(body) + "\n" + footer(pre)
            + MARK + "\n" + '<script src="%sjs/storybook.js" defer></script>\n'
            % pre + "</body>\n</html>\n")
    language_name = re.sub(r"^Learn\s+", "", cfg["title"])
    return _speaker_controls_in_body(page, cfg["code"], language_name)


def main():
    args = list(sys.argv[1:])
    check = "--check" in args
    args = [a for a in args if a != "--check"]
    unknown = [a for a in args if not re.fullmatch(r"[a-z]{2,3}", a)]
    if unknown:
        raise SystemExit("Usage: python3 tools/build-lang-topics.py [code ...] [--check]")
    codes = args or sorted(
        os.path.basename(f)[:-5] for f in glob.glob("data/topics/*.json"))
    for code in codes:
        build(code, check=check)


def build(code, check=False):
    with open("data/topics/%s.json" % code, encoding="utf-8") as f:
        cfg = json.load(f)
    live = cfg["topics"]
    live_slugs = {t["slug"] for t in live}
    skip = set(cfg.get("mirror_skip", []))
    order = [s for s in list(MIRROR) + list(cfg.get("mirror_extra", [])) if s not in skip]
    coming = [(s, cfg["coming_titles"].get(s, s.replace("-", " ").title()))
              for s in order if s not in live_slugs]
    hub_path = os.path.join(cfg["dir"], "index.html")
    topic_paths = [os.path.join(cfg["dir"], tp["slug"], "index.html") for tp in live]
    if check:
        stale = []
        if not os.path.isfile(hub_path):
            stale.append("missing hub")
        else:
            hub_raw = open(hub_path, encoding="utf-8", errors="replace").read()
            expected = content_fingerprint(cfg)
            if not re.search(r'data-topic-hub-fingerprint=["\']' + re.escape(expected) + r'["\']', hub_raw):
                stale.append("stale hub")
        for i, (tp, path) in enumerate(zip(live, topic_paths)):
            if not os.path.isfile(path):
                stale.append("missing " + tp["slug"])
                continue
            raw = open(path, encoding="utf-8", errors="replace").read()
            expected = content_fingerprint(cfg, tp)
            if not re.search(r'data-topic-fingerprint=["\']' + re.escape(expected) + r'["\']', raw):
                stale.append("stale " + tp["slug"])
        if stale:
            raise SystemExit("lang-topics [%s]: %d stale/missing page(s): %s" %
                             (code, len(stale), ", ".join(stale[:12])))
        print("lang-topics [%s]: hub + %d topics current (%d coming-soon cards)."
              % (code, len(live), len(coming)))
        return

    os.makedirs(cfg["dir"], exist_ok=True)
    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(hub_page(cfg, live, coming))
    for i, tp in enumerate(live):
        path = topic_paths[i]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(topic_page(cfg, tp,
                               live[i - 1] if i > 0 else None,
                               live[i + 1] if i + 1 < len(live) else None,
                               live))
    print("lang-topics [%s]: hub + %d topics, %d coming-soon cards."
          % (code, len(live), len(coming)))


if __name__ == "__main__":
    main()
