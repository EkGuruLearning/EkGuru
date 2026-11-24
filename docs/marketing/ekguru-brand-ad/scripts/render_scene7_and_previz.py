#!/usr/bin/env python3
"""
Fast SIMD-C (Pillow sub-pixel BICUBIC box resize) renderer for:
1) Scene 7 Finished Brand Reveal (12.0s, 1920x1080, 30fps) + Clean Particle Background MP4
2) 60.0s Timed Director's Pre-Viz / Audio-Locked Animatic (1920x1080, 30fps)
"""
import os
import time
import subprocess
import numpy as np
from PIL import Image, ImageDraw
import imageio_ffmpeg

ROOT = "docs/marketing/ekguru-brand-ad"
REF_DIR = os.path.join(ROOT, "02_reference_frames")
GFX_DIR = os.path.join(ROOT, "05_brand_graphics")
MUS_DIR = os.path.join(ROOT, "04_music_and_sfx")
EXP_DIR = os.path.join(ROOT, "06_exports")

W, H = 1920, 1080
FPS = 30
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def load_graded_pil(filename, overscale=1.16, warm_grade=True):
    img = Image.open(os.path.join(REF_DIR, filename)).convert("RGB")
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

    # Apply warm golden commercial LUT once at load time
    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr[..., 0] = np.clip(arr[..., 0] * 1.025 + 0.006, 0.0, 1.0)
    arr[..., 1] = np.clip(arr[..., 1] * 1.005 + 0.002, 0.0, 1.0)
    arr[..., 2] = np.clip(arr[..., 2] * 0.965 + 0.008, 0.0, 1.0)
    arr = np.clip(0.5 + (arr - 0.5) * 1.04, 0.0, 1.0)
    return Image.fromarray((arr * 255.0).astype(np.uint8), "RGB")


def camera_crop_pil(plate_img, zoom=1.0, pan_x=0.0, pan_y=0.0):
    """Sub-pixel smooth float box resize in C (libimaging AVX2) — zero integer jitter!"""
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


