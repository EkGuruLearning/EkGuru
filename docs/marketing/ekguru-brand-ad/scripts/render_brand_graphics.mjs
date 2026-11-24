import fs from 'fs';
import path from 'path';
import { Resvg } from '/tmp/ad_node/node_modules/@resvg/resvg-js/index.js';

const ROOT = path.resolve('docs/marketing/ekguru-brand-ad');
const FONTS_DIR = path.join(ROOT, '05_brand_graphics/fonts');
const OUT_DIR = path.join(ROOT, '05_brand_graphics');

const fontFiles = fs.readdirSync(FONTS_DIR)
  .filter(f => f.endsWith('.ttf'))
  .map(f => path.join(FONTS_DIR, f));

const devPaths = JSON.parse(fs.readFileSync(path.join(OUT_DIR, 'devanagari_paths.json'), 'utf8'));

function renderSvgToPng(svgString, outPath, width) {
  const resvg = new Resvg(svgString, {
    fitTo: { mode: 'width', value: width },
    font: {
      fontFiles,
      loadSystemFonts: false,
      defaultFontFamily: 'Inter',
    },
  });
  const pngData = resvg.render();
  fs.writeFileSync(outPath, pngData.asPng());
  console.log('Rendered:', outPath, `${pngData.width}x${pngData.height}`);
}

const LOGO_DEFS = `
    <linearGradient id="goldRule" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0"/>
      <stop offset="50%" stop-color="#fcd34d" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="eg_bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5b3df5"/>
      <stop offset="52%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
    <linearGradient id="eg_flame" x1="0.5" y1="1" x2="0.5" y2="0">
      <stop offset="0%" stop-color="#f59e0b"/>
      <stop offset="45%" stop-color="#fbbf24"/>
      <stop offset="100%" stop-color="#fff7d6"/>
    </linearGradient>
    <linearGradient id="eg_pgL" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f0ecff"/>
    </linearGradient>
    <linearGradient id="eg_pgR" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#e3dcff"/>
    </linearGradient>
    <radialGradient id="eg_glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#fbbf24" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#fbbf24" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#000000" flood-opacity="0.58"/>
    </filter>`;

function officialLogoGroup(cx, topY, size) {
  const x = cx - size / 2;
  const s = size / 512;
  return `<g transform="translate(${x}, ${topY}) scale(${s})" filter="url(#softShadow)">
    <rect width="512" height="512" rx="116" fill="url(#eg_bg)"/>
    <circle cx="256" cy="150" r="104" fill="url(#eg_glow)"/>
    <path d="M256 62c0 0 8 30 54 54 16 18 26 34 26 54a56 56 0 11-112 0c0-20 10-36 26-54 22-24 30-54 30-54z" opacity="0"/>
    <path d="M256 62c0 0 8 30 30 54 16 18 26 34 26 54a56 56 0 11-112 0c0-20 10-36 26-54 22-24 30-54 30-54z" fill="url(#eg_flame)"/>
    <path d="M256 122c0 0 4 16 15 29 8 10 13 19 13 29a28 28 0 11-56 0c0-10 5-19 13-29 11-13 15-29 15-29z" fill="#ffffff" fill-opacity="0.82"/>
    <path d="M248 258c-38-26-80-30-124-14v146c44-16 86-12 124 14z" fill="url(#eg_pgL)"/>
    <path d="M264 258c38-26 80-30 124-14v146c-44-16-86-12-124 14z" fill="url(#eg_pgR)"/>
    <path d="M256 262v146" stroke="#5b3df5" stroke-opacity="0.3" stroke-width="10" stroke-linecap="round"/>
    <path d="M150 300h68M150 330h68M150 360h54" stroke="#5b3df5" stroke-opacity="0.22" stroke-width="9" stroke-linecap="round"/>
    <path d="M294 300h68M294 330h68M308 360h54" stroke="#5b3df5" stroke-opacity="0.22" stroke-width="9" stroke-linecap="round"/>
  </g>`;
}

