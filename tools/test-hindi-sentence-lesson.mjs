#!/usr/bin/env node
/** Single-lesson pilot regression tests. Run: node tools/test-hindi-sentence-lesson.mjs
 * Uses the existing jsdom dev dependency; no browser/dependency install required.
 * Real-browser layout/offline evidence is separate from these DOM assertions.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { gzipSync } from 'node:zlib';
import { createHash } from 'node:crypto';
import { createRequire } from 'node:module';
import { JSDOM } from 'jsdom';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const rel = 'learn/hindi-sentence-structure/index.html';
const html = read(rel), script = read('js/hindi-sentence-lesson.js'), css = read('css/hindi-sentence-lesson.css');
const dom = new JSDOM(html, { url: 'https://ekguru.shop/learn/hindi-sentence-structure/', runScripts: 'outside-only', pretendToBeVisual: true });
const w = dom.window, d = w.document;
await new Promise(resolve => w.addEventListener('load', resolve, { once: true }));
w.matchMedia = q => ({ matches: false, media: q, addEventListener() {}, addListener() {} });
w.scrollTo = () => {};
w.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
let passed = 0;
function test(name, fn) { fn(); passed++; console.log('PASS ' + name); }
const $ = s => d.querySelector(s), all = s => [...d.querySelectorAll(s)];
const click = id => $('#' + id).click();
const text = id => $('#' + id).textContent;
const state = () => $('#hsl-feedback').dataset.state;
const choose = words => words.forEach(word => { const button = all('#hsl-bank button').find(b => b.textContent === word); assert.ok(button, word); button.click(); });
test('static fallback retains models, checks, lesson controls, canonical and indexing', () => {
  assert.equal(all('[data-hsl-model]').length, 3);
  assert.equal(all('.quiz details').length, 3);
  assert.ok($('#lesson-complete')); assert.ok($('#offline-ctl'));
  assert.equal($('#hsl-exercise').hidden, true);
  assert.equal($('link[rel="canonical"]').href, 'https://ekguru.shop/learn/hindi-sentence-structure/');
  assert.ok(!all('meta[name="robots"]').some(m => /noindex/.test(m.content)));
  all('script[type="application/ld+json"]').forEach(s => JSON.parse(s.textContent));
});
w.eval(read('js/storybook.js'));
w.eval(script);
test('shared storybook TOC does not break stable anchors or section names', () => {
  for (const e of all('[aria-labelledby]')) for (const id of e.getAttribute('aria-labelledby').split(/\s+/)) assert.ok(d.getElementById(id), id);
  for (const a of all('.sb-toc a,.hsl-actions a')) assert.ok(d.getElementById(a.hash.slice(1)), a.hash);
  assert.equal($('#hsl-exercise').hidden, false);
});
test('boot is idempotent', () => { w.eval(script); assert.equal(all('#hsl-bank button').length, 4); });
test('highlight uses text labels, pressed state and explanatory status', () => {
  $('[data-highlight="verb"]').click();
  assert.equal($('[data-highlight="verb"]').getAttribute('aria-pressed'), 'true');
  assert.equal($('.hsl-piece.is-active').dataset.part, 'verb');
  assert.match(text('hsl-demo-note'), /auxiliary/);
});
test('incomplete remains unscored and reveal does not count as built', () => {
  click('hsl-check'); assert.match(text('hsl-feedback'), /Not checked yet/);
  click('hsl-reveal'); assert.match(text('hsl-progress'), /0 models built/);
});
test('wrong complete order explains neutral pattern rather than forbidding all variants', () => {
  choose(['खाता', 'मैं', 'रोटी', 'हूँ']); click('hsl-check');
  assert.equal(state(), 'retry'); assert.match(text('hsl-feedback'), /Other word orders can occur/);
});
test('word toggle, answer removal and clear retain keyboard focus', () => {
  click('hsl-clear'); const first = $('#hsl-bank button'); first.focus(); first.click();
  assert.equal(d.activeElement, first); assert.equal(first.getAttribute('aria-pressed'), 'true');
  first.click(); assert.equal(all('#hsl-answer button').length, 0);
  choose(['मैं', 'रोटी']); $('#hsl-answer button').click();
  assert.equal(text('hsl-answer'), 'रोटी'); assert.equal(d.activeElement, $('#hsl-answer button'));
  $('#hsl-answer button').click(); assert.equal(d.activeElement, first);
});
test('correct model counts once; clear preserves built count', () => {
  choose(['मैं', 'रोटी', 'खाता', 'हूँ']); click('hsl-check'); click('hsl-check');
  assert.equal(state(), 'correct'); assert.match(text('hsl-progress'), /1 model built/);
  click('hsl-clear'); assert.match(text('hsl-progress'), /1 model built/);
});
test('all authored models and Devanagari graphemes survive selection', () => {
  for (const words of [['वह', 'किताब', 'पढ़ती', 'है'], ['हम', 'दिल्ली', 'में', 'रहते', 'हैं']]) {
    click('hsl-next'); assert.equal(d.activeElement, $('#hsl-prompt'));
    choose(words); assert.equal(text('hsl-answer'), words.join(''));
    click('hsl-check'); assert.equal(state(), 'correct');
  }
  assert.match(text('hsl-progress'), /3 models built/);
  click('hsl-next'); assert.match(text('hsl-prompt'), /I eat bread/);
});
test('card keyboard state follows existing flip owner without intercepting Listen', () => {
  const card = $('.vcard'); card.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true }));
  assert.equal(card.getAttribute('aria-pressed'), 'true');
  const listen = card.querySelector('.spk');
  const event = new w.KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true }); listen.dispatchEvent(event);
  assert.equal(event.defaultPrevented, false); assert.equal(card.getAttribute('aria-pressed'), 'true');
  card.click(); assert.equal(card.getAttribute('aria-pressed'), 'false');
});
test('all lesson resource URLs and script/style assets resolve locally', () => {
  for (const e of all('.hsl-next-grid a,script[src],link[rel="stylesheet"]')) {
    const url = new URL(e.getAttribute('href') || e.getAttribute('src'), w.location.href);
    if (url.origin !== w.location.origin) continue;
    const target = path.join(root, decodeURIComponent(url.pathname));
    assert.ok(fs.existsSync(target), url.pathname);
    if (url.pathname.endsWith('/')) assert.ok(fs.existsSync(path.join(target, 'index.html')));
  }
});
test('pilot copy fingerprint is current without a site-wide index rewrite', () => {
  const require = createRequire(import.meta.url);
  const { proseOf, titleOf, shingles, SHINGLE } = require('./build-copy-index.js');
  const row = JSON.parse(read('data/copy-index.json')).pages.find(p => p.u === 'learn/hindi-sentence-structure/');
  const text = proseOf(html), words = text.toLowerCase().split(' ');
  assert.deepEqual(row, { u: 'learn/hindi-sentence-structure/', t: titleOf(html), w: words.length,
    sha: createHash('sha1').update(text).digest('hex').slice(0, 16), n: words.length - SHINGLE + 1, s: shingles(words) });
});
test('motion/fallback rules and lightweight no-storage enhancement contract', () => {
  assert.match(css, /prefers-reduced-motion:reduce/); assert.match(css, /html:not\(\.hsl-ready\)/);
  assert.match(css, /\.hsl-lesson \[hidden\]\{display:none!important\}/);
  assert.ok(!/localStorage|sessionStorage|fetch\(|XMLHttpRequest|speechSynthesis/.test(script));
  const bytes = gzipSync(css).length + gzipSync(script).length;
  assert.ok(bytes <= 10 * 1024, `${bytes} gzip bytes`); console.log(`  Pilot CSS + JS: ${bytes} gzip bytes`);
});
dom.window.close();
console.log(`${passed} pilot regression checks passed`);
