#!/usr/bin/env node
/* UX state contracts for voice speed/replay controls. jsdom uses mocked speech; it is not browser/AT evidence. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM, VirtualConsole } from 'jsdom';

const read = (path) => readFileSync(path, 'utf8');
let checks = 0;
function ok(name, test) { test(); checks++; console.log('PASS ' + name); }
const markup = '<!doctype html><html lang="en" data-learning-language="hi"><body><main>' +
  '<p lang="hi">नमस्ते <button class="eg-voice" type="button" data-voice-text="नमस्ते" data-voice-lang="hi" aria-label="Play नमस्ते in Hindi"></button></p>' +
  '<details class="voice-settings"><label>Speed<select data-eg-voice-rate><option value="0.6">0.6×</option><option value="0.8" selected>0.8×</option><option value="1">1×</option></select></label>' +
  '<button type="button" data-eg-voice-slow>Slow</button><button type="button" data-eg-voice-repeat>Repeat</button>' +
  '<button type="button" data-eg-voice-stop>Stop</button><p role="status" data-eg-voice-status></p></details></main></body></html>';

function makeDevice(voices) {
  const dom = new JSDOM(markup, {
    url: 'https://ekguru.shop/learn/hindi/', runScripts: 'outside-only',
    pretendToBeVisual: true, virtualConsole: new VirtualConsole(),
  });
  const { window: w } = dom, { document: d } = w;
  const state = { voices, utterances: [], cancelCount: 0 };
  Object.defineProperty(d, 'readyState', { value: 'complete' });
  w.SpeechSynthesisUtterance = function (text) { this.text = text; };
  w.speechSynthesis = {
    getVoices: () => state.voices,
    speak: (utterance) => state.utterances.push(utterance),
    cancel: () => { state.cancelCount++; },
    addEventListener() {},
  };
  w.eval(read('js/voice-languages.js'));
  w.eval(read('js/voice.js'));
  return { dom, w, d, state, close: () => dom.window.close() };
}
const hindiVoice = { name: 'Hindi fixture', lang: 'hi-IN', voiceURI: 'hi-fixture', localService: true };

{
  const t = makeDevice([hindiVoice]);
  const slow = t.d.querySelector('[data-eg-voice-slow]');
  const repeat = t.d.querySelector('[data-eg-voice-repeat]');
  const stop = t.d.querySelector('[data-eg-voice-stop]');
  const speaker = t.d.querySelector('.eg-voice');
  ok('replay and stop controls start unavailable until an item is spoken', () => {
    assert.equal(slow.disabled, true);
    assert.equal(repeat.disabled, true);
    assert.equal(stop.disabled, true);
    assert.equal(t.state.utterances.length, 0);
  });
  ok('a successful click enables slow/repeat and stop only while playing', () => {
    speaker.click();
    assert.equal(t.state.utterances.length, 1);
    assert.equal(t.state.utterances[0].text, 'नमस्ते');
    assert.equal(t.state.utterances[0].lang, 'hi-IN');
    assert.equal(t.state.utterances[0].rate, 0.8);
    assert.equal(speaker.getAttribute('aria-pressed'), 'true');
    assert.equal(slow.disabled, false);
    assert.equal(repeat.disabled, false);
    assert.equal(stop.disabled, false);
    t.state.utterances[0].onend();
    assert.equal(speaker.getAttribute('aria-pressed'), 'false');
    assert.equal(stop.disabled, true);
    assert.equal(repeat.disabled, false);
  });
  ok('Slow replays the last exact-language item at 0.6× and returns to the current rate on Repeat', () => {
    slow.click();
    const slower = t.state.utterances.at(-1);
    assert.equal(slower.text, 'नमस्ते');
    assert.equal(slower.lang, 'hi-IN');
    assert.equal(slower.rate, 0.6);
    slower.onend();
    repeat.click();
    const replay = t.state.utterances.at(-1);
    assert.equal(replay.text, 'नमस्ते');
    assert.equal(replay.lang, 'hi-IN');
    assert.equal(replay.rate, 0.8);
    assert.equal(stop.disabled, false);
  });
  ok('Stop cancels playback, clears pressed state, and leaves the prior item available to replay', () => {
    stop.click();
    assert.ok(t.state.cancelCount > 0);
    assert.equal(stop.disabled, true);
    assert.equal(speaker.getAttribute('aria-pressed'), 'false');
    assert.equal(repeat.disabled, false);
    assert.equal(slow.disabled, false);
  });
  ok('an engine error disables Stop without discarding the replay target', () => {
    repeat.click();
    t.state.utterances.at(-1).onerror();
    assert.equal(stop.disabled, true);
    assert.equal(repeat.disabled, false);
    assert.match(t.d.querySelector('[data-eg-voice-status]').textContent, /Playback could not start or finish/);
  });
  t.close();
}

{
  const t = makeDevice([]);
  const slow = t.d.querySelector('[data-eg-voice-slow]');
  const repeat = t.d.querySelector('[data-eg-voice-repeat]');
  const stop = t.d.querySelector('[data-eg-voice-stop]');
  t.d.querySelector('.eg-voice').click();
  ok('missing voice leaves all replay controls disabled and exposes the honest fallback', () => {
    assert.equal(t.state.utterances.length, 0);
    assert.equal(slow.disabled, true);
    assert.equal(repeat.disabled, true);
    assert.equal(stop.disabled, true);
    assert.match(t.d.querySelector('[data-eg-voice-status]').textContent, /no Hindi voice/i);
  });
  t.close();
}

{
  const t = makeDevice([hindiVoice]);
  t.w.matchMedia = () => ({ matches: false });
  t.w.eval(read('js/storybook.js'));
  const pill = t.d.querySelector('.sb-speed');
  const status = t.d.getElementById('sb-speed-status');
  ok('the Storybook speed cycle has a native button, changing accessible name, live status and focus style', () => {
    assert.ok(pill);
    assert.equal(pill.tagName, 'BUTTON');
    assert.equal(pill.type, 'button');
    assert.match(pill.getAttribute('aria-label'), /0\.8× normal speed.*normal speed \(1×\)/i);
    assert.equal(pill.getAttribute('aria-describedby'), 'sb-speed-status');
    assert.equal(status.getAttribute('role'), 'status');
    assert.equal(status.getAttribute('aria-live'), 'polite');
    assert.match(read('css/storybook.css'), /\.sb-speed:focus-visible\s*\{[^}]*outline:/);
  });
  ok('speed cycles 0.8× → 1× → 0.6× and announces the selected rate', () => {
    pill.click();
    assert.equal(t.w.EkGuruVoice.rate(), 1);
    assert.match(pill.getAttribute('aria-label'), /normal speed \(1×\).*0\.6× normal speed/i);
    assert.equal(status.textContent, 'Speech speed set to normal speed (1×).');
    pill.click();
    assert.equal(t.w.EkGuruVoice.rate(), 0.6);
    assert.match(pill.getAttribute('aria-label'), /0\.6× normal speed.*0\.8× normal speed/i);
    assert.equal(status.textContent, 'Speech speed set to 0.6× normal speed.');
  });
  t.close();
}

console.log(`PASS voice UX ${checks}/${checks} (jsdom with mocked voices; native keyboard, assistive technology, device voices and audio quality not tested)`);
