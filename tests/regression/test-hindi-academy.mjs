import { readFileSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import assert from 'node:assert/strict';
import { JSDOM } from 'jsdom';

const root = process.cwd();
const read = p => readFileSync(join(root, p), 'utf8');
const manifest = JSON.parse(read('data/hindi-academy/curriculum.json'));
assert.equal(manifest.tracks.length, 5);
const ids = new Set();
for (const track of manifest.tracks) {
  assert(track.phases.length > 0);
  for (const entry of [track, ...track.phases]) {
    assert(!ids.has(entry.id)); ids.add(entry.id);
    if (entry.url) assert(existsSync(join(root, entry.url, 'index.html')), entry.url);
  }
}
for (const page of ['learn/hindi/academy/index.html', 'learn/hindi/academy/vowels/index.html', 'learn/hindi/academy/worksheet/index.html', 'learn/hindi/academy/answers/index.html']) {
  const dom = new JSDOM(read(page), { url: 'https://ekguru.shop/' + page.replace('index.html', '') });
  const doc = dom.window.document;
  assert.equal(doc.querySelectorAll('h1').length, 1, page);
  assert.equal(doc.querySelector('meta[name="robots"]').content, 'noindex, follow');
  assert.equal(doc.querySelector('link[rel="canonical"]').href, dom.window.location.href);
  const seen = new Set();
  for (const el of doc.querySelectorAll('[id]')) { assert(!seen.has(el.id), `duplicate ${el.id}`); seen.add(el.id); }
  for (const a of doc.querySelectorAll('a[href], link[href], script[src]')) {
    const url = new URL(a.getAttribute('href') || a.getAttribute('src'), dom.window.location.href);
    if (url.origin !== dom.window.location.origin) continue;
    const file = resolve(root, '.' + url.pathname, ...(url.pathname.endsWith('/') ? ['index.html'] : []));
    assert(existsSync(file), `missing ${url.href} on ${page}`);
    if (url.hash) { const target = new JSDOM(readFileSync(file, 'utf8')).window.document; assert(target.getElementById(decodeURIComponent(url.hash.slice(1))), `missing ${url.href}`); }
  }
}
const html = read('learn/hindi/academy/vowels/index.html');
const dom = new JSDOM(html, { url: 'https://ekguru.shop/learn/hindi/academy/vowels/', runScripts: 'outside-only' });
const w = dom.window, d = w.document;
const paint = [];
w.HTMLCanvasElement.prototype.getContext = () => ({ clearRect(){ paint.push('clear'); }, beginPath(){}, moveTo(){}, lineTo(){}, stroke(){ paint.push('stroke'); } });
w.HTMLCanvasElement.prototype.setPointerCapture = () => {};
const saved = { version: 1, opened: [{slug:'old',title:'Old lesson',at:1}], completed: {old:{title:'Old lesson',at:1}}, quizzes:{} };
w.localStorage.setItem('ekguru:hindi:v1:progress', JSON.stringify(saved));
w.eval(read('js/hindi-progress.js')); w.eval(read('js/hindi-academy.js'));
d.dispatchEvent(new w.Event('DOMContentLoaded'));
assert(w.EkGuruProgress.isComplete('old'), 'existing data preserved');
d.querySelector('#lesson-complete button').click();
assert(w.EkGuruProgress.isComplete('academy-vowels'));
d.querySelector('[name=q1][value="आ"]').click(); d.querySelector('[name=q2][value="after"]').click(); d.querySelector('[name=q3][value="mark"]').click();
d.querySelector('#quiz').dispatchEvent(new w.Event('submit', {bubbles:true,cancelable:true}));
assert.match(d.querySelector('#quiz-result').textContent, /3 of 3/);
assert.equal(w.EkGuruProgress.snapshot().quizzes['academy-vowels'].last, 3);
const exportText = w.EkGuruProgress.exportJSON(); assert(w.EkGuruProgress.importJSON(exportText).ok); assert(w.EkGuruProgress.isComplete('old'));
d.querySelector('#quiz').reset(); assert.equal(d.querySelector('#quiz-result').textContent, '');
d.querySelector('[data-speak]').click(); assert.match(d.querySelector('#audio-status').textContent, /No Hindi voice/);
let spoken = false;
w.EkGuruVoice = {available:(lang) => { assert.equal(lang, 'hi-IN'); return false; }, speak:()=>{spoken=true;}, stop(){}};
d.querySelector('[data-speak]').click(); assert.equal(spoken,false); assert.match(d.querySelector('#audio-status').textContent, /No Hindi voice/);
w.EkGuruVoice.available = () => true; w.EkGuruVoice.speak = (text, lang, rate) => { assert.equal(lang, 'hi-IN'); assert.equal(text, 'अनार'); assert.equal(rate, 1); spoken = true; return true; };
d.querySelector('[data-speak]').click(); assert.equal(spoken,true);
d.querySelector('#letter').value = 'आ'; d.querySelector('#letter').dispatchEvent(new w.Event('change')); assert.equal(d.querySelector('#trace-model').textContent,'आ');
d.querySelector('#toggle-model').click(); assert(d.querySelector('#trace-model').hidden); d.querySelector('#toggle-model').click(); assert(!d.querySelector('#trace-model').hidden);
d.querySelector('#clear').click(); assert(paint.includes('clear'));
console.log('PASS Hindi Academy: manifest, links, metadata, quiz, journal preservation, audio fallback and tracing controls');
