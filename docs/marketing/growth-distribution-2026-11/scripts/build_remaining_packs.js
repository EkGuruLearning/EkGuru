#!/usr/bin/env node
/**
 * Builds the remaining copy-paste & tracking packs for Sections 3, 4, 5, 7, 8, 9, and 10
 * of DISTRIBUTION-KIT-2026-11-24.md and GROWTH-PLAN-2026-11-24.md, verifying every single
 * https://ekguru.shop/... URL against the repository filesystem before writing.
 */
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "../../../..");
const KIT_DIR = path.resolve(__dirname, "..");

function ensureUrlExists(urlStr) {
  const u = new URL(urlStr);
  if (u.hostname !== "ekguru.shop") {
    throw new Error(`Unexpected hostname in ${urlStr}`);
  }
  const rel = u.pathname.replace(/^\/+/, "");
  if (rel === "") {
    if (!fs.existsSync(path.join(ROOT, "index.html"))) throw new Error("Missing root index.html");
    return urlStr;
  }
  const direct = path.join(ROOT, rel);
  const asIndex = path.join(ROOT, rel.replace(/\/+$/, ""), "index.html");
  if (fs.existsSync(direct) && fs.statSync(direct).isFile()) return urlStr;
  if (fs.existsSync(asIndex) && fs.statSync(asIndex).isFile()) return urlStr;
  throw new Error(`404 URL caught before writing kit: ${urlStr}`);
}

function verifyAllUrlsInText(text, label) {
  const matches = text.match(/https:\/\/ekguru\.shop[^\s)>\]"'`*]*/g) || [];
  let count = 0;
  for (const raw of matches) {
    const cleaned = raw.replace(/[.,;:!?]+$/, "");
    if (cleaned.includes("<") || cleaned.includes("[")) continue;
    ensureUrlExists(cleaned);
    count++;
  }
  return count;
}

function writeVerified(relPath, content) {
  const fullPath = path.join(KIT_DIR, relPath);
  const checked = verifyAllUrlsInText(content, relPath);
  fs.mkdirSync(path.dirname(fullPath), { recursive: true });
  fs.writeFileSync(fullPath, content, "utf8");
  console.log(`wrote ${relPath} (${checked} ekguru.shop URLs verified)`);
}

// ---------------------------------------------------------------------------
// 02_official_profile_first_3_posts/OFFICIAL_POSTS_CAPTIONS.md (updated w/ 4-slide carousel)
// ---------------------------------------------------------------------------
const officialPostsMd = `# Official Profiles — Bio Setup & First 3 Starter Posts (Section 8)

Target official profiles:
- **Instagram:** \`@ekguru.in\` — Bio link: \`https://ekguru.shop/?ref=ig\`
- **YouTube:** \`@ekguru_india\` — Channel link: \`https://ekguru.shop/?ref=yt\`
- **X (Twitter):** \`@ekguru_india\` — Bio link: \`https://ekguru.shop/?ref=x\`
- **Facebook Page:** EkGuru — Page website: \`https://ekguru.shop/?ref=fb\`
- **LinkedIn:** \`company/ekguru\` — Website: \`https://ekguru.shop/?ref=li\`

**Recommended Bio Line (all platforms):**
> Free Hindi & Indian-language courses, alphabet & browser practice tools. No account needed. एक भाषा, एक नई दुनिया।

---

## Post 1 — EkGuru Introduction (Single Image \`1080×1350\`)
- **Image file:** \`post_01_ekguru_intro_1080x1350.png\` (editable SVG: \`post_01_ekguru_intro_1080x1350.svg\`)

### Instagram / Facebook / LinkedIn Caption
We built EkGuru for anyone who wants to learn Hindi or another Indian language step by step — without creating an account, handing over an email address, or installing an app.

What is live right now on https://ekguru.shop/?ref=social-post1 :
- Structured Hindi path + 30-day daily routine (\`20 min/day\`, saved in your browser)
- Regional Indian language courses: Marathi, Gujarati, Tamil, Telugu, Bengali, Punjabi & Urdu
- 13 browser practice tools: Devanagari alphabet chart, numbers 1–100, flashcards, printable worksheets & name-in-Hindi explorer
- Independent tutors listed with their stated lesson details (confirm availability & terms directly with the tutor)

Learn Indian Languages. Connect with India.
एक भाषा, एक नई दुनिया।

### X / Twitter Version
EkGuru is live: free Hindi & Indian-language courses + 13 browser tools (alphabet, numbers, flashcards, worksheets, name-in-Devanagari).

No account or email required — open and start learning:
https://ekguru.shop/?ref=x-post1

---

## Post 2 — Tool Spotlight: Your Name in Hindi (\`1080×1350\`)
- **Image file:** \`post_02_name_in_hindi_tool_1080x1350.png\` (editable SVG: \`post_02_name_in_hindi_tool_1080x1350.svg\`)

### Instagram / Facebook / LinkedIn Caption
One of the easiest ways to start reading Devanagari is with a word you already know by heart: your own name.

Type any name on our free browser tool and see:
1. How it is written in Devanagari script
2. Every vowel mark (matra) and consonant cluster explained letter by letter

Try yours free (no login):
https://ekguru.shop/name-in-hindi/?ref=social-post2

### X / Twitter Version
How does your name look in Devanagari — and what does each letter actually do?

Type any name and see it broken down letter by letter in your browser (free, no sign-up):
https://ekguru.shop/name-in-hindi/?ref=x-post2

---

## Post 3 — 4-Slide Swipeable Carousel: “Do I Really Need to Learn Devanagari?” (\`1080×1350\` × 4)
- **Slide 1 (Cover):** \`post_03_devanagari_tip_1080x1350.png\`
- **Slide 2 (Why Romanised Hindi Hits a Wall):** \`post_03_slide_02_vowel_length_1080x1350.png\`
- **Slide 3 (The Logical Sound Grid):** \`post_03_slide_03_sound_grid_1080x1350.png\`
- **Slide 4 (Free 2-Week Plan + Links):** \`post_03_slide_04_two_week_plan_1080x1350.png\`

### Instagram / LinkedIn / Facebook Carousel Caption
“Can I learn Hindi using only English letters?”

You can for your first few greetings — and then romanised spelling starts hiding the exact vowel lengths (\`kal\` vs \`kāl\`) and aspirated consonants (\`kāl\` vs \`khāl\`) you need to be understood clearly.

The good news: Devanagari is organised like a logical sound table, not a random list of shapes. Twenty steady minutes a day for about two weeks is enough to start reading signs, menus, and beginner lessons.

Swipe through all 4 slides, then use both free resources:
- Full guide: https://ekguru.shop/ask/do-i-need-to-learn-devanagari/?ref=social-post3
- Interactive alphabet & audio chart: https://ekguru.shop/hindi/alphabet/?ref=social-post3

### X / Twitter Thread / Single Post Version
Do you really need to learn Devanagari for Hindi?

Romanised Hindi works for week 1, then hides vowel length (\`kal\` vs \`kāl\`) and breathy consonants (\`kāl\` vs \`khāl\`). Because Devanagari is a phonetic sound grid, ~2 steady weeks opens up real reading:
https://ekguru.shop/ask/do-i-need-to-learn-devanagari/?ref=x-post3
`;

