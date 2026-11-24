#!/usr/bin/env python3
"""
Compose an original, 100% royalty-free Indian-fusion cinematic commercial score (48kHz stereo)
and mix it with the bilingual Hindi + English voice-over stems for the 60.0s EkGuru Brand Ad.
"""
import os
import subprocess
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfiltfilt, fftconvolve
import imageio_ffmpeg

ROOT = "docs/marketing/ekguru-brand-ad"
VO_DIR = os.path.join(ROOT, "03_voiceover")
MUS_DIR = os.path.join(ROOT, "04_music_and_sfx")
SR = 48000
DUR = 60.0
N = int(SR * DUR)


def read_mono_wav(path):
    sr, data = wavfile.read(path)
    assert sr == SR, f"Expected {SR}, got {sr}"
    if data.ndim > 1:
        data = data[:, 0]
    return data.astype(np.float32) / 32768.0


def place(buf, clip, start_s, gain=1.0):
    i0 = int(start_s * SR)
    i1 = min(len(buf), i0 + len(clip))
    if i1 > i0:
        buf[i0:i1] += clip[: i1 - i0] * gain


def slice_clip(clip, t0, t1):
    s0 = max(0, int(t0 * SR))
    s1 = min(len(clip), int(t1 * SR))
    seg = clip[s0:s1].copy()
    fade = min(int(0.025 * SR), len(seg) // 4)
    if fade > 0:
        seg[:fade] *= np.linspace(0, 1, fade)
        seg[-fade:] *= np.linspace(1, 0, fade)
    return seg


def build_vo_timelines():
    en = {i: read_mono_wav(os.path.join(VO_DIR, f"en_scene_0{i}.wav")) for i in range(1, 8)}
    en_cta = read_mono_wav(os.path.join(VO_DIR, "en_scene_07_cta.wav"))
    hi = {i: read_mono_wav(os.path.join(VO_DIR, f"hi_scene_0{i}.wav")) for i in range(1, 8)}
    hi_tag = read_mono_wav(os.path.join(VO_DIR, "hi_scene_07_tagline.wav"))

    # Check first clause "हिंदी सीखिए" inside hi[4] (~0.0 .. 1.05s; recall pause was ~0.76s..1.24s)
    # Let's find exact silence gap after "हिंदी सीखिए" in hi[4]:
    win = int(0.01 * SR)
    nw = len(hi[4]) // win
    rms = np.sqrt(np.mean(hi[4][: nw * win].reshape(nw, win) ** 2, axis=1))
    # First pause between 0.55s and 1.50s
    sub = rms[55:150]
    min_idx = 55 + int(np.argmin(sub))
    hi4_intro = slice_clip(hi[4], 0.0, min_idx * 0.01)
    print(f"hi[4] intro ('हिंदी सीखिए') duration: {len(hi4_intro)/SR:.2f}s")

    # 1) HERO 60.0s WOVEN BILINGUAL MASTER (Hindi + English synchronized to 7 scenes)
    vo_bi = np.zeros(N, dtype=np.float32)
    # Scene 1 (0-8s): EN establishing hook
    place(vo_bi, en[1], 0.55, 1.0)
    # Scene 2 (8-16s): EN curiosity
    place(vo_bi, en[2], 8.55, 1.0)
    # Scene 3 (16-24s): EN EkGuru tutor connection
    place(vo_bi, en[3], 16.45, 1.0)
    # Scene 4 (24-32s): HI "हिंदी सीखिए..." + EN "Discover Hindi. Learn with Indian tutors. Find your connection."
    place(vo_bi, hi4_intro, 24.45, 1.02)
    place(vo_bi, en[4], 24.45 + len(hi4_intro) / SR + 0.38, 1.0)
    # Scene 5 (32-40s): EN + HI poetic bridge ("Because learning a language is more than learning words... क्योंकि भाषा सिर्फ शब्दों का ज्ञान नहीं।")
    place(vo_bi, en[5], 32.45, 1.0)
    place(vo_bi, hi[5], 32.45 + len(en[5]) / SR + 0.42, 1.02)
    # Scene 6 (40-48s): EN global human connection
    place(vo_bi, en[6], 40.55, 1.0)
    # Scene 7 (48-60s): EN Brand + HI Official Tagline + EN CTA
    t_s7 = 48.55
    place(vo_bi, en[7], t_s7, 1.0)
    t_hi_tag = t_s7 + len(en[7]) / SR + 0.48
    place(vo_bi, hi_tag, t_hi_tag, 1.04)
    t_cta = t_hi_tag + len(hi_tag) / SR + 0.52
    place(vo_bi, en_cta, t_cta, 1.0)
    print(f"Scene 7 VO cues: EN={t_s7:.2f}s, HI_TAG={t_hi_tag:.2f}s, CTA={t_cta:.2f}s, END={t_cta + len(en_cta)/SR:.2f}s")

    # 2) 60.0s PURE ENGLISH MASTER
    vo_en = np.zeros(N, dtype=np.float32)
    for idx, t0 in [(1, 0.55), (2, 8.55), (3, 16.45), (4, 24.55), (5, 32.65), (6, 40.55), (7, 48.65)]:
        place(vo_en, en[idx], t0, 1.0)
    place(vo_en, en_cta, 54.50, 1.0)

    # 3) 60.0s PURE HINDI MASTER (note hi[3] is 8.17s -> starts at 16.05s)
    vo_hi = np.zeros(N, dtype=np.float32)
    place(vo_hi, hi[1], 0.55, 1.0)
    place(vo_hi, hi[2], 8.45, 1.0)
    place(vo_hi, hi[3], 15.95, 1.0)
    place(vo_hi, hi[4], 24.55, 1.0)
    place(vo_hi, hi[5], 32.80, 1.0)
    place(vo_hi, hi[6], 40.45, 1.0)
    place(vo_hi, hi[7], 48.45, 1.0)
    place(vo_hi, hi_tag, 56.10, 1.0)

    for name, arr in [
        ("vo_master_60s_bilingual.wav", vo_bi),
        ("vo_master_60s_english.wav", vo_en),
        ("vo_master_60s_hindi.wav", vo_hi),
    ]:
        wavfile.write(
            os.path.join(VO_DIR, name),
            SR,
            np.clip(arr * 32767.0, -32768, 32767).astype(np.int16),
        )
    return vo_bi, vo_en, vo_hi


def midi_to_hz(m):
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))


