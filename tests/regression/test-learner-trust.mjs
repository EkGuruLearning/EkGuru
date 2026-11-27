// Source/DOM regression only: not evidence of native review, traffic or bookings.
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { JSDOM } from 'jsdom';
const read = p => readFileSync(new URL('../../' + p, import.meta.url), 'utf8');
const open = p => new JSDOM(read(p), { url: 'https://ekguru.shop/' + p, runScripts: 'outside-only' });
for (const path of ['learn/index.html', 'learn/hindi/index.html']) {
  const dom = open(path), d = dom.window.document;
  const offer = d.querySelector('[data-eg-hindi-help]');
  assert.ok(offer, path + ': optional help is server-rendered, not a popup');
  assert.ok(d.getElementById(offer.getAttribute('aria-labelledby')));
  assert.equal(offer.querySelectorAll('ol li').length, 3);
  assert.match(offer.textContent, /not included/);
  assert.match(offer.textContent, /not a confirmed booking/);
  assert.match(offer.textContent, /does not collect tutor-lesson payments/);
  assert.match(offer.textContent, /If no suitable tutor is listed/);
  const cta = offer.querySelector('a.btn');
  assert.equal(cta.pathname, '/find-tutors.html');
  assert.equal(cta.textContent, 'Compare Hindi tutor profiles');
  assert.equal(offer.querySelectorAll('form,input').length, 0, 'no implicit newsletter subscription');
  for (const a of offer.querySelectorAll('a')) {
    const url = new URL(a.href);
    const rel = url.pathname.slice(1);
    assert.equal(url.origin, 'https://ekguru.shop');
    assert.ok(existsSync(new URL('../../' + (rel.endsWith('.html') ? rel : rel + 'index.html'), import.meta.url)));
  }
  assert.equal(d.querySelectorAll('h1').length, 1);
  dom.window.close();
  console.log('PASS clear optional Hindi tutoring and working free fallback: ' + path);
}
{
  const dom = open('learn/index.html'), d = dom.window.document;
  const nodes = [...d.querySelectorAll('script[type="application/ld+json"]')]
    .flatMap(s => { const j = JSON.parse(s.textContent); return j['@graph'] || [j]; });
  const collection = nodes.filter(n => n['@type'] === 'CollectionPage');
  assert.equal(collection.length, 1, 'one consistent library entity, not duplicate Hindi-only schema');
  assert.equal(collection[0].description, d.querySelector('meta[name="description"]').content);
  assert.equal(nodes.filter(n => n['@type'] === 'Course').length, 0, 'multilingual library is not one Hindi course');
  const list = nodes.find(n => n['@id'] === 'https://ekguru.shop/learn/#courses');
  const cards = [...d.querySelectorAll('.li-hindi, .li-card')];
  assert.equal(list.numberOfItems, cards.length);
  assert.deepEqual(list.itemListElement.map(n => n.url), cards.map(a => a.href));
  assert.ok(list.itemListElement.every(n => !/Complete|certif/i.test(n.name)));
  assert.match(d.querySelector('.lede').textContent, /Coverage varies/);
  assert.ok(d.querySelector('a[href="../editorial-policy/"]'));
  dom.window.close();
  console.log('PASS Learn schema matches visible language cards and review limits');
}
{
  const dom = open('about/index.html'), d = dom.window.document;
  const text = d.querySelector('main').textContent;
  assert.match(text, /free self-paced language materials/);
  assert.match(text, /independent Hindi tutors/);
  assert.match(text, /native-speaker review is not yet recorded/);
  assert.doesNotMatch(text, /hand-checked list|taught badly to almost/);
  const graph = JSON.parse(d.querySelector('script[type="application/ld+json"]').textContent)['@graph'];
  assert.equal(graph.find(n => n['@type'] === 'AboutPage').description, d.querySelector('meta[name="description"]').content);
  dom.window.close();
  console.log('PASS About distinguishes multilingual self-study from Hindi tutoring');
}
