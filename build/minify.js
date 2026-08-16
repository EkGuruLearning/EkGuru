/* =========================================================
   EkGuru — CSS minifier
   ---------------------------------------------------------
   Produces css/style.min.css from css/style.css.

   Deliberately conservative: it strips comments, collapses
   whitespace and drops the final semicolon in a block, and
   nothing else. It leaves strings, data URIs and content
   values untouched, and it verifies the brace balance and the
   rule count before writing, so a broken file can never ship.

   Edit css/style.css, never the .min file. Run this, then patch.js.
   ========================================================= */
const fs = require("fs");
const path = require("path");
const { ROOT } = require("./load.js");

const src = path.join(ROOT, "css", "style.css");
const out = path.join(ROOT, "css", "style.min.css");
const css = fs.readFileSync(src, "utf8");

/* walk the file so quoted strings are never touched */
let s = "";
let i = 0, inStr = null, inComment = false;
while (i < css.length) {
  const c = css[i], n = css[i + 1];
  if (inComment) { if (c === "*" && n === "/") { inComment = false; i += 2; } else i++; continue; }
  if (inStr) { s += c; if (c === "\\") { s += css[++i] || ""; } else if (c === inStr) inStr = null; i++; continue; }
  if (c === "/" && n === "*") { inComment = true; i += 2; continue; }
  if (c === '"' || c === "'") { inStr = c; s += c; i++; continue; }
  s += c; i++;
}
s = s.replace(/\s*([{};:,>~])\s*/g, "$1").replace(/;}/g, "}").replace(/\s+/g, " ").trim();

/* refuse to write anything that does not match the original structure */
const count = str => (str.match(/\{/g) || []).length;
const balance = str => {
  let d = 0, j = 0, cm = false;
  while (j < str.length) {
    if (!cm && str.slice(j, j + 2) === "/*") { cm = true; j += 2; continue; }
    if (cm && str.slice(j, j + 2) === "*/") { cm = false; j += 2; continue; }
    if (!cm) { if (str[j] === "{") d++; else if (str[j] === "}") d--; }
    j++;
  }
  return d;
};
if (count(s) !== count(css) || balance(s) !== 0) {
  console.error("minify: output did not match the source, refusing to write");
  process.exit(1);
}

fs.writeFileSync(out, s);
const pct = 100 - Math.round(s.length / css.length * 100);
console.log(`minify: style.css ${css.length} -> style.min.css ${s.length}  -${pct}%  (${count(s)} rules intact)`);
