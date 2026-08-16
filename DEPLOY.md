# 🚀 DEPLOY GUIDE — EkGuru v4

**Read this once, follow it top to bottom, and your site is live in about 10 minutes.**

Nothing to install. No terminal needed. Just a browser.

---

# 📁 PART 1 — WHAT YOU ARE UPLOADING

Open your `EkGuru` folder. This is what is inside, and every single item goes to GitHub.

```
EkGuru/
│
├── 📄 index.html                  Home page
├── 📄 find-tutors.html            Search page
├── 📄 tutor.html                  Tutor profile page
├── 📄 join.html                   Become a Tutor page
├── 📄 404.html                    Shown for broken links
│
├── 📁 css/
│   └── style.css                  All styling and responsive rules
│
├── 📁 js/                         ← 7 files, ALL required
│   ├── site-config.js             Brand, email, founder, launch status
│   ├── tutors-data.js             Your 3 tutors
│   ├── i18n.js                    7 language packs
│   ├── seo-engine.js              Keyword engine
│   ├── seo.js                     Meta tags + structured data
│   ├── main.js                    Page rendering
│   └── features.js                Search, booking, share
│
├── 📁 images/                     ← 7 files
│   ├── sushila.jpg
│   ├── hemlata.jpg
│   ├── hemlata-banner.jpg
│   ├── placeholder-tutor.jpg
│   ├── placeholder-banner.jpg
│   ├── og-cover.jpg
│   ├── icon-192.png
│   └── icon-512.png
│
├── 📄 sitemap.xml                 Tells Google every page
├── 📄 robots.txt                  Allows Google + AI crawlers
├── 📄 manifest.webmanifest        Makes the site installable
├── 📄 .nojekyll                   ⚠️ CRITICAL — see Part 3
│
├── 📁 .github/workflows/
│   └── deploy.yml                 Optional auto-deploy
│
├── 📄 README.md                   Full manual
├── 📄 UPDATE-GUIDE.md             What changed each version
├── 📄 DEPLOY.md                   This file
└── 📄 EkGuru-Google-Form.md       Google Form script
```

**Folders to create on GitHub: 3** — `css`, `js`, `images`
*(Plus `.github/workflows` if you want auto-deploy — optional.)*

**Total: 26 files, about 950 KB.**

---

# 🚀 PART 2 — UPLOAD AND DEPLOY

## Step 1 · Create the repository

1. Go to **https://github.com** and sign in as `ekgurulearning`
2. Click the **`+`** at the top right → **New repository**
3. Fill in exactly:

   | Field | Value |
   |---|---|
   | Repository name | **`EkGuru`** |
   | Description | `EkGuru — Learn Hindi online with a personal Guru` |
   | Visibility | **Public** ← must be Public, GitHub Pages is only free for public repos |
   | Add a README | **leave unticked** |
   | .gitignore | **None** |
   | Licence | **None** |

4. Click **Create repository**

## Step 2 · Upload the files

1. On the empty repository page, click **uploading an existing file**
2. Open your `EkGuru` folder on your computer
3. Select **everything inside it** — press `Ctrl+A` (Windows) or `Cmd+A` (Mac)

   ⚠️ **The most common mistake:** do not drag the `EkGuru` folder itself.
   Go *inside* it, select the contents, drag those.

   ✅ Correct — you are dragging: `index.html`, `find-tutors.html`, `tutor.html`,
   `join.html`, `404.html`, `sitemap.xml`, `robots.txt`, `manifest.webmanifest`, the
   `.md` files, and the folders `css`, `js`, `images`

   ❌ Wrong — dragging a single folder called `EkGuru`. Your URL then becomes
   `/EkGuru/EkGuru/` and the page will not load.

4. GitHub keeps the folder structure automatically. Wait for every file to list.
5. In the box at the bottom type `EkGuru website v4`
6. Click **Commit changes**

## Step 3 · ⚠️ Add `.nojekyll` — DO NOT SKIP THIS

