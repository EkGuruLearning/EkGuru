import assert from "node:assert/strict";
import fs from "node:fs";
import vm from "node:vm";

let handler;
const document = { addEventListener(type, fn, capture) {
  assert.equal(type, "error");
  assert.equal(capture, true);
  handler = fn;
} };
vm.runInNewContext(fs.readFileSync("js/photo-fallback.js", "utf8"), {
  document, String, encodeURIComponent
});

const img = {
  tagName: "IMG",
  dataset: {},
  attributes: { "data-eg-photo-fallback": "" },
  src: "https://lh3.googleusercontent.com/d/1x6sYnW58CYKZeC9abLsEbM5Gd1nGivH4=w800",
  get currentSrc() { return this.src; },
  hasAttribute(name) { return Object.hasOwn(this.attributes, name); },
  removeAttribute(name) { delete this.attributes[name]; },
  onerror: null
};
const fail = () => handler({ target: img });

fail();
assert.equal(img.src, "https://drive.google.com/thumbnail?id=1x6sYnW58CYKZeC9abLsEbM5Gd1nGivH4&sz=w800");
fail();
assert.equal(img.src, "../../images/placeholder-tutor.jpg");
fail();
assert.match(img.src, /^data:image\/svg\+xml/);
console.log("PASS  Drive thumbnail retry -> local avatar -> inline fallback");
