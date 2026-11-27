#!/usr/bin/env node
/* DOM/data regression checks; native voices and real browsers need separate QA. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JSDOM } from 'jsdom';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = p => fs.readFileSync(path.join(ROOT, p), 'utf8');
const dom = new JSDOM(read('learn/hindi/practice/index.html'), { url:'https://ekguru.shop/learn/hindi/practice/', runScripts:'outside-only', pretendToBeVisual:true });
const w = dom.window, d = w.document;
await new Promise(resolve => w.addEventListener('load', resolve, { once:true }));
const spoken = [];
w.SpeechSynthesisUtterance = function (text) { this.text = text; };
w.speechSynthesis = { getVoices:()=>[{ lang:'hi-IN', name:'Test Hindi voice', voiceURI:'test-hi', localService:true }], speak:u=>spoken.push(u), cancel(){}, addEventListener(){} };
for (const file of ['voice-languages.js','voice.js','global-srs.js','hindi-learning-library-data.js','hindi-learning-library.js']) w.eval(read('js/' + file));
const data = w.EKGURU_HINDI_LIBRARY, items = data.items;
const $ = s => d.querySelector(s), all = s => [...d.querySelectorAll(s)];
let passed = 0;
function test(name, fn) { fn(); passed++; console.log('PASS ' + name); }
function change(id, value) { $('#' + id).value = value; $('#' + id).dispatchEvent(new w.Event(id === 'hll-search' ? 'input':'change', { bubbles:true })); }
function clickText(text) { const button = all('#hll-card button').find(b=>b.textContent===text); assert.ok(button, text); button.click(); }
const normal = text => text.normalize('NFC').replace(/[\s।.!?,;:“”"\-—…]+/gu,'').toLowerCase();
test('1000+ genuinely distinct Hindi models, consistent advertised counts', () => {
  assert.ok(items.length >= 1000);
  assert.equal(new Set(items.map(x=>normal(x.hi))).size, items.length);
  assert.equal(new Set(items.map(x=>x.id)).size, items.length);
  const counts = {}; items.forEach(x=>counts[x.kind]=(counts[x.kind]||0)+1);
  assert.equal(JSON.stringify(counts), JSON.stringify(data.counts));
  assert.match($('#hindi-learning-library').textContent, new RegExp(items.length.toLocaleString('en-US')));
  for (const item of items) {
    assert.ok(item.hi && item.roman && item.en && item.title && item.source);
    assert.ok(item.hi.length < 2000); assert.match(item.hi, /[\u0900-\u097f]/);
    assert.ok(data.levels.includes(item.level));
  }
});
test('search metadata and introduction reflect the expanded practice without changing indexing', () => {
  assert.equal(d.title, 'Hindi Practice: Words, Sentences & Reading | EkGuru');
  assert.equal(all('h1').length, 1); assert.equal($('h1').textContent, 'Hindi practice: words, sentences and reading');
  assert.match($('.lede').textContent, /^Hindi practice from first letters to connected reading/);
  const description = $('meta[name="description"]').content;
  assert.match(description, /paragraph reading/);
  assert.equal($('meta[property="og:description"]').content, description);
  assert.equal($('meta[name="twitter:description"]').content, description);
  assert.equal($('meta[property="og:title"]').content, d.title);
  assert.equal($('link[rel="canonical"]').href, 'https://ekguru.shop/learn/hindi/practice/');
  assert.doesNotMatch($('meta[name="robots"]').content, /noindex/);
});
test('ordered Foundation through C2; each stage ends in connected reading', () => {
  assert.equal(items[0].level,'Foundation'); assert.equal(items[0].kind,'letter');
  assert.equal(items.at(-1).level,'C2'); assert.equal(items.at(-1).kind,'paragraph');
  let rank = -1;
  for (const item of items) { const next = data.levels.indexOf(item.level); assert.ok(next>=rank); rank=next; }
  for (const stage of data.levels) assert.equal(items.filter(x=>x.level===stage).at(-1).kind, 'paragraph');
});
test('every source lesson exists including its fragment; no held half-step expansion', () => {
  const sourceCache = new Map();
  for (const item of items) {
    const url = new URL(item.source, w.location.href), rel = url.pathname.slice(1) + 'index.html';
    if (!sourceCache.has(rel)) sourceCache.set(rel, read(rel));
    if (url.hash) assert.ok(sourceCache.get(rel).includes('id="' + url.hash.slice(1) + '"'), item.source);
    assert.ok(!/\+|level\/(?:a3|b3|c3|c4|c5)/.test(item.source));
  }
});
test('initialisation needs neither network, audio autoplay nor a new progress store', () => {
  assert.equal($('#hll-app').hidden,false); assert.equal($('#hll-loading').hidden,true);
  assert.equal(spoken.length,0); assert.equal(w.localStorage.length,0);
  assert.equal($('#hll-previous').disabled,true); assert.equal($('#hll-next').disabled,false);
  w.eval(read('js/hindi-learning-library.js')); assert.equal(all('#hll-card h3').length,1);
  assert.doesNotMatch(read('js/hindi-learning-library.js'), /fetch\(|XMLHttpRequest|localStorage|sessionStorage|speechSynthesis/);
});
test('Listen uses exact current Hindi through shared voice with explicit availability', () => {
  clickText('Listen in Hindi'); assert.equal(spoken.at(-1).text,items[0].hi); assert.equal(spoken.at(-1).lang,'hi-IN');
  assert.equal($('[data-eg-voice-stop]').disabled,false);
  $('[data-eg-voice-stop]').click(); assert.equal($('[data-eg-voice-stop]').disabled,true);
});
test('filters/search have an honest empty state and navigation boundaries', () => {
  change('hll-level','C2'); change('hll-kind','letter');
  assert.equal($('#hll-empty').hidden,false); assert.equal($('#hll-card').hidden,true); assert.equal($('#hll-next').disabled,true);
  change('hll-kind','all'); change('hll-search','zzzznomatch'); assert.match($('#hll-position').textContent,/0 matching/);
  $('#hll-start').click(); assert.equal($('#hll-search').value,''); assert.equal($('#hll-level').value,'all');
  assert.equal($('#hll-card').dataset.itemId,items[0].id);
  change('hll-search','किताब'); assert.ok($('#hll-card').textContent.includes('किताब'));
  change('hll-search','book'); assert.match($('#hll-card').textContent.toLowerCase(),/book/);
});
function jumpTo(value) {
  $('#hll-number').value = String(value);
  $('#hll-jump').dispatchEvent(new w.Event('submit', { bubbles: true, cancelable: true }));
}
test('direct item navigation validates whole numbers, focuses item and respects filters', () => {
  $('#hll-start').click();
  for (const value of ['', '0', '-1', '1.5', String(items.length + 1)]) {
    jumpTo(value); assert.equal($('#hll-card').dataset.itemId, items[0].id);
    assert.equal($('#hll-number').getAttribute('aria-invalid'), 'true'); assert.equal(d.activeElement, $('#hll-number'));
    assert.match($('#hll-jump-note').textContent, /Not moved/);
  }
  jumpTo(items.length); assert.equal($('#hll-card').dataset.itemId, items.at(-1).id);
  assert.equal(d.activeElement, $('#hll-card')); assert.equal($('#hll-next').disabled, true);
  assert.equal($('#hll-number').hasAttribute('aria-invalid'), false);
  change('hll-level', 'A1'); change('hll-kind', 'paragraph');
  assert.equal($('#hll-number').max, '2'); jumpTo(2); assert.match($('#hll-position').textContent, /2 of 2/);
  change('hll-search', 'zzzznomatch'); assert.equal($('#hll-number').disabled, true); assert.equal($('#hll-jump button').disabled, true);
  $('#hll-start').click(); assert.equal($('#hll-number').disabled, false); assert.equal($('#hll-number').value, '1');
  assert.equal(w.localStorage.length, 0);
});
test('word meaning practice supports feedback/retry/clear across all seven stages', () => {
  $('#hll-start').click(); change('hll-kind', 'word');
  for (const level of data.levels) {
    change('hll-level', level);
    const item = items.find(x => x.id === $('#hll-card').dataset.itemId);
    const labels = all('.hll-meaning label'), glosses = labels.map(x => x.textContent);
    assert.equal(labels.length, 4); assert.equal(new Set(glosses.map(x => x.trim().toLowerCase())).size, 4);
    assert.equal(glosses.filter(x => x === item.en).length, 1);
    clickText('Check meaning'); assert.match($('.hll-meaning [role="status"]').textContent, /choose a meaning first/);
    labels.find(x => x.textContent !== item.en).querySelector('input').click();
    clickText('Check meaning'); assert.match($('.hll-meaning [role="status"]').textContent, /not the gloss/);
    labels.find(x => x.textContent === item.en).querySelector('input').click();
    clickText('Check meaning'); assert.match($('.hll-meaning [role="status"]').textContent, /Matched the source meaning/);
    clickText('Clear meaning choice'); assert.equal(all('.hll-meaning input:checked').length, 0);
    assert.equal(d.activeElement, $('.hll-meaning input'));
    $('#hll-next').click(); assert.equal(all('.hll-meaning input:checked').length, 0);
  }
  assert.equal(w.localStorage.length, 0);
});
test('every vocabulary item has one exact source gloss and nonduplicate choices', () => {
  $('#hll-start').click(); change('hll-kind', 'word');
  const vocab = items.filter(x => x.kind === 'word');
  for (let i = 0; i < vocab.length; i++) {
    jumpTo(i + 1);
    assert.equal($('#hll-card').dataset.itemId, vocab[i].id);
    const glosses = all('.hll-meaning label').map(x => x.textContent.trim().normalize('NFC').toLowerCase());
    assert.equal(glosses.length, 4); assert.equal(new Set(glosses).size, 4);
    for (let a = 0; a < glosses.length; a++) for (let b = a + 1; b < glosses.length; b++) {
      assert.ok(!glosses[a].includes(glosses[b]) && !glosses[b].includes(glosses[a]), 'Avoid overlapping gloss variants');
    }
    assert.equal(glosses.filter(x => x === vocab[i].en.trim().normalize('NFC').toLowerCase()).length, 1);
  }
});
test('sentence building is keyboard-native, keeps graphemes and is unscored', () => {
  $('#hll-start').click(); change('hll-kind','sentence');
  const item=items.find(x=>x.id===$('#hll-card').dataset.itemId), words=item.hi.split(/\s+/);
  clickText('Check model'); assert.match($('.hll-build [role="status"]').textContent,/Not checked/);
  for (let i=0;i<words.length;i++) { const b=$(`.hll-tiles button[data-word="${i}"]`); b.focus(); b.click(); assert.equal(d.activeElement,b); }
  assert.equal($('.hll-preview').textContent,item.hi); clickText('Check model'); assert.match($('.hll-build [role="status"]').textContent,/You built/);
  clickText('Clear words'); assert.equal(all('.hll-tiles button[aria-pressed="true"]').length,0);
  all('.hll-tiles button').forEach(b=>b.click()); clickText('Check model'); assert.match($('.hll-build [role="status"]').textContent,/differs/);
  const b=$('.hll-tiles button'); b.click(); assert.equal(b.getAttribute('aria-pressed'),'false');
});
test('paragraph room contains 14 graded passages, full and per-sentence Listen', () => {
  $('#hll-readings').click(); assert.match($('#hll-position').textContent,/1 of 14/);
  const first=items.find(x=>x.id===$('#hll-card').dataset.itemId);
  clickText('Listen to the whole paragraph'); assert.equal(spoken.at(-1).text,first.hi);
  clickText('Listen to sentence 1'); assert.equal(spoken.at(-1).text,first.hi.split('।')[0]+'।');
  assert.ok($('#hll-response')); assert.match($('#hll-card').textContent,/not automatic marking/);
  change('hll-level','C2'); assert.match($('#hll-position').textContent,/1 of 2/);
  $('#hll-next').click(); assert.equal($('#hll-next').disabled,true); assert.equal(d.activeElement,$('#hll-card'));
});
test('review explicitly uses the existing Hindi deck, deduplicates and survives reload', () => {
  clickText('Add this item to my Hindi review'); assert.equal(w.EkGuruGlobalSRS.count('hi'),1);
  clickText('Add this item to my Hindi review'); assert.equal(w.EkGuruGlobalSRS.count('hi'),1); assert.match($('#hll-card').textContent,/already in your Hindi/);
  assert.equal(w.localStorage.key(0),'ekguru:srs:hi:v1');
  const before=w.localStorage.getItem('ekguru:srs:hi:v1'); w.eval(read('js/global-srs.js'));
  assert.equal(w.localStorage.getItem('ekguru:srs:hi:v1'),before);
});
test('corrupt review data is preserved; UI cannot claim a save', () => {
  w.localStorage.setItem('ekguru:srs:hi:v1','{bad');
  clickText('Add this item to my Hindi review'); assert.equal(w.localStorage.getItem('ekguru:srs:hi:v1'),'{bad'); assert.match($('#hll-card').textContent,/Not added/);
});
test('no-voice condition remains readable, with honest unavailability and no synthesis', () => {
  w.speechSynthesis.getVoices=()=>[]; $('#hll-start').click();
  const b=$('#hll-card [data-voice-text]'); assert.equal(b.getAttribute('aria-disabled'),'true');
  const count=spoken.length; b.click(); assert.equal(spoken.length,count); assert.match($('[data-eg-voice-status]').textContent,/no Hindi voice/);
  assert.ok($('.hll-hindi').textContent); assert.ok(all('#hll-card details').length>=2);
});
test('no-JS paragraph fallback, existing labs, hidden and reduced-motion rules remain', () => {
  const html=read('learn/hindi/practice/index.html');
  assert.match(html,/<noscript>[\s\S]*?editorial|<noscript>[\s\S]*?मूल मसौदे/);
  for (const href of ['typing/','quiz/','worksheets/','conversation/','../review/','../my-progress/']) assert.ok(html.includes('href="'+href+'"'));
  const css=read('css/hindi-learning-library.css'); assert.match(css,/\.hll \[hidden\]\{display:none!important\}/); assert.match(css,/prefers-reduced-motion:reduce/);
  assert.ok(read('learn/hindi-sentence-structure/index.html').includes('../hindi/practice/#hindi-learning-library'));
  assert.ok(read('learn/hindi/index.html').includes('href="practice/#hindi-learning-library"'));
});
console.log(`${passed} Hindi collection checks passed; ${items.length} distinct learning items`);
dom.window.close();
