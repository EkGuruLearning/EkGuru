# EkGuru — Complete Cinematic Brand Advertisement Production Kit

**Brand:** EkGuru (`https://ekguru.shop`)  
**Main Tagline:** “Learn Indian Languages. Connect with India.”  
**Hindi Tagline:** “एक भाषा, एक नई दुनिया।”  
**Project Workspace:** `docs/marketing/ekguru-brand-ad/`

---

## 1. Access & Execution Audit (No-Faking Transparency Report)

| Capability / Asset | Status in Arena | Action Taken |
|---|---|---|
| **Official EkGuru Logo** | **Confirmed & Verified** (`images/logo.svg`, `images/logo-wordmark.svg`, `images/icon-512.png`) | Embedded unmodified official vector logo into all Scene 7 Brand Reveal layers & Thumbnail/Cover. |
| **Google Flow (Veo 3.1 Lite)** | **Unavailable directly from Arena** (`google_flow` / `flow` / `veo` connectors unsupported; sandbox outbound network restricted from `labs.google`) | Prepared all 7 Continuity Reference Frames (`02_reference_frames/`), exact copy-paste Veo 3.1 Lite prompts, scene-by-scene QC checklist, and one-command Veo Master Assembler (`scripts/assemble_veo_master.py`). **Manual operation required only to click Generate & Download for Scenes 1–6 (and optional Scene 7) in Google Flow.** |
| **Google Drive & Dropbox** | **Connected & Active** | Ready to ingest your exported Veo 3.1 Lite `.mp4` clips directly from Google Drive or direct chat upload. |
| **Bilingual Voice-Over (EN + HI)** | **Completed & Synchronized** | Recorded with your selected English (`voice-00`) & Hindi (`voice-01`) voices; split into 16 clean per-scene WAV stems + 3 full 60.0s timeline masters (`bilingual`, `english`, `hindi`). |
| **Original Cinematic Score & Mix** | **Completed & Broadcast-Leveled** | Composed 100% original royalty-free Indian-fusion cinematic score (Bansuri, Tanpura silk drone, Santoor/felt-piano arpeggios, warm orchestral strings, golden resolve) mixed beneath VO at `-17.8 dBFS RMS / -1.5 dBFS Peak`. |
| **Scene 7 Brand Reveal (`48–60s`)** | **Completed (Broadcast 1080p MP4)** | Rendered 30fps procedural 3D floating golden bokeh & volumetric glow + staggered luxury reveal of `EKGURU`, English tagline, HarfBuzz-shaped Devanagari `एक भाषा, एक नई दुनिया।`, and `ekguru.shop`. |
| **60s Timed Director's Pre-Viz** | **Completed (`1920x1080`, `60.00s`)** | Audio-locked 60s Pre-Viz (`ekguru_60s_directors_previz_16x9.mp4`) using our 7 QC-inspected continuity frames, smooth sub-pixel camera motion, warm cinema grade, and final bilingual audio mix. *(Explicitly labeled as Pre-Viz — NOT a substitute for Veo 3.1 Lite live-action motion clips.)* |
| **Clean Thumbnail / Cover (`16:9`)** | **Completed (`1920x1080` PNG & JPG)** | Saved to `06_exports/ekguru_thumbnail_16x9.png` & `.jpg`. |

---

## 2. Project Folder Structure

