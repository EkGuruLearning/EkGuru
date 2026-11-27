// DOM unit checks use mocked canvas APIs; a real PNG is tested in Playwright.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM } from 'jsdom';
const read = p => readFileSync(new URL('../../' + p, import.meta.url), 'utf8');
async function setup(mode = 'ok') {
  const dom = new JSDOM(read('name-in-hindi/index.html'), { url: 'https://ekguru.shop/name-in-hindi/', runScripts: 'outside-only' });
  const w = dom.window, d = w.document;
  if (d.readyState === 'loading') await new Promise(r => d.addEventListener('DOMContentLoaded', r, { once: true }));
  const drawn = [], downloads = [], urls = [];
  w.FontFace = class {
    constructor(name, src) {
      assert.equal(name, 'EkGuruCardDevanagari');
      assert.equal(src, 'url(/images/fonts/noto-sans-devanagari-700.woff2)');
    }
    load() { return mode === 'font-error' ? Promise.reject(Error('font unavailable')) : Promise.resolve(this); }
  };
  Object.defineProperty(d, 'fonts', { value: { add() {} } });
  w.HTMLCanvasElement.prototype.getContext = () => mode === 'unsupported' ? null : ({
    createLinearGradient: () => ({ addColorStop() {} }), fillRect() {},
    fillText: text => drawn.push(text), measureText: text => ({ width: text.length * 12 })
  });
  w.HTMLCanvasElement.prototype.toBlob = function (callback, type) {
    assert.equal(this.width, 1200); assert.equal(this.height, 630); assert.equal(type, 'image/png');
    callback(mode === 'no-blob' ? null : new w.Blob(['mock'], { type }));
  };
  w.URL.createObjectURL = blob => { assert.equal(blob.type, 'image/png'); urls.push('blob:local'); return 'blob:local'; };
  w.URL.revokeObjectURL = () => {};
  w.HTMLAnchorElement.prototype.click = function () { downloads.push({ href: this.href, filename: this.download }); };
  w.fetch = () => { throw Error('card code must never fetch'); };
  w.EkGuruAnalytics = { event() { throw Error('card code must not send typed names'); } };
  w.eval(read('js/name-card.js'));
  w.eval(read('js/name-card.js')); // duplicate loads cannot bind twice
  return { dom, w, d, drawn, downloads, urls };
}
const tick = () => new Promise(r => setTimeout(r, 0));
{
  const { w, d, drawn, downloads, urls } = await setup();
  const button = d.getElementById('downloadNameCard');
  button.click(); await tick();
  assert.equal(downloads.length, 0);
  assert.match(d.getElementById('name-card-status').textContent, /Type a name/);
  d.getElementById('nameIn').value = 'Sarah';
  d.querySelector('#out .big').textContent = 'सारा';
  button.click(); await tick();
  assert.equal(downloads.length, 1);
  assert.deepEqual(downloads[0], { href: 'blob:local', filename: 'ekguru-name-card.png' });
  assert.deepEqual(urls, ['blob:local']);
  assert.ok(drawn.includes('Sarah') && drawn.includes('सारा'));
  assert.ok(drawn.includes('Transliteration · spelling may vary'));
  assert.match(d.getElementById('name-card-status').textContent, /download started/);
  assert.equal(button.disabled, false);
  w.close();
  console.log('PASS name card draws a local 1200×630 PNG, keeps full result and binds once');
}
for (const mode of ['unsupported', 'no-blob', 'long-name', 'font-error']) {
  const { w, d, downloads } = await setup(mode);
  d.getElementById('nameIn').value = mode === 'long-name' ? 'A'.repeat(81) : 'Sarah';
  d.querySelector('#out .big').textContent = 'सारा';
  d.getElementById('downloadNameCard').click(); await tick();
  assert.equal(downloads.length, 0);
  assert.equal(d.getElementById('downloadNameCard').disabled, false);
  assert.match(d.getElementById('name-card-status').textContent, /Could not|shorter names/);
  w.close();
  console.log('PASS card failure is recoverable, no silent truncation: ' + mode);
}
