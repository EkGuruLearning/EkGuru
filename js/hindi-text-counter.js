/*
 * Browser-only Hindi text counter.
 * Counts Unicode code points and explicit punctuation patterns; it does not
 * attempt linguistic word segmentation or sentence parsing.
 */
(function (root) {
  "use strict";

  var SAMPLE_TEXT = "नमस्ते दुनिया।\nHello, world!";

  function measureText(value) {
    var text = value == null ? "" : String(value);
    var codePoints = Array.from(text);
    var sentenceGroups = text.match(/[.!?।॥]+/gu) || [];
    var normalizedLines = text.replace(/\r\n?/g, "\n");
    var trimmedLines = normalizedLines.trim();
    var paragraphs = trimmedLines
      ? trimmedLines.split(/\n[ \t]*\n+/u).filter(function (part) {
          return part.trim().length > 0;
        }).length
      : 0;

    return {
      words: (text.match(/\S+/gu) || []).length,
      codePoints: codePoints.length,
      charactersNoWhitespace: codePoints.filter(function (character) {
        return !/\s/u.test(character);
      }).length,
      sentenceEndings: sentenceGroups.length,
      paragraphs: paragraphs
    };
  }

  var api = Object.freeze({ measureText: measureText, sampleText: SAMPLE_TEXT });
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.EkGuruHindiTextCounter = api;

  function initialise(doc) {
    var input = doc.getElementById("tc-input");
    if (!input || input.dataset.counterReady === "true") return;
    input.dataset.counterReady = "true";

    var metrics = {
      words: doc.getElementById("tc-words"),
      codePoints: doc.getElementById("tc-code-points"),
      charactersNoWhitespace: doc.getElementById("tc-no-whitespace"),
      sentenceEndings: doc.getElementById("tc-sentence-endings"),
      paragraphs: doc.getElementById("tc-paragraphs")
    };
    var status = doc.getElementById("tc-status");
    var panel = doc.getElementById("tc-metrics");
    var noScript = doc.getElementById("tc-nojs");

    function render() {
      var counts = measureText(input.value);
      Object.keys(metrics).forEach(function (key) {
        if (metrics[key]) metrics[key].textContent = String(counts[key]);
      });
    }

    input.addEventListener("input", render);
    render();
    if (panel) panel.hidden = false;
    if (noScript) noScript.hidden = true;

    var clear = doc.getElementById("tc-clear");
    if (clear) clear.addEventListener("click", function () {
      input.value = "";
      render();
      if (status) status.textContent = "Text cleared.";
      input.focus();
    });

    var sample = doc.getElementById("tc-sample");
    if (sample) sample.addEventListener("click", function () {
      input.value = SAMPLE_TEXT;
      render();
      if (status) status.textContent = "Sample text added. Edit it or clear it at any time.";
      input.focus();
    });

    var copy = doc.getElementById("tc-copy");
    if (copy) copy.addEventListener("click", function () {
      if (!input.value) {
        if (status) status.textContent = "There is no text to copy yet.";
        input.focus();
        return;
      }
      var clipboard = root.navigator && root.navigator.clipboard;
      if (!clipboard || typeof clipboard.writeText !== "function") {
        input.focus();
        input.select();
        if (status) status.textContent = "Clipboard access is unavailable. The text is selected so you can copy it manually.";
        return;
      }
      function selectForManualCopy(message) {
        input.focus();
        input.select();
        if (status) status.textContent = message;
      }
      try {
        clipboard.writeText(input.value).then(function () {
          if (status) status.textContent = "Text copied to your clipboard.";
        }).catch(function () {
          selectForManualCopy("Clipboard access was blocked. The text is selected so you can copy it manually.");
        });
      } catch (error) {
        selectForManualCopy("Clipboard access failed. The text is selected so you can copy it manually.");
      }
    });
  }

  if (root.document) {
    if (root.document.readyState === "loading") {
      root.document.addEventListener("DOMContentLoaded", function () {
        initialise(root.document);
      }, { once: true });
    } else {
      initialise(root.document);
    }
  }
})(typeof window !== "undefined" ? window : globalThis);
