#!/usr/bin/env python3
"""EkGuru — the 38 missing learn-hindi-from-* country pages (196 total).

    python3 tools/build-country-funnel-pages.py

The old country-page generator is gone; the 158 existing pages are frozen.
This script builds ONLY the 38 missing ones, by transforming a copy of the
Maldives page (template-by-extraction: markup, comments, scripts and styles
are byte-identical to the house standard by construction).

Per-country substance (the "Why people in X learn Hindi" section) is
hand-written, specific and true for each country — the index page's own
anti-doorway rule ("pages get written when there is something specific
and true to write") is what kept these 38 unpublished until now.

Also wires: learn-hindi-by-country (ItemList 158->196, Long-tail chips,
"Every other country" section retired), sitemap-countries.xml (+38).

Idempotent: re-runs overwrite the same 38 files; the 158 frozen pages
are never touched.
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SITE = "https://ekguru.shop"
TODAY = "2026-09-14"
IST_START, IST_END = 9 * 60, 22 * 60  # tutor window on Indian time
IST_MIN = 5 * 60 + 30

# cc, slug, name, utc minutes, utc label, currency, why-paragraph, tz note?
DATA = [
 ("AD", "andorra", "Andorra", 60, "UTC+1", "EUR",
  "Andorra runs on three languages at once \u2014 Catalan at home, Spanish and French everywhere else \u2014 so its residents are already practised switchers, and that habit is the real head start: Hindi becomes a fourth system, not a first shock. The structural help is thinner. Catalan and Spanish are distant Indo-European cousins of Hindi, which shows up in the occasional deep cognate and almost nowhere else; the verb-final order, the postpositions and Devanagari all have to be learned cold. Most learners here have a concrete reason \u2014 an Indian partner, trade through Barcelona or Toulouse, a posting \u2014 and concrete reasons finish courses.", None),
 ("AG", "antigua-and-barbuda", "Antigua and Barbuda", -240, "UTC-4", "XCD",
  "Antigua\u2019s learners usually come through work or family: tourism staff serving a growing stream of Indian visitors, nurses and students who trained abroad, mixed households. English is the medium of everything, so lessons themselves need no translation layer \u2014 but English gives nothing structurally, and Antiguan Creole\u2019s analytic grammar is the opposite of Hindi\u2019s inflection, so the verb system deserves the bulk of early effort. The consolation is scheduling honesty: at UTC-4 the teaching window falls overnight, which suits night owls and nobody else \u2014 the booking page shows it in your own time so there are no surprises.", None),
 ("AO", "angola", "Angola", 60, "UTC+1", "AOA",
  "Angola and India trade oil, diamonds and scholarships \u2014 Luanda has an established Indian merchant community, and Angolan students take Indian government scholarships every year, so Hindi here is usually a career language rather than a hobby. Portuguese gives Latin-script comfort and a stock of shared Indo-European roots, but little beyond that; for Umbundu, Kimbundu or Kongo speakers, the Bantu noun-class instinct maps usefully onto Hindi\u2019s two genders and agreement. Expect the alphabet to be the first project and the postpositional phrase the second.", None),
 ("BF", "burkina-faso", "Burkina Faso", 0, "UTC+0", "XOF",
  "Hindi in Burkina Faso travels on two rails: scholarships that send Burkinab\u00e8 students to Indian universities, and the Sahel-wide familiarity with Indian films and songs, which means many learners arrive already able to hum the sounds. French handles the medium of lessons; Moor\u00e9 and Dyula, both tonal, give sharp ears but no structural shortcut \u2014 Hindi\u2019s verb-final order and split ergativity are new to everyone here. Be ready for a longer spoken phase before reading, and let the songs do some of the pronunciation work.", None),
 ("BI", "burundi", "Burundi", 120, "UTC+2", "BIF",
  "Burundi is Rundi-speaking first and francophone second, and Hindi learners here are usually students bound for Indian universities on government scholarships, or health and NGO workers whose careers pass through India. Rundi\u2019s noun classes are good preparation for a language where gender and agreement run everything, though the classes themselves do not transfer. With French as the lesson medium and Kirundi logic underneath, most learners find listening comprehension arrives well before fluent speech \u2014 plan accordingly.", None),
 ("BJ", "benin", "Benin", 60, "UTC+1", "XOF",
  "Cotonou\u2019s port trade put an Indian merchant community on the ground generations ago, and Beninese students join Indian universities on scholarships each year \u2014 the two most common reasons anyone here starts Hindi. French carries the lessons; Fon and Yoruba, with their aspect-heavy verbs and serial constructions, prepare you better than you would expect for Hindi\u2019s compound verbs, even if nothing transfers directly. Tonal first languages also mean the four-way Hindi consonant contrast usually clicks faster than the alphabet does.", None),
 ("BS", "bahamas", "Bahamas", -300, "UTC-5", "BSD",
  "The Bahamas learns Hindi through contact, not curriculum: tourism workers in Nassau and Freeport serving Indian visitors, a small long-settled Indian business community, students returning from study abroad. English does all the carrying, which makes lessons easy to follow and the grammar entirely new \u2014 there is no shortcut around the verb-final order or Devanagari. The practical fact that matters most is the clock: five hours behind India, the teaching window runs overnight, so check the converted times before picturing a routine.", None),
 ("CF", "central-african-republic", "Central African Republic", 60, "UTC+1", "XAF",
  "Bangui is francophone and Sango-speaking, and Hindi here is a language of scholarships and postings \u2014 students bound for Indian universities, mission and NGO workers whose routes run through the subcontinent. Sango\u2019s stripped-down creole grammar is about as far from Hindi\u2019s inflection as a language gets, so treat the verb system as the main project and let French carry everything else. Demand is thin but real, which is exactly why one-to-one lessons fit: there is no classroom cohort to wait for.", None),
 ("CV", "cape-verde", "Cape Verde", -60, "UTC-1", "CVE",
  "More Cape Verdeans live abroad than at home, and Hindi usually enters through that diaspora \u2014 family in Lisbon or Boston, a posting, a partner \u2014 rather than through anything on the islands themselves. Kabuverdianu gives Portuguese-flavoured vocabulary and Latin-script ease, but as a creole it offers no bridge to Hindi\u2019s morphology; expect everything grammatical to be new. The islands sit an hour behind UTC, so lesson times land in the small hours \u2014 the converted window below is worth reading twice.", None),
 ("DM", "dominica", "Dominica", -240, "UTC-4", "XCD",
  "Dominica is small enough that every Hindi learner has a nameable reason: tourism work, a nursing or medical path that runs through schools abroad, family abroad, plain curiosity fed by Indian films. English carries the lessons and Kw\u00e9y\u00f2l carries daily life; neither helps with Hindi\u2019s verb-last sentences or its script, so budget the first month for sound and alphabet alone. At UTC-4 the window is a night-owl window \u2014 the booking page converts it exactly.", None),
 ("FM", "micronesia", "Micronesia", 660, "UTC+11", "USD",
  "Realism first: hardly anyone in Chuuk, Pohnpei, Kosrae or Yap is learning Hindi today, and this page exists for the exceptions \u2014 students at US colleges meeting Hindi-speaking classmates, seafarers and nurses whose routes cross Indian crews, the merely curious. Chuukese, Pohnpeian, Kosraean and Yapese share nothing structural with Hindi, so the course starts from zero with no apologies. Note the federation spans two time zones; the window below uses Pohnpei time, and the booking page will show your island\u2019s own.",
  "The federation spans two zones \u2014 Chuuk at UTC+10, Pohnpei and Kosrae at UTC+11. The window above uses Pohnpei time; Chuuk readers should shift everything one hour earlier, and the booking page converts automatically."),
 ("GM", "gambia", "Gambia", 0, "UTC+0", "GMD",
  "Banjul and Serrekunda have traded with Indian merchants for generations, and Gambian students take Indian scholarships every year \u2014 Hindi here is a working language with a trade route behind it. English carries lessons; Mandinka, Wolof and Pular carry life, and none of them shortens the road to verb-final sentences or Devanagari. What does help is ear training: several Gambian first languages are tonal, and tonal ears tend to catch Hindi\u2019s aspiration contrasts early.", None),
 ("GN", "guinea", "Guinea", 0, "UTC+0", "GNF",
  "Conakry\u2019s Indian business community and the bauxite trade give Guinea a concrete, commercial reason to learn Hindi, and scholarships add an academic one. French is the lesson medium; Pular, Maninkakan and Susu underneath mean most learners already juggle two or three grammars, which is the best preparation there is for a fourth. Hindi\u2019s SOV order will still feel backwards for the first weeks \u2014 that passes \u2014 and the Perso-Arabic loanwords scattered through Hindi-Urdu will feel oddly familiar to any Arabic-schooled learner.", None),
 ("GQ", "equatorial-guinea", "Equatorial Guinea", 60, "UTC+1", "XAF",
  "Equatorial Guinea is Africa\u2019s only Spanish-official state, an oil economy where most study-abroad routes run to Spain \u2014 so Hindi learners here almost always have a personal reason: a partner, a posting, a plan. Spanish gives script comfort and distant Indo-European cousinhood; Fang, a Bantu language, gives a working instinct for agreement systems. With Malabo an hour behind India, the window is a civilised one \u2014 mornings and afternoons, no alarms in the dark.", None),
 ("GW", "guinea-bissau", "Guinea-Bissau", 60 - 60, "UTC+0", "XOF",
  "Follow the cashews: Guinea-Bissau grows them and India processes them, which makes Hindi arguably the most commercially useful Asian language in Bissau. Guinea-Bissau Creole, the language of daily life, is Portuguese-lexified and grammatically simple \u2014 no bridge to Hindi\u2019s inflection, but no interference either. Scholarships and trade-family ties supply the learners; the alphabet and the verb system supply the work.", None),
 ("KI", "kiribati", "Kiribati", 720, "UTC+12", "AUD",
  "Kiribati\u2019s 33 atolls are spread across three time zones and stitched together by seafaring \u2014 I-Kiribati crews work foreign ships, and students pass through Fiji\u2019s universities, where Fiji Hindi is part of the soundscape. That contact is the realistic door into Hindi here, along with plain curiosity. Gilbertese shares nothing with Hindi structurally, and the lesson window below uses Tarawa time; outer-island readers should trust the booking page\u2019s conversion over everything printed here.",
  "Kiribati spans three zones, UTC+12 to UTC+14. The window above uses Tarawa time (UTC+12); the Line Islands sit two hours later. Trust the booking page\u2019s conversion over this paragraph."),
 ("KN", "saint-kitts-and-nevis", "Saint Kitts and Nevis", -240, "UTC-4", "XCD",
  "Fifty thousand people, two islands, one time zone: St Kitts and Nevis learns Hindi the way small Caribbean states learn anything \u2014 through tourism work, study abroad, mixed families, and films. English does the carrying, which keeps lessons smooth and the grammar entirely new; budget real time for the verb-final habit and the script. The window falls overnight at UTC-4, so this is a course for night owls or early risers with discipline.", None),
 ("KP", "north-korea", "North Korea", 540, "UTC+9", "KPW",
  "Begin with the truth: inside the DPRK there is no open internet, no international payment route, and no private tutoring market, so live online lessons are not realistically accessible to ordinary residents. This page exists for the people it can actually serve \u2014 linguists comparing Korean with Hindi-Urdu (both verb-final, both particle-rich, a genuine scholarly pairing), ethnic Korean scholars abroad, and the curious. For anyone who can study, Korean is unusually good preparation: the verb goes last, particles do the grammatical work, and honorifics rhyme with Hindi\u2019s three levels of \u2018you\u2019.", None),
 ("LI", "liechtenstein", "Liechtenstein", 60, "UTC+1", "CHF",
  "Thirty-eight thousand residents, a finance-and-precision economy, and companies operating across India \u2014 Liechtenstein\u2019s Hindi learners are usually professionals with subcontinent business or mixed families in the Rhine valley. German is genuinely useful preparation: four cases train the exact muscle Hindi\u2019s postpositions need, and the standard-versus-Alemannic split at home is a lived version of Hindi\u2019s own register range. The window is an early one \u2014 mornings in Vaduz, afternoons in Delhi.", None),
 ("LR", "liberia", "Liberia", 0, "UTC+0", "LRD",
  "Liberia\u2019s American-settler history made it English-official in a francophone region, and that English carries Hindi lessons without friction. Underneath, Kpelle, Bassa and Grebo run daily life; and Vai-speaking learners hold a rare card \u2014 the Vai syllabary means Devanagari would be their second non-Latin script, not their first. Most learners here are students, traders and NGO workers; India enters the picture through scholarships, commerce and the subcontinent\u2019s large footprint in West African trade.", None),
 ("MC", "monaco", "Monaco", 60, "UTC+1", "EUR",
  "Monaco learns Hindi at the intersection of finance, yachting and family: private-wealth professionals with India desks, crew and staff whose working world includes Indian colleagues and clients, students between systems. French and Italian give the usual Romance head start \u2014 real but shallow, mostly vocabulary and script \u2014 while the trilingual Mon\u00e9gasque norm (French, Italian, English before breakfast) is the deeper advantage. Scheduling is humane: an hour behind India puts lessons in the morning and afternoon.", None),
 ("MH", "marshall-islands", "Marshall Islands", 720, "UTC+12", "USD",
  "Majuro and Ebeye face the Pacific, but Marshallese students and the large US diaspora face a world where Hindi-Urdu is everywhere \u2014 the realistic path into Hindi here runs through American colleges and workplaces. Marshallese itself, a Micronesian language, shares nothing structural with the target, so the course starts clean. The window below is a long day\u2019s window, running afternoon into the small hours; the booking page converts it exactly.", None),
 ("ML", "mali", "Mali", 0, "UTC+0", "XOF",
  "Mali counts thirteen official languages, and that number tells you the country\u2019s attitude: multilingualism is normal life, not an achievement. Bambara, the great lingua franca, puts the verb last exactly like Hindi \u2014 a genuine structural gift most learners never get \u2014 while Timbuktu\u2019s manuscript heritage means a new script is a familiar kind of project, not a frightening one. Add scholarships and gold-and-cotton trade with India, and Hindi in Bamako has firmer ground than its small numbers suggest.", None),
 ("NE", "niger", "Niger", 60, "UTC+1", "XOF",
  "If you grew up in Niamey or Kano\u2019s orbit, you may already know Hindi songs by heart \u2014 the Sahel\u2019s love affair with Indian films is decades old, and it means many Nig\u00e9rien learners arrive with the sounds pre-installed. Hausa gives no grammatical shortcut (it is Afro-Asiatic, verb-medial), but the cultural door stands wide open, and traders and scholarship students walk through it every year. Let the films carry pronunciation; spend lesson time on the verb system and the script.", None),
 ("NR", "nauru", "Nauru", 720, "UTC+12", "AUD",
  "Nauru has about twelve thousand residents, one phosphate island, and \u2014 realistically \u2014 not one Hindi classroom. This page exists anyway, for completeness and for whoever the exception turns out to be: a student abroad, a worker returned with new plans, the merely curious. English carries the lessons; Nauruan carries the island. The window below is computed honestly for UTC+12, and the booking page will confirm it in your own time.", None),
 ("PW", "palau", "Palau", 540, "UTC+9", "USD",
  "Palau\u2019s eighteen thousand people host a dive-tourism economy and a Compact relationship with the United States, and Hindi usually arrives with visitors, students and returning workers rather than any local tradition. Palauan word order runs verb-first \u2014 the mirror image of Hindi \u2014 so the first adjustment is genuinely conceptual, in a way flashcards cannot fix and conversation can. Japanese, co-official in one state, at least proves the islands can hold more than one Asian language at a time.", None),
 ("SB", "solomon-islands", "Solomon Islands", 660, "UTC+11", "SBD",
  "Honiara runs on Pijin, an English-lexified creole that gives its speakers a full English vocabulary bridge \u2014 useful, since lessons themselves happen in English. Hindi proper is rare here: the realistic learners are students in Australia and Papua New Guinea, public servants trained abroad, mixed families. Pijin grammar will not help with Hindi verbs and may briefly interfere (word order first), so expect the sentence-structure guide to earn its keep.", None),
 ("SL", "sierra-leone", "Sierra Leone", 0, "UTC+0", "SLE",
  "Freetown\u2019s Krio speakers already live the lesson Hindi-Urdu teaches \u2014 two codes, one conversation, constant switching \u2014 and that instinct transfers even though no vocabulary does. South Asian trading families, scholarships and a busy student corridor give Sierra Leone concrete reasons to learn, beyond curiosity. Temne and Mende underneath add tonal ears; English on top carries the lessons. The window is an early-riser\u2019s window at UTC+0.", None),
 ("SM", "san-marino", "San Marino", 60, "UTC+1", "EUR",
  "Thirty-three thousand citizens on a mountaintop, wrapped around Emilia-Romagna: San Marino\u2019s Hindi learners are students and professionals in the Bologna orbit, mixed families, the curious. Italian gives the standard Romance cousinhood \u2014 helpful vocabulary echoes, no grammatical ride \u2014 and Romagnol at home adds one more proof that small places hold big repertoires. Mornings in the Citt\u00e0, afternoons in Delhi: the window below.", None),
 ("SS", "south-sudan", "South Sudan", 120, "UTC+2", "SSP",
  "The world\u2019s newest country runs daily life in Juba Arabic, a creole most residents already pair with English and a mother tongue like Dinka or Nuer \u2014 three-way switching as standard equipment. Hindi enters through scholarships, NGO careers and trade with neighbours whose Indian business networks are old and deep. Juba Arabic gives no structural help, but code-switchers learn code-switching fast. Lessons run mornings to late afternoon, Juba time.", None),
 ("ST", "sao-tome-and-principe", "S\u00e3o Tom\u00e9 and Pr\u00edncipe", 0, "UTC+0", "STN",
  "Two islands, two hundred thousand people, one long cocoa history: S\u00e3o Tom\u00e9\u2019s study-abroad routes mostly run to Portugal and Brazil, so Hindi learners here are self-selected \u2014 traders, scholarship students, the determined curious. Forro, the Portuguese-lexified creole of daily life, gives script comfort and no grammar bridge. At UTC+0 the window is made for early risers; the booking page will show it in your own time.", None),
 ("TD", "chad", "Chad", 60, "UTC+1", "XAF",
  "N\u2019Djamena sits where francophone administration meets Chadian Arabic daily life, and that Arabic is a quiet superpower for Hindi-Urdu: kitab, duniya, waqt \u2014 every Perso-Arabic loanword in the language lands as an old friend. Learners here are usually scholarship students, traders on trans-Saharan routes, and mission and NGO workers. French carries the lessons; the verb-final order and Devanagari are the real syllabus. Mornings to late afternoon, N\u2019Djamena time.", None),
 ("TG", "togo", "Togo", 0, "UTC+0", "XOF",
  "Lom\u00e9\u2019s port faces the Accra\u2013Lagos corridor, one of West Africa\u2019s busiest commercial seams, and Togolese traders work it daily \u2014 commerce, scholarships and curiosity supply the Hindi learners. Ewe, tonal and verb-serialising, at least trains the ear and the instinct for stacked verbs; French carries the lessons. Coastal West Africa knows Indian films the way it knows its own, so pronunciation often arrives ahead of grammar \u2014 spend lessons accordingly.", None),
 ("TO", "tonga", "Tonga", 780, "UTC+13", "TOP",
  "The Pacific kingdom that was never colonised, with more Tongans abroad than at home: Hindi usually meets Tonga through the diaspora \u2014 seasonal workers in Australia and New Zealand, students, church and family networks where Indian neighbours are simply part of life. Tongan runs verb-first, Hindi verb-last, so the sentence habit has to flip. At UTC+13 the window runs afternoon into the small hours; check it against your own routine.", None),
 ("TV", "tuvalu", "Tuvalu", 720, "UTC+12", "AUD",
  "Eleven thousand people, nine atolls, one famous internet domain: Tuvalu learns Hindi, when it does, through Fiji \u2014 students at the regional university in Suva live inside a soundscape where Fiji Hindi is ordinary background. Seafaring adds a second thread. Tuvaluan itself shares nothing structural with the target, and at UTC+12 the window is an afternoon-into-night one. A page for the exceptions, written honestly for whoever they are.", None),
 ("VA", "vatican-city", "Vatican City", 60, "UTC+1", "EUR",
  "Eight hundred residents, nearly all clergy, diplomats or Guards \u2014 and a serious reason to learn Hindi: priests, nuns and seminarians bound for ministry in India, where the Church runs thousands of schools and hospitals. Ecclesiastical Latin, still the working language of the Holy See, trains exactly the case-system muscle Hindi\u2019s postpositions need. Lessons run mornings to late afternoon, Rome time; the booking page converts from there.", None),
 ("VU", "vanuatu", "Vanuatu", 660, "UTC+11", "VUV",
  "Vanuatu holds the densest linguistic landscape on earth \u2014 over a hundred vernaculars for three hundred thousand people \u2014 and ni-Vanuatu children routinely grow up multilingual, which research keeps flagging as the best predictor of learning one more. Hindi arrives through seasonal work in Australia and New Zealand, where Indian co-workers are common, and through study abroad. Bislama carries English vocabulary; everything grammatical starts fresh.", None),
 ("WS", "samoa", "Samoa", 780, "UTC+13", "WST",
  "Fa\u2018a Samoa travels: more Samoans live in Auckland, Sydney and the US than on the islands, and Hindi meets Samoa mostly through that diaspora \u2014 seasonal workers, students, church networks, neighbours. Samoan runs verb-first against Hindi\u2019s verb-last, so the sentence frame has to be rebuilt rather than adjusted. At UTC+13 the window stretches from afternoon deep into the night; the booking page shows it in your time.", None),
]
assert len(DATA) == 38


def fmt(mins):
    mins %= 1440
    return "%02d:%02d" % (mins // 60, mins % 60)


def window(utc_min):
    delta = utc_min - IST_MIN
    s, e = fmt(IST_START + delta), fmt(IST_END + delta)
    overnight = (IST_END + delta) % 1440 <= (IST_START + delta) % 1440
    return s + (" (previous day)" if overnight else ""), e


def names_by_slug():
    """Display names for every country page: index ItemList + new DATA."""
    h = open("learn-hindi-by-country/index.html", encoding="utf-8").read()
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    ld = json.loads(m.group(1))
    out = {}
    for g in ld["@graph"]:
        if g.get("@type") == "ItemList":
            for it in g["itemListElement"]:
                slug = it["url"].rstrip("/").rsplit("learn-hindi-from-", 1)[1]
                out[slug] = it["name"].replace("Learn Hindi from ", "")
    for cc, slug, name, *_ in DATA:
        out[slug] = name
    return out


def build_page(tpl, entry, sib_slugs, names):
    cc, slug, name, utc_min, utc_label, cur, why, tz_note = entry
    s, e = window(utc_min)
    h = tpl
    # 1. why paragraph (whole <p> after the why-h2)
    h, n = re.subn(r'(<h2>Why people in )Maldives( learn Hindi</h2>\n<p>).*?(</p>)',
                   lambda m: m.group(1) + "§§NAME§§" + m.group(2) + why + m.group(3),
                   h, count=1)
    assert n == 1, "why anchor"
    # 2. tokens (order: MVR before MV; maldives before Maldives irrelevant — distinct case)
    for old, new in [("MVR", cur), ("MV", cc), ("from-mv", "from-" + cc.lower()),
                     ("maldives", slug), ("Maldives", name),
                     ("08:30", s), ("21:30", e),
                     ("<b>UTC+5</b>", "<b>" + utc_label + "</b>"),
                     ("at UTC+5,", "at " + utc_label + ",")]:
        assert old in h, "missing token %r" % old
        h = h.replace(old, new)
    h = h.replace("§§NAME§§", name)
    # 3. tz note for multi-zone countries
    if tz_note:
        anchor = "that will be right.</p>"
        assert anchor in h
        h = h.replace(anchor, anchor + "\n<p>" + tz_note + "</p>", 1)
    # 4. sibling chips: next 12 + All countries (plain string surgery — no regex)
    chips = "\n".join('  <a href="../learn-hindi-from-%s/">%s</a>' % (sl, names[sl]) for sl in sib_slugs)
    chips += '\n  <a href="../learn-hindi-by-country/">All countries \u2192</a>'
    i = h.find("Learning Hindi from somewhere else?</h2>")
    assert i != -1, "sib h2"
    j = h.find('<div class="chips">', i)
    assert j != -1, "sib div"
    k = h.find("</div>", j)
    assert k != -1, "sib close"
    h = h[:j] + '<div class="chips">\n' + chips + '\n</div>' + h[k + len("</div>"):]
    return h


def qc(h, entry):
    cc, slug, name, utc_min, utc_label, cur, why, tz_note = entry
    # leftover scan runs on everything BEFORE the sibling-chips section, because
    # windows near "maldives" (liberia, liechtenstein) legitimately link to it
    core = h[:h.find("Learning Hindi from somewhere else")]
    for bad in ["aldives", "ALDIVES", "MVR", "08:30", "21:30", "<b>UTC+5</b>", "at UTC+5,",
                "from-mv\"", "§§NAME§§"]:
        assert bad not in core, "leftover %r in %s" % (bad, slug)
    assert 'geo.region" content="%s"' % cc in h
    assert "learn-hindi-from-%s/" % slug in h
    assert "world-languages/%s/" % slug in h
    assert cur in h and utc_label in h
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    ld = json.loads(m.group(1))
    types = [g.get("@type") for g in ld["@graph"]]
    assert types.count("Question") == 0  # questions nest inside FAQPage
    faq = [g for g in ld["@graph"] if g.get("@type") == "FAQPage"][0]
    assert len(faq["mainEntity"]) == 4
    assert faq["mainEntity"][2]["name"] == "How much does a Hindi lesson cost in %s?" % cur


def main():
    assert len(DATA) == 38
    tpl = open("learn-hindi-from-maldives/index.html", encoding="utf-8").read()
    names = names_by_slug()
    assert len(names) == 196, len(names)
    ordered = sorted(names)
    for entry in DATA:
        slug = entry[1]
        i = ordered.index(slug)
        sibs = [ordered[(i + k) % len(ordered)] for k in range(1, 13)]
        h = build_page(tpl, entry, sibs, names)
        qc(h, entry)
        d = "learn-hindi-from-%s" % slug
        os.makedirs(d, exist_ok=True)
        open(d + "/index.html", "w", encoding="utf-8").write(h)
    print("pages: 38 written")

    # --- index: ItemList 158 -> 196 ---
    ip = "learn-hindi-by-country/index.html"
    h = open(ip, encoding="utf-8").read()
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    ld = json.loads(m.group(1))
    for g in ld["@graph"]:
        if g.get("@type") == "ItemList":
            assert g["numberOfItems"] == 158, g["numberOfItems"]
            assert len(g["itemListElement"]) == 158
            pos = 159
            for cc, slug, name, *_ in sorted(DATA, key=lambda e: e[2]):
                g["itemListElement"].append({
                    "@type": "ListItem", "position": pos,
                    "name": "Learn Hindi from " + name,
                    "url": SITE + "/learn-hindi-from-%s/" % slug})
                pos += 1
            g["numberOfItems"] = 196
    h = h[:m.start(1)] + json.dumps(ld, ensure_ascii=False) + h[m.end(1):]

    # --- index: Long-tail chips ---
    tail = "\n".join('  <a href="../learn-hindi-from-%s/">%s</a>' % (slug, name)
                     for cc, slug, name, *_ in sorted(DATA, key=lambda e: e[2]))
    anchor = '  <a href="../learn-hindi-from-zimbabwe/">Zimbabwe</a>\n</div>'
    assert anchor in h
    h = h.replace(anchor, '  <a href="../learn-hindi-from-zimbabwe/">Zimbabwe</a>\n' + tail + "\n</div>", 1)

    # --- index: retire "Every other country" (plain string surgery — no regex) ---
    i2 = h.find("<h2>Every other country</h2>")
    assert i2 != -1, "every-other h2"
    k2 = h.find("</div>", i2)
    assert k2 != -1, "every-other close"
    end2 = k2 + len("</div>")
    if h[end2:end2 + 1] == "\n":
        end2 += 1
    h = h[:i2] + ('<h2>Every country, covered</h2>\n<p>Every sovereign country now has a page \u2014 each one written only when there was '
        'something specific and true to say, which is why these last 38 arrived after the rest. The rule still stands: '
        'a page earns its place with specifics, never with the country name swapped into a shared paragraph.</p>\n\n') + h[end2:]
    open(ip, "w", encoding="utf-8").write(h)
    print("index: 196 items, long-tail +38, every-other retired")

    # --- sitemap-countries: +38 ---
    sp = "sitemap-countries.xml"
    s = open(sp, encoding="utf-8").read()
    assert s.count("<loc>") == 159, s.count("<loc>")
    urls = "".join('  <url>\n    <loc>%s/learn-hindi-from-%s/</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n' % (SITE, slug, TODAY)
                   for cc, slug, name, *_ in sorted(DATA, key=lambda e: e[2]))
    assert "</urlset>" in s
    s = s.replace("</urlset>", urls + "</urlset>")
    open(sp, "w", encoding="utf-8").write(s)
    print("sitemap: +38 urls")


if __name__ == "__main__":
    main()
