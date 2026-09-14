/* =========================================================
   EkGuru — HINDI AUDIO  (v1)
   ---------------------------------------------------------
   Honest, reusable browser pronunciation using the Web Speech
   API (speechSynthesis). This is a COMPUTER voice — it is
   never described as native or recorded audio anywhere.

   Usage (no per-button JS wiring):
     <strong data-hi-audio="नमस्ते">नमस्ते</strong>
   A "Listen" button is mounted after any element carrying
   data-hi-audio. Controls: play / stop / replay. Fallback:
   if speechSynthesis is unavailable the button is replaced by
   a short "audio unavailable" note. Never autoplays.

   Also mounts the one-line honest label next to the first
   audio button on the page.
   ========================================================= */
(function () {
  "use strict";

  function supported() {
    if (typeof window === "undefined") return false;
    if ("speechSynthesis" in window &&
        typeof window.SpeechSynthesisUtterance === "function") return true;
    /* v156: API voice needs only <audio> — no local voices required. */
    return typeof Audio !== "undefined";
  }

  var active = null;

  function stop() {
    if (active) {
      try { active.btn.classList.remove("playing"); active.btn.setAttribute("aria-pressed", "false"); }
      catch (e) {}
      active = null;
    }
    if (supported()) { try { window.speechSynthesis.cancel(); } catch (e) {} }
    try { if (window.EkGuruVoice) window.EkGuruVoice.stop(); } catch (e) {}
  }

  /* v154: default speech language follows the page, never forced Hindi. */
  var DEF_LANG = (function () {
    try {
      var M = { bengali: "bn", gujarati: "gu", kannada: "kn", malayalam: "ml",
        marathi: "mr", punjabi: "pa", tamil: "ta", telugu: "te", urdu: "ur" };
      var p = String(location.pathname || "").split("/");
      for (var i = 0; i < p.length; i++) {
        if (p[i] === "languages" && p[i + 1]) return p[i + 1];
        if (p[i] === "learn" && M[p[i + 1]]) return M[p[i + 1]];
        if (i === 1 && M[p[i]]) return M[p[i]];
      }
    } catch (e) {}
    return "hi-IN";
  })();
  function speak(text, btn, langTag) {
    if (!supported()) return false;
    stop();
    /* v156: API voice engine when storybook.js is on the page. */
    if (window.EkGuruVoice && window.EkGuruVoice.speak) {
      try {
        var tag = langTag || DEF_LANG;
        btn.classList.add("playing");
        btn.setAttribute("aria-pressed", "true");
        var lblA = btn.querySelector(".hi-listen-lbl");
        if (lblA) lblA.textContent = "Stop";
        active = { btn: btn };
        window.EkGuruVoice.speak(String(text), tag, 0.8, function () {
          if (active && active.btn === btn) stop();
        });
        return true;
      } catch (e) {}
    }
    try {
      var u = new SpeechSynthesisUtterance(String(text));
      u.lang = langTag || DEF_LANG;
      u.rate = 0.8;
      u.onend = function () {
        if (active && active.btn === btn) stop();
      };
      u.onerror = function () {
        if (active && active.btn === btn) stop();
      };
      btn.classList.add("playing");
      btn.setAttribute("aria-pressed", "true");
      var lbl = btn.querySelector(".hi-listen-lbl");
      if (lbl) lbl.textContent = "Stop";
      active = { btn: btn };
      window.speechSynthesis.speak(u);
      return true;
    } catch (e) {
      stop();
      return false;
    }
  }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function mountLabel() {
    if (document.getElementById("hi-audio-note")) return;
    var note = document.createElement("p");
    note.id = "hi-audio-note";
    note.className = "muted";
    note.style.cssText = "font-size:.78rem;margin:6px 0 0;color:var(--muted,inherit)";
    note.textContent = "🔊 Listen uses your browser's computer voice — not a native recording.";
    return note;
  }

  function mount() {
    var items = document.querySelectorAll("[data-hi-audio]");
    if (!items.length) return;
    var labelPlaced = false;
    items.forEach(function (el) {
      if (el.getAttribute("data-hi-audio-mounted")) return;
      el.setAttribute("data-hi-audio-mounted", "1");
      var text = el.getAttribute("data-hi-audio");
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "hi-listen";
      btn.setAttribute("aria-label", "Listen to “" + text + "” (computer voice)");
      btn.setAttribute("aria-pressed", "false");
      if (supported()) {
        btn.innerHTML = '<span aria-hidden="true">🔊</span> <span class="hi-listen-lbl">Listen</span>';
        btn.addEventListener("click", function (e) {
          e.preventDefault();
          if (btn.classList.contains("playing")) stop();
          else speak(text, btn);
        });
      } else {
        btn.setAttribute("disabled", "disabled");
        btn.textContent = "Audio unavailable";
        btn.title = "This browser does not support computer speech.";
      }
      if (!labelPlaced) {
        var note = mountLabel();
        if (note) {
          var anchor = el.closest ? (el.closest("td,th") ? el.closest("table") : el.closest("p,li,div,section")) : null;
          anchor = anchor || el.parentNode;
          if (anchor && anchor.parentNode) { anchor.parentNode.insertBefore(note, anchor.nextSibling); labelPlaced = true; }
        }
      }
      el.appendChild(btn);
    });
  }

  /* Phase 7C Stage 4 — language-aware listen buttons for starter packs.
     Same honest computer-voice behaviour as Hindi, but the utterance language
     comes from data-say-lang (a BCP-47 tag). Only mounted when the pack
     renderer asks for it; the Hindi flow is untouched. */
  function sayLabelPlaced() {
    return !!document.getElementById("hi-audio-note");
  }

  function mountSay() {
    var items = document.querySelectorAll("[data-say]");
    if (!items.length) return;
    var labelPlaced = sayLabelPlaced();
    items.forEach(function (el) {
      if (el.getAttribute("data-say-mounted")) return;
      el.setAttribute("data-say-mounted", "1");
      var text = el.getAttribute("data-say");
      var langTag = el.getAttribute("data-say-lang") || DEF_LANG;
      var prov = (window.EkGuruAudioProvider && typeof window.EkGuruAudioProvider.describe === "function")
        ? window.EkGuruAudioProvider.describe(langTag) : { provider: supported() ? "BROWSER_TTS" : "UNAVAILABLE" };
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "hi-listen";
      btn.setAttribute("aria-label", "Listen to “" + text + "” (computer voice)");
      btn.setAttribute("aria-pressed", "false");
      if (supported() && prov.provider !== "UNAVAILABLE") {
        btn.innerHTML = '<span aria-hidden="true">🔊</span> <span class="hi-listen-lbl">Listen</span>';
        btn.title = "Computer voice (browser TTS) — " + langTag + ". Not a native recording.";
        btn.addEventListener("click", function (e) {
          e.preventDefault();
          if (btn.classList.contains("playing")) stop();
          else speak(text, btn, langTag);
        });
      } else {
        btn.setAttribute("disabled", "disabled");
        btn.textContent = "Audio unavailable";
        btn.title = "No computer voice for " + langTag + " in this browser.";
      }
      if (!labelPlaced) {
        var note = mountLabel();
        if (note) {
          var anchor = el.closest ? (el.closest("td,th") ? el.closest("table") : el.closest("p,li,div,section")) : null;
          anchor = anchor || el.parentNode;
          if (anchor && anchor.parentNode) { anchor.parentNode.insertBefore(note, anchor.nextSibling); labelPlaced = true; }
        }
      }
      el.appendChild(btn);
    });
  }

  /* style hook (CSS lives in style.min.css: .hi-listen) */
  function boot() {
    mount();
    mountSay();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }

  /* tiny public API for other features (typing trainer etc.) */
  window.EkGuruHindiAudio = { speak: speak, stop: stop, supported: supported, mountSay: mountSay };

  /* =========================================================
     Phase 7 §10 — AUDIO PROVIDER ABSTRACTION (additive, non-breaking)
     ---------------------------------------------------------
     Providers: BROWSER_TTS | RECORDED | API_TTS | UNAVAILABLE.
     resolve(langTag) returns the best provider available right now
     for a BCP-47 language tag, in priority order. Today only
     BROWSER_TTS can ever resolve — RECORDED and API_TTS are future
     hooks (no recorded audio and no API exist yet). Nothing here
     ever claims browser TTS is native or recorded.
     ========================================================= */
  window.EkGuruAudioProvider = {
    PROVIDERS: ["BROWSER_TTS", "RECORDED", "API_TTS", "UNAVAILABLE"],
    voiceExists: function (langTag) {
      if (!supported()) return false;
      try {
        var v = window.speechSynthesis.getVoices();
        if (v && v.length) {
          var tag = String(langTag).toLowerCase();
          for (var i = 0; i < v.length; i++) {
            if (String(v[i].lang || "").toLowerCase().indexOf(tag) === 0) return true;
          }
          return false; /* v31 fix: voices ARE enumerated and none match -> UNAVAILABLE */
        }
        return true; // voices not yet enumerated; speechSynthesis still exists
      } catch (e) { return false; }
    },
    resolve: function (langTag) {
      if (!supported()) return "UNAVAILABLE";
      if (!this.voiceExists(langTag)) return "UNAVAILABLE";
      return "BROWSER_TTS"; // RECORDED/API_TTS never resolve today (honest)
    },
    describe: function (langTag) {
      var p = this.resolve(langTag);
      return {
        provider: p,
        nativeRecorded: p === "RECORDED",   // always false today
        needsServer: p === "API_TTS",       // always false today
        label: p === "BROWSER_TTS" ? "computer voice (browser TTS)" :
               p === "UNAVAILABLE" ? "no audio available" : p,
      };
    },
  };
})();
