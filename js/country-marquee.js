/* Homepage country rails: two opposite marquees from real country↔language data. */
(function () {
  "use strict";

  function flagEmoji(cc) {
    cc = String(cc || "").toUpperCase();
    if (!/^[A-Z]{2}$/.test(cc)) return "";
    return String.fromCodePoint(127397 + cc.charCodeAt(0), 127397 + cc.charCodeAt(1));
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function chip(item) {
    var flag = flagEmoji(item.cc);
    return '<button type="button" class="eg-cc-chip" data-cc="' + esc(item.cc) + '"' +
      ' aria-expanded="false" aria-controls="eg-cc-panel">' +
      (flag ? '<span class="eg-cc-flag" aria-hidden="true">' + flag + "</span>" : "") +
      '<span class="eg-cc-name">' + esc(item.name) + "</span></button>";
  }

  function track(items, dir) {
    var inner = items.map(chip).join("");
    /* Duplicate for a seamless loop. The clone is aria-hidden so a
       screen reader and keyboard user see each country once. */
    return '<div class="eg-cc-viewport">' +
      '<div class="eg-cc-track eg-cc-' + dir + '" data-eg-cc-track>' +
      '<div class="eg-cc-set">' + inner + "</div>" +
      '<div class="eg-cc-set" aria-hidden="true">' + inner + "</div>" +
      "</div></div>";
  }

  function bind(host, byCc) {
    var panel = host.querySelector("#eg-cc-panel");
    if (!panel) return;
    var live = host.querySelector("#eg-cc-live");
    var current = null;

    function close() {
      current = null;
      panel.hidden = true;
      panel.innerHTML = "";
      host.querySelectorAll(".eg-cc-chip[aria-expanded='true']").forEach(function (b) {
        b.setAttribute("aria-expanded", "false");
      });
      if (live) live.textContent = "";
    }

    function open(btn) {
      var cc = btn.getAttribute("data-cc");
      var item = byCc[cc];
      if (!item) return;
      if (current === cc) { close(); return; }
      host.querySelectorAll(".eg-cc-chip[aria-expanded='true']").forEach(function (b) {
        b.setAttribute("aria-expanded", "false");
      });
      current = cc;
      btn.setAttribute("aria-expanded", "true");
      var langs = (item.langs || []).filter(Boolean).map(function (lang) {
        return typeof lang === "string" ? { name: lang, quality: "PROVISIONAL" } : lang;
      });
      var verified = langs.filter(function (lang) { return lang.quality === "VERIFIED"; });
      var provisional = langs.filter(function (lang) { return lang.quality === "PROVISIONAL"; });
      function languageList(rows, label, note) {
        if (!rows.length) return "";
        return "<h4>" + esc(label) + "</h4><p class=\"muted\">" + esc(note) + "</p>" +
          "<ul class=\"eg-cc-langs\">" + rows.map(function (lang) {
            var native = lang.native && lang.native !== lang.name ? " — " + lang.native : "";
            return "<li>" + esc(lang.name + native) + "</li>";
          }).join("") + "</ul>";
      }
      var list = languageList(verified, "Verified relationships", "Supported by a linked high-confidence source in the research inventory.") +
        languageList(provisional, "Provisional relationships", "A reputable source is recorded, but editorial verification is not complete.");
      if (!list) list = "<p class=\"muted\">No public relationship has passed the source gate.</p>";
      panel.hidden = false;
      panel.innerHTML =
        "<h3>" + esc(item.name) + "</h3>" + list;
      var spoken = langs.length ? langs.map(function (lang) { return lang.name; }).join(", ") : "none listed";
      if (live) live.textContent = item.name + ": " + spoken;
      try { panel.focus(); } catch (e) {}
    }

    host.addEventListener("click", function (e) {
      var btn = e.target.closest(".eg-cc-chip");
      if (!btn || !host.contains(btn)) return;
      open(btn);
    });

    host.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  function render() {
    var host = document.getElementById("markets");
    if (!host) return;
    var data = window.EKGURU_COUNTRY_LANGS;
    if (!Array.isArray(data) || !data.length) return;

    var mid = Math.ceil(data.length / 2);
    var a = data.slice(0, mid);
    var b = data.slice(mid);
    var byCc = {};
    data.forEach(function (item) { byCc[item.cc] = item; });

    host.setAttribute("data-eg-cc-rails", "1");
    host.innerHTML =
      '<div class="eg-cc-rails" role="region" aria-label="Countries and languages">' +
      '<p class="eg-cc-hint">Click a country to see source-gated language relationships. Provisional records are labelled.</p>' +
      track(a, "ltr") +
      track(b, "rtl") +
      '<div id="eg-cc-live" class="vh" aria-live="polite"></div>' +
      '<div id="eg-cc-panel" class="eg-cc-panel" hidden tabindex="-1"></div>' +
      "</div>";
    bind(host, byCc);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", render);
  } else {
    render();
  }
  window.EkGuruCountryRails = { render: render };
})();
