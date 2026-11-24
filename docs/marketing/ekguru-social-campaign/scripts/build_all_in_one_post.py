#!/usr/bin/env python3
"""
Builds the photographic base canvas and precision HarfBuzz Devanagari paths
for the EkGuru Flagship All-in-One Single-Post Masterpiece (1080 x 1350 px, 4:5),
combining all campaign worlds (1-on-1 tutor video call, Jaipur heritage vista,
authentic Indian cultural connection, and language study details) + bilingual
copy, 3 value pillars, official EkGuru logo, and ekguru.shop CTA onto ONE post.
"""
import json
import os
import re
import numpy as np
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = os.path.abspath("docs/marketing/ekguru-social-campaign")
PLATES = os.path.join(ROOT, "01_photographic_plates")
EDITABLE = os.path.join(ROOT, "02_editable_designs")
FONTS_DIR = os.path.abspath("docs/marketing/ekguru-brand-ad/05_brand_graphics/fonts")

MIDNIGHT = (11, 14, 23)


def grade_photo(im, warmth=1.02, contrast=1.04, color=0.96, brightness=1.0):
    im = im.convert("RGB")
    if color != 1.0:
        im = ImageEnhance.Color(im).enhance(color)
    if contrast != 1.0:
        im = ImageEnhance.Contrast(im).enhance(contrast)
    if brightness != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brightness)
    if warmth != 1.0:
        arr = np.asarray(im, dtype=np.float32)
        arr[..., 0] = np.clip(arr[..., 0] * warmth, 0, 255)
        arr[..., 2] = np.clip(arr[..., 2] * (2.0 - warmth), 0, 255)
        im = Image.fromarray(arr.astype(np.uint8), "RGB")
    return im


def fit_cover(im, target_w, target_h, anchor_x=0.5, anchor_y=0.5):
    w, h = im.size
    scale = max(target_w / w, target_h / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - target_w, int(round((nw - target_w) * anchor_x))))
    top = max(0, min(nh - target_h, int(round((nh - target_h) * anchor_y))))
    return resized.crop((left, top, left + target_w, top + target_h))


