#!/usr/bin/env python3
"""EkGuru — ONE-COMMAND FULL REBUILD (v130).

    python3 tools/build-all.py

Runs the entire generation chain in dependency order; any failure
stops the run with a non-zero exit so a half-built site never
deploys:

  1  sheetsync (LIVE tutors/reviews/settings -> js/tutors/_overrides.js)
  2  world courses (every tools/course-data/*.py -> languages/<code>/…)
  3  Indian courses (9 lang-data slugs -> learn/<slug>/…)
  3a root Indian topic trees (nine /<language>/<topic>/ trees)
  3b language-aware speaker controls for generated course and topic text
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


# ULTRA v3 generators/tests. Each slice appends here so check and write modes stay in step.
ULTRA_BUILDS = [
    ("owner-approved country phrase consolidation", ["python3", "tools/build-country-phrases.py"]),
    ("reciprocal language alternates on existing beginner guides", ["python3", "tools/build-guide-hreflang.py"]),
    ("flashcard decks from authored course vocabulary (PHASE 9)", ["python3", "tools/build-flashcards.py"]),
    ("flashcard lab on every practice page with a deck (PHASE 9)", ["python3", "tools/inject-flashcards.py"]),
    ("Hindi Academy curated paths", ["python3", "tools/build-hindi-academy.py"]),
    ("Hindi first-letters-to-reading collection on the existing practice hub", ["python3", "tools/build-hindi-learning-library.py"]),
    ("Hindi textbook contents on existing Foundation lessons", ["python3", "tools/build-hindi-textbook-reader.py"]),
    ("Student account pages", ["python3", "tools/build-student-pages.py"]),
    ("Pinned Firebase browser SDK", ["node", "tools/build-student-sdk.mjs"]),
    ("Authored depth on existing Hindi Foundation chapters", ["python3", "tools/build-hindi-foundation-depth.py"]),
    ("Existing Hindi phrase answers linked from their question/course hubs", ["python3", "tools/build-hindi-phrase-discovery.py"]),
    ("Contextual entry links for existing class and script guides", ["python3", "tools/build-contextual-entry-links.py"]),
    ("700-language draft registry + 197 country contexts", ["python3", "tools/build-language-registry.py"]),
    ("per-language AA themes (script font, direction, accent)", ["python3", "tools/build-themes.py"]),
    ("voice language tags + recording manifests (owner-supplied only)", ["python3", "tools/build-voice-languages.py"]),
    ("bounded learning plans, placement banks and offline level lists", ["python3", "tools/build-learning-data.py"]),
    ("trust, journal, review and design pages (all noindex)", ["python3", "tools/build-ultra-pages.py"]),
    ("language quality gate report (failures reported, never hidden; no page edited)", ["python3", "tools/language-gate.py"]),
    ("course health report", ["python3", "tools/course-health.py"]),
    ("Phase 1: complete authored depth and no open mechanical gaps", ["python3", "tools/audit-phase1-gap.py", "--check"]),
    ("Phase 1: contextual glosses for advanced phrase lessons", ["python3", "tools/repair-phase1-advanced-glosses.py", "--check"]),
    ("world-language long-form Learn content (Phase 3)", ["python3", "tools/build-world-phase3.py"]),
    ("flashcard decks + lab: sizes, ids, keyboard, SRS (PHASE 9)",
     ["node", "tests/regression/test-flashcards.mjs"]),
]
ULTRA_TESTS = [
    ("analytics privacy choices remain reversible across provider load races", ["node", "tests/regression/test-analytics-lifecycle.mjs"]),
    ("join wizard loads its real stylesheet and keeps navigation visible", ["node", "tests/regression/test-join-css-visibility.mjs"]),
    ("home Hindi practice checks the displayed phrase locally", ["node", "tests/regression/test-home-practice.mjs"]),
    ("country phrase consolidation stays bounded, crawlable and ad-free", ["python3", "tests/regression/test-country-phrase-consolidation.py"]),
    ("sitemap rebuilds never fabricate editorial freshness", ["python3", "tests/unit/test-sitemap-freshness.py"]),
    ("public crawl targets, assets and reciprocal hreflang", ["python3", "tools/discovery_integrity.py"]),
    ("discovery audit and relocation regression tests", ["python3", "tests/unit/test-discovery-integrity.py"]),
    ("static landing metadata survives legacy SEO runtime", ["node", "tests/regression/test-seo-runtime.mjs"]),
    ("Hindi sentence pilot: accessible practice and preserved learning contracts", ["node", "tests/regression/test-hindi-sentence-lesson.mjs"]),
    ("Hindi Academy paths and vowel companion", ["node", "tests/regression/test-hindi-academy.mjs"]),
    ("Hindi primary hub: preserved anchors and links", ["python3", "tests/regression/test-hindi-textbook-hub.py"]),
    ("Hindi textbook graph and character coverage", ["python3", "tests/unit/test-hindi-textbook-model.py"]),
    ("Hindi textbook navigation and existing lesson preservation", ["python3", "tests/regression/test-hindi-textbook-reader.py"]),
    ("Academy manifest extensibility and isolated publication fixture", ["python3", "tests/unit/test-academy-registry.py"]),
    ("Hindi learning collection: distinct sources, reading, voice and shared review", ["node", "tests/regression/test-hindi-learning-library.mjs"]),
    ("Hindi Foundation illustrations, source parity and airflow", ["python3", "tests/regression/test-hindi-foundation-illustrations.py"]),
    ("Hindi Foundation depth: authored counts, preserved SEO and legacy generator", ["python3", "tests/regression/test-hindi-foundation-depth.py"]),
    ("Hindi phrase answers: contextual inlinks and preserved publication contracts", ["python3", "tests/regression/test-hindi-phrase-discovery.py"]),
    ("Contextual entry links preserve page metadata and existing forms", ["python3", "tests/regression/test-contextual-entry-links.py"]),
    ("AdSense publisher script, verification meta and root seller identity", ["python3", "tests/regression/test-adsense-publisher-tags.py"]),
    ("Advertising launch stays blocked without account and consent evidence", ["node", "tests/regression/test-advertising-launch.mjs"]),
    ("Privacy preferences persist without renewing consent or removing withdrawal", ["node", "tests/regression/test-consent-persistence.mjs"]),
    ("Published artifact must contain the exact root ads.txt seller record", ["python3", "tests/unit/test-public-ads-txt.py"]),
    ("Student routes, sitemap, ad and SVG safety", ["python3", "tests/regression/test-lms-routes.py"]),
    ("Student contract client", ["node", "--test", "tests/student-api.test.mjs"]),
    ("Firebase web-key exception and rejection controls", ["node", "tests/unit/test-public-secret-scan.cjs"]),
    ("Attribution scanner public/private scope", ["node", "tests/unit/test-attribution-walk.js"]),
    ("Uploaded development packs stay out of the published artifact", ["python3", "tests/unit/test-public-upload-pack.py"]),
    ("Repository layout: retained tests, commands and private-folder sentinels", ["python3", "tests/unit/test-repository-layout.py"]),
    ("Phase 2 public-page inventory is current (repository-only)",
     ["python3", "tools/build-full-page-inventory.py", "--check"]),
    ("Phase 2 detailed content inventory is current (live HTTP pending)",
     ["python3", "tools/build-phase2-content-inventory.py", "--check"]),
    ("Phase 2 inventory fields, safety and scope", ["python3", "tests/regression/test-phase2-content-inventory.py"]),
    ("Hindi hunger answer: source-backed restaurant phrase and Hindi next-step routing", ["python3", "tests/regression/test-hindi-hunger-answer-content.py"]),
    ("Phase 5 original-value Hindi numbers practice (repository consistency)", ["python3", "tests/regression/test-phase5-ekguru-value.py"]),
    ("Phase 6 Hindi text counter rules, UI events and page contract", ["node", "tests/regression/test-hindi-text-counter.mjs"]),
    ("Phase 7 answer-first Q&A placement (structural check only)", ["python3", "tests/regression/test-answer-first-pages.py"]),
    ("Phase 3 repository-backed originality audit is current (human review pending)",
     ["python3", "tools/build-phase3-originality-audit.py", "--check"]),
    ("Phase 3 audit fields and non-fabrication safety", ["python3", "tests/regression/test-phase3-originality-audit.py"]),
    ("world-course quiz bank bindings, topic maps and visible copy", ["python3", "tests/regression/test-world-course-quiz-content.py"]),
    ("Spanish/French numbers lessons: complete source-matched 1–20 tables", ["python3", "tests/regression/test-world-course-numbers-content.py"]),
    ("Daily Hindi Day 23 future examples and task (repository consistency only)", ["python3", "tests/regression/test-daily-hindi-future-content.py"]),
    ("published vocabulary excludes generated segmentation placeholders", ["python3", "tests/regression/test-published-vocabulary.py"]),
    ("partial Phase 1 courses mark C1/C2 unpublished", ["python3", "tests/regression/test-partial-course-publication.py"]),
    ("rendered Phase 2 root Indian topic parity", ["python3", "tools/audit-indian-topic-parity.py", "--check"]),
    ("Indian beginner leads use their authored language data", ["python3", "tests/regression/test-language-course-uniqueness.py"]),
    ("Phase 3 long-form Learn posts (130 guides across Indian tracks + Hindi, Spanish, Arabic and German)", ["python3", "tests/regression/test-phase3-content.py"]),
    ("immutable owner indexing/canonical contract", ["python3", "tools/ultra/contract.py"]),
    ("own-content dates are current (never a rebuild timestamp)", ["python3", "tools/update-editorial-metadata.py", "--check"]),
    ("site features on every page are current (additive, strip-invertible)", ["python3", "tools/apply-ultra.py", "--check"]),
    ("site features: markers, order, robots/canonical untouched, honest bylines, no ad on interactive pages", ["python3", "tests/regression/test-ultra-integration.py"]),
    ("theme semantic AA contrast + motion budgets", ["node", "tests/regression/test-theme-contrast.mjs"]),
    ("shared runtime freshness (voice.js is built from src/runtime)", ["node", "tools/build-runtime.mjs", "--check"]),
    ("voice: exact-language voices, no autoplay, honest fallback, licensed recordings, mic transcript", ["node", "tests/regression/test-voice.mjs"]),
    ("mounted voice controls: language, labels, pressed state and fallback (mocked runtime)", ["node", "tests/regression/test-voice-mounted-controls.mjs"]),
    ("page-wide native voice controls and no nested interactive links", ["python3", "tests/regression/test-voice-page-coverage.py"]),
    ("voice speed/replay controls: availability, state and accessible labels", ["node", "tests/regression/test-voice-ux.mjs"]),
    ("Indian course/topic controls and visible target-script coverage", ["python3", "tests/regression/test-language-course-voice-controls.py"]),
    ("device journal, SRS scheduling, streak/freeze, backup, privacy", ["node", "tests/regression/test-retention.mjs"]),
    ("legacy migration, corrupt/future storage, quota and calendar regressions", ["node", "tests/regression/test-learning-storage.mjs"]),
    ("offline worker: private routes, aggregate quota, rollback, concurrency", ["node", "tests/regression/test-learning-worker.mjs"]),
    ("SEO, AEO & GEO discovery surfaces (OpenSearch, robots, llms-full, JSON-LD, Speculation Rules)", ["python3", "tools/build-seo-aeo-geo.py", "--check"]),
]


def ultra_builds(check):
    for label, cmd in ULTRA_BUILDS:
        run(label + (" --check" if check else ""), cmd + (["--check"] if check else []))


def ultra_tests():
    for label, cmd in ULTRA_TESTS:
        run(label, cmd)


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    if only and only[0] == "courses":
        run("world courses", ["python3", "tools/build-world-course.py"])
        for slug in INDIAN_SLUGS:
            run("Indian course: " + slug, ["python3", "tools/build-language-course.py", slug])
        return

    if only and only[0] == "check":
        ultra_builds(True)
        # Legacy generators compare their own output with the file, so they are checked against the
        # undecorated pages; the decoration is restored afterwards and verified separately below.
        run("strip ultra decoration for the legacy checks", ["python3", "tools/apply-ultra.py", "--strip"])
        try:
            run("root Indian topic trees --check (generator fingerprints)",
                ["python3", "tools/build-lang-topics.py", "--check"])
            run("Indian course/topic speaker controls --check",
                ["python3", "tools/patch-language-voice-controls.py", "--check"])
            run("experience bundle --check", ["python3", "tools/bundle-experience-css.py", "--check"])
            run("dark-mode safety net --check", ["python3", "tools/build-dark-fix.py", "--check"])
            run("world artwork --check", ["python3", "tools/build-world-art.py", "--check"])
            run("course hub --check", ["python3", "tools/build-course-hub.py", "--check"])
            run("course levels --check (the A1-C2 pages of every course)",
                ["python3", "tools/build-course-levels.py", "--check"])
            run("published language/level OG PNGs --check (resvg, 1200x630)",
                ["python3", "tools/build-og-images.py", "--check"])
            run("course IPA/source coverage report --check",
                ["python3", "tools/audit-course-pronunciation.py", "--check"])
            run("course romanisation --check (one scheme per course file)",
                ["python3", "tools/normalise-romanisation.py"])
            run("tutor script tags --check", ["node", "tools/langsync.js", "--check"])
            run("tutor profiles --check", ["node", "tools/build-tutor-pages.js", "--check"])
            run("home tutor grid --check", ["node", "tools/build-home-tutors.js", "--check"])
            run("market pages --check", ["node", "tools/build-market-pages.js", "--check"])
            run("roster rows --check", ["node", "tools/build-roster-rows.js", "--check"])
            run("legal pages --check (terms, privacy, disclaimer, copyright)",
                ["python3", "tools/build-legal-pages.py", "--check"])
            run("research quarantine --check", ["python3", "tools/quarantine-country-funnels.py", "--check"])
            run("draft tutor quarantine --check", ["python3", "tools/quarantine-tutor-drafts.py", "--check"])
            run("the one Hindi hub --check (/learn/hindi/ lists every real Hindi page)", ["python3", "tools/build-hindi-hub.py", "--check"])
            run("the learn index --check (/learn/ lists every language)", ["python3", "tools/build-learn-index.py", "--check"])
            run("language publication quarantine --check", ["python3", "tools/quarantine-language-surfaces.py", "--check"])
            run("courses by country --check", ["python3", "tools/build-course-countries.py", "--check"])
            run("sitemap publication gate --check", ["python3", "tools/build-sitemaps.py", "--check"])
            run("reading layer --check (969 hand-written pages)", ["python3", "tools/build-legacy-pages.py", "--check"])
            run("page layer --check (555 lesson/answer/hub pages + 273 level pages)", ["python3", "tools/build-page-layer.py", "--check"])
            run("level visuals --check (a learner per language per rung)",
                ["python3", "tools/build-visuals.py", "--check"])
            run("country visuals --check (one plate per country)",
                ["python3", "tools/build-country-visuals.py", "--check"])
            run("toolbox visuals --check (one plate per tool)",
                ["python3", "tools/build-toolbox-visuals.py", "--check"])
            run("level visuals test (the ladder, the figures, the strip)",
                ["node", "tests/regression/test-level-visuals.mjs"])
            run("course levels test (every course readable at every level)",
                ["node", "tests/regression/test-course-levels.mjs"])
            run("course voice controls + optional IPA renderer test",
                ["python3", "tests/regression/test-course-voice-buttons.py"])
            run("country visuals test (numbers match the data)",
                ["node", "tests/regression/test-country-visuals.mjs"])
            run("toolbox visuals test (the plates cannot lie about the pages)",
                ["node", "tests/regression/test-toolbox-visuals.mjs"])
            run("offline playable test (the game plays with the network off)",
                ["node", "tests/regression/test-offline-playable.mjs"])
            run("readiness audit selftest (the word counter, on unspaced scripts)",
                ["python3", "tools/audit-adsense-readiness.py", "--selftest"])
            run("ads readiness, repository mode (ads.txt, canonicals, sitemaps)",
                ["node", "tools/adsready.js", "--local"])
            run("print sheets --check (only the sheet prints)", ["python3", "tools/build-print-sheets.py", "--check"])
            run("site shell --check (header + footer on every page)", ["node", "tools/build-shell.js", "--check"])
            run("country specifics --check (P3 de-templated country pages)", ["python3", "tools/apply-country-specifics.py", "--check"])
            run("country SEO copy --check (titles, descriptions, roster honesty)", ["python3", "tools/apply-country-seo.py", "--check"])
            run("tutor location specifics --check (P3 location pages + FAQ markup parity)", ["python3", "tools/apply-tutor-location-specifics.py", "--check"])
            run("copy index --check", ["node", "tools/build-copy-index.js", "--check"])
            run("search publication check", ["python3", "tools/check-search-index.py"])
            run("ownership test (matcher vs its own corpus)", ["node", "tests/regression/test-copy-index.mjs"])
            run("search facet test (country + language)", ["node", "tests/regression/test-search-facets.mjs"])
            run("header drawer test (one owner, one open)", ["node", "tests/regression/test-shell-drawer.mjs"])
            run("course country search test", ["node", "tests/regression/test-course-country.mjs"])
            run("reading layer test (one stylesheet, two bands)", ["node", "tests/regression/test-reading-layer.mjs"])
            run("page layer test (one design on all 828 pages)", ["node", "tests/regression/test-page-layer.mjs"])
            run("book mode test (stepped Hindi lessons + generated practice)", ["node", "tests/regression/test-book-mode.mjs"])
            run("print sheet test (what lands on paper)", ["node", "tests/regression/test-print-sheets.mjs"])
            run("print sheet dom test (the copy the script builds)",
                ["node", "tests/regression/test-print-sheet-dom.mjs"])
            run("print visible test (what the printer receives)",
                ["node", "tests/regression/test-print-visible.mjs"])
            run("ad policy --check (loader only where the matrix allows)",
                ["python3", "tools/inject-ads.py", "--check"])
            run("ad policy test (excluded pages carry no ad tag)",
                ["node", "tests/regression/test-ad-policy.mjs"])
            run("questions api --check (votes on every question page)",
                ["python3", "tools/inject-questions-api.py", "--check"])
            run("duplicate external scripts --check", ["python3", "tools/dedupe-script-tags.py", "--check"])
            run("questions api test (flag -> queue -> community)",
                ["node", "tests/regression/test-question-api.mjs"])
            run("refresh test (a reload shows the deploy and starts nothing)",
                ["node", "tests/regression/test-refresh-quiet.mjs"])
            run("page skeleton test (one main, skip link lands)", ["node", "tests/regression/test-page-skeleton.mjs"])
            run("sheet-apply test (sheet row -> site)", ["node", "tests/integration/test-sheet-apply.js"])
            run("live-feed test (apps script feed, loaders, privacy)", ["node", "tests/integration/test-live-feed.js"])
            run("public surface gate (deploy set = website only; no contact data, no secrets)",
                ["node", "tests/regression/test-public-surface.mjs"])
            run("intake test (online forms: pending-only, honeypot, caps)", ["node", "tests/integration/test-intake.js"])
            run("sheetsync policy test (build side refuses marketplace values)",
                ["node", "tests/integration/test-sheetsync-policy.js"])
            run("sheet-only guru bake test (approved=yes rows bake, private cells never)",
                ["node", "tests/integration/test-sheet-only-bake.mjs"])
            run("orphan tutor page quarantine (a sheet-only guru set active=no loses the public page)",
                ["node", "tests/regression/test-orphan-tutor-quarantine.mjs"])
            run("no-competitor-attribution gate (public output + rendered strings)",
                ["node", "tests/regression/test-no-competitor-attribution.js"])
            run("experience DOM test", ["node", "tests/regression/test-experience-dom.mjs"])
        finally:
            subprocess.run(["python3", "tools/apply-ultra.py"], check=False)
        ultra_tests()
        print("\n✔ generated layers are current. This is NOT a native-review, publication, AdSense or release-readiness claim.")
        return

    run("sheetsync (live sheet -> overrides)", ["node", "tools/sheetsync.js"])
    run("world courses (all)", ["python3", "tools/build-world-course.py"])
    for slug in INDIAN_SLUGS:
        run("Indian course: " + slug, ["python3", "tools/build-language-course.py", slug])
    run("root Indian topic trees (nine languages)", ["python3", "tools/build-lang-topics.py"])
    run("Indian course/topic speaker controls (preserve authored wording)",
        ["python3", "tools/patch-language-voice-controls.py"])
    run("phase7 registries", ["python3", "tools/build-phase7-registries.py"])
    run("phase7c registries", ["python3", "tools/build-phase7c-registries.py"])
    run("phase7c pages", ["python3", "tools/build-phase7-pages.py"])
    run("inventory validate", ["python3", "tools/validate-inventory.py"])
    run("inventory build", ["python3", "tools/build-inventory.py"])
    run("country language pages", ["python3", "tools/build-country-language-pages.py"])
    ultra_builds(False)
    run("experience bundle (css/experience.css -> style.min.css)", ["python3", "tools/bundle-experience-css.py"])
    run("dark-mode safety net (hard-coded light boxes -> theme tokens)", ["python3", "tools/build-dark-fix.py"])
    run("world artwork (9 emblems)", ["python3", "tools/build-world-art.py"])
    run("course hub + home teaser", ["python3", "tools/build-course-hub.py"])
    run("course levels (A1-C2 pages, and the rail on every hub)",
        ["python3", "tools/build-course-levels.py"])
    run("OG cards for published language-level pages (SVG to PNG via resvg)",
        ["python3", "tools/build-og-images.py"])
    run("course pronunciation coverage audit (source data only; may remain blocked)",
        ["python3", "tools/audit-course-pronunciation.py"])
    run("storybook injector (Hindi TTS + design)", ["python3", "tools/inject-storybook.py"])
    run("speaker markup for injected language chapter banners",
        ["python3", "tools/patch-language-voice-controls.py"])
    run("ads policy (which pages may load the ad script)", ["python3", "tools/inject-ads.py"])
    run("consent injector (cookie notice)", ["python3", "tools/inject-consent.py"])
    run("tutor script tags (langsync)", ["node", "tools/langsync.js"])
    run("tutor profiles (page + sitemaps + feed)", ["node", "tools/build-tutor-pages.js"])
    run("home tutor grid", ["node", "tools/build-home-tutors.js"])
    run("market pages (6 locales)", ["node", "tools/build-market-pages.js"])
    run("roster rows (long-tail tutor lists)", ["node", "tools/build-roster-rows.js"])
    run("legal pages (contents card + clause ids)", ["python3", "tools/build-legal-pages.py"])
    run("research quarantine", ["python3", "tools/quarantine-country-funnels.py"])
    run("draft tutor quarantine", ["python3", "tools/quarantine-tutor-drafts.py"])
    run("language publication quarantine", ["python3", "tools/quarantine-language-surfaces.py"])
    run("courses by country (published + sourced)", ["python3", "tools/build-course-countries.py"])
    run("Hindi learning pages (learn/hindi/**)", ["python3", "tools/build-hindi-pages.py"])
    run("the one Hindi hub (/learn/hindi/ — every Hindi page from one door)", ["python3", "tools/build-hindi-hub.py"])
    run("the learn index (/learn/ — every language from one page)", ["python3", "tools/build-learn-index.py"])
    run("country visuals (one plate per country, on both country page sets)",
        ["python3", "tools/build-country-visuals.py"])
    run("toolbox visuals (one plate per tool, from the tool's own data)",
        ["python3", "tools/build-toolbox-visuals.py"])
    run("reading layer (969 pages onto the design system)", ["python3", "tools/build-legacy-pages.py"])
    run("page layer (555 lesson/answer/hub + 273 level pages)", ["python3", "tools/build-page-layer.py"])
    run("level visuals (a learner per language per rung)", ["python3", "tools/build-visuals.py"])
    run("print sheets (worksheet prints as a sheet)", ["python3", "tools/build-print-sheets.py"])
    run("questions api (flags and likes reach other learners)",
        ["python3", "tools/inject-questions-api.py"])
    run("duplicate external scripts", ["python3", "tools/dedupe-script-tags.py"])
    run("country SEO copy (titles, descriptions, roster honesty)", ["python3", "tools/apply-country-seo.py"])
    run("site shell (one header + one footer, every page)", ["node", "tools/build-shell.js"])
    run("sitemap publication gate", ["python3", "tools/build-sitemaps.py"])
    run("search index (published pages only)", ["python3", "tools/build-search-index.py"])
    run("copy index (ownership fingerprints)", ["node", "tools/build-copy-index.js"])
    run("truthful editorial dates", ["python3", "tools/update-editorial-metadata.py"])
    run("site features on every page (theme, voice, journal, bylines, honest notices)", ["python3", "tools/apply-ultra.py"])
    run("partial Phase 1 course publication boundary", ["python3", "tests/regression/test-partial-course-publication.py"])
    run("rendered Phase 2 root Indian topic parity + report",
        ["python3", "tools/audit-indian-topic-parity.py", "--write-report"])
    run("Phase 2: full public-page technical inventory", ["python3", "tools/build-full-page-inventory.py"])
    run("Phase 2: detailed content inventory", ["python3", "tools/build-phase2-content-inventory.py"])
    run("Phase 3 master-command originality audit and human-review queue",
        ["python3", "tools/build-phase3-originality-audit.py"])
    run("doctor", ["node", "tools/doctor.js"])
    print("\n══════════════════════════════════════════")
    print("build-all complete — every step passed.")
    print("Review `git status`, then commit + deploy.")
    print("══════════════════════════════════════════")


if __name__ == "__main__":
    main()