// ---------------------------------------------------------------------------
// 03_shorts_reels_pack/SHORTS_AND_REELS_PACK.md (3 rendered MP4s + all 15 scripts)
// ---------------------------------------------------------------------------
const shortsMd = `# YouTube Shorts & Instagram Reels Pack — 3 Rendered MP4s + All 15 Scripts (Section 4)

Repeatable 25–30 second vertical (\`1080×1920\`, \`9:16\`) format:
**Hook question (0–3s) → 3–10 crisp script + pronunciation cards → 1-line takeaway + free browser link in bio.**

> **Review rule before posting:** Have one native speaker or EkGuru tutor listen to any recorded voiceover once before publishing. Every third video, invite an active EkGuru tutor to voice or co-post the Reel and credit their profile link \`https://ekguru.shop/tutor/<slug>/?ref=tutor-<slug>\`.

---

## Part A — Ready-to-Upload Rendered \`1080×1920\` MP4 Videos (Days 11–14 Sprint)

All three starter Shorts are already rendered in this folder at \`1080×1920\` (\`30fps\`, H.264 + AAC royalty-free Indian-fusion instrumental bed, HarfBuzz-verified Devanagari typography, zero missing glyphs). You can upload them directly or record a 25-second voiceover on top inside YouTube Shorts / Instagram Reels using the spoken script below each file:

### Rendered Video 1 — \`short_01_count_1_to_10_hindi_9x16.mp4\` (\`27.0s\`)
- **Cover thumbnail:** \`short_01_cover_1080x1920.png\`
- **Target URL:** https://ekguru.shop/learn/hindi/numbers/?ref=yt-shorts
- **Voiceover / Spoken Script (optional mic overlay):**
  - \`0–3s\`: “Learn to count from 1 to 10 in Hindi in twenty seconds.”
  - \`3–23s\`: “1 — ek (एक). 2 — do (दो). 3 — teen (तीन). 4 — chaar (चार). 5 — paanch (पाँच). 6 — chhah (छह). 7 — saat (सात). 8 — aath (आठ). 9 — nau (नौ). 10 — das (दस).”
  - \`23–27s\`: “Numbers all the way to 100 with audio are free on EkGuru — no login, link in bio.”
- **Title / Caption:** Count 1 to 10 in Hindi in 20 Seconds (१ से १०) | Free 1–100 audio chart: https://ekguru.shop/learn/hindi/numbers/?ref=yt-shorts

### Rendered Video 2 — \`short_02_your_name_in_hindi_9x16.mp4\` (\`24.0s\`)
- **Cover thumbnail:** \`short_02_cover_1080x1920.png\`
- **Target URL:** https://ekguru.shop/name-in-hindi/?ref=yt-shorts
- **Voiceover / Spoken Script:**
  - \`0–3.5s\`: “How does your name look in Hindi — and how do the letters fit together?”
  - \`3.5–9s\`: “Anna becomes अन्ना — अ, half-न, plus ना.”
  - \`9–14.5s\`: “David becomes डेविड — डे, वि, ड.”
  - \`14.5–19.5s\`: “Maya becomes माया — मा plus या.”
  - \`19.5–24s\`: “Type your own name free in your browser — no sign-up. Link in bio.”
- **Title / Caption:** How Does Your Name Look in Hindi? (Devanagari Breakdown) | Try yours free: https://ekguru.shop/name-in-hindi/?ref=yt-shorts

### Rendered Video 3 — \`short_03_auto_ride_3_phrases_9x16.mp4\` (\`25.0s\`)
- **Cover thumbnail:** \`short_03_cover_1080x1920.png\`
- **Target URL:** https://ekguru.shop/learn/hindi/?ref=yt-shorts
- **Voiceover / Spoken Script:**
  - \`0–3.5s\`: “Three polite Hindi phrases for every auto-rickshaw ride in India.”
  - \`3.5–9.3s\`: “One: Kitne paise? (कितने पैसे?) — How much is the fare?”
  - \`9.3–15.1s\`: “Two: Meter se chaliye (मीटर से चलिए) — Please go by the meter.”
  - \`15.1–20.9s\`: “Three: Yahan rok dijiye (यहाँ रोक दीजिए) — Please stop right here.”
  - \`20.9–25s\`: “More everyday Hindi and regional Indian language lessons are free on EkGuru — link in bio.”
- **Title / Caption:** 3 Polite Hindi Phrases for Every Auto Ride in India | Free course: https://ekguru.shop/learn/hindi/?ref=yt-shorts

---

## Part B — Complete Scripts for All 12 Follow-Up Hooks (Weeks 3–4 Rotation)

### Script 4 — Hindi Days of the Week in 20 Seconds
- **Hook (0–3s):** “All 7 days of the week in Hindi — notice how every one ends in *-vaar*!”
- **On-Screen Cards (3–23s):**
  - सोमवार · *Somvaar* · Monday
  - मंगलवार · *Mangalvaar* · Tuesday
  - बुधवार · *Budhvaar* · Wednesday
  - गुरुवार · *Guruvaar* · Thursday
  - शुक्रवार · *Shukravaar* · Friday
  - शनिवार · *Shanivaar* · Saturday
  - रविवार · *Ravivaar* · Sunday
- **Close + Link:** “Full time & calendar guide free on EkGuru: https://ekguru.shop/learn/hindi/?ref=yt-shorts”

### Script 5 — 5 Natural Ways to Say Thank You (and Respond) in Hindi
- **Hook (0–3s):** “Textbook Hindi says *Dhanyavaad* — here is how people thank each other across everyday situations.”
- **Cards (3–24s):**
  1. धन्यवाद · *Dhanyavaad* — Polite formal “Thank you”
  2. शुक्रिया · *Shukriya* — Warm everyday conversational “Thanks”
  3. बहुत धन्यवाद · *Bahut dhanyavaad* — “Thank you very much”
  4. आपकी बड़ी मेहरबानी · *Aapki badi meharbaani* — “Very kind of you”
  5. कोई बात नहीं · *Koi baat nahin* — “No problem / You’re welcome”
- **Close + Link:** “Read when to use each: https://ekguru.shop/ask/how-to-say-thank-you-in-hindi/?ref=yt-shorts”

### Script 6 — Why Hindi Has 3 Words for “You” (*Aap*, *Tum*, *Tu*)
- **Hook (0–3s):** “Use the wrong word for ‘you’ in Hindi and you can sound way too formal — or accidentally rude.”
- **Cards (3–24s):**
  1. आप (*Aap*) + हैं — Respectful: elders, strangers, shopkeepers, work, anyone new (**safe default!**)
  2. तुम (*Tum*) + हो — Familiar: close friends, younger relatives, peers
  3. तू (*Tu*) + है — Very intimate (childhood best friend, prayer, or can sound blunt if misused)
- **Close + Link:** “When in doubt, always start with *Aap*. Free beginner Hindi path: https://ekguru.shop/learn/hindi/?ref=yt-shorts”

### Script 7 — How to Introduce Yourself in Hindi in 3 Lines
- **Hook (0–3s):** “Introduce yourself naturally in Hindi with just three sentences.”
- **Cards (3–24s):**
  1. नमस्ते, मेरा नाम [Name] है। · *Namaste, mera naam [Name] hai.* (“Hello, my name is…”)
  2. मैं [City/Country] से हूँ। · *Main [Place] se hoon.* (“I am from…”)
  3. मैं थोड़ी हिंदी सीख रहा / रही हूँ। · *Main thodi Hindi seekh raha/rahi hoon.* (“I’m learning a little Hindi.”)
- **Close + Link:** “Full pronunciation guide: https://ekguru.shop/ask/how-to-introduce-yourself-in-hindi/?ref=yt-shorts”

### Script 8 — Hindi or Urdu: What Is the Actual Difference?
- **Hook (0–3s):** “If you learn spoken Hindi, can you understand spoken Urdu too?”
- **Cards (3–24s):**
  1. **Everyday speech:** Core verbs, pronouns, and grammar are shared — street conversation overlaps heavily.
  2. **Script:** Hindi uses left-to-right **Devanagari**; Urdu uses right-to-left **Nastaliq** (Perso-Arabic).
  3. **Formal vocabulary:** News & literature draw more from Sanskrit in Hindi and Persian/Arabic in Urdu.
- **Close + Link:** “Side-by-side breakdown: https://ekguru.shop/ask/hindi-or-urdu-which-to-learn/?ref=yt-shorts”

### Script 9 — 10 Hindi Words English Borrowed (You Already Know Them!)
- **Hook (0–3s):** “You already speak at least 10 Hindi/Indian-origin words in everyday English.”
- **Rapid Cards (3–24s):**
  - जंगल (*jangal* → jungle) · शैंपू (*chāmpo* → shampoo) · बंगला (*banglā* → bungalow) · पजामा (*pājāmā* → pyjamas) · चाय (*chāy* → chai) · गुरु (*guru*) · कर्म (*karma*) · अवतार (*avatār*) · बरामदा (*barāmdā* → veranda) · चटनी (*chatnī* → chutney)
- **Close + Link:** “Build real sentences next: https://ekguru.shop/daily-hindi/?ref=yt-shorts”

### Script 10 — What Does “Ji” (जी) Actually Mean in India?
- **Hook (0–3s):** “Why do Hindi speakers add the tiny word *ji* (जी) to names, yes, and greetings?”
- **Cards (3–24s):**
  1. **After a name/role:** *Sharma ji*, *Didi ji*, *Master ji* — instant warmth & respect (gender-neutral!)
  2. **Polite “Yes”:** *Haan ji* (हाँ जी) or simply *Ji* — much softer than a bare “haan”
  3. **Polite “Pardon?”:** *Ji?* with a gentle rising tone = “Sorry, could you repeat that?”
- **Close + Link:** “Practice everyday polite Hindi free: https://ekguru.shop/learn/hindi/?ref=yt-shorts”

### Script 11 — Marathi: 5 Phrases for the Market in Pune or Mumbai
- **Hook (0–3s):** “Moved to Pune or Mumbai? Try these 5 Marathi phrases at your local market.”
- **Cards (3–24s):**
  1. नमस्कार · *Namaskaar* — Hello
  2. हे कितीला आहे? · *He kitīlā āhe?* — How much is this?
  3. थोडं कमी करा ना · *Thoda kamī karā nā* — Please reduce it a little
  4. मला मराठी थोडं थोडं येतं · *Malā Marāthī thoda thoda yeta* — I know a little Marathi
  5. धन्यवाद · *Dhanyavaad* — Thank you
- **Close + Link:** “Free English + Hindi + Marathi course: https://ekguru.shop/learn/marathi/?ref=yt-shorts”

### Script 12 — Gujarati: 5 Warm Phrases for a New Neighbour in Ahmedabad or Surat
- **Hook (0–3s):** “New in Gujarat? Five Gujarati phrases your neighbours will love hearing.”
- **Cards (3–24s):**
  1. કેમ છો? · *Kem chho?* — How are you?
  2. મજામાં! · *Majāmā!* — Doing great!
  3. મારું નામ … છે · *Māru nāma … chhe* — My name is …
  4. હું થોડું ગુજરાતી શીખું છું · *Hu thodu Gujarātī shīkhu chhu* — I’m learning a little Gujarati
  5. આભार · *Ābhār* — Thank you
- **Close + Link:** “Free structured Gujarati course: https://ekguru.shop/learn/gujarati/?ref=yt-shorts”

### Script 13 — Tamil: 5 Phrases for Your First Week in Chennai
- **Hook (0–3s):** “Just moved to Chennai? Start with these 5 everyday spoken Tamil phrases.”
- **Cards (3–24s):**
  1. வணக்கம் · *Vanakkam* — Hello / respectful greeting
  2. எப்படி இருக்கீங்க? · *Eppadi irukkeenga?* — How are you?
  3. எவ்வளவு? · *Evvalavu?* — How much?
  4. கொஞ்சம் தமிழ் தெரியும் · *Konjam Tamil theriyum* — I know a little Tamil
  5. நன்றி · *Nandri* — Thank you
- **Close + Link:** “Free step-by-step Tamil course (no login): https://ekguru.shop/learn/tamil/?ref=yt-shorts”

### Script 14 — Telugu: 5 Everyday Phrases for Hyderabad
- **Hook (0–3s):** “Living in Hyderabad? Five Telugu phrases that immediately build warmth.”
- **Cards (3–24s):**
  1. నమస్కారం · *Namaskāram* — Hello
  2. ఎలా ఉన్నారు? · *Elā unnāru?* — How are you? (polite)
  3. ఇది ఎంత? · *Idi entha?* — How much is this?
  4. నాకు కొంచెం తెలుగు వచ్చు · *Nāku konchem Telugu vacchu* — I know a little Telugu
  5. ధన్యవాదాలు · *Dhanyavādālu* — Thank you
- **Close + Link:** “Free structured Telugu course: https://ekguru.shop/learn/telugu/?ref=yt-shorts”

### Script 15 — Bengali: 5 Everyday Phrases for Kolkata
- **Hook (0–3s):** “Shifted to Kolkata or visiting Bengal? Five Bengali phrases to use right away.”
- **Cards (3–24s):**
  1. নমস্কার · *Nomoshkar* — Hello
  2. কেমন আছেন? · *Kemon achhen?* — How are you? (polite)
  3. এটার দাম কত? · *Etar daam koto?* — What is the price of this?
  4. আমি অল্প বাংলা শিখছি · *Ami olpo Bangla shikhchhi* — I am learning a little Bengali
  5. ধন্যবাদ · *Dhonnobad* — Thank you
- **Close + Link:** “Free Bengali topic hub & practice: https://ekguru.shop/bengali/?ref=yt-shorts”
`;

