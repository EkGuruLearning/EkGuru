#!/usr/bin/env python3
"""Render the remaining visual & video deliverables for the Nov 2026 Distribution Kit:

1. Post 3 Complete 4-Slide Devanagari Carousel (Slides 2, 3, 4 at 1080x1350 SVG + PNG)
   in 02_official_profile_first_3_posts/
2. Printable Hindi Class Home Practice Sheet (1240x1754 A4 SVG + PNG)
   in 06_backlink_outreach_pack/ (promised in Email 2 of DISTRIBUTION-KIT-2026-11-24.md)
3. Three ready-to-upload 1080x1920 (9:16, 30fps, H.264 + AAC) MP4 Shorts/Reels
   in 03_shorts_reels_pack/ matching Section 4 Scripts 1, 2, and 3:
     - short_01_count_1_to_10_hindi_9x16.mp4  (27.0s)
     - short_02_your_name_in_hindi_9x16.mp4   (24.0s)
     - short_03_auto_ride_3_phrases_9x16.mp4  (25.0s)
   plus cover PNGs for visual inspection.

All Devanagari text is shaped via HarfBuzz (uharfbuzz + fontTools) into exact vector
paths so zero glyph/matra shaping errors can ever occur.
"""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path

import imageio_ffmpeg
from PIL import Image

from build_visual_assets import (
    OUT_DIR,
    POSTS_DIR,
    ROOT,
    SHAPER,
    logo_group,
    render_svgs_with_resvg,
)

SHORTS_DIR = OUT_DIR / "03_shorts_reels_pack"
OUTREACH_DIR = OUT_DIR / "06_backlink_outreach_pack"
SCORE_FLAC = ROOT / "docs/marketing/ekguru-brand-ad/04_music_and_sfx/ekguru_cinematic_score_60s.flac"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def deva_path(text: str, x: float, y: float, size: float, fill: str, align: str = "center") -> str:
    d, _ = SHAPER.shape_to_path(text, x, y, size, align=align)
    return f'<path d="{d}" fill="{fill}"/>'


def assert_no_unshaped_devanagari(svg: str, label: str) -> None:
    for m in re.finditer(r"<text[^>]*>(.*?)</text>", svg, re.S):
        if re.search(r"[\u0900-\u097F]", m.group(1)):
            raise ValueError(f"Unshaped Devanagari inside <text> in {label}: {m.group(1)!r}")


# ---------------------------------------------------------------------------
# 1. Post 3 Carousel Slides 2, 3, and 4 (1080x1350)
# ---------------------------------------------------------------------------