```text
docs/marketing/ekguru-brand-ad/
├── 01_approved_veo_clips/                     # Place approved raw 8s Veo 3.1 Lite MP4s here (scene_01.mp4 .. scene_07.mp4)
├── 02_reference_frames/                       # QC-approved 16:9 visual continuity plates for Google Flow "Frames to Video"
│   ├── scene_01_jaipur_sunrise_16x9.jpg
│   ├── scene_02_learner_curiosity_16x9.jpg
│   ├── scene_03_tutor_connection_16x9.jpg
│   ├── scene_04_joy_of_learning_16x9.jpg
│   ├── scene_05_indian_culture_16x9.jpg
│   ├── scene_06_global_connection_16x9.jpg
│   └── scene_07_brand_reveal_bg_16x9.jpg
├── 03_voiceover/                              # Individual per-scene EN & HI WAVs + 60s timeline VO stems
│   ├── en_scene_01.wav .. en_scene_07.wav, en_scene_07_cta.wav
│   ├── hi_scene_01.wav .. hi_scene_07.wav, hi_scene_07_tagline.wav
│   ├── vo_master_60s_bilingual.flac
│   ├── vo_master_60s_english.flac
│   └── vo_master_60s_hindi.flac
├── 04_music_and_sfx/                          # 100% original royalty-free score + broadcast master mixes
│   ├── ekguru_cinematic_score_60s.flac
│   ├── ekguru_master_audio_60s_bilingual.flac / .mp3
│   ├── ekguru_master_audio_60s_english.flac   / .mp3
│   └── ekguru_master_audio_60s_hindi.flac     / .mp3
├── 05_brand_graphics/                         # Official EkGuru SVG logos, HarfBuzz Devanagari vectors & 1080p/9:16 overlays
│   ├── ekguru_logo_official.svg
│   ├── scene_07_endcard_overlay_1920x1080.png
│   ├── scene_07_endcard_overlay_1080x1920.png
│   ├── scene_07_endcard_preview_dark_1920x1080.png
│   └── scene_07_clean_particle_bg_12s_16x9.mp4
├── 06_exports/                                # Playable renders & final deliverables
│   ├── ekguru_60s_directors_previz_16x9.mp4   # 60.0s Timed Pre-Viz (1920x1080, 30fps, H.264 + AAC)
│   ├── scene_07_brand_reveal_master_16x9.mp4  # 12.0s Finished Brand Ending (48–60s)
│   ├── ekguru_thumbnail_16x9.png / .jpg       # Clean 16:9 Cover / Thumbnail
│   └── (ekguru_ad_FINAL_60s_16x9.mp4, 9x16, & 15s teaser generated via assemble_veo_master.py)
└── scripts/
    ├── render_brand_graphics.mjs
    ├── compose_music_and_mix.py
    ├── render_scene7_and_previz.py
    └── assemble_veo_master.py
```

---

## 3. Step-by-Step Google Flow (Veo 3.1 Lite) Credit-Saving Operator Guide

To preserve your free Google Flow credits and guarantee **100% character & lighting continuity** across Scenes 2, 3, and 4:

1. Open **Google Flow** and select **Veo 3.1 Lite**, **16:9 Aspect Ratio**, **8 seconds**, **1 output per prompt** (do not batch-generate 4 variations at once).
2. **Generate ONE scene at a time**, starting with **Scene 1**.
3. Where Google Flow offers **Frames to Video (First Frame)**, upload the matching QC-approved plate from `02_reference_frames/` — especially for **Scenes 2, 3, and 4**, where our plates lock the **exact same international learner, sweater, sunlit desk, and Indian tutor**!
4. Inspect each 8-second MP4 against the **Scene QC Gate** below before moving to the next scene. Save each approved clip as `scene_01.mp4` … `scene_06.mp4` (and optional `scene_07.mp4`).

### Scene-by-Scene Prompts & QC Gates

#### SCENE 1 — THE BEAUTY OF INDIA (`0–8s`) -> save as `scene_01.mp4`
- **Optional Start Frame:** `02_reference_frames/scene_01_jaipur_sunrise_16x9.jpg`
- **Prompt:**
  > Cinematic aerial drone shot of Jaipur, India at sunrise, beautiful historic palaces, authentic Rajasthani architecture, warm golden sunlight, elegant heritage streets, atmospheric morning light, breathtaking wide establishing shot, slow smooth camera movement, ultra realistic, premium international travel and education commercial, cinematic color grading, 16:9, no text, no watermark.
- **QC Gate:** Smooth forward drone glide; realistic Rajasthani sandstone arches; no floating roofs, warped vehicles, or text overlays.

#### SCENE 2 — THE DREAM OF DISCOVERING INDIA (`8–16s`) -> save as `scene_02.mp4`
- **Recommended Start Frame (locks learner identity):** `02_reference_frames/scene_02_learner_curiosity_16x9.jpg`
- **Prompt:**
  > A young international adult student sitting beside a beautiful sunlit window, exploring a Hindi language book and writing Indian words in a notebook, curious and inspired expression, modern comfortable study space, natural human behavior, soft warm daylight, cinematic medium shot slowly moving into a close-up, premium international EdTech advertisement, ultra realistic, 16:9, no visible brand names, no text, no watermark.
- **QC Gate:** Five natural fingers on pen hand; calm genuine expression; no garbled AI letters jumping on the book cover.