// ---------------------------------------------------------------------------
// 05_quora_and_whatsapp_pack/QUORA_ANSWERS_PACK.md (Section 3)
// ---------------------------------------------------------------------------
const quoraMd = `# Quora Ready-to-Adapt Answers Pack (Section 3)

**Posting Rules (from \`DISTRIBUTION-KIT-2026-11-24.md\`):**
1. Pick questions that are **6+ months old** with **few detailed answers** so your answer stays near the top.
2. Keep answers **120–240 words**, adapt slightly to the exact wording of the question, and put **at most ONE link at the very end**.
3. Always disclose honestly (*“I run EkGuru”* / *“my site”*) — never pretend to be a random third party.
4. Never claim “verified”, “native”, “best”, or “commission-free” unless written on the page you link to.

---

## Answer 1 — “Can I learn Hindi in 3 months?”
Yes, you can reach genuinely useful conversational Hindi in three months if you practice most days — as long as you define “learn” realistically. Three months will not let you follow fast movie dialogue or formal news broadcasts without subtitles, so anyone promising full fluency in 90 days is overselling. What three steady months *can* give you is everyday survival and social Hindi: introducing yourself, ordering food, bargaining politely, taking an auto, asking directions, and holding ten-minute conversations with patient speakers.

A routine that works reliably:
1. **Weeks 1–2:** Spend 20 minutes a day learning Devanagari vowels, matras, and the main consonant rows so you stop relying on inconsistent English spellings.
2. **Weeks 3–8:** Learn high-frequency sentence frames (*mujhe … chahiye*, *… kahan hai?*, *main … kar raha/rahi hoon*) and say every line out loud.
3. **Weeks 9–12:** Have one short live conversation a week so your ears adjust to real speed.

I run a free 30-day starter path built around 20-minute browser sessions (no account needed): https://ekguru.shop/ask/can-i-learn-hindi-in-3-months/?ref=quora

---

## Answer 2 — “How long does it take to learn Hindi for an English speaker?”
For an English speaker studying steadily (around 30–45 minutes most days plus occasional speaking practice), Hindi usually breaks down into three honest milestones:

- **First 2–3 weeks:** Reading Devanagari slowly. Because Devanagari is phonetic — no silent letters and consistent vowel signs — the script looks intimidating on day one and becomes surprisingly logical by week two.
- **4 to 6 months:** Everyday conversational comfort — handling travel, family small talk, food, time, numbers, and basic past/present/future sentences, even though noun gender and postpositions (*ne*, *ko*, *se*) will still trip you up sometimes.
- **1 to 2 years:** Comfortable, natural fluency across varied topics and faster native speech.

Two things shorten the timeline noticeably: learning Devanagari early instead of staying on romanised text, and saying phrases out loud from week one so retroflex vs dental consonants (*t/d* with tongue curled vs at the teeth) feel physical rather than theoretical.

I wrote a fuller breakdown with study-hour estimates on my site, EkGuru: https://ekguru.shop/ask/how-long-to-learn-hindi/?ref=quora

---

## Answer 3 — “Is Hindi hard for English speakers?”
Hindi is medium-difficulty for English speakers — easier in some ways than European languages with huge irregular verb tables, and trickier in three specific places:

1. **Word order (SOV):** English says *“I drink chai”*; Hindi puts the verb at the end: *“Main chai peeta/peeti hoon”* (*I chai drink*). Your brain adapts to this within a couple of weeks.
2. **Four-way consonant contrasts:** Hindi distinguishes unaspirated vs breathy consonants (*pal* = moment vs *phal* = fruit) and dental vs retroflex sounds. Listening and repeating out loud matters much more than silent reading.
3. **Grammatical gender & postpositions:** Every noun is masculine or feminine, and words like “in/on/to” come *after* the noun rather than before it.

What makes Hindi friendlier than people expect is **Devanagari**: once you learn the vowel marks, words are pronounced the way they are written.

I maintain a free Hindi learning site (EkGuru) and put together a practical guide on what feels hard at first and how to tackle it: https://ekguru.shop/ask/is-hindi-hard-to-learn/?ref=quora

---

## Answer 4 — “Do I really need to learn Devanagari script to speak Hindi?”
Strictly speaking, you can learn a handful of travel phrases using romanised Hindi (*Namaste*, *Kitne paise?*, *Dhanyavaad*). If you are visiting India for five days, romanised phrases are plenty.

If you want to learn conversational Hindi beyond a week or two, skipping Devanagari usually slows you down more than learning it:
- People spell romanised Hindi inconsistently (*kal*, *kaal*, and *khaal* are three completely different words that casual English spelling blurs together).
- Good dictionaries, graded readers, street signs, food labels, and WhatsApp messages use Devanagari.
- Unlike English spelling, Devanagari is arranged systematically by how your mouth forms each sound — throat, palate, roof of mouth, teeth, lips — and has no silent letters.

At roughly 20 minutes a day, most adult learners can sound out words comfortably in about two weeks. I run EkGuru, where we published a detailed guide and free browser alphabet chart (no login): https://ekguru.shop/ask/do-i-need-to-learn-devanagari/?ref=quora

---

## Answer 5 — “How can I teach my child Hindi while living abroad (US / UK / Canada / Australia)?”
With heritage learners growing up in an English-dominant environment, consistency beats long weekend cramming almost every time:

1. **Under age 7 — keep it spoken and playful:** Songs, short stories, naming foods at dinner, and five minutes of playful Hindi at bedtime work much better than grammar worksheets. Even if your child replies in English at first, hearing steady Hindi builds comprehension.
2. **Ages 7+ — add tiny visual wins:** Have them write family members’ names in Devanagari, count steps or snacks in Hindi, and do 10–15 minutes of interactive reading/listening three or four times a week.
3. **Separate encouragement from correction:** Gently recast mistakes by repeating the natural sentence back rather than stopping them mid-thought.

If you eventually want structured outside practice, EkGuru (a language site I run) has free browser tools with no login plus a directory of independent Hindi tutors showing their stated rates — always confirm schedule and lesson terms directly with the tutor before booking: https://ekguru.shop/ask/hindi-for-kids-how-to-start/?ref=quora

---

## Answer 6 — “Should I learn Hindi or Urdu?”
If your goal is **everyday spoken conversation**, learning the basics of one gives you most of the spoken foundation of the other. Core pronouns, verb tenses, numbers, and daily street expressions overlap heavily across northern India, Pakistan, and diaspora communities.

Choose based on **where and how you will read and listen**:
- **Pick Hindi first** if you want to read **Devanagari** (left-to-right, phonetic, also used for Marathi), travel or work in India, or move toward formal Hindi media, signs, and literature (which draw more vocabulary from Sanskrit).
- **Pick Urdu first** if your family, literature, poetry (*ghazals*), or community uses the **Nastaliq** script (right-to-left Perso-Arabic) and formal vocabulary rooted in Persian and Arabic.

Many learners start with spoken core grammar + Devanagari and later learn the Urdu script (or vice versa) once the spoken foundation is solid. I wrote a calm, practical comparison on my project EkGuru here: https://ekguru.shop/ask/hindi-or-urdu-which-to-learn/?ref=quora

---

## Answer 7 — “What is the fastest free way to learn basic Marathi / Tamil / Telugu / Gujarati after moving to a new Indian city?”
Most newcomers make the mistake of starting with formal literary grammar instead of the **30 everyday transactions** you actually repeat in your first month: greeting security guards and neighbours, auto/cab directions, buying vegetables and groceries, numbers, and telling people politely *“I am still learning, please speak slowly.”*

What helps fastest if you already know English (and especially if you also know Hindi):
1. **Compare English + Hindi + the local language side by side** so you spot shared roots and where word endings differ.
2. **Learn polite request endings first** (like *-ā* / *karā nā* in Marathi, *-unga* in Tamil, *-andi* in Telugu) — locals appreciate polite effort immediately, even with a small vocabulary.
3. **Practice 15–20 minutes daily** on one topic at a time (numbers, food, directions, time).

I built free browser courses for Marathi, Tamil, Telugu, Gujarati, Bengali, and Punjabi on EkGuru (no account required) — for example, here is the Marathi course: https://ekguru.shop/learn/marathi/?ref=quora
`;

