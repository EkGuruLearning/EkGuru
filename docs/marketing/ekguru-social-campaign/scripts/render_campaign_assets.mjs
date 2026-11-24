import fs from 'fs';
import path from 'path';
import { Resvg } from '/tmp/ad_node/node_modules/@resvg/resvg-js/index.js';

const ROOT = path.resolve('docs/marketing/ekguru-social-campaign');
const EDITABLE_DIR = path.join(ROOT, '02_editable_designs');
const EXPORT_DIR = path.join(ROOT, '03_final_exports');
const FONTS_DIR = path.resolve('docs/marketing/ekguru-brand-ad/05_brand_graphics/fonts');

fs.mkdirSync(EDITABLE_DIR, { recursive: true });
fs.mkdirSync(EXPORT_DIR, { recursive: true });

const fontFiles = fs.readdirSync(FONTS_DIR)
  .filter(f => f.endsWith('.ttf'))
  .map(f => path.join(FONTS_DIR, f));

const hindi = JSON.parse(fs.readFileSync(path.join(EDITABLE_DIR, 'hindi_shaped_paths.json'), 'utf8'));

// Palette — Editorial Luxury International EdTech
const IVORY = '#F7F3EA';
const SOFT_IVORY = '#E5DFD2';
const MUTED_SAND = '#C8BFA8';
const GOLD = '#D4AF6A';
const BRIGHT_GOLD = '#E5C787';
const SAFFRON = '#E68A35';
const MIDNIGHT = '#0B0E17';

const SHARED_DEFS = `
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
    <linearGradient id="goldFadeRight" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="${GOLD}" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="${GOLD}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="goldFadeCenter" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="${GOLD}" stop-opacity="0"/>
      <stop offset="50%" stop-color="${BRIGHT_GOLD}" stop-opacity="0.80"/>
      <stop offset="100%" stop-color="${GOLD}" stop-opacity="0"/>
    </linearGradient>
    <filter id="logoDrop" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="8" stdDeviation="14" flood-color="#000000" flood-opacity="0.52"/>
    </filter>`;

// Exact unmodified official EkGuru vector logo from images/logo.svg
function officialEkGuruLogo(x, y, size, withShadow = true) {
  const s = size / 512;
  return `<g id="official-ekguru-logo" transform="translate(${x}, ${y}) scale(${s})"${withShadow ? ' filter="url(#logoDrop)"' : ''}>
    <rect width="512" height="512" rx="116" fill="url(#eg_bg)"/>
    <circle cx="256" cy="150" r="104" fill="url(#eg_glow)"/>
    <path d="M256 62c0 0 8 30 30 54 16 18 26 34 26 54a56 56 0 11-112 0c0-20 10-36 26-54 22-24 30-54 30-54z" fill="url(#eg_flame)"/>
    <path d="M256 122c0 0 4 16 15 29 8 10 13 19 13 29a28 28 0 11-56 0c0-10 5-19 13-29 11-13 15-29 15-29z" fill="#ffffff" fill-opacity="0.82"/>
    <path d="M248 258c-38-26-80-30-124-14v146c44-16 86-12 124 14z" fill="url(#eg_pgL)"/>
    <path d="M264 258c38-26 80-30 124-14v146c-44-16-86-12-124 14z" fill="url(#eg_pgR)"/>
    <path d="M256 262v146" stroke="#5b3df5" stroke-opacity="0.3" stroke-width="10" stroke-linecap="round"/>
    <path d="M150 300h68M150 330h68M150 360h54" stroke="#5b3df5" stroke-opacity="0.22" stroke-width="9" stroke-linecap="round"/>
    <path d="M294 300h68M294 330h68M308 360h54" stroke="#5b3df5" stroke-opacity="0.22" stroke-width="9" stroke-linecap="round"/>
  </g>`;
}

