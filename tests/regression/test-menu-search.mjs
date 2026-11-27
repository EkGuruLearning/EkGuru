// Drive the shipped feature runtime: removing navigation search must not
// disable the homepage or directory search, including after a live repaint.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM } from 'jsdom';
const read = (p) => readFileSync(new URL('../../' + p, import.meta.url), 'utf8');
for (const page of ['index.html', 'find-tutors.html', 'join.html']) {
  const dom = new JSDOM(read(page), { url: 'https://ekguru.shop/' + page, runScripts: 'outside-only', pretendToBeVisual: true });
  const w = dom.window, d = w.document;
  const heroBefore = d.querySelector('.xp-searchbox')?.innerHTML;
  assert.ok(d.querySelector('.hdr .nav'), 'real site navigation is present');
  w.scrollTo = () => {};
  w.matchMedia = () => ({ matches: false });
  w.eval(read('js/i18n.js'));
  w.EKGURU_TUTORS = [];
  w.eval(read('js/features.js'));
  d.dispatchEvent(new w.Event('DOMContentLoaded'));
  assert.equal(d.querySelectorAll('.hdr .nav input[type="search"], .hdr .nav .hdr-search, #hdr-search').length, 0, page);
  assert.ok(d.querySelector('.hdr .nav a[href*="learn"]'), 'Learn remains available');
  for (const id of ['home-q', 'f-q']) {
    const input = d.getElementById(id);
    if (!input) continue;
    assert.equal(input.dataset.acReady, '1', page + ': search still wired');
    input.value = 'Hindi';
    input.dispatchEvent(new w.Event('input', { bubbles: true }));
    await new Promise((resolve) => w.setTimeout(resolve, 120));
    assert.equal(input.closest('.ac-wrap').querySelector('.ac-box').hidden, false);
    input.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    assert.equal(input.closest('.ac-wrap').querySelector('.ac-box').hidden, true);
  }
  if (heroBefore) assert.equal(d.querySelector('.xp-searchbox').innerHTML, heroBefore, 'homepage course CTA stays untouched');
  w.dispatchEvent(new w.CustomEvent('ekguru:repaint'));
  assert.equal(d.querySelectorAll('.hdr .nav input[type="search"], #hdr-search').length, 0, 'repaint cannot restore drawer search');
  dom.window.close();
  console.log('PASS menu has no search; existing content search preserved: ' + page);
}

// Legacy hero inputs remain supported even though the current homepage uses a CTA.
{
  const dom = new JSDOM('<nav class="nav"></nav><form id="home-search"><input id="home-q" type="search"></form>', { url: 'https://ekguru.shop/', runScripts: 'outside-only' });
  const w = dom.window, d = w.document;
  w.eval(read('js/features.js'));
  d.dispatchEvent(new w.Event('DOMContentLoaded'));
  const input = d.getElementById('home-q');
  assert.equal(input.dataset.acReady, '1');
  input.value = 'Hindi';
  input.dispatchEvent(new w.Event('focus'));
  assert.equal(input.closest('.ac-wrap').querySelector('.ac-box').hidden, false);
  assert.equal(d.querySelector('.nav input'), null);
  w.close();
  console.log('PASS legacy hero search remains wired, outside navigation');
}