// ---------------------------------------------------------------------------
// 05_quora_and_whatsapp_pack/WHATSAPP_TELEGRAM_HINGLISH_PACK.md (Section 5)
// ---------------------------------------------------------------------------
const whatsappHinglishMd = `# WhatsApp Status & City Relocation Groups Pack — Hinglish (Section 5)

> **Important scope rule from \`GROWTH-PLAN-2026-11-24.md\` Section 3:**
> Do **not** promote \`/learn/kannada/\` (Bengaluru) or \`/learn/malayalam/\` yet while those courses are marked \`noindex\` and awaiting completion/native review. Focus city relocation posts on **Pune/Mumbai (Marathi), Hyderabad (Telugu), Chennai (Tamil), Ahmedabad/Vadodara/Surat (Gujarati), Kolkata (Bengali), and Chandigarh/Punjab (Punjabi)**.

---

## 1. Founder Personal WhatsApp Status / Broadcast / Family & Alumni Groups

**Hinglish Version:**
> Namaste! Maine **EkGuru** banaya hai — Hindi aur 7 Indian languages (Marathi, Gujarati, Tamil, Telugu, Bengali, Punjabi, Urdu) step-by-step free seekhne ke liye. Koi login, account ya email nahi chahiye, seedha browser mein chalta hai.
>
> Agar aapke kisi dost, colleague ya NRI family ke bachchon ko kaam aaye to zaroor share kijiyega:
> https://ekguru.shop/?ref=wa
>
> Kuch bhi galat lage ya koi suggestion ho to seedha mujhe message karke batayein, main turant theek kar dunga.

**Short 2-Line WhatsApp Status Caption (pair with \`post_01_ekguru_intro_1080x1350.png\`):**
> Free Hindi & Indian-language courses + 13 browser tools (no login/app needed). Feedback welcome: https://ekguru.shop/?ref=wa-status

---

## 2. City-Specific Relocation & Newcomer WhatsApp / Telegram / Facebook Groups

### 2.1 Pune & Mumbai Newcomers — Marathi (\`?ref=wa-marathi\`)
> Dosto, agar Pune ya Mumbai shift hue ho aur rozmarra ki basic Marathi seekhni hai (auto, market, neighbours, office small talk), to maine ek free structured course banaya hai jahan har shabd **English, Hindi aur Marathi** teeno mein saath-saath dikhta hai — koi sign-up ya app download nahi chahiye:
> https://ekguru.shop/learn/marathi/?ref=wa-marathi
> Main khud EkGuru bana raha hoon — batao kaunse roz ke situations aur add karoon?

### 2.2 Hyderabad Newcomers — Telugu (\`?ref=wa-telugu\`)
> Hi everyone — agar aap haal hi mein Hyderabad shift hue hain aur basic spoken Telugu seekhna chahte hain (cab/auto, shops, polite greetings, numbers), to maine EkGuru par ek free step-by-step Telugu course banaya hai (English + Hindi + Telugu side by side, bina kisi login ke):
> https://ekguru.shop/learn/telugu/?ref=wa-telugu
> Mera apna project hai — honest feedback zaroor dijiyega!

### 2.3 Chennai Newcomers — Tamil (\`?ref=wa-tamil\`)
> Friends, Chennai mein naye aaye logon ke liye maine EkGuru par ek free beginner Tamil course rakha hai — pronunciation, everyday phrases, topic chapters aur practice quizzes seedha browser mein (no account/email needed):
> https://ekguru.shop/learn/tamil/?ref=wa-tamil
> Main is site ko build kar raha hoon; agar koi everyday Chennai situation missing lage to zaroor batayein.

### 2.4 Ahmedabad / Gandhinagar / Vadodara / Surat — Gujarati (\`?ref=wa-gujarati\`)
> Namaste dosto! Gujarat shift hue logon ke liye maine EkGuru par ek free step-by-step Gujarati course banaya hai — har word English, Hindi aur Gujarati mein compare karke seekh sakte hain, bina kisi login ke:
> https://ekguru.shop/learn/gujarati/?ref=wa-gujarati
> Feedback doge to aur behtar bana paunga!

### 2.5 Kolkata Newcomers — Bengali (\`?ref=wa-bengali\`)
> Hi dosto — agar Kolkata shift hue ho aur roz ki basic Bangla (greetings, numbers, market, directions, polite conversation) free mein seekhna chahte ho, to mera yeh browser-based Bengali hub dekho (no login required):
> https://ekguru.shop/bengali/?ref=wa-bengali
> Main EkGuru chala raha hoon — kuch bhi improve karna ho to seedha batana!

### 2.6 Chandigarh / Mohali / Punjab — Punjabi (\`?ref=wa-punjabi\`)
> Sat Sri Akal / Namaste dosto! Punjabi aur Gurmukhi basics step-by-step seekhne ke liye maine EkGuru par ek free course aur numbers/practice tools banaye hain (account ya email nahi chahiye):
> https://ekguru.shop/learn/punjabi/?ref=wa-punjabi
> Dekh kar batayiye kaisa laga!

### 2.7 NRI Family & Cousins Group — Kids’ Name in Hindi + 30-Day Path (\`?ref=wa-nri\`)
> Namaste! Agar ghar mein bachche ya cousins abroad Hindi seekh rahe hain, to yeh chhota free browser tool unhe bahut pasand aata hai — apna naam type karo aur Devanagari mein har akshar ka matlab dekho (koi login ya email nahi maangta):
> https://ekguru.shop/name-in-hindi/?ref=wa-nri
> Aur roz 15–20 min practice ke liye free 30-day path bhi hai: https://ekguru.shop/daily-hindi/?ref=wa-nri
`;

