// Real analytics runtime; each case gets an independent browser. No network.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM } from 'jsdom';
const source = readFileSync(new URL('../js/analytics.js', import.meta.url), 'utf8');
let cases = 0;
function browser({ consent, dnt, gpc, owner, provider = 'goatcounter' } = {}) {
  const dom = new JSDOM('<!doctype html><head></head><body></body>', {
    url: 'https://ekguru.shop/learn/hindi/?ref=travel-pilot', runScripts: 'outside-only', pretendToBeVisual: true,
  });
  const w = dom.window;
  if (consent !== undefined) w.localStorage.setItem('ekguru_cookie_consent_v3', JSON.stringify({ analytics: consent }));
  if (owner) w.localStorage.setItem('ekguru_no_track', '1');
  if (dnt) Object.defineProperty(w.navigator, 'doNotTrack', { value: '1' });
  if (gpc) Object.defineProperty(w.navigator, 'globalPrivacyControl', { value: true });
  w.EKGURU_SITE = { analytics: { provider, site: 'ekguru' } };
  w.eval(source);
  const scripts = () => [...w.document.querySelectorAll('script[src]')];
  function choose(allowed) {
    w.localStorage.setItem('ekguru_cookie_consent_v3', JSON.stringify({ analytics: allowed }));
    w.document.dispatchEvent(new w.CustomEvent('ekguru:consent', { detail: { analytics: allowed } }));
  }
  // Mimic count.js assigning count() and completing its asynchronous load.
  const hits = [];
  function finishLoad() {
    w.goatcounter.count = function (data) { hits.push(data || { pageview: true }); };
    scripts().find((s) => /gc\.zgo\.at/.test(s.src)).dispatchEvent(new w.Event('load'));
  }
  return { w, scripts, choose, hits, finishLoad, close: () => dom.window.close() };
}
function test(name, run) { run(); cases++; console.log('PASS ' + name); }

test('reject → accept resumes events/direct calls without a second script or pageview', () => {
  const b = browser();
  assert.equal(b.scripts().length, 1);
  assert.equal(b.w.goatcounter.no_onload, true, 'async provider may not auto-count after rejection');
  b.finishLoad();
  assert.equal(b.hits.length, 1);
  b.w.EkGuruAnalytics.event('booking_open', 'public-tutor-id');
  assert.equal(b.hits.length, 2);
  assert.equal(b.hits[1].path, 'event/booking_open');
  b.choose(false);
  b.w.EkGuruAnalytics.event('booking_open', 'public-tutor-id');
  b.w.goatcounter.count({ path: 'event/legacy', event: true });
  assert.equal(b.hits.length, 2, 'both paths stop');
  b.choose(true);
  assert.equal(b.hits.length, 2, 'accept does not duplicate pageview');
  b.w.EkGuruAnalytics.event('booking_open', 'public-tutor-id');
  b.w.goatcounter.count({ path: 'event/legacy', event: true });
  assert.equal(b.hits.length, 4, 'both paths resume');
  for (let i = 0; i < 3; i++) { b.choose(false); b.choose(true); }
  b.w.EkGuruAnalytics.event('whatsapp_click', 'public-tutor-id');
  assert.equal(b.hits.length, 5, 'no duplicate event handlers after repeated choices');
  assert.equal(b.scripts().length, 1);
  b.close();
});

test('reject before count.js finishes blocks pageview and late legacy implementation', () => {
  const b = browser();
  b.choose(false);
  b.finishLoad();
  b.w.goatcounter.count({ path: 'event/legacy', event: true });
  assert.equal(b.hits.length, 0);
  b.choose(true);
  assert.equal(b.hits.length, 1, 'first permitted pageview is recorded once');
  b.choose(true);
  assert.equal(b.hits.length, 1);
  b.close();
});

test('initial saved rejection loads nothing; later acceptance loads once', () => {
  const b = browser({ consent: false });
  assert.equal(b.scripts().length, 0);
  b.choose(true);
  assert.equal(b.scripts().length, 1);
  b.finishLoad();
  assert.equal(b.hits.length, 1);
  b.choose(false); b.choose(true);
  assert.equal(b.scripts().length, 1);
  assert.equal(b.hits.length, 1);
  b.close();
});

for (const flag of ['dnt', 'gpc', 'owner']) {
  test(flag + ' blocks loading even when analytics accepted', () => {
    const b = browser({ [flag]: true });
    assert.equal(b.scripts().length, 0);
    b.choose(true);
    assert.equal(b.scripts().length, 0);
    b.close();
  });
}

test('owner exclusion set after load silences future direct and helper calls', () => {
  const b = browser(); b.finishLoad();
  b.w.EkGuruAnalytics.optOut();
  b.w.EkGuruAnalytics.event('booking_open', 'public-tutor-id');
  b.w.goatcounter.count({ path: 'event/legacy', event: true });
  assert.equal(b.hits.length, 1);
  b.w.EkGuruAnalytics.optIn();
  b.w.EkGuruAnalytics.event('booking_open', 'public-tutor-id');
  assert.equal(b.hits.length, 2);
  b.close();
});

test('background page waits for visibility; provider click binding is retained once', () => {
  const b = browser();
  let bindings = 0;
  b.w.goatcounter.bind_events = () => { bindings++; };
  let visibility = 'hidden';
  Object.defineProperty(b.w.document, 'visibilityState', { get: () => visibility });
  b.finishLoad();
  assert.equal(b.hits.length, 0);
  assert.equal(bindings, 1);
  visibility = 'visible';
  b.w.document.dispatchEvent(new b.w.Event('visibilitychange'));
  assert.equal(b.hits.length, 1);
  b.choose(false); b.choose(true);
  b.w.document.dispatchEvent(new b.w.Event('visibilitychange'));
  assert.equal(b.hits.length, 1);
  assert.equal(bindings, 1);
  b.close();
});

test('blocked or failed provider never breaks page interactions', () => {
  const b = browser();
  assert.doesNotThrow(() => b.w.EkGuruAnalytics.event('booking_open', 'public-tutor-id'));
  b.scripts()[0].dispatchEvent(new b.w.Event('error'));
  b.choose(false); b.choose(true);
  assert.equal(b.hits.length, 0);
  b.close();
});

test('Plausible helper events also honour rejection and reacceptance', () => {
  const b = browser({ provider: 'plausible' });
  const events = [];
  b.w.plausible = (...args) => events.push(args);
  b.w.EkGuruAnalytics.event('booking_open', 'public-tutor-id');
  b.choose(false);
  b.w.EkGuruAnalytics.event('booking_open', 'public-tutor-id');
  assert.equal(events.length, 1);
  b.choose(true);
  b.w.EkGuruAnalytics.event('booking_open', 'public-tutor-id');
  assert.equal(events.length, 2);
  assert.equal(b.scripts().length, 1);
  b.close();
});
console.log(`PASS: ${cases} analytics lifecycle cases; no live requests sent`);
