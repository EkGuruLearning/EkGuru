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
    return typeof window !== "undefined" && "speechSynthesis" in window &&
           typeof window.SpeechSynthesisUtterance === "function";
  }

  var active = null;

  function stop() {
    if (active) {
      try { active.btn.classList.remove("playing"); active.btn.setAttribute("aria-pressed", "false"); }
      catch (e) {}
      active = null;
    }
    if (supported()) { try { window.speechSynthesis.cancel(); } catch (e) {} }
  }

  function speak(text, btn) {
    if (!supported()) return false;
    stop();
    try {
      var u = new SpeechSynthesisUtterance(String(text));
      u.lang = "hi-IN";
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

  /* style hook (CSS lives in style.min.css: .hi-listen) */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }

  /* tiny public API for other features (typing trainer etc.) */
  window.EkGuruHindiAudio = { speak: speak, stop: stop, supported: supported };

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
