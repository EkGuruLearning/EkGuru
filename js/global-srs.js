/* =========================================================
   EkGuru — GLOBAL SRS ENGINE v1
   ---------------------------------------------------------
   Implements P0-E: global SRS engine
   - language-neutral core
   - language-specific content
   - Storage namespace safe for multi-language use

   Cards may include:
   - vocabulary
   - phrases
   - sentence patterns
   - grammar patterns
   - mistakes
   - pronunciation contrasts
   - listening items
   - production prompts

   Do NOT add every question to SRS. Use selective eligibility.

   Namespace: ekguru:srs:<lang>:v1

   API: window.EkGuruGlobalSRS
   Extends Hindi SRS but global.
   ========================================================= */
(function(){
  "use strict";

  var VERSION = 1;
  var PREFIX = "ekguru:srs:";

  function storageKey(lang){
    lang = lang || "global";
    return PREFIX + lang + ":v" + VERSION;
  }

  function read(lang){
    var key = storageKey(lang);
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return {version: VERSION, cards:{}};
      var o = JSON.parse(raw);
      if (o && o.version===VERSION && o.cards) return o;
      return {version: VERSION, cards:{}};
    } catch(e){
      return {version: VERSION, cards:{}};
    }
  }

  function write(lang, o){
    var key = storageKey(lang);
    try {
      localStorage.setItem(key, JSON.stringify(o));
    } catch(e){}
  }

  function contentId(prompt, answer, lang){
    var s = (lang||"") + "|" + String(prompt||"") + "|" + String(answer||"");
    var h = 0;
    for (var i=0;i<s.length;i++){ h = (h*31 + s.charCodeAt(i))|0; }
    return "c" + Math.abs(h).toString(36);
  }

  var SRS = {
    version: VERSION,

    add: function(spec){
      var lang = spec.language || "global";
      var o = read(lang);
      var id = spec.card_id || contentId(spec.prompt, spec.answer, lang);
      if (o.cards[id]) return {id:id, added:false, card:o.cards[id]};

      // Selective eligibility — only add if eligible
      if (spec.srs_eligible===false) return {id:id, added:false, reason:"not eligible"};

      var now = Date.now();
      var card = {
        card_id: id,
        content_id: spec.content_id || id,
        language: lang,
        target: spec.target || spec.prompt || "",
        source: spec.source || "",
        prompt: spec.prompt || "",
        answer: spec.answer || "",
        category: spec.category || "vocabulary", // vocab, phrase, sentence, grammar, mistake, pronunciation, listening, production
        level: spec.level || "A1",
        skill: spec.skill || "vocabulary",
        country: spec.country || null,
        ease: 2.5,
        interval: 0,
        due_date: now,
        review_count: 0,
        last_reviewed: 0,
        version: VERSION,
        added_at: now,
        srs_eligible: true
      };
      o.cards[id] = card;
      write(lang, o);
      return {id:id, added:true, card:card};
    },

    has: function(id, lang){
      if (lang){
        return !!read(lang).cards[id];
      }
      // Check all languages
      var langs = SRS.languages();
      for (var i=0;i<langs.length;i++){
        if (read(langs[i]).cards[id]) return true;
      }
      return false;
    },

    languages: function(){
      var out = [];
      try {
        for (var i=0;i<localStorage.length;i++){
          var k = localStorage.key(i);
          if (k && k.indexOf(PREFIX)===0){
            var parts = k.split(":");
            if (parts.length>=3){
              var lang = parts[2];
              if (out.indexOf(lang)===-1) out.push(lang);
            }
          }
        }
      } catch(e){}
      return out;
    },

    due: function(lang, limit){
      var langs = lang ? [lang] : SRS.languages();
      var now = Date.now();
      var out = [];
      langs.forEach(function(l){
        var o = read(l);
        Object.keys(o.cards).forEach(function(id){
          var c = o.cards[id];
          if (c.due_date <= now) out.push(c);
        });
      });
      out.sort(function(a,b){ return a.due_date - b.due_date; });
      return limit ? out.slice(0, limit) : out;
    },

    all: function(lang){
      if (lang){
        var o = read(lang);
        return Object.keys(o.cards).map(function(id){ return o.cards[id]; });
      }
      var all = [];
      SRS.languages().forEach(function(l){
        var o = read(l);
        Object.keys(o.cards).forEach(function(id){ all.push(o.cards[id]); });
      });
      return all;
    },

    count: function(lang){
      if (lang) return Object.keys(read(lang).cards).length;
      var total = 0;
      SRS.languages().forEach(function(l){ total += Object.keys(read(l).cards).length; });
      return total;
    },

    dueCount: function(lang){
      return SRS.due(lang).length;
    },

    isDue: function(card_id, lang){
      if (lang){
        var c = read(lang).cards[card_id];
        return c && c.due_date <= Date.now();
      }
      var langs = SRS.languages();
      for (var i=0;i<langs.length;i++){
        var c = read(langs[i]).cards[card_id];
        if (c && c.due_date <= Date.now()) return true;
      }
      return false;
    },

    review: function(card_id, rating, lang){
      // rating: again, hard, good, easy
      var targetLang = lang;
      var o = null;
      var c = null;

      if (lang){
        o = read(lang);
        c = o.cards[card_id];
      } else {
        // Find card
        var langs = SRS.languages();
        for (var i=0;i<langs.length;i++){
          var o2 = read(langs[i]);
          if (o2.cards[card_id]){
            o = o2;
            c = o2.cards[card_id];
            targetLang = langs[i];
            break;
          }
        }
      }

      if (!c) return null;

      var day = 86400000;
      var interval = c.interval || 0;
      var ease = c.ease || 2.5;

      if (rating==="again"){
        interval = 0; ease = Math.max(1.3, ease-0.2);
      } else if (rating==="hard"){
        interval = Math.max(1, interval*1.2); ease = Math.max(1.3, ease-0.15);
      } else if (rating==="good"){
        interval = interval===0 ? 1 : Math.max(1, interval*ease);
      } else {
        interval = interval===0 ? 3 : Math.max(1, interval*ease*1.3);
        ease = Math.min(3.5, ease+0.15);
      }

      c.interval = Math.round(interval*10)/10;
      c.ease = Math.round(ease*100)/100;
      c.review_count = (c.review_count||0)+1;
      c.last_reviewed = Date.now();
      c.due_date = c.last_reviewed + Math.round(c.interval*day);
      o.cards[card_id] = c;
      write(targetLang, o);
      return c;
    },

    remove: function(card_id, lang){
      if (lang){
        var o = read(lang);
        if (!o.cards[card_id]) return false;
        delete o.cards[card_id];
        write(lang, o);
        return true;
      }
      var removed = false;
      SRS.languages().forEach(function(l){
        var o = read(l);
        if (o.cards[card_id]){
          delete o.cards[card_id];
          write(l, o);
          removed = true;
        }
      });
      return removed;
    },

    addMistake: function(question_id, lang, level, skill){
      // Auto-add mistake to SRS if eligible
      var id = "mistake-" + question_id;
      SRS.add({
        card_id: id,
        language: lang||"global",
        prompt: "Mistake: " + question_id,
        answer: "Review needed",
        category: "mistake",
        level: level||"A1",
        skill: skill||"general",
        srs_eligible: true
      });
    },

    // For UI
    getDueCardsByLanguage: function(){
      var out = {};
      SRS.languages().forEach(function(l){
        out[l] = SRS.due(l, 20);
      });
      return out;
    }
  };

  window.EkGuruGlobalSRS = SRS;

  // Backward compatibility: if Hindi SRS exists, expose global too
  if (window.EkGuruSRS){
    window.EkGuruSRS.global = SRS;
  }

  console.log("[EkGuruGlobalSRS] v1 loaded languages", SRS.languages().length);
})();
