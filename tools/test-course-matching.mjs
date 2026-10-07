/*
 * Regression test for the course player's word ↔ meaning matching activity.
 * It exercises the production pair builder and DOM renderer without jsdom,
 * then measures how much of the authored course-practice data can use the
 * vocabulary-backed matching UI without ambiguous duplicate meanings.
 *
 * Run: node tools/test-course-matching.mjs
 */
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
process.chdir(ROOT);

class FakeElement {
  constructor(tagName) {
    this.tagName = String(tagName).toUpperCase();
    this.children = [];
    this.attributes = Object.create(null);
    this.listeners = Object.create(null);
    this.className = "";
    this.textContent = "";
    this.value = "";
    this.disabled = false;
    this.parentNode = null;
    this.classList = {
      add: (...names) => {
        const classes = new Set(String(this.className || "").split(/\s+/).filter(Boolean));
        names.forEach((name) => classes.add(name));
        this.className = Array.from(classes).join(" ");
      },
      contains: (name) => String(this.className || "").split(/\s+/).includes(name),
    };
  }
  appendChild(child) {
    child.parentNode = this;
    this.children.push(child);
    return child;
  }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return Object.hasOwn(this.attributes, name) ? this.attributes[name] : null; }
  addEventListener(type, listener) { this.listeners[type] = listener; }
  click() {
    if (!this.disabled && this.listeners.click) this.listeners.click({ target: this, preventDefault() {} });
  }
}

const document = {
  readyState: "loading",
  createElement: (tagName) => new FakeElement(tagName),
  addEventListener() {},
};
const window = { addEventListener() {} };
const source = fs.readFileSync("js/course-player.js", "utf8");
vm.runInNewContext(source, {
  document,
  window,
  localStorage: { getItem: () => null, setItem() {} },
  Date,
  Math,
  console,
});
const Player = window.EKGURU_COURSE_PLAYER.Player;
const player = Object.create(Player.prototype);
const pairs = [
  { left: "नमस्ते", right: "hello" },
  { left: "धन्यवाद", right: "thank you" },
  { left: "माफ़ कीजिए", right: "sorry / excuse me" },
];

const plain = (value) => JSON.parse(JSON.stringify(value));
const descendants = (node, tagName) => {
  const found = [];
  const visit = (current) => {
    if (current.tagName === tagName) found.push(current);
    current.children.forEach(visit);
  };
  visit(node);
  return found;
};
let passed = 0;
function check(name, fn) {
  fn();
  passed++;
  console.log(`  ok  ${name}`);
}

