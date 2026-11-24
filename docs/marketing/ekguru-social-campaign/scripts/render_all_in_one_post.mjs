import fs from 'fs';
import path from 'path';
import { Resvg } from '/tmp/ad_node/node_modules/@resvg/resvg-js/index.js';

const ROOT = path.resolve('docs/marketing/ekguru-social-campaign');
const EDITABLE_DIR = path.join(ROOT, '02_editable_designs');
const EXPORT_DIR = path.join(ROOT, '03_final_exports');
const FONTS_DIR = path.resolve('docs/marketing/ekguru-brand-ad/05_brand_graphics/fonts');

const fontFiles = fs.readdirSync(FONTS_DIR)
  .filter(f => f.endsWith('.ttf'))
  .map(f => path.join(FONTS_DIR, f));

const hindi = JSON.parse(fs.readFileSync(path.join(EDITABLE_DIR, 'hindi_all_in_one_paths.json'), 'utf8'));

const IVORY = '#F7F3EA';
const SOFT_IVORY = '#E5DFD2';
const MUTED_SAND = '#C8BFA8';
const GOLD = '#D4AF6A';
const BRIGHT_GOLD = '#E5C787';
const SAFFRON = '#E68A35';
const MIDNIGHT = '#0B0E17';

function hPath(key, fill = BRIGHT_GOLD) {
  const item = hindi[key];
  const esc = item.text.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  return `<g data-hindi-text="${esc}"><title>${esc}</title><path d="${item.path}" fill="${fill}"/></g>`;
}

