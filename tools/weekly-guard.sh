#!/usr/bin/env bash
# EkGuru weekly AdSense + SEO guard (plan PART C, Phase 10).
#
#   bash tools/weekly-guard.sh          # from the repository root
#   STRICT_LIVE=1 bash tools/weekly-guard.sh   # treat Cloudflare challenge as hard fail
#
# Live checks hit https://ekguru.shop; repo checks run against this checkout.
# Exit 0 = ALL GREEN (or live probes challenged by Cloudflare WAF while local
# equivalents pass). Any real HTTP/content/policy FAIL exits 1.
#
# Why Cloudflare challenge handling exists:
#   ekguru.shop is proxied through Cloudflare in front of GitHub Pages.
#   Cloudflare Bot Fight / WAF rules frequently return HTTP 403/503 with header
#   `cf-mitigated: challenge` to datacenter runner IPs (GitHub Actions), causing
#   all live curl checks to fail even when the live site is healthy and masking
#   real regressions. When `cf-mitigated: challenge` is detected and STRICT_LIVE
#   is not 1, each live probe falls back to verifying the exact local repository
#   file invariant and logs a clear ⚠️ CF_CHALLENGE row in $GITHUB_STEP_SUMMARY.
#   Non-challenge failures (404, 500, 522, 526 origin SSL expiry, or failed
#   content/policy invariants) still fail the build with exit 1.
set -u
cd "$(dirname "$0")/.." || exit 2
SITE="${SITE:-https://ekguru.shop}"
STRICT_LIVE="${STRICT_LIVE:-0}"
FAIL=0
CF_CHALLENGED=0
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 EkGuruGuard/1.2 (+https://ekguru.shop/contact/)"
fetch(){ curl -sL --max-time 25 --retry 2 --retry-delay 3 -A "$UA" "$@"; }
code(){ curl -sL --max-time 25 --retry 2 --retry-delay 3 -A "$UA" -o /dev/null -w '%{http_code}' "$1"; }
# diag <url>: one line with the status code and whether Cloudflare challenged us
diag(){ curl -sIL --max-time 25 -A "$UA" "$1" 2>/dev/null | tr -d '\r' | awk 'tolower($0) ~ /^http\/|^cf-mitigated:|^server:/ {printf "%s · ", $0}' | sed 's/ · $//'; }
SUMMARY="${GITHUB_STEP_SUMMARY:-}"
[ -n "$SUMMARY" ] && printf '## Weekly guard — %s\n\n| check | result | detail |\n|---|---|---|\n' "$(date -u +%Y-%m-%dT%H:%MZ)" >> "$SUMMARY"

ck(){
  local name="$1"
  local live_cmd="$2"
  local local_fallback="${3:-}"
  local url=""
  url=$(printf '%s' "$live_cmd" | grep -o '\$SITE/[^ )"'"'"']*' | head -1)
  url=${url/\$SITE/$SITE}
  printf "%-58s" "$name"
  if eval "$live_cmd" >/dev/null 2>&1; then
    echo "OK"
    [ -n "$SUMMARY" ] && printf '| %s | ✅ OK | |\n' "$name" >> "$SUMMARY"
    return
  fi

  local why=""
  [ -n "$url" ] && why=$(diag "$url")
  if [ "$STRICT_LIVE" != "1" ] && [ -n "$local_fallback" ] && printf '%s' "$why" | grep -qi 'cf-mitigated:[[:space:]]*challenge'; then
    if eval "$local_fallback" >/dev/null 2>&1; then
      echo "CF_CHALLENGE (repo OK)  ← $why"
      [ -n "$SUMMARY" ] && printf '| %s | ⚠️ CF_CHALLENGE | %s (local repo invariant OK) |\n' "$name" "$why" >> "$SUMMARY"
      CF_CHALLENGED=$((CF_CHALLENGED + 1))
      return
    fi
  fi

  echo "FAIL${why:+  ← $why}"
  if [ "${GITHUB_ACTIONS:-}" = "true" ]; then
    printf '::error title=Weekly guard::%s failed; %s\n' "$name" "${why:-see check command in tools/weekly-guard.sh}"
  fi
  [ -n "$SUMMARY" ] && printf '| %s | ❌ FAIL | %s |\n' "$name" "${why:-see log}" >> "$SUMMARY"
  FAIL=1
}

ck "site 200"              '[ "$(code $SITE/)" = 200 ]'                                                                          'test -s index.html'
ck "hindi/ 200"            '[ "$(code $SITE/hindi/)" = 200 ]'                                                                    'test -s hindi/index.html'
ck "contact/ 200"          '[ "$(code $SITE/contact/)" = 200 ]'                                                                  'test -s contact/index.html'
ck "ads.txt publisher"     'fetch $SITE/ads.txt | grep -q "google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0"'         'grep -q "google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0" ads.txt'
ck "loader on homepage"    'fetch $SITE/ | grep -q adsbygoogle'                                                                  'grep -q adsbygoogle index.html'
ck "loader on hindi"       'fetch $SITE/hindi/ | grep -q adsbygoogle'                                                            'grep -q adsbygoogle hindi/index.html'
ck "no ads on privacy"     '[ "$(code $SITE/privacy/)" = 200 ] && ! fetch $SITE/privacy/ | grep -q adsbygoogle.js'               'test -s privacy/index.html && ! grep -q adsbygoogle.js privacy/index.html'
ck "no ads on courses"     '[ "$(code $SITE/courses/)" = 200 ] && ! fetch $SITE/courses/ | grep -q adsbygoogle.js'               'test -s courses/index.html && ! grep -q adsbygoogle.js courses/index.html'
ck "robots allows"         'fetch $SITE/robots.txt | grep -q "^Allow: /"'                                                        'grep -q "^Allow: /" robots.txt'
ck "sitemap index 200"     '[ "$(code $SITE/sitemap-index.xml)" = 200 ]'                                                         'test -s sitemap-index.xml && grep -q "<sitemapindex" sitemap-index.xml'
ck "policy gate correct"   'python3 -c "import json,sys; d=json.load(open(\"data/monetization/google-monetization.json\")); sys.exit(0 if d[\"ad_policy\"][\"loader_allowed\"]==[\"HIGH_CONTENT\",\"MEDIUM_CONTENT\"] else 1)"'
ck "runtime flags still off" 'grep -q "ADS_RUNTIME_ENABLED *= *false" js/monetization.js && grep -q "ADVERTISING_AVAILABLE *= *false" js/cookie-consent.js'
ck "inject idempotent"     'python3 tools/inject-ads.py --check'
ck "ad policy tests"       'node tools/test-ad-policy.mjs'
ck "CI green (main)"       'gh run list -R "${GITHUB_REPOSITORY:-EkGuruLearning/EkGuru}" --branch main --workflow ci.yml --limit 1 --json conclusion -q ".[0].conclusion" | grep -qx success'

echo
if [ $FAIL -eq 0 ] && [ $CF_CHALLENGED -eq 0 ]; then
  echo "GUARD: ALL GREEN"
elif [ $FAIL -eq 0 ]; then
  echo "GUARD: REPO & POLICY GREEN ($CF_CHALLENGED live probe(s) received Cloudflare Bot Fight challenge; local invariants verified)"
  [ -n "$SUMMARY" ] && printf '\nNote: %d live probe(s) received `cf-mitigated: challenge` from Cloudflare for the GitHub runner IP; all local repository/policy checks passed. Review verified crawler access and WAF diagnostics with the hosting owner; a spoofable User-Agent is not a safe WAF bypass.\n' "$CF_CHALLENGED" >> "$SUMMARY"
else
  echo "GUARD: FAILURES — report the FAIL lines to the owner"
  [ -n "$SUMMARY" ] && printf '\nOne or more checks failed without a Cloudflare bot challenge (or failed local verification).\n' >> "$SUMMARY"
fi
exit $FAIL
