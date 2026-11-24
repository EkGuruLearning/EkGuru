#!/usr/bin/env python3
"""
Render the 9:16 Vertical (1080x1920, 30fps) Instagram Reels & YouTube Shorts suite:
1) 06_exports/ekguru_60s_instagram_reel_youtube_shorts_9x16.mp4 (Full 60.0s Bilingual Commercial)
2) 06_exports/ekguru_15s_reel_shorts_teaser_9x16.mp4            (15.0s High-Impact Reel/Shorts Teaser)
3) 06_exports/scene_07_brand_reveal_master_9x16.mp4             (12.0s Standalone Vertical Brand Ending)
"""
import os
import time
import subprocess
import numpy as np
from PIL import Image
from scipy.io import wavfile
import imageio_ffmpeg

ROOT = "docs/marketing/ekguru-brand-ad"
REF_V_DIR = os.path.join(ROOT, "02_reference_frames_9x16")
GFX_DIR = os.path.join(ROOT, "05_brand_graphics")
VO_DIR = os.path.join(ROOT, "03_voiceover")
MUS_DIR = os.path.join(ROOT, "04_music_and_sfx")
EXP_DIR = os.path.join(ROOT, "06_exports")

W, H = 1080, 1920
FPS = 30
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def load_graded_vertical(filename, overscale=1.15, warm_grade=True):
    img = Image.open(os.path.join(REF_V_DIR, filename)).convert("RGB")
    iw, ih = img.size
    target_ratio = W / H
    if iw / ih > target_ratio:
        nw = int(ih * target_ratio)
        x0 = (iw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / target_ratio)
        y0 = (ih - nh) // 2
        img = img.crop((0, y0, iw, y0 + nh))

    ow, oh = int(W * overscale), int(H * overscale)
    img = img.resize((ow, oh), Image.Resampling.LANCZOS)
    if not warm_grade:
        return img

    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr[..., 0] = np.clip(arr[..., 0] * 1.025 + 0.006, 0.0, 1.0)
    arr[..., 1] = np.clip(arr[..., 1] * 1.005 + 0.002, 0.0, 1.0)
    arr[..., 2] = np.clip(arr[..., 2] * 0.965 + 0.008, 0.0, 1.0)
    arr = np.clip(0.5 + (arr - 0.5) * 1.04, 0.0, 1.0)
    return Image.fromarray((arr * 255.0).astype(np.uint8), "RGB")


def camera_crop_pil(plate_img, zoom=1.0, pan_x=0.0, pan_y=0.0):
    ow, oh = plate_img.size
    crop_w = W / zoom
    crop_h = H / zoom
    max_dx = max(0.0, (ow - crop_w) * 0.5)
    max_dy = max(0.0, (oh - crop_h) * 0.5)
    cx = ow * 0.5 + pan_x * max_dx
    cy = oh * 0.5 + pan_y * max_dy
    x0 = max(0.0, cx - crop_w * 0.5)
    y0 = max(0.0, cy - crop_h * 0.5)
    x1 = min(float(ow), x0 + crop_w)
    y1 = min(float(oh), y0 + crop_h)
    return plate_img.resize((W, H), Image.Resampling.BICUBIC, box=(x0, y0, x1, y1))


def ease_in_out(u):
    u = max(0.0, min(1.0, float(u)))
    return 0.5 * (1.0 - np.cos(np.pi * u))


def smoothstep(t, t0, t1):
    u = max(0.0, min(1.0, (t - t0) / max(t1 - t0, 1e-5)))
    return u * u * (3.0 - 2.0 * u)


