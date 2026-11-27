#!/usr/bin/env node
// Read-only checklist. This cannot certify a CMP or authorize ad serving.
import { readFileSync, existsSync } from 'node:fs';
const read = (p) => readFileSync(new URL('../' + p, import.meta.url), 'utf8');
const mon = JSON.parse(read('data/monetization/google-monetization.json'));
const cookie = read('js/cookie-consent.js');
const runtime = read('js/monetization.js');
const home = read('index.html');
const client = mon.publisher.adsense_client;
const checks = {
  publisher_matches_home: home.includes('content="' + client + '"') && home.includes('client=' + client),
  ads_txt_matches: read('ads.txt').split(/\r?\n/).some((l) => l.trim() === `google.com, ${mon.publisher.ads_txt_id}, DIRECT, f08c47fec0942fa0`),
  privacy_page_exists: existsSync(new URL('../privacy/index.html', import.meta.url)),
  referrer_policy_compatible: /<meta[^>]*content="strict-origin-when-cross-origin"[^>]*name="referrer"/.test(home),
  local_advertising_choice_disabled: /ADVERTISING_AVAILABLE\s*=\s*false/.test(cookie),
  ad_runtime_stays_disabled: /ADS_RUNTIME_ENABLED\s*=\s*false/.test(runtime),
  sensitive_routes_excluded: ['/contact/', '/join.html', '/search/', '/courses/', '/privacy/'].every((p) => mon.excluded_paths.includes(p)),
};
const result = {
  status: Object.values(checks).every(Boolean) ? 'BLOCKED_ACCOUNT_AND_PRODUCTION_VERIFICATION' : 'REPOSITORY_CHECK_FAILED',
  launch_authorized: false,
  repository_checks: checks,
  recorded_account_status: mon.approval_status,
  recorded_consent_status: mon.consent.status,
  outstanding_evidence: [
    'AdSense Sites status for ekguru.shop (account review; not established by publisher code)',
    'Published certified CMP message for the correct domain and regional settings',
    'Production accept, reject, manage-options, revoke and no-choice network tests',
    'Certified CMP integration with runtime gating and accurate privacy disclosures',
    'Editorial/policy clearance, account exclusions and explicit owner release approval',
  ],
  next_step: 'AdSense > Privacy & messaging > European regulations > Create/Manage > select ekguru.shop; see docs/ADVERTISING-CONSENT-LAUNCH.md',
};
if (process.argv.includes('--json')) console.log(JSON.stringify(result, null, 2));
else {
  console.log('Advertising launch: ' + result.status + '\n');
  for (const [name, pass] of Object.entries(checks)) console.log((pass ? 'PASS ' : 'FAIL ') + name);
  console.log('\nAccount status recorded in repository: ' + result.recorded_account_status);
  console.log('Consent status recorded in repository: ' + result.recorded_consent_status);
  console.log('\nNOT enabled. Required evidence:');
  result.outstanding_evidence.forEach((x) => console.log('- ' + x));
  console.log('\nNext: ' + result.next_step);
}
// Diagnostic mode is successful even when launch is honestly blocked.
// --check is the release gate and intentionally fails without authorization.
if (process.argv.includes('--check')) process.exitCode = 1;
else if (!Object.values(checks).every(Boolean)) process.exitCode = 1;
