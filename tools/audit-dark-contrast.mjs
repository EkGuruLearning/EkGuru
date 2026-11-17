#!/usr/bin/env node
/**
 * Dark-mode / light-mode text-contrast audit (WCAG 2.x ratios).
 *
 * Loads each page in headless Chromium with the EkGuru theme forced
 * (localStorage `ekguru:theme:v2` + html[data-theme]), scrolls once so lazy
 * sections mount, then walks EVERY text node and computes the contrast of its
 * colour against the painted background (walking up through translucent
 * parents). Prints the failures per page — "certain" = solid colours below
 * 4.5:1 (3:1 for large text), "unknown" = text over an image/gradient that
 * needs a human eye — and writes the full report to
 * /tmp/shot/contrast-<theme>-<width>.json.
 *
 * usage:
 *   python3 -m http.server 8765 &          # serve the repo
 *   node tools/audit-dark-contrast.mjs http://127.0.0.1:8765 dark 390 / /hindi/ /courses/
 *
 * Needs puppeteer-core + @sparticuz/chromium (npm i -D, not committed). 17 Nov 2026:
 * this is the audit behind the "25 — DARK / CONTRAST" block in css/ultra.css.
 */
import chromium from "@sparticuz/chromium";
import puppeteer from "puppeteer-core";
import fs from "node:fs";
const [,, base, theme, w, ...urls] = process.argv;
const browser = await puppeteer.launch({ args: chromium.args, executablePath: await chromium.executablePath(), headless: true });
const page = await browser.newPage();
await page.setViewport({ width: +w || 390, height: 844 });
await page.evaluateOnNewDocument((t) => { try { localStorage.setItem("ekguru:theme:v2", t); } catch (e) {} }, theme);
const report = {};
for (const u of urls) {
  try {
    await page.goto(base + u, { waitUntil: "load", timeout: 60000 });
  } catch (e) { report[u] = { error: e.message }; continue; }
  await page.evaluate((t) => document.documentElement.setAttribute("data-theme", t), theme);
  // reveal lazy things
  await page.evaluate(async () => {
    const h = document.documentElement.scrollHeight;
    for (let y = 0; y < h; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
    window.scrollTo(0, 0);
    document.querySelectorAll(".reveal,[data-reveal]").forEach(e => e.classList.add("in", "is-visible", "revealed"));
  });
  await new Promise(r => setTimeout(r, 600));
  report[u] = await page.evaluate(() => {
    const parse = (c) => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(",").map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
    const lum = ({ r, g, b }) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
    const blend = (fg, bg) => ({ r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1 });
    const ratio = (a, b) => { const l1 = lum(a), l2 = lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); };
    const bodyBg = parse(getComputedStyle(document.body).backgroundColor);
    const htmlBg = parse(getComputedStyle(document.documentElement).backgroundColor);
    const pageBg = (bodyBg && bodyBg.a > 0) ? bodyBg : (htmlBg && htmlBg.a > 0 ? htmlBg : { r: 255, g: 255, b: 255, a: 1 });
    function effBg(el) {
      let node = el, acc = null, unknown = false;
      while (node && node !== document.documentElement) {
        const cs = getComputedStyle(node);
        const bi = cs.backgroundImage;
        const bc = parse(cs.backgroundColor);
        if (bi && bi !== "none") { unknown = true; }
        if (bc && bc.a > 0) {
          if (bc.a >= 1 && !unknown) { return { bg: acc ? blend(acc, bc) : bc, unknown: false }; }
          acc = acc ? blend(acc, bc) : bc;
          if (bc.a >= 1) return { bg: acc, unknown };
        }
        node = node.parentElement;
      }
      const base = pageBg;
      return { bg: acc ? blend(acc, base) : base, unknown };
    }
    const sel = (el) => { const parts = []; let n = el; while (n && n !== document.body && parts.length < 4) { let s = n.tagName.toLowerCase(); if (n.id) s += "#" + n.id; else if (n.className && typeof n.className === "string") s += "." + n.className.trim().split(/\s+/).slice(0, 2).join("."); parts.unshift(s); n = n.parentElement; } return parts.join(">"); };
    const out = []; const seen = new Set();
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let t;
    while ((t = walker.nextNode())) {
      const txt = t.nodeValue.replace(/\s+/g, " ").trim();
      if (txt.length < 2) continue;
      const el = t.parentElement; if (!el) continue;
      if (["SCRIPT", "STYLE", "NOSCRIPT", "TEMPLATE", "OPTION"].includes(el.tagName)) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === "hidden" || cs.display === "none" || parseFloat(cs.opacity) < 0.3) continue;
      const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
      if (el.closest("[hidden],[aria-hidden='true'],details:not([open])>:not(summary)")) continue;
      let fg = parse(cs.color); if (!fg) continue;
      const { bg, unknown } = effBg(el);
      if (fg.a < 1) fg = blend(fg, bg);
      const fs = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight, 10) >= 700;
      const large = fs >= 24 || (fs >= 18.66 && bold);
      const need = large ? 3 : 4.5;
      const rt = ratio(fg, bg);
      if (rt < need) {
        const key = sel(el) + "|" + cs.color + "|" + Math.round(rt * 10);
        if (seen.has(key)) continue; seen.add(key);
        out.push({ sel: sel(el), text: txt.slice(0, 40), fg: cs.color, bg: `rgb(${Math.round(bg.r)},${Math.round(bg.g)},${Math.round(bg.b)})`, ratio: +rt.toFixed(2), need, unknown, fs });
      }
    }
    return { pageBg: `rgb(${pageBg.r},${pageBg.g},${pageBg.b})`, issues: out.sort((a, b) => a.ratio - b.ratio) };
  });
}
await browser.close();
fs.mkdirSync("/tmp/shot", { recursive: true });
fs.writeFileSync(`/tmp/shot/contrast-${theme}-${w}.json`, JSON.stringify(report, null, 1));
for (const [u, r] of Object.entries(report)) {
  if (r.error) { console.log(`\n## ${u}  ERROR ${r.error}`); continue; }
  const bad = r.issues.filter(i => !i.unknown), unk = r.issues.filter(i => i.unknown);
  console.log(`\n## ${u}  bg=${r.pageBg}  certain=${bad.length} gradient/unknown=${unk.length}`);
  for (const i of bad.slice(0, 25)) console.log(`  ${i.ratio}/${i.need}  ${i.fg} on ${i.bg}  ${i.sel}  "${i.text}"`);
  for (const i of unk.slice(0, 8)) console.log(`  ?${i.ratio}/${i.need}  ${i.fg} on ~${i.bg}  ${i.sel}  "${i.text}"`);
}
