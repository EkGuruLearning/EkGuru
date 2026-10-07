#!/usr/bin/env node
/* Render the generated Open Graph SVG batch with the pinned resvg renderer. */
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Resvg } from "@resvg/resvg-js";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const FONT_FILES = [
  path.join(ROOT, "tools/assets/og-fonts/DejaVuSans.ttf"),
  path.join(ROOT, "tools/assets/og-fonts/DejaVuSans-Bold.ttf"),
];
for (const fontFile of FONT_FILES) {
  if (!existsSync(fontFile)) throw new Error(`bundled font is missing: ${fontFile}`);
}
const checking = process.argv.includes("--check");
const items = JSON.parse(readFileSync(0, "utf8"));
if (!Array.isArray(items)) throw new Error("renderer input must be a JSON array");

let written = 0;
const stale = [];
const hashes = new Map();
const outputs = new Set();
for (const item of items) {
  if (!item || typeof item.svg !== "string" || typeof item.output !== "string") {
    throw new Error("each render item needs svg and output strings");
  }
  const target = path.resolve(ROOT, item.output);
  if (!target.startsWith(ROOT + path.sep)) throw new Error(`output escapes repository: ${item.output}`);
  if (outputs.has(target)) throw new Error(`duplicate output path: ${item.output}`);
  outputs.add(target);
  const renderer = new Resvg(item.svg, {
    textRendering: 2,
    font: {
      fontFiles: FONT_FILES,
      loadSystemFonts: false,
      defaultFontFamily: "DejaVu Sans",
      sansSerifFamily: "DejaVu Sans",
    },
  });
  const rendered = renderer.render();
  if (rendered.width !== 1200 || rendered.height !== 630) {
    throw new Error(`${item.output}: expected 1200x630, got ${rendered.width}x${rendered.height}`);
  }
  const png = rendered.asPng();
  if (png.length > 300_000) throw new Error(`${item.output}: PNG exceeds 300 KB (${png.length} bytes)`);
  const hash = createHash("sha256").update(png).digest("hex");
  if (hashes.has(hash)) throw new Error(`${item.output}: image duplicates ${hashes.get(hash)}`);
  hashes.set(hash, item.output);
  if (checking) {
    if (!existsSync(target) || !readFileSync(target).equals(png)) stale.push(item.output);
  } else if (!existsSync(target) || !readFileSync(target).equals(png)) {
    mkdirSync(path.dirname(target), { recursive: true });
    writeFileSync(target, png);
    written++;
  }
}

if (stale.length) {
  for (const output of stale.slice(0, 12)) console.error(`STALE ${output} — run tools/build-og-images.py`);
  if (stale.length > 12) console.error(`... and ${stale.length - 12} more stale PNG(s)`);
  process.exitCode = 1;
} else if (checking) {
  console.log(`ok    OG PNGs: ${items.length} deterministic 1200x630 render(s), each <=300 KB`);
} else {
  console.log(`OG PNGs: ${written} written; ${items.length} deterministic 1200x630 render(s), each <=300 KB`);
}