def make_stereo_reverb_ir(rt60=2.6, dur=3.2):
    rng = np.random.default_rng(2026)
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    decay = np.exp(-6.91 * t / rt60)
    # Pre-delay 22ms + smooth early reflections
    ir_l = rng.normal(0, 1, n).astype(np.float32) * decay
    ir_r = rng.normal(0, 1, n).astype(np.float32) * decay
    ir_l[: int(0.022 * SR)] *= np.linspace(0, 1, int(0.022 * SR))
    ir_r[: int(0.025 * SR)] *= np.linspace(0, 1, int(0.025 * SR))
    sos = butter(2, [140 / (SR / 2), 4200 / (SR / 2)], btype="bandpass", output="sos")
    ir_l = sosfiltfilt(sos, ir_l).astype(np.float32)
    ir_r = sosfiltfilt(sos, ir_r).astype(np.float32)
    norm = max(np.sqrt(np.sum(ir_l**2)), 1e-6)
    return ir_l / norm, ir_r / norm


def synth_bansuri_note(freq, dur, amp=0.12, vib_rate=5.1, vib_depth=0.005):
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    vib = 1.0 + vib_depth * np.sin(2 * np.pi * vib_rate * t) * np.clip((t - 0.18) / 0.35, 0, 1)
    phase = 2 * np.pi * np.cumsum(freq * vib) / SR
    # Warm bamboo flute harmonics (strong fundamental + soft 2nd & 3rd) + subtle breath air
    tone = (
        1.00 * np.sin(phase)
        + 0.34 * np.sin(2 * phase + 0.2)
        + 0.11 * np.sin(3 * phase + 0.5)
        + 0.03 * np.sin(4 * phase)
    )
    rng = np.random.default_rng(int(freq * 100))
    breath = rng.normal(0, 0.035, n).astype(np.float32)
    sos = butter(2, [900 / (SR / 2), 2600 / (SR / 2)], btype="bandpass", output="sos")
    breath = sosfiltfilt(sos, breath).astype(np.float32)
    # Soft expressive attack & release
    att = min(int(0.24 * SR), n // 3)
    rel = min(int(0.38 * SR), n // 2)
    env = np.ones(n, dtype=np.float32)
    env[:att] = 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, att)))
    env[-rel:] = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, rel)))
    return (tone + breath) * env * amp