// ---------------------------------------------------------------------------
// 06_backlink_outreach_pack/OUTREACH_EMAILS_AND_QUERIES.md + outreach_tracker.csv
// ---------------------------------------------------------------------------
const outreachMd = `# Backlink & Resource-Page Outreach Pack (Section 7 — Week 4: 3 Emails / Day)

**Rules for high reply rates & zero spam flags:**
1. Send **3 genuinely personalised emails per day** from your real inbox — always reference the exact page title or recent article/video you looked at.
2. Reply within **24 hours** to anyone who writes back.
3. Send **at most ONE polite follow-up** after **7 days** if there is no reply — then stop.
4. Never buy links, exchange paid guest posts, or make claims not stated on the site.
5. For **Email 2 (Hindi schools / temple classes / NRI parent groups)**, you already have the ready-to-attach printable sheet in this folder:
   - \`ekguru_hindi_class_home_practice_sheet_A4.png\` (and editable \`.svg\`)

---

## 1. Google Search Queries to Build Your Prospect List (15 Minutes = 30 Prospects)

Run these directly in Google Search and add matching pages with active external resource lists to \`outreach_tracker.csv\`:

1. **University South Asian / Hindi Language Centres:**
   - \`"Hindi" "resources" "language" site:.edu\`
   - \`"South Asian languages" "online resources" "Hindi" site:.edu\`
   - \`"Hindi" "useful links" university department\`
   - \`"Devanagari" "practice" "links" site:.ac.uk\`
2. **Sunday Hindi Schools, Bal Vihar / Temple Classes & Heritage Parent Groups (US, UK, Canada, Australia, UAE, Singapore):**
   - \`"Hindi school" "resources" parents\`
   - \`"Hindi classes" Sunday children "practice" resources\`
   - \`"heritage language" Hindi parents resources\`
3. **Independent Language Bloggers, Polyglot Newsletters & Relocation Guides:**
   - \`"learn Hindi" blog "free resources"\`
   - \`"Indian languages" learning resources list\`
   - \`"moving to Pune" OR "moving to Chennai" OR "moving to Hyderabad" learn local language\`

---

## 2. Email Templates (Personalise \`[Bracketed Fields]\` Before Sending!)

### Email 1 — University Department / Language Resource Page (\`?ref=email-edu\`)

**Subject:** Free browser-based Hindi & Indian-language tools for your \`[Department / Page Title]\` list

Hello \`[Professor / Coordinator Name]\`,

I came across \`[University Name]\`’s Hindi language resources page (\`[Exact URL of Their Resource Page]\`) and noticed your links for beginner script and vocabulary practice.

I run **EkGuru** (https://ekguru.shop/learn/hindi/?ref=email-edu), an independent free site for learning Hindi and seven regional Indian languages (Marathi, Gujarati, Tamil, Telugu, Bengali, Punjabi, and Urdu). Everything runs directly in the browser with no student account, login, or tracking cookies:
- Interactive Devanagari alphabet & audio chart: https://ekguru.shop/hindi/alphabet/?ref=email-edu
- 13 browser practice tools (numbers 1–100, flashcards, printable worksheets): https://ekguru.shop/toolbox/?ref=email-edu

If you feel any of these would be useful for self-study alongside your classes, a link on your resources page would mean a great deal to a small project. And if you or your instructors ever spot a linguistic mistake, please tell me — I will fix it right away.

Warm regards,
Prakash
EkGuru — https://ekguru.shop

---

### Email 2 — Sunday Hindi School / Temple Class / NRI Parent Coordinator (\`?ref=email-school\`)
*(Tip: You can attach \`ekguru_hindi_class_home_practice_sheet_A4.png\` directly or offer it first as below.)*

**Subject:** Free at-home Hindi practice tools for \`[School / Program Name]\` students (no login)

Hello \`[Coordinator / Teacher Name]\`,

I’m Prakash, writing from Jaipur. I saw \`[School / Community Name]\`’s Hindi program for children and wanted to share a free set of home-practice tools I built that requires **no student login, email, or app download** (so kids can practice safely on any family tablet or laptop):

- **30-Day Daily Hindi Path** (~15–20 min/day, saved locally in the browser): https://ekguru.shop/daily-hindi/?ref=email-school
- **Devanagari Alphabet & Numbers 1–100 + Printable Worksheets:** https://ekguru.shop/toolbox/?ref=email-school
- **Name in Devanagari Explorer** (kids love seeing their own name explained letter by letter): https://ekguru.shop/name-in-hindi/?ref=email-school

Parents in weekly classes often ask for simple, distraction-free weekday practice. Would you be open to mentioning it in your parent newsletter or class resources? I also put together a clean one-page printable At-Home Hindi Practice Sheet (happy to send it over or customise the header for your class at no cost).

Thank you for teaching and keeping the language alive,
Prakash
EkGuru — https://ekguru.shop

---

### Email 3 — Language Blogger / Newsletter Writer / YouTuber (\`?ref=email-creator\`)

**Subject:** Quick note on your \`[Exact Post / Video Title]\` + a free Hindi toolbox

Hi \`[First Name]\`,

I just read/watched your piece on \`[Exact Post/Video Title — add 1 genuine sentence about a specific point they made]\`.

I’m building **EkGuru** (https://ekguru.shop/toolbox/?ref=email-creator), a small free Hindi and Indian-language site with a 30-day browser study plan and 13 lightweight tools — including a letter-by-letter Name-in-Devanagari converter (https://ekguru.shop/name-in-hindi/?ref=email-creator) and printable practice sheets with zero sign-up walls.

If you ever update your Hindi resource recommendations or test free browser tools, I’d be glad if you took a look — and I genuinely welcome critique on anything you’d improve.

Thanks,
Prakash
EkGuru — https://ekguru.shop

---

### Single 7-Day Polite Follow-Up (Send Once Only, Reply in Same Thread)

**Subject:** Re: \`[Original Subject]\`

Hello \`[Name]\`,

Just floating this once in case my note last week got buried in a busy inbox — no rush at all, and no worries if it isn’t a fit for \`[Organization / Site Name]\` right now.

If you ever want the one-page printable Hindi practice sheet or spot anything we should add to https://ekguru.shop/toolbox/?ref=email-followup, just let me know.

Best wishes,
Prakash
`;

const outreachCsv = `date_sent,segment,organization,contact_name,contact_email,target_page_url,template_used,followup_due_date,followup_sent,status,backlink_live_url,notes
2026-12-08,university,"Example University South Asia Center","Dr. Example","example@university.edu","https://example.edu/hindi/resources",Email 1 (.edu),2026-12-15,no,draft,"","Replace this sample row with your first 3 real prospects"
`;

