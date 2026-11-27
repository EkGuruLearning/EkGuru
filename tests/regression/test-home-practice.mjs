// Exercise the real homepage script, not a duplicate answer-checking model.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!doctype html><div class="xp-hero-copy"></div>', {
  url: 'https://ekguru.shop/', runScripts: 'outside-only', pretendToBeVisual: true,
});
const { window: w } = dom;
w.matchMedia = () => ({ matches: true }); // No motion timers needed in this test.
w.Math.random = () => 0;
w.fetch = () => { throw new Error('Practice must not require a remote API'); };
w.eval(readFileSync(new URL('../../js/home-future.js', import.meta.url), 'utf8'));
const doc = w.document;
const form = doc.querySelector('[data-hf-type]');
const input = form.querySelector('input');
const msg = form.querySelector('[data-hf-type-msg]');
const next = doc.querySelector('[data-hf-next]');
const word = () => doc.querySelector('[data-hf-word]').textContent;
const roman = () => doc.querySelector('[data-hf-roman]').textContent;
function check(value, ok) {
  input.value = value;
  input.dispatchEvent(new w.Event('input', { bubbles: true }));
  assert.equal(msg.textContent, '', 'editing clears stale success/error');
  form.dispatchEvent(new w.Event('submit', { bubbles: true, cancelable: true }));
  assert.equal(input.getAttribute('aria-invalid'), String(!ok), JSON.stringify(value));
  assert.equal(msg.textContent.startsWith('✓ Correct!'), ok, JSON.stringify(value));
}
assert.equal(input.labels.length, 1);
assert.equal(msg.getAttribute('role'), 'status');
assert.ok(form.querySelector('button[type="submit"]'), 'mobile has a visible check button');
const count = Number(doc.querySelector('[data-hf-progress]').textContent.split('/')[1]);
const seen = new Set();
for (let i = 0; i < count; i++) {
  const hi = word(), latin = roman();
  assert.ok(!seen.has(hi)); seen.add(hi);
  check('', false);
  check('   ', false);
  check('?!।', false);
  check('random wrong answer', false);
  check('नमस्ते', hi === 'नमस्ते'); // old independent list must not leak through
  check(hi + ' गलत', false);
  check(latin + ' wrong', false);
  check(hi, true);
  check(hi.normalize('NFD'), true);
  check(latin, true);
  check('  ' + latin.toUpperCase().replaceAll(' ', '   ') + '  ', true);
  check(hi.replace(/[?।]+$/, '') + '।', true);
  if (hi.includes('्')) check(hi.replaceAll('्', ''), false);
  if (hi === 'धन्यवाद') check('dhanyavad', true);
  if (hi === 'माफ़ कीजिए') check('maaf kijiye', true);
  if (hi === 'हाँ') check('नहीं', false);
  if (hi === 'नहीं') check('हाँ', false);
  check(hi, true);
  assert.equal(word(), hi, 'successful checks never silently advance the exercise');
  input.value = 'edited after success';
  input.dispatchEvent(new w.Event('input', { bubbles: true }));
  assert.equal(msg.textContent, '');
  assert.equal(input.hasAttribute('aria-invalid'), false);
  next.click();
  assert.equal(input.value, '');
  assert.equal(msg.textContent, '');
  assert.equal(input.hasAttribute('aria-invalid'), false);
}
assert.equal(word(), 'नमस्ते', 'Next wraps around the same phrase list');
input.value = 'नमस्ते';
input.dispatchEvent(new w.CompositionEvent('compositionstart'));
form.dispatchEvent(new w.Event('submit', { cancelable: true }));
assert.equal(msg.textContent, '', 'IME composition cannot submit a partial word');
input.dispatchEvent(new w.CompositionEvent('compositionend'));
check('नमस्ते', true);
let spoken;
w.EkGuruVoice = { speak: (text, lang) => { spoken = { text, lang }; return true; } };
next.click();
doc.querySelector('[data-hf-listen]').click();
assert.deepEqual(spoken, { text: word(), lang: 'hi' }, 'listen and check use the visible phrase');
dom.window.close();
console.log(`PASS: home practice — ${count} phrases; correct/wrong, Unicode, reset, IME, voice, no API`);
