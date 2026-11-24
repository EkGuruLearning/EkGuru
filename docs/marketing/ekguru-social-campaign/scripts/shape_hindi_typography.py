#!/usr/bin/env python3
"""
Precision OpenType HarfBuzz shaper for mixed Devanagari + Latin editorial copy.
Splits runs by script so Devanagari conjuncts/matras/repha/nukta shape with
`script='Deva'` (Noto Sans Devanagari) and inline English words (`learners`,
`tutors`, `Tutors`) shape with `script='Latn'` (Inter Medium) with exact metrics.
"""
import json
import os
import re
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS_DIR = os.path.abspath("docs/marketing/ekguru-brand-ad/05_brand_graphics/fonts")
DEVA_FONT_PATH = os.path.join(FONTS_DIR, "NotoSansDevanagari-Complete-500.ttf")
LATN_FONT_PATH = os.path.join(FONTS_DIR, "inter-latin-500-normal.ttf")

OUT_DIR = os.path.abspath("docs/marketing/ekguru-social-campaign/02_editable_designs")
os.makedirs(OUT_DIR, exist_ok=True)


class FontShaper:
    def __init__(self, path):
        with open(path, "rb") as f:
            self.data = f.read()
        self.face = hb.Face(self.data)
        self.font = hb.Font(self.face)
        self.upem = self.face.upem
        self.tt = TTFont(path)
        self.glyph_set = self.tt.getGlyphSet()

    def shape_run(self, text, script_tag, lang_tag="hi"):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.direction = "ltr"
        buf.script = script_tag
        buf.language = lang_tag
        features = {"kern": True, "liga": True}
        hb.shape(self.font, buf, features)
        return buf.glyph_infos, buf.glyph_positions


deva_shaper = FontShaper(DEVA_FONT_PATH)
latn_shaper = FontShaper(LATN_FONT_PATH)


def split_script_runs(text):
    pattern = re.compile(r"([A-Za-z]+)")
    parts = pattern.split(text)
    runs = []
    for part in parts:
        if not part:
            continue
        if re.fullmatch(r"[A-Za-z]+", part):
            runs.append(("Latn", part))
        else:
            runs.append(("Deva", part))
    return runs


def shape_line_to_svg_path(text, font_size, x, baseline_y, align="left"):
    runs = split_script_runs(text)
    rendered_segments = []
    total_advance_px = 0.0

    for script_tag, substr in runs:
        shaper = latn_shaper if script_tag == "Latn" else deva_shaper
        lang = "en" if script_tag == "Latn" else "hi"
        infos, positions = shaper.shape_run(substr, script_tag, lang)
        scale = font_size / shaper.upem
        seg_glyphs = []
        seg_adv = 0.0
        for info, pos in zip(infos, positions):
            gname = shaper.tt.getGlyphOrder()[info.codepoint]
            seg_glyphs.append((shaper.glyph_set, gname, seg_adv + pos.x_offset * scale, pos.y_offset * scale, scale))
            seg_adv += pos.x_advance * scale
        # Add subtle optical breathing room after Devanagari danda+space before an inline Latin word
        if script_tag == "Deva" and substr.endswith("। "):
            seg_adv += font_size * 0.16
        rendered_segments.append((seg_glyphs, total_advance_px))
        total_advance_px += seg_adv

    if align == "center":
        start_x = x - total_advance_px / 2.0
    elif align == "right":
        start_x = x - total_advance_px
    else:
        start_x = x

    parts_cmds = []
    for seg_glyphs, seg_offset_x in rendered_segments:
        for gset, gname, rel_x, rel_y, s in seg_glyphs:
            gx = start_x + seg_offset_x + rel_x
            gy = baseline_y - rel_y
            spen = SVGPathPen(gset)
            tpen = TransformPen(spen, (s, 0.0, 0.0, -s, gx, gy))
            gset[gname].draw(tpen)
            cmd = spen.getCommands()
            if cmd:
                parts_cmds.append(cmd)

    return {
        "text": text,
        "width": round(total_advance_px, 2),
        "path": " ".join(parts_cmds),
    }


LINES_SPEC = {
    # Slide 1 (left-aligned at x=72)
    "s1_hi": ("एक भाषा... एक नई दुनिया।", 28.0, 72.0, 1200.0, "left"),

    # Slide 2 (left-aligned at x=72, 2 balanced lines)
    "s2_hi_1": ("सिर्फ भाषा नहीं, भारत की संस्कृति और लोगों से", 27.0, 72.0, 1118.0, "left"),
    "s2_hi_2": ("जुड़ने का एक नया अनुभव।", 27.0, 72.0, 1162.0, "left"),

    # Slide 3 (left-aligned at x=72, 2 balanced lines below centerpiece frame)
    "s3_hi_1": ("दुनिया भर के learners को भारतीय भाषा के", 27.0, 72.0, 1084.0, "left"),
    "s3_hi_2": ("tutors से जोड़ने का एक मंच।", 27.0, 72.0, 1128.0, "left"),

    # Slide 4 (left-aligned at x=72, 2 balanced lines)
    "s4_hi_1": ("अपनी पसंद की भाषा खोजिए। Tutors से जुड़िए।", 26.5, 72.0, 1124.0, "left"),
    "s4_hi_2": ("भारत को एक नए अंदाज़ में जानिए।", 26.5, 72.0, 1166.0, "left"),

    # Slide 5 (centered at x=540)
    "s5_hi": ("एक भाषा, एक नई दुनिया।", 31.0, 540.0, 764.0, "center"),

    # X Post 1200x675 (left-aligned at x=56)
    "x_hi": ("एक भाषा, एक नई दुनिया।", 23.5, 56.0, 472.0, "left"),
}

results = {}
for key, (txt, size, x, y, align) in LINES_SPEC.items():
    res = shape_line_to_svg_path(txt, size, x, y, align)
    results[key] = res
    print(f"{key:10s} | width={res['width']:6.1f}px | {txt}")

out_json = os.path.join(OUT_DIR, "hindi_shaped_paths.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Saved:", out_json)
