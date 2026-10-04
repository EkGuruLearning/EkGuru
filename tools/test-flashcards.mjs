/* PHASE 9 gate — flashcard decks and the flashcard lab.
   Run:  node tools/test-flashcards.mjs          (needs: npm i jsdom)

   What it proves, in order:
     1. every deck (data/flashcards/<code>.json) has >= 200 cards,
        unique, safe ids; the JS twin (js/flashcards-<code>.js)
        carries exactly the same deck;
     2. every practice page that should carry the lab carries it,
        with its own deck, and a language without a deck gets none;
     3. the lab, in a real DOM: flip reveals the meaning and never
        hides the word, arrow keys move, chips filter, "Add to review"
        calls the shared SRS once, nothing speaks without a click,
        and prefers-reduced-motion is honoured.

   Exits 1 on the first failed expectation. */
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");
let failures = 0;

function check(name, ok, extra = "") {
  console.log(`${ok ? "ok  " : "FAIL"}  ${name}${extra ? "  — " + extra : ""}`);
  if (!ok) failures++;
}
function read(p) { return readFileSync(`${ROOT}/${p}`, "utf8"); }
/* Key order differs between the pretty JSON and the compact JS twin; the
   decks have to be equal, not identically formatted. */
function stable(v) {
  if (Array.isArray(v)) return "[" + v.map(stable).join(",") + "]";
  if (v && typeof v === "object") {
    return "{" + Object.keys(v).sort().map((k) => JSON.stringify(k) + ":" + stable(v[k])).join(",") + "}";
  }
  return JSON.stringify(v);
}
function json(p) { return JSON.parse(read(p)); }

/* ---------- 1. decks --------------------------------------------------- */
const decks = {};
const deckFiles = readdirSync(`${ROOT}/data/flashcards`).filter((f) => f.endsWith(".json"));
check("a deck exists for every language that authors vocabulary", deckFiles.length >= 38,
  `${deckFiles.length} decks`);

const ID_RE = /^[a-zA-Z0-9_.:-]{1,150}$/;
const RESERVED = ["__proto__", "constructor", "prototype"];
const CATS = ["greetings", "numbers", "food", "travel", "family", "time", "colors",
  "body", "verbs", "adjectives", "phrases", "nouns", "other"];
let thin = [], badIds = [], dupes = 0, missingLevel = 0, jsMismatch = 0;
for (const f of deckFiles) {
  const d = json(`data/flashcards/${f}`);
  const code = f.replace(/\.json$/, "");
  decks[code] = d;
  if (!Array.isArray(d.cards) || d.cards.length < 200) {
    thin.push(`${code}:${(d.cards || []).length}`);
  }
  const seen = new Set();
  for (const c of d.cards || []) {
    if (!ID_RE.test(c.id || "") || RESERVED.includes(c.id)) badIds.push(`${code}:${c.id}`);
    if (seen.has(c.id)) dupes++;
    seen.add(c.id);
    if (!c.t || !c.en) missingLevel++;
    if (!CATS.includes(c.cat)) badIds.push(`${code}:cat=${c.cat}`);
  }
  if (d.categories && Object.values(d.categories).reduce((a, b) => a + b, 0) !== d.cards.length) {
    jsMismatch++;
  }
  const jsPath = `js/flashcards-${code}.js`;
  if (!existsSync(`${ROOT}/${jsPath}`)) { jsMismatch++; continue; }
  const m = read(jsPath).match(/^window\.EKGURU_FLASHCARDS_[A-Z0-9_]+=(.*);$/m);
  const inJs = m ? JSON.parse(m[1]) : null;
  if (!inJs || stable(inJs) !== stable(d)) jsMismatch++;
}
check("every deck meets the 200-card minimum", thin.length === 0,
  thin.length ? thin.slice(0, 6).join(" ") : `${deckFiles.length} decks`);