// 16:9 End Card (full + animated layers)
function makeEndCard16x9({ includeBackdrop = false, layer = 'all' }) {
  const showLogo = layer === 'all' || layer === 'logo_and_title';
  const showEn = layer === 'all' || layer === 'en_tagline';
  const showHi = layer === 'all' || layer === 'hi_tagline';
  const showUrl = layer === 'all' || layer === 'url_pill';

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs>
    ${LOGO_DEFS}
    <radialGradient id="centerGlow" cx="50%" cy="46%" r="48%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="${includeBackdrop ? '0.20' : '0.12'}"/>
      <stop offset="45%" stop-color="#fbbf24" stop-opacity="${includeBackdrop ? '0.07' : '0.04'}"/>
      <stop offset="100%" stop-color="#090a0f" stop-opacity="0"/>
    </radialGradient>
  </defs>
  ${includeBackdrop ? `<rect width="1920" height="1080" fill="#0b0c12"/><rect width="1920" height="1080" fill="url(#centerGlow)"/>` : ''}
  ${showLogo ? `
    ${officialLogoGroup(960, 192, 164)}
    <text x="960" y="458" text-anchor="middle" font-family="Plus Jakarta Sans, Inter" font-size="74" font-weight="800" letter-spacing="10" fill="#ffffff">EKGURU</text>
    <rect x="680" y="492" width="560" height="2" fill="url(#goldRule)"/>
  ` : ''}
  ${showEn ? `<text x="960" y="558" text-anchor="middle" font-family="Inter" font-size="38" font-weight="500" letter-spacing="0.8" fill="#f8fafc">Learn Indian Languages. Connect with India.</text>` : ''}
  ${showHi ? `<path d="${devPaths.endcard_16x9}" fill="#fcd34d"/>` : ''}
  ${showUrl ? `
    <g transform="translate(960, 728)">
      <rect x="-175" y="-36" width="350" height="58" rx="29" fill="#ffffff" fill-opacity="0.08" stroke="#fbbf24" stroke-opacity="0.54" stroke-width="1.6"/>
      <text x="0" y="3" text-anchor="middle" font-family="Inter" font-size="28" font-weight="600" letter-spacing="2.2" fill="#fef3c7">ekguru.shop</text>
    </g>
  ` : ''}
</svg>`;
}

// 9:16 Vertical End Card (1080x1920 — full + staggered animated layers inside Reels/Shorts safe zone y=560..1260, x=210..870)
function makeEndCard9x16({ includeBackdrop = false, layer = 'all' }) {
  const showLogo = layer === 'all' || layer === 'logo_and_title';
  const showEn = layer === 'all' || layer === 'en_tagline';
  const showHi = layer === 'all' || layer === 'hi_tagline';
  const showUrl = layer === 'all' || layer === 'url_pill';

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    ${LOGO_DEFS}
    <radialGradient id="centerGlowV" cx="50%" cy="48%" r="48%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.20"/>
      <stop offset="50%" stop-color="#fbbf24" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#090a0f" stop-opacity="0"/>
    </radialGradient>
  </defs>
  ${includeBackdrop ? `<rect width="1080" height="1920" fill="#0b0c12"/><rect width="1080" height="1920" fill="url(#centerGlowV)"/>` : ''}
  ${showLogo ? `
    ${officialLogoGroup(540, 585, 176)}
    <text x="540" y="868" text-anchor="middle" font-family="Plus Jakarta Sans, Inter" font-size="72" font-weight="800" letter-spacing="9" fill="#ffffff">EKGURU</text>
    <rect x="280" y="906" width="520" height="2" fill="url(#goldRule)"/>
  ` : ''}
  ${showEn ? `
    <text x="540" y="982" text-anchor="middle" font-family="Inter" font-size="36" font-weight="500" letter-spacing="0.4" fill="#f8fafc">Learn Indian Languages.</text>
    <text x="540" y="1034" text-anchor="middle" font-family="Inter" font-size="36" font-weight="500" letter-spacing="0.4" fill="#fde68a">Connect with India.</text>
  ` : ''}
  ${showHi ? `<path d="${devPaths.endcard_9x16}" fill="#fcd34d"/>` : ''}
  ${showUrl ? `
    <g transform="translate(540, 1218)">
      <rect x="-185" y="-38" width="370" height="64" rx="32" fill="#ffffff" fill-opacity="0.09" stroke="#fbbf24" stroke-opacity="0.56" stroke-width="1.8"/>
      <text x="0" y="5" text-anchor="middle" font-family="Inter" font-size="30" font-weight="600" letter-spacing="2.2" fill="#fef3c7">ekguru.shop</text>
    </g>
  ` : ''}
</svg>`;
}

// 9:16 Vertical Cover / Thumbnail Overlay (1080x1920 — grid-center 1:1 & 4:5 safe too!)
function makeCoverOverlay9x16() {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    ${LOGO_DEFS}
    <linearGradient id="vertScrim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#090a10" stop-opacity="0.20"/>
      <stop offset="42%" stop-color="#090a10" stop-opacity="0.18"/>
      <stop offset="62%" stop-color="#0b0c14" stop-opacity="0.78"/>
      <stop offset="82%" stop-color="#090a10" stop-opacity="0.93"/>
      <stop offset="100%" stop-color="#090a10" stop-opacity="0.96"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1920" fill="url(#vertScrim)"/>

  <!-- Centered inside Instagram Profile 1:1 / 4:5 crop & Reels Safe Zone (y=960..1460) -->
  ${officialLogoGroup(540, 930, 126)}
  <text x="540" y="1116" text-anchor="middle" font-family="Plus Jakarta Sans, Inter" font-size="52" font-weight="800" letter-spacing="7" fill="#ffffff">EKGURU</text>
  <text x="540" y="1196" text-anchor="middle" font-family="Plus Jakarta Sans, Inter" font-size="48" font-weight="700" fill="#ffffff">Learn Indian Languages.</text>
  <text x="540" y="1256" text-anchor="middle" font-family="Plus Jakarta Sans, Inter" font-size="44" font-weight="600" fill="#fde68a">Connect with India.</text>
  <rect x="290" y="1286" width="500" height="2" fill="url(#goldRule)"/>
  <path d="${devPaths.cover_9x16}" fill="#fcd34d"/>
  <g transform="translate(540, 1428)">
    <rect x="-175" y="-34" width="350" height="58" rx="29" fill="#ffffff" fill-opacity="0.12" stroke="#fcd34d" stroke-opacity="0.72" stroke-width="1.8"/>
    <text x="0" y="4" text-anchor="middle" font-family="Inter" font-size="28" font-weight="600" letter-spacing="2" fill="#ffffff">ekguru.shop</text>
  </g>
</svg>`;
}

renderSvgToPng(makeEndCard9x16({ includeBackdrop: false, layer: 'all' }), path.join(OUT_DIR, 'scene_07_endcard_overlay_1080x1920.png'), 1080);
renderSvgToPng(makeEndCard9x16({ includeBackdrop: true, layer: 'all' }), path.join(OUT_DIR, 'scene_07_endcard_preview_dark_1080x1920.png'), 1080);
for (const l of ['logo_and_title', 'en_tagline', 'hi_tagline', 'url_pill']) {
  renderSvgToPng(makeEndCard9x16({ includeBackdrop: false, layer: l }), path.join(OUT_DIR, `layer_${l}_1080x1920.png`), 1080);
}
renderSvgToPng(makeCoverOverlay9x16(), path.join(OUT_DIR, 'reel_cover_overlay_1080x1920.png'), 1080);
