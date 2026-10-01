/* Optional correction / review-offer form. No approval API, no automatic submission, no contact data kept in localStorage. */
(function () {
  'use strict';
  var form = document.querySelector('[data-eg-review-form]');
  if (!form) return;
  var consent = form.elements.namedItem('consent_to_publish'), name = form.elements.namedItem('public_name'), status = form.querySelector('[role="status"]'), endpoint = null;
  function names() { name.disabled = !consent.checked; name.required = consent.checked; if (!consent.checked) name.value = ''; }
  consent.addEventListener('change', names); names();
  fetch('/data/reviews/queue-config.json', { credentials: 'omit' }).then(function (r) { return r.json(); }).then(function (c) {
    if (c.enabled && /^https:\/\/script\.google\.com\/macros\/s\/[^/]+\/exec$/.test(c.endpoint)) endpoint = c.endpoint;
  }).catch(function () { /* the queue stays disabled */ });
  function field(k) { var el = form.elements.namedItem(k); return el ? String(el.value || '').trim() : ''; }
  function payload() {
    var data = { kind: field('kind'), language: field('language'), page_url: field('page_url'), content_digest: field('content_digest'), message: field('message'),
      source_url: field('source_url'), contact_email: field('contact_email'), consent_to_publish: consent.checked, website: field('website') };
    if (consent.checked) data.public_name = name.value.trim();
    return data;
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    if (!form.elements.namedItem('agree').checked) { status.textContent = 'Please confirm that this is a suggestion, not an approval.'; return; }
    if (!endpoint) { status.textContent = 'The private queue is not enabled or verified. Nothing was sent. Download the suggestion JSON and contact the maintainer through the contact page.'; return; }
    var button = form.querySelector('[type="submit"]'); button.disabled = true; status.textContent = 'Sending a pending suggestion…';
    fetch(endpoint, { method: 'POST', mode: 'no-cors', credentials: 'omit', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify({ action: 'review_suggestion', payload: payload() }) })
      .then(function () { status.textContent = 'A request was attempted. This cross-origin endpoint gives no readable receipt, so delivery and review are NOT confirmed. Contact the maintainer if it matters. No approval or publication change was made.'; })
      .catch(function () { status.textContent = 'Submission could not be confirmed. Nothing is approved. Download the JSON and send it to the maintainer.'; })
      .then(function () { button.disabled = false; });
  });
  form.querySelector('[data-eg-review-export]').addEventListener('click', function () {
    if (!form.reportValidity()) return;
    var data = payload(); delete data.website;
    var u = URL.createObjectURL(new Blob([JSON.stringify({ type: 'ekguru-pending-suggestion', version: 1, payload: data }, null, 2)], { type: 'application/json' })), a = document.createElement('a');
    a.href = u; a.download = 'ekguru-pending-suggestion.json'; a.click(); setTimeout(function () { URL.revokeObjectURL(u); }, 1000);
    status.textContent = 'Downloaded to your device only. The file may include contact information you chose to enter. It is not a review approval.';
  });
})();