check("card ids are unique, stable and SRS-safe", badIds.length === 0,
  badIds.slice(0, 3).join(" ") || "all clean");
check("no duplicate card ids", dupes === 0, `${dupes} duplicates`);
check("every card has a front and a meaning", missingLevel === 0, `${missingLevel} empty`);
check("each js/flashcards-<code>.js twin matches its JSON deck", jsMismatch === 0,
  `${jsMismatch} mismatched`);

/* ---------- 2. the lab is on the pages that have a deck ---------------- */
const INDIAN = { hindi: "hi", bengali: "bn", gujarati: "gu", kannada: "kn",
  malayalam: "ml", marathi: "mr", punjabi: "pa", tamil: "ta", telugu: "te", urdu: "ur" };
const pages = [];
for (const code of Object.keys(decks)) {
  const p = `languages/${code}/practice/index.html`;
  if (existsSync(`${ROOT}/${p}`)) pages.push([p, code]);
}
for (const [slug, code] of Object.entries(INDIAN)) {
  const p = `learn/${slug}/practice/index.html`;
  if (existsSync(`${ROOT}/${p}`) && decks[code]) pages.push([p, code]);
}
let missing = [], wrong = [], noScripts = [];
for (const [p, code] of pages) {
  const raw = read(p);
  if (!raw.includes("<!-- ekguru:flashcards:start -->")) { missing.push(p); continue; }
  if (!raw.includes(`data-eg-flashcards="${code}"`)) wrong.push(p);
  if (!raw.includes(`/js/flashcards-${code}.js`) || !raw.includes("/js/flashcard-ui.js")) noScripts.push(p);
  const first = decks[code].cards[0];
  if (!raw.includes(first.t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"))) {
    wrong.push(`${p} (static card missing)`);
  }
}
check("every practice page with a deck carries the lab", missing.length === 0,
  missing.slice(0, 4).join(" ") || `${pages.length} pages`);
check("each lab names its own language and shows a real card", wrong.length === 0,
  wrong.slice(0, 3).join(" ") || "all matched");
check("each lab loads its deck and the shared UI", noScripts.length === 0,
  noScripts.slice(0, 3).join(" ") || "all wired");
check("a language without a deck gets no lab", !read("learn/kannada/practice/index.html")
  .includes("ekguru:flashcards:start"));

/* ---------- 3. the lab in a DOM --------------------------------------- */
const dom = new JSDOM(
  `<!doctype html><html><body><div id="fc" data-eg-flashcards="hi"></div></body></html>`,
  { url: "https://ekguru.shop/learn/hindi/practice/", pretendToBeVisual: true, runScripts: "dangerously" });
const { window } = dom;
const doc = window.document;
let spoken = 0, spokenArgs = null;
window.speechSynthesis = { speak() { spoken++; }, cancel() {}, getVoices() { return []; } };
window.EkGuruVoice = { speak(text, lang, rate) { spoken++; spokenArgs = [text, lang, rate]; return true; } };
window.matchMedia = () => ({ matches: false, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} });
const srsCalls = [];
window.EkGuruGlobalSRS = { add: (spec) => { srsCalls.push(spec); return { id: "x", added: true }; } };
function evalFile(file) {
  const s = doc.createElement("script");
  s.textContent = read(file);
  doc.head.appendChild(s);
}
evalFile("js/flashcards-hi.js");
evalFile("js/flashcard-ui.js");

const el = doc.getElementById("fc");
check("the UI exposes a mount()", typeof window.EkGuruFlashcards?.mount === "function");
const api = window.EkGuruFlashcards.mount(el, { code: "hi", name: "Hindi", speech: "hi-IN" });
check("mount() renders a lab for the deck", !!api && api.count === decks.hi.cards.length,
  api ? `${api.count} cards` : "no api");
check("the lab never speaks on load", spoken === 0, `${spoken} utterances`);
check("the lab owns no speech engine of its own", !/speechSynthesis\.speak|SpeechSynthesisUtterance/
  .test(read("js/flashcard-ui.js")));

