/* =========================================================
   EkGuru — B12 voice-speed test (tools/test-tts-speed.mjs)

   P0: voice speed 0.1–1.0 in 0.1 steps on every voice
   surface, default 0.8×, persisted, no autoplay, honest
   "browser voice" labeling.

   Run: node tools/test-tts-speed.mjs
   ========================================================= */
import { JSDOM } from "jsdom";
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(new URL("..", import.meta.url).pathname);
const js = (f) => fs.readFileSync(path.join(ROOT, f), "utf8");
const tick = () => new Promise((r) => setTimeout(r, 40));

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log("  PASS  " + name); }
  catch (e) { fail++; console.log("  FAIL  " + name + " — " + e.message); }
}
function assert(c, m) { if (!c) throw new Error(m); }
function assertEq(a, b, m) {
  if (a !== b) throw new Error((m || "eq") + ` (got ${JSON.stringify(a)}, want ${JSON.stringify(b)})`);
}

/* speechSynthesis + SpeechSynthesisUtterance stub that captures
   every utterance and records which calls came from a gesture. */
function stubSpeech(w) {
  w.__utterances = [];
  w.__gesture = false;
  class U {
    constructor(text) { this.text = text; this.rate = 1; this.lang = ""; }
  }
  w.SpeechSynthesisUtterance = U;
  w.speechSynthesis = {
    speak(u) { w.__utterances.push({ u, fromGesture: w.__gesture }); },
    cancel() {}, getVoices() { return []; },
    addEventListener() {}, removeEventListener() {}
  };
}

function makeDom(html, url) {
  const dom = new JSDOM(html, { url: url || "https://ekguru.shop/test/", runScripts: "outside-only" });
  stubSpeech(dom.window);
  return dom;
}
function evalScripts(dom, files) {
  for (const f of files) dom.window.eval(js(f));
}

