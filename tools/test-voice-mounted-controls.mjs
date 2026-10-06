#!/usr/bin/env node
/*
 * Mounted-control integration checks against generated/on-disk course and topic
 * HTML in jsdom with mocked speech voices. This checks DOM semantics and click
 * wiring, not native keyboard activation in a browser or assistive technology.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM, VirtualConsole } from 'jsdom';

const read = (path) => readFileSync(path, 'utf8');
const fixtures = [
  ['vocabulary', 'learn/marathi/vocabulary/index.html', 'mr'],
  ['dialogues', 'learn/marathi/practice/conversation/index.html', 'mr'],
  ['grammar/examples', 'learn/marathi/grammar/index.html', 'mr'],
  ['alphabet/pronunciation', 'learn/marathi/pronunciation/index.html', 'mr'],
  ['numbers', 'learn/marathi/numbers/index.html', 'mr'],
  ['Marathi and Hindi comparison', 'marathi/marathi-vs-hindi/index.html', 'mr'],
  ['Marathi topic hub', 'marathi/index.html', 'mr'],
];
let checks = 0;
function check(name, fn) {
  fn();
  checks++;
  console.log(`PASS ${name}`);
}
const deviceVoices = [
  { name: 'Fixture Marathi', lang: 'mr-IN', voiceURI: 'fixture-mr', localService: true },
  { name: 'Fixture Hindi', lang: 'hi-IN', voiceURI: 'fixture-hi', localService: true },
];

function mount(path, voices = deviceVoices) {
  const dom = new JSDOM(read(path), {
    url: `https://ekguru.shop/${path}`,
    runScripts: 'outside-only',
    pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),
  });
  const { window: w } = dom;
  const speech = [];
  Object.defineProperty(w.document, 'readyState', { value: 'complete' });
  w.SpeechSynthesisUtterance = function (text) { this.text = text; };
  w.speechSynthesis = {
    getVoices: () => voices,
    speak: (utterance) => speech.push(utterance),
    cancel() {},
    addEventListener() {},
  };
  w.eval(read('js/voice-languages.js'));
  w.eval(read('js/voice.js'));
  return { dom, window: w, document: w.document, speech, close: () => w.close() };
}

for (const [category, path, expectedLang] of fixtures) {
  const page = mount(path);
  const { document: d, speech } = page;
  const buttons = [...d.querySelectorAll('button[data-sb-say]')];
  check(`${category}: speaker controls render as named native buttons`, () => {
    assert.ok(buttons.length > 0, `${path} must contain speaker controls`);
    for (const button of buttons) {
      assert.equal(button.type, 'button', `${path}: avoid accidental form submission`);
      assert.ok(button.getAttribute('aria-label')?.trim(), `${path}: accessible name`);
      assert.equal(button.getAttribute('aria-pressed'), 'false', `${path}: idle state`);
    }
  });
  const selected = buttons.find((button) => button.getAttribute('data-voice-lang') === expectedLang);
  check(`${category}: click speaks the exact marked language and toggles aria-pressed`, () => {
    assert.ok(selected, `${path}: expected ${expectedLang} control`);
    assert.equal(speech.length, 0, 'mounting must not autoplay');
    selected.click();
    assert.equal(speech.length, 1, 'one activation should make one speech request');
    assert.equal(speech[0].text, selected.getAttribute('data-sb-say'));
    assert.equal(speech[0].voice.lang, expectedLang === 'mr' ? 'mr-IN' : 'hi-IN');
    assert.equal(selected.getAttribute('aria-pressed'), 'true');
    speech[0].onend();
    assert.equal(selected.getAttribute('aria-pressed'), 'false');
  });
  if (category === 'Marathi and Hindi comparison') {
    const hindi = buttons.find((button) => button.getAttribute('data-voice-lang') === 'hi');
    check('comparison: explicitly Hindi-labelled example selects Hindi, not Marathi', () => {
      assert.ok(hindi, 'comparison must have an explicitly Hindi control');
      hindi.click();
      assert.equal(speech.at(-1).text, hindi.getAttribute('data-sb-say'));
      assert.equal(speech.at(-1).voice.lang, 'hi-IN');
    });
  }
  page.close();
}

{
  const page = mount('learn/marathi/vocabulary/index.html', []);
  const button = page.document.querySelector('button[data-sb-say]');
  check('no matching device voice: control remains named, is marked unavailable, and does not speak', () => {
    assert.ok(button);
    assert.ok(button.getAttribute('aria-label'));
    assert.equal(button.getAttribute('aria-disabled'), 'true');
    assert.match(button.title, /no Marathi voice/i);
    button.click();
    assert.equal(page.speech.length, 0);
    assert.equal(button.getAttribute('aria-pressed'), 'false');
  });
  page.close();
}

{
  const path = 'languages/index.html';
  const source = read(path);
  const languageMapMatch = read('js/voice-languages.js').match(/window\.EKGURU_VOICE_LANGUAGES=(\{[^\n]*\});/);
  assert.ok(languageMapMatch, 'generated voice language map is present');
  const languageMap = JSON.parse(languageMapMatch[1]);
  const codes = [...new Set([...source.matchAll(/data-voice-lang="([^"]+)"/g)].map((m) => m[1]))];
  const tags = codes.map((code) => languageMap[code]?.tag || code);
  const voices = tags.map((lang, index) => ({
    name: `Fixture ${lang}`, lang, voiceURI: `fixture-${index}`, localService: true,
  }));
  const page = mount(path, voices);
  const buttons = [...page.document.querySelectorAll('button[data-say-lang]')];
  check('global language directory: every spoken language name is a named native control outside links', () => {
    assert.equal(buttons.length, 32);
    for (const button of buttons) {
      assert.equal(button.type, 'button');
      assert.ok(button.getAttribute('aria-label')?.trim());
      assert.equal(button.getAttribute('aria-pressed'), 'false');
      assert.equal(button.closest('a'), null);
    }
  });
  check('global language directory: each name speaks with its own marked locale', () => {
    for (const button of buttons) {
      const before = page.speech.length;
      button.click();
      assert.equal(page.speech.length, before + 1);
      assert.equal(page.speech.at(-1).text, button.getAttribute('data-say'));
      assert.equal(page.speech.at(-1).lang, button.getAttribute('data-say-lang'));
      page.speech.at(-1).onend();
    }
  });
  page.close();
}

{
  const page = mount('world-languages/afghanistan/index.html', [
    { name: 'Fixture Turkmen', lang: 'tk-TM', voiceURI: 'fixture-tk', localService: true },
  ]);
  const button = page.document.querySelector('button[data-lang="tk"][data-say="Türkmençe"]');
  check('legacy data-lang controls honor their explicit language instead of falling back to Hindi', () => {
    assert.ok(button);
    assert.equal(button.getAttribute('aria-pressed'), 'false');
    button.click();
    assert.equal(page.speech.length, 1);
    assert.equal(page.speech[0].text, 'Türkmençe');
    assert.equal(page.speech[0].voice.lang, 'tk-TM');
  });
  page.close();
}

{
  const page = mount('learn/aap-tum-tu-hindi/index.html', [
    { name: 'Fixture Hindi', lang: 'hi-IN', voiceURI: 'fixture-hi', localService: true },
  ]);
  const button = page.document.querySelector('button.spk[data-sb-say]');
  check('legacy Storybook speaker buttons receive a language-specific accessible name at mount', () => {
    assert.ok(button);
    assert.equal(button.type, 'button');
    assert.equal(button.getAttribute('aria-label'), `Play ${button.getAttribute('data-sb-say')} in Hindi`);
    assert.equal(button.getAttribute('aria-pressed'), 'false');
    button.click();
    assert.equal(page.speech[0].text, button.getAttribute('data-sb-say'));
    assert.equal(page.speech[0].voice.lang, 'hi-IN');
  });
  page.close();
}

console.log(`PASS mounted controls ${checks}/${checks} (jsdom; mocked voices; native keyboard and assistive-technology behavior not tested)`);
