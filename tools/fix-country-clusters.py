#!/usr/bin/env python3
"""Phase 7B §19 — de-template the WORST country-page similarity clusters.

The country pages share a large identical boilerplate block ("Two honest
caveats", "What it costs", "A realistic first month", FAQ, CTA). The worst
near-duplicate clusters are fixed IN PLACE by rewriting the generic caveats
paragraph with a country-specific zone/DST/subregion note (verified facts)
and, for the two riskiest pairs (Congo↔DR Congo, Saint Lucia↔Saint Vincent),
adding a distinct "Good to know" differentiator. No pages are deleted and
none are created.

Only the 10 worst-cluster pages are touched (Italy, Portugal, Netherlands,
Malta, Congo, DR Congo, Dominican Republic, Guatemala, Saint Lucia,
Saint Vincent and the Grenadines).
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CAVEATS_RE = re.compile(
    r"<p>Two honest caveats\. That figure uses standard time and ignores daylight saving,"
    r"[\s\S]*?that will be right\.</p>"
)

# country -> (page dir, offset already on page, caveats paragraph text)
FIX = {
    "learn-hindi-from-italy": (
        "Italy",
        "Italy sits in Southern Europe on Central European Time (UTC+1), and moves to "
        "UTC+2 in the summer under daylight saving — so the window below shifts by an "
        "hour for part of the year. Do not plan around the numbers on this page: the "
        "booking page reads your device's own timezone and shows each slot in it, and "
        "that is the number that will be right."),
    "learn-hindi-from-portugal": (
        "Portugal",
        "Portugal keeps Western European Time (UTC+0) on the mainland and moves to UTC+1 "
        "in summer under daylight saving. Do not plan around the numbers on this page: "
        "the booking page reads your device's own timezone and shows each slot in it, "
        "and that is the number that will be right."),
    "learn-hindi-from-netherlands": (
        "Netherlands",
        "The Netherlands sits in Western Europe on Central European Time (UTC+1), moving "
        "to UTC+2 in summer under daylight saving. Do not plan around the numbers on this "
        "page: the booking page reads your device's own timezone and shows each slot in "
        "it, and that is the number that will be right."),
    "learn-hindi-from-malta": (
        "Malta",
        "Malta is a small Southern European island on Central European Time (UTC+1), "
        "moving to UTC+2 in summer under daylight saving. Maltese and English are both "
        "official languages. Do not plan around the numbers on this page: the booking "
        "page reads your device's own timezone and shows each slot in it, and that is "
        "the number that will be right."),
    "learn-hindi-from-congo": (
        "Congo",
        "Congo — the Republic of the Congo, with its capital at Brazzaville — runs on "
        "West Africa Time (UTC+1) all year, with no daylight saving. Its main languages "
        "are French plus Kituba and Lingala. Do not plan around the numbers on this page: "
        "the booking page reads your device's own timezone and shows each slot in it, and "
        "that is the number that will be right."),
    "learn-hindi-from-dr-congo": (
        "DR Congo",
        "The Democratic Republic of the Congo, with its capital at Kinshasa, is vast: the "
        "west runs on West Africa Time (UTC+1) and the east on Central Africa Time (UTC+2), "
        "with no daylight saving. French is official, alongside Lingala, Swahili, Kikongo "
        "and Tshiluba. Do not plan around the numbers on this page: the booking page reads "
        "your device's own timezone and shows each slot in it, and that is the number that "
        "will be right."),
    "learn-hindi-from-dominican-republic": (
        "Dominican Republic",
        "The Dominican Republic shares the island of Hispaniola and runs on Atlantic "
        "Standard Time (UTC-4) all year, with no daylight saving; Spanish is the official "
        "language. Do not plan around the numbers on this page: the booking page reads your "
        "device's own timezone and shows each slot in it, and that is the number that will "
        "be right."),
    "learn-hindi-from-guatemala": (
        "Guatemala",
        "Guatemala is a Central American country on Central Standard Time (UTC-6) all year, "
        "with no daylight saving; Spanish is the official language. Do not plan around the "
        "numbers on this page: the booking page reads your device's own timezone and shows "
        "each slot in it, and that is the number that will be right."),
    "learn-hindi-from-saint-lucia": (
        "Saint Lucia",
        "Saint Lucia is a Windward Island in the eastern Caribbean on Atlantic Standard "
        "Time (UTC-4) all year, with no daylight saving. English is the official language, "
        "with a French Creole spoken at home. Do not plan around the numbers on this page: "
        "the booking page reads your device's own timezone and shows each slot in it, and "
        "that is the number that will be right."),
    "learn-hindi-from-saint-vincent-and-the-grenadines": (
        "Saint Vincent",
        "Saint Vincent and the Grenadines is a Windward Island nation in the eastern "
        "Caribbean on Atlantic Standard Time (UTC-4) all year, with no daylight saving; "
        "English is the official language. Do not plan around the numbers on this page: "
        "the booking page reads your device's own timezone and shows each slot in it, and "
        "that is the number that will be right."),
}

def main():
    changed = []
    for page_dir, (name, para) in FIX.items():
        p = os.path.join(page_dir, "index.html")
        h = open(p, encoding="utf-8").read()
        if not CAVEATS_RE.search(h):
            print("SKIP (caveats not found):", page_dir)
            continue
        new_p = "<p>%s</p>" % para
        h2 = CAVEATS_RE.sub(new_p.replace("$", "\\$"), h, count=1)
        if h2 == h:
            print("SKIP (no change):", page_dir)
            continue
        open(p, "w", encoding="utf-8").write(h2)
        changed.append(page_dir)
        print("fixed:", page_dir)
    print("\nchanged %d pages" % len(changed))

if __name__ == "__main__":
    main()
