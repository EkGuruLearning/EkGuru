/* =========================================================
   EkGuru — DEVICE-ONLY LEARNING JOURNAL v1
   ---------------------------------------------------------
   No account, analytics request, tracking cookie or paid reward. Everything is stored on this device
   (localStorage, key ekguru:learning:v1) plus the per-language review decks of js/global-srs.js.

   Honest limits: completion is a self-report; XP and badges are activity records, not certificates;
   the starting-point check is a rough recognition quiz, not a CEFR test; active time is approximate;
   reminders fire only while an EkGuru page is open (no background push, no subscription).
   A saved journal that cannot be read or is from a future version is PRESERVED: saves are blocked
   until a validated backup replaces it.
   ========================================================= */
(function (w) {
  'use strict';
  if (w.EkGuruRetention) return;
  var KEY = 'ekguru:learning:v1', MIGRATION = 'ekguru:hindi:shared-srs-migration:v1', MAX_FILE = 2 * 1024 * 1024;
  var LEVELS = ['A1', 'A1+', 'A2', 'A2+', 'B1', 'B1+', 'B2', 'B2+', 'C1', 'C1+', 'C2'];
  var METRIC_LEVELS = ['legacy'].concat(LEVELS);
  var RTL = ['ar', 'fa', 'ur', 'ps', 'he', 'yi'];
  var inputs = null, reminderTimer = null, lastActivity = Date.now(), readable = true;

  function plain(o) { return !!o && typeof o === 'object' && !Array.isArray(o); }
  function langOK(l) { return typeof l === 'string' && /^[a-z]{2,3}$/.test(l); }
  function num(n, max) { return typeof n === 'number' && isFinite(n) && n >= 0 && n <= max; }
  function str(t, max) { return typeof t === 'string' && t.length <= max; }
  function dayKey(date) { var d = date || new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function dayDate(key) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(key || '')) return null;
    var a = key.split('-').map(Number), d = new Date(a[0], a[1] - 1, a[2], 12);
    return dayKey(d) === key ? d : null;
  }
  function shifted(key, n) { var d = dayDate(key); if (!d) return ''; d.setDate(d.getDate() + n); return dayKey(d); }
  function weekKey(key) { var d = dayDate(key); if (!d) return ''; d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return dayKey(d); }
  function safeURL(raw) {
    if (!str(raw, 500) || raw.charAt(0) !== '/' || raw.indexOf('//') === 0 || /\\|%2e|%2f|%5c|[<>\x00-\x1f]/i.test(raw)) return false;
    try {
      var u = new URL(raw, location.origin);
      return u.origin === location.origin && !u.search && !u.username && !u.password &&
        /^\/(?:learn|languages|daily-hindi|toolbox|courses)\//.test(u.pathname) && u.pathname.split('/').indexOf('..') < 0;
    } catch (_) { return false; }
  }

  function empty() { return { version: 1, selected: 'hi', languages: {}, days: {}, freezes: {}, reminder: null }; }
  function validateJournal(j) {
    if (!plain(j) || j.version !== 1 || !langOK(j.selected) || !plain(j.languages) || !plain(j.days) || !plain(j.freezes)) throw new Error('Unknown journal version or invalid journal.');
    if (Object.keys(j).some(function (k) { return ['version', 'selected', 'languages', 'days', 'freezes', 'reminder'].indexOf(k) < 0; })) throw new Error('Unknown journal field.');
    if (Object.keys(j.languages).length > 700 || Object.keys(j.days).length > 3660 || Object.keys(j.freezes).length > 520) throw new Error('Journal exceeds the import limits.');
    Object.keys(j.days).forEach(function (d) { var x = j.days[d]; if (!dayDate(d) || !plain(x) || !num(x.xp, 100000) || !num(x.reviews, 10000)) throw new Error('Invalid study date or activity.'); });
    Object.keys(j.freezes).forEach(function (k) { if (!dayDate(k) || !dayDate(j.freezes[k]) || weekKey(shifted(j.freezes[k], 1)) !== k) throw new Error('Invalid streak freeze.'); });
    Object.keys(j.languages).forEach(function (l) {
      var x = j.languages[l];
      if (!langOK(l) || !plain(x) || !plain(x.completed) || !plain(x.levels) || !plain(x.reviewCredit) || Object.keys(x.completed).length > 5000 || Object.keys(x.reviewCredit).length > 5000) throw new Error('Invalid language progress.');
      Object.keys(x.completed).forEach(function (url) {
        var a = x.completed[url];
        if (!safeURL(url) || !plain(a) || !str(a.title, 300) || METRIC_LEVELS.indexOf(a.level) < 0 || !num(a.at, 1e14) || (a.active !== undefined && typeof a.active !== 'boolean')) throw new Error('Invalid completed lesson.');
      });
      Object.keys(x.levels).forEach(function (level) {
        var a = x.levels[level];
        if (METRIC_LEVELS.indexOf(level) < 0 || !plain(a) || !num(a.attempts, 1e7) || !num(a.correct, a.attempts) || !num(a.seconds, 1e9)) throw new Error('Invalid level metrics.');
      });
      Object.keys(x.reviewCredit).forEach(function (d) {
        var ids = x.reviewCredit[d];
        if (!dayDate(d) || !Array.isArray(ids) || ids.length > 10000 || ids.some(function (id) { return !str(id, 150) || ['__proto__', 'constructor', 'prototype'].indexOf(id) >= 0; })) throw new Error('Invalid review credit.');
      });
      if (x.last !== null && (!plain(x.last) || !safeURL(x.last.url) || !str(x.last.title, 300) || METRIC_LEVELS.indexOf(x.last.level) < 0 || !num(x.last.at, 1e14))) throw new Error('Unsafe continue link.');
      if (x.placement !== null && (!plain(x.placement) || LEVELS.indexOf(x.placement.level) < 0 || !num(x.placement.right, 10) || !num(x.placement.total, 10) || x.placement.right > x.placement.total || !num(x.placement.at, 1e14))) throw new Error('Invalid starting-point record.');
    });
    if (j.reminder !== null && (!plain(j.reminder) || !/^([01]\d|2[0-3]):[0-5]\d$/.test(j.reminder.time) || !(j.reminder.last === null || dayDate(j.reminder.last)))) throw new Error('Invalid local reminder.');
    return j;
  }
  function announce(t) {
    if (w.EkGuruUI) w.EkGuruUI.toast(t);
    else { var n = document.querySelector('[data-eg-journal-status]'); if (n) n.textContent = t; }
  }
  function read() {
    try { var raw = localStorage.getItem(KEY); readable = true; return raw ? validateJournal(JSON.parse(raw)) : empty(); }
    catch (_) { readable = false; return empty(); }
  }
  function save(j) {
    try { validateJournal(j); } catch (e) { announce(e.message + ' This change was not saved.'); return false; }
    if (!readable) { announce('An unreadable saved journal was preserved. Import a validated backup to replace it.'); return false; }
    try { localStorage.setItem(KEY, JSON.stringify(j)); return true; }
    catch (_) { announce('Browser storage is unavailable or full. This change was not saved.'); return false; }
  }
  function language(j, l) {
    if (!langOK(l)) throw new Error('Invalid language.');
    if (!j.languages[l]) j.languages[l] = { completed: {}, levels: {}, reviewCredit: {}, last: null, placement: null };
    return j.languages[l];
  }
  function levelOf(x, id) {
    if (LEVELS.indexOf(id) < 0) id = 'legacy';
    if (!x.levels[id]) x.levels[id] = { attempts: 0, correct: 0, seconds: 0 };
    return x.levels[id];
  }
  function touch(j, xp) {
    var key = dayKey();
    if (!j.days[key]) j.days[key] = { xp: 0, reviews: 0 };
    j.days[key].xp = Math.min(100000, j.days[key].xp + (xp || 0));
    return j.days[key];
  }
  function lvl(id) { return LEVELS.indexOf(id) >= 0 ? id : 'legacy'; }

  function complete(l, id, url, title) {
    if (!safeURL(url)) return false;
    var j = read(), x = language(j, l);
    if (x.completed[url]) {
      if (x.completed[url].active !== false) return false;
      x.completed[url].active = true; return save(j);
    }
    x.completed[url] = { title: String(title || 'Lesson').slice(0, 300), level: lvl(id), at: Date.now() };
    touch(j, 20);
    return save(j);
  }
  function uncomplete(l, url) {
    if (!safeURL(url)) return false;
    var j = read(), x = language(j, l);
    if (!x.completed[url] || x.completed[url].active === false) return false;
    x.completed[url].active = false; return save(j);
  }
  function visit(l, id, url, title) {
    if (!safeURL(url)) return false;
    var j = read(), x = language(j, l);
    x.last = { url: url, title: String(title || 'Lesson').slice(0, 300), level: lvl(id), at: Date.now() };
    j.selected = l; return save(j);
  }
  function practice(l, id, correct) {
    var j = read(), x = language(j, l), a = levelOf(x, id);
    a.attempts = Math.min(1e7, a.attempts + 1);
    if (correct) a.correct = Math.min(a.attempts, a.correct + 1);
    touch(j, 0); return save(j);
  }
  function activeTime(l, id, seconds) {
    if (!num(seconds, 60)) return false;
    var j = read(), x = language(j, l), a = levelOf(x, id);
    a.seconds = Math.min(1e9, a.seconds + Math.round(seconds)); return save(j);
  }
  function reviewCredit(l, id) {
    var j = read(), x = language(j, l), d = dayKey();
    if (!x.reviewCredit[d]) x.reviewCredit[d] = [];
    if (x.reviewCredit[d].indexOf(id) >= 0) return false;
    x.reviewCredit[d].push(id); touch(j, 5).reviews++; return save(j);
  }
  function streak(j, date) {
    var today = dayKey(date), at = j.days[today] ? today : shifted(today, -1), n = 0;
    var frozen = Object.keys(j.freezes).map(function (k) { return j.freezes[k]; });
    for (var i = 0; i < 3660; i++) {
      if (j.days[at]) n++; else if (frozen.indexOf(at) < 0) break;
      at = shifted(at, -1);
    }
    return n;
  }
  function freeze(date) {
    var j = read(), today = dayKey(date), miss = shifted(today, -1), week = weekKey(today);
    if (j.days[miss] || j.freezes[week] || !j.days[shifted(miss, -1)]) return false;
    j.freezes[week] = miss; return save(j);
  }

  /* ---- export / import: learning journal and typed decks only, never arbitrary storage ---- */
  function exportData() {
    var journal = read();
    if (!readable) throw new Error('The unreadable saved journal was preserved; a verified export cannot be produced.');
    var decks = {}, srs = w.EkGuruGlobalSRS;
    if (srs) srs.languages().forEach(function (l) {
      if (l === 'global') return;
      if (!srs.isReadable(l)) throw new Error('The saved ' + l + ' deck is unreadable and was preserved.');
      decks[l] = { version: 1, cards: Object.fromEntries(srs.all(l).map(function (c) { return [c.card_id, c]; })) };
    });
    var out = JSON.stringify({ type: 'ekguru-learning-backup', version: 1, journal: journal, decks: decks }, null, 2);
    if (new TextEncoder().encode(out).length > MAX_FILE) throw new Error('Backup exceeds 2 MB. Remove unneeded review cards first.');
    return out;
  }
  function validateBackup(raw) {
    if (typeof raw !== 'string' || new TextEncoder().encode(raw).length > MAX_FILE) throw new Error('Import must be a JSON file under 2 MB.');
    var b = JSON.parse(raw);
    if (!plain(b) || b.type !== 'ekguru-learning-backup' || b.version !== 1 || !plain(b.decks)) throw new Error('Unknown backup version.');
    if (Object.keys(b).some(function (k) { return ['type', 'version', 'journal', 'decks'].indexOf(k) < 0; })) throw new Error('Unknown backup field.');
    validateJournal(b.journal);
    var count = 0, srs = w.EkGuruGlobalSRS;
    Object.keys(b.decks).forEach(function (l) {
      var d = b.decks[l];
      if (!langOK(l) || !plain(d) || d.version !== 1 || !plain(d.cards) || Object.keys(d).some(function (k) { return k !== 'version' && k !== 'cards'; })) throw new Error('Invalid review deck.');
      Object.keys(d.cards).forEach(function (id) {
        count++;
        if (count > 10000 || !(srs ? srs.validCard(d.cards[id], l, id) : false)) throw new Error('Malformed review card or cross-language deck.');
      });
    });
    return b;
  }
  function importData(raw) {
    var b = validateBackup(raw), writes = {}, before = {}, changed = [];
    writes[KEY] = JSON.stringify(b.journal);
    writes[MIGRATION] = 'done';
    if (w.EkGuruGlobalSRS) w.EkGuruGlobalSRS.languages().filter(function (l) { return l !== 'global'; }).forEach(function (l) { writes['ekguru:srs:' + l + ':v1'] = null; });
    Object.keys(b.decks).forEach(function (l) { writes['ekguru:srs:' + l + ':v1'] = JSON.stringify(b.decks[l]); });
    // localStorage has no transactions: snapshot the allowlisted keys and roll back on quota failure.
    try {
      Object.keys(writes).forEach(function (k) { before[k] = localStorage.getItem(k); });
      Object.keys(writes).forEach(function (k) { changed.push(k); if (writes[k] === null) localStorage.removeItem(k); else localStorage.setItem(k, writes[k]); });
    } catch (e) {
      changed.reverse().forEach(function (k) { try { if (before[k] === null) localStorage.removeItem(k); else localStorage.setItem(k, before[k]); } catch (_) {} });
      throw new Error('Import could not be saved. Storage is unavailable or full.');
    }
    readable = true; scheduleReminder(); return true;
  }

  /* ---- UI helpers (textContent only; no HTML from stored data) ---- */
  function node(tag, value, attrs) {
    var el = document.createElement(tag);
    if (value !== null && value !== undefined) el.textContent = value;
    Object.keys(attrs || {}).forEach(function (k) { el.setAttribute(k, attrs[k]); });
    return el;
  }
  function button(label, act) { var b = node('button', label, { type: 'button' }); b.addEventListener('click', act); return b; }
  function link(label, url) { return node('a', label, { href: url }); }
  function fetchInputs() {
    if (inputs) return Promise.resolve(inputs);
    var url = '/data/learning/index.json';
    var response = navigator.onLine === false ? (w.caches ? caches.match(url) : Promise.resolve(null)) : fetch(url, { credentials: 'omit' });
    return Promise.resolve(response).then(function (r) { if (!r || !r.ok) throw new Error('Learning plans unavailable.'); return r.json(); })
      .then(function (d) { if (d.version !== 1 || !Array.isArray(d.languages)) throw new Error('Invalid learning plans.'); inputs = d; return d; });
  }
  function languageSelect(chosen, data) {
    var s = node('select', null, { 'aria-label': 'Learning language' });
    data.languages.forEach(function (l) { s.appendChild(node('option', l.name, { value: l.code })); });
    s.value = data.languages.some(function (l) { return l.code === chosen; }) ? chosen : 'hi';
    return s;
  }
  function plan(host) {
    fetchInputs().then(function (data) {
      var j = read(), l = host.getAttribute('data-eg-language') || j.selected, course = data.languages.find(function (x) { return x.code === l; });
      if (!course) return;
      var x = j.languages[l], lv = course.levels.find(function (a) { return x && x.placement && a.id === x.placement.level; }) || course.levels[0];
      var todo = lv.lessons.find(function (a) { return !x || !x.completed[a.url] || x.completed[a.url].active === false; }) || lv.lessons[0];
      host.replaceChildren(node('h3', 'Today: a short ' + course.name + ' session'), node('p', 'Suggested 10–15 minutes, not a measured promise.'));
      if (todo) host.appendChild(link('1. Read: ' + todo.title, todo.url));
      var due = w.EkGuruGlobalSRS ? w.EkGuruGlobalSRS.dueCount(l) : 0;
      host.appendChild(node('p', '2. Review up to ten due cards (' + due + ' due now). '));
      host.lastChild.appendChild(link('Open your review deck', '/learn/progress/'));
      if (lv.listening) {
        host.appendChild(node('p', '3. Listen once: ' + lv.listening.roman + ' — ' + lv.listening.meaning));
        host.appendChild(node('button', null, { type: 'button', class: 'eg-voice', hidden: '', 'data-voice-text': lv.listening.text, 'data-voice-lang': l, 'aria-label': 'Play ' + lv.listening.text + ' in ' + course.name }));
        if (w.EkGuruVoice) w.EkGuruVoice.mount(host);
      }
      host.appendChild(node('p', 'If no matching voice is installed, skip listening and read the romanisation.'));
    }).catch(function () { /* the server-rendered plan stays useful offline */ });
  }
  function continueLink(host) {
    var j = read(), l = host.getAttribute('data-eg-language') || j.selected, x = j.languages[l];
    if (x && x.last && safeURL(x.last.url)) host.replaceChildren(node('span', 'Continue where you left off: '), link(x.last.title, x.last.url), node('span', ' · '), link('Learning journal', '/learn/progress/'));
  }
  function journal(host) {
    fetchInputs().then(function (data) {
      var j = read(); host.replaceChildren();
      var picker = languageSelect(j.selected, data), lab = node('label', 'Language ');
      lab.appendChild(picker); host.appendChild(lab);
      var stats = node('div', null, { class: 'eg-journal' }), controls = node('div', null, { class: 'eg-controls' }), reviews = node('section', null), status = node('p', '', { role: 'status', 'data-eg-journal-status': '' });
      host.append(stats, controls, reviews, status);
      function paint() {
        j = read();
        if (!readable) status.textContent = 'Unreadable saved journal preserved. Import a validated backup to replace it.';
        var l = picker.value, x = language(j, l), srs = w.EkGuruGlobalSRS, cards = srs ? srs.all(l) : [];
        var completed = Object.keys(x.completed).filter(function (u) { return x.completed[u].active !== false; }).length;
        var xp = Object.keys(j.days).reduce(function (n, d) { return n + j.days[d].xp; }, 0), reviewed = cards.filter(function (c) { return c.review_count > 0; }).length, badges = [];
        if (completed >= 1) badges.push('First lesson'); if (completed >= 10) badges.push('Ten lessons'); if (reviewed >= 20) badges.push('Twenty cards reviewed'); if (streak(j) >= 7) badges.push('Seven study days');
        stats.replaceChildren(node('h2', completed + ' lessons marked complete · ' + streak(j) + ' study-day streak'),
          node('p', xp + ' XP across this device journal. Badges: ' + (badges.join(', ') || 'none yet') + '. These are activity records, not certificates.'),
          node('p', reviewed + ' words/cards reviewed, ' + cards.length + ' in this language deck.'));
        var table = node('table', null), head = node('tr', null), body = node('tbody', null);
        ['Level', 'Answers', 'Accuracy', 'Active time'].forEach(function (t) { head.appendChild(node('th', t, { scope: 'col' })); });
        table.appendChild(node('thead', null)).appendChild(head);
        Object.keys(x.levels).sort(function (a, b) { return METRIC_LEVELS.indexOf(a) - METRIC_LEVELS.indexOf(b); }).forEach(function (id) {
          var a = x.levels[id], tr = node('tr', null);
          [id === 'legacy' ? 'Legacy (level not recorded)' : id, String(a.attempts), a.attempts ? Math.round(a.correct / a.attempts * 100) + '%' : 'No answers recorded', Math.floor(a.seconds / 60) + ' min (approx.)'].forEach(function (t) { tr.appendChild(node('td', t)); });
          body.appendChild(tr);
        });
        table.appendChild(body); stats.appendChild(table);
        reviews.replaceChildren(node('h2', 'Review up to ten due cards'));
        if (srs && !srs.isReadable(l)) { status.textContent = 'Unreadable saved ' + l + ' review deck preserved. Import a validated backup to replace it.'; return; }
        var due = srs ? srs.due(l, 10) : [];
        if (!due.length) { reviews.appendChild(node('p', 'No cards are due in this language. Add selected vocabulary from a lesson to begin.')); return; }
        var c = due[0], card = node('article', null, { class: 'eg-journal' }), answer = node('p', c.answer, { hidden: '' });
        card.append(node('p', c.prompt, { lang: c.prompt_language || 'en', dir: RTL.indexOf(c.prompt_language) >= 0 ? 'rtl' : 'auto' }), answer, button('Reveal answer', function () { answer.hidden = false; }));
        var ratings = node('div', null, { class: 'eg-controls' });
        ['again', 'hard', 'good', 'easy'].forEach(function (r) {
          ratings.appendChild(button(r.charAt(0).toUpperCase() + r.slice(1), function () {
            if (answer.hidden) { status.textContent = 'Reveal the answer before choosing a recall rating.'; return; }
            if (!srs.review(c.card_id, r, l)) { status.textContent = 'This review could not be saved.'; return; }
            status.textContent = 'Review saved: ' + r + '. No pronunciation score was produced.'; paint();
          }));
        });
        card.appendChild(ratings); reviews.appendChild(card);
      }
      picker.addEventListener('change', function () { var next = read(); next.selected = picker.value; save(next); paint(); });
      controls.appendChild(button('Use one missed-day freeze', function () { status.textContent = freeze() ? 'One missed day bridged for this week; no study activity invented.' : 'No eligible missed day, or this week’s freeze is already used.'; paint(); }));
      controls.appendChild(button('Export learning JSON', function () {
        try {
          var blob = new Blob([exportData()], { type: 'application/json' }), u = URL.createObjectURL(blob), a = link('Download', u);
          a.download = 'ekguru-learning-' + dayKey() + '.json'; a.click(); setTimeout(function () { URL.revokeObjectURL(u); }, 1000);
          status.textContent = 'Exported this journal and language decks only.';
        } catch (e) { status.textContent = e.message; }
      }));
      var file = node('input', null, { type: 'file', accept: 'application/json,.json', 'aria-label': 'Choose learning backup JSON' }), confirmBox = node('input', null, { type: 'checkbox' }), confirmLabel = node('label', ' Replace this device journal/decks (export first)');
      confirmLabel.prepend(confirmBox);
      controls.append(file, confirmLabel, button('Validate and import', function () {
        var f = file.files[0];
        if (!f || !confirmBox.checked) { status.textContent = 'Choose a backup and explicitly confirm replacement.'; return; }
        if (f.size > MAX_FILE) { status.textContent = 'Import exceeds 2 MB.'; return; }
        f.text().then(function (raw) { importData(raw); status.textContent = 'Validated import complete. No booking or payment storage was touched.'; picker.value = read().selected; paint(); }).catch(function (e) { status.textContent = e.message; });
      }));
      controls.appendChild(button('Clear offline learning snapshots', function () {
        if (!w.confirm('Remove saved offline learning snapshots on this device? Your learning journal and review decks will be kept.')) return;
        offline(null, 'clear-offline').then(function () { status.textContent = 'Saved offline snapshots cleared; learning progress kept.'; }).catch(function (e) { status.textContent = e.message; });
      }));
      var time = node('input', null, { type: 'time', value: j.reminder ? j.reminder.time : '18:00', 'aria-label': 'Optional local reminder time' });
      controls.append(time, button('Enable local reminder', function () {
        enableReminder(time.value).then(function (ok) { status.textContent = ok ? 'Reminder enabled while EkGuru is open. No background push or subscription.' : 'Notifications were not permitted or are unsupported.'; });
      }), button('Disable reminder', function () { disableReminder(); status.textContent = 'Reminder removed on this device.'; }));
      paint();
    }).catch(function () { host.textContent = 'Learning inputs could not load. Your existing progress is not erased; try again online.'; });
  }
  function placement(host) {
    fetchInputs().then(function (data) {
      var picker = languageSelect(read().selected, data), box = node('div', null, { class: 'eg-journal' }), status = node('p', 'A rough recognition check, not a certified CEFR placement.', { role: 'status' }), session, lab = node('label', 'Choose a learning language ');
      lab.appendChild(picker); host.replaceChildren(lab); host.append(box, status, button('Begin optional starting-point check', begin));
      function begin() {
        fetch('/data/learning/placement/' + picker.value + '.json', { credentials: 'omit' }).then(function (r) { if (!r.ok) throw new Error('Question bank unavailable.'); return r.json(); }).then(function (d) {
          if (!Array.isArray(d.questions) || d.questions.length < 5) throw new Error('Fewer than five valid existing question keys are available. Choose a beginner lesson manually.');
          var course = data.languages.find(function (l) { return l.code === picker.value; });
          session = { language: picker.value, questions: d.questions, used: {}, taken: 0, right: 0, difficulty: 0, levels: course.levels.map(function (l) { return l.id; }) };
          picker.disabled = true; ask();
        }).catch(function (e) { status.textContent = e.message; });
      }
      function ask() {
        var left = session.questions.filter(function (q) { return !session.used[q.id]; });
        if (session.taken >= 10 || (session.taken >= 5 && !left.length) || !left.length) { finish(); return; }
        var wanted = session.levels[session.difficulty], q = left.find(function (x) { return x.level === wanted; }) || left[0];
        session.used[q.id] = true;
        box.replaceChildren(node('h3', 'Question ' + (session.taken + 1) + ' of up to 10'), node('p', q.q));
        q.options.forEach(function (o, i) {
          box.appendChild(button(o, function () {
            box.querySelectorAll('button').forEach(function (b) { b.disabled = true; });
            var right = i === q.answer; session.taken++; if (right) session.right++;
            session.difficulty = Math.max(0, Math.min(session.levels.length - 1, session.difficulty + (right ? 1 : -1)));
            status.textContent = (right ? '✓ Correct. ' : '✕ Not quite. Answer: ' + q.options[q.answer] + '. ') + (q.why || '');
            box.appendChild(button(session.taken >= 10 ? 'See starting point' : 'Next question', ask));
          }));
        });
      }
      function finish() {
        var id = session.levels[Math.max(0, session.difficulty - 1)], course = data.languages.find(function (l) { return l.code === session.language; });
        var target = course.levels.find(function (l) { return l.id === id; }) || course.levels[0], j = read(), x = language(j, session.language);
        x.placement = { level: id, right: session.right, total: session.taken, at: Date.now() }; j.selected = session.language; save(j); picker.disabled = false;
        box.replaceChildren(node('h3', 'Suggested starting point: ' + course.name + ' ' + id), node('p', session.right + ' of ' + session.taken + ' recognition answers correct. Not a certificate, fluency assessment or native-reviewed placement.'), link('Try this existing level', target.url));
        status.textContent = 'Start lower if the lesson feels difficult. You can always choose a different level.';
      }
    }).catch(function () { /* the server-rendered onboarding stays usable */ });
  }

  /* ---- reminders: only after an explicit Enable action, only while a page is open ---- */
  function scheduleReminder() {
    if (reminderTimer) clearInterval(reminderTimer); reminderTimer = null;
    var j = read(); if (!j.reminder || !w.Notification || Notification.permission !== 'granted') return;
    reminderTimer = setInterval(function () {
      var now = new Date(), cur = read(); if (!cur.reminder) return;
      var t = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
      if (t === cur.reminder.time && cur.reminder.last !== dayKey(now)) {
        try { new Notification('EkGuru: your optional study time', { body: 'One lesson, up to ten review cards, and optional listening. Open your device journal.' }); cur.reminder.last = dayKey(now); save(cur); } catch (_) {}
      }
    }, 30000);
  }
  function enableReminder(time) {
    if (!/^([01]\d|2[0-3]):[0-5]\d$/.test(time) || !w.Notification || !Notification.requestPermission) return Promise.resolve(false);
    return Notification.requestPermission().then(function (p) {
      if (p !== 'granted') return false;
      var j = read(); j.reminder = { time: time, last: null };
      if (!save(j)) return false; scheduleReminder(); return true;
    }).catch(function () { return false; });
  }
  function disableReminder() { var j = read(); j.reminder = null; save(j); if (reminderTimer) clearInterval(reminderTimer); reminderTimer = null; }

  /* ---- offline snapshots: ask the worker for an explicit bounded download ---- */
  function offline(url, action) {
    if (!navigator.serviceWorker) return Promise.reject(new Error('Offline downloads are unsupported here.'));
    var ready = Promise.race([navigator.serviceWorker.ready, new Promise(function (_, reject) { setTimeout(function () { reject(new Error('Offline worker is not ready. Reload online and try again.')); }, 8000); })]);
    return ready.then(function (reg) {
      return new Promise(function (resolve, reject) {
        var channel = new MessageChannel(), timer = setTimeout(function () { reject(new Error('Offline download timed out. No success is claimed.')); }, 60000);
        channel.port1.onmessage = function (e) { clearTimeout(timer); if (e.data.ok) resolve(e.data); else reject(new Error(e.data.reason || 'Download failed.')); };
        if (!reg.active) { clearTimeout(timer); reject(new Error('Offline worker is inactive.')); return; }
        reg.active.postMessage({ type: action || 'download-level', url: url }, [channel.port2]);
      });
    });
  }

  function boot() {
    document.querySelectorAll('[data-eg-today]').forEach(plan);
    document.querySelectorAll('[data-eg-continue]').forEach(continueLink);
    document.querySelectorAll('[data-eg-progress]').forEach(journal);
    document.querySelectorAll('[data-eg-placement]').forEach(placement);
    document.querySelectorAll('[data-eg-download-level]').forEach(function (b) {
      b.hidden = false;
      b.addEventListener('click', function () {
        b.disabled = true;
        var out = b.parentNode.querySelector('[role="status"]'); if (out) out.textContent = 'Downloading a bounded level snapshot…';
        offline(b.getAttribute('data-eg-download-level')).then(function (r) { if (out) out.textContent = 'Saved ' + r.files + ' files (' + Math.ceil(r.bytes / 1024) + ' KB) for offline reading. Voice availability is still device-dependent.'; })
          .catch(function (e) { if (out) out.textContent = e.message; }).then(function () { b.disabled = false; });
      });
    });
    document.querySelectorAll('[data-eg-complete]').forEach(function (b) {
      b.hidden = false;
      b.addEventListener('click', function () {
        var box = b.closest('[data-eg-language]'), l = box ? box.getAttribute('data-eg-language') : 'hi';
        if (complete(l, b.getAttribute('data-eg-level') || 'A1', b.getAttribute('data-eg-complete'), b.getAttribute('data-eg-title') || document.title)) {
          b.disabled = true; b.textContent = 'Marked complete on this device'; announce('Lesson completion saved. This is not a proficiency certificate.');
        }
      });
    });
    document.querySelectorAll('[data-eg-add-card]').forEach(function (b) {
      b.hidden = false;
      b.addEventListener('click', function () {
        var srs = w.EkGuruGlobalSRS; if (!srs) return;
        var l = b.getAttribute('data-eg-language') || 'hi';
        var result = srs.add({ language: l, prompt_language: l, prompt: b.getAttribute('data-eg-word') || '', target: b.getAttribute('data-eg-word') || '', answer: b.getAttribute('data-eg-meaning') || '', source: b.getAttribute('data-eg-roman') || '', level: b.getAttribute('data-eg-level') || 'A1', srs_eligible: true });
        announce(result.added ? 'Selected vocabulary saved to its language review deck.' : (result.reason || 'This card is already in the language deck.'));
        if (result.added || !result.reason) { b.disabled = true; b.textContent = 'In review deck'; }
      });
    });
    var page = document.querySelector('[data-eg-lesson-page]');
    if (page) visit(page.getAttribute('data-eg-language'), page.getAttribute('data-eg-level'), location.pathname, document.title);
    ['pointerdown', 'keydown', 'touchstart'].forEach(function (type) { document.addEventListener(type, function () { lastActivity = Date.now(); }, { passive: true }); });
    if (page) setInterval(function () { if (!document.hidden && Date.now() - lastActivity < 60000) activeTime(page.getAttribute('data-eg-language'), page.getAttribute('data-eg-level'), 15); }, 15000);
    w.addEventListener('ekguru:srs-review', function (e) { var d = e.detail || {}; if (langOK(d.language)) reviewCredit(d.language, d.card_id); });
    w.addEventListener('pagehide', function () { if (reminderTimer) clearInterval(reminderTimer); });
    scheduleReminder();
  }
  w.EkGuruRetention = { version: 1, key: KEY, read: read, complete: complete, uncomplete: uncomplete, visit: visit, practice: practice, activeTime: activeTime, streak: streak, freeze: freeze, dayKey: dayKey, weekKey: weekKey, exportData: exportData, validateBackup: validateBackup, importData: importData, enableReminder: enableReminder, disableReminder: disableReminder, downloadLevel: offline, safeURL: safeURL, validateJournal: validateJournal };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})(window);