// ---------------------------------------------------------------------------
// 07_submissions_and_30day_tracker/DIRECTORY_AND_ARTICLE_SUBMISSIONS.md (Section 9)
// ---------------------------------------------------------------------------
const submissionsMd = `# One-Time Free Directory Submissions & IndieHackers / Dev.to Article (Section 9)

All copy below obeys EkGuru’s strict accuracy policy: zero invented user numbers, zero unverified claims, and honest disclosure of what runs locally in the browser.

---

## 1. Bing Webmaster Tools (2 Minutes — Day 1)
1. Open \`https://www.bing.com/webmasters\` and sign in.
2. Choose **Import from Google Search Console** → select \`https://ekguru.shop/\`.
3. Verify that \`https://ekguru.shop/sitemap-index.xml\` appears under **Sitemaps** (submit it manually if not).
4. Why it matters: powers **Bing, DuckDuckGo, Yahoo, Ecosia, and ChatGPT Search** discovery automatically.

---

## 2. AlternativeTo.net Listing (“Free Alternative to Hindi Learning Apps”)
- **App / Site Name:** EkGuru
- **Official Website:** \`https://ekguru.shop/\`
- **Pricing / License:** Free (No account required; optional community support; independent tutor listings arranged directly with tutors)
- **Platforms:** Web / Browser (Desktop & Mobile, offline-capable PWA caching for saved lessons)
- **Alternatives To (tag 3–5):** Duolingo, Memrise, Ling App, Drops, Mondly
- **Short Tagline (≤ 100 chars):**
  > Free browser-based Hindi & Indian-language courses, flashcards, printable sheets, and script tools.
- **Full Description (Copy-Paste):**
  > EkGuru is a free browser-based platform for learning Hindi and regional Indian languages (including Marathi, Gujarati, Tamil, Telugu, Bengali, Punjabi, and Urdu) alongside core world-language courses.
  >
  > Everything works without creating an account, handing over an email address, or installing a mobile app:
  > - Structured CEFR-inspired course rungs with dialogues, grammar notes, and self-check quizzes
  > - A 30-day daily Hindi routine (~20 minutes/day) with local browser spaced-repetition review
  > - 13 lightweight browser tools: Devanagari alphabet audio chart, numbers 1–100 reader, printable worksheet generator with answer keys, and a letter-by-letter Name-in-Devanagari converter
  > - Optional directory of independent language tutors displaying their stated lesson details

---

## 3. Hacker News — “Show HN” Submission (Focus on \`/toolbox/\` & Zero-Account Architecture)
- **Title:** \`Show HN: EkGuru – 13 browser-only Hindi and Indian-language tools (no login)\`
- **URL:** \`https://ekguru.shop/toolbox/?ref=show-hn\`
- **Founder First Comment (post immediately after submitting):**
  > Hi HN — I built EkGuru from Jaipur because most material for Indian regional languages (like Marathi, Gujarati, Tamil, Telugu, Bengali, and Punjabi) alongside Hindi is either locked behind mobile app sign-up walls or scattered across unstructured videos.
  >
  > A few technical choices that might be interesting to folks here:
  > - **Zero accounts / zero cookies:** Spaced-repetition flashcards (\`SM-2\`-lite), daily streak tracking, and JSON progress backups live entirely in \`localStorage\`, and analytics uses cookieless GoatCounter.
  > - **Offline-capable static pages:** Built with plain HTML/CSS/JS generators so pages work on low-bandwidth mobile connections and pin cleanly via a bounded Service Worker.
  > - **Print-first CSS sheets:** Every worksheet page (\`https://ekguru.shop/learn/hindi/practice/worksheets/\`) generates real printable practice sheets + answer keys that strip all site chrome on \`Ctrl+P\`.
  > - **Script breakdown:** \`https://ekguru.shop/name-in-hindi/\` explains Devanagari vowel matras and consonant conjuncts letter by letter.
  >
  > Would love honest feedback on anything that feels clunky, broken, or missing for learners.

---

## 4. Product Hunt Launch Draft (Schedule After First 5–10 Active Learners Give Feedback)
- **Name:** EkGuru
- **Tagline (≤ 60 chars):** \`Free Hindi & Indian-language courses + 13 browser tools\`
- **Links:**
  - Website: \`https://ekguru.shop/?ref=producthunt\`
  - Toolbox: \`https://ekguru.shop/toolbox/?ref=producthunt\`
- **Maker Comment:**
  > Hey Product Hunt! I’m Prakash from Jaipur, and I’m building EkGuru — a calm, zero-login web platform to learn Hindi and Indian regional languages (Marathi, Gujarati, Tamil, Telugu, Bengali, Punjabi, Urdu).
  >
  > Whether you moved to a new Indian city and want everyday local phrases, are raising kids abroad who want to read their name in Devanagari (\`https://ekguru.shop/name-in-hindi/\`), or want a structured 20-minute daily Hindi plan (\`https://ekguru.shop/daily-hindi/\`), you can open any page and start immediately without creating an account. Tell me what language or tool we should improve next!

---

## 5. Ready-to-Publish Article for IndieHackers & Dev.to

**Title:** Why I Built a Free Hindi & Indian-Language Site with 13 Browser Tools (and Zero Sign-Up Walls)
**Tags:** \`webdev\`, \`indiandev\`, \`edtech\`, \`showdev\`

### Article Body (Copy-Paste & Adapt)
If you move to Pune, Hyderabad, Chennai, Ahmedabad, or Kolkata for work — or if you grow up outside India wanting to speak Hindi with your grandparents — you run into a strange gap on the web.

Major global apps spend most of their energy on Spanish, French, or Japanese. For Indian languages, learners often bounce between sign-up-gated mobile apps that teach unnatural sentences, expensive courses, or random videos with inconsistent romanised spelling.

So I started building **EkGuru** (https://ekguru.shop/?ref=devto) with three constraints from day one:

#### 1. Open a URL, start learning in 2 seconds (no login wall)
Nothing kills curiosity faster than an onboarding funnel asking for your email, age, daily notification permission, and credit card trial before showing you a single letter of Devanagari.

On EkGuru, every tool and lesson is a plain, fast static web page:
- Want to see how your name works in Devanagari? Open https://ekguru.shop/name-in-hindi/?ref=devto, type a name, and see every vowel mark (*matra*) and consonant cluster broken down immediately.
- Need numbers 1 to 100 with native script digits and pronunciation? Open https://ekguru.shop/learn/hindi/numbers/?ref=devto.
- Want a structured 20-minute daily habit? https://ekguru.shop/daily-hindi/?ref=devto saves your progress and spaced-repetition flashcards directly in your browser’s \`localStorage\` — with one-click JSON export/import if you switch devices.

#### 2. Side-by-side English + Hindi + Regional Indian Languages
Millions of people relocating within India already know English and some Hindi, and want to learn **Marathi, Gujarati, Tamil, Telugu, Bengali, or Punjabi** for everyday life — speaking to neighbours, auto drivers, and local shopkeepers. Showing English, Hindi, and the target regional language side by side helps learners spot shared roots and polite verb endings much faster.

#### 3. Real printable worksheets (just press \`Ctrl+P\`)
Parents and Sunday Hindi school teachers still love paper practice. Instead of locking PDFs behind email capture forms, our worksheet pages (https://ekguru.shop/learn/hindi/practice/worksheets/?ref=devto) generate fresh practice sheets in the browser and use dedicated \`@media print\` rules so pressing Print outputs *only* the clean worksheet and answer key.

#### What I learned the hard way: building pages != discovery
Building static generators is addictive for an engineer — it’s easy to keep polishing features inside your repo while almost nobody knows the site exists. Right now I’ve frozen new auto-generated page templates completely for 30 days to focus on real human distribution: talking to learners, helping in language communities, working with the independent tutors listed on https://ekguru.shop/find-tutors.html?ref=devto, and fixing whatever real visitors find confusing.

If you’re learning Hindi or another Indian language (or building lightweight static educational tools), take a look at the toolbox here and tell me honestly what you’d improve:
https://ekguru.shop/toolbox/?ref=devto
`;

