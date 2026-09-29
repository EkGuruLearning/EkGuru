#!/usr/bin/env bash
# EkGuru weekly AdSense + SEO guard (plan PART C, Phase 10).
#
#   bash tools/weekly-guard.sh          # from the repository root
#
# Live checks hit https://ekguru.shop; repo checks run against this checkout.
# Exit 0 = ALL GREEN. Any FAIL exits 1 — tell the owner which line failed.
# Also run weekly by .github/workflows/live-guard.yml (network checks can be
# flaky in CI; a single FAIL there is a prompt to re-run locally, not a verdict).
set -u
cd "$(dirname "$0")/.." || exit 2
SITE="${SITE:-https://ekguru.shop}"
FAIL=0
C="curl -sL --max-time 25"
code(){ curl -sL --max-time 25 -o /dev/null -w '%{http_code}' "$1"; }
ck(){ printf "%-58s" "$1"; shift; if eval "$*" >/dev/null 2>&1; then echo "OK"; else echo "FAIL"; FAIL=1; fi; }

ck "site 200"              '[ "$(code $SITE/)" = 200 ]'
ck "hindi/ 200"            '[ "$(code $SITE/hindi/)" = 200 ]'
ck "contact/ 200"          '[ "$(code $SITE/contact/)" = 200 ]'
ck "ads.txt publisher"     '$C $SITE/ads.txt | grep -q "google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0"'
ck "loader on homepage"    '$C $SITE/ | grep -q adsbygoogle'
ck "loader on hindi"       '$C $SITE/hindi/ | grep -q adsbygoogle'
ck "no ads on privacy"     '[ "$(code $SITE/privacy/)" = 200 ] && ! $C $SITE/privacy/ | grep -q adsbygoogle.js'
ck "no ads on courses"     '[ "$(code $SITE/courses/)" = 200 ] && ! $C $SITE/courses/ | grep -q adsbygoogle.js'
ck "robots allows"         '$C $SITE/robots.txt | grep -q "^Allow: /"'
ck "sitemap index 200"     '[ "$(code $SITE/sitemap-index.xml)" = 200 ]'
ck "policy gate correct"   'python3 -c "import json,sys; d=json.load(open(\"data/monetization/google-monetization.json\")); sys.exit(0 if d[\"ad_policy\"][\"loader_allowed\"]==[\"HIGH_CONTENT\",\"MEDIUM_CONTENT\"] else 1)"'
ck "runtime flags still off" 'grep -q "ADS_RUNTIME_ENABLED *= *false" js/monetization.js && grep -q "ADVERTISING_AVAILABLE *= *false" js/cookie-consent.js'
ck "inject idempotent"     'python3 tools/inject-ads.py --check'
ck "ad policy tests"       'node tools/test-ad-policy.mjs'
ck "CI green (main)"       'gh run list --branch main --workflow ci.yml --limit 1 --json conclusion -q ".[0].conclusion" | grep -qx success'

echo
[ $FAIL -eq 0 ] && echo "GUARD: ALL GREEN" || echo "GUARD: FAILURES — report the FAIL lines to the owner"
exit $FAIL
