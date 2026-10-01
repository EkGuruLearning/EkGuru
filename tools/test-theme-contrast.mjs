#!/usr/bin/env node
/* WCAG 2.x contrast for every per-language theme in light, dark and high-contrast modes, plus motion/voice size budgets. */
import fs from 'node:fs';
import zlib from 'node:zlib';
const read = (f) => fs.readFileSync(f, 'utf8');
const tokens = read('css/tokens.css');
function vars(selectorPattern) {
  const m = tokens.match(new RegExp(selectorPattern + '\\{([^}]*)\\}'));
  if (!m) throw new Error('token block missing: ' + selectorPattern);
  return Object.fromEntries([...m[1].matchAll(/--eg-([a-z-]+):(#[0-9a-fA-F]{6})/g)].map((x) => [x[1], x[2]]));
}
const base = {
  light: vars(String.raw`:root,html\[data-theme="light"\]`),
  dark: vars(String.raw`html\[data-theme="dark"\]`),
  contrast: vars(String.raw`html\[data-theme="contrast"\]`),
};
const lum = (hex) => {
  const c = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((v) => v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
  return .2126 * c[0] + .7152 * c[1] + .0722 * c[2];
};
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + .05) / (y + .05); };
let pairs = 0; const failures = [];
function need(label, fg, bg, min) {
  pairs++; const r = ratio(fg, bg);
  if (r < min) failures.push(`${label}: ${fg} on ${bg} = ${r.toFixed(2)} < ${min}`);
}
const registry = JSON.parse(read('data/languages/registry.json')).languages.filter((r) => r.course || r.starter_pack);
const themes = fs.readdirSync('data/themes').filter((f) => f.endsWith('.json')).map((f) => JSON.parse(read('data/themes/' + f)));
if (themes.length !== registry.length) failures.push(`theme count ${themes.length} != registry course/starter languages ${registry.length}`);
for (const theme of themes) {
  const reg = registry.find((r) => r.code === theme.code);
  if (!reg) { failures.push(`${theme.code}: theme without registry row`); continue; }
  if (theme.direction !== reg.direction) failures.push(`${theme.code}: direction ${theme.direction} != registry ${reg.direction}`);
  for (const mode of ['light', 'dark', 'contrast']) {
    const t = { ...base[mode], accent: theme[mode].accent, 'accent-contrast': theme[mode].accent_contrast };
    const L = `${theme.code}/${mode}`;
    need(L + ' ink/bg', t.ink, t.bg, 4.5); need(L + ' ink/surface', t.ink, t.surface, 4.5); need(L + ' ink/soft', t.ink, t.soft, 4.5);
    need(L + ' secondary/surface', t.secondary, t.surface, 4.5); need(L + ' secondary/soft', t.secondary, t.soft, 4.5);
    need(L + ' muted/bg', t.muted, t.bg, 4.5); need(L + ' muted/surface', t.muted, t.surface, 4.5);
    need(L + ' accent/bg', t.accent, t.bg, 4.5); need(L + ' accent/surface', t.accent, t.surface, 4.5);
    need(L + ' accent-contrast/accent', t['accent-contrast'], t.accent, 4.5);
    need(L + ' line/bg (UI border)', t.line, t.bg, 3); need(L + ' line/surface (UI border)', t.line, t.surface, 3);
    need(L + ' focus/bg', t.focus, t.bg, 3); need(L + ' focus/surface', t.focus, t.surface, 3);
    need(L + ' success/surface', t.success, t.surface, 4.5); need(L + ' error/surface', t.error, t.surface, 4.5);
  }
}
const gz = (f) => zlib.gzipSync(read(f)).length;
if (gz('js/ui-motion.js') > 12 * 1024) failures.push('js/ui-motion.js exceeds 12KB gzip');
if (fs.existsSync('js/voice.js') && Buffer.byteLength(read('js/voice.js')) > 10 * 1024) failures.push('js/voice.js exceeds 10KB');
if (!/prefers-reduced-motion:\s*reduce/.test(tokens) || !/prefers-reduced-motion:\s*reduce/.test(read('css/ultra.css'))) failures.push('reduced-motion CSS missing');
if (!/matchMedia\('\(prefers-reduced-motion: reduce\)'\)/.test(read('js/ui-motion.js'))) failures.push('ui-motion does not read reduced motion');
if (failures.length) { console.error('FAIL theme contrast/budgets\n' + failures.slice(0, 40).join('\n')); process.exit(1); }
console.log(`PASS theme contrast: ${themes.length} themes × 3 modes, ${pairs} semantic pairs; motion/voice budgets and reduced-motion hooks present`);