const EMOJI = /[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/u;

/* ---------------- A. module semantics ---------------- */
console.log("A. js/tts-speed.js — range, default, persistence, snapping");
{
  const dom = makeDom("<!doctype html><html><body></body></html>");
  evalScripts(dom, ["js/tts-speed.js"]);
  const T = dom.window.EKGURU_TTS;
  t("module exposed as window.EKGURU_TTS", () => assert(T && typeof T.getRate === "function" && typeof T.setRate === "function"));
  t("default rate is 0.8", () => assertEq(T.getRate(), 0.8));
  t("bounds constants 0.1 / 1.0 / 0.1 step / 0.8 default", () =>
    { assertEq(T.min, 0.1); assertEq(T.max, 1.0); assertEq(T.step, 0.1); assertEq(T.def, 0.8); });
  t("persists to localStorage key ekguru_tts_rate", () => {
    T.setRate(0.5);
    assertEq(dom.window.localStorage.getItem("ekguru_tts_rate"), "0.5");
    assertEq(T.getRate(), 0.5);
  });
  t("setRate snaps to 0.1 steps (0.42 -> 0.4, 0.96 -> 1.0)", () => {
    assertEq(T.setRate(0.42), 0.4);
    assertEq(T.setRate(0.96), 1.0);
  });
  t("setRate clamps into 0.1-1.0 (2 -> 1.0, 0.02 -> 0.1, junk -> 0.8)", () => {
    assertEq(T.setRate(2), 1.0);
    assertEq(T.setRate(0.02), 0.1);
    assertEq(T.setRate("junk"), 0.8);
  });
  t("legacy values migrate: 1.25->1.0, 0.85->0.9, 0.05->0.1, garbage->0.8", () => {
    for (const [stored, want] of [["1.25", 1.0], ["0.85", 0.9], ["0.05", 0.1], ["garbage", 0.8]]) {
      dom.window.localStorage.setItem("ekguru_tts_rate", stored);
      assertEq(T.getRate(), want, "stored " + stored);
    }
  });
}

/* ---------------- B. the pill ---------------- */
console.log("B. speed pill — mounting, cycling, honesty");
await (async () => {
  const dom = makeDom(
    "<!doctype html><html><body>" +
    '<script src="../js/storybook.js" defer></script>' +
    "</body></html>");
  evalScripts(dom, ["js/tts-speed.js"]);
  await tick();
  t("pill mounts on a page that loads a voice script", () => {
    const p = dom.window.document.querySelector(".sb-speed");
    assert(p, "no .sb-speed button found");
  });
  t("pill has no emoji", () => {
    const p = dom.window.document.querySelector(".sb-speed");
    assert(p && !EMOJI.test(p.innerHTML + p.title + p.getAttribute("aria-label")), "emoji found in pill");
  });
  t("pill labels the voice honestly (browser voice, not a recording)", () => {
    const p = dom.window.document.querySelector(".sb-speed");
    assert(p && /browser/i.test(p.title), "title lacks 'browser'");
    assert(p && /browser/i.test(p.getAttribute("aria-label") || ""), "aria-label lacks 'browser'");
  });
  t("pill starts at the persisted rate (0.8 default)", () => {
    const p = dom.window.document.querySelector(".sb-speed");
    assert(p && p.innerHTML.indexOf("0.8") >= 0, "pill does not show 0.8");
  });
  t("cycling walks 0.1 steps and wraps 1.0 -> 0.1", () => {
    const p = dom.window.document.querySelector(".sb-speed");
    const seq = [];
    for (let i = 0; i < 10; i++) { p.click(); seq.push(dom.window.EKGURU_TTS.getRate()); }
    assertEq(JSON.stringify(seq), JSON.stringify([0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]), "cycle order");
  });
  t("a pill click writes the new rate immediately (speak-time reads see it)", () => {
    const p = dom.window.document.querySelector(".sb-speed");
    p.click();
    const painted = parseFloat(p.querySelector("b").textContent);
    assertEq(dom.window.EKGURU_TTS.getRate(), painted, "pill write visible to getRate");
  });
  {
    const dom2 = makeDom("<!doctype html><html><body></body></html>");
    evalScripts(dom2, ["js/tts-speed.js"]);
    await tick();
    t("pill does NOT mount on a page with no voice script", () =>
      assert(!dom2.window.document.querySelector(".sb-speed"), "pill mounted without voice script"));
  }
  {
    const dom3 = makeDom("<!doctype html><html><body></body></html>");
    stubSpeech(dom3);
    delete dom3.window.speechSynthesis;
    evalScripts(dom3, ["js/tts-speed.js"]);
    await tick();
    t("no pill when speechSynthesis is unavailable", () =>
      assert(!dom3.window.document.querySelector(".sb-speed"), "pill without speechSynthesis"));
  }
})();

/* ---------------- C. speak-time rate on real surfaces ---------------- */
console.log("C. voice surfaces read the shared rate at speak time");
await (async () => {
  /* hindi-audio.js — full boot, real click, captured utterance */
  const dom = makeDom(
    "<!doctype html><html><body><p data-hi-audio=\"नमस्ते\">नमस्ते</p></body></html>");
  evalScripts(dom, ["js/tts-speed.js", "js/hindi-audio.js"]);
  await tick();
  t("hindi-audio: a tap speaks at the shared rate (0.3 after setRate)", () => {
    dom.window.EKGURU_TTS.setRate(0.3);
    const btn = dom.window.document.querySelector(".hi-listen");
    assert(btn, "no listen button booted");
    dom.window.__gesture = true;
    btn.click();
    const last = dom.window.__utterances[dom.window.__utterances.length - 1];
    assert(last, "no utterance captured");
    assertEq(last.u.rate, 0.3, "utterance rate");
  });
  t("hindi-audio: nothing spoke before the gesture (no autoplay)", () => {
    const before = dom.window.__utterances.filter((x) => !x.fromGesture).length;
    assertEq(before, 0, "utterances without a gesture");
  });
  t("hindi-audio: rate change applies to the NEXT utterance with no reload", () => {
    const btn = dom.window.document.querySelector(".hi-listen");
    btn.classList.remove("playing"); // stub never fires onend; toggle off first
    dom.window.EKGURU_TTS.setRate(0.7);
    dom.window.__gesture = true;
    btn.click();
    const u = dom.window.__utterances[dom.window.__utterances.length - 1].u;
    assertEq(u.rate, 0.7, "second utterance rate");
  });
  t("hindi-audio: the honest browser-voice label is on the page", () => {
    assert(dom.window.document.body.textContent.indexOf("browser's computer voice") >= 0,
      "honest label missing");
  });

  /* course-player.js — IIFE; prove no boot-time speech + the shared
     rate line is live in source (same one-liner hindi-audio proved
     above, same EKGURU_TTS read). */
  const dom2 = makeDom("<!doctype html><html><body></body></html>");
  evalScripts(dom2, ["js/tts-speed.js", "js/course-player.js"]);
  await tick();
  t("course-player: nothing speaks on page load (no autoplay)", () =>
    assertEq(dom2.window.__utterances.length, 0, "utterances after load"));
  const cp = js("js/course-player.js");
  t("course-player: speak() reads EKGURU_TTS with 0.8 fallback", () =>
    assert(/u\.rate = window\.EKGURU_TTS \? window\.EKGURU_TTS\.getRate\(\) : 0\.8/.test(cp), "rate line missing"));
})();

/* ---------------- D. source-level invariants ---------------- */
console.log("D. source invariants — no stale rates, no autoplay, honest labels");
{
  const sb = js("js/storybook.js");
  t("storybook: old 0.85 default and 1.25 rate removed", () =>
    { assert(!/0\.85/.test(sb), "0.85 still present"); assert(!/1\.25/.test(sb), "1.25 still present"); });
  t("storybook: speed-pill emoji (turtle/rabbit) removed", () =>
    assert(!sb.includes("\u{1F422}") && !sb.includes("\u{1F407}"), "turtle/rabbit emoji present"));
  t("storybook: no duplicate speed pill created", () =>
    assert(!/paintRate/.test(sb) && !/var RATES = /.test(sb), "old pill code remains"));
  t("storybook: reads the shared module at speak time", () =>
    assert(/window\.EKGURU_TTS\s*&&\s*window\.EKGURU_TTS\.getRate\(\)/.test(sb), "EKGURU_TTS read missing"));

  const pe = js("js/practice-engine.js");
  const ha = js("js/hindi-audio.js");
  t("practice-engine + hindi-audio: no literal rate passed to EkGuruVoice.speak", () =>
    { assert(!/EkGuruVoice\.speak\(String\(text\), tag, 0\.8\)/.test(pe), "practice-engine literal 0.8");
      assert(!/EkGuruVoice\.speak\(String\(text\), tag, 0\.8\)/.test(ha), "hindi-audio literal 0.8"); });

  for (const [f, code] of [["js/storybook.js", sb], ["js/course-player.js", cp2()],
                           ["js/practice-engine.js", pe], ["js/hindi-audio.js", ha]]) {
    t(f + ": no boot-time speechSynthesis.speak at IIFE top level", () => {
      const bad = code.split("\n").find((l) => /^\s{0,2}window\.speechSynthesis\.speak\(/.test(l));
      assert(!bad, "boot-time speak at: " + bad);
    });
  }
  t("hindi-audio: EkGuruAudioProvider still labels the voice honestly", () =>
    assert(/computer voice \(browser TTS\)/.test(ha), "honest provider label missing"));
}
function cp2() { return js("js/course-player.js"); }

/* ---------------- E. the injected script tag ---------------- */
console.log("E. site-wide injection — js/tts-speed.js on the real pages");
{
  const RE = /<script src="(\.\.\/)*js\/tts-speed\.js" defer><\/script>/;
  const probe = (f) => RE.test(fs.readFileSync(path.join(ROOT, f), "utf8"));
  t("injected on a storybook page (answers/)", () =>
    assert(probe("answers/best-hindi-movies-to-learn-hindi/index.html")));
  t("injected on a Hindi section page (hindi/)", () => assert(probe("hindi/index.html")));
  t("injected on the homepage", () => assert(probe("index.html")));
  const inject = js("tools/inject-modern.py");
  t("inject-modern.py lists tts-speed in MODERN_JS", () =>
    assert(inject.indexOf('("js/tts-speed.js", "tts-speed")') >= 0));
  const sw = js("sw.js");
  t("sw.js precaches ./js/tts-speed.js", () => assert(sw.indexOf('"./js/tts-speed.js"') >= 0));
  const count = (function () {
    let n = 0;
    for (const dir of fs.readdirSync(ROOT, { withFileTypes: true })) {
      if (!dir.isDirectory() || dir.name.startsWith(".")) continue;
      for (const sub of fs.readdirSync(path.join(ROOT, dir.name), { withFileTypes: true })) {
        if (!sub.isDirectory()) continue;
        const f = path.join(ROOT, dir.name, sub.name, "index.html");
        if (fs.existsSync(f) && RE.test(fs.readFileSync(f, "utf8"))) n++;
      }
    }
    return n;
  })();
  t("injected across the site (sample of section pages: " + count + ")", () => assert(count > 20));
}

console.log(`\ntts-speed: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