class FastVerticalScene7:
    def __init__(self):
        bg_raw = load_graded_vertical("scene_07_brand_reveal_bg_9x16.jpg", overscale=1.12, warm_grade=False)
        arr = np.asarray(bg_raw, dtype=np.float32) / 255.0
        oh, ow, _ = arr.shape
        yy, xx = np.mgrid[0:oh, 0:ow].astype(np.float32)
        rr = np.sqrt(((xx - ow * 0.5) / (ow * 0.58)) ** 2 + ((yy - oh * 0.48) / (oh * 0.52)) ** 2)
        vig = np.clip(1.0 - 0.35 * (rr**1.6), 0.40, 1.0)[..., None]
        arr = np.clip(arr * 0.74 * vig, 0.0, 1.0)
        self.bg_plate = Image.fromarray((arr * 255.0).astype(np.uint8), "RGB")

        # Prebuild two parallax RGBA bokeh sheets (fast single-crop C compositing per frame!)
        self.sheet_a = self._make_bokeh_sheet(seed=108, count=65, min_r=4, max_r=18, max_op=0.22)
        self.sheet_b = self._make_bokeh_sheet(seed=216, count=35, min_r=10, max_r=30, max_op=0.14)

        self.layers = {
            name: Image.open(os.path.join(GFX_DIR, f"layer_{name}_1080x1920.png")).convert("RGBA")
            for name in ["logo_and_title", "en_tagline", "hi_tagline", "url_pill"]
        }
        self.full_endcard = Image.open(os.path.join(GFX_DIR, "scene_07_endcard_overlay_1080x1920.png")).convert("RGBA")
        self.black = Image.new("RGB", (W, H), (0, 0, 0))

    @staticmethod
    def _make_bokeh_sheet(seed, count, min_r, max_r, max_op):
        sw, sh = W + 240, H + 480
        canvas = np.zeros((sh, sw, 4), dtype=np.float32)
        rng = np.random.default_rng(seed)
        for _ in range(count):
            cx = rng.uniform(30, sw - 30)
            cy = rng.uniform(30, sh - 30)
            rad = rng.uniform(min_r, max_r)
            op = rng.uniform(0.05, max_op)
            ri = int(rad * 2.2) + 2
            x0, x1 = max(0, int(cx) - ri), min(sw, int(cx) + ri)
            y0, y1 = max(0, int(cy) - ri), min(sh, int(cy) + ri)
            yy, xx = np.ogrid[y0:y1, x0:x1]
            d2 = ((xx - cx) ** 2 + (yy - cy) ** 2) / (rad**2)
            a = np.exp(-1.3 * d2) * op
            canvas[y0:y1, x0:x1, 0] = 255.0
            canvas[y0:y1, x0:x1, 1] = 214.0
            canvas[y0:y1, x0:x1, 2] = 122.0
            canvas[y0:y1, x0:x1, 3] = np.clip(canvas[y0:y1, x0:x1, 3] + a * 255.0, 0.0, 255.0)
        return Image.fromarray(canvas.astype(np.uint8), "RGBA")

    @staticmethod
    def _fade_rgba(img_rgba, op):
        if op >= 0.998:
            return img_rgba
        arr = np.asarray(img_rgba).copy()
        arr[..., 3] = (arr[..., 3].astype(np.float32) * op).astype(np.uint8)
        return Image.fromarray(arr, "RGBA")

    def render_frame(self, local_t, total_dur=12.0, fast_teaser_cues=False):
        u = local_t / total_dur
        base_rgb = camera_crop_pil(self.bg_plate, zoom=1.0 + 0.05 * u, pan_x=0.0, pan_y=-0.16 * u)
        rgba = base_rgb.convert("RGBA")

        # 2-layer parallax upward bokeh drift
        dx1 = int(60 + 45 * np.sin(local_t * 0.35))
        dy1 = int((local_t * 22.0) % 420)
        p1 = self.sheet_a.crop((dx1, dy1, dx1 + W, dy1 + H))

        dx2 = int(100 - 55 * np.cos(local_t * 0.28))
        dy2 = int((local_t * 34.0) % 420)
        p2 = self.sheet_b.crop((dx2, dy2, dx2 + W, dy2 + H))

        rgba.alpha_composite(p1)
        rgba.alpha_composite(p2)

        cues = (
            [
                ("logo_and_title", 0.15, 0.75),
                ("en_tagline", 0.65, 1.35),
                ("hi_tagline", 1.85, 2.55),
                ("url_pill", 2.90, 3.60),
            ]
            if fast_teaser_cues
            else [
                ("logo_and_title", 0.35, 1.45),
                ("en_tagline", 1.75, 2.85),
                ("hi_tagline", 5.10, 6.10),
                ("url_pill", 7.65, 8.65),
            ]
        )
        for name, t0, t1 in cues:
            op = smoothstep(local_t, t0, t1)
            if op <= 0.002:
                continue
            shift_y = int(round((1.0 - op) * 14.0))
            lyr = self._fade_rgba(self.layers[name], op)
            rgba.alpha_composite(lyr, dest=(0, shift_y))

        rgb = rgba.convert("RGB")
        fade_start = total_dur - 0.42
        if local_t > fade_start:
            fade = max(0.0, min(1.0, (total_dur - local_t) / 0.42))
            rgb = Image.blend(self.black, rgb, fade)
        return rgb


