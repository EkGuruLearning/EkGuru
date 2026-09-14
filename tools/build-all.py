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
  9  doctor (SEO + privacy + gate + admin stats)

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
    run("doctor", ["node", "tools/doctor.js"])
    print("\n══════════════════════════════════════════")
    print("build-all complete — every step passed.")
    print("Review `git status`, then commit + deploy.")
    print("══════════════════════════════════════════")


if __name__ == "__main__":
    main()