// Architectural gold rule + subtle saffron jewel accent
function goldSaffronAccentLeft(x, y) {
  return `<g transform="translate(${x}, ${y})">
    <polygon points="0,-4.5 4.5,0 0,4.5 -4.5,0" fill="${SAFFRON}"/>
    <rect x="14" y="-0.8" width="68" height="1.6" fill="${GOLD}" fill-opacity="0.88"/>
  </g>`;
}

// Consistent Top Editorial Header across Slides 1-4 (and tailored header for Slide 5 where hero logo is centered)
function slideTopHeader(slideNum, includeMiniBrand = true) {
  const numStr = `0${slideNum} / 05`;
  if (includeMiniBrand) {
    return `<g id="top-editorial-header">
      ${officialEkGuruLogo(72, 54, 40, false)}
      <text x="126" y="81" font-family="Plus Jakarta Sans" font-size="18" font-weight="800" letter-spacing="4.2" fill="${IVORY}">EKGURU</text>
      <text x="912" y="79" text-anchor="end" font-family="Inter" font-size="11.5" font-weight="600" letter-spacing="2.8" fill="${BRIGHT_GOLD}" fill-opacity="0.92">WHERE THE WORLD MEETS INDIA</text>
      <line x1="928" y1="66" x2="928" y2="83" stroke="${GOLD}" stroke-opacity="0.40" stroke-width="1"/>
      <text x="1008" y="79" text-anchor="end" font-family="Inter" font-size="12.5" font-weight="600" letter-spacing="1.8" fill="${IVORY}" fill-opacity="0.88">${numStr}</text>
    </g>`;
  }
  return `<g id="top-editorial-header">
    <text x="72" y="81" font-family="Inter" font-size="12" font-weight="600" letter-spacing="3.2" fill="${BRIGHT_GOLD}" fill-opacity="0.88">WHERE THE WORLD MEETS INDIA</text>
    <text x="1008" y="81" text-anchor="end" font-family="Inter" font-size="12.5" font-weight="600" letter-spacing="1.8" fill="${IVORY}" fill-opacity="0.88">${numStr}</text>
  </g>`;
}

// Consistent Bottom Carousel Footer & Progress Indicator across Slides 1-5
function slideBottomFooter(slideNum) {
  // 5-segment progress bars centered around x=540
  const bars = [];
  let curX = 480;
  for (let i = 1; i <= 5; i++) {
    const isAct = i === slideNum;
    const w = isAct ? 36 : 14;
    bars.push(`<rect x="${curX}" y="1281" width="${w}" height="3" rx="1.5" fill="${isAct ? GOLD : IVORY}" fill-opacity="${isAct ? '0.96' : '0.24'}"/>`);
    curX += w + 8;
  }

  const showSwipe = slideNum < 5;
  return `<g id="bottom-carousel-footer">
    <line x1="72" y1="1248" x2="1008" y2="1248" stroke="${GOLD}" stroke-opacity="0.18" stroke-width="1"/>
    ${slideNum < 5 ? `<text x="72" y="1288" font-family="Inter" font-size="14.5" font-weight="500" letter-spacing="2.0" fill="${MUTED_SAND}">ekguru.shop</text>` : ''}
    <g id="progress-bars">${bars.join('')}</g>
    ${showSwipe ? `
    <g id="swipe-cue" transform="translate(1008, 1283)">
      <text x="-26" y="4" text-anchor="end" font-family="Inter" font-size="12" font-weight="600" letter-spacing="2.8" fill="${BRIGHT_GOLD}">SWIPE</text>
      <line x1="-18" y1="0" x2="-2" y2="0" stroke="${BRIGHT_GOLD}" stroke-width="1.6" stroke-linecap="round"/>
      <polyline points="-7,-4.5 -1.5,0 -7,4.5" fill="none" stroke="${BRIGHT_GOLD}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
    </g>` : ''}
  </g>`;
}

function hindiPathElem(key, fill = BRIGHT_GOLD) {
  const item = hindi[key];
  const esc = item.text.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  return `<g data-hindi-text="${esc}"><title>${esc}</title><path d="${item.path}" fill="${fill}"/></g>`;
}