// ---------------------------------------------------------------------------
// 07_submissions_and_30day_tracker/30_DAY_EXECUTION_TRACKER.md (Section 10)
// ---------------------------------------------------------------------------
const tracker30Md = `# EkGuru 30-Day Growth Sprint — Daily Execution Tick-List (Section 10)

Daily time budget: **30–40 minutes/day**.
Hard rule during all 30 days: **0 new auto-generated pages** — measure, index, distribute, and double down on what sends real GoatCounter visits.

---

## Week 1 — Measurement, Indexing & Tutor Network Activation

- [ ] **Day 1 (30–40 min) — Owner Setup & Live Verification**
  - [ ] Merge PR #76 so the claim-safe \`images/og-cover.{jpg,webp}\`, static 19-tutor \`find-tutors.html\`, rebuilt \`days-and-months-in-*\` pages, and \`og:image:alt\` fixes deploy to \`https://ekguru.shop/\`.
  - [ ] Run Facebook Sharing Debugger + LinkedIn Post Inspector on \`https://ekguru.shop/\` → click **Scrape Again** to clear cached OG previews.
  - [ ] Open \`https://ekguru.goatcounter.com\` → Settings → enable viewing & record baseline 7-day visits/referrers/pages below.
  - [ ] Open Google Search Console → **URL Inspection** → \`https://ekguru.shop/\` → **Test Live URL**. *(If blocked by Cloudflare, turn off Cloudflare Bot Fight Mode immediately before anything else!)*
  - [ ] Submit **only** \`https://ekguru.shop/sitemap-index.xml\` under GSC Sitemaps.
  - [ ] Request indexing in GSC for first 3 URLs from \`04_channel_copy_paste_pack/GSC_INSPECT_URLS.txt\`:
    - \`https://ekguru.shop/\`
    - \`https://ekguru.shop/learn/hindi/\`
    - \`https://ekguru.shop/name-in-hindi/\`
  - [ ] Import GSC into **Bing Webmaster Tools** (\`07_submissions_and_30day_tracker/DIRECTORY_AND_ARTICLE_SUBMISSIONS.md\` §1).

- [ ] **Day 2 (30 min) — Tutor WhatsApp Batch 1 (Tutors 1–5) + GSC**
  - [ ] Open \`01_tutor_whatsapp_kit/tutor_whatsapp_dashboard.html\` (or \`TUTOR_WHATSAPP_MESSAGES.md\`) and send personalised WhatsApp outreach + share blurb to **Batch 1 (Tutors 1–5)**.
  - [ ] Request indexing in GSC for 3 URLs: \`/toolbox/\`, \`/daily-hindi/\`, \`/hindi/alphabet/\`.
  - [ ] Test one \`?ref=test\` link yourself and verify it appears in GoatCounter Referrers.

- [ ] **Day 3 (35 min) — Tutor Batch 2 (Tutors 6–10) + Publish First 3 Official Social Posts**
  - [ ] Send personalised WhatsApp messages to **Batch 2 (Tutors 6–10)**.
  - [ ] Update bios & publish **Post 1, Post 2, and Post 3 (4-slide Devanagari carousel)** from \`02_official_profile_first_3_posts/\` across Instagram (\`ekguru.in\`), X (\`@ekguru_india\`), YouTube Community (\`@ekguru_india\`), Facebook Page, and LinkedIn (\`company/ekguru\`).
  - [ ] Request indexing in GSC for 3 URLs: \`/learn/marathi/\`, \`/learn/tamil/\`, \`/learn/telugu/\`.

- [ ] **Day 4 (30 min) — Warm-Up Helpful Reddit Comments (No Self-Post Yet) + GSC**
  - [ ] Post **3 genuinely helpful comments** in \`r/Hindi\` / \`r/LanguageLearning\` (use \`04_channel_copy_paste_pack/CHANNEL_LAUNCH_PACK.md\` comment templates only where directly relevant; disclose *“I run that site”* whenever linking).
  - [ ] Request indexing in GSC for 3 URLs: \`/learn/gujarati/\`, \`/bengali/\`, \`/learn/punjabi/\`.

- [ ] **Day 5 (35 min) — First Reddit Tool Post + 2 Quora Answers**
  - [ ] Publish the \`r/Hindi\` browser-tools post from \`04_channel_copy_paste_pack/CHANNEL_LAUNCH_PACK.md\` (check subreddit self-promo rules first).
  - [ ] Post **Answers 1 & 2** on Quora from \`05_quora_and_whatsapp_pack/QUORA_ANSWERS_PACK.md\`.
  - [ ] Request indexing in GSC for \`/find-tutors.html\`, \`/hindi-tutor/\`, \`/ask/do-i-need-to-learn-devanagari/\`.

- [ ] **Day 6 (30 min) — Tutor Batch 3 (Remaining Tutors 11–19) + Founder WhatsApp Status**
  - [ ] Send personalised WhatsApp messages to **Batch 3 (Tutors 11–19)** so all 19 live tutors have their \`?ref=tutor-<slug>\` link.
  - [ ] Post Founder Hinglish WhatsApp Status & personal alumni/friends message from \`05_quora_and_whatsapp_pack/WHATSAPP_TELEGRAM_HINGLISH_PACK.md\` §1.

- [ ] **Day 7 — WEEK 1 SCORECARD CHECK**
  - GoatCounter 7-day visits: \`________\` | Top 3 referrers: \`________________________\`
  - GSC Indexed pages: \`________\` | Discovered not indexed: \`________\` | Crawled not indexed: \`________\`
  - Tutors who shared on status/story (\`?ref=tutor-*\` clicks): \`________ / 19\`

---

## Week 2 — Audience 1 City Communities (Relocation Learners) & Quora

- [ ] **Day 8:** Read \`r/pune\` rules → post/comment Marathi relocation thread (\`?ref=reddit-pune\`) + 1 Quora answer (Answer 3) + Pune WhatsApp/Telegram relocation group message.
- [ ] **Day 9:** Read \`r/hyderabad\` rules → Telugu relocation post/comment (\`?ref=reddit-hyd\`) + 1 Quora answer (Answer 4) + AlternativeTo.net listing (\`07_...\` §2).
- [ ] **Day 10:** Read \`r/chennai\` rules → Tamil relocation post/comment (\`?ref=reddit-chennai\`) + 1 Quora answer (Answer 5).
- [ ] **Day 11:** Upload **Short 1** (\`03_shorts_reels_pack/short_01_count_1_to_10_hindi_9x16.mp4\`) to YouTube Shorts, Instagram Reels & Facebook Reels + 1 Quora answer (Answer 6).
- [ ] **Day 12:** Reply to every Reddit/Quora/YouTube comment + 1 helpful \`r/ABCDesis\` or NRI parent group comment (no spam) + 1 Quora answer (Answer 7).
- [ ] **Day 13:** Upload **Short 2** (\`03_shorts_reels_pack/short_02_your_name_in_hindi_9x16.mp4\`) to Shorts & Reels + share in family WhatsApp status.
- [ ] **Day 14 — FIRST 14-DAY DECISION REVIEW (Apply Growth Plan Section 5 Rules!)**
  - GoatCounter 14-day total visits: \`________\`
  - **Winning channel #1 (DOUBLE in Weeks 3–4):** \`________________________\`
  - **Zero-visit channel after 3 tries (DROP for now):** \`________________________\`

---

## Week 3 — Short Video Cadence + Backlink Outreach Launch

- [ ] **Day 15:** Upload **Short 3** (\`03_shorts_reels_pack/short_03_auto_ride_3_phrases_9x16.mp4\`) + send first **3 personalised outreach emails** (\`06_backlink_outreach_pack/\`, log in \`outreach_tracker.csv\`).
- [ ] **Day 16:** Send **3 outreach emails** (Hindi schools / NRI parent groups with \`ekguru_hindi_class_home_practice_sheet_A4.png\` ready) + double-down action on Winning Channel #1.
- [ ] **Day 17:** Record/post **Script 4** (*Hindi days of the week*) from \`03_shorts_reels_pack/SHORTS_AND_REELS_PACK.md\` + send **3 outreach emails**.
- [ ] **Day 18:** Publish Dev.to / IndieHackers article (\`07_...\` §5) + send **3 outreach emails**.
- [ ] **Day 19:** Co-create **Script 6 or 7** with an active EkGuru tutor (credit their \`/tutor/<slug>/\` profile!) + send **3 outreach emails**.
- [ ] **Day 20:** Submit **Show HN** (\`/toolbox/?ref=show-hn\`, \`07_...\` §3) when you have 1–2 hours free to reply to technical comments + send **3 outreach emails**.
- [ ] **Day 21:** Weekly check — reply to outreach responses within 24h; log GoatCounter referrers.

---

## Week 4 — Regional Shorts, Outreach Follow-Ups & Day-28 Index Audit

- [ ] **Day 22:** Post **Script 11** (*Marathi 5 market phrases*) + Gujarat subreddit/community post (\`?ref=reddit-guj\`) + **3 new outreach emails** + 7-day single follow-up on Day 15 emails.
- [ ] **Day 23:** Send **3 new outreach emails** + 7-day follow-up on Day 16 emails + helpful Reddit/Quora reply.
- [ ] **Day 24:** Post **Script 13 or 14** (*Tamil Chennai* or *Telugu Hyderabad*) + Kolkata community post (\`?ref=reddit-kol\` → \`https://ekguru.shop/bengali/?ref=reddit-kol\`) + **3 new outreach emails**.
- [ ] **Day 25:** Send **3 new outreach emails** + 7-day follow-ups + invite second tutor for a 25s phrase Reel.
- [ ] **Day 26:** Post **Script 12 or 15** (*Gujarati* or *Bengali*) + **3 new outreach emails**.
- [ ] **Day 27:** Follow up gently with any tutors who haven’t shared their profile yet; spotlight active tutors on official stories.
- [ ] **Day 28 — SECOND MAJOR REVIEW (GSC Indexing Ratio Check)**
  - GSC Indexed count: \`________\` vs Total Not Indexed: \`________\`
  - *Decision gate:* If **>70% of submitted/discovered pages remain “Not indexed”** after 4 weeks of real external links, prepare the Phase-2 plan to consolidate/noindex thin template pages down to the ~150 strongest pages based on real GSC & GoatCounter data.
- [ ] **Day 29:** Prepare Product Hunt launch page (\`07_...\` §4) if 5–10 real users have given feedback.
- [ ] **Day 30 — 30-DAY SPRINT SUMMARY**
  - Total 30-day GoatCounter visits: \`________\`
  - Top 5 landing pages: \`________________________________________________\`
  - Top 3 referrers: \`________________________________________________\`
  - Backlinks earned: \`________\` | Tutor inquiries/bookings: \`________\`
  - Bring these 4 numbers into your next planning session to set Month 2 priorities (including completing Kannada A1/A2 with a native reviewer for Bengaluru relocation demand).
`;

