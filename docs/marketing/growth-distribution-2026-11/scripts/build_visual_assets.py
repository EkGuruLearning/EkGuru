#!/usr/bin/env python3
"""Build EkGuru claim-safe Open Graph cover (1200x630) and the 3 Official Profile
Starter Posts (1080x1350) defined in GROWTH-PLAN-2026-11-24.md Section 6(a) and
DISTRIBUTION-KIT-2026-11-24.md Section 8.

All Devanagari glyphs are shaped via HarfBuzz (uharfbuzz) + fontTools into exact
vector <path> elements so matras, halants, and conjuncts (अन्ना, नमस्ते, डेविड, किताब)
render with zero raster or shaping defects, and all Latin/punctuation uses Plus Jakarta
Sans / Inter so zero missing-glyph boxes ever appear.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "docs/marketing/growth-distribution-2026-11"
OG_SVG_DIR = OUT_DIR / "00_og_cover"
POSTS_DIR = OUT_DIR / "02_official_profile_first_3_posts"
FONTS_DIR = ROOT / "docs/marketing/ekguru-brand-ad/05_brand_graphics/fonts"

DEVA_MED = FONTS_DIR / "NotoSansDevanagari-Complete-500.ttf"


class HarfBuzzSVGShaper:
    def __init__(self, font_path: Path):
        self.data = font_path.read_bytes()
        self.face = hb.Face(self.data)
        self.hb_font = hb.Font(self.face)
        self.tt = TTFont(str(font_path))
        self.upem = self.tt["head"].unitsPerEm
        self.glyph_set = self.tt.getGlyphSet()

    def shape_to_path(
        self,
        text: str,
        x: float,
        y: float,
        font_size: float,
        align: str = "left",
    ) -> tuple[str, float]:
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb_font, buf, {"kern": True, "liga": True})

        scale = font_size / self.upem
        infos = buf.glyph_infos
        positions = buf.glyph_positions
        total_adv = sum(p.x_advance for p in positions) * scale

        cursor_x = x
        if align == "center":
            cursor_x = x - total_adv / 2.0
        elif align == "right":
            cursor_x = x - total_adv

        spen = SVGPathPen(self.glyph_set)
        for info, pos in zip(infos, positions):
            if info.codepoint == 0:
                raise ValueError(f"Unmapped glyph (.notdef) while shaping {text!r}")
            gname = self.tt.getGlyphName(info.codepoint)
            gx = cursor_x + pos.x_offset * scale
            gy = y - pos.y_offset * scale
            tpen = TransformPen(spen, (scale, 0.0, 0.0, -scale, gx, gy))
            self.glyph_set[gname].draw(tpen)
            cursor_x += pos.x_advance * scale

        return spen.getCommands(), total_adv


SHAPER = HarfBuzzSVGShaper(DEVA_MED)


def logo_group(x: float, y: float, size: float, uid: str) -> str:
    """Embed the unmodified official EkGuru vector mark from images/logo.svg."""
    s = size / 512.0
    return f"""<g transform="translate({x},{y}) scale({s:.6f})">
      <defs>
        <linearGradient id="lbg_{uid}" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#5b3df5"/>
          <stop offset="52%" stop-color="#8b5cf6"/>
          <stop offset="100%" stop-color="#ec4899"/>
        </linearGradient>
        <linearGradient id="lfl_{uid}" x1="0.5" y1="1" x2="0.5" y2="0">
          <stop offset="0%" stop-color="#f59e0b"/>
          <stop offset="45%" stop-color="#fbbf24"/>
          <stop offset="100%" stop-color="#fff7d6"/>
        </linearGradient>
        <linearGradient id="lpgL_{uid}" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="100%" stop-color="#f0ecff"/>
        </linearGradient>
        <linearGradient id="lpgR_{uid}" x1="1" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="100%" stop-color="#e3dcff"/>
        </linearGradient>
        <radialGradient id="lgl_{uid}" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0%" stop-color="#fbbf24" stop-opacity=".55"/>
          <stop offset="100%" stop-color="#fbbf24" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="512" height="512" rx="116" fill="url(#lbg_{uid})"/>
      <circle cx="256" cy="150" r="104" fill="url(#lgl_{uid})"/>
      <path d="M256 62c0 0 8 30 30 54 16 18 26 34 26 54a56 56 0 11-112 0c0-20 10-36 26-54 22-24 30-54 30-54z" fill="url(#lfl_{uid})"/>
      <path d="M256 122c0 0 4 16 15 29 8 10 13 19 13 29a28 28 0 11-56 0c0-10 5-19 13-29 11-13 15-29 15-29z" fill="#fff" fill-opacity=".82"/>
      <path d="M248 258c-38-26-80-30-124-14v146c44-16 86-12 124 14z" fill="url(#lpgL_{uid})"/>
      <path d="M264 258c38-26 80-30 124-14v146c-44-16-86-12-124 14z" fill="url(#lpgR_{uid})"/>
      <path d="M256 262v146" stroke="#5b3df5" stroke-opacity=".3" stroke-width="10" stroke-linecap="round"/>
      <path d="M150 300h68M150 330h68M150 360h54" stroke="#5b3df5" stroke-opacity=".22" stroke-width="9" stroke-linecap="round"/>
      <path d="M294 300h68M294 330h68M308 360h54" stroke="#5b3df5" stroke-opacity=".22" stroke-width="9" stroke-linecap="round"/>
    </g>"""


def build_og_cover_svg() -> str:
    hi_tagline_d, _ = SHAPER.shape_to_path("एक भाषा, एक नई दुनिया।", 64, 388, 30, align="left")
    # Right card spans x=756..1144 (width=388), inner padding 24px -> x=780..1120 (width=340)
    # 3 tiles inside 340px: 3 * 104 + 2 * 14 = 340px -> x=780, 898, 1016
    tile_a_d, _ = SHAPER.shape_to_path("अ", 832, 206, 44, align="center")
    tile_ka_d, _ = SHAPER.shape_to_path("क", 950, 206, 44, align="center")
    tile_na_d, _ = SHAPER.shape_to_path("न", 1068, 206, 44, align="center")
    namaste_d, _ = SHAPER.shape_to_path("नमस्ते", 802, 344, 40, align="left")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F1422"/>
      <stop offset="55%" stop-color="#171D31"/>
      <stop offset="100%" stop-color="#22192E"/>
    </linearGradient>
    <radialGradient id="warmGlow" cx="0.82" cy="0.22" r="0.58">
      <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.24"/>
      <stop offset="55%" stop-color="#8B5CF6" stop-opacity="0.11"/>
      <stop offset="100%" stop-color="#0F1422" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="leftGlow" cx="0.12" cy="0.88" r="0.5">
      <stop offset="0%" stop-color="#5B3DF5" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#0F1422" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="goldLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FBBF24"/>
      <stop offset="100%" stop-color="#F97316" stop-opacity="0.2"/>
    </linearGradient>
    <linearGradient id="cardBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="100%" stop-color="#F6F0E6"/>
    </linearGradient>
    <linearGradient id="ctaPill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#EA580C"/>
    </linearGradient>
  </defs>

  <rect width="1200" height="630" fill="url(#bgGrad)"/>
  <rect width="1200" height="630" fill="url(#warmGlow)"/>
  <rect width="1200" height="630" fill="url(#leftGlow)"/>

  <!-- Subtle architectural border frame -->
  <rect x="24" y="24" width="1152" height="582" rx="26" fill="none" stroke="#FFFFFF" stroke-opacity="0.09" stroke-width="1.5"/>

  <!-- Brand header: Official EkGuru logo + wordmark -->
  {logo_group(64, 66, 62, "og")}
  <text x="142" y="103" font-family="Plus Jakarta Sans" font-weight="800" font-size="32" fill="#FFFFFF" letter-spacing="-0.5">EkGuru</text>
  <text x="143" y="125" font-family="Inter" font-weight="500" font-size="14.5" fill="#CBD5E1" letter-spacing="0.3">One Student. One Goal. One Guru.</text>

  <!-- Left column: Claim-safe headline -->
  <text x="64" y="220" font-family="Plus Jakarta Sans" font-weight="800" font-size="50" fill="#FFFFFF" letter-spacing="-1.0">Learn Indian Languages.</text>
  <text x="64" y="282" font-family="Plus Jakarta Sans" font-weight="800" font-size="50" fill="#FBBF24" letter-spacing="-1.0">Connect with India.</text>

  <rect x="64" y="314" width="236" height="3.5" rx="2" fill="url(#goldLine)"/>

  <!-- HarfBuzz-shaped Hindi tagline -->
  <path d="{hi_tagline_d}" fill="#FDE68A"/>

  <!-- Honest, accurate site value proposition -->
  <text x="64" y="444" font-family="Inter" font-weight="500" font-size="20" fill="#E2E8F0">Free self-paced courses, script &amp; pronunciation tools,</text>
  <text x="64" y="474" font-family="Inter" font-weight="500" font-size="20" fill="#E2E8F0">and 1-on-1 online tutor profiles — no sign-up to start.</text>

  <!-- Bottom feature pills + URL badge (64..704, cleanly separated from right card at x=756) -->
  <g transform="translate(64, 514)">
    <rect x="0" y="0" width="160" height="42" rx="21" fill="url(#ctaPill)"/>
    <text x="80" y="27" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="700" font-size="17" fill="#FFFFFF">ekguru.shop</text>

    <rect x="172" y="0" width="144" height="42" rx="21" fill="#FFFFFF" fill-opacity="0.09" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
    <text x="244" y="26.5" text-anchor="middle" font-family="Inter" font-weight="600" font-size="14.5" fill="#F8FAFC">Free Courses</text>

    <rect x="328" y="0" width="154" height="42" rx="21" fill="#FFFFFF" fill-opacity="0.09" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
    <text x="405" y="26.5" text-anchor="middle" font-family="Inter" font-weight="600" font-size="14.5" fill="#F8FAFC">Browser Tools</text>

    <rect x="494" y="0" width="144" height="42" rx="21" fill="#FFFFFF" fill-opacity="0.09" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
    <text x="566" y="26.5" text-anchor="middle" font-family="Inter" font-weight="600" font-size="14.5" fill="#F8FAFC">1-on-1 Tutors</text>
  </g>

  <!-- Right column: Warm cream interactive study preview card (756..1144, symmetric 24px inner padding) -->
  <g>
    <rect x="756" y="74" width="388" height="482" rx="26" fill="url(#cardBg)" stroke="#FDE68A" stroke-opacity="0.45" stroke-width="1.5"/>

    <text x="782" y="116" font-family="Inter" font-weight="700" font-size="13" fill="#7C3AED" letter-spacing="1.4">SCRIPT · SOUND · PRACTICE</text>

    <!-- 3 Devanagari script tiles (780..1120) -->
    <rect x="780" y="138" width="104" height="108" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <path d="{tile_a_d}" fill="#1E1B4B"/>
    <text x="832" y="231" text-anchor="middle" font-family="Inter" font-weight="600" font-size="13.5" fill="#64748B">a · vowel</text>

    <rect x="898" y="138" width="104" height="108" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <path d="{tile_ka_d}" fill="#1E1B4B"/>
    <text x="950" y="231" text-anchor="middle" font-family="Inter" font-weight="600" font-size="13.5" fill="#64748B">ka · stop</text>

    <rect x="1016" y="138" width="104" height="108" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <path d="{tile_na_d}" fill="#1E1B4B"/>
    <text x="1068" y="231" text-anchor="middle" font-family="Inter" font-weight="600" font-size="13.5" fill="#64748B">na · dental</text>

    <!-- Word & greeting card (780..1120) -->
    <rect x="780" y="266" width="340" height="122" rx="18" fill="#1E1B4B"/>
    <text x="802" y="296" font-family="Inter" font-weight="600" font-size="12" fill="#A5B4FC" letter-spacing="1.1">EVERYDAY GREETING</text>
    <path d="{namaste_d}" fill="#FBBF24"/>
    <text x="802" y="372" font-family="Inter" font-weight="500" font-size="15" fill="#E2E8F0">namaste — hello / respectful greeting</text>

    <!-- Language course list inside card (780..1120) -->
    <rect x="780" y="408" width="340" height="124" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <text x="802" y="438" font-family="Plus Jakarta Sans" font-weight="700" font-size="15.5" fill="#0F172A">Hindi + Indian-language courses</text>
    <text x="802" y="464" font-family="Inter" font-weight="500" font-size="13.5" fill="#475569">Hindi · Marathi · Gujarati · Tamil</text>
    <text x="802" y="486" font-family="Inter" font-weight="500" font-size="13.5" fill="#475569">Telugu · Bengali · Punjabi · Urdu</text>
    <text x="802" y="514" font-family="Inter" font-weight="600" font-size="12.5" fill="#EA580C">Structured lessons · Quizzes · Free tools</text>
  </g>
</svg>"""


