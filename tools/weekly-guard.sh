#!/usr/bin/env bash
# EkGuru weekly AdSense + SEO guard (plan PART C, Phase 10).
#
#   bash tools/weekly-guard.sh          # from the repository root
#
# Live checks hit https://ekguru.shop; repo checks run against this checkout.
# Exit 0 = ALL GREEN. Any FAIL exits 1 — tell the owner which line failed.
# Also run weekly by .github/workflows/live-guard.yml (network checks can be
# flaky in CI; a single FAIL there is a prompt to re-run locally, not a verdict).
#
# 17 Nov 2026 — why the weekly run went red every Monday since 2 Nov:
#   ekguru.shop now resolves to Cloudflare (104.21.x / 172.67.x), i.e. the
#   DNS records are proxied in front of GitHub Pages. Two consequences:
#     1. Cloudflare's bot rules challenge a bare `curl` from a datacenter IP
#        (403 / 503 "Just a moment…", header `cf-mitigated: challenge`), so
#        every live check failed at once while the repo checks stayed green.
#     2. GitHub can no longer complete the ACME challenge for the Pages
#        certificate (`https_certificate.state = bad_authz`), so the origin
#        certificate is NOT renewing (expires 2026-12-09). Visitors are fine
#        while Cloudflare's edge certificate fronts the site, but the
#        Cloudflare SSL mode must be "Full" (not "Full (strict)") or the site
#        returns 526 once the origin cert lapses. Owner action, Cloudflare
#        dashboard — not something the repo can fix.
#   This script now (a) sends a browser-like User-Agent with retries,
#   (b) records WHY a line failed (HTTP code + cf-mitigated header) and
#   (c) writes the table to $GITHUB_STEP_SUMMARY so the reason is visible on
#   the run page even after the logs expire.
set -u
cd "$(dirname "$0")/.." || exit 2
SITE="${SITE:-https://ekguru.shop}"
FAIL=0
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 EkGuruGuard/1.1 (+https://ekguru.shop/contact/)"
fetch(){ curl -sL --max-time 25 --retry 2 --retry-delay 3 -A "$UA" "$@"; }
code(){ curl -sL --max-time 25 --retry 2 --retry-delay 3 -A "$UA" -o /dev/null -w '%{http_code}' "$1"; }
# diag <url>: one line with the status code and whether Cloudflare challenged us
diag(){ curl -sIL --max-time 25 -A "$UA" "$1" 2>/dev/null | tr -d '\r' | awk 'tolower($0) ~ /^http\/|^cf-mitigated:|^server:/ {printf "%s · ", $0}' | sed 's/ · $//'; }
SUMMARY="${GITHUB_STEP_SUMMARY:-}"
[ -n "$SUMMARY" ] && printf '## Weekly guard — %s\n\n| check | result | detail |\n|---|---|---|\n' "$(date -u +%Y-%m-%dT%H:%MZ)" >> "$SUMMARY"
ck(){
  local name="$1"; shift
  local url=""
  # the check is passed single-quoted, so it still says the literal "$SITE/…"
  url=$(printf '%s' "$*" | grep -o '\$SITE/[^ )"'"'"']*' | head -1); url=${url/\$SITE/$SITE}
  printf "%-58s" "$name"
  if eval "$*" >/dev/null 2>&1; then
    echo "OK"
    [ -n "$SUMMARY" ] && printf '| %s | ✅ OK | |\n' "$name" >> "$SUMMARY"
  else
    local why=""
    [ -n "$url" ] && why=$(diag "$url")
    echo "FAIL${why:+  ← $why}"
    [ -n "$SUMMARY" ] && printf '| %s | ❌ FAIL | %s |\n' "$name" "${why:-see log}" >> "$SUMMARY"
    FAIL=1
  fi
}

ck "site 200"              '[ "$(code $SITE/)" = 200 ]'
ck "hindi/ 200"            '[ "$(code $SITE/hindi/)" = 200 ]'
ck "contact/ 200"          '[ "$(code $SITE/contact/)" = 200 ]'
ck "ads.txt publisher"     'fetch $SITE/ads.txt | grep -q "google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0"'
ck "loader on homepage"    'fetch $SITE/ | grep -q adsbygoogle'
ck "loader on hindi"       'fetch $SITE/hindi/ | grep -q adsbygoogle'
ck "no ads on privacy"     '[ "$(code $SITE/privacy/)" = 200 ] && ! fetch $SITE/privacy/ | grep -q adsbygoogle.js'
ck "no ads on courses"     '[ "$(code $SITE/courses/)" = 200 ] && ! fetch $SITE/courses/ | grep -q adsbygoogle.js'
ck "robots allows"         'fetch $SITE/robots.txt | grep -q "^Allow: /"'
ck "sitemap index 200"     '[ "$(code $SITE/sitemap-index.xml)" = 200 ]'
ck "policy gate correct"   'python3 -c "import json,sys; d=json.load(open(\"data/monetization/google-monetization.json\")); sys.exit(0 if d[\"ad_policy\"][\"loader_allowed\"]==[\"HIGH_CONTENT\",\"MEDIUM_CONTENT\"] else 1)"'
ck "runtime flags still off" 'grep -q "ADS_RUNTIME_ENABLED *= *false" js/monetization.js && grep -q "ADVERTISING_AVAILABLE *= *false" js/cookie-consent.js'
ck "inject idempotent"     'python3 tools/inject-ads.py --check'
ck "ad policy tests"       'node tools/test-ad-policy.mjs'
ck "CI green (main)"       'gh run list -R "${GITHUB_REPOSITORY:-EkGuruLearning/EkGuru}" --branch main --workflow ci.yml --limit 1 --json conclusion -q ".[0].conclusion" | grep -qx success'

echo
if [ $FAIL -eq 0 ]; then
  echo "GUARD: ALL GREEN"
else
  echo "GUARD: FAILURES — report the FAIL lines to the owner"
  echo "  · 'cf-mitigated: challenge' on a live line = Cloudflare blocked the probe, not a broken page:"
  echo "    add a WAF skip rule for the EkGuruGuard user-agent, or turn Bot Fight Mode off for /ads.txt, /robots.txt, /sitemap-index.xml."
  [ -n "$SUMMARY" ] && printf '\n`cf-mitigated: challenge` = Cloudflare challenged the probe (allow the EkGuruGuard UA in the WAF). A plain non-200 = the page really is down.\n' >> "$SUMMARY"
fi
exit $FAIL
