#!/usr/bin/env node
/* Focused unit and page-contract checks for the browser-only Hindi text counter. */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { runInNewContext } from "node:vm";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const require = createRequire(import.meta.url);
const { measureText, sampleText } = require("../js/hindi-text-counter.js");
const page = readFileSync(path.join(ROOT, "toolbox/hindi-text-counter/index.html"), "utf8");
const hub = readFileSync(path.join(ROOT, "toolbox/index.html"), "utf8");
const registry = readFileSync(path.join(ROOT, "js/tool-registry.js"), "utf8");

const zero = {
  words: 0,
  codePoints: 0,
  charactersNoWhitespace: 0,
  sentenceEndings: 0,
  paragraphs: 0,
};
assert.deepEqual(measureText(""), zero, "empty input has zero counts");
assert.equal(measureText(" \t\r\n ").words, 0, "whitespace alone is not a word");
assert.equal(measureText(" \t\r\n ").charactersNoWhitespace, 0,
  "Unicode whitespace is removed only from the no-whitespace total");

const mixed = "नमस्ते दुनिया।\nHello, world!";
const mixedCounts = measureText(mixed);
assert.equal(mixedCounts.words, 4, "mixed Hindi/English words use whitespace tokens");
assert.equal(mixedCounts.sentenceEndings, 2, "Hindi danda and English exclamation are counted");
assert.equal(mixedCounts.paragraphs, 1, "a single line break stays in one paragraph");
assert.equal(mixedCounts.codePoints, Array.from(mixed).length,
  "the total counts Unicode code points, not UTF-16 code units");
assert.equal(mixedCounts.charactersNoWhitespace,
  Array.from(mixed).filter((character) => !/\s/u.test(character)).length,
  "the no-whitespace total removes whitespace code points");

const emoji = measureText("A🙏🏽");
assert.equal(emoji.words, 1);
assert.equal(emoji.codePoints, 3,
  "a supplementary emoji and skin-tone modifier each count as a code point");
assert.equal(emoji.charactersNoWhitespace, 3);

assert.equal(measureText("e\u0301").codePoints, 2,
  "a decomposed accent is not normalized or collapsed");
assert.equal(measureText("é").codePoints, 1,
  "precomposed and decomposed text can have different code-point totals");

const punctuation = measureText("Wait... Really?! ठीक॥");
assert.equal(punctuation.sentenceEndings, 3,
  "runs of period, question, exclamation, danda and double danda count once each");
assert.equal(measureText("Namaste Hindi").sentenceEndings, 0,
  "the tool does not infer sentence boundaries without a listed mark");

const paragraphs = measureText("first\r\nline\r\n \t\r\nsecond");
assert.equal(paragraphs.paragraphs, 2, "CRLF and whitespace-only blank lines split paragraphs");
assert.equal(paragraphs.words, 3, "a single line break does not split a word token");
assert.equal(measureText("\n \n").paragraphs, 0, "blank input has no non-empty paragraphs");

assert.equal(sampleText, "नमस्ते दुनिया।\nHello, world!", "sample content is stable");
assert.equal(measureText(sampleText).words, 4);

assert.match(page, /<title>Hindi Text Counter/);
assert.match(page, /<link rel="canonical" href="https:\/\/ekguru\.shop\/toolbox\/hindi-text-counter\/"/);
assert.equal((page.match(/<div[ >]/g) || []).length, page.split("</div>").length - 1,
  "the page's div containers are balanced");
assert.match(page, /data-ad-class="INTERACTIVE_LEARNING"/);
assert.match(page, /ekguru:shell-header:start/);
assert.match(page, /ekguru:shell-footer:start/);
assert.match(page, /ekguru:chapter/);
assert.match(page, /no Hindi speaker buttons/,
  "the storybook hint explains that this utility has no speech controls");
const ldJson = [...page.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)]
  .map((match) => JSON.parse(match[1]));
assert.ok(ldJson.some((block) => (block["@graph"] || []).some((entry) => entry["@type"] === "WebApplication")),
  "the page advertises its free utility without asserting editorial approval");
