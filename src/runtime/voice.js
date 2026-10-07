/* EkGuru shared voice provider v2 (readable source; js/voice.js is the minified build).
   Click-only. Same-language device voices only (never another language's default voice).
   Licensed recordings win and are labelled; synthetic speech is always labelled synthetic.
   No remote TTS, no autoplay, no microphone access here. */
(function (w, d) {
  'use strict';
  if (w.EkGuruVoice && w.EkGuruVoice.version === 2) return;
  var LANGS = w.EKGURU_VOICE_LANGUAGES || {};
  // Legacy/macro codes that name the same spoken language in a registry code and a device voice.
  var ALIAS = { iw: 'he', 'in': 'id', ji: 'yi', nb: 'no', nn: 'no', tl: 'fil', cmn: 'zh', zsm: 'ms', uzn: 'uz', npi: 'ne', arb: 'ar', kmr: 'ku', pbu: 'ps' };
  var CONTROL = '.eg-voice,[data-voice-text],[data-sb-say],.spk,[data-say]';
  var LICENSES = ['CC0-1.0', 'CC-BY-4.0', 'CC-BY-SA-4.0', 'owner-recorded'];
  var synth = w.speechSynthesis || null, Utter = w.SpeechSynthesisUtterance || null;
  var state = { last: null, audio: null, active: null, playing: false, manifests: {}, rate: 0.8 };

  function canon(tag) { return String(tag || '').replace(/_/g, '-'); }
  function primary(tag) { var p = canon(tag).split('-')[0].toLowerCase(); return ALIAS[p] || p; }
  function store(key, value) {
    try { if (value === undefined) return w.localStorage.getItem(key); w.localStorage.setItem(key, value); } catch (_) { /* storage may be blocked */ }
    return null;
  }
  function entry(x) {
    var raw = String(x || '').trim(), code = LANGS[raw] ? raw : null;
    if (!code) { var p = canon(raw).split('-')[0].toLowerCase(); code = LANGS[p] ? p : null; }
    if (code) return { code: code, tag: LANGS[code].tag, name: LANGS[code].name || code };
    return { code: primary(raw), tag: canon(raw) || 'und', name: raw || 'this language' };
  }
  function sameLanguage(voiceLang, e) {
    var vp = primary(voiceLang);
    if (vp !== primary(e.tag)) return false;
    // zh-HK/zh-MO voices speak Cantonese; the registry course is Mandarin.
    return !(e.code === 'zh' && /^(zh-(HK|MO)|yue)/i.test(canon(voiceLang)));
  }
  function voices(x) {
    var e = entry(x), list = [], pref = store('ekguru:voice:' + e.code);
    try { list = synth ? Array.prototype.slice.call(synth.getVoices() || []) : []; } catch (_) { list = []; }
    return list.filter(function (v) { return v && v.lang && sameLanguage(v.lang, e); }).map(function (v) {
      var score = (pref && v.voiceURI === pref ? 1000 : 0) + (canon(v.lang).toLowerCase() === canon(e.tag).toLowerCase() ? 50 : 0) + (v.localService ? 10 : 0) + (v['default'] ? 1 : 0);
      return { voice: v, name: v.name || v.lang, lang: v.lang, uri: v.voiceURI || v.name, score: score };
    }).sort(function (a, b) { return b.score - a.score; });
  }
  function recording(x, text) {
    var e = entry(x), m = state.manifests[e.code] || [];
    for (var i = 0; i < m.length; i++) if (m[i].text === text) return m[i];
    return null;
  }
  function available(x, text) { return !!(synth && Utter && voices(x).length) || (text !== undefined && !!recording(x, text)); }
  function missing(x) { var e = entry(x); return 'Your browser has no ' + e.name + ' voice. Romanisation is shown instead.'; }
  function say(message) {
    var node = d.querySelector('[data-eg-voice-status]');
    if (node) node.textContent = message; else if (w.EkGuruUI) w.EkGuruUI.toast(message);
  }
  function label(e, text) { return 'Play ' + text + ' in ' + e.name; }
  function press(el, on) { if (el && el.setAttribute) el.setAttribute('aria-pressed', on ? 'true' : 'false'); }
  function syncAuxControls() {
    d.querySelectorAll('[data-eg-voice-slow],[data-eg-voice-repeat]').forEach(function (b) { b.disabled = !state.last; });
    d.querySelectorAll('[data-eg-voice-stop]').forEach(function (b) { b.disabled = !state.playing; });
  }
  function stop() {
    try { if (synth) synth.cancel(); } catch (_) { /* no-op */ }
    if (state.audio) { try { state.audio.pause(); } catch (_) { /* no-op */ } state.audio = null; }
    press(state.active, false); state.active = null; state.playing = false;
    syncAuxControls();
  }
  function speak(text, x, rate, onend, el) {
    text = String(text == null ? '' : text).replace(/\s+/g, ' ').trim();
    var e = entry(x);
    if (!text || text.length > 2000 || !/^[A-Za-z]{2,8}(-[A-Za-z0-9]{1,8})*$/.test(e.tag)) return false;
    var rec = recording(x, text), list = rec ? [] : voices(x);
    if (!rec && (!synth || !Utter || !list.length)) { say(missing(x)); return false; }
    stop(); state.last = { text: text, x: x, el: el || null };
    var r = rate || state.rate;
    if (el) { state.active = el; press(el, true); }
    state.playing = true; syncAuxControls();
    function done(ok) {
      state.playing = false; press(el, false); if (state.active === el) state.active = null;
      syncAuxControls();
      if (!ok) say('Playback could not start or finish. Romanisation is still shown.');
      if (typeof onend === 'function') { try { onend(ok); } catch (_) { /* caller error */ } }
    }
    if (rec) {
      try {
        var a = new w.Audio(rec.url); a.playbackRate = r; state.audio = a;
        a.onended = function () { done(true); }; a.onerror = function () { done(false); };
        var p = a.play(); if (p && p.catch) p['catch'](function () { done(false); });
        say(rec.kind === 'human' ? 'Recorded by ' + rec.recorder + ' (' + rec.license + ').' : 'Synthetic voice (recorded file, ' + rec.license + ').');
        return true;
      } catch (_) { done(false); return false; }
    }
    var u = new Utter(text); u.voice = list[0].voice; u.lang = list[0].lang; u.rate = r;
    u.onend = function () { done(true); }; u.onerror = function () { done(false); };
    try { synth.speak(u); } catch (_) { done(false); return false; }
    say('Synthetic voice — ' + list[0].name + ' (' + list[0].lang + '). Not a native recording.');
    return true;
  }
  function prefer(x, uri) {
    var e = entry(x);
    if (!voices(x).some(function (v) { return v.uri === uri; })) return false;
    store('ekguru:voice:' + e.code, uri); fill(); return true;
  }
  function setRate(r) {
    r = Number(r);
    if (!(r >= 0.5 && r <= 1.5)) return false;
    state.rate = r; store('ekguru:voice:rate', String(r));
    d.querySelectorAll('[data-eg-voice-rate]').forEach(function (s) { s.value = String(r); });
    return true;
  }
  function registerManifest(m) {
    if (!m || !Array.isArray(m.entries)) return 0;
    var e = entry(m.lang), keep = [];
    m.entries.forEach(function (x) {
      var ok = x && typeof x.text === 'string' && x.text && typeof x.lang === 'string' && primary(x.lang) === primary(e.tag)
        && typeof x.url === 'string' && /^\/audio\/[A-Za-z0-9._\/-]+\.(mp3|ogg|opus|wav|m4a)$/.test(x.url) && x.url.indexOf('..') < 0 && x.url.indexOf('//') < 0 && LICENSES.indexOf(x.license) >= 0
        && (x.kind === 'synthetic' || (x.kind === 'human' && typeof x.recorder === 'string' && x.recorder && typeof x.source_url === 'string' && /^https:\/\//.test(x.source_url)));
      if (ok) keep.push(x);
    });
    state.manifests[e.code] = keep; mount(); return keep.length;
  }
  function pageLanguage(el) {
    var explicit = el.getAttribute('data-voice-lang') || el.getAttribute('data-voice-code') || el.getAttribute('data-say-lang') || el.getAttribute('data-saylang') || el.getAttribute('data-lang');
    if (explicit) return explicit;
    var near = el.closest ? el.closest('[lang]') : null, root = d.documentElement.getAttribute('lang') || '';
    if (near && near !== d.documentElement && near.getAttribute('lang') && primary(near.getAttribute('lang')) !== primary(root)) return near.getAttribute('lang');
    return d.documentElement.getAttribute('data-learning-language') || 'hi';
  }
  function textOf(el) {
    var t = el.getAttribute('data-voice-text') || el.getAttribute('data-sb-say') || el.getAttribute('data-say');
    return t != null && t !== '' ? t : (el.classList.contains('spk') ? el.textContent : '');
  }
  function mount(root) {
    (root || d).querySelectorAll(CONTROL).forEach(function (el) {
      var text = textOf(el); if (!text) return;
      var x = pageLanguage(el), e = entry(x), ok = available(x, String(text).replace(/\s+/g, ' ').trim());
      if (el.tagName === 'BUTTON' && !el.getAttribute('type')) el.setAttribute('type', 'button');
      if (el.classList.contains('eg-voice')) {
        el.hidden = false; el.textContent = '🔊';
        if (!el.getAttribute('aria-label')) el.setAttribute('aria-label', label(e, text));
      } else if (!el.getAttribute('aria-label')) el.setAttribute('aria-label', label(e, text));
      el.setAttribute('aria-pressed', el.getAttribute('aria-pressed') || 'false');
      if (ok) { el.removeAttribute('aria-disabled'); el.removeAttribute('title'); }
      else { el.setAttribute('aria-disabled', 'true'); el.setAttribute('title', missing(x)); }
    });
    fill(); syncAuxControls();
  }
  function fill() {
    d.querySelectorAll('[data-eg-voice-picker]').forEach(function (sel) {
      var x = sel.getAttribute('data-eg-voice-picker'), list = voices(x), pref = store('ekguru:voice:' + entry(x).code);
      sel.textContent = '';
      if (!list.length) { var o = d.createElement('option'); o.textContent = 'No matching voice on this device'; o.value = ''; sel.appendChild(o); sel.disabled = true; return; }
      sel.disabled = false;
      list.forEach(function (v) { var o = d.createElement('option'); o.value = v.uri; o.textContent = v.name + ' (' + v.lang + ')'; o.selected = pref ? pref === v.uri : v === list[0]; sel.appendChild(o); });
    });
    d.querySelectorAll('[data-eg-voice-note]').forEach(function (n) { var x = n.getAttribute('data-eg-voice-note'); n.textContent = available(x) ? '' : missing(x); });
  }
  function repeat(rate) { if (!state.last) return false; return speak(state.last.text, state.last.x, rate, null, state.last.el); }
  d.addEventListener('click', function (ev) {
    var t = ev.target && ev.target.closest ? ev.target : null; if (!t) return;
    var ctl = t.closest('[data-eg-voice-stop],[data-eg-voice-slow],[data-eg-voice-repeat]');
    if (ctl) {
      if (ctl.hasAttribute('data-eg-voice-stop')) stop(); else repeat(ctl.hasAttribute('data-eg-voice-slow') ? 0.6 : undefined);
      return;
    }
    var el = t.closest(CONTROL); if (!el) return;
    var text = textOf(el); if (!text) return;
    ev.preventDefault(); ev.stopPropagation();
    var x = pageLanguage(el);
    if (state.active === el) { stop(); return; }
    speak(text, x, undefined, null, el);
  }, true);
  d.addEventListener('change', function (ev) {
    var t = ev.target;
    if (t && t.matches && t.matches('[data-eg-voice-picker]')) prefer(t.getAttribute('data-eg-voice-picker'), t.value);
    else if (t && t.matches && t.matches('[data-eg-voice-rate]')) setRate(t.value);
  });
  var saved = Number(store('ekguru:voice:rate')); if (saved >= 0.5 && saved <= 1.5) state.rate = saved;
  function boot() {
    mount();
    d.querySelectorAll('[data-eg-voice-rate]').forEach(function (s) { s.value = String(state.rate); });
    if (synth && synth.addEventListener) synth.addEventListener('voiceschanged', function () { mount(); });
    setTimeout(mount, 600); // some engines publish voices without a voiceschanged event
  }
  w.EkGuruVoice = {
    version: 2, speak: speak, stop: stop, repeat: repeat, slow: function () { return repeat(0.6); }, available: available, missing: missing, voices: function (x) { return voices(x).map(function (v) { return { name: v.name, lang: v.lang, uri: v.uri }; }); },
    prefer: prefer, rate: function () { return state.rate; }, setRate: setRate, registerManifest: registerManifest, tagFor: function (x) { return entry(x).tag; }, mount: mount, label: function (x, t) { return label(entry(x), t); }
  };
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', boot); else boot();
})(window, document);