// Build SVG with either relative href (for lightweight editable .svg) or base64 data URI (for @resvg/resvg-js PNG export)
function makeSlide01Svg(imgHref) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>${SHARED_DEFS}</defs>
  <image href="${imgHref}" x="0" y="0" width="1080" height="1350"/>
  ${slideTopHeader(1, true)}

  <g id="editorial-copy">
    ${goldSaffronAccentLeft(76, 828)}
    <text x="72" y="894" font-family="Plus Jakarta Sans" font-size="56" font-weight="800" letter-spacing="-0.5" fill="${IVORY}">A LANGUAGE CAN</text>
    <text x="72" y="960" font-family="Plus Jakarta Sans" font-size="56" font-weight="800" letter-spacing="-0.5" fill="${IVORY}">OPEN A WHOLE</text>
    <text x="72" y="1026" font-family="Plus Jakarta Sans" font-size="56" font-weight="800" letter-spacing="-0.5" fill="${BRIGHT_GOLD}">NEW WORLD.</text>

    <text x="72" y="1088" font-family="Inter" font-size="25.5" font-weight="400" fill="${SOFT_IVORY}">What if learning an Indian language</text>
    <text x="72" y="1126" font-family="Inter" font-size="25.5" font-weight="400" fill="${SOFT_IVORY}">brought you closer to India?</text>

    <rect x="72" y="1154" width="240" height="1" fill="url(#goldFadeRight)"/>
    ${hindiPathElem('s1_hi', BRIGHT_GOLD)}
  </g>

  ${slideBottomFooter(1)}
</svg>`;
}

function makeSlide02Svg(imgHref) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>${SHARED_DEFS}</defs>
  <image href="${imgHref}" x="0" y="0" width="1080" height="1350"/>
  ${slideTopHeader(2, true)}

  <!-- Crisp 1px Muted-Gold Gallery Frame around Photograph -->
  <rect x="72" y="134" width="936" height="672" rx="10" fill="none" stroke="${GOLD}" stroke-opacity="0.34" stroke-width="1.2"/>

  <g id="editorial-copy">
    ${goldSaffronAccentLeft(76, 854)}
    <text x="72" y="922" font-family="Plus Jakarta Sans" font-size="56" font-weight="800" letter-spacing="-0.5" fill="${IVORY}">MORE THAN JUST WORDS.</text>

    <text x="72" y="984" font-family="Inter" font-size="26" font-weight="400" fill="${SOFT_IVORY}">Discover the language. Understand the culture.</text>
    <text x="72" y="1022" font-family="Inter" font-size="26" font-weight="400" fill="${SOFT_IVORY}">Connect with the people.</text>

    <rect x="72" y="1058" width="280" height="1" fill="url(#goldFadeRight)"/>
    ${hindiPathElem('s2_hi_1', BRIGHT_GOLD)}
    ${hindiPathElem('s2_hi_2', BRIGHT_GOLD)}
  </g>

  ${slideBottomFooter(2)}
</svg>`;
}

function makeSlide03Svg(imgHref) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>${SHARED_DEFS}</defs>
  <image href="${imgHref}" x="0" y="0" width="1080" height="1350"/>
  ${slideTopHeader(3, true)}

  <!-- Upper Headline Feature Stage -->
  <g id="upper-headline">
    ${goldSaffronAccentLeft(76, 158)}
    <text x="72" y="238" font-family="Plus Jakarta Sans" font-size="68" font-weight="800" letter-spacing="-0.8" fill="${IVORY}">MEET EKGURU.</text>
  </g>

  <!-- Crisp 1px Muted-Gold Cinema Frame around Video-Call Photograph -->
  <rect x="72" y="288" width="936" height="576" rx="10" fill="none" stroke="${GOLD}" stroke-opacity="0.34" stroke-width="1.2"/>

  <!-- Lower Supporting Copy + Hindi Stage -->
  <g id="editorial-copy">
    <text x="72" y="936" font-family="Inter" font-size="26.5" font-weight="400" fill="${SOFT_IVORY}">A platform helping learners around the world</text>
    <text x="72" y="976" font-family="Inter" font-size="26.5" font-weight="400" fill="${SOFT_IVORY}">discover and connect with Indian language tutors.</text>

    <rect x="72" y="1018" width="280" height="1" fill="url(#goldFadeRight)"/>
    ${hindiPathElem('s3_hi_1', BRIGHT_GOLD)}
    ${hindiPathElem('s3_hi_2', BRIGHT_GOLD)}
  </g>

  ${slideBottomFooter(3)}