// ---------------------------------------------------------------------------
// Updated Master README.md
// ---------------------------------------------------------------------------
const masterReadme = `# EkGuru Growth Plan & Complete Distribution Execution Kit (Nov 2026)

**PRIVATE INTERNAL PACKAGE** — Stored under \`docs/marketing/growth-distribution-2026-11/\`, which is automatically excluded from public deployment (\`_site\`) by \`tools/build-public-dist.py\` and verified clean of personal contact data by \`node tests/regression/test-public-surface.mjs\`.

Every \`https://ekguru.shop/...\` URL across this entire kit has been programmatically checked against the repository tree so zero \`404\` links exist.

---

## Folder Map (100% of \`GROWTH-PLAN-2026-11-24.md\` & \`DISTRIBUTION-KIT-2026-11-24.md\`)

| Folder / File | What’s Inside | Status |
|---|---|---|
| \`GROWTH-PLAN-2026-11-24.md\` & \`DISTRIBUTION-KIT-2026-11-24.md\` | Original strategy & distribution source documents archived privately | Complete |
| \`00_og_cover/\` | Master SVG + PNG (\`1200×630\`) for the claim-safe site-wide \`images/og-cover.{jpg,webp}\` | Live in repo |
| \`01_tutor_whatsapp_kit/\` | \`TUTOR_WHATSAPP_MESSAGES.md\` + interactive copy-paste \`tutor_whatsapp_dashboard.html\` for all **19 public tutors** (Day 2 / Day 3 / Day 6 batches, \`?ref=tutor-<slug>\`, zero private contact fields) | Ready to send |
| \`02_official_profile_first_3_posts/\` | **Post 1** (\`post_01_ekguru_intro_1080x1350.png\`), **Post 2** (\`post_02_name_in_hindi_tool_1080x1350.png\`), **Post 3 Complete 4-Slide Devanagari Carousel** (\`post_03_devanagari_tip_1080x1350.png\` + \`post_03_slide_02..04_*_1080x1350.png\`), editable SVGs, and \`OFFICIAL_POSTS_CAPTIONS.md\` | Visually verified |
| \`03_shorts_reels_pack/\` | **3 Ready-to-Upload \`1080×1920\` (\`9:16\`) MP4 Videos** (\`short_01_count_1_to_10_hindi_9x16.mp4\`, \`short_02_your_name_in_hindi_9x16.mp4\`, \`short_03_auto_ride_3_phrases_9x16.mp4\`), cover PNGs, plus \`SHORTS_AND_REELS_PACK.md\` with **all 15 scripts** (Hindi + Marathi, Gujarati, Tamil, Telugu, Bengali) | Encoded & verified |
| \`04_channel_copy_paste_pack/\` | \`CHANNEL_LAUNCH_PACK.md\` (Reddit city & language posts + comment templates + NRI communities) and \`GSC_INSPECT_URLS.txt\` (priority URLs for Google Search Console) | URL-verified |
| \`05_quora_and_whatsapp_pack/\` | \`QUORA_ANSWERS_PACK.md\` (7 full 150–230 word answers mapped to real \`/ask/...\` URLs) + \`WHATSAPP_TELEGRAM_HINGLISH_PACK.md\` (Founder status + 7 city relocation messages) | Ready to paste |
| \`06_backlink_outreach_pack/\` | \`OUTREACH_EMAILS_AND_QUERIES.md\` (Google search queries + 3 email templates + 7-day follow-up), \`outreach_tracker.csv\`, and **printable A4 handout** \`ekguru_hindi_class_home_practice_sheet_A4.{svg,png}\` for Hindi schools & parent groups | Ready to send |
| \`07_submissions_and_30day_tracker/\` | \`DIRECTORY_AND_ARTICLE_SUBMISSIONS.md\` (Bing Webmaster Tools, AlternativeTo, Show HN, Product Hunt, full Dev.to / IndieHackers article) + \`30_DAY_EXECUTION_TRACKER.md\` (Day 1 → Day 30 checklist & review scorecards) | Ready to run |
| \`scripts/\` | Deterministic generators (\`build_visual_assets.py\`, \`build_shorts_and_printables.py\`, \`build_distribution_kit.js\`, \`build_remaining_packs.js\`) | Reproducible |

---

## URL Corrections Caught & Applied Automatically

Two draft URL patterns in the original notes would have hit \`404\` on production and were corrected everywhere in this kit:
1. \`/learn/hindi/alphabet/\` → **https://ekguru.shop/hindi/alphabet/**
2. Regional Indian courses (\`/languages/<code>/course/\` only exists for world languages) →
   - Marathi: **https://ekguru.shop/learn/marathi/**
   - Gujarati: **https://ekguru.shop/learn/gujarati/**
   - Tamil: **https://ekguru.shop/learn/tamil/**
   - Telugu: **https://ekguru.shop/learn/telugu/**
   - Punjabi: **https://ekguru.shop/learn/punjabi/**
   - Urdu: **https://ekguru.shop/learn/urdu/**
   - Bengali: **https://ekguru.shop/bengali/**
   *(Note: \`/learn/kannada/\` and \`/learn/malayalam/\` exist on disk as \`noindex\` drafts — excluded from active promotion per \`GROWTH-PLAN-2026-11-24.md\` Section 3 until native review is complete.)*
`;

writeVerified("02_official_profile_first_3_posts/OFFICIAL_POSTS_CAPTIONS.md", officialPostsMd);
writeVerified("03_shorts_reels_pack/SHORTS_AND_REELS_PACK.md", shortsMd);
writeVerified("05_quora_and_whatsapp_pack/QUORA_ANSWERS_PACK.md", quoraMd);
writeVerified("05_quora_and_whatsapp_pack/WHATSAPP_TELEGRAM_HINGLISH_PACK.md", whatsappHinglishMd);
writeVerified("06_backlink_outreach_pack/OUTREACH_EMAILS_AND_QUERIES.md", outreachMd);
writeVerified("06_backlink_outreach_pack/outreach_tracker.csv", outreachCsv);
writeVerified("07_submissions_and_30day_tracker/DIRECTORY_AND_ARTICLE_SUBMISSIONS.md", submissionsMd);
writeVerified("07_submissions_and_30day_tracker/30_DAY_EXECUTION_TRACKER.md", tracker30Md);
writeVerified("README.md", masterReadme);