def build_post_01_svg() -> str:
    """Section 8 Post 1: Official Intro — free Hindi & Indian-language courses, no account."""
    hi_sub_d, _ = SHAPER.shape_to_path("एक भाषा, एक नई दुनिया।", 84, 434, 34, align="left")
    cards_svg = []
    lang_cards = [
        ("Hindi", "हिन्दी", "Structured course · tools · tutors"),
        ("Marathi", "मराठी", "5 levels · 15 lessons · quizzes"),
        ("Gujarati", "गुजराती", "5 levels · 15 lessons · quizzes"),
        ("Bengali", "बंगाली", "Course + phrase &amp; topic hub"),
        ("Tamil", "तमिल", "5 levels · 15 lessons · quizzes"),
        ("Telugu", "तेलुगु", "5 levels · 15 lessons · quizzes"),
        ("Punjabi", "पंजाबी", "5 levels · 15 lessons · quizzes"),
        ("Urdu", "उर्दू", "5 levels · 15 lessons · quizzes"),
    ]
    for idx, (eng, deva, meta) in enumerate(lang_cards):
        col = idx % 2
        row = idx // 2
        cx = 84 + col * 468
        cy = 510 + row * 144
        d_path, _ = SHAPER.shape_to_path(deva, cx + 412, cy + 56, 28, align="right")
        cards_svg.append(f"""
    <g>
      <rect x="{cx}" y="{cy}" width="444" height="124" rx="22" fill="#FFFFFF" fill-opacity="0.07" stroke="#FFFFFF" stroke-opacity="0.15" stroke-width="1.5"/>
      <text x="{cx+28}" y="{cy+52}" font-family="Plus Jakarta Sans" font-weight="800" font-size="28" fill="#FFFFFF">{eng}</text>
      <path d="{d_path}" fill="#FBBF24"/>
      <text x="{cx+28}" y="{cy+92}" font-family="Inter" font-weight="500" font-size="17" fill="#CBD5E1">{meta}</text>
    </g>""")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
  <defs>
    <linearGradient id="p1bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F1422"/>
      <stop offset="55%" stop-color="#181F36"/>
      <stop offset="100%" stop-color="#241934"/>
    </linearGradient>
    <radialGradient id="p1glow" cx="0.85" cy="0.15" r="0.55">
      <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#0F1422" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="p1cta" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#EA580C"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1350" fill="url(#p1bg)"/>
  <rect width="1080" height="1350" fill="url(#p1glow)"/>
  <rect x="34" y="34" width="1012" height="1282" rx="34" fill="none" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="1.5"/>

  <!-- Header -->
  {logo_group(84, 84, 72, "p1")}
  <text x="176" y="126" font-family="Plus Jakarta Sans" font-weight="800" font-size="36" fill="#FFFFFF">EkGuru</text>
  <text x="177" y="152" font-family="Inter" font-weight="500" font-size="16" fill="#CBD5E1">One Student. One Goal. One Guru.</text>
  <rect x="760" y="96" width="236" height="44" rx="22" fill="#FFFFFF" fill-opacity="0.09" stroke="#FBBF24" stroke-opacity="0.45" stroke-width="1.2"/>
  <text x="878" y="124" text-anchor="middle" font-family="Inter" font-weight="700" font-size="15" fill="#FDE68A" letter-spacing="0.8">NO ACCOUNT NEEDED</text>

  <!-- Main Title -->
  <text x="84" y="256" font-family="Plus Jakarta Sans" font-weight="800" font-size="58" fill="#FFFFFF" letter-spacing="-1.2">Free Hindi &amp; Indian-</text>
  <text x="84" y="328" font-family="Plus Jakarta Sans" font-weight="800" font-size="58" fill="#FBBF24" letter-spacing="-1.2">Language Courses.</text>
  <text x="84" y="382" font-family="Inter" font-weight="500" font-size="24" fill="#E2E8F0">Open in your browser. Saved on your device. Zero paywalls.</text>
  <path d="{hi_sub_d}" fill="#FDE68A"/>

  <text x="84" y="486" font-family="Inter" font-weight="700" font-size="15" fill="#94A3B8" letter-spacing="1.6">AVAILABLE COURSES ON EKGURU TODAY</text>

  {''.join(cards_svg)}

  <!-- Footer CTA -->
  <rect x="84" y="1126" width="912" height="132" rx="28" fill="#FFFFFF" fill-opacity="0.06" stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="1.5"/>
  <text x="120" y="1178" font-family="Plus Jakarta Sans" font-weight="700" font-size="25" fill="#FFFFFF">Start any course right away — free.</text>
  <text x="120" y="1215" font-family="Inter" font-weight="500" font-size="18" fill="#CBD5E1">Plus script guides, phrasebooks &amp; 1-on-1 tutor profiles.</text>
  <rect x="708" y="1156" width="254" height="72" rx="36" fill="url(#p1cta)"/>
  <text x="835" y="1201" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="25" fill="#FFFFFF">ekguru.shop</text>