#### SCENE 3 — THE HUMAN CONNECTION (`16–24s`) -> save as `scene_03.mp4`
- **Recommended Start Frame (locks same learner + Indian tutor):** `02_reference_frames/scene_03_tutor_connection_16x9.jpg`
- **Prompt:**
  > Premium cinematic scene of a friendly Indian language tutor teaching Hindi to a young international adult learner through a realistic laptop video call. Show both people in separate locations, naturally smiling and communicating, tutor explaining a simple Hindi word, learner listening attentively and responding with enthusiasm, authentic human expressions, realistic laptop screen and video call composition, professional but welcoming environments, soft natural lighting, cinematic close-ups and smooth camera movement, ultra realistic international EdTech commercial, 16:9, no logos, no subtitles, no watermark.
- **QC Gate:** Laptop hinge/screen stays rigid; tutor on screen moves naturally in sync with video-call framing; no fake platform UI or brand logos.

#### SCENE 4 — THE JOY OF LEARNING (`24–32s`) -> save as `scene_04.mp4`
- **Recommended Start Frame (locks same learner push-in):** `02_reference_frames/scene_04_joy_of_learning_16x9.jpg`
- **Prompt:**
  > A young international adult learner happily practicing spoken Hindi during an online lesson with an Indian tutor, close-up of the learner speaking confidently, writing a few Hindi practice notes in a notebook, genuine smile and natural expressions, warm modern study environment, cinematic camera push-in, premium realistic international language-learning advertisement, soft natural light, 16:9, no subtitles, no text overlays, no watermark.
- **QC Gate:** Natural lip/jaw movement while speaking; natural hand holding pen; clean unbranded laptop back.

#### SCENE 5 — EXPERIENCE INDIAN CULTURE (`32–40s`) -> save as `scene_05.mp4`
- **Optional Start Frame:** `02_reference_frames/scene_05_indian_culture_16x9.jpg`
- **Prompt:**
  > A breathtaking cinematic cultural journey through India, authentic Jaipur heritage architecture, colorful traditional Indian markets, beautiful handmade crafts, welcoming local people, intricate architectural details, natural cultural interactions, warm golden-hour lighting, elegant cinematic tracking shots, realistic colors, premium international travel commercial, ultra realistic, 16:9, no text, no watermark.
- **QC Gate:** Natural walking motion in background; authentic textiles/crafts; zero gibberish shop-sign text.

#### SCENE 6 — CONNECTION BEYOND BORDERS (`40–48s`) -> save as `scene_06.mp4`
- **Optional Start Frame:** `02_reference_frames/scene_06_global_connection_16x9.jpg`
- **Prompt:**
  > A cinematic montage of diverse young adult people from different countries connecting through language and cultural exchange, warm natural smiles, authentic conversations, sharing notebooks and cultural experiences, beautiful modern international environments, emotional human connection, realistic expressions, elegant camera movement, premium global education brand commercial, cinematic lighting, ultra realistic, 16:9, no text, no watermark.
- **QC Gate:** Natural eye-lines and laughter between friends; realistic hands holding cups/pens; not a classroom.

#### SCENE 7 — BRAND REVEAL BACKGROUND (`48–60s`) -> *Already Finished or Optional `scene_07.mp4`*
- **Note:** `06_exports/scene_07_brand_reveal_master_16x9.mp4` is **already finished at broadcast 1080p** with 3D golden bokeh particles and the real EkGuru logo & typography! If you also wish to generate a Veo background plate (`scene_07.mp4`), `assemble_veo_master.py` will automatically composite the exact official EkGuru logo, taglines, and `ekguru.shop` on top of it:
  > Elegant premium cinematic brand reveal background, sophisticated deep charcoal and black atmosphere with subtle warm golden light particles, beautiful soft golden illumination emerging from the center, refined luxury international education brand commercial ending, slow elegant camera movement, clean central negative space for placing the real EkGuru logo and tagline during editing, premium cinematic finish, 16:9, no generated text, no watermark.

---

## 4. How to Finish the Final Veo Commercial

Once you generate **Scene 1** (for immediate inspection) or **Scenes 1–6** in Google Flow:
1. Upload the MP4(s) directly in this chat **or** place them in a folder in your connected **Google Drive** and tell me the filename/folder.
2. I will inspect every clip frame-by-frame against the Visual & Brand QC Checklist, place approved originals untouched into `01_approved_veo_clips/`, and run:
   ```bash
   python3 docs/marketing/ekguru-brand-ad/scripts/assemble_veo_master.py --mode main
   ```
3. Once you review and approve the main 60s 16:9 commercial (`ekguru_ad_FINAL_60s_16x9.mp4`), I will run `--mode derivatives` to export the **9:16 Reels/Shorts vertical cut** and **15-second Teaser**.
