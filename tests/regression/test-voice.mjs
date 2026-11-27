#!/usr/bin/env node
/* The real production bundle in jsdom with mocked device voices/audio/microphone. Mocks are not proof of device coverage. */
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { JSDOM, VirtualConsole } from 'jsdom';
const read = (f) => readFileSync(f, 'utf8');
let checks = 0;
const ok = (name, fn) => { fn(); checks++; console.log('PASS ' + name); };
const PAGE = '<!doctype html><html lang="en" data-learning-language="hi"><body><main><p lang="hi"><span>नमस्ते</span><button type="button" class="eg-voice" hidden data-voice-text="नमस्ते" data-voice-lang="hi" aria-label="Play नमस्ते in Hindi"></button></p><details class="voice-settings"><label>Voice<select data-eg-voice-picker="hi"></select></label><label>Speed<select data-eg-voice-rate><option value="0.6">0.6</option><option value="0.8">0.8</option><option value="1">1</option></select></label><button type="button" data-eg-voice-slow>Slow</button><button type="button" data-eg-voice-repeat>Repeat</button><button type="button" data-eg-voice-stop>Stop</button><p data-eg-voice-status role="status"></p></details></main></body></html>';
function device(voices = [], html = PAGE) {
  const dom = new JSDOM(html, { url: 'https://ekguru.shop/languages/hi/', runScripts: 'outside-only', pretendToBeVisual: true, virtualConsole: new VirtualConsole() });
  const w = dom.window, d = w.document, state = { voices, speech: [], cancels: 0, audio: [], changed: null };
  Object.defineProperty(d, 'readyState', { value: 'complete' });
  w.SpeechSynthesisUtterance = function (t) { this.text = t; };
  w.speechSynthesis = { getVoices: () => state.voices, speak: (u) => state.speech.push(u), cancel: () => { state.cancels++; }, addEventListener: (e, f) => { if (e === 'voiceschanged') state.changed = f; } };
  w.Audio = function (url) { this.url = url; this.play = () => { state.audio.push(this); return Promise.resolve(); }; this.pause = () => { this.paused = true; }; };
  w.eval(read('js/voice-languages.js')); w.eval(read('js/voice.js'));
  return { w, d, state, V: w.EkGuruVoice, btn: () => d.querySelector('.eg-voice'), status: () => d.querySelector('[data-eg-voice-status]').textContent, close: () => w.close() };
}
const v = (lang, uri = lang, extra = {}) => ({ name: 'Fixture ' + uri, lang, voiceURI: uri, localService: true, ...extra });
{
  const t = device([v('en-US'), v('hi-IN', 'hi-1'), v('hi-IN', 'hi-2'), v('ko-KR'), v('ur-PK'), v('ne-NP')]);
  ok('nothing speaks or plays at boot (no autoplay)', () => { assert.equal(t.state.speech.length, 0); assert.equal(t.state.audio.length, 0); });
  ok('the server-rendered hidden placeholder is enabled with its exact label and is not disabled', () => { assert.equal(t.btn().hidden, false); assert.equal(t.btn().getAttribute('aria-label'), 'Play नमस्ते in Hindi'); assert.equal(t.btn().getAttribute('aria-disabled'), null); });
  ok('the picker lists only Hindi voices — never English, Korean, Urdu or Nepali', () => { assert.deepEqual([...t.d.querySelectorAll('[data-eg-voice-picker] option')].map((o) => o.value), ['hi-1', 'hi-2']); assert.equal(t.V.voices('hi').every((x) => x.lang === 'hi-IN'), true); });
  ok('a preference persists per language and is used; another language voice is refused', () => { assert.equal(t.V.prefer('hi', 'ko-KR'), false); assert.equal(t.V.prefer('hi', 'hi-2'), true); assert.equal(t.w.localStorage.getItem('ekguru:voice:hi'), 'hi-2'); t.btn().click(); assert.equal(t.state.speech.at(-1).voice.voiceURI, 'hi-2'); assert.equal(t.state.speech.at(-1).lang, 'hi-IN'); assert.equal(t.state.speech.at(-1).rate, 0.8); });
  ok('speech starts only from a click and is labelled synthetic, not a native recording', () => { assert.match(t.status(), /^Synthetic voice — Fixture hi-2 \(hi-IN\)\. Not a native recording\./); });
  ok('pressed state follows playback and resets on end', () => { assert.equal(t.btn().getAttribute('aria-pressed'), 'true'); t.state.speech.at(-1).onend(); assert.equal(t.btn().getAttribute('aria-pressed'), 'false'); });
  ok('slow and repeat reuse the last item and language; stop cancels', () => { const n = t.state.speech.length; t.d.querySelector('[data-eg-voice-slow]').click(); assert.equal(t.state.speech.length, n + 1); assert.equal(t.state.speech.at(-1).rate, 0.6); t.d.querySelector('[data-eg-voice-repeat]').click(); assert.equal(t.state.speech.at(-1).rate, 0.8); t.d.querySelector('[data-eg-voice-stop]').click(); assert.equal(t.btn().getAttribute('aria-pressed'), 'false'); assert.ok(t.state.cancels > 0); });
  ok('speed select persists 0.6 / 0.8 / 1 and rejects out-of-range values', () => { const s = t.d.querySelector('[data-eg-voice-rate]'); s.value = '1'; s.dispatchEvent(new t.w.Event('change', { bubbles: true })); assert.equal(t.V.rate(), 1); assert.equal(t.w.localStorage.getItem('ekguru:voice:rate'), '1'); assert.equal(t.V.setRate(9), false); });
  ok('an engine error resets the control and says so, never switching language', () => { t.btn().click(); const u = t.state.speech.at(-1); u.onerror(); assert.equal(t.btn().getAttribute('aria-pressed'), 'false'); assert.match(t.status(), /Playback could not start or finish/); assert.equal(u.voice.lang, 'hi-IN'); });
  ok('empty, overlong and malformed requests are refused', () => { assert.equal(t.V.speak('', 'hi'), false); assert.equal(t.V.speak('a'.repeat(2001), 'hi'), false); assert.equal(t.V.speak('x', 'not a language!!'), false); });
  ok('legacy controls delegate to the same provider without nesting a second button', () => { const b = t.d.createElement('button'); b.setAttribute('data-sb-say', 'क'); b.innerHTML = 'क<small>ka</small>'; t.d.querySelector('main').appendChild(b); const n = t.state.speech.length; t.V.mount(); b.click(); assert.equal(t.state.speech.length, n + 1); assert.equal(t.state.speech.at(-1).text, 'क'); assert.equal(b.querySelectorAll('button').length, 0); const s = t.d.createElement('span'); s.className = 'spk'; s.textContent = 'पानी'; t.d.querySelector('main').appendChild(s); s.click(); assert.equal(t.state.speech.at(-1).text, 'पानी'); });
  ok('mounting repeatedly does not duplicate controls or double-speak', () => { const count = t.d.querySelectorAll('.eg-voice').length; t.V.mount(); t.V.mount(); assert.equal(t.d.querySelectorAll('.eg-voice').length, count); const n = t.state.speech.length; t.btn().click(); assert.equal(t.state.speech.length, n + 1); });
  t.close();
}
{
  const t = device([v('en-US'), v('ne-NP'), v('ur-PK')]);
  ok('no Hindi voice: control is aria-disabled, nothing speaks, the exact honest text is exposed', () => { assert.equal(t.btn().getAttribute('aria-disabled'), 'true'); assert.equal(t.btn().title, 'Your browser has no Hindi voice. Romanisation is shown instead.'); t.btn().click(); assert.equal(t.state.speech.length, 0); assert.equal(t.status(), 'Your browser has no Hindi voice. Romanisation is shown instead.'); assert.equal(t.V.available('hi'), false); });
  ok('related languages (Nepali, Urdu) are never used as a Hindi voice', () => { assert.equal(t.V.voices('hi').length, 0); assert.equal(t.V.speak('नमस्ते', 'hi'), false); assert.equal(t.d.querySelector('[data-eg-voice-picker] option').textContent, 'No matching voice on this device'); });
  ok('voiceschanged enables the control without autoplay', () => { t.state.voices = [v('hi-IN')]; t.state.changed(); assert.equal(t.btn().getAttribute('aria-disabled'), null); assert.equal(t.state.speech.length, 0); });
  t.close();
}
{
  const t = device([v('zh-HK', 'cantonese')], PAGE.replace('data-learning-language="hi"', 'data-learning-language="zh"').replace(/data-voice-lang="hi"/, 'data-voice-lang="zh"'));
  ok('Cantonese zh-HK is not accepted for the Mandarin course; zh-CN is', () => { assert.equal(t.V.available('zh'), false); t.state.voices = [v('zh-CN', 'mandarin')]; assert.equal(t.V.available('zh'), true); });
  ok('a same-language regional voice is accepted and shown with its real tag', () => { const s = device([v('es-MX', 'mx')], PAGE.replace(/data-voice-lang="hi"/, 'data-voice-lang="es"').replace('data-eg-voice-picker="hi"', 'data-eg-voice-picker="es"')); assert.equal(s.V.available('es'), true); s.btn().click(); assert.match(s.status(), /\(es-MX\)/); s.close(); });
  t.close();
}
{
  const t = device([v('ku', 'kurdish-macro'), v('kmr', 'kurmanji'), v('ps', 'pashto-macro'), v('pbu', 'northern-pashto')]);
  ok('specific Kurdish and Northern Pashto tags retain registry values and match macro-language device aliases', () => {
    assert.equal(t.V.tagFor('ku'), 'kmr');
    assert.equal(t.V.tagFor('ps'), 'pbu');
    assert.deepEqual([...t.V.voices('ku')].map((x) => x.lang).sort(), ['kmr', 'ku']);
    assert.deepEqual([...t.V.voices('ps')].map((x) => x.lang).sort(), ['pbu', 'ps']);
  });
  t.close();
}
{
  const t = device([]);
  const rec = { text: 'नमस्ते', lang: 'hi-IN', url: '/audio/hi/namaste.mp3', kind: 'human', recorder: 'Fixture Recorder (test only)', license: 'CC-BY-4.0', source_url: 'https://example.com/test-fixture' };
  ok('a licensed same-language human recording is playable without any device voice and is attributed', () => { assert.equal(t.V.registerManifest({ lang: 'hi-IN', entries: [rec] }), 1); assert.equal(t.V.available('hi', 'नमस्ते'), true); t.btn().click(); assert.equal(t.state.audio.length, 1); assert.equal(t.state.speech.length, 0); assert.match(t.status(), /^Recorded by Fixture Recorder \(test only\) \(CC-BY-4\.0\)\./); });
  ok('unlicensed, remote, wrong-language, anonymous-human and unknown-license entries are rejected', () => { for (const patch of [{ license: '' }, { license: 'all-rights-reserved' }, { url: 'https://example.com/a.mp3' }, { url: '/audio/../x.mp3' }, { lang: 'en-US' }, { recorder: '' }, { source_url: 'http://x' }]) assert.equal(t.V.registerManifest({ lang: 'hi-IN', entries: [{ ...rec, ...patch }] }), 0, JSON.stringify(patch)); });
  ok('a synthetic recording is never described as human', () => { t.V.stop(); t.V.registerManifest({ lang: 'hi-IN', entries: [{ ...rec, kind: 'synthetic', recorder: null }] }); t.btn().click(); assert.match(t.status(), /^Synthetic voice/); });
  t.close();
}
{
  const dom = new JSDOM('<html lang="en" data-learning-language="hi"><body><section data-eg-speaking data-eg-language="hi"><button data-eg-microphone>Start</button><button data-eg-microphone-stop disabled>Stop</button><p data-eg-transcript>No microphone permission requested.</p></section></body></html>', { url: 'https://ekguru.shop/design/', runScripts: 'outside-only', virtualConsole: new VirtualConsole() });
  const w = dom.window; let started = 0, recognition; Object.defineProperty(w.document, 'readyState', { value: 'complete' });
  w.speechSynthesis = { getVoices: () => [], cancel() {}, addEventListener() {} }; w.eval(read('js/voice-languages.js')); w.eval(read('js/voice.js'));
  w.SpeechRecognition = function () { recognition = this; this.start = () => started++; this.stop = () => this.onend(); }; w.eval(read('js/speech-ui.js'));
  ok('the microphone is not started or requested on load', () => assert.equal(started, 0));
  ok('a click starts recognition in the language tag; the result is a sanitised transcript, never a score', () => { w.document.querySelector('[data-eg-microphone]').click(); assert.equal(started, 1); assert.equal(recognition.lang, 'hi-IN'); assert.equal(recognition.continuous, false); recognition.onresult({ results: [[{ transcript: '<script>alert(1)</script>' }]] }); const out = w.document.querySelector('[data-eg-transcript]'); assert.match(out.textContent, /We heard: .*transcript only, not a pronunciation score/); assert.equal(out.querySelectorAll('script').length, 0); recognition.onend(); assert.equal(w.document.querySelector('[data-eg-microphone]').disabled, false); });
  w.close();
  const none = new JSDOM('<html lang="en" data-learning-language="hi"><body><section data-eg-speaking><button data-eg-microphone>Start</button><p data-eg-transcript></p></section></body></html>', { url: 'https://ekguru.shop/', runScripts: 'outside-only', virtualConsole: new VirtualConsole() });
  Object.defineProperty(none.window.document, 'readyState', { value: 'complete' }); none.window.eval(read('js/voice-languages.js')); none.window.eval(read('js/voice.js')); none.window.eval(read('js/speech-ui.js'));
  ok('without SpeechRecognition the control says so honestly', () => assert.match(none.window.document.querySelector('[data-eg-transcript]').textContent, /not available in this browser/)); none.window.close();
}
const CORE_VOICE_TAGS = {
  hi: 'hi-IN', bn: 'bn-IN', gu: 'gu-IN', mr: 'mr-IN', pa: 'pa-IN', ta: 'ta-IN', te: 'te-IN', ur: 'ur-PK',
  ar: 'ar-SA', fr: 'fr-FR', de: 'de-DE', es: 'es-ES', it: 'it-IT', ja: 'ja-JP', ko: 'ko-KR', pt: 'pt-BR',
  ru: 'ru-RU', zh: 'zh-CN',
};
ok('the 18 Phase 11 core course tags match the configured BCP-47 locale tags', () => {
  const rows = new Map(JSON.parse(read('data/languages/registry.json')).languages.map((r) => [r.code, r]));
  const w = new JSDOM('', { runScripts: 'outside-only' }).window;
  w.eval(read('js/voice-languages.js'));
  for (const [code, tag] of Object.entries(CORE_VOICE_TAGS)) {
    assert.ok(rows.get(code)?.course || rows.get(code)?.starter_pack, `${code} is published`);
    assert.equal(rows.get(code).speech_tag, tag, `${code} source tag`);
    assert.equal(w.EKGURU_VOICE_LANGUAGES[code]?.tag, tag, `${code} generated tag`);
  }
  w.close();
});
ok('every course, starter-pack and language-pack code matches its registry tag and manifest', () => {
  const rows = JSON.parse(read('data/languages/registry.json')).languages;
  const byCode = new Map(rows.map((r) => [r.code, r]));
  const expected = new Set(rows.filter((r) => r.course || r.starter_pack).map((r) => r.code));
  for (const p of JSON.parse(read('data/language-packs.json')).packs) if (byCode.has(p.lang)) expected.add(p.lang);
  const w = new JSDOM('', { runScripts: 'outside-only' }).window;
  w.eval(read('js/voice-languages.js'));
  const languages = w.EKGURU_VOICE_LANGUAGES;
  for (const code of expected) {
    const row = byCode.get(code), entry = languages[code];
    assert.ok(entry, `${code} is in the generated map`);
    assert.equal(entry.tag, row.speech_tag, `${code} matches its registry tag`);
    assert.equal(entry.name, row.name, `${code} matches its registry name`);
    assert.match(entry.tag, /^[A-Za-z]{2,8}(-[A-Za-z0-9]{1,8})*$/, `${code} tag shape`);
    assert.equal(Intl.getCanonicalLocales(entry.tag).length, 1, `${code} parses as a BCP-47 locale`);
    const manifest = JSON.parse(read(`data/audio-manifest/${code}.json`));
    assert.equal(manifest.lang, row.speech_tag, `${code} manifest language tag`);
    assert.ok(Array.isArray(manifest.entries), `${code} recording entries`);
  }
  let checkedAliases = 0;
  const codeMap = JSON.parse(read('data/global/language-code-map.json')).canonical_course_codes;
  for (const [canonical, details] of Object.entries(codeMap)) {
    if (!languages[canonical]) continue;
    for (const alias of details.aliases || []) {
      if (alias.length !== 2 || alias === canonical) continue;
      assert.deepEqual(languages[alias], languages[canonical], `${alias} uses ${canonical}'s voice tag`);
      checkedAliases++;
    }
  }
  assert.ok(checkedAliases > 0, 'legacy two-letter aliases are exercised');
  w.close();
});
ok('voice.js stays within its 10KB budget and is the only speech engine in js/', () => { assert.ok(Buffer.byteLength(read('js/voice.js')) <= 10 * 1024); for (const f of readdirSync('js').filter((n) => n.endsWith('.js') && n !== 'voice.js')) { const t = read('js/' + f); assert.doesNotMatch(t, /new\s+(?:window\.)?SpeechSynthesisUtterance|speechSynthesis\.speak\s*\(|translate_tts|translate\.googleapis/, f); } });
ok('known listening autoplay regression is absent', () => assert.doesNotMatch(read('js/practice-engine.js'), /play once on load/));
console.log(`PASS voice ${checks}/${checks} (mocked devices; not Android/iOS/desktop voice availability evidence)`);
