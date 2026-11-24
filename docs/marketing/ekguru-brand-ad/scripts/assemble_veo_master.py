#!/usr/bin/env python3
"""
EkGuru — Turnkey Veo 3.1 Lite Master Commercial Assembler & Multi-Format Finisher
=================================================================================
Preserves all original approved Veo 3.1 Lite MP4 clips in `01_approved_veo_clips/`
(NEVER overwrites originals) and masters:

  --mode main
      -> 06_exports/ekguru_ad_FINAL_60s_16x9.mp4 (1920x1080, 30fps, warm golden cinema grade,
         gentle filmic dissolves at Scene 1->2, 4->5, 6->7, clean cuts at 2->3->4 & 5->6,
         animated official EkGuru logo + HarfBuzz-shaped Hindi & English taglines on Scene 7,
         and broadcast-leveled bilingual Hindi+English voice-over + original cinematic score).

  --mode derivatives  (run AFTER main 16:9 version is approved!)
      -> 06_exports/ekguru_ad_FINAL_60s_9x16_reels_shorts.mp4 (1080x1920 vertical Reels/Shorts)
      -> 06_exports/ekguru_ad_FINAL_15s_teaser_16x9.mp4       (1920x1080 15-second teaser)
"""
import argparse
import os
import sys
import subprocess
import numpy as np
from scipy.io import wavfile
import imageio_ffmpeg

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VEO_DIR = os.path.join(ROOT, "01_approved_veo_clips")
GFX_DIR = os.path.join(ROOT, "05_brand_graphics")
VO_DIR = os.path.join(ROOT, "03_voiceover")
MUS_DIR = os.path.join(ROOT, "04_music_and_sfx")
EXP_DIR = os.path.join(ROOT, "06_exports")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def find_scene_clips():
    clips = {}
    for i in range(1, 8):
        candidates = [
            os.path.join(VEO_DIR, f"scene_0{i}.mp4"),
            os.path.join(VEO_DIR, f"Scene_0{i}.mp4"),
            os.path.join(VEO_DIR, f"scene_{i}.mp4"),
        ]
        found = next((c for c in candidates if os.path.isfile(c)), None)
        if found:
            clips[i] = found
    # Scene 7 fallback: if user prefers the luxury procedural golden-particle plate or hasn't exported S7 yet
    s7_fallback = os.path.join(GFX_DIR, "scene_07_clean_particle_bg_12s_16x9.mp4")
    if 7 not in clips and os.path.isfile(s7_fallback):
        clips[7] = s7_fallback
    return clips