console.log("\nCourse-player matching activity\n");
check("lesson vocabulary becomes distinct word–meaning pairs", () => {
  const vocab = [
    { t: "नमस्ते", en: "hello" },
    { t: "धन्यवाद", en: "thank you" },
    { t: "माफ़ कीजिए", en: "sorry / excuse me" },
    { t: "शुक्रिया", en: "thank you" }, // ambiguous duplicate gloss is omitted
    { t: "", en: "empty source" },
  ];
  assert.deepEqual(plain(player.matchingPairs({ type: "matching" }, vocab)), pairs);
});
check("explicit authored pairs take precedence and the activity is capped at six", () => {
  const explicit = Array.from({ length: 7 }, (_, i) => ({ left: `word ${i}`, right: `meaning ${i}` }));
  const result = plain(player.matchingPairs({ pairs: explicit }, [{ t: "ignored", en: "ignored" }]));
  assert.equal(result.length, 6);
  assert.equal(result[0].left, "word 0");
  assert.equal(result[5].right, "meaning 5");
});
check("fewer than two distinct pairs are left for the legacy fallback", () => {
  assert.equal(player.matchingPairs({ type: "matching" }, [{ t: "नमस्ते", en: "hello" }]).length, 1);
  assert.equal(player.matchingPairs({ pairs: [{ left: "one", right: "same" }, { left: "two", right: "same" }] }, []).length, 1);
});
check("the UI labels native-script terms and provides keyboard-native selects", () => {
  const host = new FakeElement("div");
  const activity = player.buildMatching(host, pairs, null, "hi");
  assert.equal(activity.selects.length, pairs.length);
  assert.equal(activity.check.tagName, "BUTTON");
  assert.equal(activity.check.getAttribute("type"), "button");
  assert.equal(activity.list.getAttribute("role"), "group");
  assert.equal(activity.list.getAttribute("aria-label"), "Vocabulary matching exercise");
  activity.rows.forEach((row, index) => {
    const label = row.children[0];
    const select = row.children[1];
    assert.equal(label.textContent, pairs[index].left);
    assert.equal(label.getAttribute("lang"), "hi");
    assert.equal(label.getAttribute("dir"), "auto");
    assert.equal(label.getAttribute("for"), select.getAttribute("id"));
    assert.match(select.getAttribute("aria-label"), /^Meaning for /);
    assert.equal(select.children.length, pairs.length + 1); // placeholder plus every meaning
  });
});
check("an incomplete set is not graded and can still be completed", () => {
  const host = new FakeElement("div");
  let result = null;
  const activity = player.buildMatching(host, pairs, (correct, message) => { result = { correct, message }; }, "hi");
  activity.check.click();
  assert.equal(result.correct, null);
  assert.match(result.message, /every word/);
  assert.equal(activity.check.disabled, false);
  assert.equal(activity.selects.every((select) => !select.disabled), true);
});
check("all correct pairs score once and lock the completed activity", () => {
  const host = new FakeElement("div");
  let result = null;
  const activity = player.buildMatching(host, pairs, (correct, message) => { result = { correct, message }; }, "hi");
  activity.selects.forEach((select, index) => { select.value = String(index); });
  activity.check.click();
  activity.check.click();
  assert.deepEqual(result, { correct: true, message: "All pairs matched." });
  assert.equal(activity.check.disabled, true);
  assert.equal(activity.selects.every((select) => select.disabled), true);
  assert.equal(activity.rows.every((row) => row.classList.contains("match-correct")), true);
});
check("a wrong match is scored once, marked invalid, and reveals the answer key", () => {
  const host = new FakeElement("div");
  let result = null;
  const activity = player.buildMatching(host, pairs, (correct, message, answerKey) => {
    result = { correct, message, answerKey };
  }, "hi");
  activity.selects.forEach((select, index) => { select.value = String(index); });
  activity.selects[0].value = "1";
  activity.check.click();
  assert.equal(result.correct, false);
  assert.match(result.message, /correct meanings/);
  assert.match(result.answerKey, /नमस्ते → hello/);
  assert.equal(activity.selects[0].getAttribute("aria-invalid"), "true");
  assert.equal(activity.selects[1].getAttribute("aria-invalid"), "false");
  assert.equal(activity.rows.every((row) => row.children.some((child) => child.className === "match-answer")), true);
});

console.log("\nExisting course-data coverage\n");
let matchingItems = 0;
let usableItems = 0;
for (const phase of fs.readdirSync("data/courses").filter((name) => /^phase-/.test(name)).sort()) {
  const phasePath = path.join("data/courses", phase);
  if (!fs.statSync(phasePath).isDirectory()) continue;
  for (const file of fs.readdirSync(phasePath).filter((name) => name.endsWith(".json"))) {
    const course = JSON.parse(fs.readFileSync(path.join(phasePath, file), "utf8"));
    for (const unit of (course.level && course.level.units) || []) {
      for (const lesson of (unit.lessons || [])) {
        for (const item of (lesson.practice || []).filter((question) => question.type === "matching")) {
          matchingItems++;
          if (player.matchingPairs(item, lesson.vocab || []).length >= 2) usableItems++;
        }
      }
    }
  }
}
assert.ok(matchingItems > 1000, `expected a substantial existing matching bank; found ${matchingItems}`);
assert.ok(usableItems / matchingItems >= 0.7,
  `expected ≥70% pair coverage without duplicate glosses; got ${usableItems}/${matchingItems}`);
console.log(`  ok  ${usableItems}/${matchingItems} authored matching prompts can use unambiguous lesson-vocabulary pairs`);
console.log(`\n${passed + 1} checks passed. This measures schema/rendering coverage, not independent linguistic review.\n`);
