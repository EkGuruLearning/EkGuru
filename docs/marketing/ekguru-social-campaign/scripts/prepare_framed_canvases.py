#!/usr/bin/env python3
"""
Prepares pixel-exact photographic base canvases (1080x1350 for Instagram Carousel
Slides 1-5, and 1200x675 for the X/Twitter Landscape Post) with unified warm-ivory
and midnight-navy editorial color grading, rounded gallery masking, and smooth
negative-space vignettes ready for crisp vector typography & official logo compositing.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = os.path.abspath("docs/marketing/ekguru-social-campaign")
PLATES = os.path.join(ROOT, "01_photographic_plates")
OUT = os.path.join(ROOT, "02_editable_designs")
os.makedirs(OUT, exist_ok=True)

MIDNIGHT = (11, 14, 23)       # #0B0E17
ELEVATED_NAVY = (16, 21, 34)  # #101522


def save_base(im, stem):
    # Save lossless PNG to /tmp for zero-generation-loss PNG rendering, and 4:4:4 Q96 JPG in 02_editable_designs for lightweight editable SVGs
    os.makedirs("/tmp/ekguru_social_bases", exist_ok=True)
    im.save(f"/tmp/ekguru_social_bases/{stem}.png")
    im.save(os.path.join(OUT, f"{stem}.jpg"), quality=96, subsampling=0, optimize=True)


def grade_photo(im, warmth=1.03, contrast=1.04, color=0.96, brightness=1.0):
    """Subtle Condé Nast editorial color harmony across all plates."""
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
    left = int(round((nw - target_w) * anchor_x))
    top = int(round((nh - target_h) * anchor_y))
    left = max(0, min(nw - target_w, left))
    top = max(0, min(nh - target_h, top))
    return resized.crop((left, top, left + target_w, top + target_h))


def make_midnight_canvas(w, h, glow_center=(0.5, 0.42), glow_radius=0.65, glow_strength=0.14):
    """Deep midnight-navy architectural canvas with subtle warm-charcoal ambient depth."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w * glow_center[0], h * glow_center[1]
    r = max(w, h) * glow_radius
    dist = np.sqrt(((xx - cx) / r) ** 2 + ((yy - cy) / r) ** 2)
    falloff = np.clip(1.0 - dist, 0.0, 1.0) ** 2.0

    base = np.zeros((h, w, 3), dtype=np.float32)
    base[..., 0] = MIDNIGHT[0] + falloff * (34 * glow_strength / 0.14)
    base[..., 1] = MIDNIGHT[1] + falloff * (28 * glow_strength / 0.14)
    base[..., 2] = MIDNIGHT[2] + falloff * (22 * glow_strength / 0.14)

    # Ultra-subtle film grain (+/- 1.2 luma) to prevent 8-bit gradient banding
    rng = np.random.default_rng(42)
    noise = rng.normal(0.0, 1.1, (h, w, 1)).astype(np.float32)
    base = np.clip(base + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(base, "RGB")


def paste_rounded(canvas, photo, x, y, radius=12):
    w, h = photo.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    # Soft drop shadow on midnight canvas
    shadow = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle((20, 24, 20 + w - 1, 24 + h - 1), radius=radius, fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.alpha_composite(shadow, (x - 20, y - 20))
    canvas = canvas_rgba.convert("RGB")
    canvas.paste(photo, (x, y), mask)
    return canvas


def build_slide_01():
    # Full-bleed golden-hour Jaipur hook
    raw = Image.open(os.path.join(PLATES, "slide_01_hook_jaipur_4x5.jpg"))
    photo = fit_cover(grade_photo(raw, warmth=1.03, contrast=1.05, color=0.97), 1080, 1350, 0.5, 0.35)
    arr = np.asarray(photo, dtype=np.float32)
    h, w, _ = arr.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    # Top header protection (y=0..175) so metadata over bright golden sky has >7:1 contrast
    top_alpha = (np.clip(1.0 - yy / 175.0, 0.0, 1.0) ** 1.45) * 0.78
    # Bottom smooth editorial gradient (y=650..1350) + lower-left diagonal shadow behind headline
    bot_t = np.clip((yy - 650.0) / (1350.0 - 650.0), 0.0, 1.0)
    bot_alpha = np.clip(bot_t ** 1.28 * 1.04, 0.0, 0.97)

    # Soft localized shadow behind left-aligned headline ("A LANGUAGE CAN...") while keeping hand & Jaipur glowing
    hl_x = np.clip(1.0 - xx / 760.0, 0.0, 1.0) ** 1.35
    hl_y = np.clip((yy - 720.0) / 260.0, 0.0, 1.0)
    hl_guard = hl_x * hl_y * 0.62

    alpha = np.maximum(top_alpha, np.maximum(bot_alpha, hl_guard))[..., None]
    dark = np.array(MIDNIGHT, dtype=np.float32)[None, None, :]
    out = np.clip(arr * (1.0 - alpha) + dark * alpha, 0, 255).astype(np.uint8)
    save_base(Image.fromarray(out, "RGB"), "base_slide_01")


def build_slide_02():
    # Framed Jaipur courtyard cultural connection
    canvas = make_midnight_canvas(1080, 1350, glow_center=(0.5, 0.36), glow_strength=0.13)
    raw = Image.open(os.path.join(PLATES, "slide_02_culture_jaipur_4x5.jpg"))
    photo = fit_cover(grade_photo(raw, warmth=1.02, contrast=1.04, color=0.96), 936, 672, 0.5, 0.52)
    canvas = paste_rounded(canvas, photo, 72, 134, radius=10)
    save_base(canvas, "base_slide_02")


def build_slide_03():
    # Centerpiece wide cinema frame showing BOTH learner & Indian tutor on laptop call
    canvas = make_midnight_canvas(1080, 1350, glow_center=(0.5, 0.45), glow_strength=0.13)
    raw = Image.open(os.path.join(PLATES, "slide_03_tutor_videocall_4x5.jpg"))
    photo = fit_cover(grade_photo(raw, warmth=1.03, contrast=1.04, color=0.96), 936, 576, 0.48, 0.45)
    canvas = paste_rounded(canvas, photo, 72, 288, radius=10)
    save_base(canvas, "base_slide_03")


def build_slide_04():
    # Asymmetric split editorial triptych (16px midnight-charcoal gutters)
    canvas = make_midnight_canvas(1080, 1350, glow_center=(0.5, 0.38), glow_strength=0.13)
    p_a = fit_cover(
        grade_photo(Image.open(os.path.join(PLATES, "slide_04a_learner_practice.jpg")), warmth=1.03, contrast=1.04, color=0.96),
        492, 660, 0.5, 0.35
    )
    p_b = fit_cover(
        grade_photo(Image.open(os.path.join(PLATES, "slide_04b_indian_tutor.jpg")), warmth=1.01, contrast=1.04, color=0.95),
        428, 322, 0.58, 0.35
    )
    p_c = fit_cover(
        grade_photo(Image.open(os.path.join(PLATES, "slide_04c_notebook_details.jpg")), warmth=1.02, contrast=1.05, color=0.96),
        428, 322, 0.52, 0.50
    )
    canvas = paste_rounded(canvas, p_a, 72, 134, radius=10)
    canvas = paste_rounded(canvas, p_b, 580, 134, radius=10)
    canvas = paste_rounded(canvas, p_c, 580, 472, radius=10)
    save_base(canvas, "base_slide_04")


def build_slide_05():
    # Luxury deep charcoal & muted-gold ceremonial finale
    raw = Image.open(os.path.join(PLATES, "slide_05_charcoal_gold_bg.jpg"))
    photo = fit_cover(grade_photo(raw, warmth=1.02, contrast=1.06, color=0.92, brightness=0.92), 1080, 1350, 0.5, 0.5)
    arr = np.asarray(photo, dtype=np.float32)
    h, w, _ = arr.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # Keep central text area & top/bottom chrome calm velvet charcoal while preserving side/corner golden bokeh
    dist = np.sqrt(((xx - 540.0) / 420.0) ** 2 + ((yy - 660.0) / 470.0) ** 2)
    center_calm = np.clip(1.0 - dist, 0.0, 1.0) ** 1.5 * 0.48
    top_bar_calm = np.clip(1.0 - yy / 125.0, 0.0, 1.0) ** 1.4 * 0.72
    bot_bar_calm = np.clip((yy - 1230.0) / 120.0, 0.0, 1.0) ** 1.4 * 0.72
    calm = np.maximum(center_calm, np.maximum(top_bar_calm, bot_bar_calm))
    dark = np.array(MIDNIGHT, dtype=np.float32)[None, None, :]
    out = np.clip(arr * (1.0 - calm[..., None]) + dark * calm[..., None], 0, 255).astype(np.uint8)
    save_base(Image.fromarray(out, "RGB"), "base_slide_05")


def build_x_landscape():
    # 1200x675 bespoke 16:9 composition: clean negative space on left (x=0..455),
    # learner in sunlit study in center (x=465..780), Jaipur & Hawa Mahal through open window on right (x=785..1200)!
    canvas = make_midnight_canvas(1200, 675, glow_center=(0.22, 0.5), glow_strength=0.05)
    raw = Image.open(os.path.join(PLATES, "x_post_worlds_landscape_16x9.jpg"))
    graded = grade_photo(raw, warmth=1.02, contrast=1.04, color=0.96)

    # Shift right by +152px so Hawa Mahal stays 100% intact inside x=835..1195 while left negative space clears the mug
    shift_x = 152
    scaled = graded.resize((1209, 675), Image.Resampling.LANCZOS)
    right_part = scaled.crop((0, 0, 1200 - shift_x, 675))  # width = 1048px, placed at x=152..1200

    c_arr = np.asarray(canvas, dtype=np.float32)
    p_arr = np.asarray(right_part, dtype=np.float32)

    px = np.arange(1200 - shift_x, dtype=np.float32)[None, :, None]
    blend = np.clip((px - 50.0) / 285.0, 0.0, 1.0)
    blend = blend * blend * (3.0 - 2.0 * blend)

    c_arr[:, shift_x:1200, :] = c_arr[:, shift_x:1200, :] * (1.0 - blend) + p_arr * blend

    # Extra clean negative-space guard on left & lower-left behind tagline + website pill
    yy, xx = np.mgrid[0:675, 0:1200].astype(np.float32)
    left_guard = np.clip(1.0 - xx / 480.0, 0.0, 1.0) ** 1.35 * 0.62
    bot_left_guard = (np.clip(1.0 - xx / 495.0, 0.0, 1.0) ** 1.2) * (np.clip((yy - 460.0) / 180.0, 0.0, 1.0)) * 0.85
    guard = np.maximum(left_guard, bot_left_guard)
    dark = np.array(MIDNIGHT, dtype=np.float32)[None, None, :]
    c_arr = np.clip(c_arr * (1.0 - guard[..., None]) + dark * guard[..., None], 0, 255)

    save_base(Image.fromarray(c_arr.astype(np.uint8), "RGB"), "base_x_landscape")


if __name__ == "__main__":
    build_slide_01()
    build_slide_02()
    build_slide_03()
    build_slide_04()
    build_slide_05()
    build_x_landscape()
    print("All 6 photographic base canvases built successfully.")
