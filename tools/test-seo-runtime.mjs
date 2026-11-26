/* Static landing metadata must survive the legacy SEO runtime unchanged.
   jsdom DOM execution only; not a real-browser or ranking measurement. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM } from 'jsdom';

const read = path => readFileSync(new URL('../' + path, import.meta.url), 'utf8');
const paths = ['hindi-classes/', 'hindi-tutor-near-me/', 'learn/hindi/', 'name-in-hindi/', 'tutor/neha-sharma/', 'es/hindi/', 'about/'];
for (const path of paths) {
  const dom = new JSDOM(read(path + 'index.html'), {
    url: 'https://ekguru.shop/' + path, runScripts: 'outside-only'
  });
  const { window } = dom;
  window.EKGURU_SITE = { baseUrl: 'https://ekguru.shop/', brand: 'EkGuru' };
  window.EKGURU_MARKETS = [{ code: 'en', locale: 'en-US' }, { code: 'es', locale: 'es-ES' }];
  const before = window.document.head.innerHTML;
  window.eval(read('js/seo.js'));
  assert.equal(window.document.head.innerHTML, before, path + ': no unrelated home metadata injected');
  console.log('PASS static metadata survives SEO runtime:', path);
  window.close();
}
// The guard must not disable the legacy pages it actually owns.
for (const path of ['', 'es/']) {
  const dom = new JSDOM(read(path + 'index.html'), { url: 'https://ekguru.shop/' + path, runScripts: 'outside-only' });
  const { window } = dom;
  window.EKGURU_SITE = { baseUrl: 'https://ekguru.shop/', brand: 'EkGuru' };
  window.EKGURU_MARKETS = [{ code: 'en', locale: 'en-US' }, { code: 'es', locale: 'es-ES' }];
  window.eval(read('js/i18n.js'));
  window.eval(read('js/seo.js'));
  assert.equal(window.document.querySelector('link[rel="canonical"]').href, 'https://ekguru.shop/' + path);
  assert.ok(window.document.querySelector('link[hreflang="x-default"]'));
  console.log('PASS original homepage SEO runtime:', path || '/');
  window.close();
}