Files beginning with a dot are **hidden** on Windows and Mac, so drag-and-drop almost
always misses `.nojekyll`. **Without it GitHub can serve a blank white page.**

**Check:** look at your repository file list. Do you see `.nojekyll`?

**If it is missing, create it — it takes 15 seconds:**

1. On the repository page click **Add file** → **Create new file**
2. In the filename box type exactly: `.nojekyll`
3. Leave the content **completely empty**
4. Scroll down → **Commit new file**

## Step 4 · Turn on GitHub Pages

1. Click the **Settings** tab (top right of the repository)
2. In the left sidebar scroll down and click **Pages**
3. Under **Build and deployment → Source** choose **Deploy from a branch**
4. Two dropdowns appear:
   * Branch: **`main`**
   * Folder: **`/ (root)`**
5. Click **Save**

## Step 5 · Wait, then open

Wait **1 to 2 minutes**, then refresh the Settings → Pages screen. A green box appears:
*"Your site is live at…"*

### 🎉 **https://ekgurulearning.github.io/EkGuru/**

---

# ✅ PART 3 — CHECK IT WORKS

Open your live URL and tick these off:

**Desktop**
- [ ] Home page loads with the purple hero section
- [ ] Header shows a 🔍 search box and an orange **"Coming soon"** pill
- [ ] Type `hem` in the search box — Hemlata appears instantly with her photo and $12
- [ ] Type `child` — 2 tutors appear *(synonyms working)*
- [ ] Type `beginer` with the typo — still finds tutors
- [ ] 3 tutor cards on the home page
- [ ] **Click anywhere on a card** — the profile opens
- [ ] Hemlata's banner is **fully visible**, nothing cut off
- [ ] Click **📅 Book a lesson** — the booking window opens with time slots
- [ ] Click the 🌐 globe → Español — the whole site translates
- [ ] Click 🌐 → العربية — the layout flips right-to-left
- [ ] Footer shows **"Founded by Prakash · MNIT Jaipur · B.Tech CSE 2022–2026"**

**Mobile** *(open the URL on your phone)*
- [ ] Hamburger menu opens with search, links and language, all full width
- [ ] Cards are one per row with full-width buttons
- [ ] Booking window fits the screen
- [ ] Nothing scrolls sideways

**Right-click → View page source** and confirm you can see:
- [ ] `<meta name="keywords"` with a very long list
- [ ] `<script type="application/ld+json">` with `"@type":"Person","name":"Prakash"`

---

# 🔍 PART 4 — GET GOOGLE TO FIND YOU

Do this the same day you deploy. It is the difference between being found in 2 weeks
and being found in 3 months.

## 4.1 Google Search Console — essential

1. Go to **https://search.google.com/search-console**
2. **Add property** → choose **URL prefix**
3. Enter `https://ekgurulearning.github.io/EkGuru/`
4. Verify with the **HTML tag** method:
   * Google gives you a line like `<meta name="google-site-verification" content="abc123..." />`
   * Open `index.html` on GitHub → pencil ✏️ → paste it right after the `<title>` line
   * Commit, wait a minute, click **Verify**
5. Once verified: **Sitemaps** in the left menu → type `sitemap.xml` → **Submit**
6. **URL Inspection** → paste your home page URL → **Request indexing**
7. Repeat step 6 for each tutor profile URL

## 4.2 Bing Webmaster Tools — 2 minutes, worth it

**https://www.bing.com/webmasters** — you can **import directly from Google Search
Console** in one click. Bing also powers DuckDuckGo, Yahoo and several AI assistants.

## 4.3 Rich Results Test — confirm your stars

**https://search.google.com/test/rich-results**

Paste `https://ekgurulearning.github.io/EkGuru/tutor.html?id=sushila-g`
You should see **Person, Review, Video, Breadcrumb** all valid.

Paste your home page — you should see **Course, FAQ, HowTo, Breadcrumb**.

## 4.4 PageSpeed Insights

**https://pagespeed.web.dev** — paste your home page. You should score in the 90s.

## 4.5 Build links — this matters most

Google ranks pages that other sites link to. Add your URL to:

