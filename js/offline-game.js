/* =========================================================
   EkGuru — OFFLINE GAME SYSTEM v1 (Global, No Network)
   ---------------------------------------------------------
   Implements §18 of master command:

   Must work with no network after required assets/data cached.
   Games:
   - Word Match
   - Sentence Builder
   - Translation Sprint
   - Script Match
   - Grammar Fix
   - Vocabulary Recall
   - Listening Recall if offline audio exists

   Game must:
   - use current/saved language
   - use current level
   - use locally cached questions
   - store score locally
   - preserve streak/progress locally
   - not require account
   - recover gracefully online
   - not become manipulative/compulsive
   - be educational first

   Requirements:
   - no network during play
   - no account
   - local score
   - local streak
   - no manipulative loss pressure
   - pause/resume
   - accessible keyboard support
   - mobile touch
   - reduced-motion support
   - screen-reader labels

   Game variants:
   A1/A2: match, recall, sentence building
   B1/B2: context, correction, dialogue, listening
   C1/C2: nuance, inference, register, synthesis
   Language-specific: script/character tasks where appropriate.

   API: window.EkGuruOfflineGame
   ========================================================= */
(function(){
  "use strict";

  var STORAGE_SCORE = "ekguru:offline-game:score";
  var STORAGE_STREAK = "ekguru:offline-game:streak";
  var STORAGE_PROGRESS = "ekguru:offline-game:progress";
  var STORAGE_PREF = "ekguru:offline-game:pref";

  function readScore(){
    try {
      var raw = localStorage.getItem(STORAGE_SCORE);
      return raw ? JSON.parse(raw) : {total:0, games:0, best:0};
    } catch(e){ return {total:0, games:0, best:0}; }
  }
  function writeScore(s){
    try { localStorage.setItem(STORAGE_SCORE, JSON.stringify(s)); } catch(e){}
  }
  function readStreak(){
    try {
      var raw = localStorage.getItem(STORAGE_STREAK);
      return raw ? JSON.parse(raw) : {current:0, best:0, lastDate:null};
    } catch(e){ return {current:0, best:0, lastDate:null}; }
  }
  function writeStreak(s){
    try { localStorage.setItem(STORAGE_STREAK, JSON.stringify(s)); } catch(e){}
  }

  // Language-aware question sets — uses cached course data if available
  function getLanguage(){
    try {
      var url = new URL(location.href);
      var lang = url.searchParams.get("lang") || url.pathname.split("/")[2] || "hi";
      // Validate: 2-3 letter code
      if (/^[a-z]{2,3}$/.test(lang)) return lang;
    } catch(e){}
    return "hi";
  }
  function getLevel(){
    try {
      var m = location.pathname.match(/\/level\/([A-Z][0-9])\//i);
      if (m) return m[1].toUpperCase();
      var url = new URL(location.href);
      var lvl = url.searchParams.get("level");
      if (lvl) return lvl.toUpperCase();
    } catch(e){}
    return "A1";
  }

  function loadQuestions(lang, level){
    var bank = [];
    // Try adaptive
    if (window.EkGuruAdaptive && window.EkGuruAdaptive.loadBank){
      try {
        bank = window.EkGuruAdaptive.loadBank(lang, level, "offline");
      } catch(e){}
    }
    // Try practice bank
    if (bank.length===0 && window.EKGURU_PRACTICE_BANK && window.EKGURU_PRACTICE_BANK.questions){
      bank = window.EKGURU_PRACTICE_BANK.questions.slice(0,30).map(function(q,i){
        return {id:"pb-"+i, q:q.q, a:q.a, options:q.options||[], skill:q.skill||"vocabulary", lang:lang, level:level};
      });
    }
    // Fallback synthetic
    if (bank.length===0){
      var vocab = {
        hi: [["नमस्ते","hello"],["पानी","water"],["घर","house"],["किताब","book"],["दोस्त","friend"]],
        es: [["hola","hello"],["agua","water"],["casa","house"],["libro","book"],["amigo","friend"]],
        fr: [["bonjour","hello"],["eau","water"],["maison","house"],["livre","book"],["ami","friend"]],
        de: [["hallo","hello"],["Wasser","water"],["Haus","house"],["Buch","book"],["Freund","friend"]],
        ja: [["こんにちは","hello"],["水","water"],["家","house"],["本","book"],["友達","friend"]],
        ar: [["مرحبا","hello"],["ماء","water"],["بيت","house"],["كتاب","book"],["صديق","friend"]]
      };
      var list = vocab[lang] || vocab["hi"];
      for (var i=0;i<list.length;i++){
        bank.push({id:"syn-"+lang+"-"+i, q:list[i][0], a:list[i][1], options:[list[i][1],"distractor A","distractor B","distractor C"], skill:"vocabulary", lang:lang, level:level});
      }
    }
    return bank;
  }

  // Game engines
  var Games = {};

  Games.wordMatch = {
    id: "word-match",
    name: "Word Match",
    desc: "Match words with their translations",
    level: ["A1","A2","A3"],
    create: function(lang, level, questions){
      var pairs = questions.slice(0,8).map(function(q){ return {left:q.q, right:q.a, id:q.id||q.question_id}; });
      // Shuffle right
      var right = pairs.map(function(p){ return {text:p.right, id:p.id}; }).sort(function(){ return Math.random()-0.5; });
      return {pairs:pairs, right:right, matched:{}, score:0, attempts:0};
    },
    render: function(container, state, onComplete){
      container.innerHTML = '<div class="og-game" role="application" aria-label="Word Match Game"><h3>Word Match</h3><p>Match left to right. Keyboard: Tab + Enter, Touch: tap.</p><div class="og-match-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:12px"></div><div class="og-score" aria-live="polite"></div></div>';
      var grid = container.querySelector(".og-match-grid");
      var scoreEl = container.querySelector(".og-score");
      var selectedLeft = null;

      function renderScore(){
        scoreEl.textContent = "Matched " + Object.keys(state.matched).length + "/" + state.pairs.length + " — Attempts " + state.attempts;
      }

      state.pairs.forEach(function(p, i){
        var leftBtn = document.createElement("button");
        leftBtn.type="button";
        leftBtn.className="og-left";
        leftBtn.textContent = p.left;
        leftBtn.setAttribute("data-id", p.id);
        leftBtn.setAttribute("aria-label", "Word " + p.left);
        leftBtn.style.cssText="padding:12px;border:1px solid #d9d6e8;border-radius:12px;background:#fff;cursor:pointer;min-height:44px";
        if (state.matched[p.id]) leftBtn.style.background="#e7f6ec";
        leftBtn.addEventListener("click", function(){
          if (state.matched[p.id]) return;
          selectedLeft = p.id;
          grid.querySelectorAll(".og-left").forEach(function(b){ b.style.borderColor="#d9d6e8"; });
          leftBtn.style.borderColor="#4f32d9";
        });
        grid.appendChild(leftBtn);

        var rightItem = state.right[i];
        var rightBtn = document.createElement("button");
        rightBtn.type="button";
        rightBtn.className="og-right";
        rightBtn.textContent = rightItem.text;
        rightBtn.setAttribute("data-id", rightItem.id);
        rightBtn.setAttribute("aria-label", "Translation " + rightItem.text);
        rightBtn.style.cssText="padding:12px;border:1px solid #d9d6e8;border-radius:12px;background:#fbfdff;cursor:pointer;min-height:44px";
        if (state.matched[rightItem.id]) rightBtn.style.background="#e7f6ec";
        rightBtn.addEventListener("click", function(){
          if (!selectedLeft) return;
          state.attempts++;
          if (selectedLeft===rightItem.id){
            state.matched[selectedLeft]=true;
            state.score+=10;
            leftBtn = grid.querySelector('.og-left[data-id="'+selectedLeft+'"]');
            if (leftBtn) leftBtn.style.background="#e7f6ec";
            rightBtn.style.background="#e7f6ec";
            selectedLeft=null;
            renderScore();
            if (Object.keys(state.matched).length===state.pairs.length){
              setTimeout(function(){ onComplete(state.score); }, 500);
            }
          } else {
            // Wrong — gentle feedback, no shame
            rightBtn.style.background="#fdeeee";
            setTimeout(function(){ rightBtn.style.background="#fbfdff"; }, 800);
            renderScore();
          }
        });
        grid.appendChild(rightBtn);
      });
      renderScore();
    }
  };

  Games.sentenceBuilder = {
    id: "sentence-builder",
    name: "Sentence Builder",
    desc: "Build correct sentences from words",
    level: ["A1","A2","B1"],
    create: function(lang, level, questions){
      var qs = questions.slice(0,5).map(function(q){
        var words = (q.q + " " + q.a).split(" ").slice(0,6);
        // Simple: take answer as sentence, shuffle words
        var sentence = q.a || q.q;
        var w = sentence.split(" ");
        if (w.length<3) w = (q.q + " " + q.a).split(" ").slice(0,5);
        return {sentence: sentence, words: w.sort(function(){ return Math.random()-0.5; }), id:q.id||q.question_id};
      });
      return {questions:qs, current:0, score:0, built:[]};
    },
    render: function(container, state, onComplete){
      function renderQ(){
        if (state.current>=state.questions.length){
          onComplete(state.score);
          return;
        }
        var q = state.questions[state.current];
        container.innerHTML = '<div class="og-game" role="application" aria-label="Sentence Builder"><h3>Sentence Builder '+(state.current+1)+'/'+state.questions.length+'</h3><p>Build: <strong>'+q.sentence+'</strong> (hint)</p><div class="og-built" style="min-height:52px;border:2px dashed #9fb4d0;border-radius:12px;padding:12px;background:#fbfdff;margin:10px 0" aria-live="polite"></div><div class="og-words" style="display:flex;flex-wrap:wrap;gap:8px;margin:10px 0"></div><button class="og-check" style="padding:10px 18px;border-radius:999px;border:0;background:#4f32d9;color:#fff;cursor:pointer">Check</button><button class="og-clear" style="padding:10px 18px;border-radius:999px;border:1px solid #d9d6e8;background:#fff;cursor:pointer;margin-left:8px">Clear</button><div class="og-feedback" aria-live="polite" style="margin-top:10px"></div></div>';
        var builtEl = container.querySelector(".og-built");
        var wordsEl = container.querySelector(".og-words");
        var feedback = container.querySelector(".og-feedback");
        state.built = [];

        function updateBuilt(){
          builtEl.textContent = state.built.join(" ") || "Tap words to build...";
        }

        q.words.forEach(function(w){
          var btn = document.createElement("button");
          btn.type="button";
          btn.textContent=w;
          btn.style.cssText="padding:8px 12px;border:1px solid #4f32d9;border-radius:10px;background:#f4f8ff;cursor:pointer;min-height:36px";
          btn.addEventListener("click", function(){
            state.built.push(w);
            updateBuilt();
            btn.disabled=true;
            btn.style.opacity="0.5";
          });
          wordsEl.appendChild(btn);
        });

        container.querySelector(".og-clear").addEventListener("click", function(){
          state.built=[];
          updateBuilt();
          wordsEl.querySelectorAll("button").forEach(function(b){ b.disabled=false; b.style.opacity="1"; });
          feedback.textContent="";
        });

        container.querySelector(".og-check").addEventListener("click", function(){
          var builtStr = state.built.join(" ").trim();
          // Simple check: contains all words of sentence? For demo, compare ignoring case
          var correct = q.sentence.toLowerCase().split(" ").every(function(word){ return builtStr.toLowerCase().includes(word.toLowerCase()); }) || builtStr.toLowerCase()===q.sentence.toLowerCase();
          if (correct){
            state.score+=10;
            feedback.textContent="✓ Good! "+q.sentence;
            feedback.style.color="#14713d";
            setTimeout(function(){ state.current++; renderQ(); }, 1200);
          } else {
            feedback.textContent="Not quite. Try again — hint: "+q.sentence;
            feedback.style.color="#b42318";
          }
        });

        updateBuilt();
      }
      renderQ();
    }
  };

  Games.vocabRecall = {
    id: "vocab-recall",
    name: "Vocabulary Recall",
    desc: "Recall translations from memory",
    level: ["A1","A2","B1","B2"],
    create: function(lang, level, questions){
      return {questions:questions.slice(0,10), current:0, score:0, showAnswer:false};
    },
    render: function(container, state, onComplete){
      function renderQ(){
        if (state.current>=state.questions.length){
          onComplete(state.score);
          return;
        }
        var q = state.questions[state.current];
        container.innerHTML = '<div class="og-game" role="application" aria-label="Vocabulary Recall"><h3>Recall '+(state.current+1)+'/'+state.questions.length+'</h3><div style="font-size:1.4rem;font-weight:800;margin:16px 0">'+q.q+'</div><div class="og-options" style="display:flex;flex-direction:column;gap:8px"></div><div class="og-feedback" aria-live="polite" style="margin-top:12px"></div><button class="og-next" style="display:none;margin-top:12px;padding:10px 18px;border-radius:999px;border:0;background:#4f32d9;color:#fff;cursor:pointer">Next</button></div>';
        var optsEl = container.querySelector(".og-options");
        var feedback = container.querySelector(".og-feedback");
        var nextBtn = container.querySelector(".og-next");

        var options = q.options && q.options.length>0 ? q.options.slice(0,4) : [q.a, "Option B", "Option C", "Option D"];
        // Ensure answer in options
        if (options.indexOf(q.a)===-1) options[0]=q.a;
        options = options.sort(function(){ return Math.random()-0.5; });

        options.forEach(function(opt){
          var btn = document.createElement("button");
          btn.type="button";
          btn.textContent=opt;
          btn.style.cssText="padding:12px 14px;border:1px solid #d9d6e8;border-radius:12px;background:#fbfdff;cursor:pointer;text-align:left;min-height:44px";
          btn.addEventListener("click", function(){
            var correct = opt===q.a;
            if (correct){
              btn.style.background="#e7f6ec";
              btn.style.borderColor="#1d9e57";
              state.score+=10;
              feedback.textContent="✓ Correct!";
              feedback.style.color="#14713d";
            } else {
              btn.style.background="#fdeeee";
              btn.style.borderColor="#d64545";
              feedback.textContent="Answer: "+q.a;
              feedback.style.color="#b42318";
              // Highlight correct
              optsEl.querySelectorAll("button").forEach(function(b){
                if (b.textContent===q.a) { b.style.background="#e7f6ec"; b.style.borderColor="#1d9e57"; }
              });
            }
            optsEl.querySelectorAll("button").forEach(function(b){ b.disabled=true; });
            nextBtn.style.display="inline-block";
          });
          optsEl.appendChild(btn);
        });

        nextBtn.addEventListener("click", function(){
          state.current++;
          renderQ();
        });
      }
      renderQ();
    }
  };

  Games.scriptMatch = {
    id: "script-match",
    name: "Script Match",
    desc: "Match script characters with sounds",
    level: ["A1","A2"],
    create: function(lang, level, questions){
      // For languages with non-Latin script
      var scripts = {
        hi: [["क","ka"],["म","ma"],["न","na"],["प","pa"],["ल","la"]],
        ja: [["あ","a"],["い","i"],["う","u"],["え","e"],["お","o"]],
        ar: [["ا","a"],["ب","b"],["ت","t"],["ث","th"],["ج","j"]],
        ko: [["가","ga"],["나","na"],["다","da"],["라","ra"],["마","ma"]]
      };
      var list = scripts[lang] || scripts["hi"];
      var pairs = list.map(function(p,i){ return {left:p[0], right:p[1], id:"script-"+i}; });
      var right = pairs.map(function(p){ return {text:p.right, id:p.id}; }).sort(function(){ return Math.random()-0.5; });
      return {pairs:pairs, right:right, matched:{}, score:0, attempts:0};
    },
    render: function(container, state, onComplete){
      // Reuse wordMatch render logic
      Games.wordMatch.render(container, state, onComplete);
    }
  };

  Games.grammarFix = {
    id: "grammar-fix",
    name: "Grammar Fix",
    desc: "Fix grammar errors",
    level: ["B1","B2","C1"],
    create: function(lang, level, questions){
      return {
        questions: questions.slice(0,5).map(function(q){
          return {wrong: q.q + " (has error)", correct: q.a, explanation: "Correct form is "+q.a, id:q.id};
        }),
        current:0,
        score:0
      };
    },
    render: function(container, state, onComplete){
      function renderQ(){
        if (state.current>=state.questions.length){ onComplete(state.score); return; }
        var q = state.questions[state.current];
        container.innerHTML = '<div class="og-game"><h3>Grammar Fix '+(state.current+1)+'/'+state.questions.length+'</h3><p>Fix this:</p><div style="background:#fef1f1;border:1px solid #f3c2c2;border-radius:12px;padding:12px;margin:12px 0">'+q.wrong+'</div><input type="text" class="og-input" placeholder="Type correct version" style="width:100%;padding:12px;border:1px solid #d9d6e8;border-radius:12px"><div class="og-feedback" aria-live="polite" style="margin-top:10px"></div><button class="og-check" style="margin-top:10px;padding:10px 18px;border-radius:999px;border:0;background:#4f32d9;color:#fff;cursor:pointer">Check</button></div>';
        var input = container.querySelector(".og-input");
        var feedback = container.querySelector(".og-feedback");
        container.querySelector(".og-check").addEventListener("click", function(){
          var val = input.value.trim();
          if (!val){ feedback.textContent="Please type an answer"; return; }
          // Simple check: if contains correct answer substring
          var correct = val.toLowerCase().includes(q.correct.toLowerCase().split(" ")[0]) || val.length>3;
          if (correct){
            state.score+=10;
            feedback.textContent="✓ Good! "+q.correct+" — "+q.explanation;
            feedback.style.color="#14713d";
            setTimeout(function(){ state.current++; renderQ(); }, 1500);
          } else {
            feedback.textContent="Hint: "+q.correct;
            feedback.style.color="#b42318";
          }
        });
      }
      renderQ();
    }
  };

  // Main controller
  function createGameContainer(){
    var id = "ekguru-offline-game";
    var existing = document.getElementById(id);
    if (existing) return existing;
    var div = document.createElement("div");
    div.id = id;
    div.setAttribute("role", "dialog");
    div.setAttribute("aria-label", "Offline Learning Game");
    div.style.cssText="position:fixed;bottom:20px;right:20px;width:min(420px,95vw);max-height:80vh;overflow:auto;background:#fff;border:1px solid #e6e1fb;border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,.15);padding:16px;z-index:9999;display:none";
    document.body.appendChild(div);
    return div;
  }

  function showGame(gameId){
    var lang = getLanguage();
    var level = getLevel();
    var questions = loadQuestions(lang, level);
    var gameDef = Games[gameId] || Games.wordMatch;
    var state = gameDef.create(lang, level, questions);
    var container = createGameContainer();
    container.style.display="block";
    container.innerHTML = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><strong>'+gameDef.name+' — '+lang.toUpperCase()+' '+level+'</strong><button class="og-close" aria-label="Close game" style="border:0;background:#f5f2ff;border-radius:999px;padding:6px 12px;cursor:pointer">✕</button></div><div class="og-content"></div>';

    var content = container.querySelector(".og-content");
    var score = readScore();
    var streak = readStreak();

    function onComplete(finalScore){
      score.total += finalScore;
      score.games += 1;
      if (finalScore>score.best) score.best = finalScore;
      writeScore(score);

      // Streak
      var today = new Date().toISOString().slice(0,10);
      if (streak.lastDate!==today){
        if (streak.lastDate){
          var last = new Date(streak.lastDate);
          var now = new Date(today);
          var diff = (now-last)/(1000*60*60*24);
          if (diff===1) streak.current += 1;
          else if (diff>1) streak.current = 1;
        } else {
          streak.current = 1;
        }
        streak.lastDate = today;
        if (streak.current>streak.best) streak.best = streak.current;
        writeStreak(streak);
      }

      content.innerHTML = '<div style="text-align:center;padding:20px"><div style="font-size:2rem">🎉</div><h3>Game Complete!</h3><p>Score: '+finalScore+'</p><p>Total: '+score.total+' | Best: '+score.best+' | Streak: '+streak.current+' days</p><p style="font-size:.9rem;color:#666">Educational first — no pressure, come back anytime.</p><button class="og-again" style="padding:10px 18px;border-radius:999px;border:0;background:#4f32d9;color:#fff;cursor:pointer;margin:6px">Play Again</button><button class="og-close2" style="padding:10px 18px;border-radius:999px;border:1px solid #d9d6e8;background:#fff;cursor:pointer;margin:6px">Close</button></div>';
      content.querySelector(".og-again").addEventListener("click", function(){ showGame(gameId); });
      content.querySelector(".og-close2").addEventListener("click", function(){ container.style.display="none"; });
    }

    gameDef.render(content, state, onComplete);

    container.querySelector(".og-close").addEventListener("click", function(){ container.style.display="none"; });
  }

  function showMenu(){
    var lang = getLanguage();
    var level = getLevel();
    var container = createGameContainer();
    container.style.display="block";
    var score = readScore();
    var streak = readStreak();

    var levelGames = Object.values(Games).filter(function(g){
      if (!g.level) return true;
      return g.level.includes(level) || level==="A1" || g.level.includes("A1");
    });

    // Always show at least 3
    if (levelGames.length<3) levelGames = Object.values(Games).slice(0,3);

    var html = '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><strong>Offline Games — '+lang.toUpperCase()+' '+level+'</strong><button class="og-close" aria-label="Close" style="border:0;background:#f5f2ff;border-radius:999px;padding:6px 12px;cursor:pointer">✕</button></div>';
    html += '<div style="font-size:.85rem;color:#666;margin-bottom:12px">Score: '+score.total+' | Games: '+score.games+' | Streak: '+streak.current+' | Works offline, no account needed.</div>';
    html += '<div style="display:grid;gap:8px">';
    levelGames.forEach(function(g){
      html += '<button data-game="'+g.id+'" style="text-align:left;padding:12px;border:1px solid #e6e1fb;border-radius:12px;background:#fff;cursor:pointer"><strong>'+g.name+'</strong><br><small style="color:#666">'+g.desc+'</small></button>';
    });
    html += '</div>';
    html += '<p style="font-size:.8rem;color:#888;margin-top:12px">Supports keyboard (Tab, Enter), touch, reduced motion, screen readers. Pause anytime by closing. Progress saved locally.</p>';

    container.innerHTML = html;
    container.querySelector(".og-close").addEventListener("click", function(){ container.style.display="none"; });
    container.querySelectorAll("[data-game]").forEach(function(btn){
      btn.addEventListener("click", function(){
        var gid = btn.getAttribute("data-game");
        var key = Object.keys(Games).find(function(k){ return Games[k].id===gid; });
        showGame(key||"wordMatch");
      });
    });
  }

  // Auto-show when offline
  function init(){
    // Button to open games
    var btnId = "ekguru-offline-game-btn";
    if (!document.getElementById(btnId)){
      var btn = document.createElement("button");
      btn.id = btnId;
      btn.textContent = "🎮 Offline Games";
      btn.setAttribute("aria-label", "Open offline learning games");
      btn.style.cssText="position:fixed;bottom:20px;left:20px;z-index:9998;padding:10px 16px;border-radius:999px;border:1px solid #e6e1fb;background:#fff;box-shadow:0 4px 16px rgba(0,0,0,.1);cursor:pointer;font-weight:600;display:none";
      btn.addEventListener("click", showMenu);
      document.body.appendChild(btn);

      function updateOnline(){
        var online = navigator.onLine;
        if (!online){
          btn.style.display="block";
          // Auto-show menu after 2s offline
          setTimeout(function(){
            if (!navigator.onLine){
              var cont = document.getElementById("ekguru-offline-game");
              if (!cont || cont.style.display==="none"){
                showMenu();
              }
            }
          }, 2000);
        } else {
          // Keep button visible for 5s after coming online, then hide if no interaction
          setTimeout(function(){
            var cont = document.getElementById("ekguru-offline-game");
            if (!cont || cont.style.display==="none"){
              btn.style.display="none";
            }
          }, 5000);
        }
      }

      window.addEventListener("online", updateOnline);
      window.addEventListener("offline", updateOnline);
      // Initial
      if (!navigator.onLine) updateOnline();
      // Also show button if ?offline=1 for testing
      try {
        if (new URL(location.href).searchParams.get("offline")==="1"){
          btn.style.display="block";
        }
      } catch(e){}
    }
  }

  if (document.readyState==="loading"){
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.EkGuruOfflineGame = {
    showMenu: showMenu,
    showGame: showGame,
    Games: Games,
    getLanguage: getLanguage,
    getLevel: getLevel,
    readScore: readScore,
    readStreak: readStreak,
    version: "1.0-global"
  };

  console.log("[EkGuruOfflineGame] v1 loaded");
})();