</svg>`;
}

function makeSlide04Svg(imgHref) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>${SHARED_DEFS}</defs>
  <image href="${imgHref}" x="0" y="0" width="1080" height="1350"/>
  ${slideTopHeader(4, true)}

  <!-- Hairline Gold Borders around Split Editorial Triptych Panels -->
  <g id="triptych-frames">
    <rect x="72" y="134" width="492" height="660" rx="10" fill="none" stroke="${GOLD}" stroke-opacity="0.32" stroke-width="1.2"/>
    <rect x="580" y="134" width="428" height="322" rx="10" fill="none" stroke="${GOLD}" stroke-opacity="0.32" stroke-width="1.2"/>
    <rect x="580" y="472" width="428" height="322" rx="10" fill="none" stroke="${GOLD}" stroke-opacity="0.32" stroke-width="1.2"/>
  </g>

  <g id="editorial-copy">
    ${goldSaffronAccentLeft(76, 838)}
    <text x="72" y="898" font-family="Plus Jakarta Sans" font-size="45" font-weight="800" letter-spacing="-0.4" fill="${IVORY}">YOUR JOURNEY. YOUR LANGUAGE.</text>
    <text x="72" y="952" font-family="Plus Jakarta Sans" font-size="45" font-weight="800" letter-spacing="-0.4" fill="${BRIGHT_GOLD}">YOUR CONNECTION.</text>

    <text x="72" y="1008" font-family="Inter" font-size="24" font-weight="400" fill="${SOFT_IVORY}">Discover Hindi and other Indian languages. Explore tutors.</text>
    <text x="72" y="1043" font-family="Inter" font-size="24" font-weight="400" fill="${SOFT_IVORY}">Connect with the tutor who matches your learning interests.</text>

    <rect x="72" y="1074" width="280" height="1" fill="url(#goldFadeRight)"/>
    ${hindiPathElem('s4_hi_1', BRIGHT_GOLD)}
    ${hindiPathElem('s4_hi_2', BRIGHT_GOLD)}
  </g>

  ${slideBottomFooter(4)}
</svg>`;
}