assert.match(hub, /href="\.\.\/toolbox\/hindi-text-counter\/"/);
assert.match(registry, /slug: "hindi-text-counter"/);
assert.match(registry, /last_tested: "pending"/);
assert.match(page, /id="tc-input"/);
assert.match(page, /id="tc-sample"/);
assert.match(page, /id="tc-copy"/);
assert.match(page, /id="tc-clear"/);
assert.match(page, /id="tc-code-points"/);
assert.match(page, /src="\.\.\/\.\.\/js\/hindi-text-counter\.js"/);
assert.match(page, /does not upload the text/i);
assert.match(page, /does not use grapheme-cluster segmentation/i);
assert.match(page, /whitespace-separated tokens/i);
assert.equal((page.match(/<main\b/g) || []).length, 1, "one main landmark");
assert.equal((page.match(/<h1\b/g) || []).length, 1, "one page heading");
assert.doesNotMatch(page, /adsbygoogle/i, "the utility page has no ad loader");

class FakeElement {
  constructor() {
    this.value = "";
    this.textContent = "";
    this.hidden = false;
    this.dataset = {};
    this.listeners = {};
    this.focused = false;
    this.selected = false;
  }
  addEventListener(type, callback) {
    (this.listeners[type] ||= []).push(callback);
  }
  dispatch(type) {
    for (const callback of this.listeners[type] || []) callback({ type, target: this });
  }
  click() { this.dispatch("click"); }
  focus() { this.focused = true; }
  select() { this.selected = true; }
}

function runUiSmoke(clipboard) {
  const ids = [
    "tc-input", "tc-words", "tc-code-points", "tc-no-whitespace",
    "tc-sentence-endings", "tc-paragraphs", "tc-status", "tc-metrics",
    "tc-nojs", "tc-clear", "tc-sample", "tc-copy",
  ];
  const elements = Object.fromEntries(ids.map((id) => [id, new FakeElement()]));
  elements["tc-metrics"].hidden = true;
  const document = {
    readyState: "complete",
    getElementById: (id) => elements[id] || null,
    addEventListener() {},
  };
  const window = { document, navigator: { clipboard } };
  const source = readFileSync(path.join(ROOT, "js/hindi-text-counter.js"), "utf8");
  runInNewContext(source, { window, globalThis: window });
  return elements;
}

const copied = [];
const ui = runUiSmoke({ writeText: (text) => Promise.resolve(copied.push(text)) });
assert.equal(ui["tc-metrics"].hidden, false, "initialization reveals live metrics");
assert.equal(ui["tc-nojs"].hidden, true, "initialization hides the no-JavaScript note");
ui["tc-input"].value = mixed;
ui["tc-input"].dispatch("input");
assert.equal(ui["tc-words"].textContent, "4", "input events update visible counts");
assert.equal(ui["tc-sentence-endings"].textContent, "2");
ui["tc-clear"].click();
assert.equal(ui["tc-input"].value, "", "clear empties the text field");
assert.equal(ui["tc-words"].textContent, "0", "clear resets counters");
assert.equal(ui["tc-input"].focused, true, "clear returns focus to the text field");
ui["tc-sample"].click();
assert.equal(ui["tc-input"].value, sampleText, "sample button fills the example");
ui["tc-copy"].click();
await new Promise((resolve) => setImmediate(resolve));
assert.deepEqual(copied, [sampleText], "copy button requests only the explicitly selected text");
assert.equal(ui["tc-status"].textContent, "Text copied to your clipboard.");

const noClipboard = runUiSmoke(undefined);
noClipboard["tc-input"].value = "copy manually";
noClipboard["tc-copy"].click();
assert.equal(noClipboard["tc-input"].selected, true, "clipboard fallback selects text for manual copying");
assert.match(noClipboard["tc-status"].textContent, /copy it manually/);

console.log("PASS  Hindi text counter: counting rules, UI events, copy fallback and page contract");