def build_post03_slide02_svg() -> str:
    """Slide 2/4: Why Romanised Hindi Hits a Wall (kal / kaal / khaal)."""
    rows = [
        ("कल", "kal", "yesterday / tomorrow", "short vowel ‘a’ + unaspirated ‘k’", "#38BDF8"),
        ("काल", "kāl", "time / era / period", "long vowel ‘ā’ matra changes the meaning", "#FBBF24"),
        ("खाल", "khāl", "skin / hide / bark", "aspirated ‘kh’ consonant + long ‘ā’ matra", "#F472B6"),
    ]
    cards = []
    y0 = 408
    for idx, (deva, rom, eng, note, col) in enumerate(rows):
        cy = y0 + idx * 212
        cards.append(f"""
        <rect x="84" y="{cy}" width="912" height="184" rx="26" fill="#FFFFFF" fill-opacity="0.06" stroke="{col}" stroke-opacity="0.45" stroke-width="2"/>
        <rect x="116" y="{cy + 26}" width="186" height="132" rx="20" fill="#0F172A" stroke="{col}" stroke-opacity="0.35" stroke-width="1.5"/>
        {deva_path(deva, 209, cy + 114, 68, col, "center")}
        <text x="342" y="{cy + 74}" font-family="Plus Jakarta Sans" font-weight="800" font-size="34" fill="#FFFFFF">{esc(rom)}  —  {esc(eng)}</text>
        <text x="342" y="{cy + 122}" font-family="Inter" font-weight="500" font-size="21" fill="#CBD5E1">{esc(note)}</text>
        <text x="342" y="{cy + 154}" font-family="Inter" font-weight="600" font-size="17" fill="{col}">Casual texting often spells all three “kal” or “kaal”</text>
        """)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
  <defs>
    <linearGradient id="bg32" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="55%" stop-color="#1E1B4B"/>
      <stop offset="100%" stop-color="#311042"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1350" fill="url(#bg32)"/>
  {logo_group(84, 72, 68, "p3s2")}
  <text x="172" y="114" font-family="Plus Jakarta Sans" font-weight="800" font-size="30" fill="#FFFFFF">EkGuru</text>
  <text x="172" y="140" font-family="Inter" font-weight="500" font-size="17" fill="#FDE68A">Devanagari Guide · Slide 2 of 4</text>
  <rect x="854" y="84" width="142" height="44" rx="22" fill="#FFFFFF" fill-opacity="0.1" stroke="#FBBF24" stroke-opacity="0.5"/>
  <text x="925" y="113" text-anchor="middle" font-family="Inter" font-weight="700" font-size="18" fill="#FDE68A">2 / 4 →</text>

  <text x="84" y="246" font-family="Plus Jakarta Sans" font-weight="800" font-size="48" fill="#FFFFFF">Why Romanised Hindi</text>
  <text x="84" y="306" font-family="Plus Jakarta Sans" font-weight="800" font-size="48" fill="#FBBF24">Hits a Ceiling Fast</text>
  <text x="84" y="358" font-family="Inter" font-weight="500" font-size="22" fill="#CBD5E1">English letters hide two contrasts Hindi relies on in every sentence:</text>

  {''.join(cards)}

  <rect x="84" y="1068" width="912" height="194" rx="28" fill="#EA580C" fill-opacity="0.18" stroke="#FB923C" stroke-opacity="0.55" stroke-width="2"/>
  <text x="540" y="1132" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="29" fill="#FFFFFF">Devanagari removes the guesswork immediately.</text>
  <text x="540" y="1178" text-anchor="middle" font-family="Inter" font-weight="500" font-size="21" fill="#FED7AA">Every vowel length and breathy consonant has its own unmistakable mark.</text>
  <text x="540" y="1224" text-anchor="middle" font-family="Inter" font-weight="700" font-size="19" fill="#FDE68A">Swipe for how the sound grid works →</text>
</svg>"""


def build_post03_slide03_svg() -> str:
    """Slide 3/4: Devanagari Is a Logical Sound Grid."""
    cols = [
        ("क", "ka", "unvoiced · light", "#38BDF8"),
        ("ख", "kha", "unvoiced · breathy", "#FBBF24"),
        ("ग", "ga", "voiced · light", "#34D399"),
        ("घ", "gha", "voiced · breathy", "#F472B6"),
    ]
    boxes = []
    for i, (ch, rom, desc, col) in enumerate(cols):
        bx = 84 + i * 234
        boxes.append(f"""
        <rect x="{bx}" y="438" width="210" height="250" rx="24" fill="#FFFFFF" fill-opacity="0.07" stroke="{col}" stroke-opacity="0.55" stroke-width="2"/>
        {deva_path(ch, bx + 105, 555, 92, "#FFFFFF", "center")}
        <text x="{bx + 105}" y="616" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="30" fill="{col}">{rom}</text>
        <text x="{bx + 105}" y="654" text-anchor="middle" font-family="Inter" font-weight="500" font-size="17" fill="#CBD5E1">{esc(desc)}</text>
        """)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
  <defs>
    <linearGradient id="bg33" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="55%" stop-color="#1E1B4B"/>
      <stop offset="100%" stop-color="#172554"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1350" fill="url(#bg33)"/>
  {logo_group(84, 72, 68, "p3s3")}
  <text x="172" y="114" font-family="Plus Jakarta Sans" font-weight="800" font-size="30" fill="#FFFFFF">EkGuru</text>
  <text x="172" y="140" font-family="Inter" font-weight="500" font-size="17" fill="#FDE68A">Devanagari Guide · Slide 3 of 4</text>
  <rect x="854" y="84" width="142" height="44" rx="22" fill="#FFFFFF" fill-opacity="0.1" stroke="#38BDF8" stroke-opacity="0.5"/>
  <text x="925" y="113" text-anchor="middle" font-family="Inter" font-weight="700" font-size="18" fill="#BAE6FD">3 / 4 →</text>

  <text x="84" y="246" font-family="Plus Jakarta Sans" font-weight="800" font-size="46" fill="#FFFFFF">It’s Organised by Sound,</text>
  <text x="84" y="306" font-family="Plus Jakarta Sans" font-weight="800" font-size="46" fill="#38BDF8">Not a Random Alphabet</text>
  <text x="84" y="362" font-family="Inter" font-weight="500" font-size="22" fill="#CBD5E1">Every consonant row follows the exact same 4-step pattern in your mouth:</text>

  <text x="84" y="416" font-family="Inter" font-weight="700" font-size="16" fill="#94A3B8" letter-spacing="1.4">ROW 1 EXAMPLE — THROAT (VELAR) CONSONANTS</text>
  {''.join(boxes)}

  <rect x="84" y="736" width="912" height="264" rx="28" fill="#FFFFFF" fill-opacity="0.06" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1.5"/>
  <text x="540" y="792" text-anchor="middle" font-family="Inter" font-weight="700" font-size="17" fill="#FDE68A" letter-spacing="1.4">ADD ONE VOWEL MARK (MATRA) TO ANY CONSONANT</text>
  {deva_path("क   का   कि   की   कु   के", 540, 888, 66, "#FFFFFF", "center")}
  <text x="540" y="952" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="700" font-size="28" fill="#FBBF24">ka  ·  kā  ·  ki  ·  kī  ·  ku  ·  ke</text>
  <text x="540" y="984" text-anchor="middle" font-family="Inter" font-weight="500" font-size="18" fill="#CBD5E1">Learn those vowel marks once and they work across the entire script.</text>

  <rect x="84" y="1050" width="912" height="210" rx="28" fill="#1E293B" stroke="#38BDF8" stroke-opacity="0.4" stroke-width="2"/>
  <text x="540" y="1116" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="30" fill="#FFFFFF">Bonus: One Script, Multiple Languages</text>
  <text x="540" y="1166" text-anchor="middle" font-family="Inter" font-weight="500" font-size="21" fill="#E2E8F0">Devanagari is also used for Marathi (Pune &amp; Mumbai) and Nepali.</text>
  <text x="540" y="1216" text-anchor="middle" font-family="Inter" font-weight="700" font-size="19" fill="#38BDF8">Swipe for the free 2-week plan →</text>
</svg>"""


def build_post03_slide04_svg() -> str:
    """Slide 4/4: Practical 2-Week Plan + Verified Links."""
    steps = [
        ("Days 1–4", "Vowels &amp; Matras", "अ आ इ ई उ ऊ ए ऐ ओ औ", "Hear &amp; spot each vowel sign", "#FBBF24"),
        ("Days 5–10", "5 Consonant Rows", "", "20 minutes a day, row by row with tap-to-hear audio", "#38BDF8"),
        ("Days 11–14", "Real Everyday Words", "", "Read signs, names, food menus &amp; beginner lessons", "#34D399"),
    ]
    step_svg = []
    for i, (tag, title, deva_sample, sub, col) in enumerate(steps):
        sy = 404 + i * 184
        if deva_sample:
            sub_block = f"""
            {deva_path(deva_sample, 314, sy + 114, 28, "#FDE68A", "left")}
            <text x="646" y="{sy + 112}" font-family="Inter" font-weight="500" font-size="19.5" fill="#CBD5E1">— {sub}</text>
            """
        else:
            sub_block = f'<text x="314" y="{sy + 114}" font-family="Inter" font-weight="500" font-size="20.5" fill="#CBD5E1">{sub}</text>'
        step_svg.append(f"""
        <rect x="84" y="{sy}" width="912" height="158" rx="24" fill="#FFFFFF" fill-opacity="0.06" stroke="{col}" stroke-opacity="0.5" stroke-width="2"/>
        <rect x="114" y="{sy + 44}" width="166" height="70" rx="18" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-opacity="0.6"/>
        <text x="197" y="{sy + 88}" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="24" fill="{col}">{tag}</text>
        <text x="314" y="{sy + 68}" font-family="Plus Jakarta Sans" font-weight="800" font-size="30" fill="#FFFFFF">{title}</text>
        {sub_block}
        """)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
  <defs>
    <linearGradient id="bg34" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="55%" stop-color="#1E1B4B"/>
      <stop offset="100%" stop-color="#311042"/>
    </linearGradient>
    <linearGradient id="cta34" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#EA580C"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1350" fill="url(#bg34)"/>
  {logo_group(84, 72, 68, "p3s4")}
  <text x="172" y="114" font-family="Plus Jakarta Sans" font-weight="800" font-size="30" fill="#FFFFFF">EkGuru</text>
  <text x="172" y="140" font-family="Inter" font-weight="500" font-size="17" fill="#FDE68A">Devanagari Guide · Slide 4 of 4</text>
  <rect x="854" y="84" width="142" height="44" rx="22" fill="#34D399" fill-opacity="0.18" stroke="#34D399" stroke-opacity="0.6"/>
  <text x="925" y="113" text-anchor="middle" font-family="Inter" font-weight="700" font-size="18" fill="#A7F3D0">4 / 4 ✓</text>

  <text x="84" y="246" font-family="Plus Jakarta Sans" font-weight="800" font-size="48" fill="#FFFFFF">How to Learn Devanagari</text>
  <text x="84" y="306" font-family="Plus Jakarta Sans" font-weight="800" font-size="48" fill="#34D399">in ~2 Steady Weeks</text>
  <text x="84" y="358" font-family="Inter" font-weight="500" font-size="22" fill="#CBD5E1">20 minutes a day in your browser — free, no account or app download:</text>

  {''.join(step_svg)}

  <rect x="84" y="982" width="912" height="284" rx="30" fill="url(#cta34)"/>
  {deva_path("एक भाषा, एक नई दुनिया।", 540, 1054, 42, "#FFFBEB", "center")}
  <text x="540" y="1114" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="30" fill="#FFFFFF">Start Free on EkGuru — No Login Needed</text>
  <text x="540" y="1166" text-anchor="middle" font-family="Inter" font-weight="700" font-size="23" fill="#FFFBEB">1. Interactive Alphabet:  ekguru.shop/hindi/alphabet/</text>
  <text x="540" y="1208" text-anchor="middle" font-family="Inter" font-weight="700" font-size="22" fill="#FEF3C7">2. Full Article:  ekguru.shop/ask/do-i-need-to-learn-devanagari/</text>
  <text x="540" y="1244" text-anchor="middle" font-family="Inter" font-weight="600" font-size="18" fill="#FDE68A">Save this post for your Week 1 study routine</text>
</svg>"""


# ---------------------------------------------------------------------------
# 2. Printable Hindi Class Home Practice Sheet (1240x1754 A4)
# ---------------------------------------------------------------------------

def build_class_handout_svg() -> str:
    """1-page A4 printable handout offered in Email 2 to Hindi schools & parent groups."""
    tools = [
        ("1. Devanagari Alphabet Chart & Audio", "ekguru.shop/hindi/alphabet/", "Tap any vowel or consonant to hear pronunciation and practice recognition."),
        ("2. Free 30-Day Daily Hindi Path", "ekguru.shop/daily-hindi/", "Short 20-minute daily lessons; progress saves locally in the browser."),
        ("3. Hindi Numbers 1 to 100", "ekguru.shop/learn/hindi/numbers/", "Full table + interactive number reader for everyday counting practice."),
        ("4. Write Your Name in Hindi", "ekguru.shop/name-in-hindi/", "Kids type their name and see every Devanagari letter explained step by step."),
        ("5. Printable Practice Worksheets", "ekguru.shop/learn/hindi/practice/worksheets/", "Generate clean print-ready Hindi worksheets with answer keys at home."),
    ]
    tool_cards = []
    for idx, (title, url, desc) in enumerate(tools):
        ty = 398 + idx * 142
        tool_cards.append(f"""
        <rect x="80" y="{ty}" width="1080" height="122" rx="18" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2"/>
        <rect x="104" y="{ty + 22}" width="8" height="78" rx="4" fill="#EA580C"/>
        <text x="132" y="{ty + 50}" font-family="Plus Jakarta Sans" font-weight="800" font-size="24" fill="#0F172A">{esc(title)}</text>
        <text x="1132" y="{ty + 50}" text-anchor="end" font-family="Inter" font-weight="700" font-size="20" fill="#C2410C">{esc(url)}</text>
        <text x="132" y="{ty + 90}" font-family="Inter" font-weight="500" font-size="19" fill="#475569">{esc(desc)}</text>
        """)

    phrases = [
        ("नमस्ते", "Namaste", "Hello / respectful greeting"),
        ("धन्यवाद", "Dhanyavaad", "Thank you"),
        ("कृपया", "Kripaya", "Please"),
        ("हाँ  /  नहीं", "Haan  /  Nahin", "Yes  /  No"),
        ("मेरा नाम ... है।", "Mera naam ... hai.", "My name is ..."),
    ]
    phrase_rows = []
    for idx, (deva, rom, eng) in enumerate(phrases):
        py = 1236 + idx * 72
        bg = "#F8FAFC" if idx % 2 == 0 else "#FFFFFF"
        phrase_rows.append(f"""
        <rect x="80" y="{py}" width="1080" height="68" rx="10" fill="{bg}" stroke="#E2E8F0" stroke-width="1"/>
        {deva_path(deva, 118, py + 46, 32, "#1E1B4B", "left")}
        <text x="480" y="{py + 44}" font-family="Plus Jakarta Sans" font-weight="700" font-size="22" fill="#C2410C">{esc(rom)}</text>
        <text x="800" y="{py + 44}" font-family="Inter" font-weight="500" font-size="21" fill="#334155">{esc(eng)}</text>
        """)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="1754" viewBox="0 0 1240 1754">
  <rect width="1240" height="1754" fill="#FFFDF9"/>
  <rect x="48" y="48" width="1144" height="1658" rx="28" fill="#FFFDF9" stroke="#CBD5E1" stroke-width="2"/>

  <!-- Header Banner -->
  <rect x="80" y="80" width="1080" height="224" rx="24" fill="#1E1B4B"/>
  {logo_group(116, 118, 92, "handout")}
  <text x="234" y="160" font-family="Plus Jakarta Sans" font-weight="800" font-size="42" fill="#FFFFFF">EkGuru — At-Home Hindi Practice Sheet</text>
  <text x="234" y="204" font-family="Inter" font-weight="500" font-size="22" fill="#E2E8F0">Free browser tools for students &amp; families · No login, email, or app install needed</text>
  {deva_path("एक भाषा, एक नई दुनिया।", 234, 258, 30, "#FDE68A", "left")}
  <text x="1124" y="258" text-anchor="end" font-family="Plus Jakarta Sans" font-weight="700" font-size="22" fill="#FBBF24">https://ekguru.shop</text>

  <!-- Section 1 -->
  <text x="80" y="366" font-family="Plus Jakarta Sans" font-weight="800" font-size="26" fill="#1E1B4B">10-Minute Daily Home Practice Links (Open in Any Phone, Tablet, or Computer Browser)</text>
  {''.join(tool_cards)}

  <!-- Section 2 -->
  <text x="80" y="1166" font-family="Plus Jakarta Sans" font-weight="800" font-size="26" fill="#1E1B4B">5 Everyday Family Phrases to Say Out Loud Together This Week</text>
  <rect x="80" y="1186" width="1080" height="44" rx="8" fill="#1E1B4B"/>
  <text x="118" y="1215" font-family="Inter" font-weight="700" font-size="18" fill="#FFFFFF">DEVANAGARI</text>
  <text x="480" y="1215" font-family="Inter" font-weight="700" font-size="18" fill="#FDE68A">HOW TO SAY IT</text>
  <text x="800" y="1215" font-family="Inter" font-weight="700" font-size="18" fill="#FFFFFF">MEANING</text>
  {''.join(phrase_rows)}

  <!-- Footer -->
  <text x="620" y="1654" text-anchor="middle" font-family="Inter" font-weight="600" font-size="18" fill="#475569">Free to print and share with Hindi school students &amp; parent groups · Learn Indian Languages. Connect with India. · ekguru.shop</text>
</svg>"""


# ---------------------------------------------------------------------------
# 3. Three 9:16 Vertical Shorts/Reels (1080x1920, 30fps, H.264 + AAC)
# ---------------------------------------------------------------------------

def short_shell_svg(badge: str, progress: float, body_svg: str, uid: str) -> str:
    pw = max(24, int(912 * max(0.0, min(1.0, progress))))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  <defs>
    <linearGradient id="sbg_{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="52%" stop-color="#1E1B4B"/>
      <stop offset="100%" stop-color="#311042"/>
    </linearGradient>
    <linearGradient id="scta_{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#EA580C"/>
      <stop offset="100%" stop-color="#F59E0B"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1920" fill="url(#sbg_{uid})"/>
  <circle cx="920" cy="240" r="280" fill="#EA580C" fill-opacity="0.12"/>
  <circle cx="160" cy="1640" r="320" fill="#6366F1" fill-opacity="0.14"/>

  <!-- Top Bar -->
  {logo_group(84, 108, 76, uid)}
  <text x="180" y="152" font-family="Plus Jakarta Sans" font-weight="800" font-size="34" fill="#FFFFFF">EkGuru</text>
  <text x="180" y="182" font-family="Inter" font-weight="500" font-size="19" fill="#FDE68A">ekguru.shop · Free Indian Languages</text>

  <rect x="690" y="120" width="306" height="52" rx="26" fill="#FFFFFF" fill-opacity="0.1" stroke="#FBBF24" stroke-opacity="0.45"/>
  <text x="843" y="154" text-anchor="middle" font-family="Inter" font-weight="700" font-size="20" fill="#FDE68A">{esc(badge)}</text>

  <!-- Progress Bar -->
  <rect x="84" y="226" width="912" height="10" rx="5" fill="#FFFFFF" fill-opacity="0.14"/>
  <rect x="84" y="226" width="{pw}" height="10" rx="5" fill="url(#scta_{uid})"/>

  {body_svg}

  <!-- Bottom Safe Footer -->
  <text x="540" y="1808" text-anchor="middle" font-family="Inter" font-weight="600" font-size="22" fill="#94A3B8">Learn Indian Languages. Connect with India.</text>
</svg>"""


def make_short01_slides() -> list[tuple[str, float]]:
    """Script 1: Count 1 to 10 in Hindi (27.0s total)."""
    slides: list[tuple[str, float]] = []
    hook_body = f"""
    <rect x="84" y="420" width="912" height="980" rx="40" fill="#FFFFFF" fill-opacity="0.06" stroke="#FBBF24" stroke-opacity="0.45" stroke-width="2.5"/>
    <text x="540" y="560" text-anchor="middle" font-family="Inter" font-weight="700" font-size="26" fill="#FBBF24" letter-spacing="2">20-SECOND HINDI CHALLENGE</text>
    <text x="540" y="680" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="68" fill="#FFFFFF">Count 1 to 10</text>
    <text x="540" y="766" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="68" fill="#FDE68A">in Hindi</text>
    {deva_path("१  से  १०  हिंदी गिनती", 540, 940, 74, "#38BDF8", "center")}
    <text x="540" y="1080" text-anchor="middle" font-family="Inter" font-weight="500" font-size="32" fill="#E2E8F0">Say each number out loud with the screen!</text>
    <rect x="230" y="1170" width="620" height="96" rx="48" fill="url(#scta_s1h)"/>
    <text x="540" y="1230" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="34" fill="#FFFFFF">Ready? Let’s go →</text>
    """
    slides.append((short_shell_svg("HINDI NUMBERS 1–10", 0.06, hook_body, "s1h"), 3.0))

    nums = [
        ("1", "१", "एक", "ek", "eh-k"),
        ("2", "२", "दो", "do", "doh"),
        ("3", "३", "तीन", "teen", "teen"),
        ("4", "४", "चार", "chaar", "chaar"),
        ("5", "५", "पाँच", "paanch", "paanch (nasal a)"),
        ("6", "६", "छह", "chhah", "chhah"),
        ("7", "७", "सात", "saat", "saat"),
        ("8", "८", "आठ", "aath", "aath (retroflex th)"),
        ("9", "९", "नौ", "nau", "nau"),
        ("10", "१०", "दस", "das", "duh-s"),
    ]
    for i, (lat_n, dev_n, word, rom, tip) in enumerate(nums):
        uid = f"s1n{i+1}"
        prog = (i + 1) / 11.0
        body = f"""
        <rect x="84" y="380" width="912" height="1060" rx="42" fill="#FFFFFF" fill-opacity="0.07" stroke="#38BDF8" stroke-opacity="0.45" stroke-width="2.5"/>
        <text x="540" y="490" text-anchor="middle" font-family="Inter" font-weight="700" font-size="28" fill="#94A3B8" letter-spacing="2">NUMBER {lat_n} OF 10</text>
        <rect x="270" y="540" width="240" height="200" rx="28" fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.18"/>
        <text x="390" y="676" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="112" fill="#FFFFFF">{lat_n}</text>
        <rect x="570" y="540" width="240" height="200" rx="28" fill="#0F172A" stroke="#FBBF24" stroke-opacity="0.5"/>
        {deva_path(dev_n, 690, 676, 112, "#FBBF24", "center")}

        {deva_path(word, 540, 960, 152, "#FFFFFF", "center")}
        <text x="540" y="1110" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="78" fill="#FDE68A">“{rom}”</text>
        <text x="540" y="1200" text-anchor="middle" font-family="Inter" font-weight="500" font-size="30" fill="#CBD5E1">Sound tip: {esc(tip)}</text>
        <text x="540" y="1340" text-anchor="middle" font-family="Inter" font-weight="600" font-size="26" fill="#38BDF8">ekguru.shop/learn/hindi/numbers/</text>
        """
        slides.append((short_shell_svg(f"COUNT {lat_n} / 10", prog, body, uid), 2.0))

    cta_body = f"""
    <rect x="84" y="400" width="912" height="1040" rx="42" fill="#FFFFFF" fill-opacity="0.07" stroke="#34D399" stroke-opacity="0.55" stroke-width="2.5"/>
    <text x="540" y="530" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="56" fill="#34D399">You Just Counted 1–10!</text>
    {deva_path("एक · दो · तीन · चार · पाँच", 540, 670, 52, "#FFFFFF", "center")}
    {deva_path("छह · सात · आठ · नौ · दस", 540, 760, 52, "#FDE68A", "center")}
    <text x="540" y="900" text-anchor="middle" font-family="Inter" font-weight="500" font-size="32" fill="#E2E8F0">Practice numbers 1 to 100 with tap-to-hear audio</text>
    <text x="540" y="952" text-anchor="middle" font-family="Inter" font-weight="500" font-size="32" fill="#E2E8F0">and an instant Hindi number reader — 100% free.</text>
    <rect x="134" y="1060" width="812" height="176" rx="34" fill="url(#scta_s1c)"/>
    <text x="540" y="1136" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="34" fill="#FFFFFF">ekguru.shop/learn/hindi/numbers/</text>
    <text x="540" y="1192" text-anchor="middle" font-family="Inter" font-weight="600" font-size="25" fill="#FFFBEB">No account · No app install · Link in bio</text>
    {deva_path("एक भाषा, एक नई दुनिया।", 540, 1348, 42, "#FDE68A", "center")}
    """
    slides.append((short_shell_svg("NUMBERS 1–100 FREE", 1.0, cta_body, "s1c"), 4.0))
    return slides


def make_short02_slides() -> list[tuple[str, float]]:
    """Script 2: Your Name in Hindi (/name-in-hindi/) — 24.0s total."""
    slides: list[tuple[str, float]] = []
    hook = f"""
    <rect x="84" y="420" width="912" height="980" rx="40" fill="#FFFFFF" fill-opacity="0.06" stroke="#FBBF24" stroke-opacity="0.45" stroke-width="2.5"/>
    <text x="540" y="560" text-anchor="middle" font-family="Inter" font-weight="700" font-size="26" fill="#FBBF24" letter-spacing="2">FREE BROWSER TOOL</text>
    <text x="540" y="676" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="62" fill="#FFFFFF">How Does Your Name</text>
    <text x="540" y="758" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="62" fill="#FDE68A">Look in Hindi?</text>
    {deva_path("आपका नाम हिंदी में", 540, 930, 76, "#38BDF8", "center")}
    <text x="540" y="1074" text-anchor="middle" font-family="Inter" font-weight="500" font-size="31" fill="#E2E8F0">See every Devanagari letter explained step by step.</text>
    <rect x="190" y="1168" width="700" height="98" rx="49" fill="url(#scta_s2h)"/>
    <text x="540" y="1230" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="32" fill="#FFFFFF">ekguru.shop/name-in-hindi/</text>
    """
    slides.append((short_shell_svg("NAME IN HINDI TOOL", 0.12, hook, "s2h"), 3.5))

    examples = [
        ("Anna", "अन्ना", "अ   +   न्   +   ना", "a  +  half-n (halant)  +  nā", "Double ‘nn’ joins cleanly into a conjunct cluster", 5.5),
        ("David", "डेविड", "डे   +   वि   +   ड", "de  +  vi  +  d", "Short ‘i’ matra wraps to the left of ‘va’", 5.5),
        ("Maya", "माया", "मा   +   या", "mā  +  yā", "Two open long ‘ā’ vowel marks — rhythmic &amp; clear", 5.0),
    ]
    for idx, (eng, deva, deva_parts, rom_parts, note, dur) in enumerate(examples):
        uid = f"s2e{idx+1}"
        prog = (idx + 2) / 5.0
        body = f"""
        <rect x="84" y="370" width="912" height="1080" rx="42" fill="#FFFFFF" fill-opacity="0.07" stroke="#38BDF8" stroke-opacity="0.45" stroke-width="2.5"/>
        <text x="144" y="458" font-family="Inter" font-weight="700" font-size="22" fill="#94A3B8" letter-spacing="1.5">TYPE ANY NAME IN ENGLISH</text>
        <rect x="144" y="484" width="792" height="118" rx="24" fill="#0F172A" stroke="#FBBF24" stroke-opacity="0.55" stroke-width="2"/>
        <text x="190" y="560" font-family="Plus Jakarta Sans" font-weight="800" font-size="52" fill="#FFFFFF">{eng}</text>
        <text x="890" y="558" text-anchor="end" font-family="Inter" font-weight="700" font-size="24" fill="#FBBF24">Convert ✓</text>

        <text x="540" y="694" text-anchor="middle" font-family="Inter" font-weight="700" font-size="22" fill="#38BDF8" letter-spacing="1.6">DEVANAGARI SCRIPT</text>
        {deva_path(deva, 540, 885, 168, "#FDE68A", "center")}

        <rect x="134" y="978" width="812" height="206" rx="26" fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.16"/>
        <text x="540" y="1032" text-anchor="middle" font-family="Inter" font-weight="700" font-size="20" fill="#94A3B8" letter-spacing="1.5">LETTER-BY-LETTER BREAKDOWN</text>
        {deva_path(deva_parts, 540, 1108, 48, "#FFFFFF", "center")}
        <text x="540" y="1162" text-anchor="middle" font-family="Inter" font-weight="600" font-size="25" fill="#38BDF8">{rom_parts}</text>

        <text x="540" y="1272" text-anchor="middle" font-family="Inter" font-weight="500" font-size="26" fill="#E2E8F0">{note}</text>
        <text x="540" y="1376" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="700" font-size="27" fill="#FBBF24">ekguru.shop/name-in-hindi/</text>
        """
        slides.append((short_shell_svg(f"EXAMPLE {idx+1} / 3", prog, body, uid), dur))

    cta = f"""
    <rect x="84" y="410" width="912" height="1020" rx="42" fill="#FFFFFF" fill-opacity="0.07" stroke="#34D399" stroke-opacity="0.55" stroke-width="2.5"/>
    <text x="540" y="548" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="58" fill="#FFFFFF">Try Your Own Name!</text>
    {deva_path("अन्ना  ·  डेविड  ·  माया", 540, 700, 68, "#FDE68A", "center")}
    <text x="540" y="838" text-anchor="middle" font-family="Inter" font-weight="500" font-size="32" fill="#E2E8F0">Instant Devanagari spelling + letter breakdown</text>
    <text x="540" y="892" text-anchor="middle" font-family="Inter" font-weight="500" font-size="32" fill="#E2E8F0">right in your browser — no sign-up, no email.</text>
    <rect x="134" y="1020" width="812" height="180" rx="34" fill="url(#scta_s2c)"/>
    <text x="540" y="1098" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="36" fill="#FFFFFF">ekguru.shop/name-in-hindi/</text>
    <text x="540" y="1156" text-anchor="middle" font-family="Inter" font-weight="600" font-size="25" fill="#FFFBEB">Comment your name below &amp; check link in bio!</text>
    {deva_path("एक भाषा, एक नई दुनिया।", 540, 1330, 42, "#FDE68A", "center")}
    """
    slides.append((short_shell_svg("TRY YOURS FREE", 1.0, cta, "s2c"), 4.5))
    return slides


def make_short03_slides() -> list[tuple[str, float]]:
    """Script 3: 3 Phrases for the Auto Ride in India — 25.0s total."""
    slides: list[tuple[str, float]] = []
    hook = f"""
    <rect x="84" y="420" width="912" height="980" rx="40" fill="#FFFFFF" fill-opacity="0.06" stroke="#FBBF24" stroke-opacity="0.45" stroke-width="2.5"/>
    <text x="540" y="560" text-anchor="middle" font-family="Inter" font-weight="700" font-size="26" fill="#FBBF24" letter-spacing="2">EVERYDAY INDIA SURVIVAL HINDI</text>
    <text x="540" y="676" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="60" fill="#FFFFFF">3 Hindi Phrases for</text>
    <text x="540" y="758" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="60" fill="#FDE68A">Every Auto Ride</text>
    {deva_path("ऑटो रिक्शा के ३ ज़रूरी वाक्य", 540, 926, 58, "#38BDF8", "center")}
    <text x="540" y="1068" text-anchor="middle" font-family="Inter" font-weight="500" font-size="31" fill="#E2E8F0">Polite, natural Hindi you’ll use on day one.</text>
    <rect x="210" y="1168" width="660" height="98" rx="49" fill="url(#scta_s3h)"/>
    <text x="540" y="1230" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="33" fill="#FFFFFF">Save this before your ride →</text>
    """
    slides.append((short_shell_svg("TRAVEL HINDI · 3 PHRASES", 0.12, hook, "s3h"), 3.5))

    phrases = [
        ("1", "कितने पैसे?", "Kitne paise?", "How much is the fare?", "Ask politely before hopping in"),
        ("2", "मीटर से चलिए।", "Meter se chaliye.", "Please go by the meter.", "‘Chaliye’ uses the respectful -iye form"),
        ("3", "यहाँ रोक दीजिए।", "Yahan rok dijiye.", "Please stop right here.", "‘Rok dijiye’ = polite request to pull over"),
    ]
    for idx, (num, deva, rom, eng, tip) in enumerate(phrases):
        uid = f"s3p{idx+1}"
        prog = (idx + 2) / 5.0
        body = f"""
        <rect x="84" y="380" width="912" height="1060" rx="42" fill="#FFFFFF" fill-opacity="0.07" stroke="#38BDF8" stroke-opacity="0.45" stroke-width="2.5"/>
        <text x="540" y="486" text-anchor="middle" font-family="Inter" font-weight="700" font-size="26" fill="#FBBF24" letter-spacing="2">PHRASE {num} OF 3</text>

        <rect x="134" y="544" width="812" height="240" rx="30" fill="#0F172A" stroke="#FBBF24" stroke-opacity="0.45" stroke-width="2"/>
        {deva_path(deva, 540, 696, 86, "#FFFFFF", "center")}

        <text x="540" y="904" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="56" fill="#FDE68A">“{esc(rom)}”</text>
        <text x="540" y="1016" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="700" font-size="44" fill="#38BDF8">{esc(eng)}</text>

        <rect x="144" y="1116" width="792" height="128" rx="24" fill="#FFFFFF" fill-opacity="0.06"/>
        <text x="540" y="1190" text-anchor="middle" font-family="Inter" font-weight="500" font-size="27" fill="#E2E8F0">{esc(tip)}</text>

        <text x="540" y="1358" text-anchor="middle" font-family="Inter" font-weight="600" font-size="26" fill="#94A3B8">ekguru.shop/learn/hindi/</text>
        """
        slides.append((short_shell_svg(f"AUTO PHRASE {num} / 3", prog, body, uid), 5.8))

    cta = f"""
    <rect x="84" y="400" width="912" height="1040" rx="42" fill="#FFFFFF" fill-opacity="0.07" stroke="#34D399" stroke-opacity="0.55" stroke-width="2.5"/>
    <text x="540" y="520" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="52" fill="#34D399">Quick Recap</text>
    {deva_path("१. कितने पैसे?", 540, 640, 48, "#FFFFFF", "center")}
    {deva_path("२. मीटर से चलिए।", 540, 732, 48, "#FDE68A", "center")}
    {deva_path("३. यहाँ रोक दीजिए।", 540, 824, 48, "#38BDF8", "center")}
    <text x="540" y="948" text-anchor="middle" font-family="Inter" font-weight="500" font-size="30" fill="#E2E8F0">Learn Hindi + Marathi, Tamil, Telugu, Gujarati,</text>
    <text x="540" y="996" text-anchor="middle" font-family="Inter" font-weight="500" font-size="30" fill="#E2E8F0">Bengali, Punjabi &amp; Urdu — free on EkGuru.</text>
    <rect x="134" y="1084" width="812" height="172" rx="34" fill="url(#scta_s3c)"/>
    <text x="540" y="1158" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="36" fill="#FFFFFF">ekguru.shop/learn/hindi/</text>
    <text x="540" y="1212" text-anchor="middle" font-family="Inter" font-weight="600" font-size="25" fill="#FFFBEB">Free step-by-step course · No account needed</text>
    {deva_path("एक भाषा, एक नई दुनिया।", 540, 1356, 42, "#FDE68A", "center")}
    """
    slides.append((short_shell_svg("FREE COURSE IN BIO", 1.0, cta, "s3c"), 4.1))
    return slides


def encode_short_from_slides(
    slides: list[tuple[str, float]],
    mp4_out: Path,
    cover_png_out: Path,
    audio_offset_s: float = 0.0,
) -> None:
    SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    total_dur = sum(d for _, d in slides)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        jobs = []
        png_paths = []
        for idx, (svg, _) in enumerate(slides):
            assert_no_unshaped_devanagari(svg, f"{mp4_out.name}[{idx}]")
            p = tmp_dir / f"slide_{idx:02d}.png"
            jobs.append({"svg": svg, "png_path": str(p)})
            png_paths.append(p)
        render_svgs_with_resvg(jobs)

        # Save slide 1 (first content card) or hook card as cover PNG
        with Image.open(png_paths[0]) as im:
            im.save(cover_png_out, format="PNG", optimize=True)

        # Build ffmpeg concat file (repeat last path per ffmpeg concat demuxer quirk)
        concat_txt = tmp_dir / "slides.txt"
        lines = []
        for p, (_, dur) in zip(png_paths, slides):
            lines.append(f"file '{p.as_posix()}'")
            lines.append(f"duration {dur:.3f}")
        lines.append(f"file '{png_paths[-1].as_posix()}'")
        concat_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")

        fade_out_start = max(0.5, total_dur - 1.8)
        cmd = [
            FFMPEG,
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_txt),
            "-ss", f"{audio_offset_s:.2f}",
            "-t", f"{total_dur:.3f}",
            "-i", str(SCORE_FLAC),
            "-vf", "fps=30,format=yuv420p",
            "-af", f"volume=0.55,afade=t=in:st=0:d=0.8,afade=t=out:st={fade_out_start:.2f}:d=1.6",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            "-movflags", "+faststart",
            str(mp4_out),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"encoded {mp4_out.relative_to(ROOT)} ({mp4_out.stat().st_size / 1024:.1f} KB, {total_dur:.1f}s)")


def main() -> None:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTREACH_DIR.mkdir(parents=True, exist_ok=True)
    SHORTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Post 3 Slides 2, 3, 4 + Class Handout SVG/PNG
    s2_svg = build_post03_slide02_svg()
    s3_svg = build_post03_slide03_svg()
    s4_svg = build_post03_slide04_svg()
    handout_svg = build_class_handout_svg()

    s2_base = POSTS_DIR / "post_03_slide_02_vowel_length_1080x1350"
    s3_base = POSTS_DIR / "post_03_slide_03_sound_grid_1080x1350"
    s4_base = POSTS_DIR / "post_03_slide_04_two_week_plan_1080x1350"
    ho_base = OUTREACH_DIR / "ekguru_hindi_class_home_practice_sheet_A4"

    s2_base.with_suffix(".svg").write_text(s2_svg, encoding="utf-8")
    s3_base.with_suffix(".svg").write_text(s3_svg, encoding="utf-8")
    s4_base.with_suffix(".svg").write_text(s4_svg, encoding="utf-8")
    ho_base.with_suffix(".svg").write_text(handout_svg, encoding="utf-8")

    png_targets = [
        {"svg": s2_svg, "png_path": str(s2_base.with_suffix(".png"))},
        {"svg": s3_svg, "png_path": str(s3_base.with_suffix(".png"))},
        {"svg": s4_svg, "png_path": str(s4_base.with_suffix(".png"))},
        {"svg": handout_svg, "png_path": str(ho_base.with_suffix(".png"))},
    ]
    for job in png_targets:
        assert_no_unshaped_devanagari(job["svg"], job["png_path"])
    render_svgs_with_resvg(png_targets)
    for job in png_targets:
        with Image.open(job["png_path"]) as im:
            im.save(job["png_path"], format="PNG", optimize=True)

    # 2. Three 9:16 MP4 Shorts/Reels
    encode_short_from_slides(
        make_short01_slides(),
        SHORTS_DIR / "short_01_count_1_to_10_hindi_9x16.mp4",
        SHORTS_DIR / "short_01_cover_1080x1920.png",
        audio_offset_s=0.0,
    )
    encode_short_from_slides(
        make_short02_slides(),
        SHORTS_DIR / "short_02_your_name_in_hindi_9x16.mp4",
        SHORTS_DIR / "short_02_cover_1080x1920.png",
        audio_offset_s=12.0,
    )
    encode_short_from_slides(
        make_short03_slides(),
        SHORTS_DIR / "short_03_auto_ride_3_phrases_9x16.mp4",
        SHORTS_DIR / "short_03_cover_1080x1920.png",
        audio_offset_s=24.0,
    )


if __name__ == "__main__":
    main()
