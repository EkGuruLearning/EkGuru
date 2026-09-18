#!/usr/bin/env python3
"""EkGuru — ONE-COMMAND FULL REBUILD (v130).

    python3 tools/build-all.py

Runs the entire generation chain in dependency order; any failure
stops the run with a non-zero exit so a half-built site never
deploys:

  1  sheetsync (LIVE tutors/reviews/settings -> js/tutors/_overrides.js)
  2  world courses (every tools/course-data/*.py -> languages/<code>/…)
  3  Indian courses (9 lang-data slugs -> learn/<slug>/…)
  4  phase7 registries (source of truth for speech tags, countries)
  5  phase7c registries (PRODUCTION/AVAILABLE/BETA split)
  6  phase7c pages (hub, per-language pages, home sync)
  7  inventory (validate + build data/global + country language pages)
  8  search index
  9  storybook injector (Hindi pages get TTS + design)
 10  ads policy + consent boundary
 11  experience layer (css/experience.css -> style.min.css, world artwork,
     /courses/ + the home teaser)
 12  tutor layer (script tags, profile pages + sitemaps + feed, home cards,
     the six market pages, every other page that lists tutors)
 13  legal pages (terms/privacy/disclaimer/copyright get ids + a contents
     card), courses by country, the reading layer (969 hand-written pages onto
     one stylesheet, plus the support band and each page's next step), the page
     layer (the other 555 hand-written pages onto the same one), the A1–C2 level
     pages of every course, site shell
     (one header + one footer on all 1,564 pages), copy index (the check phase
     also runs the ownership, search-facet, drawer, course, reading and page
     layer tests)
 14  doctor (SEO + privacy + gate + admin stats)

The two layers in 11-12 are generated from the same data the pages are, so
they run last and cannot be overwritten by an injector. `python3
tools/build-all.py check` runs every generator's --check instead of writing,
and is what CI should call.

Steps 2-3 both feed data/courses.json + sitemap-courses.xml; steps
4-6 read those, so the order above is load-bearing — do not reorder.

Network: step 1 and step 8 (privacy --live) need internet. If the
sheet fetch fails the run stops: baking stale tutor data over a
fresh tree is worse than stopping.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

INDIAN_SLUGS = ["bengali", "gujarati", "kannada", "malayalam", "marathi",
                "punjabi", "tamil", "telugu", "urdu"]


def run(label, cmd):
    print("\n━━━ %s ━━━" % label, flush=True)
    print("$ " + " ".join(cmd), flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print("\n⛔ FAILED: %s (exit %d) — stopping, fix this first." % (label, r.returncode))
        sys.exit(r.returncode)
    print("✓ %s done." % label, flush=True)


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    if only and only[0] == "courses":
        run("world courses", ["python3", "tools/build-world-course.py"])
        for slug in INDIAN_SLUGS:
            run("Indian course: " + slug, ["python3", "tools/build-language-course.py", slug])
        return

    if only and only[0] == "check":
        run("experience bundle --check", ["python3", "tools/bundle-experience-css.py", "--check"])
        run("world artwork --check", ["python3", "tools/build-world-art.py", "--check"])
        run("course hub --check", ["python3", "tools/build-course-hub.py", "--check"])
        run("course levels --check (the A1-C2 pages of every course)",
            ["python3", "tools/build-course-levels.py", "--check"])
        run("tutor script tags --check", ["node", "tools/langsync.js", "--check"])
        run("tutor profiles --check", ["node", "tools/build-tutor-pages.js", "--check"])
        run("home tutor grid --check", ["node", "tools/build-home-tutors.js", "--check"])
        run("market pages --check", ["node", "tools/build-market-pages.js", "--check"])
        run("roster rows --check", ["node", "tools/build-roster-rows.js", "--check"])
        run("legal pages --check (terms, privacy, disclaimer, copyright)",
            ["python3", "tools/build-legal-pages.py", "--check"])
        run("courses by country --check", ["python3", "tools/build-course-countries.py", "--check"])
        run("reading layer --check (969 hand-written pages)", ["python3", "tools/build-legacy-pages.py", "--check"])
        run("page layer --check (555 lesson/answer/hub pages + 273 level pages)", ["python3", "tools/build-page-layer.py", "--check"])
        run("level visuals --check (a learner per language per rung)",
            ["python3", "tools/build-visuals.py", "--check"])
        run("country visuals --check (one plate per country)",
            ["python3", "tools/build-country-visuals.py", "--check"])
        run("level visuals test (the ladder, the figures, the strip)",
            ["node", "tools/test-level-visuals.mjs"])
        run("course levels test (every course readable at every level)",
            ["node", "tools/test-course-levels.mjs"])
        run("country visuals test (numbers match the data)",
            ["node", "tools/test-country-visuals.mjs"])
        run("offline playable test (the game plays with the network off)",
            ["node", "tools/test-offline-playable.mjs"])
        run("readiness audit selftest (the word counter, on unspaced scripts)",
            ["python3", "tools/audit-adsense-readiness.py", "--selftest"])
        run("ads readiness, repository mode (ads.txt, canonicals, sitemaps)",
            ["node", "tools/adsready.js", "--local"])
        run("print sheets --check (only the sheet prints)", ["python3", "tools/build-print-sheets.py", "--check"])
        run("site shell --check (header + footer on every page)", ["node", "tools/build-shell.js", "--check"])
        run("copy index --check", ["node", "tools/build-copy-index.js", "--check"])
        run("ownership test (matcher vs its own corpus)", ["node", "tools/test-copy-index.mjs"])
        run("search facet test (country + language)", ["node", "tools/test-search-facets.mjs"])
        run("header drawer test (one owner, one open)", ["node", "tools/test-shell-drawer.mjs"])
        run("course country search test", ["node", "tools/test-course-country.mjs"])
        run("reading layer test (one stylesheet, two bands)", ["node", "tools/test-reading-layer.mjs"])
        run("page layer test (one design on all 828 pages)", ["node", "tools/test-page-layer.mjs"])
        run("print sheet test (what lands on paper)", ["node", "tools/test-print-sheets.mjs"])
        run("print sheet dom test (the copy the script builds)",
            ["node", "tools/test-print-sheet-dom.mjs"])
        run("print visible test (what the printer receives)",
            ["node", "tools/test-print-visible.mjs"])
        run("ad policy --check (loader only where the matrix allows)",
            ["python3", "tools/inject-ads.py", "--check"])
        run("ad policy test (excluded pages carry no ad tag)",
            ["node", "tools/test-ad-policy.mjs"])
        run("questions api --check (votes on every question page)",
            ["python3", "tools/inject-questions-api.py", "--check"])
        run("questions api test (flag -> queue -> community)",
            ["node", "tools/test-question-api.mjs"])
        run("refresh test (a reload shows the deploy and starts nothing)",
            ["node", "tools/test-refresh-quiet.mjs"])
        run("page skeleton test (one main, skip link lands)", ["node", "tools/test-page-skeleton.mjs"])
        run("sheet-apply test (sheet row -> site)", ["node", "tools/test-sheet-apply.js"])
        run("experience DOM test", ["node", "tools/test-experience-dom.mjs"])
        print("\n✔ every generated layer is up to date.")
        return

    run("sheetsync (live sheet -> overrides)", ["node", "tools/sheetsync.js"])
    run("world courses (all)", ["python3", "tools/build-world-course.py"])
    for slug in INDIAN_SLUGS:
        run("Indian course: " + slug, ["python3", "tools/build-language-course.py", slug])
    run("phase7 registries", ["python3", "tools/build-phase7-registries.py"])
    run("phase7c registries", ["python3", "tools/build-phase7c-registries.py"])
    run("phase7c pages", ["python3", "tools/build-phase7-pages.py"])
    run("inventory validate", ["python3", "tools/validate-inventory.py"])
    run("inventory build", ["python3", "tools/build-inventory.py"])
    run("country language pages", ["python3", "tools/build-country-language-pages.py"])
    run("search index", ["python3", "tools/build-search-index.py"])
    run("experience bundle (css/experience.css -> style.min.css)", ["python3", "tools/bundle-experience-css.py"])
    run("world artwork (9 emblems)", ["python3", "tools/build-world-art.py"])
    run("course hub + home teaser", ["python3", "tools/build-course-hub.py"])
    run("course levels (A1-C2 pages, and the rail on every hub)",
        ["python3", "tools/build-course-levels.py"])
    run("storybook injector (Hindi TTS + design)", ["python3", "tools/inject-storybook.py"])
    run("ads policy (which pages may load the ad script)", ["python3", "tools/inject-ads.py"])
    run("consent injector (cookie notice)", ["python3", "tools/inject-consent.py"])
    run("tutor script tags (langsync)", ["node", "tools/langsync.js"])
    run("tutor profiles (page + sitemaps + feed)", ["node", "tools/build-tutor-pages.js"])
    run("home tutor grid", ["node", "tools/build-home-tutors.js"])
    run("market pages (6 locales)", ["node", "tools/build-market-pages.js"])
    run("roster rows (long-tail tutor lists)", ["node", "tools/build-roster-rows.js"])
    run("legal pages (contents card + clause ids)", ["python3", "tools/build-legal-pages.py"])
    run("courses by country (194 countries + the build queue)", ["python3", "tools/build-course-countries.py"])
    run("Hindi learning pages (learn/hindi/**)", ["python3", "tools/build-hindi-pages.py"])
    run("country visuals (one plate per country, on both country page sets)",
        ["python3", "tools/build-country-visuals.py"])
    run("reading layer (969 pages onto the design system)", ["python3", "tools/build-legacy-pages.py"])
    run("page layer (555 lesson/answer/hub + 273 level pages)", ["python3", "tools/build-page-layer.py"])
    run("level visuals (a learner per language per rung)", ["python3", "tools/build-visuals.py"])
    run("print sheets (worksheet prints as a sheet)", ["python3", "tools/build-print-sheets.py"])
    run("questions api (flags and likes reach other learners)",
        ["python3", "tools/inject-questions-api.py"])
    run("site shell (one header + one footer, every page)", ["node", "tools/build-shell.js"])
    run("copy index (ownership fingerprints)", ["node", "tools/build-copy-index.js"])
    run("doctor", ["node", "tools/doctor.js"])
    print("\n══════════════════════════════════════════")
    print("build-all complete — every step passed.")
    print("Review `git status`, then commit + deploy.")
    print("══════════════════════════════════════════")


if __name__ == "__main__":
    main()
