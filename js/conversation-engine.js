/* =========================================================
   EkGuru — DETERMINISTIC CONVERSATION ENGINE  (Phase 7C §21)
   ---------------------------------------------------------
   A rule-based, data-driven conversation simulator.

   - Reads data/conversation-scenarios.json (fixed, reviewed basic
     Hindi). Every NPC line, choice and explanation is authored data;
     there is NO model, NO network call, NO AI. The engine walks a
     finite state machine: scenario -> step -> choice -> feedback.

   - HONESTY: the UI is labelled "Deterministic practice — not AI".
     There are no AI_ASSISTED scenarios yet because no secure provider
     relay exists (§22); when one does, it plugs in as a separate
     provider, never replacing this engine.

   - Rendering contract: the engine renders INSIDE a container element
     (passed to mount()), re-drawing on every state change. If the data
     fails to load, it renders an unavailable note and never throws.

   API (window.EkGuruConversation):
     ready()  -> Promise resolved once scenarios are loaded
     list()   -> scenario summaries [{id,title,level,goal,context}]
     mount(containerEl, scenarioId)  -> start a scenario in the element
   ========================================================= */
(function (root) {
  "use strict";

  var DATA_URL = (function () {
    try {
      var cs = document.currentScript;
      if (cs && cs.src) {
        var p = cs.src.split("?")[0];
        return p.substring(0, p.lastIndexOf("/") + 1) + "../data/conversation-scenarios.json";
      }
    } catch (e) {}
    return "data/conversation-scenarios.json";
  })();

  var scenarios = null;
  var readyPromise = null;

  function ready() {
    if (readyPromise) return readyPromise;
    readyPromise = new Promise(function (resolve, reject) {
      if (typeof root.fetch !== "function") { reject(new Error("no fetch")); return; }
      root.fetch(DATA_URL, { cache: "no-cache" })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error("scenarios " + r.status)); })
        .then(function (d) { scenarios = (d && d.scenarios) ? d.scenarios : []; resolve(scenarios); })
        .catch(reject);
    });
    return readyPromise;
  }

  function list() {
    return (scenarios || []).map(function (s) {
      return { id: s.id, title: s.title, level: s.level, goal: s.goal, context: s.context };
    });
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function mount(el, scenarioId) {
    if (!el) return;
    ready().then(function (list2) {
      var sc = null;
      for (var i = 0; i < list2.length; i++) if (list2[i].id === scenarioId) sc = list2[i];
      if (!sc) { el.innerHTML = '<p class="muted">Scenario not found.</p>'; return; }
      run(el, sc);
    }).catch(function () {
      el.innerHTML = '<p class="muted">Conversation practice is unavailable right now. '
        + 'The rest of this page works normally.</p>';
    });
  }

  function run(el, sc) {
    var idx = 0;
    var lastFeedback = "";

    function render() {
      var step = sc.steps[idx];
      var html = "";
      html += '<p class="muted conv-tag">Deterministic practice — rule-based, not AI</p>';
      html += '<h3 class="conv-title">' + esc(sc.title) + '</h3>';
      html += '<p class="muted conv-context">' + esc(sc.context) + '</p>';
      html += '<div class="conv-npc"><span class="conv-npc-tag">' + esc(step.npc) + '</span>'
        + '<span class="conv-roman">' + esc(step.npc_roman) + '</span>'
        + '<span class="conv-en">' + esc(step.npc_en) + '</span></div>';
      html += '<p class="conv-prompt">' + esc(step.prompt) + '</p>';
      html += '<div class="conv-choices">';
      step.choices.forEach(function (c, ci) {
        html += '<button type="button" class="btn conv-choice" data-ci="' + ci + '">'
          + esc(c.text) + '<span class="conv-roman">' + esc(c.roman) + '</span>'
          + '<span class="conv-en">' + esc(c.en) + '</span></button>';
      });
      html += '</div>';
      if (lastFeedback) html += '<div class="note conv-fb" role="status">' + lastFeedback + '</div>';
      el.innerHTML = html;

      el.querySelectorAll(".conv-choice").forEach(function (b) {
        b.addEventListener("click", function () {
          var c = step.choices[parseInt(b.getAttribute("data-ci"), 10)];
          var correct = !!c.correct;
          var fb = correct
            ? '<b>✓ Correct.</b> ' + esc(step.explanation)
            : '<b>Not quite.</b> ' + esc(step.explanation)
              + (c.note ? ' <i>(' + esc(c.note) + ')</i>' : '');
          if (step.vocabulary && step.vocabulary.length) {
            fb += '<span class="conv-vocab">' + step.vocabulary.map(function (v) {
              return '<b>' + esc(v.target) + '</b> <span class="conv-roman">' + esc(v.roman)
                + '</span> — ' + esc(v.meaning);
            }).join(" · ") + '</span>';
          }
          lastFeedback = fb;
          var buttons = '<div style="margin-top:10px">';
          if (!correct) {
            buttons += '<button type="button" class="btn ghost conv-retry">Try that line again</button> ';
          }
          if (idx < sc.steps.length - 1) {
            buttons += '<button type="button" class="btn conv-next">Next line</button>';
          }
          buttons += '</div>';
          if (idx >= sc.steps.length - 1 && correct) {
            fb += '<div class="note" style="margin-top:10px"><b>Scenario complete.</b> '
              + esc(sc.completion) + '</div>'
              + '<div style="margin-top:8px"><button type="button" class="btn ghost conv-restart">Start this scenario again</button></div>';
          } else {
            fb += buttons;
          }
          el.innerHTML = '';
          var fbBox = document.createElement("div");
          fbBox.innerHTML = fb;
          el.appendChild(fbBox);
          var nxt = fbBox.querySelector(".conv-next");
          if (nxt) nxt.addEventListener("click", function () { idx++; lastFeedback = ""; render(); });
          var retry = fbBox.querySelector(".conv-retry");
          if (retry) retry.addEventListener("click", function () { lastFeedback = ""; render(); });
          var rst = fbBox.querySelector(".conv-restart");
          if (rst) rst.addEventListener("click", function () { idx = 0; lastFeedback = ""; render(); });
          if (correct && root.EkGuruProgress) {
            try { root.EkGuruProgress.recordQuiz("conversation-" + sc.id, 1, 1); } catch (e) {}
          }
        });
      });
    }
    render();
  }

  root.EkGuruConversation = { ready: ready, list: list, mount: mount };
})(typeof window !== "undefined" ? window : globalThis);
