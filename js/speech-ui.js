/* Optional speaking transcript and licensed-recording manifests. Click-only microphone; never a pronunciation score.
   No remote TTS, no autoplay, no background listening. Manifests are fetched only for languages flagged with real recordings. */
(function (w, d) {
  'use strict';
  function voice() { return w.EkGuruVoice; }
  function pageLanguage() { return d.documentElement.getAttribute('data-learning-language') || 'hi'; }
  function loadManifest(code) {
    var meta = (w.EKGURU_VOICE_LANGUAGES || {})[code];
    if (!meta || !meta.rec || !voice()) return;
    var url = '/data/audio-manifest/' + code + '.json';
    var request = (w.navigator.onLine === false && w.caches) ? w.caches.match(url) : w.fetch(url, { credentials: 'omit' });
    Promise.resolve(request).then(function (r) { if (!r || !r.ok) throw new Error('manifest'); return r.json(); })
      .then(function (manifest) { voice().registerManifest(manifest); })
      .catch(function () { /* recordings are optional; device speech or romanisation remains */ });
  }
  function microphone(box) {
    var start = box.querySelector('[data-eg-microphone]'), stop = box.querySelector('[data-eg-microphone-stop]'), out = box.querySelector('[data-eg-transcript]');
    if (!start || !out) return;
    var Recognition = w.SpeechRecognition || w.webkitSpeechRecognition, active = null;
    if (!Recognition) {
      start.setAttribute('aria-disabled', 'true');
      out.textContent = 'Speech recognition is not available in this browser. Reading, writing and listening practice still work.';
      return;
    }
    start.addEventListener('click', function () {
      if (active) return;
      var code = box.getAttribute('data-eg-language') || pageLanguage();
      var r = new Recognition();
      r.lang = voice() ? voice().tagFor(code) : code; r.interimResults = false; r.continuous = false; r.maxAlternatives = 1;
      r.onresult = function (event) {
        var alternative = event.results && event.results[0] && event.results[0][0];
        out.textContent = alternative ? 'We heard: “' + String(alternative.transcript).slice(0, 300) + '”. This is a transcript only, not a pronunciation score.' : 'Nothing was recognised. This is not a score.';
      };
      r.onerror = function (event) { out.textContent = 'Microphone or recognition was not available (' + String(event && event.error || 'error') + '). Nothing was scored.'; };
      r.onend = function () { active = null; start.disabled = false; if (stop) stop.disabled = true; };
      active = r; start.disabled = true; if (stop) stop.disabled = false;
      out.textContent = 'Listening… Your browser may send audio to its speech provider.';
      try { r.start(); } catch (_) { active = null; start.disabled = false; if (stop) stop.disabled = true; out.textContent = 'Microphone could not start. Nothing was scored.'; }
    });
    if (stop) stop.addEventListener('click', function () { if (active) { try { active.stop(); } catch (_) { /* already stopped */ } } });
  }
  function boot() {
    loadManifest(pageLanguage());
    d.querySelectorAll('[data-eg-speaking]').forEach(microphone);
  }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', boot); else boot();
})(window, document);