</svg>"""


def build_post_02_svg() -> str:
    """Section 8 Post 2: /name-in-hindi/ showcase — 'Your name in Hindi, letter by letter.'"""
    anna_full_d, _ = SHAPER.shape_to_path("अन्ना", 770, 518, 76, align="center")
    step1_d, _ = SHAPER.shape_to_path("अ", 214, 730, 62, align="center")
    step2_d, _ = SHAPER.shape_to_path("न्", 540, 730, 62, align="center")
    step3_d, _ = SHAPER.shape_to_path("ना", 866, 730, 62, align="center")

    ex_david_d, _ = SHAPER.shape_to_path("डेविड", 336, 996, 44, align="right")
    ex_sara_d, _ = SHAPER.shape_to_path("सारा", 650, 996, 44, align="right")
    ex_liam_d, _ = SHAPER.shape_to_path("लियाम", 964, 996, 44, align="right")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
  <defs>
    <linearGradient id="p2bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FAF6EE"/>
      <stop offset="100%" stop-color="#F2E9DA"/>
    </linearGradient>
    <linearGradient id="p2card" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#151B2E"/>
      <stop offset="100%" stop-color="#231B38"/>
    </linearGradient>
    <linearGradient id="p2cta" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5B3DF5"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
  </defs>

  <rect width="1080" height="1350" fill="url(#p2bg)"/>
  <rect x="34" y="34" width="1012" height="1282" rx="34" fill="none" stroke="#1E1B4B" stroke-opacity="0.1" stroke-width="1.5"/>

  <!-- Header -->
  {logo_group(84, 80, 68, "p2")}
  <text x="170" y="120" font-family="Plus Jakarta Sans" font-weight="800" font-size="34" fill="#0F172A">EkGuru</text>
  <text x="171" y="145" font-family="Inter" font-weight="600" font-size="15.5" fill="#64748B">FREE INTERACTIVE TOOL</text>

  <!-- Headline -->
  <text x="84" y="246" font-family="Plus Jakarta Sans" font-weight="800" font-size="60" fill="#0F172A" letter-spacing="-1.3">Your name in Hindi,</text>
  <text x="84" y="318" font-family="Plus Jakarta Sans" font-weight="800" font-size="60" fill="#5B3DF5" letter-spacing="-1.3">letter by letter.</text>
  <text x="84" y="370" font-family="Inter" font-weight="500" font-size="23" fill="#334155">Devanagari writes by sound, not English spelling. See every syllable explained.</text>

  <!-- Main Demonstration Card: Anna -> अन्ना -->
  <rect x="84" y="408" width="912" height="172" rx="28" fill="url(#p2card)"/>
  <text x="132" y="454" font-family="Inter" font-weight="700" font-size="13.5" fill="#A5B4FC" letter-spacing="1.5">ENGLISH NAME</text>
  <text x="132" y="528" font-family="Plus Jakarta Sans" font-weight="800" font-size="64" fill="#FFFFFF">Anna</text>
  <text x="488" y="516" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="44" fill="#FBBF24">→</text>
  <text x="770" y="440" text-anchor="middle" font-family="Inter" font-weight="700" font-size="13.5" fill="#FDE68A" letter-spacing="1.5">DEVANAGARI SCRIPT</text>
  <path d="{anna_full_d}" fill="#FBBF24"/>
  <text x="770" y="560" text-anchor="middle" font-family="Inter" font-weight="500" font-size="17.5" fill="#E2E8F0">pronounced: an-nā</text>

  <!-- 3 Letter-by-letter tiles -->
  <text x="84" y="626" font-family="Inter" font-weight="700" font-size="15" fill="#475569" letter-spacing="1.5">HOW EACH SOUND CONNECTS</text>

  <g>
    <rect x="84" y="646" width="260" height="208" rx="24" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <path d="{step1_d}" fill="#1E1B4B"/>
    <text x="214" y="790" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="23" fill="#5B3DF5">1. a (short vowel)</text>
    <text x="214" y="822" text-anchor="middle" font-family="Inter" font-weight="500" font-size="16.5" fill="#475569">Starts the word</text>

    <text x="377" y="758" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="36" fill="#94A3B8">+</text>

    <rect x="410" y="646" width="260" height="208" rx="24" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <path d="{step2_d}" fill="#1E1B4B"/>
    <text x="540" y="790" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="23" fill="#5B3DF5">2. n (half-consonant)</text>
    <text x="540" y="822" text-anchor="middle" font-family="Inter" font-weight="500" font-size="16.5" fill="#475569">Halant drops the 'a'</text>

    <text x="703" y="758" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="36" fill="#94A3B8">+</text>

    <rect x="736" y="646" width="260" height="208" rx="24" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <path d="{step3_d}" fill="#1E1B4B"/>
    <text x="866" y="790" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="23" fill="#5B3DF5">3. nā (long vowel ā)</text>
    <text x="866" y="822" text-anchor="middle" font-family="Inter" font-weight="500" font-size="16.5" fill="#475569">Adds the long 'ā' mark</text>
  </g>

  <!-- More real examples row -->
  <text x="84" y="908" font-family="Inter" font-weight="700" font-size="15" fill="#475569" letter-spacing="1.5">MORE EXAMPLES IN THE TOOL</text>

  <rect x="84" y="930" width="284" height="104" rx="20" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="114" y="992" font-family="Plus Jakarta Sans" font-weight="700" font-size="25" fill="#0F172A">David</text>
  <path d="{ex_david_d}" fill="#EA580C"/>

  <rect x="398" y="930" width="284" height="104" rx="20" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="428" y="992" font-family="Plus Jakarta Sans" font-weight="700" font-size="25" fill="#0F172A">Sara</text>
  <path d="{ex_sara_d}" fill="#EA580C"/>

  <rect x="712" y="930" width="284" height="104" rx="20" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="742" y="992" font-family="Plus Jakarta Sans" font-weight="700" font-size="25" fill="#0F172A">Liam</text>
  <path d="{ex_liam_d}" fill="#EA580C"/>

  <!-- Bottom CTA Banner (zero overlap!) -->
  <rect x="84" y="1080" width="912" height="178" rx="28" fill="#0F172A"/>
  <text x="124" y="1148" font-family="Plus Jakarta Sans" font-weight="800" font-size="27" fill="#FFFFFF">Try your own name &amp; hear it spoken:</text>
  <text x="124" y="1192" font-family="Inter" font-weight="500" font-size="19" fill="#CBD5E1">Free browser tool · No sign-up required</text>
  <rect x="588" y="1130" width="376" height="78" rx="39" fill="url(#p2cta)"/>
  <text x="776" y="1178" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="21.5" fill="#FFFFFF">ekguru.shop/name-in-hindi</text>
</svg>"""


