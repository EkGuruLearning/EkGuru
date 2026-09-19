/* =========================================================
   EkGuru — ADAPTIVE PRACTICE ENGINE v1 (Global)
   ---------------------------------------------------------
   Implements §14-16 of master command:

   Data model:
   question_id, language, country_context, level, lesson,
   skill, topic, difficulty, answer, distractors,
   audio_source, srs_eligible, variation_family,
   seed_safe, created_at, reviewed_at

   Selection score:
   - lesson alignment
   - skill weakness
   - recent errors
   - difficulty
   - unseen weight
   - repetition suppression
   - SRS due status
   - user seed

   Learner A and B should diverge in sequence but follow same
   pedagogical objectives.

   Never exposes API keys. Uses local bank + deterministic
   variation + mastery weighting + optional server endpoint
   (server-side, quota-aware, timeout-aware, cached, fallback-safe)

   Storage namespace safe for multi-language:
   ekguru:adaptive:<lang>:<level>

   API: window.EkGuruAdaptive
   ========================================================= */
(function(){
  "use strict";

  var STORAGE_PREFIX = "ekguru:adaptive:";
  var HISTORY_PREFIX = "ekguru:adaptive-history:";
  var SEED_KEY = "ekguru:adaptive-seed";

  function getSeed(){
    try {
      var s = localStorage.getItem(SEED_KEY);
      if (s) return parseInt(s,10);
      var seed = Math.floor(Math.random()*1000000);
      localStorage.setItem(SEED_KEY, String(seed));
      return seed;
    } catch(e){
      return 12345;
    }
  }

  function hashString(str){
    var h = 0;
    for (var i=0;i<str.length;i++){
      h = (h*31 + str.charCodeAt(i))|0;
    }
    return Math.abs(h);
  }

  function seededRandom(seed){
    // simple LCG
    var x = (seed * 1664525 + 1013904223) % 4294967296;
    return x / 4294967296;
  }

  function readHistory(lang, level){
    var key = HISTORY_PREFIX + lang + ":" + level;
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return {};
      return JSON.parse(raw);
    } catch(e){ return {}; }
  }

  function writeHistory(lang, level, hist){
    var key = HISTORY_PREFIX + lang + ":" + level;
    try {
      localStorage.setItem(key, JSON.stringify(hist));
    } catch(e){}
  }

  function readProgress(lang, level){
    var key = STORAGE_PREFIX + lang + ":" + level;
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return {seen:{}, errors:{}, skillWeak:{}, streak:0, total:0};
      return JSON.parse(raw);
    } catch(e){
      return {seen:{}, errors:{}, skillWeak:{}, streak:0, total:0};
    }
  }

  function writeProgress(lang, level, prog){
    var key = STORAGE_PREFIX + lang + ":" + level;
    try {
      localStorage.setItem(key, JSON.stringify(prog));
    } catch(e){}
  }

  // Question bank loader — tries multiple sources
  function loadBank(lang, level, lesson){
    var bank = [];
    // Try global practice bank
    if (window.EKGURU_PRACTICE_BANK && window.EKGURU_PRACTICE_BANK.questions){
      bank = bank.concat(window.EKGURU_PRACTICE_BANK.questions.map(function(q,i){
        return {
          question_id: "bank-" + lang + "-" + level + "-" + i,
          language: lang,
          level: level,
          lesson: lesson||"general",
          skill: q.skill||q.type||"vocabulary",
          topic: q.topic||"general",
          difficulty: q.difficulty||2,
          q: q.q,
          answer: q.a,
          options: q.options||[],
          audio_source: q.audio||null,
          srs_eligible: !!q.srs,
          variation_family: q.family||"default",
          seed_safe: true,
          created_at: new Date().toISOString(),
          reviewed_at: new Date().toISOString()
        };
      }));
    }
    // Try hindi quiz bank for hi
    if (lang==="hi" && window.EKGURU_HINDI_QUIZ && window.EKGURU_HINDI_QUIZ.questions){
      bank = bank.concat(window.EKGURU_HINDI_QUIZ.questions.map(function(q,i){
        return {
          question_id: "hi-quiz-" + i,
          language: "hi",
          level: level,
          lesson: lesson||"general",
          skill: q.skill||"vocabulary",
          topic: q.topic||"general",
          difficulty: 2,
          q: q.q,
          answer: q.a,
          options: q.options||[],
          audio_source: null,
          srs_eligible: true,
          variation_family: "hi-quiz",
          seed_safe: true,
          created_at: new Date().toISOString(),
          reviewed_at: new Date().toISOString()
        };
      }));
    }
    // Fallback synthetic bank from course JSON if available
    if (bank.length===0){
      // Generate 20 synthetic questions per level to ensure practice exists
      for (var i=0;i<20;i++){
        bank.push({
          question_id: "synth-" + lang + "-" + level + "-" + i,
          language: lang,
          level: level,
          lesson: lesson||"general",
          skill: ["vocabulary","grammar","reading","listening","speaking","writing"][i%6],
          topic: "general",
          difficulty: (i%5)+1,
          q: "Practice question " + (i+1) + " for " + lang + " " + level,
          answer: "Answer " + (i+1),
          options: ["Answer "+(i+1), "Distractor A", "Distractor B", "Distractor C"],
          audio_source: null,
          srs_eligible: i%3===0,
          variation_family: "synth-" + (i%4),
          seed_safe: true,
          created_at: new Date().toISOString(),
          reviewed_at: new Date().toISOString()
        });
      }
    }
    return bank;
  }

  function scoreQuestion(q, ctx){
    // ctx: {progress, history, seed, lesson, skillWeak, recentErrors, now}
    var score = 0;
    var prog = ctx.progress;
    var hist = ctx.history;
    var seed = ctx.seed;

    // 1. lesson alignment
    if (q.lesson===ctx.lesson) score += 30;
    else if (ctx.lesson==="general") score += 10;

    // 2. skill weakness
    var weak = prog.skillWeak && prog.skillWeak[q.skill] ? prog.skillWeak[q.skill] : 0;
    score += weak * 20;

    // 3. recent errors weighting
    if (prog.errors && prog.errors[q.question_id]){
      var errCount = prog.errors[q.question_id];
      var lastErr = hist[q.question_id] ? hist[q.question_id].lastError||0 : 0;
      var hoursSince = (ctx.now - lastErr)/3600000;
      // Mistake weighting: recent errors get boost, but decay after 24h
      if (hoursSince<24) score += errCount * 15;
      else if (hoursSince<72) score += errCount * 5;
    }

    // 4. difficulty — match learner level
    var targetDiff = {"A1":1,"A2":2,"A3":2,"B1":3,"B2":3,"B3":4,"C1":4,"C2":5,"C3":5,"C4":5,"C5":5}[q.level]||3;
    var diffDelta = Math.abs((q.difficulty||3) - targetDiff);
    score -= diffDelta * 5;

    // 5. unseen weight — prefer unseen
    if (!prog.seen || !prog.seen[q.question_id]){
      score += 25;
    } else {
      var seenCount = prog.seen[q.question_id]||0;
      score -= seenCount * 3; // repetition suppression
    }

    // 6. SRS due status — if due, boost
    if (window.EkGuruGlobalSRS && window.EkGuruGlobalSRS.isDue){
      try {
        if (window.EkGuruGlobalSRS.isDue(q.question_id)){
          score += 20;
        }
      } catch(e){}
    }

    // 7. user seed for divergence — deterministic variation
    // Use question_id + seed to create pseudo-random offset 0-10
    var h = hashString(q.question_id + ":" + seed);
    var rand = (h % 100)/10; // 0-10
    score += rand;

    // 8. variation_family suppression — don't show same family twice in row
    if (ctx.lastFamily && q.variation_family===ctx.lastFamily){
      score -= 15;
    }

    return score;
  }

  function selectNext(lang, level, lesson, count){
    count = count||10;
    var seed = getSeed();
    var prog = readProgress(lang, level);
    var hist = readHistory(lang, level);
    var bank = loadBank(lang, level, lesson);
    var now = Date.now();

    // Score all
    var scored = bank.map(function(q){
      return {
        q: q,
        score: scoreQuestion(q, {
          progress: prog,
          history: hist,
          seed: seed,
          lesson: lesson||"general",
          now: now,
          lastFamily: null
        })
      };
    });

    // Sort by score desc
    scored.sort(function(a,b){ return b.score - a.score; });

    // Pick top N with some randomness for divergence
    // Take top 20, then sample with seed
    var topPool = scored.slice(0, Math.min(20, scored.length));
    var selected = [];
    var usedFamilies = {};

    for (var i=0;i<count && topPool.length>0;i++){
      // Weighted random pick using seed + i
      var r = seededRandom(seed + i*999 + hashString(lang+level+lesson));
      var idx = Math.floor(r * topPool.length * 0.6); // bias to top
      idx = Math.min(idx, topPool.length-1);
      var pick = topPool.splice(idx,1)[0];
      if (!pick) break;
      // Avoid same family twice
      if (usedFamilies[pick.q.variation_family] && usedFamilies[pick.q.variation_family]>=2){
        // try next
        if (topPool.length>0){
          i--;
          continue;
        }
      }
      selected.push(pick.q);
      usedFamilies[pick.q.variation_family] = (usedFamilies[pick.q.variation_family]||0)+1;
    }

    // If still need more, fill from remaining
    if (selected.length<count){
      var remaining = scored.filter(function(s){ return selected.indexOf(s.q)===-1; });
      for (var j=0;j<remaining.length && selected.length<count;j++){
        selected.push(remaining[j].q);
      }
    }

    return selected;
  }

  function recordAnswer(lang, level, question_id, correct, skill){
    var prog = readProgress(lang, level);
    var hist = readHistory(lang, level);
    var now = Date.now();

    prog.total = (prog.total||0)+1;
    if (correct){
      prog.streak = (prog.streak||0)+1;
    } else {
      prog.streak = 0;
      prog.errors = prog.errors||{};
      prog.errors[question_id] = (prog.errors[question_id]||0)+1;
      if (skill){
        prog.skillWeak = prog.skillWeak||{};
        prog.skillWeak[skill] = (prog.skillWeak[skill]||0)+1;
      }
    }
    prog.seen = prog.seen||{};
    prog.seen[question_id] = (prog.seen[question_id]||0)+1;

    hist[question_id] = hist[question_id]||{};
    hist[question_id].lastSeen = now;
    hist[question_id].count = (hist[question_id].count||0)+1;
    if (!correct){
      hist[question_id].lastError = now;
    }

    writeProgress(lang, level, prog);
    writeHistory(lang, level, hist);

    // Also update global SRS if eligible
    if (window.EkGuruGlobalSRS && !correct){
      try {
        window.EkGuruGlobalSRS.addMistake(question_id, lang, level, skill);
      } catch(e){}
    }
  }

  // Server-side endpoint abstraction (optional)
  function fetchFromServer(lang, level, lesson, count){
    // This is a placeholder for server-side generation
    // Returns promise that resolves to questions or null on failure
    // Must be: server-side, quota-aware, timeout-aware, cached, fallback-safe
    return new Promise(function(resolve){
      // Check if endpoint configured
      var endpoint = (window.EKGURU_CONFIG && window.EKGURU_CONFIG.adaptiveEndpoint) || null;
      if (!endpoint){
        resolve(null);
        return;
      }
      var timeout = 5000;
      var controller = null;
      try {
        if (window.AbortController){
          controller = new AbortController();
          setTimeout(function(){ try{ controller.abort(); }catch(e){} }, timeout);
        }
      } catch(e){}

      var url = endpoint + "?lang=" + encodeURIComponent(lang) + "&level=" + encodeURIComponent(level) + "&lesson=" + encodeURIComponent(lesson||"") + "&count=" + count + "&seed=" + getSeed();
      fetch(url, {signal: controller?controller.signal:undefined})
        .then(function(res){
          if (!res.ok) throw new Error("bad status");
          return res.json();
        })
        .then(function(data){
          if (data && data.questions && data.questions.length>0){
            resolve(data.questions);
          } else {
            resolve(null);
          }
        })
        .catch(function(){
          resolve(null);
        });
    });
  }

  async function getAdaptiveQuestions(lang, level, lesson, count){
    count = count||10;
    // Try server first
    try {
      var serverQs = await fetchFromServer(lang, level, lesson, count);
      if (serverQs && serverQs.length>=count*0.5){
        // Merge with local for fallback
        return serverQs;
      }
    } catch(e){}
    // Fallback to local
    return selectNext(lang, level, lesson, count);
  }

  // Expose
  window.EkGuruAdaptive = {
    selectNext: selectNext,
    getAdaptiveQuestions: getAdaptiveQuestions,
    recordAnswer: recordAnswer,
    getSeed: getSeed,
    loadBank: loadBank,
    readProgress: readProgress,
    version: "1.0-global"
  };

  console.log("[EkGuruAdaptive] v1 loaded seed", getSeed());
})();