* ✅ **Your Preply profile** description — highest value, same topic
* ✅ **YouTube** — channel About section and every video description
* ✅ **Instagram / Facebook / LinkedIn** bio
* ✅ **Your email signature**
* ✅ Reddit r/Hindi, r/languagelearning — genuinely helpful comments only
* ✅ Quora answers about learning Hindi

---

# 🌐 PART 5 — CUSTOM DOMAIN (recommended before launch)

`ekguru.com` looks far more professional than `ek-guru.github.io` and Google trusts it more.

1. Buy the domain (GoDaddy, Namecheap, Google Domains — around ₹800/year)
2. In your repo: **Settings → Pages → Custom domain** → type `ekguru.com` → **Save**
3. At your domain registrar add these DNS records:

   | Type | Name | Value |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | ekgurulearning.github.io |

4. Wait up to an hour, then tick **Enforce HTTPS**
5. Update one line in `js/site-config.js`:
   ```js
   baseUrl: "https://ekguru.com/",
   ```
6. Update the three `/EkGuru/` paths in `404.html`
7. Re-submit the sitemap in Search Console

---

# 🔄 PART 6 — UPDATING AFTER LAUNCH

**Changing a price, a bio, adding a review:**
1. Repository → `js` → `tutors-data.js`
2. Click the pencil ✏️
3. Edit right in the browser
4. **Commit changes**
5. Wait 1 minute, hard-refresh with `Ctrl+F5`

**Adding a photo:**
1. `images` folder → **Add file** → **Upload files** → drag → Commit
2. Then edit `js/tutors-data.js` to point at it

**Going live (removing the "Coming soon" pill):**
`js/site-config.js` → change `status: "soon"` to `status: "live"`

---

# 🔍 PART 7 — WHAT PEOPLE WILL FIND YOU BY

Here is where your traffic will realistically come from, in order.

## Tier 1 — you should rank here within weeks

These are brand and founder terms with almost no competition:

| Search term | Why you will rank |
|---|---|
| `ekguru` | Your brand, nobody else uses it |
| `ek guru hindi` | Brand variant |
| `ekguru learning` | Brand variant |
| `prakash mnit jaipur` | Founder name, indexed via Person schema |
| `prakash ekguru` | Founder + brand |
| `ekguru founder` | Founder + brand |
| `mnit jaipur startup ekguru` | Founder + college |
| `sushila g hindi tutor` | Tutor name |
| `hemlata hindi tutor` | Tutor name |
| `one student one guru one goal` | Your tagline |

## Tier 2 — realistic within 2 to 4 months

Long-tail phrases where big platforms compete weakly:

* `hindi tutor for kids online`
* `native hindi tutor with trial lesson`
* `learn devanagari script online`
* `affordable hindi lessons under 5 dollars`
* `one to one hindi lessons online`
* `hindi tutor in my timezone`
* `hindi conversation practice with a native speaker`
* `hindi tutor for heritage speakers`
* `learn hindi to talk to family`
* `hindi lessons for travel to india`
* `indian hindi tutoring platform`
* `preply alternative for hindi`

## Tier 3 — 6 to 12 months, needs more tutors and reviews

The high-volume head terms where Preply and italki spend real money:

* `learn hindi online`
* `hindi tutor`
* `online hindi classes`
* `hindi teacher near me`

## Question searches — AI assistants pick these up quickly

Your FAQ and HowTo schema target these directly:

* "how much do hindi lessons cost"
* "how to learn hindi online"
* "where can i find a native hindi tutor"
* "best way to learn hindi for beginners"
* "how long does it take to learn hindi"

## What actually moves you up the list

| Action | Impact |
|---|---|
| Each new tutor with a full unique bio | ⭐⭐⭐⭐⭐ a whole new page Google can rank |
| Real student reviews | ⭐⭐⭐⭐⭐ fresh content plus ⭐ stars in results |
| Intro video on every profile | ⭐⭐⭐⭐ video results face far less competition |
| Link from your Preply profile | ⭐⭐⭐⭐ same-topic link, very strong |
| Custom domain | ⭐⭐⭐ |
| More keywords in the tag | ⭐ Google ignores the keywords tag |

