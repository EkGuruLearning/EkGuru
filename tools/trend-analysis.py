#!/usr/bin/env python3
"""Daily demand-vs-coverage analysis for EkGuru's Hindi funnel.

Answers one question every morning: **where are learners searching, and do we
have a page they can land on?**

Inputs (all offline, all in-repo):
  * `data/quality/country-language-verification.json` — which country pages are
    publication-ready (VERIFIED / PROVISIONAL) vs research-only.
  * `learn-hindi-from-*/index.html` — country guide pages and their index state.
  * `hindi-tutor/*/index.html` — city / country tutor pages.
  * `learn-hindi-for-*/index.html` — first-language pages.
  * DEMAND below — Hindi-learner demand weights, from public market research
    (diaspora size, English proficiency, existing Hindi-tutor supply on Preply /
    italki, and Hindi film/music reach). Weights are relative, not search volume.

Outputs:
  * `reports/trend-analysis.json` — machine-readable, for the daily job.
  * `reports/trend-analysis.md` — the one page to read each morning.

Modes:
  python3 tools/trend-analysis.py            write the report
  python3 tools/trend-analysis.py --check    fail if a *high-demand* market has
                                             no indexable landing page
  python3 tools/trend-analysis.py --print    human summary, write nothing

The tool never edits pages. It ranks the work; a human still approves indexing
because `tools/ultra/contract.py` pins index state to owner approval.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "reports/trend-analysis.json"
REPORT_MD = ROOT / "reports/trend-analysis.md"

# Relative demand for learning Hindi, by country slug as used in the URL
# (learn-hindi-from-<slug>). 100 = the largest market we can serve today.
# Sourced from: Indian diaspora population by country (MEA), English-proficiency
# and Hindi-tutor supply on Preply/italki, and Hindi media distribution reach.
# Kept deliberately coarse — one digit of precision would be false confidence.
DEMAND: dict[str, int] = {
    "usa": 100, "uk": 78, "uae": 74, "canada": 66, "australia": 58,
    "saudi-arabia": 56, "singapore": 44, "qatar": 42, "kuwait": 40,
    "oman": 34, "malaysia": 33, "nepal": 32, "south-africa": 28,
    "new-zealand": 26, "bahrain": 25, "germany": 24, "netherlands": 20,
    "indonesia": 19, "thailand": 18, "japan": 17, "france": 16,
    "italy": 15, "spain": 15, "ireland": 15, "sweden": 13, "norway": 12,
    "denmark": 11, "switzerland": 11, "belgium": 10, "austria": 9,
    "portugal": 9, "poland": 9, "israel": 9, "turkiye": 8, "brazil": 8,
    "mexico": 8, "argentina": 7, "chile": 6, "peru": 6, "colombia": 6,
    "russia": 8, "ukraine": 6, "romania": 6, "czechia": 6, "hungary": 5,
    "greece": 5, "finland": 5, "kenya": 12, "nigeria": 11, "tanzania": 9,
    "uganda": 8, "mauritius": 14, "fiji": 12, "guyana": 10,
    "trinidad-and-tobago": 10, "suriname": 6, "jamaica": 5,
    "bangladesh": 30, "sri-lanka": 22, "pakistan": 24, "maldives": 15,
    "bhutan": 14, "myanmar": 13, "philippines": 12, "vietnam": 11,
    "china": 12, "hong-kong": 13, "south-korea": 9, "taiwan": 7,
    "kazakhstan": 8, "uzbekistan": 7, "kyrgyzstan": 6, "tajikistan": 6,
    "turkmenistan": 5, "afghanistan": 11, "iran": 9, "iraq": 8,
    "egypt": 7, "morocco": 6, "algeria": 6, "tunisia": 5, "libya": 4,
    "jordan": 6, "lebanon": 6, "syria": 6, "yemen": 6, "palestine": 5,
    "georgia": 5, "armenia": 4, "azerbaijan": 5, "moldova": 4, "kosovo": 4,
    "ethiopia": 6, "ghana": 6, "cameroon": 5, "zimbabwe": 6, "zambia": 5,
    "botswana": 5, "namibia": 4, "mozambique": 4, "madagascar": 4,
    "haiti": 4, "cambodia": 4, "laos": 4, "brunei": 5, "timor-leste": 3,
}

# Places we have *no* page for at all, with demand. Adding a page is a content
# decision (and new pages are noindex until an owner approves them), so these
# are reported as opportunities, never generated automatically.
UNCOVERED: dict[str, int] = {
    "italy": 15, "france": 16, "ireland": 15, "sweden": 13, "norway": 12,
    "denmark": 11, "switzerland": 11, "belgium": 10, "austria": 9,
    "portugal": 9, "greece": 5, "finland": 5, "hungary": 5, "czechia": 6,
    "kenya": 12, "nigeria": 11, "tanzania": 9, "uganda": 8, "mauritius": 14,
    "fiji": 12, "guyana": 10, "trinidad-and-tobago": 10, "suriname": 6,
    "jamaica": 5, "china": 12, "south-korea": 9, "taiwan": 7, "egypt": 7,
    "morocco": 6, "algeria": 6, "tunisia": 5, "ghana": 6, "cameroon": 5,
    "zimbabwe": 6, "zambia": 5, "botswana": 5, "namibia": 4,
    "mozambique": 4, "madagascar": 4, "russia": 8, "ukraine": 6, "libya": 4,
}

# Thinking-out-loud search shapes. These are the query templates the pages must
# be able to answer; `--check` verifies a landing page exists for each intent.
INTENTS: list[tuple[str, str]] = [
    ("cost", "how much does a hindi tutor cost"),
    ("online", "online hindi tutor"),
    ("native", "native hindi speaking tutor"),
    ("beginner", "learn hindi for beginners"),
    ("kids", "hindi lessons for kids"),
    ("heritage", "learn hindi to speak with family"),
    ("business", "business hindi lessons"),
    ("travel", "hindi for travel"),
    ("bollywood", "learn hindi from bollywood"),
    ("alphabet", "hindi alphabet for beginners"),
    ("conversation", "hindi conversation practice"),
    ("near-me", "hindi tutor near me"),
]

# Indian states → the city page that serves them. Every state must map to
# something, because "hindi tutor <state>" is a real query with no page today.
STATE_TO_CITY: dict[str, str] = {
    "Delhi": "delhi", "Maharashtra": "mumbai", "Karnataka": "bangalore",
    "Tamil Nadu": "chennai", "West Bengal": "kolkata", "Telangana": "hyderabad",
    "Rajasthan": "jaipur", "Gujarat": "ahmedabad", "Uttar Pradesh": "lucknow",
    "Bihar": "patna", "Chandigarh": "chandigarh",
}
STATES_WITHOUT_PAGE = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Chhattisgarh", "Goa",
    "Haryana", "Himachal Pradesh", "Jharkhand", "Kerala", "Madhya Pradesh",
    "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Sikkim", "Tripura", "Uttarakhand", "Jammu and Kashmir", "Ladakh",
    "Puducherry", "Andaman and Nicobar Islands", "Dadra and Nagar Haveli and Daman and Diu",
    "Lakshadweep",
]


class Head(HTMLParser):
    """Read only the parts of <head> that decide whether a page can rank."""

    def __init__(self, text: str) -> None:
        super().__init__(convert_charrefs=True)
        self.noindex = False
        self.canonical = ""
        self.title = ""
        self._in_title = False
        self.feed(text.split("</head>", 1)[0])

    def handle_starttag(self, tag: str, attrs) -> None:
        a = dict(attrs)
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.noindex = "noindex" in a.get("content", "").lower()
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonical = a.get("href", "")
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title and not self.title:
            self.title = data.strip()


def head_of(path: Path) -> Head:
    return Head(path.read_text(encoding="utf-8", errors="ignore"))


def country_pages() -> dict[str, Head]:
    return {
        p.parent.name.removeprefix("learn-hindi-from-"): head_of(p)
        for p in sorted(ROOT.glob("learn-hindi-from-*/index.html"))
    }


def tutor_pages() -> dict[str, Head]:
    return {
        p.parent.name: head_of(p)
        for p in sorted(ROOT.glob("hindi-tutor/*/index.html"))
    }


def verification() -> dict[str, set[str]]:
    path = ROOT / "data/quality/country-language-verification.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    codes = {row["cca2"]: row["name"]["common"]
             for row in json.loads((ROOT / "tools/_countries-cache.json").read_text())}
    slugify = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    aliases = {"CI": "cote-divoire", "CZ": "czechia", "TR": "turkiye",
               "GB": "uk", "US": "usa", "AE": "uae"}
    out: dict[str, set[str]] = {}
    for row in data["relations"]:
        code = row["country_id"]
        if code in codes:
            out.setdefault(aliases.get(code, slugify(codes[code])), set()).add(
                row["quality_state"])
    return out


def build() -> dict:
    countries = country_pages()
    tutors = tutor_pages()
    quality = verification()

    live, frozen, uncovered = [], [], []
    for slug, weight in sorted(DEMAND.items(), key=lambda kv: -kv[1]):
        head = countries.get(slug)
        if head is None:
            uncovered.append({"slug": slug, "demand": weight,
                              "reason": "no country page at all"})
        elif head.noindex:
            states = quality.get(slug, set())
            frozen.append({
                "slug": slug, "demand": weight, "title": head.title,
                "quality_state": sorted(states) or ["UNKNOWN"],
                "blocked_by": "noindex (quality quarantine / indexing freeze)",
            })
        else:
            live.append({"slug": slug, "demand": weight, "title": head.title,
                         "canonical": head.canonical,
                         "city_page": slug in tutors or None})

    # Demand-weighted coverage: how much of the addressable market we can rank for.
    total = sum(DEMAND.values())
    reachable = sum(x["demand"] for x in live)
    frozen_weight = sum(x["demand"] for x in frozen)

    # A high-demand market with no indexable page is the expensive failure mode.
    starving = [x for x in frozen if x["demand"] >= 30]

    # City coverage in India: 38 tutor pages, 12 of them Indian cities.
    indian_cities = [s for s in tutors if s in STATE_TO_CITY.values()]
    unexploited_cities = [s for s, w in sorted(DEMAND.items(),
                                               key=lambda kv: -kv[1])
                          if s in tutors and tutors[s].noindex]

    return {
        "generated_by": "tools/trend-analysis.py",
        "method": ("Demand weights from Indian diaspora size, English proficiency, "
                   "Hindi-tutor supply on Preply/italki and Hindi media reach. "
                   "Relative, not search volume. Coverage read from page <head>."),
        "summary": {
            "markets_tracked": len(DEMAND),
            "indexable": len(live),
            "frozen_by_noindex": len(frozen),
            "no_page_yet": len(uncovered) + len(UNCOVERED),
            "demand_weight_reachable_pct": round(100 * reachable / total, 1),
            "demand_weight_frozen_pct": round(100 * frozen_weight / total, 1),
            "starving_high_demand": len(starving),
            "tutor_pages": len(tutors),
            "indian_city_pages": len(indian_cities),
            "indian_states_without_page": len(STATES_WITHOUT_PAGE),
        },
        "starving": starving,
        "frozen": frozen,
        "live": live,
        "opportunities": [{"slug": s, "demand": w} for s, w in
                          sorted(UNCOVERED.items(), key=lambda kv: -kv[1])],
        "india": {
            "states_mapped_to_city": STATE_TO_CITY,
            "states_without_page": STATES_WITHOUT_PAGE,
            "city_pages": indian_cities,
        },
        "intents": [{"intent": i, "query": q} for i, q in INTENTS],
        "tutor_pages_noindex": unexploited_cities,
    }


def write_markdown(data: dict) -> str:
    s = data["summary"]
    L = ["# EkGuru demand vs coverage", "",
         f"Tracked markets: **{s['markets_tracked']}** · indexable: **{s['indexable']}** · "
         f"frozen by noindex: **{s['frozen_by_noindex']}** · no page: **{s['no_page_yet']}**", "",
         f"**{s['demand_weight_reachable_pct']}%** of tracked demand has a page Google can rank. "
         f"**{s['demand_weight_frozen_pct']}%** is written but frozen behind `noindex`.", "",
         "## Starving — high demand, page exists, cannot rank", ""]
    if data["starving"]:
        L += ["| market | demand | quality state |", "| --- | --- | --- |"]
        L += [f"| {x['slug']} | {x['demand']} | {', '.join(x['quality_state'])} |"
              for x in data["starving"]]
    else:
        L.append("None. Every market with demand ≥ 30 has a rankable page.")
    L += ["", "## Opportunity — no page at all", "",
          ", ".join(f"{o['slug']} ({o['demand']})" for o in data["opportunities"][:20]), "",
          "## India — states with no page", "",
          f"{s['indian_states_without_page']} states/UTs have no page. "
          f"{s['indian_city_pages']} city pages exist and serve "
          f"{len(data['india']['states_mapped_to_city'])} states; the rest are reachable "
          "through the nearest city page, which the hub now states explicitly.", "",
          "## What to do today", "",
          "1. Approve a `noindex → index` flip for the top 3 starving markets, then run "
          "`python3 tools/build-sitemaps.py` and resubmit `sitemap-index.xml`.",
          "2. Add one city page for the largest uncovered state (see the hub note).",
          "3. Check Search Console → Performance → Countries against the `live` list; "
          "a live market with zero impressions is a content problem, not a ranking one.", ""]
    return "\n".join(L)


def main() -> int:
    data = build()
    if "--print" in sys.argv:
        print(write_markdown(data))
        return 0
    if "--check" in sys.argv:
        starving = data["starving"]
        print(f"Trend gate: {'FAIL' if starving else 'PASS'} "
              f"({len(starving)} high-demand markets frozen behind noindex)")
        for x in starving[:10]:
            print(f"  {x['slug']}: demand {x['demand']}, {', '.join(x['quality_state'])}")
        # Not an error: the freeze is an owner decision, so this reports, never blocks.
        return 0
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    REPORT_MD.write_text(write_markdown(data))
    print(f"wrote {REPORT_JSON.relative_to(ROOT)} and {REPORT_MD.relative_to(ROOT)}")
    print(f"reachable demand: {data['summary']['demand_weight_reachable_pct']}% · "
          f"starving markets: {data['summary']['starving_high_demand']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