function makeSlide05Svg(imgHref) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350" width="1080" height="1350">
  <defs>${SHARED_DEFS}</defs>
  <image href="${imgHref}" x="0" y="0" width="1080" height="1350"/>

  <!-- Subtle Ceremonial Architectural Outer Hairline -->
  <rect x="44" y="38" width="992" height="1274" rx="14" fill="none" stroke="${GOLD}" stroke-opacity="0.20" stroke-width="1"/>

  ${slideTopHeader(5, false)}

  <!-- Official Unmodified EkGuru Logo & Brand Finale -->
  <g id="brand-hero">
    ${officialEkGuruLogo(464, 198, 152, true)}
    <text x="540" y="424" text-anchor="middle" font-family="Plus Jakarta Sans" font-size="56" font-weight="800" letter-spacing="10" fill="${IVORY}">EKGURU</text>

    <!-- Centered Gold Rule + Saffron Jewel -->
    <rect x="360" y="458" width="360" height="1.2" fill="url(#goldFadeCenter)"/>
    <polygon points="540,453.5 544.5,458.6 540,463.7 535.5,458.6" fill="${SAFFRON}"/>

    <text x="540" y="548" text-anchor="middle" font-family="Plus Jakarta Sans" font-size="48" font-weight="800" letter-spacing="-0.3" fill="${IVORY}">YOUR CONNECTION WITH</text>
    <text x="540" y="608" text-anchor="middle" font-family="Plus Jakarta Sans" font-size="48" font-weight="800" letter-spacing="-0.3" fill="${BRIGHT_GOLD}">INDIA STARTS HERE.</text>

    <text x="540" y="692" text-anchor="middle" font-family="Inter" font-size="28" font-weight="500" letter-spacing="0.4" fill="${SOFT_IVORY}">Learn Indian Languages. Connect with India.</text>
    ${hindiPathElem('s5_hi', BRIGHT_GOLD)}

    <!-- Luxury Call to Action Pill -->
    <g id="cta-button" transform="translate(540, 882)">
      <rect x="-210" y="-37" width="420" height="74" rx="37" fill="url(#ctaGold)"/>
      <rect x="-208" y="-35" width="416" height="70" rx="35" fill="none" stroke="#FFF8E7" stroke-opacity="0.45" stroke-width="1"/>
      <text x="-12" y="8" text-anchor="middle" font-family="Plus Jakarta Sans" font-size="21" font-weight="800" letter-spacing="3.2" fill="${MIDNIGHT}">EXPLORE EKGURU</text>
      <line x1="126" y1="1" x2="148" y2="1" stroke="${MIDNIGHT}" stroke-width="2.2" stroke-linecap="round"/>
      <polyline points="141,-5.5 148.5,1 141,7.5" fill="none" stroke="${MIDNIGHT}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <!-- Crisp High-Contrast Website Lockup -->
    <text x="540" y="1008" text-anchor="middle" font-family="Inter" font-size="33" font-weight="600" letter-spacing="2.4" fill="${IVORY}">ekguru.shop</text>
    <rect x="440" y="1028" width="200" height="1.4" fill="url(#goldFadeCenter)"/>
  </g>

  ${slideBottomFooter(5)}
</svg>`;
}

function makeXLandscapeSvg(imgHref) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675">
  <defs>${SHARED_DEFS}</defs>
  <image href="${imgHref}" x="0" y="0" width="1200" height="675"/>

  <!-- Subtle Outer Architectural Frame -->
  <rect x="20" y="20" width="1160" height="635" rx="10" fill="none" stroke="${GOLD}" stroke-opacity="0.22" stroke-width="1"/>

  <!-- Left Negative-Space Editorial Column (x=56..435, completely clear of learner & Jaipur architecture) -->
  <g id="x-brand-header">
    ${officialEkGuruLogo(56, 48, 42, false)}
    <text x="112" y="77" font-family="Plus Jakarta Sans" font-size="20" font-weight="800" letter-spacing="4.5" fill="${IVORY}">EKGURU</text>
  </g>

  <g id="x-headline">
    ${goldSaffronAccentLeft(60, 124)}
    <text x="56" y="182" font-family="Plus Jakarta Sans" font-size="50" font-weight="800" letter-spacing="-0.6" fill="${IVORY}">LANGUAGE</text>
    <text x="56" y="236" font-family="Plus Jakarta Sans" font-size="50" font-weight="800" letter-spacing="-0.6" fill="${IVORY}">CONNECTS</text>
    <text x="56" y="290" font-family="Plus Jakarta Sans" font-size="50" font-weight="800" letter-spacing="-0.6" fill="${BRIGHT_GOLD}">WORLDS.</text>
  </g>

  <g id="x-supporting-copy">
    <text x="56" y="344" font-family="Inter" font-size="20.5" font-weight="500" fill="${SOFT_IVORY}">Discover Indian languages.</text>
    <text x="56" y="376" font-family="Inter" font-size="20.5" font-weight="500" fill="${SOFT_IVORY}">Connect with Indian tutors.</text>
    <text x="56" y="408" font-family="Inter" font-size="20.5" font-weight="500" fill="${SOFT_IVORY}">Experience India beyond words.</text>

    <rect x="56" y="432" width="210" height="1" fill="url(#goldFadeRight)"/>
    ${hindiPathElem('x_hi', BRIGHT_GOLD)}
  </g>

  <g id="x-footer-cta">
    <text x="56" y="542" font-family="Inter" font-size="16" font-weight="500" letter-spacing="0.2" fill="${MUTED_SAND}">Learn Indian Languages. Connect with India.</text>

    <g transform="translate(56, 564)">
      <rect x="0" y="0" width="238" height="50" rx="25" fill="#111726" fill-opacity="0.90" stroke="${GOLD}" stroke-opacity="0.72" stroke-width="1.5"/>
      <text x="104" y="32" text-anchor="middle" font-family="Inter" font-size="19.5" font-weight="600" letter-spacing="1.6" fill="${IVORY}">ekguru.shop</text>
      <line x1="194" y1="25" x2="212" y2="25" stroke="${BRIGHT_GOLD}" stroke-width="1.8" stroke-linecap="round"/>
      <polyline points="206,19.5 212.5,25 206,30.5" fill="none" stroke="${BRIGHT_GOLD}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
  </g>
</svg>`;
}

