# One-Time Free Directory Submissions & IndieHackers / Dev.to Article (Section 9)

All copy below obeys EkGuru’s strict accuracy policy: zero invented user numbers, zero unverified claims, and honest disclosure of what runs locally in the browser.

---

## 1. Bing Webmaster Tools (2 Minutes — Day 1)
1. Open `https://www.bing.com/webmasters` and sign in.
2. Choose **Import from Google Search Console** → select `https://ekguru.shop/`.
3. Verify that `https://ekguru.shop/sitemap-index.xml` appears under **Sitemaps** (submit it manually if not).
4. Why it matters: powers **Bing, DuckDuckGo, Yahoo, Ecosia, and ChatGPT Search** discovery automatically.

---

## 2. AlternativeTo.net Listing (“Free Alternative to Hindi Learning Apps”)
- **App / Site Name:** EkGuru
- **Official Website:** `https://ekguru.shop/`
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

## 3. Hacker News — “Show HN” Submission (Focus on `/toolbox/` & Zero-Account Architecture)
- **Title:** `Show HN: EkGuru – 13 browser-only Hindi and Indian-language tools (no login)`
- **URL:** `https://ekguru.shop/toolbox/?ref=show-hn`
- **Founder First Comment (post immediately after submitting):**
  > Hi HN — I built EkGuru from Jaipur because most material for Indian regional languages (like Marathi, Gujarati, Tamil, Telugu, Bengali, and Punjabi) alongside Hindi is either locked behind mobile app sign-up walls or scattered across unstructured videos.
  >
  > A few technical choices that might be interesting to folks here:
  > - **Zero accounts / zero cookies:** Spaced-repetition flashcards (`SM-2`-lite), daily streak tracking, and JSON progress backups live entirely in `localStorage`, and analytics uses cookieless GoatCounter.
  > - **Offline-capable static pages:** Built with plain HTML/CSS/JS generators so pages work on low-bandwidth mobile connections and pin cleanly via a bounded Service Worker.
  > - **Print-first CSS sheets:** Every worksheet page (`https://ekguru.shop/learn/hindi/practice/worksheets/`) generates real printable practice sheets + answer keys that strip all site chrome on `Ctrl+P`.
  > - **Script breakdown:** `https://ekguru.shop/name-in-hindi/` explains Devanagari vowel matras and consonant conjuncts letter by letter.
  >
  > Would love honest feedback on anything that feels clunky, broken, or missing for learners.

---

## 4. Product Hunt Launch Draft (Schedule After First 5–10 Active Learners Give Feedback)
- **Name:** EkGuru
- **Tagline (≤ 60 chars):** `Free Hindi & Indian-language courses + 13 browser tools`
- **Links:**
  - Website: `https://ekguru.shop/?ref=producthunt`
  - Toolbox: `https://ekguru.shop/toolbox/?ref=producthunt`
- **Maker Comment:**
  > Hey Product Hunt! I’m Prakash from Jaipur, and I’m building EkGuru — a calm, zero-login web platform to learn Hindi and Indian regional languages (Marathi, Gujarati, Tamil, Telugu, Bengali, Punjabi, Urdu).
  >
  > Whether you moved to a new Indian city and want everyday local phrases, are raising kids abroad who want to read their name in Devanagari (`https://ekguru.shop/name-in-hindi/`), or want a structured 20-minute daily Hindi plan (`https://ekguru.shop/daily-hindi/`), you can open any page and start immediately without creating an account. Tell me what language or tool we should improve next!

---

## 5. Ready-to-Publish Article for IndieHackers & Dev.to

**Title:** Why I Built a Free Hindi & Indian-Language Site with 13 Browser Tools (and Zero Sign-Up Walls)
**Tags:** `webdev`, `indiandev`, `edtech`, `showdev`

### Article Body (Copy-Paste & Adapt)
If you move to Pune, Hyderabad, Chennai, Ahmedabad, or Kolkata for work — or if you grow up outside India wanting to speak Hindi with your grandparents — you run into a strange gap on the web.

Major global apps spend most of their energy on Spanish, French, or Japanese. For Indian languages, learners often bounce between sign-up-gated mobile apps that teach unnatural sentences, expensive courses, or random videos with inconsistent romanised spelling.

So I started building **EkGuru** (https://ekguru.shop/?ref=devto) with three constraints from day one:

#### 1. Open a URL, start learning in 2 seconds (no login wall)
Nothing kills curiosity faster than an onboarding funnel asking for your email, age, daily notification permission, and credit card trial before showing you a single letter of Devanagari.

On EkGuru, every tool and lesson is a plain, fast static web page:
- Want to see how your name works in Devanagari? Open https://ekguru.shop/name-in-hindi/?ref=devto, type a name, and see every vowel mark (*matra*) and consonant cluster broken down immediately.
- Need numbers 1 to 100 with native script digits and pronunciation? Open https://ekguru.shop/learn/hindi/numbers/?ref=devto.
- Want a structured 20-minute daily habit? https://ekguru.shop/daily-hindi/?ref=devto saves your progress and spaced-repetition flashcards directly in your browser’s `localStorage` — with one-click JSON export/import if you switch devices.

#### 2. Side-by-side English + Hindi + Regional Indian Languages
Millions of people relocating within India already know English and some Hindi, and want to learn **Marathi, Gujarati, Tamil, Telugu, Bengali, or Punjabi** for everyday life — speaking to neighbours, auto drivers, and local shopkeepers. Showing English, Hindi, and the target regional language side by side helps learners spot shared roots and polite verb endings much faster.

#### 3. Real printable worksheets (just press `Ctrl+P`)
Parents and Sunday Hindi school teachers still love paper practice. Instead of locking PDFs behind email capture forms, our worksheet pages (https://ekguru.shop/learn/hindi/practice/worksheets/?ref=devto) generate fresh practice sheets in the browser and use dedicated `@media print` rules so pressing Print outputs *only* the clean worksheet and answer key.

#### What I learned the hard way: building pages != discovery
Building static generators is addictive for an engineer — it’s easy to keep polishing features inside your repo while almost nobody knows the site exists. Right now I’ve frozen new auto-generated page templates completely for 30 days to focus on real human distribution: talking to learners, helping in language communities, working with the independent tutors listed on https://ekguru.shop/find-tutors.html?ref=devto, and fixing whatever real visitors find confusing.

If you’re learning Hindi or another Indian language (or building lightweight static educational tools), take a look at the toolbox here and tell me honestly what you’d improve:
https://ekguru.shop/toolbox/?ref=devto
