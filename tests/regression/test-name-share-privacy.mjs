// Exercise actual share handlers: the requested share URL may contain a name,
// but analytics must receive only a low-cardinality script label, never names.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM } from 'jsdom';
const read = p => readFileSync(new URL('../../' + p, import.meta.url), 'utf8');
for (const [slug, script] of [['hindi', 'devanagari'], ['punjabi', 'gurmukhi'], ['arabic', 'arabic']]) {
  for (const mechanism of ['clipboard', 'share']) {
    const dom = new JSDOM(read('name-in-' + slug + '/index.html'), {
      url: 'https://ekguru.shop/name-in-' + slug + '/', runScripts: 'outside-only'
    });
    const w = dom.window, d = w.document;
    if (d.readyState === 'loading') await new Promise(resolve => d.addEventListener('DOMContentLoaded', resolve, { once: true }));
    const events = [], shared = [];
    w.EkGuruAnalytics = { event: (...args) => events.push(args) };
    if (mechanism === 'share') w.navigator.share = async payload => shared.push(payload.url);
    else Object.defineProperty(w.navigator, 'clipboard', { value: { writeText: async text => shared.push(text) } });
    for (const file of ['js/translit.js', 'js/non-indic-scripts.js', 'js/names-data.js', 'js/script-map.js']) w.eval(read(file));
    if (slug === 'hindi') {
      const controller = [...d.querySelectorAll('script:not([src])')].find(s => s.textContent.includes('function shareUrlFor'));
      assert.ok(controller, 'actual inline Hindi controller found');
      w.eval(controller.textContent);
    } else w.eval(read('js/name-in-script.js'));
    // Several names prove event cardinality is not tied to user input.
    for (const name of ['Sarah', 'Michael']) {
      const input = d.getElementById('nameIn');
      input.value = name;
      input.dispatchEvent(new w.Event('input'));
      await new Promise(resolve => w.setTimeout(resolve, 120));
      d.getElementById('shareLinkBtn').click();
      await Promise.resolve();
      assert.equal(new URL(shared.at(-1)).searchParams.get('n'), name, 'user-requested share remains functional');
      assert.deepEqual(events.at(-1), ['name_share', script]);
      assert.ok(!JSON.stringify(events).includes(name), 'no typed name in any analytics call');
    }
    assert.equal(events.filter(e => e[0] === 'name_share').length, 2);
    w.close();
    console.log(`PASS ${slug} ${mechanism}: share works, typed names stay out of analytics`);
  }
}
