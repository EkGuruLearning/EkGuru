/* Static landing metadata must survive the legacy SEO runtime unchanged.
   jsdom DOM execution only; not a real-browser or ranking measurement. */
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
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
  assert.equal(window.document.querySelector('link[hreflang="x-default"]').href, 'https://ekguru.shop/');
  assert.equal(window.document.querySelector('link[hreflang="en"]').href, 'https://ekguru.shop/');
  assert.equal(window.document.querySelector('link[hreflang="es"]').href, 'https://ekguru.shop/es/');
  console.log('PASS original homepage SEO runtime:', path || '/');
  window.close();
}

// Country-independent language fallbacks must survive runtime rendering.
// These are the seven existing translations, not fabricated country pages.
let internationalCases = 0;
const browsers = ['en-IN', 'es-MX', 'pt-PT', 'ar-SA'];
const targetCanonicals = new Map();
function targetCanonical(href) {
  if (!targetCanonicals.has(href)) {
    const target = new URL(href).pathname.slice(1) || 'index.html';
    const rel = target.endsWith('/') ? target + 'index.html' : target;
    assert.ok(existsSync(new URL('../' + rel, import.meta.url)), `${href}: real translation`);
    const targetDom = new JSDOM(read(rel));
    targetCanonicals.set(href, targetDom.window.document.querySelector('link[rel="canonical"]').href);
    targetDom.window.close();
  }
  return targetCanonicals.get(href);
}
for (const browserLanguage of browsers) {
  for (const file of ['index.html', 'find-tutors.html', 'join.html']) {
    for (const selected of ['en', 'es', 'fr', 'de', 'pt', 'ja', 'ar']) {
      const dom = new JSDOM(read(file), {
        url: 'https://ekguru.shop/' + (file === 'index.html' ? '' : file) + '?lang=' + selected,
        runScripts: 'outside-only'
      });
      const { window } = dom, d = window.document;
      Object.defineProperty(window.navigator, 'language', { value: browserLanguage });
      window.eval(read('js/site-config.js'));
      window.eval(read('js/i18n.js'));
      window.eval(read('js/seo.js'));
      const markets = window.EKGURU_MARKETS;
      const fileName = file === 'index.html' ? '' : file;
      const fallback = 'https://ekguru.shop/' + fileName;
      const canonical = 'https://ekguru.shop/' + (selected === 'en' ? '' : selected + '/') + fileName;
      assert.equal(d.querySelector('link[rel="canonical"]').href, canonical);
      assert.equal(d.querySelector('link[hreflang="x-default"]').href, fallback);
      assert.equal(window.EKGURU_LANG, selected, 'explicit learner choice still works');
      for (const m of markets) {
        const expected = 'https://ekguru.shop/' + (m.code === 'en' ? '' : m.code + '/') + fileName;
        for (const language of [m.code, m.locale]) {
          const links = [...d.querySelectorAll('link[hreflang]')].filter(e => e.hreflang === language);
          assert.equal(links.length, 1, `${file} ${selected}: one ${language} alternate`);
          assert.equal(links[0].href, expected);
          assert.equal(targetCanonical(expected), expected);
        }
      }
      // Re-running this metadata helper must not duplicate its locale set.
      window.eval(read('js/seo.js'));
      const alternateLocales = [...d.querySelectorAll('meta[property="og:locale:alternate"]')].map(e => e.content);
      assert.equal(alternateLocales.length, markets.length - 1);
      assert.equal(new Set(alternateLocales).size, alternateLocales.length);
      assert.equal(d.querySelectorAll('link[hreflang="x-default"]').length, 1);
      dom.window.close(); internationalCases++;
    }
  }
}
console.log(`PASS ${internationalCases} international runtime cases: real translated targets, generic/regional tags, stable default and locale deduplication`);

// No x-default="" (which resolves to the current URL) on the noindex shell.
{
  const dom = new JSDOM(read('tutor.html'), { url: 'https://ekguru.shop/tutor.html', runScripts: 'outside-only' });
  dom.window.eval(read('js/site-config.js'));
  dom.window.eval(read('js/seo.js'));
  assert.equal(dom.window.document.querySelector('link[rel="canonical"]'), null);
  assert.equal(dom.window.document.querySelector('link[hreflang="x-default"]'), null);
  assert.match(dom.window.document.querySelector('meta[name="robots"]').content, /noindex/);
  dom.window.close();
  console.log('PASS noindex shell stays noindex with no empty default or canonical');
}
