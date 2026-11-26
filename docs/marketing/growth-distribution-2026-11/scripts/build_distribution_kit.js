#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { loadSite } = require("../../../../tools/lib/site-data");

const ROOT = path.resolve(__dirname, "../../../..");
const OUT = path.join(ROOT, "docs/marketing/growth-distribution-2026-11");

function ensureUrlExists(urlPath) {
  const clean = urlPath.replace(/^https:\/\/ekguru\.shop\//, "").split("?")[0].split("#")[0];
  const candidates = clean === ""
    ? [path.join(ROOT, "index.html")]
    : clean.endsWith(".html")
    ? [path.join(ROOT, clean)]
    : [path.join(ROOT, clean, "index.html"), path.join(ROOT, clean + ".html")];
  const ok = candidates.some((p) => fs.existsSync(p));
  if (!ok) {
    throw new Error(`Broken URL in distribution kit: ${urlPath} (checked ${candidates.join(", ")})`);
  }
  return urlPath;
}

function escHtml(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function buildTutorKit(tutors) {
  const dir = path.join(OUT, "01_tutor_whatsapp_kit");
  fs.mkdirSync(dir, { recursive: true });

  const batches = [
    { label: "Batch 1 — Day 2 (Tutors 1–5)", items: tutors.slice(0, 5) },
    { label: "Batch 2 — Day 3 (Tutors 6–10)", items: tutors.slice(5, 10) },
    { label: "Batch 3 — Day 6 (Tutors 11–19)", items: tutors.slice(10) },
  ];

  let md = `# EkGuru — Personalized WhatsApp Share Kit for All ${tutors.length} Public Tutors

> **Privacy & Safety:** Generated strictly from public profile slugs in \`sitemap-tutors.xml\` / \`loadSite().publicTutors\`. No tutor phone numbers or email addresses are stored in this file.
> **Tracking:** Every tutor link carries \`?ref=tutor-<slug>\` so GoatCounter (\`ekguru.goatcounter.com\`) shows exactly which tutor shares bring visitors.

---
`;

  const htmlCards = [];

  batches.forEach((batch, bIdx) => {
    md += `\n## ${batch.label}\n\n`;
    batch.items.forEach((t, idx) => {
      const globalNum = bIdx === 0 ? idx + 1 : bIdx === 1 ? idx + 6 : idx + 11;
      const profileUrl = ensureUrlExists(`https://ekguru.shop/tutor/${t.id}/?ref=tutor-${t.id}`);
      const firstName = t.name.replace(/\s+[A-Z]\.?$/, "").split(/\s+/)[0];
      const subjects = (t.teaches && t.teaches.length ? t.teaches.slice(0, 3).join(", ") : "Hindi");

      const dmToTutor =
        `Namaste ${t.name} ji,\n\n` +
        `EkGuru par aapka public tutor profile live hai:\n` +
        `${profileUrl}\n\n` +
        `Ek chhota sa kaam — agar aap is link ko apne WhatsApp status, Instagram bio/story ya LinkedIn par share karein, to jo students seedha aapke link se aayenge unki enquiry seedha aapke naam se aayegi. EkGuru aapse lesson payment par koi commission nahi leta.\n\n` +
        `Aap chahein to neeche wala ready message copy karke status par laga sakte hain:\n` +
        `"I teach 1-on-1 online lessons (${subjects}) on EkGuru. Check my profile & send a trial enquiry here: ${profileUrl}"\n\n` +
        `Agar profile mein kuch update karna ho (photo, intro video, subjects ya timing), to mujhe yahin bata dijiye.\n\n` +
        `— Prakash, EkGuru`;

      const statusForTutor =
        `I teach 1-on-1 online lessons (${subjects}) on EkGuru. View my teaching profile & enquire for a lesson here: ${profileUrl}`;

      const waHref = `https://wa.me/?text=${encodeURIComponent(dmToTutor)}`;

      md += `### ${globalNum}. ${t.name} (\`/tutor/${t.id}/\`)\n`;
      md += `- **Headline:** ${t.headline || "Online Hindi Tutor"}\n`;
      md += `- **Tracked Profile Link:** \`${profileUrl}\`\n`;
      md += `- **1-Click WhatsApp Composer:** [Open in WhatsApp](${waHref})\n\n`;
      md += `**Message for Prakash to send to ${firstName} ji:**\n\`\`\`text\n${dmToTutor}\n\`\`\`\n\n`;
      md += `**Ready status/story caption for ${firstName} ji:**\n\`\`\`text\n${statusForTutor}\n\`\`\`\n\n---\n\n`;

      htmlCards.push(`
      <article class="card" data-batch="${bIdx + 1}">
        <div class="card-top">
          <label class="done-toggle">
            <input type="checkbox" data-tutor-check="${escHtml(t.id)}">
            <span><strong>#${globalNum} ${escHtml(t.name)}</strong> <small>(${escHtml(batch.label.split("—")[1].trim())})</small></span>
          </label>
          <a class="slug" href="${escHtml(profileUrl)}" target="_blank" rel="noopener">/tutor/${escHtml(t.id)}/</a>
        </div>
        <p class="headline">${escHtml(t.headline || "")}</p>
        <textarea readonly rows="8" id="msg-${escHtml(t.id)}">${escHtml(dmToTutor)}</textarea>
        <div class="actions">
          <button type="button" class="btn primary" data-copy="msg-${escHtml(t.id)}">Copy Message</button>
          <a class="btn wa" href="${escHtml(waHref)}" target="_blank" rel="noopener">Open in WhatsApp ↗</a>
        </div>
      </article>`);
    });
  });

  fs.writeFileSync(path.join(dir, "TUTOR_WHATSAPP_MESSAGES.md"), md, "utf8");

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>EkGuru Tutor WhatsApp Outreach Dashboard (Private Local Tool)</title>
<style>
  :root { color-scheme: dark; }
  body { font-family: Inter, system-ui, sans-serif; background: #0f1422; color: #f8fafc; margin: 0; padding: 32px 20px; }
  .wrap { max-width: 980px; margin: 0 auto; }
  h1 { font-size: 1.75rem; margin: 0 0 8px; }
  .sub { color: #cbd5e1; margin: 0 0 24px; line-height: 1.5; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(430px, 1fr)); gap: 18px; }
  .card { background: #181f34; border: 1px solid rgba(255,255,255,.12); border-radius: 16px; padding: 18px; }
  .card.is-done { opacity: .58; border-color: #22c55e; }
  .card-top { display: flex; justify-content: space-between; align-items: center; gap: 10px; }
  .done-toggle { display: flex; align-items: center; gap: 8px; cursor: pointer; }
  .slug { color: #fbbf24; font-size: .85rem; text-decoration: none; }
  .headline { color: #94a3b8; font-size: .88rem; margin: 8px 0 10px; }
  textarea { width: 100%; box-sizing: border-box; background: #0f1422; color: #e2e8f0; border: 1px solid rgba(255,255,255,.14); border-radius: 10px; padding: 10px; font-size: .82rem; line-height: 1.45; resize: vertical; }
  .actions { display: flex; gap: 10px; margin-top: 10px; }
  .btn { padding: 9px 14px; border-radius: 999px; border: 0; font-weight: 600; font-size: .85rem; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; }
  .btn.primary { background: #5b3df5; color: #fff; }
  .btn.wa { background: #16a34a; color: #fff; }
</style>
</head>
<body>
<div class="wrap">
  <h1>EkGuru — Tutor WhatsApp Share Dashboard (${tutors.length} Public Tutors)</h1>
  <p class="sub">Private local helper (excluded from public deploy). Tick checkboxes save in your browser so you can send Batch 1 (Day 2), Batch 2 (Day 3), and Batch 3 (Day 6) cleanly.</p>
  <div class="grid">${htmlCards.join("\n")}</div>
</div>
<script>
  document.querySelectorAll("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const el = document.getElementById(btn.dataset.copy);
      navigator.clipboard.writeText(el.value);
      const old = btn.textContent;
      btn.textContent = "Copied ✓";
      setTimeout(() => { btn.textContent = old; }, 1400);
    });
  });
  document.querySelectorAll("[data-tutor-check]").forEach((chk) => {
    const key = "ekguru:outreach:" + chk.dataset.tutorCheck;
    chk.checked = localStorage.getItem(key) === "1";
    chk.closest(".card").classList.toggle("is-done", chk.checked);
    chk.addEventListener("change", () => {
      localStorage.setItem(key, chk.checked ? "1" : "0");
      chk.closest(".card").classList.toggle("is-done", chk.checked);
    });
  });
</script>
</body>
</html>`;
  fs.writeFileSync(path.join(dir, "tutor_whatsapp_dashboard.html"), html, "utf8");
}

function buildOfficialPostsCaptions() {
  const dir = path.join(OUT, "02_official_profile_first_3_posts");
  ensureUrlExists("https://ekguru.shop/");
  ensureUrlExists("https://ekguru.shop/name-in-hindi/");
  ensureUrlExists("https://ekguru.shop/ask/do-i-need-to-learn-devanagari/");
  ensureUrlExists("https://ekguru.shop/hindi/alphabet/");

  const md = `# Official Social Profiles — First 3 Starter Posts (Ready to Upload)

Accounts linked in site schema (\`sameAs\`):
- **Instagram:** \`@ekguru.in\`
- **X (Twitter):** \`@ekguru_india\`
- **YouTube:** \`@ekguru_india\` (Community tab)
- **LinkedIn:** \`linkedin.com/company/ekguru\`
- **Facebook:** Official EkGuru page

---

## Post 1 — EkGuru Platform Introduction
**Image file:** \`post_01_ekguru_intro_1080x1350.png\`

### Instagram / Facebook / LinkedIn Caption
\`\`\`text
EkGuru is open: free self-paced courses for Hindi and Indian languages — right in your browser, with no account to create.

Available courses today:
• Hindi (structured course, script & pronunciation tools, 1-on-1 tutor profiles)
• Marathi, Gujarati, Bengali, Tamil, Telugu, Punjabi & Urdu (5 levels, lessons & quizzes)

Your progress and spaced-repetition review cards stay saved on your own device.

Start learning free:
https://ekguru.shop/?ref=social-post1

एक भाषा, एक नई दुनिया।
#LearnHindi #IndianLanguages #Devanagari #LanguageLearning #EkGuru
\`\`\`

### X (Twitter) Caption
\`\`\`text
EkGuru: free Hindi and Indian-language courses in your browser.

Hindi, Marathi, Gujarati, Bengali, Tamil, Telugu, Punjabi & Urdu — structured lessons, script guides, and quizzes. No account or sign-up wall.

Start here: https://ekguru.shop/?ref=x-post1
\`\`\`

---

## Post 2 — Free Tool Showcase (\`/name-in-hindi/\`)
**Image file:** \`post_02_name_in_hindi_tool_1080x1350.png\`

### Instagram / Facebook / LinkedIn Caption
\`\`\`text
Your name in Hindi — explained letter by letter.

Devanagari writes by sound, not by English spelling. For example, “Anna” becomes अन्ना:
1. अ (short vowel 'a')
2. न् (half-consonant 'n' with halant)
3. ना ('n' + long 'ā' vowel mark)

Type your own name to see every syllable broken down and hear it spoken aloud (free, no sign-up):
https://ekguru.shop/name-in-hindi/?ref=social-post2

#NameInHindi #Devanagari #LearnHindi #HindiScript #EkGuru
\`\`\`

### X (Twitter) Caption
\`\`\`text
How is your name written in Hindi — and why?

Devanagari writes by sound, not English spelling (“Anna” → अ + न् + ना = अन्ना).

Try your own name letter by letter (free, no account):
https://ekguru.shop/name-in-hindi/?ref=x-post2
\`\`\`

---

## Post 3 — Learner FAQ (\`Do I need to learn Devanagari?\`)
**Image file:** \`post_03_devanagari_tip_1080x1350.png\`

### Instagram / Facebook / LinkedIn Caption
\`\`\`text
“Do I need to learn Devanagari before speaking Hindi?”

You can start with spoken Hindi and Romanized text — plenty of beginners do.

Why learning the script (~2 weeks) pays off fast:
1. English spelling hides real Hindi contrasts — soft dental त (ta) vs retroflex ट (ṭa), and द (da) vs ड (ḍa).
2. Devanagari has no silent letters: once you know the vowel marks (matras), किताब (kitāb) reads just as it sounds.

Read the short honest guide:
https://ekguru.shop/ask/do-i-need-to-learn-devanagari/?ref=social-post3

Free interactive alphabet chart:
https://ekguru.shop/hindi/alphabet/?ref=social-post3
\`\`\`

### X (Twitter) Caption
\`\`\`text
“Do I need to learn Devanagari?”

You can skip it at first — but English spelling merges त (soft dental ta) and ट (retroflex ṭa) into the same “ta”. Learning the script takes ~2 weeks and fixes pronunciation early.

Full breakdown: https://ekguru.shop/ask/do-i-need-to-learn-devanagari/?ref=x-post3
\`\`\`
`;
  fs.writeFileSync(path.join(dir, "OFFICIAL_POSTS_CAPTIONS.md"), md, "utf8");
}

function buildShortsAndChannelPack() {
  const shortsDir = path.join(OUT, "03_shorts_reels_pack");
  const channelsDir = path.join(OUT, "04_channel_copy_paste_pack");
  fs.mkdirSync(shortsDir, { recursive: true });
  fs.mkdirSync(channelsDir, { recursive: true });

  // Verify every single target URL in the channel pack exists on disk!
  // Note: Indian courses live at /learn/<language>/ (NOT /languages/<code>/course/, which is only for world courses).
  const urls = [
    "https://ekguru.shop/",
    "https://ekguru.shop/learn/hindi/",
    "https://ekguru.shop/learn/marathi/",
    "https://ekguru.shop/learn/gujarati/",
    "https://ekguru.shop/learn/tamil/",
    "https://ekguru.shop/learn/telugu/",
    "https://ekguru.shop/learn/kannada/",
    "https://ekguru.shop/bengali/",
    "https://ekguru.shop/learn/punjabi/",
    "https://ekguru.shop/learn/urdu/",
    "https://ekguru.shop/name-in-hindi/",
    "https://ekguru.shop/learn/hindi/numbers/",
    "https://ekguru.shop/ask/do-i-need-to-learn-devanagari/",
    "https://ekguru.shop/find-tutors.html",
  ];
  urls.forEach(ensureUrlExists);

  const shortsMd = `# EkGuru — 3 Educational Shorts & Reels Shoot/Upload Pack (Days 11–14)

> **Ready-to-upload master videos already in repo:**
> - 15s 9:16 Teaser: \`docs/marketing/ekguru-brand-ad/06_exports/ekguru_15s_reel_shorts_teaser_9x16.mp4\`
> - 60s 9:16 Brand Reel/Short: \`docs/marketing/ekguru-brand-ad/06_exports/ekguru_60s_instagram_reel_youtube_shorts_9x16.mp4\`
>
> Below are the **3 faceless / screen-recording 25-second educational Shorts** from Section 4 of the Distribution Kit with exact titles, teleprompter scripts, on-screen text cues, and tracked pinned comments.

---

## Short 1 — Count 1 to 10 in Hindi in 25 Seconds
- **YouTube Shorts / Reels Title:** \`Count 1 to 10 in Hindi in 25 seconds (Devanagari + pronunciation)\`
- **Screen / Visual:** Open \`https://ekguru.shop/learn/hindi/numbers/\` on mobile view (or white slides with big Devanagari + digits).
- **Spoken Script (25s):**
  - \`0:00–0:03\` — "Count one to ten in Hindi with me — repeat after each one:"
  - \`0:03–0:20\` — "एक (ek — 1), दो (do — 2), तीन (teen — 3), चार (chaar — 4), पाँच (paanch — 5), छह (chhah — 6), सात (saat — 7), आठ (aath — 8), नौ (nau — 9), दस (das — 10)."
  - \`0:20–0:25\` — "All numbers up to 100 with audio are free at ekguru.shop — no sign-up."
- **Pinned Comment / Description Link:**
  \`Practice Hindi numbers 1–100 free (no sign-up): https://ekguru.shop/learn/hindi/numbers/?ref=short-numbers\`

---

## Short 2 — How Does Your Name Look in Hindi?
- **YouTube Shorts / Reels Title:** \`How your English name is written in Hindi (letter by letter)\`
- **Screen / Visual:** Screen-record typing \`Anna\`, \`David\`, and \`Sara\` live on \`https://ekguru.shop/name-in-hindi/\`.
- **Spoken Script (25s):**
  - \`0:00–0:04\` — "Ever wondered why your name looks different in Hindi script?"
  - \`0:04–0:14\` — "Hindi writes by sound, not English letters. Watch 'Anna': अ (short a) + न् (half n) + ना (long nā) = अन्ना."
  - \`0:14–0:20\` — "'David' becomes डेविड, and you can tap to hear it spoken."
  - \`0:20–0:25\` — "Try your own name free at ekguru.shop/name-in-hindi."
- **Pinned Comment / Description Link:**
  \`Write your name in Hindi letter-by-letter (free): https://ekguru.shop/name-in-hindi/?ref=short-name\`

---

## Short 3 — 3 Hindi Phrases for an Auto Ride in India
- **YouTube Shorts / Reels Title:** \`3 everyday Hindi phrases for taking an auto in India\`
- **Screen / Visual:** Big Devanagari + phonetic pronunciation cards on warm cream background.
- **Spoken Script (28s):**
  - \`0:00–0:03\` — "Three polite Hindi phrases you will actually use in an auto in India:"
  - \`0:03–0:10\` — "Number 1: भैया, यहाँ चलेंगे? — Bhaiya, yahan chalenge? ('Will you go here?')"
  - \`0:10–0:17\` — "Number 2: मीटर से चलिए — Meter se chaliye ('Please go by the meter.')"
  - \`0:17–0:24\` — "Number 3: बस यहाँ रोक दीजिए — Bas yahan rok dijiye ('Please stop right here.')"
  - \`0:24–0:28\` — "Learn everyday spoken Hindi free at ekguru.shop."
- **Pinned Comment / Description Link:**
  \`Free spoken Hindi course & phrase guides (no sign-up): https://ekguru.shop/learn/hindi/?ref=short-auto\`
`;
  fs.writeFileSync(path.join(shortsDir, "SHORTS_AND_REELS_PACK.md"), shortsMd, "utf8");

  const channelsMd = `# EkGuru — Pre-Filled Reddit, Quora, Email Outreach & GSC Pack

Every URL below has been verified against the repository build and tagged with a unique \`?ref=\` parameter for GoatCounter (\`ekguru.goatcounter.com\`).

---

## 1. Day-1 Google Search Console URL Inspection List (Copy 1 by 1)
> **Important URL Correction:** Indian-language courses live at \`/learn/<language>/\` (e.g. \`/learn/marathi/\`), NOT \`/languages/mr/course/\` (which would 404). Every URL below is verified on disk:
\`\`\`text
https://ekguru.shop/
https://ekguru.shop/learn/hindi/
https://ekguru.shop/learn/marathi/
https://ekguru.shop/learn/gujarati/
https://ekguru.shop/learn/tamil/
https://ekguru.shop/learn/telugu/
https://ekguru.shop/bengali/
https://ekguru.shop/name-in-hindi/
https://ekguru.shop/learn/hindi/numbers/
https://ekguru.shop/find-tutors.html
\`\`\`

---

## 2. City & Language Subreddit Posts (1 Post Every 3–4 Days — Never Bulk-Post!)

### Post A — \`r/pune\` (Marathi Course)
**Title:** \`Made a free Marathi course for people who moved to Pune — no login, feedback welcome\`
\`\`\`text
Namaskar r/pune,

A lot of people moving to Pune for work or college ask how to pick up everyday Marathi beyond just a few random words, without hitting a paywall or sign-up wall.

I built a free, browser-based Marathi course on EkGuru — 5 levels, 15 structured lessons, and quizzes that save progress locally in your browser (no account, no app install):
https://ekguru.shop/learn/marathi/?ref=reddit-pune

If you are a native Marathi speaker in Pune and spot any phrasing that sounds bookish instead of how Punekars actually speak, please tell me in the comments — I am actively fixing lessons based on native feedback.
\`\`\`

### Post B — \`r/hyderabad\` (Telugu Course)
**Title:** \`Built a free Telugu beginner course (5 levels, no sign-up) for newcomers to Hyderabad — would love feedback\`
\`\`\`text
Hello r/hyderabad,

For anyone who recently moved to Hyderabad and wants to learn practical Telugu (script + romanized pronunciation + quizzes) without creating an account:
https://ekguru.shop/learn/telugu/?ref=reddit-hyderabad

Everything runs in the browser and stores progress on your device only. Native Telugu speakers — if any sentence feels unnatural compared to everyday Hyderabad Telugu, please let me know so I can improve it.
\`\`\`

### Post C — \`r/chennai\` (Tamil Course)
**Title:** \`Made a free browser-based Tamil course (no login / no app) — looking for honest feedback\`
\`\`\`text
Vanakkam r/chennai,

I put together a structured free Tamil course (5 levels, 15 lessons, script + pronunciation + quizzes, saved locally in the browser with no sign-up):
https://ekguru.shop/learn/tamil/?ref=reddit-chennai

Built for people living in Chennai or learning Tamil from scratch. If any Tamil speaker has 2 minutes to glance at Level 1 and point out anything that could be clearer or more natural, I would really appreciate it.
\`\`\`

### Post D — \`r/ahmedabad\` (Gujarati Course)
**Title:** \`Free Gujarati course in the browser (no account needed) — made for beginners & newcomers\`
\`\`\`text
Kem chho r/ahmedabad,

Sharing a free self-paced Gujarati course I built on EkGuru — covers Gujarati script, everyday phrases, 5 levels and quizzes right in the browser without any login:
https://ekguru.shop/learn/gujarati/?ref=reddit-ahmedabad

Would love feedback from Gujarati speakers on any words or examples you think beginners should learn first!
\`\`\`

### Post E — \`r/kolkata\` (Bengali Hub + Course)
**Title:** \`Built a free Bengali learning hub & beginner course (no sign-up) — feedback welcome\`
\`\`\`text
Nomoshkar r/kolkata,

If anyone here has friends/partners learning Bangla or moved to Kolkata recently, I built a free Bengali topic & course hub (phrases, script, pronunciation, quizzes — no account wall):
https://ekguru.shop/bengali/?ref=reddit-kolkata

Happy to fix anything native Bangla speakers flag!
\`\`\`

### Post F — \`r/bangalore\` (Kannada Course)
**Title:** \`Made a free Kannada beginner course in the browser (no login / no app) for newcomers to Bengaluru\`
\`\`\`text
Namaskara r/bangalore,

For anyone who moved to Bengaluru and wants a structured, zero-paywall way to learn everyday Kannada (script, pronunciation, 5 levels & quizzes stored locally in your browser):
https://ekguru.shop/learn/kannada/?ref=reddit-bangalore

Native Kannada speakers — if any phrase feels textbook-stiff compared to spoken Bengaluru Kannada, please tell me so I can fix it!
\`\`\`

### Post G — \`r/hindi\` (Hindi Course + Name Tool)
**Title:** \`Free self-paced Hindi course + letter-by-letter Devanagari name tool (no login, device-only progress)\`
\`\`\`text
Namaste r/hindi,

Sharing two free resources I have been building at EkGuru for Hindi learners:
1. Full structured Hindi course & grammar/script guides (no sign-up, progress stays in localStorage):
   https://ekguru.shop/learn/hindi/?ref=reddit-hindi
2. Interactive "Your Name in Hindi" tool that breaks names down syllable-by-syllable instead of black-box transliteration:
   https://ekguru.shop/name-in-hindi/?ref=reddit-hindi

No paywalls on any of the self-study material. Honest critiques from learners and Hindi teachers are very welcome.
\`\`\`

---

## 3. Ready-to-Post Quora Answers (Days 15–19)

### Quora Answer 1 — *"Do I need to learn the Devanagari script to learn Hindi?"*
\`\`\`text
You do not have to learn Devanagari on day one if your only goal is surviving a two-week trip — spoken phrases and romanized Hindi will get you started.

However, if you want to learn Hindi beyond basic greetings, spending ~10–14 days on Devanagari saves months of confusion later for two concrete reasons:

1. English spelling hides core Hindi sound contrasts. Romanized Hindi writes both त (soft dental 'ta', tongue touching upper teeth) and ट (retroflex 'ṭa', tongue curled back) as "ta". Same for द (soft 'da') and ड (retroflex 'ḍa'). Native speakers hear these as completely different words.
2. Devanagari is phonetic. Unlike English, there are virtually no silent spelling traps — once you learn the vowel marks (matras), किताब (kitāb, "book") is pronounced the way it is written.

Full disclosure: I maintain EkGuru, where we wrote a short practical breakdown of when to learn vs. skip Devanagari (free, no login):
https://ekguru.shop/ask/do-i-need-to-learn-devanagari/?ref=quora-devanagari
\`\`\`

### Quora Answer 2 — *"What is a good free website to learn Hindi or Marathi from scratch?"*
\`\`\`text
If you want structured lessons rather than random phrase lists — without creating an account — take a look at EkGuru (disclosure: I build and maintain it).

What is free on the site right now:
• Structured Hindi lessons covering Devanagari script, pronunciation, grammar notes, numbers, and everyday dialogues: https://ekguru.shop/learn/hindi/?ref=quora-freehindi
• Full 5-level beginner courses for Marathi, Gujarati, Tamil, Telugu, Kannada, Bengali, Punjabi, and Urdu (for example Marathi here: https://ekguru.shop/learn/marathi/?ref=quora-marathi)
• Progress and spaced-repetition flashcards stay in your browser on your own device.

If you reach a stage where you want live speaking practice, there is also a public directory of independent 1-on-1 tutors, though all the courses and tools remain completely free on their own.
\`\`\`

---

## 4. Cold / Warm Outreach Emails (5 Personalized Emails on Days 22–24)

### Template 1 — University Hindi / South Asian Studies Club
**Subject:** \`Free browser-based Hindi & Indian-language tools for [University Name] students\`
\`\`\`text
Hi [Name / Committee],

I came across [Society / Department Name] at [University] and wanted to share a free resource your members learning Hindi or other Indian languages might find useful.

I run EkGuru (https://ekguru.shop/?ref=uni-outreach) — a free, no-account web platform with structured courses in Hindi, Marathi, Gujarati, Tamil, Telugu, Bengali, Punjabi, and Urdu, plus an interactive Devanagari letter-by-letter name tool (https://ekguru.shop/name-in-hindi/?ref=uni-outreach).

Nothing is behind a login wall and progress saves locally on the student's browser. If you keep a student resource list or newsletter, feel free to include it — and if your language coordinator spots any topic you wish existed, I'd be glad to build it.

Warm regards,
Prakash
Founder, EkGuru (MNIT Jaipur alumnus)
https://ekguru.shop/
\`\`\`

### Template 2 — Travel / Relocation to India Blogger ("Moving to Pune / Bangalore / Hyderabad")
**Subject:** \`Quick free language link for your [City] newcomers guide\`
\`\`\`text
Hi [Name],

Really enjoyed your practical guide on moving to [Pune / Hyderabad / Chennai]. One challenge newcomers always mention after settling in is picking up basic local [Marathi / Telugu / Tamil] without installing another subscription app.

I built a free 5-level [Language] starter course that opens directly in the browser with no sign-up:
[Insert verified course link, e.g. https://ekguru.shop/learn/marathi/?ref=blog-pune]

If you ever update your local tips section, feel free to link to it if you find it helpful for your readers!

Best,
Prakash
EkGuru — https://ekguru.shop/
\`\`\`
`;
  fs.writeFileSync(path.join(channelsDir, "CHANNEL_LAUNCH_PACK.md"), channelsMd, "utf8");
  fs.writeFileSync(
    path.join(channelsDir, "GSC_INSPECT_URLS.txt"),
    urls.slice(0, 10).join("\n") + "\n",
    "utf8"
  );
}

function buildMasterReadme(tutorCount) {
  const md = `# EkGuru — Growth Plan & Distribution Kit Execution Package (Nov 2026)

> **PRIVATE INTERNAL DIRECTORY (\`docs/marketing/\`)** — Automatically excluded from the public \`_site\` build by \`tools/build-public-dist.py\` and enforced by \`tools/test-public-surface.mjs\`.

## 1. Saved Master Documents
- [\`GROWTH-PLAN-2026-11-24.md\`](./GROWTH-PLAN-2026-11-24.md) — Audit & 30-day honest growth strategy
- [\`DISTRIBUTION-KIT-2026-11-24.md\`](./DISTRIBUTION-KIT-2026-11-24.md) — Copy-paste distribution playbook

## 2. Repository Fixes Completed (Growth Plan Section 6)
- **6(a) Claim-Safe Open Graph Cover (\`images/og-cover.jpg\` & \`images/og-cover.webp\`, \`1200×630\`):** Replaced the old cover (which contained *"Verified native tutors"* / *"From $3"* / *"7 languages"* and a tutor photo) with a crisp, honest, vector-rendered EkGuru brand cover aligned 100% with site disclosures. Editable SVG saved in [\`00_og_cover/ekguru_og_cover_1200x630.svg\`](./00_og_cover/ekguru_og_cover_1200x630.svg).
- **6(b) Stale Time/Days Pages Fixed:** Fixed \`learning_code()\` in \`tools/apply-ultra.py\` for \`days-and-months-in-<lang>\` and rebuilt \`days-and-months-in-{gujarati,kannada,telugu,urdu}/index.html\` via \`tools/build-time-pages-bodies.py\`. Both \`build-time-pages-bodies.py --check\` and \`apply-ultra.py --check\` now pass with 0 stale pages.
- **6(c) Crawler-Visible Static Tutor Cards on \`find-tutors.html\`:** Extended \`tools/build-home-tutors.js\` so \`#find-list\` in \`find-tutors.html\` ships all ${tutorCount} active public tutor cards in static HTML for first-pass crawlers while keeping \`tools/ultra/contract.py\` (index + canonical freeze) and live JS filtering 100% intact.
- **6(d) Weekly Workflows (\`live-guard.yml\` & \`course-health.yml\`):** Updated \`tools/weekly-guard.sh\` so Cloudflare \`cf-mitigated: challenge\` responses on datacenter runner IPs verify local file invariants and log \`⚠️ CF_CHALLENGE\` instead of masking real failures, while real HTTP/SSL/policy errors still exit 1. Updated \`tools/course-health.py\` to auto-ensure the \`course-health\` label and update issues via GitHub REST API.
- **6(e) Page-Specific \`og:image:alt\` & \`twitter:image:alt\`:** Updated \`tools/build-phase7-pages.py\` template and replaced hardcoded *"EkGuru — free, self-paced Hindi learning"* across \`start/\`, \`languages/\`, all 29 \`languages/*/index.html\` hubs, \`find-tutors.html\`, and \`tutor/index.html\` with each page's actual title without altering \`robots\` or \`canonical\`.
- **6(f) PR #63:** Verified already closed on GitHub.
- **6(g) Commission Honesty:** Kept truthful disclosure (\`EkGuru does not collect tutor-lesson payments in this release\` on \`find-tutors.html\`) with zero fabricated marketplace/commission claims.

## 3. Ready-to-Use Distribution Assets
1. **[\`01_tutor_whatsapp_kit/\`](./01_tutor_whatsapp_kit/)**
   - \`TUTOR_WHATSAPP_MESSAGES.md\` — Personalized messages + \`?ref=tutor-<slug>\` links for all **${tutorCount} live public tutors** (grouped into Day 2, Day 3, and Day 6 batches).
   - \`tutor_whatsapp_dashboard.html\` — Open locally in any browser for 1-click **Copy Message** & **Open in WhatsApp** buttons with tick-box progress tracking.
2. **[\`02_official_profile_first_3_posts/\`](./02_official_profile_first_3_posts/)**
   - \`post_01_ekguru_intro_1080x1350.png\` (+ \`.svg\`)
   - \`post_02_name_in_hindi_tool_1080x1350.png\` (+ \`.svg\`)
   - \`post_03_devanagari_tip_1080x1350.png\` (+ \`.svg\`)
   - \`OFFICIAL_POSTS_CAPTIONS.md\` — Ready captions for Instagram, X, LinkedIn, and Facebook.
3. **[\`03_shorts_reels_pack/SHORTS_AND_REELS_PACK.md\`](./03_shorts_reels_pack/SHORTS_AND_REELS_PACK.md)**
   - 3 complete 25-second Shorts/Reels scripts (\`1–10 Hindi Numbers\`, \`Your Name in Hindi\`, \`3 Auto Ride Phrases\`) + links to the rendered \`9:16\` master videos in \`docs/marketing/ekguru-brand-ad/06_exports/\`.
4. **[\`04_channel_copy_paste_pack/\`](./04_channel_copy_paste_pack/)**
   - \`CHANNEL_LAUNCH_PACK.md\` — Pre-filled Reddit posts (\`r/pune\`, \`r/hyderabad\`, \`r/chennai\`, \`r/ahmedabad\`, \`r/kolkata\`, \`r/hindi\`), Quora answers, and university/blogger outreach emails.
   - \`GSC_INSPECT_URLS.txt\` — Exact 10 URLs to submit in Google Search Console on Day 1.
`;
  fs.writeFileSync(path.join(OUT, "README.md"), md, "utf8");
}

function main() {
  const site = loadSite();
  const tutors = site.publicTutors;
  buildTutorKit(tutors);
  buildOfficialPostsCaptions();
  buildShortsAndChannelPack();
  buildMasterReadme(tutors.length);
  console.log(`Built complete distribution kit for ${tutors.length} public tutors in ${path.relative(ROOT, OUT)}`);
}

main();