class FastScene7:
    def __init__(self):
        bg_raw = load_graded_pil("scene_07_brand_reveal_bg_16x9.jpg", overscale=1.12, warm_grade=False)
        # Pre-darken edges cleanly once so central golden illumination & typography shine
        arr = np.asarray(bg_raw, dtype=np.float32) / 255.0
        oh, ow, _ = arr.shape
        yy, xx = np.mgrid[0:oh, 0:ow].astype(np.float32)
        rr = np.sqrt(((xx - ow * 0.5) / (ow * 0.55)) ** 2 + ((yy - oh * 0.46) / (oh * 0.55)) ** 2)
        vig = np.clip(1.0 - 0.35 * (rr**1.6), 0.42, 1.0)[..., None]
        arr = np.clip(arr * 0.76 * vig, 0.0, 1.0)
        self.bg_plate = Image.fromarray((arr * 255.0).astype(np.uint8), "RGB")

        # Prebuild soft bokeh sprite (64x64 RGBA) for fast C compositing
        sp_sz = 64
        sy, sx = np.mgrid[0:sp_sz, 0:sp_sz].astype(np.float32)
        d2 = ((sx - 31.5) ** 2 + (sy - 31.5) ** 2) / (15.0**2)
        alpha = np.clip(np.exp(-1.2 * d2) * 255.0, 0, 255).astype(np.uint8)
        sp_rgba = np.zeros((sp_sz, sp_sz, 4), dtype=np.uint8)
        sp_rgba[..., 0] = 255
        sp_rgba[..., 1] = 212
        sp_rgba[..., 2] = 118
        sp_rgba[..., 3] = alpha
        self.sprite_base = Image.fromarray(sp_rgba, "RGBA")

        rng = np.random.default_rng(108)
        self.num_p = 45
        self.px = rng.uniform(0.08 * W, 0.92 * W, self.num_p)
        self.py = rng.uniform(0.08 * H, 0.94 * H, self.num_p)
        self.vx = rng.uniform(-8.0, 8.0, self.num_p)
        self.vy = rng.uniform(-18.0, -6.0, self.num_p)
        self.psz = rng.integers(8, 38, self.num_p)
        self.pop = rng.uniform(0.08, 0.28, self.num_p)
        self.pph = rng.uniform(0, 2 * np.pi, self.num_p)

        self.layers = {
            name: Image.open(os.path.join(GFX_DIR, f"layer_{name}_1920x1080.png")).convert("RGBA")
            for name in ["logo_and_title", "en_tagline", "hi_tagline", "url_pill"]
        }
        self.black = Image.new("RGB", (W, H), (0, 0, 0))

    def render_pair(self, local_t):
        u = local_t / 12.0
        base_rgb = camera_crop_pil(self.bg_plate, zoom=1.0 + 0.05 * u, pan_x=0.0, pan_y=-0.18 * u)
        clean_rgba = base_rgb.convert("RGBA")

        # Paste floating bokeh sprites
        particle_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for i in range(self.num_p):
            cx = int((self.px[i] + self.vx[i] * local_t + 10.0 * np.sin(local_t * 0.55 + self.pph[i])) % W)
            cy = int((self.py[i] + self.vy[i] * local_t) % H)
            sz = int(self.psz[i])
            tw = 0.65 + 0.35 * np.sin(local_t * 1.5 + self.pph[i])
            op = float(self.pop[i] * tw)
            sp = self.sprite_base.resize((sz, sz), Image.Resampling.BILINEAR)
            r, g, b, a = sp.split()
            a = a.point(lambda v, s=op: int(v * s))
            sp.putalpha(a)
            particle_layer.alpha_composite(sp, dest=(max(0, min(W - sz, cx - sz // 2)), max(0, min(H - sz, cy - sz // 2))))

        clean_rgba = Image.alpha_composite(clean_rgba, particle_layer)
        clean_rgb = clean_rgba.convert("RGB")

        typo_rgba = clean_rgba.copy()
        cues = [
            ("logo_and_title", 0.35, 1.45),
            ("en_tagline", 1.75, 2.85),
            ("hi_tagline", 5.10, 6.10),
            ("url_pill", 7.65, 8.65),
        ]
        for name, t0, t1 in cues:
            op = smoothstep(local_t, t0, t1)
            if op <= 0.002:
                continue
            lyr = self.layers[name]
            shift_y = int(round((1.0 - op) * 12.0))
            if op < 0.998:
                r, g, b, a = lyr.split()
                a = a.point(lambda v, s=op: int(v * s))
                lyr = Image.merge("RGBA", (r, g, b, a))
            typo_rgba.alpha_composite(lyr, dest=(0, shift_y))

        typo_rgb = typo_rgba.convert("RGB")
        if local_t > 11.55:
            fade = max(0.0, min(1.0, (12.0 - local_t) / 0.45))
            clean_rgb = Image.blend(self.black, clean_rgb, fade)
            typo_rgb = Image.blend(self.black, typo_rgb, fade)

        return clean_rgb, typo_rgb


def main():
    t0_wall = time.time()
    plates = {
        1: load_graded_pil("scene_01_jaipur_sunrise_16x9.jpg", 1.16),
        2: load_graded_pil("scene_02_learner_curiosity_16x9.jpg", 1.16),
        3: load_graded_pil("scene_03_tutor_connection_16x9.jpg", 1.16),
        4: load_graded_pil("scene_04_joy_of_learning_16x9.jpg", 1.16),
        5: load_graded_pil("scene_05_indian_culture_16x9.jpg", 1.16),
        6: load_graded_pil("scene_06_global_connection_16x9.jpg", 1.16),
    }
    s7 = FastScene7()
    black = Image.new("RGB", (W, H), (0, 0, 0))
    print(f"Plates prepared in {time.time() - t0_wall:.1f}s")

    def scene_frame_pil(sc, local_u):
        u = max(0.0, min(1.0, float(local_u)))
        e = ease_in_out(u)
        if sc == 1:
            return camera_crop_pil(plates[1], zoom=1.01 + 0.08 * u, pan_x=-0.35 + 0.70 * u, pan_y=0.15 - 0.30 * u)
        elif sc == 2:
            return camera_crop_pil(plates[2], zoom=1.00 + 0.09 * e, pan_x=-0.15 + 0.25 * e, pan_y=0.10 - 0.15 * e)
        elif sc == 3:
            return camera_crop_pil(plates[3], zoom=1.01 + 0.07 * e, pan_x=0.20 - 0.35 * e, pan_y=0.0)
        elif sc == 4:
            return camera_crop_pil(plates[4], zoom=1.00 + 0.095 * e, pan_x=0.05 + 0.15 * e, pan_y=-0.05)
        elif sc == 5:
            return camera_crop_pil(plates[5], zoom=1.02 + 0.075 * u, pan_x=-0.40 + 0.80 * u, pan_y=0.05)
        elif sc == 6:
            return camera_crop_pil(plates[6], zoom=1.08 - 0.065 * e, pan_x=-0.25 + 0.50 * e, pan_y=0.0)
        raise ValueError(sc)

    audio_master = os.path.join(MUS_DIR, "ekguru_master_audio_60s_bilingual.wav")
    s7_clean_mp4 = os.path.join(GFX_DIR, "scene_07_clean_particle_bg_12s_16x9.mp4")
    s7_master_mp4 = os.path.join(EXP_DIR, "scene_07_brand_reveal_master_16x9.mp4")
    previz_mp4 = os.path.join(EXP_DIR, "ekguru_60s_directors_previz_16x9.mp4")

    # Stream all three outputs in a single memory-light pass (zero frame caching!)
    p_clean = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", s7_clean_mp4],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    p_s7 = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-ss", "48", "-t", "12", "-i", audio_master,
         "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", s7_master_mp4],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    p_previz = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-i", audio_master,
         "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", previz_mp4],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    _, s7_first_frame = s7.render_pair(0.0)
    diss_half = 0.35

    for f_idx in range(60 * FPS):
        t = f_idx / FPS
        if t < 48.0:
            sc = min(6, int(t // 8.0) + 1)
            local_u = (t - (sc - 1) * 8.0) / 8.0
            fr = scene_frame_pil(sc, local_u)

            if t < 0.55:
                fr = Image.blend(black, fr, t / 0.55)

            for bt, (sp, sn) in [(8.0, (1, 2)), (32.0, (4, 5))]:
                if abs(t - bt) < diss_half:
                    alpha = ease_in_out((t - (bt - diss_half)) / (2 * diss_half))
                    fp = scene_frame_pil(sp, (t - (sp - 1) * 8.0) / 8.0)
                    fn = scene_frame_pil(sn, (t - (sn - 1) * 8.0) / 8.0)
                    fr = Image.blend(fp, fn, alpha)

            if t >= 47.55:
                alpha = ease_in_out((t - 47.55) / 0.45)
                fr = Image.blend(fr, s7_first_frame, alpha)

            p_previz.stdin.write(fr.tobytes())
        else:
            lt = t - 48.0
            fr_clean, fr_typo = s7.render_pair(lt)
            p_clean.stdin.write(fr_clean.tobytes())
            p_s7.stdin.write(fr_typo.tobytes())
            p_previz.stdin.write(fr_typo.tobytes())

        if (f_idx + 1) % 300 == 0:
            print(f"  Rendered {f_idx + 1}/1800 frames ({time.time() - t0_wall:.1f}s elapsed)")

    for p in (p_clean, p_s7, p_previz):
        p.stdin.close()
    for p in (p_clean, p_s7, p_previz):
        p.wait()

    print(f"ALL RENDERS COMPLETE in {time.time() - t0_wall:.1f}s!")


if __name__ == "__main__":
    main()