def build_post_03_svg() -> str:
    """Section 8 Post 3: 'Do I need to learn Devanagari?' educational tip card."""
    ta_dental_d, _ = SHAPER.shape_to_path("त", 193, 650, 68, align="center")
    ta_retro_d, _ = SHAPER.shape_to_path("ट", 411, 650, 68, align="center")
    da_dental_d, _ = SHAPER.shape_to_path("द", 669, 650, 68, align="center")
    da_retro_d, _ = SHAPER.shape_to_path("ड", 887, 650, 68, align="center")
    kitab_d, _ = SHAPER.shape_to_path("किताब", 464, 974, 48, align="right")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
  <defs>
    <linearGradient id="p3bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111625"/>
      <stop offset="100%" stop-color="#1D1732"/>
    </linearGradient>
    <linearGradient id="p3accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#EA580C"/>
    </linearGradient>
  </defs>

  <rect width="1080" height="1350" fill="url(#p3bg)"/>
  <rect x="34" y="34" width="1012" height="1282" rx="34" fill="none" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="1.5"/>

  <!-- Header -->
  {logo_group(84, 80, 68, "p3")}
  <text x="170" y="120" font-family="Plus Jakarta Sans" font-weight="800" font-size="34" fill="#FFFFFF">EkGuru</text>
  <text x="171" y="145" font-family="Inter" font-weight="600" font-size="15.5" fill="#FBBF24" letter-spacing="1">HONEST LEARNER FAQ</text>

  <!-- Question & Direct Answer -->
  <text x="84" y="244" font-family="Plus Jakarta Sans" font-weight="800" font-size="56" fill="#FFFFFF" letter-spacing="-1.1">“Do I need to learn</text>
  <text x="84" y="314" font-family="Plus Jakarta Sans" font-weight="800" font-size="56" fill="#FBBF24" letter-spacing="-1.1">Devanagari first?”</text>

  <rect x="84" y="352" width="912" height="118" rx="22" fill="#FFFFFF" fill-opacity="0.07" stroke="#FBBF24" stroke-opacity="0.35" stroke-width="1.5"/>
  <text x="118" y="402" font-family="Plus Jakarta Sans" font-weight="700" font-size="25" fill="#FFFFFF">Short answer: You can skip it at first —</text>
  <text x="118" y="440" font-family="Inter" font-weight="500" font-size="22" fill="#E2E8F0">but it takes ~2 weeks and immediately fixes your pronunciation.</text>

  <!-- Why Romanization misleads learners -->
  <text x="84" y="524" font-family="Inter" font-weight="700" font-size="15" fill="#94A3B8" letter-spacing="1.5">1. ENGLISH SPELLING HIDES DISTINCT HINDI SOUNDS</text>

  <g>
    <!-- Card Left: x=84..520 (mid=302; left half center=193, right half center=411) -->
    <rect x="84" y="546" width="436" height="226" rx="24" fill="#FFFDF9"/>
    <text x="302" y="582" text-anchor="middle" font-family="Inter" font-weight="700" font-size="15" fill="#64748B">Both written “ta” in English:</text>
    <path d="{ta_dental_d}" fill="#1E1B4B"/>
    <text x="193" y="698" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="700" font-size="19" fill="#5B3DF5">soft dental t</text>
    <text x="193" y="726" text-anchor="middle" font-family="Inter" font-weight="500" font-size="15" fill="#475569">tongue on teeth</text>

    <line x1="302" y1="600" x2="302" y2="742" stroke="#E2E8F0" stroke-width="2"/>

    <path d="{ta_retro_d}" fill="#EA580C"/>
    <text x="411" y="698" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="700" font-size="19" fill="#EA580C">retroflex ṭ</text>
    <text x="411" y="726" text-anchor="middle" font-family="Inter" font-weight="500" font-size="15" fill="#475569">tongue curled back</text>

    <!-- Card Right: x=560..996 (mid=778; left half center=669, right half center=887) -->
    <rect x="560" y="546" width="436" height="226" rx="24" fill="#FFFDF9"/>
    <text x="778" y="582" text-anchor="middle" font-family="Inter" font-weight="700" font-size="15" fill="#64748B">Both written “da” in English:</text>
    <path d="{da_dental_d}" fill="#1E1B4B"/>
    <text x="669" y="698" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="700" font-size="19" fill="#5B3DF5">soft dental d</text>
    <text x="669" y="726" text-anchor="middle" font-family="Inter" font-weight="500" font-size="15" fill="#475569">as in “daal” (lentils)</text>

    <line x1="778" y1="600" x2="778" y2="742" stroke="#E2E8F0" stroke-width="2"/>

    <path d="{da_retro_d}" fill="#EA580C"/>
    <text x="887" y="698" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="700" font-size="19" fill="#EA580C">retroflex ḍ</text>
    <text x="887" y="726" text-anchor="middle" font-family="Inter" font-weight="500" font-size="15" fill="#475569">crisp roof-of-mouth</text>
  </g>

  <!-- Phonetic advantage -->
  <text x="84" y="832" font-family="Inter" font-weight="700" font-size="15" fill="#94A3B8" letter-spacing="1.5">2. NO SILENT LETTERS — WHAT YOU SEE IS WHAT YOU SAY</text>
  <rect x="84" y="854" width="912" height="196" rx="24" fill="#FFFFFF" fill-opacity="0.06" stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="1.5"/>
  <text x="540" y="902" text-anchor="middle" font-family="Inter" font-weight="500" font-size="21" fill="#E2E8F0">Once you know the vowel marks (matras), you can sound out almost any word:</text>
  <path d="{kitab_d}" fill="#FDE68A"/>
  <text x="502" y="972" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="38" fill="#FBBF24">→</text>
  <text x="542" y="973" font-family="Plus Jakarta Sans" font-weight="800" font-size="42" fill="#FDE68A">ki-tā-b</text>
  <text x="540" y="1024" text-anchor="middle" font-family="Inter" font-weight="500" font-size="18.5" fill="#CBD5E1">kitāb (“book”) — consistent spelling, consistent vowel length.</text>

  <!-- CTA -->
  <rect x="84" y="1098" width="912" height="160" rx="28" fill="url(#p3accent)"/>
  <text x="126" y="1158" font-family="Plus Jakarta Sans" font-weight="800" font-size="28" fill="#FFFFFF">Read the full guide + free Devanagari chart:</text>
  <text x="126" y="1202" font-family="Inter" font-weight="600" font-size="21" fill="#FFFBEB">ekguru.shop/ask/do-i-need-to-learn-devanagari/</text>
  <text x="126" y="1234" font-family="Inter" font-weight="500" font-size="17" fill="#FEF3C7">Free alphabet audio &amp; stroke guide at ekguru.shop/hindi/alphabet/</text>