**Three excellent profiles beat ten million keywords.** The engine gives you reach;
real content is what converts that reach into rankings.

---

# 🎯 PART 8 — YOUR SEO SETUP IN NUMBERS

| | |
|---|---|
| Keyword combination space | **12,665,492** |
| Per language | 1,809,356 |
| Vocabulary terms | 215 across 11 categories |
| Phrases written per page | 200–290, **every page a different set** |
| Keywords tag length | ~2,390 characters per page |
| Founder phrases | 40, prioritised on every page |
| Unique page variants | 42 — 6 pages × 7 languages |
| Schema types | **12** |
| hreflang tags | 8 per page |
| Site size | 952 KB total |

**The 12 schema types:** Organization, WebSite, WebPage, Breadcrumb, Course, ItemList,
Person (tutor), Person (founder), Service, Review, VideoObject, FAQPage, HowTo,
Speakable.

**A straight answer about keyword counts.** Generating tens of millions of phrases is
easy; the maths above is real. But Google dropped the meta keywords tag as a ranking
signal in 2009, and cramming a page with keywords gets it filtered out. So this build
does both things properly: the engine writes a genuine, page-specific keyword tag that
Bing, Yandex and AI crawlers do read, while the rankings work is done where it actually
counts — 12 schema types, unique titles and descriptions on 42 page variants, real
content, fast loading and clean mobile design. Everything it claims is true about what
EkGuru offers, so there is nothing here that can be penalised.

---

# 🆘 PART 9 — TROUBLESHOOTING

### White page
1. **Is `.nojekyll` in the repository?** This is 90% of white pages. See Step 3.
2. Hard refresh: `Ctrl+F5` / `Cmd+Shift+R`
3. Is `index.html` at the **top level** of the repo? If you see an `EkGuru` folder
   instead, delete everything and re-upload the contents.
4. Press `F12` → **Console** — any red error names the file at fault.

> This site is built so a white page is nearly impossible. If JavaScript fails you get a
> **red box naming the broken section**, not a blank screen.

### No styling
`css/style.css` did not upload, or the folder is named `CSS` instead of `css`.
GitHub is case-sensitive.

### Search box missing
`js/features.js` did not upload. Check the `js` folder has all **7** files.

### Photo shows a grey silhouette
File missing or the name does not match exactly. `Hemlata.jpg` ≠ `hemlata.jpg`.

### A tutor vanished after editing
Syntax error in `js/tutors-data.js` — usually a missing comma between two `{ }` blocks,
or an extra comma after the last one. Press `F12` → Console for the line number.

### Changes not appearing
Did you click **Commit changes**? Deployment takes 1–2 minutes. Then `Ctrl+F5`.

### Google not showing the site
Search `site:ekgurulearning.github.io/EkGuru` — results mean you are indexed. If not, use
Search Console → URL Inspection → Request indexing. New sites take 1–4 weeks. Normal.

---

# ✅ PART 10 — LAUNCH CHECKLIST

**Before you announce it**
- [ ] All 26 files uploaded, `.nojekyll` confirmed present
- [ ] GitHub Pages on, site loads at the live URL
- [ ] Tested on your own phone
- [ ] Hemlata's real bio, city and video ID filled in
- [ ] Tara's photo and real details added
- [ ] Personal email and WhatsApp set for each tutor
- [ ] Every `EDIT ME` in `js/tutors-data.js` resolved
- [ ] Search Console verified and sitemap submitted
- [ ] Rich Results Test passes on a profile page

**On launch day**
- [ ] `status: "soon"` → `status: "live"` in `js/site-config.js`
- [ ] Link added to your Preply profile and YouTube description
- [ ] Announce on social media
- [ ] Ask your first students for reviews

---

**Built by Prakash · MNIT Jaipur · B.Tech CSE 2022–2026**

© EkGuru — One Student. One Guru. One Goal.
