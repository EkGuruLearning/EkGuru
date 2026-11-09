/* Optional correction / review-offer form. Sends to the private queue
   (when enabled) AND writes a contact row to the sheet via the intake
   endpoint, so every suggestion is recorded and can be followed up. */
(function () {
  'use strict';
  var form = document.querySelector('[data-eg-review-form]');
  if (!form) return;
  var consent = form.elements.namedItem('consent_to_publish'), name = form.elements.namedItem('public_name'), status = form.querySelector('[role="status"]'), endpoint = null;
  function names() { name.disabled = !consent.checked; name.required = consent.checked; if (!consent.checked) name.value = ''; }
  consent.addEventListener('change', names); names();
  fetch('/data/reviews/queue-config.json', { credentials: 'omit' }).then(function (r) { return r.json(); }).then(function (c) {
    if (c.enabled && /^https:\/\/(www\.)?script\.google\.com\/macros\/s\/[^/]+\/exec$/.test(c.endpoint)) endpoint = c.endpoint;
  }).catch(function () { /* the queue stays disabled */ });
  function field(k) { var el = form.elements.namedItem(k); return el ? String(el.value || '').trim() : ''; }
  function payload() {
    var data = { kind: field('kind'), language: field('language'), page_url: field('page_url'), content_digest: field('content_digest'), message: field('message'),
      source_url: field('source_url'), contact_email: field('contact_email'), consent_to_publish: consent.checked, website: field('website') };
    if (consent.checked) data.public_name = name.value.trim();
    return data;
  }
  /* Also write to the sheet through the shared intake endpoint so the
     suggestion is recorded even when the private queue is disabled. */
  function sendToSheet(data) {
    if (typeof window.EkGuruIntake === "undefined" || !window.EkGuruIntake.ready()) return Promise.resolve({ ok: false, error: "Intake is not available right now." });
    var fields = {
      name: data.public_name || data.contact_email.split("@")[0] || "Correction suggestion",
      email: data.contact_email || "",
      subject: data.kind || "correction",
      topic: data.language ? "language: " + data.language : "",
      message: data.message + (data.page_url ? "\nPage: " + data.page_url : "") + (data.source_url ? "\nSource: " + data.source_url : "") + (data.content_digest ? "\nDigest: " + data.content_digest : ""),
      page: data.page_url || ""
    };
    return window.EkGuruIntake.submit("contact", fields, true, data.website);
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    if (!form.elements.namedItem('agree').checked) { status.textContent = 'Please confirm that this is a suggestion, not an approval.'; return; }
    var button = form.querySelector('[type="submit"]'); button.disabled = true; status.textContent = 'Sending a pending suggestion…';
    var sent = [];
    var data = payload();
    /* 1. Private queue (if enabled) */
    if (endpoint) {
      sent.push(fetch(endpoint, { method: 'POST', mode: 'no-cors', credentials: 'omit', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify({ action: 'review_suggestion', payload: data }) })
        .then(function () { return { queue: true, ok: true }; })
        .catch(function () { return { queue: true, ok: false }; }));
    }
    /* 2. Sheet via intake (always attempted) */
    sent.push(sendToSheet(data));
    Promise.all(sent).then(function (results) {
      var sheetOk = results.some(function (r) { return r.ok === true && r.queue !== true; });
      var queueOk = results.some(function (r) { return r.queue === true && r.ok === true; });
      if (sheetOk || queueOk) {
        status.textContent = 'Your suggestion was recorded. The owner reviews it privately — this is not an approval or a publication.';
      } else {
        status.textContent = 'Nothing could be sent right now. Download the suggestion JSON and contact the maintainer through the contact page.';
      }
      button.disabled = false;
    });
  });
  form.querySelector('[data-eg-review-export]').addEventListener('click', function () {
    if (!form.reportValidity()) return;
    var data = payload(); delete data.website;
    var u = URL.createObjectURL(new Blob([JSON.stringify({ type: 'ekguru-pending-suggestion', version: 1, payload: data }, null, 2)], { type: 'application/json' })), a = document.createElement('a');
    a.href = u; a.download = 'ekguru-pending-suggestion.json'; a.click(); setTimeout(function () { URL.revokeObjectURL(u); }, 1000);
    status.textContent = 'Downloaded to your device only. The file may include contact information you chose to enter. It is not a review approval.';
  });
})();