</svg>"""


def render_svgs_with_resvg(jobs: list[dict]) -> None:
    node_code = r"""
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { Resvg } from "@resvg/resvg-js";

const jobs = JSON.parse(readFileSync(0, "utf8"));
const fontDir = "docs/marketing/ekguru-brand-ad/05_brand_graphics/fonts";
const fontFiles = [
  path.join(fontDir, "plus-jakarta-sans-latin-600-normal.ttf"),
  path.join(fontDir, "plus-jakarta-sans-latin-700-normal.ttf"),
  path.join(fontDir, "plus-jakarta-sans-latin-800-normal.ttf"),
  path.join(fontDir, "inter-latin-400-normal.ttf"),
  path.join(fontDir, "inter-latin-500-normal.ttf"),
  path.join(fontDir, "inter-latin-600-normal.ttf"),
  path.join(fontDir, "inter-latin-700-normal.ttf"),
  "tools/assets/og-fonts/DejaVuSans.ttf",
  "tools/assets/og-fonts/DejaVuSans-Bold.ttf",
];

for (const job of jobs) {
  const resvg = new Resvg(job.svg, {
    textRendering: 2,
    font: {
      fontFiles,
      loadSystemFonts: false,
      defaultFontFamily: "Inter",
      sansSerifFamily: "Inter",
    },
  });
  const png = resvg.render().asPng();
  mkdirSync(path.dirname(job.png_path), { recursive: true });
  writeFileSync(job.png_path, png);
  console.log(`rendered ${job.png_path} (${(png.length / 1024).toFixed(1)} KB)`);
}
"""
    subprocess.run(
        ["node", "--input-type=module", "-e", node_code],
        input=json.dumps(jobs),
        text=True,
        cwd=str(ROOT),
        check=True,
    )


def main() -> None:
    OG_SVG_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    og_svg = build_og_cover_svg()
    p1_svg = build_post_01_svg()
    p2_svg = build_post_02_svg()
    p3_svg = build_post_03_svg()

    (OG_SVG_DIR / "ekguru_og_cover_1200x630.svg").write_text(og_svg, encoding="utf-8")
    (POSTS_DIR / "post_01_ekguru_intro_1080x1350.svg").write_text(p1_svg, encoding="utf-8")
    (POSTS_DIR / "post_02_name_in_hindi_tool_1080x1350.svg").write_text(p2_svg, encoding="utf-8")
    (POSTS_DIR / "post_03_devanagari_tip_1080x1350.svg").write_text(p3_svg, encoding="utf-8")

    og_tmp_png = OG_SVG_DIR / "ekguru_og_cover_1200x630.png"
    p1_png = POSTS_DIR / "post_01_ekguru_intro_1080x1350.png"
    p2_png = POSTS_DIR / "post_02_name_in_hindi_tool_1080x1350.png"
    p3_png = POSTS_DIR / "post_03_devanagari_tip_1080x1350.png"

    render_svgs_with_resvg([
        {"svg": og_svg, "png_path": str(og_tmp_png)},
        {"svg": p1_svg, "png_path": str(p1_png)},
        {"svg": p2_svg, "png_path": str(p2_png)},
        {"svg": p3_svg, "png_path": str(p3_png)},
    ])

    with Image.open(og_tmp_png) as im:
        rgb = im.convert("RGB")
        assert rgb.size == (1200, 630), f"Unexpected OG size: {rgb.size}"
        jpg_out = ROOT / "images/og-cover.jpg"
        webp_out = ROOT / "images/og-cover.webp"
        rgb.save(jpg_out, format="JPEG", quality=90, optimize=True, progressive=True)
        rgb.save(webp_out, format="WEBP", quality=88, method=6)
        print(f"wrote {jpg_out.relative_to(ROOT)} ({jpg_out.stat().st_size / 1024:.1f} KB)")
        print(f"wrote {webp_out.relative_to(ROOT)} ({webp_out.stat().st_size / 1024:.1f} KB)")

    for png_file in (og_tmp_png, p1_png, p2_png, p3_png):
        with Image.open(png_file) as im:
            im.save(png_file, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
