/*
 * Regression test for the course player's sentence-reordering activity.
 * Exercises the production builder with a small DOM double and measures
 * existing lesson-practice coverage. This is not browser or language QA.
 *
 * Run: node tools/test-course-reorder.mjs
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
const deterministicMath = Object.create(Math);
deterministicMath.random = () => 0;
const source = fs.readFileSync("js/course-player.js", "utf8");
vm.runInNewContext(source, {
  document,
  window,
  localStorage: { getItem: () => null, setItem() {} },
  Date,
  Math: deterministicMath,
  console,
});
const Player = window.EKGURU_COURSE_PLAYER.Player;
const player = Object.create(Player.prototype);

let passed = 0;
function check(name, fn) {
  fn();
  passed++;
  console.log(`  ok  ${name}`);
}
function bySourceOrder(buttons) {
  return buttons.slice().sort((left, right) =>
    Number(left.getAttribute("data-token-index")) - Number(right.getAttribute("data-token-index")));
}

console.log("\nCourse-player sentence reordering\n");
check("renders semantic, labelled buttons and a live sentence preview", () => {
  const host = new FakeElement("div");
  const answer = "We will learn together.";
  const activity = player.buildReorder(host, answer, null, "en");
  assert.ok(activity);
  assert.equal(activity.buttons.length, 4);
  assert.equal(activity.buttons.every((button) => button.tagName === "BUTTON"), true);
  assert.equal(activity.buttons.every((button) => button.getAttribute("type") === "button"), true);
  assert.equal(activity.buttons.every((button) => /^Word \d+: /.test(button.getAttribute("aria-label"))), true);
  assert.equal(activity.buttons.every((button) => button.getAttribute("lang") === "en"), true);
  assert.equal(activity.buttons.every((button) => button.getAttribute("dir") === "auto"), true);
  assert.equal(activity.pool.getAttribute("role"), "group");
  assert.equal(activity.pool.getAttribute("lang"), "en");
  assert.equal(activity.pool.getAttribute("dir"), "auto");
  assert.equal(activity.builtBox.getAttribute("role"), "status");
  assert.equal(activity.builtBox.getAttribute("aria-live"), "polite");
  assert.equal(activity.builtBox.getAttribute("lang"), "en");
  assert.equal(activity.builtBox.getAttribute("dir"), "auto");
  assert.notEqual(activity.buttons.map((button) => button.getAttribute("data-token-index")).join(","), "0,1,2,3");
  assert.equal(activity.builtBox.textContent, "— choose words above —");
});
check("words toggle in sentence order without losing button focus, and Clear resets", () => {
  const host = new FakeElement("div");
  const activity = player.buildReorder(host, "red green blue", null, "en");
  const original = bySourceOrder(activity.buttons);
  original[2].click();
  original[0].click();
  assert.equal(activity.builtBox.textContent, "blue red");
  assert.equal(original[2].disabled, false);
  assert.equal(original[2].getAttribute("aria-pressed"), "true");
  original[2].click();
  assert.equal(activity.builtBox.textContent, "red");
  assert.equal(original[2].getAttribute("aria-pressed"), "false");
  original[2].click();
  assert.equal(activity.builtBox.textContent, "red blue");
  activity.clear.click();
  assert.equal(activity.builtBox.textContent, "— choose words above —");
  assert.equal(original.every((button) => !button.disabled), true);
  assert.equal(original.every((button) => button.getAttribute("aria-pressed") === "false"), true);
});
check("incomplete attempts remain unscored and a completed correct order scores once", () => {
  const host = new FakeElement("div");
  const results = [];
  const activity = player.buildReorder(host, "one two three", (correct, message, answer) => {
    results.push({ correct, message, answer });
  }, "en");
  const original = bySourceOrder(activity.buttons);
  original[0].click();
  activity.check.click();
  assert.equal(results.at(-1).correct, null);
  assert.match(results.at(-1).message, /every word once/i);
  assert.equal(activity.check.disabled, false);
  activity.clear.click();
  assert.equal(results.at(-1).message, "");
  original.forEach((button) => button.click());
  activity.check.click();
  activity.check.click();
  assert.deepEqual(results.at(-1), { correct: true, message: "Correct order.", answer: "one two three" });
  assert.equal(results.filter((result) => result.correct === true).length, 1);
  assert.equal(activity.check.disabled, true);
  assert.equal(activity.clear.disabled, true);
  assert.equal(original.every((button) => button.disabled), true);
});
check("an incorrect order returns the exact authored answer for feedback", () => {
  const host = new FakeElement("div");
  let result = null;
  const answer = "go home now";
  const activity = player.buildReorder(host, answer, (correct, message, answerKey) => {
    result = { correct, message, answerKey };
  }, "en");
  const original = bySourceOrder(activity.buttons);
  [original[1], original[0], original[2]].forEach((button) => button.click());
  activity.check.click();
  assert.equal(result.correct, false);
  assert.equal(result.answerKey, answer);
  assert.equal(activity.check.disabled, true);
});
check("single-token answers are left to the existing text-entry fallback", () => {
  assert.equal(player.buildReorder(new FakeElement("div"), "धन्यवाद!", null, "hi"), null);
});

console.log("\nExisting lesson-practice data coverage\n");
let reorderItems = 0;
let multiWordItems = 0;
let finalTestReorderItems = 0;
for (const phase of fs.readdirSync("data/courses").filter((name) => /^phase-/.test(name)).sort()) {
  const phasePath = path.join("data/courses", phase);
  if (!fs.statSync(phasePath).isDirectory()) continue;
  for (const file of fs.readdirSync(phasePath).filter((name) => name.endsWith(".json"))) {
    const course = JSON.parse(fs.readFileSync(path.join(phasePath, file), "utf8"));
    for (const unit of (course.level && course.level.units) || []) {
      for (const lesson of (unit.lessons || [])) {
        for (const item of (lesson.practice || []).filter((question) => question.type === "reorder")) {
          reorderItems++;
          if (String(item.answer || "").trim().split(/\s+/).filter(Boolean).length > 1) multiWordItems++;
        }
      }
    }
    for (const item of ((course.test && course.test.items) || [])) {
      if (item.type === "reorder") finalTestReorderItems++;
    }
  }
}
assert.ok(reorderItems > 1000, `expected a substantial existing reorder bank; found ${reorderItems}`);
assert.ok(multiWordItems / reorderItems >= 0.9,
  `expected ≥90% multi-word reorder coverage; got ${multiWordItems}/${reorderItems}`);
console.log(`  ok  ${multiWordItems}/${reorderItems} existing prompts can use the word-order interaction; single-token prompts retain text entry; ${finalTestReorderItems} final-test reorder items currently exist`);
console.log(`\n${passed + 1} checks passed. This measures interaction/schema coverage, not browser QA or linguistic review.\n`);