const card = () => doc.getElementById(el.querySelector(".fc-card").id);
const front = () => el.querySelector(".fc-side-front").childNodes[0].textContent;
const back = () => el.querySelector(".fc-side-back");
check("the front shows the language's own word", front() === decks.hi.cards[0].t, front());
check("the meaning starts hidden from assistive tech",
  back().getAttribute("aria-hidden") === "true" && !back().textContent.includes("undefined"));

const flip = el.querySelector('[data-fc="flip"]');
flip.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
check("clicking flips the card", card().getAttribute("data-flipped") === "true" &&
  flip.getAttribute("aria-pressed") === "true");
check("flipping reveals the meaning, never hides the word",
  back().getAttribute("aria-hidden") === "false" &&
  el.querySelector(".fc-side-front").getAttribute("aria-hidden") !== "true");
check("the meaning is the authored English gloss",
  back().textContent.trim() === decks.hi.cards[0].en, back().textContent.trim());

const before = front();
el.dispatchEvent(new window.KeyboardEvent("keydown", { key: "ArrowRight", bubbles: true }));
check("arrow keys move between cards", front() !== before, `${before} -> ${front()}`);
check("moving re-hides the meaning", back().getAttribute("aria-hidden") === "true");

const chip = el.querySelectorAll("[data-fc-cat]")[1];
const cat = chip.getAttribute("data-fc-cat");
chip.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
const shown = el.querySelector(".fc-progress").textContent;
const catCount = decks.hi.categories[cat];
check("a category chip filters the deck", shown.includes(`of ${catCount}`), `${cat}: ${shown}`);
check("the chip reports its pressed state",
  el.querySelector(`[data-fc-cat="${cat}"]`).getAttribute("aria-pressed") === "true");

el.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
const addBtn = el.querySelector('[data-fc="review"]');
addBtn.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
check("Add to review calls the shared SRS once", srsCalls.length === 1,
  `${srsCalls.length} calls`);
check("the saved card carries the deck's own text",
  srsCalls[0]?.prompt && srsCalls[0]?.answer && srsCalls[0]?.language === "hi");
check("the lab says where the card went", /review queue/i.test(el.querySelector(".fc-msg").textContent));

const speakBtn = el.querySelector('[data-fc="speak"]');
speakBtn.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
check("Speak only speaks after a click", spoken === 1, `${spoken} utterances`);
check("Speak goes through js/voice.js with the card's own tag",
  spokenArgs && spokenArgs[0] === front() && spokenArgs[1] === "hi-IN" && spokenArgs[2] === 0.8,
  JSON.stringify(spokenArgs));

/* reduced motion */
const dom2 = new JSDOM(`<!doctype html><html><body><div id="fc2" data-eg-flashcards="de"></div></body></html>`,
  { url: "https://ekguru.shop/languages/de/practice/", pretendToBeVisual: true, runScripts: "dangerously" });
dom2.window.matchMedia = () => ({ matches: true, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} });
const s2 = dom2.window.document.createElement("script");
s2.textContent = read("js/flashcards-de.js");
dom2.window.document.head.appendChild(s2);
const s3 = dom2.window.document.createElement("script");
s3.textContent = read("js/flashcard-ui.js");
dom2.window.document.head.appendChild(s3);
const el2 = dom2.window.document.getElementById("fc2");
dom2.window.EkGuruFlashcards.mount(el2, { code: "de", name: "German", speech: "de-DE" });
check("prefers-reduced-motion reaches the card",
  el2.querySelector(".fc-card").getAttribute("data-reduced-motion") === "true");
check("a lab for a language with no deck says so honestly",
  window.EkGuruFlashcards.mount(window.document.createElement("div"), { code: "xx" }) === null);

console.log(failures ? `\n${failures} check(s) failed` : "\nall flashcard checks passed");
process.exit(failures ? 1 : 0);