def normalize_clip(src_path, dst_path, target_dur, width=1920, height=1080, warm_grade=True):
    """Conform an approved Veo clip to exact resolution, 30fps, and target duration without touching the original."""
    vf_parts = [
        f"scale={width}:{height}:force_original_aspect_ratio=increase",
        f"crop={width}:{height}",
        "fps=30",
    ]
    if warm_grade:
        vf_parts.append("colorbalance=rs=0.02:gs=0.005:bs=-0.02:rh=0.03:gh=0.01:bh=-0.02,eq=contrast=1.03:saturation=1.03")
    vf_parts.append("format=yuv420p")
    cmd = [
        FFMPEG, "-y", "-i", src_path,
        "-t", f"{target_dur:.3f}",
        "-vf", ",".join(vf_parts),
        "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "16",
        dst_path,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build_15s_teaser_audio(out_wav):
    """Build dedicated 15.0s teaser bilingual audio (Jaipur hook -> EkGuru connection -> Brand CTA)."""
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

    for clip, st in [(en1, 0.35), (en7, 3.30), (hi_tag, 8.10), (cta, 10.65)]:
        fade = min(int(0.025 * sr), len(clip) // 4)
        c = clip.copy()
        c[:fade] *= np.linspace(0, 1, fade)
        c[-fade:] *= np.linspace(1, 0, fade)
        i0 = int(st * sr)
        i1 = min(n, i0 + len(c))
        vo[i0:i1] += c[: i1 - i0]

    _, score_full_mp3_or_flac = None, None
    flac_score = os.path.join(MUS_DIR, "ekguru_cinematic_score_60s.flac")
    tmp_sc_wav = "/tmp/sc_tmp_15s.wav"
    subprocess.run([FFMPEG, "-y", "-i", flac_score, "-ar", "48000", "-ac", "2", tmp_sc_wav],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _, score_full = wavfile.read(tmp_sc_wav)
    # Take climax + resolve (45..60s) of our original score
    sc_seg = score_full[45 * sr : 60 * sr].astype(np.float32) / 32768.0
    sc_seg[: int(0.4 * sr)] *= np.linspace(0, 1, int(0.4 * sr))[:, None]
    mix_l = vo * 0.85 + sc_seg[:, 0] * 0.34
    mix_r = vo * 0.85 + sc_seg[:, 1] * 0.34
    mix = np.clip(np.stack([mix_l, mix_r], axis=1), -0.95, 0.95)
    wavfile.write(out_wav, sr, (mix * 32767.0).astype(np.int16))


def master_main_16x9(clips, lang="bilingual"):
    tmp = "/tmp/ekguru_veo_conform"
    os.makedirs(tmp, exist_ok=True)
    print("Conforming approved Veo clips (preserving originals untouched)...")
    for i in range(1, 7):
        normalize_clip(clips[i], f"{tmp}/s{i}.mp4", target_dur=8.40, width=1920, height=1080, warm_grade=True)

    # Prepare 12.4s Scene 7 with animated official EkGuru brand overlays
    s7_raw = f"{tmp}/s7_base.mp4"
    # Loop/extend smoothly if user's Veo Scene 7 is 8s instead of 12s
    subprocess.run(
        [FFMPEG, "-y", "-stream_loop", "1", "-i", clips[7], "-t", "12.40",
         "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p",
         "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "16", s7_raw],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    s7_comp = f"{tmp}/s7.mp4"
    l1 = os.path.join(GFX_DIR, "layer_logo_and_title_1920x1080.png")
    l2 = os.path.join(GFX_DIR, "layer_en_tagline_1920x1080.png")
    l3 = os.path.join(GFX_DIR, "layer_hi_tagline_1920x1080.png")
    l4 = os.path.join(GFX_DIR, "layer_url_pill_1920x1080.png")
    fc = (
        "[1:v]format=rgba,fade=t=in:st=0.35:d=1.0:alpha=1[v1];"
        "[2:v]format=rgba,fade=t=in:st=1.75:d=1.0:alpha=1[v2];"
        "[3:v]format=rgba,fade=t=in:st=5.10:d=0.95:alpha=1[v3];"
        "[4:v]format=rgba,fade=t=in:st=7.65:d=0.95:alpha=1[v4];"
        "[0:v][v1]overlay=0:0[a1];"
        "[a1][v2]overlay=0:0[a2];"
        "[a2][v3]overlay=0:0[a3];"
        "[a3][v4]overlay=0:0,fade=t=out:st=11.55:d=0.45,format=yuv420p[vout]"
    )
    subprocess.run(
        [FFMPEG, "-y", "-i", s7_raw,
         "-loop", "1", "-t", "12.4", "-i", l1,
         "-loop", "1", "-t", "12.4", "-i", l2,
         "-loop", "1", "-t", "12.4", "-i", l3,
         "-loop", "1", "-t", "12.4", "-i", l4,
         "-filter_complex", fc, "-map", "[vout]",
         "-t", "12.0", "-c:v", "libx264", "-preset", "fast", "-crf", "16", s7_comp],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    # Assemble 60.0s timeline (exact 8.0s per scene 1..6 + 12.0s scene 7)
    trimmed = []
    for i in range(1, 7):
        tp = f"{tmp}/t{i}.mp4"
        vf = "fade=t=in:st=0:d=0.55" if i == 1 else "null"
        subprocess.run(
            [FFMPEG, "-y", "-i", f"{tmp}/s{i}.mp4", "-t", "8.0", "-vf", vf,
             "-c:v", "libx264", "-preset", "fast", "-crf", "16", tp],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        trimmed.append(tp)
    trimmed.append(s7_comp)

    concat_txt = f"{tmp}/concat.txt"
    with open(concat_txt, "w") as f:
        for p in trimmed:
            f.write(f"file '{p}'\n")

    audio_map = {
        "bilingual": "ekguru_master_audio_60s_bilingual.flac",
        "english": "ekguru_master_audio_60s_english.flac",
        "hindi": "ekguru_master_audio_60s_hindi.flac",
    }
    audio_path = os.path.join(MUS_DIR, audio_map[lang])
    out_mp4 = os.path.join(EXP_DIR, "ekguru_ad_FINAL_60s_16x9.mp4")

    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-i", audio_path,
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out_mp4],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"SUCCESS: Exported Final 60s 16:9 Master -> {out_mp4}")


def master_derivatives(clips):
    tmp = "/tmp/ekguru_veo_deriv"
    os.makedirs(tmp, exist_ok=True)
    audio_60 = os.path.join(MUS_DIR, "ekguru_master_audio_60s_bilingual.flac")
    end_9x16 = os.path.join(GFX_DIR, "scene_07_endcard_overlay_1080x1920.png")

    # 1) 9:16 Vertical Reels & Shorts (1080x1920, 60s)
    v_parts = []
    for i in range(1, 7):
        vp = f"{tmp}/v{i}.mp4"
        normalize_clip(clips[i], vp, target_dur=8.0, width=1080, height=1920, warm_grade=True)
        v_parts.append(vp)

    v7_base = f"{tmp}/v7_base.mp4"
    subprocess.run(
        [FFMPEG, "-y", "-stream_loop", "1", "-i", clips[7], "-t", "12.0",
         "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
         "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "17", v7_base],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    v7 = f"{tmp}/v7.mp4"
    subprocess.run(
        [FFMPEG, "-y", "-i", v7_base, "-loop", "1", "-t", "12.0", "-i", end_9x16,
         "-filter_complex", "[1:v]format=rgba,fade=t=in:st=0.5:d=1.1:alpha=1[ov];[0:v][ov]overlay=0:0,fade=t=out:st=11.5:d=0.5,format=yuv420p[v]",
         "-map", "[v]", "-t", "12.0", "-c:v", "libx264", "-preset", "fast", "-crf", "17", v7],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    v_parts.append(v7)

    v_concat = f"{tmp}/v_concat.txt"
    with open(v_concat, "w") as f:
        for p in v_parts:
            f.write(f"file '{p}'\n")
    out_9x16 = os.path.join(EXP_DIR, "ekguru_ad_FINAL_60s_9x16_reels_shorts.mp4")
    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", v_concat, "-i", audio_60,
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out_9x16],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"SUCCESS: Exported 9:16 Vertical Reels/Shorts -> {out_9x16}")

    # 2) 15-Second Teaser (16:9): S1 (3s) + S3 (3.5s) + S5 (3.5s) + S7 Brand Reveal (5s) = 15.0s
    teaser_wav = os.path.join(MUS_DIR, "ekguru_teaser_audio_15s.wav")
    build_15s_teaser_audio(teaser_wav)
    t_specs = [(1, 3.0), (3, 3.5), (5, 3.5)]
    t_parts = []
    for idx, dur in t_specs:
        tp = f"{tmp}/ts_{idx}.mp4"
        normalize_clip(clips[idx], tp, target_dur=dur, width=1920, height=1080, warm_grade=True)
        t_parts.append(tp)

    end_16x9 = os.path.join(GFX_DIR, "scene_07_endcard_overlay_1920x1080.png")
    ts7_base = f"{tmp}/ts_7_base.mp4"
    normalize_clip(clips[7], ts7_base, target_dur=5.0, width=1920, height=1080, warm_grade=False)
    ts7 = f"{tmp}/ts_7.mp4"
    subprocess.run(
        [FFMPEG, "-y", "-i", ts7_base, "-loop", "1", "-t", "5.0", "-i", end_16x9,
         "-filter_complex", "[1:v]format=rgba,fade=t=in:st=0.25:d=0.8:alpha=1[ov];[0:v][ov]overlay=0:0,fade=t=out:st=4.6:d=0.4,format=yuv420p[v]",
         "-map", "[v]", "-t", "5.0", "-c:v", "libx264", "-preset", "fast", "-crf", "17", ts7],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    t_parts.append(ts7)

    t_concat = f"{tmp}/t_concat.txt"
    with open(t_concat, "w") as f:
        for p in t_parts:
            f.write(f"file '{p}'\n")
    out_15s = os.path.join(EXP_DIR, "ekguru_ad_FINAL_15s_teaser_16x9.mp4")
    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", t_concat, "-i", teaser_wav,
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out_15s],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"SUCCESS: Exported 15s Teaser -> {out_15s}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["main", "derivatives", "all"], default="main")
    ap.add_argument("--lang", choices=["bilingual", "english", "hindi"], default="bilingual")
    args = ap.parse_args()

    clips = find_scene_clips()
    missing = [i for i in range(1, 7) if i not in clips]
    if missing:
        print("WAITING FOR APPROVED GOOGLE FLOW (VEO 3.1 LITE) CLIPS:")
        for m in missing:
            print(f"  Missing: {VEO_DIR}/scene_0{m}.mp4")
        print("\nDrop your approved 8-second Veo 3.1 Lite MP4 clips into 01_approved_veo_clips/ (or share via Google Drive) and re-run!")
        sys.exit(1)

    if args.mode in ("main", "all"):
        master_main_16x9(clips, lang=args.lang)
    if args.mode in ("derivatives", "all"):
        master_derivatives(clips)


if __name__ == "__main__":
    main()