function makeAllInOneSvg(imgHref) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>
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
    <linearGradient id="ctaGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ECD196"/>
      <stop offset="55%" stop-color="#D7B26B"/>
      <stop offset="100%" stop-color="#C69D52"/>
    </linearGradient>
    <linearGradient id="cardSurface" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#13192A"/>
      <stop offset="100%" stop-color="#0E1320"/>
    </linearGradient>
    <linearGradient id="ctaBannerBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#151C2E"/>
      <stop offset="60%" stop-color="#101524"/>
      <stop offset="100%" stop-color="#181A24"/>
    </linearGradient>
    <linearGradient id="goldFadeRight" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="${GOLD}" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="${GOLD}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <image href="${imgHref}" x="0" y="0" width="1080" height="1350"/>

  <!-- 1. Top Brand & Campaign Identity Bar -->
  <g id="top-brand-bar">
    <g id="official-ekguru-logo" transform="translate(64, 42) scale(0.09375)">
      <rect width="512" height="512" rx="116" fill="url(#eg_bg)"/>
      <circle cx="256" cy="150" r="104" fill="url(#eg_glow)"/>
      <path d="M256 62c0 0 8 30 30 54 16 18 26 34 26 54a56 56 0 11-112 0c0-20 10-36 26-54 22-24 30-54 30-54z" fill="url(#eg_flame)"/>
      <path d="M256 122c0 0 4 16 15 29 8 10 13 19 13 29a28 28 0 11-56 0c0-10 5-19 13-29 11-13 15-29 15-29z" fill="#ffffff" fill-opacity="0.82"/>
      <path d="M248 258c-38-26-80-30-124-14v146c44-16 86-12 124 14z" fill="url(#eg_pgL)"/>
      <path d="M264 258c38-26 80-30 124-14v146c-44-16-86-12-124 14z" fill="url(#eg_pgR)"/>
      <path d="M256 262v146" stroke="#5b3df5" stroke-opacity="0.3" stroke-width="10" stroke-linecap="round"/>
      <path d="M150 300h68M150 330h68M150 360h54" stroke="#5b3df5" stroke-opacity="0.22" stroke-width="9" stroke-linecap="round"/>
      <path d="M294 300h68M294 330h68M308 360h54" stroke="#5b3df5" stroke-opacity="0.22" stroke-width="9" stroke-linecap="round"/>
    </g>
    <text x="126" y="75" font-family="Plus Jakarta Sans" font-size="24" font-weight="800" letter-spacing="5" fill="${IVORY}">EKGURU</text>

    <g transform="translate(1016, 66)">
      <rect x="-324" y="-18" width="324" height="34" rx="17" fill="#121726" stroke="${GOLD}" stroke-opacity="0.38" stroke-width="1"/>
      <polygon points="-302,-1 -298.5,-4.5 -295,-1 -298.5,2.5" fill="${SAFFRON}"/>
      <text x="-154" y="4" text-anchor="middle" font-family="Inter" font-size="11.5" font-weight="600" letter-spacing="2.5" fill="${BRIGHT_GOLD}">WHERE THE WORLD MEETS INDIA</text>
    </g>
  </g>

  <!-- 2. 4-Panel Architectural Story Grid Hairline Frames & Subtle Glass Label Pills -->
  <g id="story-grid-frames">
    <!-- Top-Left: Live 1-on-1 Tutor Call -->
    <rect x="64" y="116" width="608" height="334" rx="10" fill="none" stroke="${GOLD}" stroke-opacity="0.36" stroke-width="1.2"/>
    <rect x="78" y="408" width="286" height="28" rx="14" fill="#0B0E17" fill-opacity="0.78" stroke="${GOLD}" stroke-opacity="0.38" stroke-width="0.9"/>
    <text x="221" y="426" text-anchor="middle" font-family="Inter" font-size="11" font-weight="600" letter-spacing="2.0" fill="${IVORY}">1-ON-1 INDIAN LANGUAGE TUTORS</text>

    <!-- Right Tall: Jaipur Heritage -->
    <rect x="686" y="116" width="330" height="528" rx="10" fill="none" stroke="${GOLD}" stroke-opacity="0.36" stroke-width="1.2"/>
    <rect x="700" y="602" width="194" height="28" rx="14" fill="#0B0E17" fill-opacity="0.80" stroke="${GOLD}" stroke-opacity="0.42" stroke-width="0.9"/>
    <text x="797" y="620" text-anchor="middle" font-family="Inter" font-size="11" font-weight="600" letter-spacing="2.0" fill="${BRIGHT_GOLD}">CONNECT WITH INDIA</text>

    <!-- Bottom-Left: Living Culture -->
    <rect x="64" y="464" width="297" height="180" rx="10" fill="none" stroke="${GOLD}" stroke-opacity="0.36" stroke-width="1.2"/>
    <rect x="76" y="604" width="166" height="27" rx="13.5" fill="#0B0E17" fill-opacity="0.82" stroke="${GOLD}" stroke-opacity="0.40" stroke-width="0.9"/>
    <text x="159" y="621.5" text-anchor="middle" font-family="Inter" font-size="10.8" font-weight="600" letter-spacing="1.9" fill="${IVORY}">EXPLORE CULTURE</text>

    <!-- Bottom-Center: Learning Journey -->
    <rect x="375" y="464" width="297" height="180" rx="10" fill="none" stroke="${GOLD}" stroke-opacity="0.36" stroke-width="1.2"/>
    <rect x="387" y="604" width="192" height="27" rx="13.5" fill="#0B0E17" fill-opacity="0.82" stroke="${GOLD}" stroke-opacity="0.40" stroke-width="0.9"/>
    <text x="483" y="621.5" text-anchor="middle" font-family="Inter" font-size="10.8" font-weight="600" letter-spacing="1.9" fill="${IVORY}">MEANINGFUL JOURNEY</text>
  </g>

  <!-- 3. Core Brand Message & Bilingual Tagline Stage -->
  <g id="core-headline-stage">
    <g transform="translate(68, 678)">
      <polygon points="0,-4.5 4.5,0 0,4.5 -4.5,0" fill="${SAFFRON}"/>
      <rect x="14" y="-0.8" width="64" height="1.6" fill="${GOLD}" fill-opacity="0.88"/>
    </g>

    <!-- Hindi Main Tagline aligned cleanly at top-right of typography stage -->
    ${hPath('aio_tagline_hi', BRIGHT_GOLD)}

    <text x="64" y="736" font-family="Plus Jakarta Sans" font-size="44" font-weight="800" letter-spacing="-0.5" fill="${IVORY}">LEARN INDIAN LANGUAGES.</text>
    <text x="64" y="790" font-family="Plus Jakarta Sans" font-size="44" font-weight="800" letter-spacing="-0.5" fill="${BRIGHT_GOLD}">CONNECT WITH INDIA.</text>

    <text x="64" y="838" font-family="Inter" font-size="22.5" font-weight="400" fill="${SOFT_IVORY}">EkGuru helps learners worldwide discover and connect with Indian language tutors.</text>
    ${hPath('aio_sub_hi', MUTED_SAND)}
  </g>

  <!-- 4. Three Editorial Value Pillars (Zero Clutter, Instant Scan) -->
  <g id="value-pillars">
    <!-- Pillar 1 -->
    <rect x="64" y="916" width="306" height="152" rx="11" fill="url(#cardSurface)" stroke="${GOLD}" stroke-opacity="0.30" stroke-width="1.1"/>
    <text x="88" y="952" font-family="Inter" font-size="13" font-weight="700" letter-spacing="2.4" fill="${SAFFRON}">01</text>
    <line x1="114" y1="947" x2="162" y2="947" stroke="${GOLD}" stroke-opacity="0.45" stroke-width="1"/>
    <text x="88" y="986" font-family="Plus Jakarta Sans" font-size="18.5" font-weight="800" letter-spacing="0.4" fill="${IVORY}">DISCOVER LANGUAGES</text>
    <text x="88" y="1014" font-family="Inter" font-size="15.5" font-weight="400" fill="${SOFT_IVORY}">Hindi &amp; Indian languages</text>
    ${hPath('aio_p1_hi', BRIGHT_GOLD)}

    <!-- Pillar 2 -->
    <rect x="387" y="916" width="306" height="152" rx="11" fill="url(#cardSurface)" stroke="${GOLD}" stroke-opacity="0.30" stroke-width="1.1"/>
    <text x="411" y="952" font-family="Inter" font-size="13" font-weight="700" letter-spacing="2.4" fill="${SAFFRON}">02</text>
    <line x1="439" y1="947" x2="487" y2="947" stroke="${GOLD}" stroke-opacity="0.45" stroke-width="1"/>
    <text x="411" y="986" font-family="Plus Jakarta Sans" font-size="18.5" font-weight="800" letter-spacing="0.4" fill="${IVORY}">CONNECT WITH TUTORS</text>
    <text x="411" y="1014" font-family="Inter" font-size="15.5" font-weight="400" fill="${SOFT_IVORY}">Match your learning goals</text>
    ${hPath('aio_p2_hi', BRIGHT_GOLD)}

    <!-- Pillar 3 -->
    <rect x="710" y="916" width="306" height="152" rx="11" fill="url(#cardSurface)" stroke="${GOLD}" stroke-opacity="0.30" stroke-width="1.1"/>
    <text x="734" y="952" font-family="Inter" font-size="13" font-weight="700" letter-spacing="2.4" fill="${SAFFRON}">03</text>
    <line x1="762" y1="947" x2="810" y2="947" stroke="${GOLD}" stroke-opacity="0.45" stroke-width="1"/>
    <text x="734" y="986" font-family="Plus Jakarta Sans" font-size="18.5" font-weight="800" letter-spacing="0.4" fill="${IVORY}">EXPERIENCE CULTURE</text>
    <text x="734" y="1014" font-family="Inter" font-size="15.5" font-weight="400" fill="${SOFT_IVORY}">Connect beyond just words</text>
    ${hPath('aio_p3_hi', BRIGHT_GOLD)}
  </g>

  <!-- 5. Bottom High-Impact Website & CTA Banner -->
  <g id="bottom-cta-banner">
    <rect x="64" y="1096" width="952" height="154" rx="14" fill="url(#ctaBannerBg)" stroke="${GOLD}" stroke-opacity="0.48" stroke-width="1.3"/>

    <text x="100" y="1142" font-family="Inter" font-size="13" font-weight="600" letter-spacing="2.8" fill="${BRIGHT_GOLD}">YOUR CONNECTION WITH INDIA STARTS HERE</text>
    <text x="100" y="1192" font-family="Plus Jakarta Sans" font-size="38" font-weight="800" letter-spacing="1.6" fill="${IVORY}">ekguru.shop</text>
    <text x="100" y="1224" font-family="Inter" font-size="15.5" font-weight="400" letter-spacing="0.6" fill="${MUTED_SAND}">Visit https://ekguru.shop to explore Indian language tutors</text>

    <!-- Champagne Gold CTA Pill -->
    <g transform="translate(790, 1173)">
      <rect x="-188" y="-34" width="376" height="68" rx="34" fill="url(#ctaGold)"/>
      <rect x="-186" y="-32" width="372" height="64" rx="32" fill="none" stroke="#FFF8E7" stroke-opacity="0.45" stroke-width="1"/>
      <text x="-12" y="7" text-anchor="middle" font-family="Plus Jakarta Sans" font-size="19.5" font-weight="800" letter-spacing="2.8" fill="${MIDNIGHT}">EXPLORE EKGURU</text>
      <line x1="118" y1="0.5" x2="138" y2="0.5" stroke="${MIDNIGHT}" stroke-width="2.2" stroke-linecap="round"/>
      <polyline points="131,-5.5 138.5,0.5 131,6.5" fill="none" stroke="${MIDNIGHT}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
  </g>

  <!-- Subtle Bottom Signature -->
  <text x="540" y="1302" text-anchor="middle" font-family="Inter" font-size="12.5" font-weight="500" letter-spacing="2.8" fill="${MUTED_SAND}" fill-opacity="0.82">A LANGUAGE CAN OPEN A WHOLE NEW WORLD  ·  EKGURU.SHOP</text>
</svg>`;
}

// 1. Save lightweight editable SVG
const editableSvg = makeAllInOneSvg('base_all_in_one.jpg');
fs.writeFileSync(path.join(EDITABLE_DIR, 'ekguru_all_in_one_post_1080x1350.svg'), editableSvg, 'utf8');

// 2. Render zero-loss 1080x1350 PNG
const srcPath = '/tmp/ekguru_social_bases/base_all_in_one.png';
const b64 = fs.readFileSync(srcPath).toString('base64');
const inlineSvg = makeAllInOneSvg(`data:image/png;base64,${b64}`);
const resvg = new Resvg(inlineSvg, {
  fitTo: { mode: 'width', value: 1080 },
  font: {
    fontFiles,
    loadSystemFonts: false,
    defaultFontFamily: 'Inter',
  },
});
const rendered = resvg.render();
const outPath = path.join(EXPORT_DIR, 'ekguru_all_in_one_post_1080x1350.png');
fs.writeFileSync(outPath, rendered.asPng());
console.log(`Exported: ${outPath} (${rendered.width}x${rendered.height})`);
