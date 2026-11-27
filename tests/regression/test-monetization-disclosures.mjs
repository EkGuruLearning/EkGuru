// Public wording must describe the shipped code, not a hypothetical launch.
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { JSDOM } from 'jsdom';
const read = p => readFileSync(new URL('../../' + p, import.meta.url), 'utf8');
for (const path of ['privacy/index.html', 'cookie-policy/index.html', 'monetization-disclosure/index.html']) {
  const dom = new JSDOM(read(path));
  dom.window.document.querySelectorAll('script,style').forEach(n => n.remove());
  const text = dom.window.document.body.textContent;
  assert.match(text, /review loader/i, path);
  assert.match(text, /Advertising is disabled|runtime ad units.*disabled|runtime ad units remain disabled/i, path);
  assert.match(text, /not a Google-certified CMP\/TCF/, path);
  assert.doesNotMatch(text, /no AdSense loader|Public pages contain no|Public HTML contains no|denied by default|only after consent|not requested unless you allow/i, path);
  assert.ok(!dom.window.document.querySelector('script[src*="adsbygoogle"]'), 'legal pages remain loader-free');
  dom.window.close();
  console.log('PASS review-loader versus disabled-runtime disclosure: ' + path);
}
const privacy = read('privacy/index.html'), cookies = read('cookie-policy/index.html');
for (const html of [privacy, cookies]) {
  assert.match(html, /by default/);
  assert.match(html, /Only essential/);
  assert.match(html, /Global Privacy Control/);
  assert.match(html, /Doing nothing/);
}
assert.match(privacy, /does not subscribe you to marketing/);
assert.match(privacy, /Google Input Tools/);
assert.match(read('js/cookie-consent.js'), /ADVERTISING_AVAILABLE = false/);
assert.match(read('js/monetization.js'), /ADS_RUNTIME_ENABLED = false/);
assert.match(read('index.html'), /adsbygoogle\.js/);
console.log('PASS policy wording matches opt-out analytics, request-only email and disabled ad gates');
function walk(dir) {
  return readdirSync(new URL('../../' + dir, import.meta.url), { withFileTypes: true })
    .flatMap(e => e.isDirectory() ? walk(dir + '/' + e.name) : e.name.endsWith('.html') ? [dir + '/' + e.name] : []);
}
const tools = walk('toolbox'), materials = walk('materials');
for (const path of [...tools, ...materials, 'name-in-hindi/index.html']) {
  const dom = new JSDOM(read(path), { url: 'https://ekguru.shop/' + path });
  assert.ok([...dom.window.document.querySelectorAll('a[href]')].some(a => a.href === 'https://ekguru.shop/support/'), path + ': static support link, works without JS');
  dom.window.close();
}
console.log(`PASS static support coverage: ${tools.length} toolbox + ${materials.length} materials + Hindi name tool`);
const sellerLines = read('ads.txt').split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'));
assert.deepEqual(sellerLines, ['google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0']);
console.log('PASS ads.txt retains exactly one authorized DIRECT record');