def synth_santoor_pluck(freq, dur, amp=0.09):
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    # Warm plucked string / felt piano hybrid: harmonics decay faster at higherpartials
    sig = np.zeros(n, dtype=np.float32)
    partials = [(1.0, 1.0, 1.8), (2.0, 0.42, 1.1), (3.0, 0.18, 0.75), (4.003, 0.08, 0.45), (5.008, 0.03, 0.3)]
    for mult, g, tau in partials:
        sig += g * np.sin(2 * np.pi * freq * mult * t) * np.exp(-t / tau)
    att = min(int(0.008 * SR), n // 4)
    sig[:att] *= np.linspace(0, 1, att)
    fade_end = min(int(0.08 * SR), n // 4)
    sig[-fade_end:] *= np.linspace(1, 0, fade_end)
    return sig * amp


def synth_warm_pad_chord(midi_notes, dur, amp=0.065):
    n = int(SR * dur)
    t = np.arange(n, dtype=np.float32) / SR
    l = np.zeros(n, dtype=np.float32)
    r = np.zeros(n, dtype=np.float32)
    for idx, m in enumerate(midi_notes):
        f = midi_to_hz(m)
        # Warm analog strings/cello detuned ensemble
        for det, pan_l, pan_r in [(-0.0022, 0.85, 0.35), (0.0, 0.65, 0.65), (0.0024, 0.35, 0.85)]:
            ph = 2 * np.pi * f * (1.0 + det) * t + idx * 0.7
            wave = 0.68 * np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
            l += wave * pan_l
            r += wave * pan_r
    att = min(int(1.1 * SR), n // 3)
    rel = min(int(1.4 * SR), n // 3)
    env = np.ones(n, dtype=np.float32)
    env[:att] = 0.5 * (1 - np.cos(np.pi * np.linspace(0, 1, att)))
    env[-rel:] = 0.5 * (1 + np.cos(np.pi * np.linspace(0, 1, rel)))
    sos = butter(2, 1900 / (SR / 2), btype="lowpass", output="sos")
    l = sosfiltfilt(sos, l * env).astype(np.float32) * (amp / max(len(midi_notes), 1))
    r = sosfiltfilt(sos, r * env).astype(np.float32) * (amp / max(len(midi_notes), 1))
    return l, r


def compose_score():
    dry_l = np.zeros(N, dtype=np.float32)
    dry_r = np.zeros(N, dtype=np.float32)
    wet_send = np.zeros(N, dtype=np.float32)

    def add_stereo(l_sig, r_sig, start_s, send=0.45):
        i0 = int(start_s * SR)
        i1 = min(N, i0 + len(l_sig))
        if i1 > i0:
            seg_l = l_sig[: i1 - i0]
            seg_r = r_sig[: i1 - i0]
            dry_l[i0:i1] += seg_l
            dry_r[i0:i1] += seg_r
            wet_send[i0:i1] += 0.5 * (seg_l + seg_r) * send

    def add_mono(sig, start_s, pan=0.0, send=0.55):
        gl = np.sqrt(0.5 * (1.0 - pan))
        gr = np.sqrt(0.5 * (1.0 + pan))
        add_stereo(sig * gl, sig * gr, start_s, send=send)

    # 1. Subtle Golden Tanpura / Warm Atmospheric Drone (0..18s, returning gently at 47..60s)
    t_full = np.arange(N, dtype=np.float32) / SR
    drone_env = np.zeros(N, dtype=np.float32)
    # 0..18s fade in & gentle taper
    e1 = int(18 * SR)
    drone_env[:e1] = np.sin(np.pi * np.linspace(0, 1, e1)) ** 0.7 * 0.85
    # Gentle continuous bed 14..48s
    drone_env[int(12 * SR) : int(49 * SR)] = np.maximum(drone_env[int(12 * SR) : int(49 * SR)], 0.45)
    # Final brand resolve 47..60s
    s7 = int(47 * SR)
    drone_env[s7:] = np.maximum(drone_env[s7:], np.sin(np.pi * np.linspace(0.15, 1.0, N - s7)) * 0.9)
    drone_env[-int(2.2 * SR) :] *= np.linspace(1, 0, int(2.2 * SR))

    d_f1, d_f2, d_f3 = midi_to_hz(38), midi_to_hz(45), midi_to_hz(50)  # D2, A2, D3
    tanpura_l = (
        0.028 * np.sin(2 * np.pi * d_f1 * t_full)
        + 0.020 * np.sin(2 * np.pi * d_f2 * 1.001 * t_full + 0.4)
        + 0.016 * np.sin(2 * np.pi * d_f3 * 0.999 * t_full + 1.1)
    ) * drone_env
    tanpura_r = (
        0.028 * np.sin(2 * np.pi * d_f1 * t_full)
        + 0.020 * np.sin(2 * np.pi * d_f2 * 0.999 * t_full + 0.9)
        + 0.016 * np.sin(2 * np.pi * d_f3 * 1.001 * t_full + 0.2)
    ) * drone_env
    dry_l += tanpura_l
    dry_r += tanpura_r
    wet_send += 0.35 * (tanpura_l + tanpura_r)

    # 2. Scene 1 (0..8s): Gentle Bansuri Sunrise Motif (D Major / Kalyan touch)
    bansuri_s1 = [
        (0.25, 69, 1.6, 0.075),   # A4
        (1.75, 71, 1.3, 0.070),   # B4
        (2.95, 74, 2.0, 0.078),   # D5
        (5.25, 78, 1.3, 0.095),   # F#5 (blooms right as VO finishes Scene 1!)
        (6.40, 76, 1.7, 0.088),   # E5 -> floats into Scene 2
    ]
    for st, m, d, a in bansuri_s1:
        add_mono(synth_bansuri_note(midi_to_hz(m), d, amp=a), st, pan=-0.12, send=0.72)

    # 3. Harmonic Chord Progression across Scenes 2..7
    chords = [
        # Scene 2 (8..16s): Warm curiosity
        (8.0, 4.2, [50, 57, 62, 66], 0.055),       # Dmaj7
        (12.0, 4.2, [47, 54, 59, 62, 66], 0.062),  # Bm9
        # Scene 3 (16..24s): Human connection
        (16.0, 4.2, [43, 50, 55, 59, 66], 0.072),  # Gmaj7
        (20.0, 4.2, [45, 52, 57, 64], 0.076),      # Asus4/A
        # Scene 4 (24..32s): Joy of learning
        (24.0, 4.2, [50, 57, 62, 66, 69], 0.082),  # Dadd9
        (28.0, 4.2, [45, 52, 57, 61, 64], 0.084),  # A major warm
        # Scene 5 (32..40s): Experience Indian culture (emotional lift!)
        (32.0, 4.2, [43, 50, 55, 59, 62, 66], 0.096),  # Gmaj9 lush
        (36.0, 4.2, [47, 54, 59, 62, 66, 69], 0.100),  # Bm11
        # Scene 6 (40..48s): Connection beyond borders (peak warmth!)
        (40.0, 4.2, [43, 50, 55, 62, 66, 71], 0.108),  # Gmaj7(#11/9)
        (44.0, 4.3, [45, 52, 57, 62, 64, 69], 0.114),  # A13sus4 uplifting swell
        # Scene 7 (48..60s): Sophisticated Brand Reveal in Dadd9
        (48.0, 6.5, [38, 45, 50, 57, 62, 66, 69], 0.110),  # Deep luxury Dadd9
        (54.0, 5.8, [38, 45, 50, 57, 64, 66, 74], 0.092),  # Final golden resolve
    ]
    for st, dur, notes, amp in chords:
        pl, pr = synth_warm_pad_chord(notes, dur, amp=amp)
        add_stereo(pl, pr, st, send=0.55)

    # 4. Gentle Santoor / Felt-Piano Arpeggio Pattern (8..48s) + Luxury Shimmer Chimes (48..59s)
    arp_patterns = [
        (8.0, [62, 66, 69, 74], 0.50, 16, 0.052),    # Scene 2 gentle
        (16.0, [59, 62, 67, 71, 74, 71, 67, 62] * 2, 0.50, 16, 0.058),  # Scene 3
        (24.0, [62, 66, 69, 74, 76, 74, 69, 66] * 2, 0.50, 16, 0.064),  # Scene 4
        (32.0, [59, 62, 66, 71, 74, 78, 74, 71] * 2, 0.50, 16, 0.072),  # Scene 5
        (40.0, [62, 67, 71, 74, 76, 78, 81, 78] * 2, 0.50, 16, 0.078),  # Scene 6 build
    ]
    for base_t, seq, step, count, amp in arp_patterns:
        for k in range(count):
            m = seq[k % len(seq)]
            t_note = base_t + k * step
            pan = 0.25 * np.sin(k * 0.9)
            add_mono(synth_santoor_pluck(midi_to_hz(m), 1.65, amp=amp), t_note, pan=pan, send=0.52)

    # Expressive Bansuri soaring counter-melody in Scene 5 & Scene 6 & Brand Resolve
    bansuri_late = [
        (35.6, 74, 1.4, 0.070),   # D5
        (38.6, 78, 1.5, 0.082),   # F#5
        (44.8, 76, 1.4, 0.085),   # E5
        (46.1, 78, 1.8, 0.092),   # F#5 -> resolves into Scene 7!
        (48.1, 74, 2.8, 0.078),   # D5 warm resolve on EkGuru reveal
    ]
    for st, m, d, a in bansuri_late:
        add_mono(synth_bansuri_note(midi_to_hz(m), d, amp=a), st, pan=0.14, send=0.75)

    # Scene 7 Crystalline Golden Harmonic Shimmer (48.0s, 53.2s, 58.6s)
    for st, notes, a in [
        (48.05, [62, 69, 74, 78, 81], 0.058),
        (53.20, [66, 74, 76, 81], 0.046),
        (57.80, [62, 69, 74, 86], 0.042),
    ]:
        for idx, m in enumerate(notes):
            add_mono(synth_santoor_pluck(midi_to_hz(m), 2.8, amp=a), st + idx * 0.14, pan=-0.2 + 0.1 * idx, send=0.72)

    # Apply lush stereo concert-hall convolution reverb
    ir_l, ir_r = make_stereo_reverb_ir(rt60=2.5, dur=3.0)
    rev_l = fftconvolve(wet_send, ir_l)[:N] * 0.42
    rev_r = fftconvolve(wet_send, ir_r)[:N] * 0.42

    mus_l = dry_l + rev_l
    mus_r = dry_r + rev_r

    # Clean master fade-in (0.3s) and fade-out (1.2s at 58.8..60.0s)
    mus_l[: int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    mus_r[: int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    fo = int(1.4 * SR)
    mus_l[-fo:] *= np.linspace(1, 0, fo) ** 1.3
    mus_r[-fo:] *= np.linspace(1, 0, fo) ** 1.3

    peak = max(np.max(np.abs(mus_l)), np.max(np.abs(mus_r)), 1e-6)
    mus_l = mus_l * (0.62 / peak)
    mus_r = mus_r * (0.62 / peak)

    stereo_score = np.stack([mus_l, mus_r], axis=1)
    score_path = os.path.join(MUS_DIR, "ekguru_cinematic_score_60s.wav")
    wavfile.write(score_path, SR, np.clip(stereo_score * 32767.0, -32768, 32767).astype(np.int16))
    print("Saved standalone musical score:", score_path)
    return stereo_score


def mix_vo_and_score(vo_mono, score_stereo, out_wav_path):
    # Warm broadcast EQ on VO (gentle high-pass at 80Hz + subtle presence)
    sos_hp = butter(2, 80 / (SR / 2), btype="highpass", output="sos")
    vo = sosfiltfilt(sos_hp, vo_mono).astype(np.float32)
    vo_peak = max(np.max(np.abs(vo)), 1e-6)
    vo = vo * (0.82 / vo_peak)  # Clear, upfront -1.7 dBFS peak VO

    # Smooth look-ahead sidechain ducking envelope from VO activity
    env_raw = np.abs(vo)
    # 180ms look-ahead + smooth 350ms Gaussian-like window
    win_len = int(0.45 * SR)
    kernel = np.hanning(win_len).astype(np.float32)
    kernel /= np.sum(kernel)
    shifted_vo = np.pad(env_raw, (0, int(0.14 * SR)))[int(0.14 * SR) :]
    activity = np.convolve(shifted_vo, kernel, mode="same")
    duck = 1.0 - 0.62 * np.clip(activity / 0.045, 0.0, 1.0)
    # Music sits gracefully underneath VO (~ -15 dB during speech, ~ -8.5 dB in scenic breaths)
    music_gain = 0.42 * duck

    mix_l = vo + score_stereo[:, 0] * music_gain
    mix_r = vo + score_stereo[:, 1] * music_gain

    # Soft mastering limiter (tanh ceiling at 0.92)
    mix = np.stack([mix_l, mix_r], axis=1)
    mx = max(np.max(np.abs(mix)), 1e-6)
    if mx > 0.89:
        mix = 0.89 * np.tanh(mix / 0.89)

    wavfile.write(out_wav_path, SR, np.clip(mix * 32767.0, -32768, 32767).astype(np.int16))
    # Also export 256kbps MP3 for convenience
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    mp3_out = out_wav_path.replace(".wav", ".mp3")
    subprocess.run(
        [ffmpeg, "-y", "-i", out_wav_path, "-b:a", "256k", mp3_out],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    rms_db = 20 * np.log10(np.sqrt(np.mean(mix**2)) + 1e-9)
    pk_db = 20 * np.log10(np.max(np.abs(mix)) + 1e-9)
    print(f"Saved master mix: {out_wav_path} (RMS={rms_db:.1f} dBFS, Peak={pk_db:.1f} dBFS)")


if __name__ == "__main__":
    vo_bi, vo_en, vo_hi = build_vo_timelines()
    score = compose_score()
    mix_vo_and_score(vo_bi, score, os.path.join(MUS_DIR, "ekguru_master_audio_60s_bilingual.wav"))
    mix_vo_and_score(vo_en, score, os.path.join(MUS_DIR, "ekguru_master_audio_60s_english.wav"))
    mix_vo_and_score(vo_hi, score, os.path.join(MUS_DIR, "ekguru_master_audio_60s_hindi.wav"))