def add_bottom_pill_scrim(im, height_px=54, strength=0.68):
    """Subtle bottom corner darkening so micro-caption badges read effortlessly."""
    arr = np.asarray(im, dtype=np.float32)
    h, w, _ = arr.shape
    yy = np.arange(h, dtype=np.float32)[:, None, None]
    t = np.clip((yy - (h - height_px)) / float(height_px), 0.0, 1.0)
    alpha = (t ** 1.4) * strength
    dark = np.array(MIDNIGHT, dtype=np.float32)[None, None, :]
    out = np.clip(arr * (1.0 - alpha) + dark * alpha, 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGB")


def paste_rounded(canvas, photo, x, y, radius=10):
    w, h = photo.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    shadow = Image.new("RGBA", (w + 36, h + 36), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((18, 22, 18 + w - 1, 22 + h - 1), radius=radius, fill=(0, 0, 0, 135))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    rgba = canvas.convert("RGBA")
    rgba.alpha_composite(shadow, (x - 18, y - 18))
    canvas = rgba.convert("RGB")
    canvas.paste(photo, (x, y), mask)
    return canvas


def build_base_canvas():
    w, h = 1080, 1350
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # Subtle ambient gold-navy studio glow behind the grid and bottom CTA
    d1 = np.sqrt(((xx - 540.0) / 680.0) ** 2 + ((yy - 380.0) / 520.0) ** 2)
    f1 = np.clip(1.0 - d1, 0.0, 1.0) ** 2.0

    base = np.zeros((h, w, 3), dtype=np.float32)
    base[..., 0] = MIDNIGHT[0] + f1 * 24.0
    base[..., 1] = MIDNIGHT[1] + f1 * 21.0
    base[..., 2] = MIDNIGHT[2] + f1 * 18.0

    rng = np.random.default_rng(77)
    base = np.clip(base + rng.normal(0.0, 1.0, (h, w, 1)), 0, 255).astype(np.uint8)
    canvas = Image.fromarray(base, "RGB")

    # 4-Panel Architectural Story Grid (x=64..1016 -> 952px wide, y=116..644 -> 528px tall, 14px gutters)
    # 1. Top-Left Main Cinema Stage (608 x 334): Live 1-on-1 Tutor Video Call
    p_call = fit_cover(
        grade_photo(Image.open(os.path.join(PLATES, "slide_03_tutor_videocall_4x5.jpg")), warmth=1.03, contrast=1.04, color=0.96),
        608, 334, 0.48, 0.44
    )
    p_call = add_bottom_pill_scrim(p_call, 56, 0.72)

    # 2. Right Tall Heritage Vista (330 x 528): Golden-hour Jaipur traveler & palaces
    p_jaipur = fit_cover(
        grade_photo(Image.open(os.path.join(PLATES, "slide_01_hook_jaipur_4x5.jpg")), warmth=1.03, contrast=1.05, color=0.97),
        330, 528, 0.46, 0.42
    )
    p_jaipur = add_bottom_pill_scrim(p_jaipur, 58, 0.75)

    # 3. Bottom-Left Frame A (297 x 180): Authentic Jaipur Courtyard Culture & People
    p_culture = fit_cover(
        grade_photo(Image.open(os.path.join(PLATES, "slide_02_culture_jaipur_4x5.jpg")), warmth=1.02, contrast=1.04, color=0.96),
        297, 180, 0.50, 0.48
    )
    p_culture = add_bottom_pill_scrim(p_culture, 48, 0.74)

    # 4. Bottom-Center Frame B (297 x 180): Language Notebook, Pen, Masala Chai & Brass Lotus
    p_study = fit_cover(
        grade_photo(Image.open(os.path.join(PLATES, "slide_04c_notebook_details.jpg")), warmth=1.02, contrast=1.05, color=0.96),
        297, 180, 0.52, 0.50
    )
    p_study = add_bottom_pill_scrim(p_study, 48, 0.74)

    canvas = paste_rounded(canvas, p_call, 64, 116, radius=10)
    canvas = paste_rounded(canvas, p_jaipur, 686, 116, radius=10)
    canvas = paste_rounded(canvas, p_culture, 64, 464, radius=10)
    canvas = paste_rounded(canvas, p_study, 375, 464, radius=10)

    os.makedirs("/tmp/ekguru_social_bases", exist_ok=True)
    canvas.save("/tmp/ekguru_social_bases/base_all_in_one.png")
    canvas.save(os.path.join(EDITABLE, "base_all_in_one.jpg"), quality=96, subsampling=0, optimize=True)


# Shape Hindi lines for the All-in-One Post
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
        hb.shape(self.font, buf, {"kern": True, "liga": True})
        return buf.glyph_infos, buf.glyph_positions


deva_s = FontShaper(os.path.join(FONTS_DIR, "NotoSansDevanagari-Complete-500.ttf"))
latn_s = FontShaper(os.path.join(FONTS_DIR, "inter-latin-500-normal.ttf"))


def shape_line(text, font_size, x, baseline_y, align="left"):
    parts = re.compile(r"([A-Za-z]+)").split(text)
    runs = [("Latn" if re.fullmatch(r"[A-Za-z]+", p) else "Deva", p) for p in parts if p]
    segs = []
    total_adv = 0.0
    for sc, sub in runs:
        sh = latn_s if sc == "Latn" else deva_s
        infos, poss = sh.shape_run(sub, sc, "en" if sc == "Latn" else "hi")
        scale = font_size / sh.upem
        glyphs = []
        adv = 0.0
        for inf, pos in zip(infos, poss):
            gn = sh.tt.getGlyphOrder()[inf.codepoint]
            glyphs.append((sh.glyph_set, gn, adv + pos.x_offset * scale, pos.y_offset * scale, scale))
            adv += pos.x_advance * scale
        if sc == "Deva" and sub.endswith("। "):
            adv += font_size * 0.16
        segs.append((glyphs, total_adv))
        total_adv += adv

    sx = x - total_adv / 2.0 if align == "center" else (x - total_adv if align == "right" else x)
    cmds = []
    for glyphs, off_x in segs:
        for gset, gn, rx, ry, s in glyphs:
            spen = SVGPathPen(gset)
            tpen = TransformPen(spen, (s, 0.0, 0.0, -s, sx + off_x + rx, baseline_y - ry))
            gset[gn].draw(tpen)
            c = spen.getCommands()
            if c:
                cmds.append(c)
    return {"text": text, "width": round(total_adv, 2), "path": " ".join(cmds)}


if __name__ == "__main__":
    build_base_canvas()
    shaped = {
        "aio_tagline_hi": shape_line("एक भाषा, एक नई दुनिया।", 27.0, 1016.0, 742.0, "right"),
        "aio_sub_hi": shape_line(
            "दुनिया भर के learners को भारतीय भाषा के tutors से जोड़ने का मंच।",
            23.5, 64.0, 886.0, "left"
        ),
        "aio_p1_hi": shape_line("अपनी पसंद की भाषा खोजिए", 16.5, 88.0, 1046.0, "left"),
        "aio_p2_hi": shape_line("भारतीय Tutors से जुड़िए", 16.5, 411.0, 1046.0, "left"),
        "aio_p3_hi": shape_line("संस्कृति और लोगों से जुड़िए", 16.5, 734.0, 1046.0, "left"),
    }
    out_p = os.path.join(EDITABLE, "hindi_all_in_one_paths.json")
    with open(out_p, "w", encoding="utf-8") as f:
        json.dump(shaped, f, ensure_ascii=False, indent=2)
    for k, v in shaped.items():
        print(f"{k:16s} | width={v['width']:6.1f}px | {v['text']}")