const SPECS = [
  {
    name: 'ekguru_instagram_slide_01',
    baseFile: 'base_slide_01.jpg',
    outPng: 'ekguru_instagram_slide_01_1080x1350.png',
    width: 1080,
    fn: makeSlide01Svg,
  },
  {
    name: 'ekguru_instagram_slide_02',
    baseFile: 'base_slide_02.jpg',
    outPng: 'ekguru_instagram_slide_02_1080x1350.png',
    width: 1080,
    fn: makeSlide02Svg,
  },
  {
    name: 'ekguru_instagram_slide_03',
    baseFile: 'base_slide_03.jpg',
    outPng: 'ekguru_instagram_slide_03_1080x1350.png',
    width: 1080,
    fn: makeSlide03Svg,
  },
  {
    name: 'ekguru_instagram_slide_04',
    baseFile: 'base_slide_04.jpg',
    outPng: 'ekguru_instagram_slide_04_1080x1350.png',
    width: 1080,
    fn: makeSlide04Svg,
  },
  {
    name: 'ekguru_instagram_slide_05',
    baseFile: 'base_slide_05.jpg',
    outPng: 'ekguru_instagram_slide_05_1080x1350.png',
    width: 1080,
    fn: makeSlide05Svg,
  },
  {
    name: 'ekguru_x_twitter_post_1200x675',
    baseFile: 'base_x_landscape.jpg',
    outPng: 'ekguru_x_twitter_post_1200x675.png',
    width: 1200,
    fn: makeXLandscapeSvg,
  },
];

for (const spec of SPECS) {
  // 1. Save lightweight editable SVG referencing relative base PNG
  const editableSvg = spec.fn(spec.baseFile);
  fs.writeFileSync(path.join(EDITABLE_DIR, `${spec.name}.svg`), editableSvg, 'utf8');

  // 2. Render self-contained PNG using data-URI base image
  const losslessPath = `/tmp/ekguru_social_bases/${spec.baseFile.replace('.jpg', '.png')}`;
  const srcPath = fs.existsSync(losslessPath) ? losslessPath : path.join(EDITABLE_DIR, spec.baseFile);
  const mime = srcPath.endsWith('.png') ? 'image/png' : 'image/jpeg';
  const b64 = fs.readFileSync(srcPath).toString('base64');
  const inlineSvg = spec.fn(`data:${mime};base64,${b64}`);
  const resvg = new Resvg(inlineSvg, {
    fitTo: { mode: 'width', value: spec.width },
    font: {
      fontFiles,
      loadSystemFonts: false,
      defaultFontFamily: 'Inter',
    },
  });
  const rendered = resvg.render();
  const outPath = path.join(EXPORT_DIR, spec.outPng);
  fs.writeFileSync(outPath, rendered.asPng());
  console.log(`Exported: ${spec.outPng} (${rendered.width}x${rendered.height})`);
}