def build_15s_teaser_audio(out_flac):
    sr = 48000
    n = 15 * sr
    vo = np.zeros(n, dtype=np.float32)

    def rd(name):
        _, d = wavfile.read(os.path.join(VO_DIR, name))
        return (d[:, 0] if d.ndim > 1 else d).astype(np.float32) / 32768.0

    en1 = rd("en_scene_01.wav")[: int(2.25 * sr)]  # "Every language tells a story."
    en7 = rd("en_scene_07.wav")                     # "EkGuru. Learn Indian Languages. Connect with India."
    hi_tag = rd("hi_scene_07_tagline.wav")          # "एक भाषा, एक नई दुनिया।"
    cta = rd("en_scene_07_cta.wav")                 # "Your journey begins at ekguru.shop."

    for clip, st in [(en1, 0.30), (en7, 3.15), (hi_tag, 7.95), (cta, 10.50)]:
        fade = min(int(0.025 * sr), len(clip) // 4)
        c = clip.copy()
        c[:fade] *= np.linspace(0, 1, fade)
        c[-fade:] *= np.linspace(1, 0, fade)
        i0 = int(st * sr)
        i1 = min(n, i0 + len(c))
        vo[i0:i1] += c[: i1 - i0]

    tmp_sc = "/tmp/sc_60_tmp.wav"
    subprocess.run(
        [FFMPEG, "-y", "-i", os.path.join(MUS_DIR, "ekguru_cinematic_score_60s.flac"), "-ar", "48000", "-ac", "2", tmp_sc],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    _, score_full = wavfile.read(tmp_sc)
    sc_seg = score_full[45 * sr : 60 * sr].astype(np.float32) / 32768.0
    sc_seg[: int(0.35 * sr)] *= np.linspace(0, 1, int(0.35 * sr))[:, None]

    # Gentle sidechain ducking under VO
    win = int(0.35 * sr)
    kern = np.hanning(win).astype(np.float32)
    kern /= np.sum(kern)
    act = np.convolve(np.abs(vo), kern, mode="same")
    duck = (1.0 - 0.58 * np.clip(act / 0.045, 0.0, 1.0))[:, None]
    mix = vo[:, None] * 0.82 + sc_seg * (0.40 * duck)
    mx = np.max(np.abs(mix))
    if mx > 0.89:
        mix = 0.89 * np.tanh(mix / 0.89)

    tmp_out = "/tmp/teaser_15s.wav"
    wavfile.write(tmp_out, sr, (mix * 32767.0).astype(np.int16))
    subprocess.run([FFMPEG, "-y", "-i", tmp_out, "-compression_level", "8", out_flac],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    t0 = time.time()
    plates = {
        1: load_graded_vertical("scene_01_jaipur_sunrise_9x16.jpg", 1.15),
        2: load_graded_vertical("scene_02_learner_curiosity_9x16.jpg", 1.15),
        3: load_graded_vertical("scene_03_tutor_connection_9x16.jpg", 1.15),
        4: load_graded_vertical("scene_04_joy_of_learning_9x16.jpg", 1.15),
        5: load_graded_vertical("scene_05_indian_culture_9x16.jpg", 1.15),
        6: load_graded_vertical("scene_06_global_connection_9x16.jpg", 1.15),
    }
    s7 = FastVerticalScene7()
    black = Image.new("RGB", (W, H), (0, 0, 0))
    print(f"9:16 plates loaded in {time.time() - t0:.1f}s", flush=True)

    def scene_frame_v(sc, local_u):
        u = max(0.0, min(1.0, float(local_u)))
        e = ease_in_out(u)
        if sc == 1:
            return camera_crop_pil(plates[1], zoom=1.01 + 0.08 * u, pan_x=0.0, pan_y=0.28 - 0.56 * u)
        elif sc == 2:
            return camera_crop_pil(plates[2], zoom=1.00 + 0.09 * e, pan_x=-0.10 + 0.20 * e, pan_y=0.12 - 0.20 * e)
        elif sc == 3:
            return camera_crop_pil(plates[3], zoom=1.01 + 0.075 * e, pan_x=0.12 - 0.24 * e, pan_y=0.05 - 0.10 * e)
        elif sc == 4:
            return camera_crop_pil(plates[4], zoom=1.00 + 0.09 * e, pan_x=0.0, pan_y=0.08 - 0.16 * e)
        elif sc == 5:
            return camera_crop_pil(plates[5], zoom=1.01 + 0.08 * u, pan_x=-0.18 + 0.36 * u, pan_y=0.18 - 0.30 * u)
        elif sc == 6:
            return camera_crop_pil(plates[6], zoom=1.08 - 0.065 * e, pan_x=-0.15 + 0.30 * e, pan_y=0.0)
        raise ValueError(sc)

    audio_60 = os.path.join(MUS_DIR, "ekguru_master_audio_60s_bilingual.flac")
    out_60_v = os.path.join(EXP_DIR, "ekguru_60s_instagram_reel_youtube_shorts_9x16.mp4")
    out_s7_v = os.path.join(EXP_DIR, "scene_07_brand_reveal_master_9x16.mp4")

    # 1) Render 60.0s 9:16 Vertical Commercial + 12.0s Scene 7 Vertical Master
    p_60 = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-i", audio_60,
         "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out_60_v],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    p_s7 = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-ss", "48", "-t", "12", "-i", audio_60,
         "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out_s7_v],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    s7_first = s7.render_frame(0.0, total_dur=12.0, fast_teaser_cues=False)
    diss_half = 0.35

    for f_idx in range(60 * FPS):
        t = f_idx / FPS
        if t < 48.0:
            sc = min(6, int(t // 8.0) + 1)
            local_u = (t - (sc - 1) * 8.0) / 8.0
            fr = scene_frame_v(sc, local_u)
            if t < 0.50:
                fr = Image.blend(black, fr, t / 0.50)
            for bt, (sp, sn) in [(8.0, (1, 2)), (32.0, (4, 5))]:
                if abs(t - bt) < diss_half:
                    alpha = ease_in_out((t - (bt - diss_half)) / (2 * diss_half))
                    fp = scene_frame_v(sp, (t - (sp - 1) * 8.0) / 8.0)
                    fn = scene_frame_v(sn, (t - (sn - 1) * 8.0) / 8.0)
                    fr = Image.blend(fp, fn, alpha)
            if t >= 47.55:
                alpha = ease_in_out((t - 47.55) / 0.45)
                fr = Image.blend(fr, s7_first, alpha)
            p_60.stdin.write(fr.tobytes())
        else:
            fr_s7 = s7.render_frame(t - 48.0, total_dur=12.0, fast_teaser_cues=False)
            raw = fr_s7.tobytes()
            p_60.stdin.write(raw)
            p_s7.stdin.write(raw)

        if (f_idx + 1) % 300 == 0:
            print(f"  9:16 60s Reel: {f_idx + 1}/1800 frames ({time.time() - t0:.1f}s)", flush=True)

    p_60.stdin.close()
    p_s7.stdin.close()
    p_60.wait()
    p_s7.wait()
    print(f"Saved 60s 9:16 Reel/Shorts -> {out_60_v}", flush=True)

    # 2) Render 15.0s High-Impact 9:16 Reel / Shorts Teaser
    teaser_flac = os.path.join(MUS_DIR, "ekguru_teaser_audio_15s_bilingual.flac")
    build_15s_teaser_audio(teaser_flac)
    out_15_v = os.path.join(EXP_DIR, "ekguru_15s_reel_shorts_teaser_9x16.mp4")

    p_15 = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-i", teaser_flac,
         "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out_15_v],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    s7_t_first = s7.render_frame(0.0, total_dur=5.5, fast_teaser_cues=True)

    # 15s structure: S1 (0..3.0s) -> S3 (3.0..6.3s) -> S5 (6.3..9.5s) -> S7 Brand Reveal (9.5..15.0s)
    for f_idx in range(15 * FPS):
        t = f_idx / FPS
        if t < 3.0:
            fr = scene_frame_v(1, t / 3.0)
            if t < 0.35:
                fr = Image.blend(black, fr, t / 0.35)
        elif t < 6.3:
            fr = scene_frame_v(3, (t - 3.0) / 3.3)
        elif t < 9.5:
            fr = scene_frame_v(5, (t - 6.3) / 3.2)
            if t >= 9.15:
                alpha = ease_in_out((t - 9.15) / 0.35)
                fr = Image.blend(fr, s7_t_first, alpha)
        else:
            fr = s7.render_frame(t - 9.5, total_dur=5.5, fast_teaser_cues=True)
        p_15.stdin.write(fr.tobytes())

    p_15.stdin.close()
    p_15.wait()
    print(f"Saved 15s 9:16 Teaser -> {out_15_v} (Total wall time: {time.time() - t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
