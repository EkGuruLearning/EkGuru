# EkGuru 🎓
### One Student. One Guru. One Goal.

A complete, **pure front-end** website for online Hindi tutoring.
Built with plain HTML, CSS and JavaScript — **no database, no build step, no npm install,
no server**. You upload the files, and the site is live.

**Live URL after deploy:** https://ek-guru.github.io/Preply/

---

# 📖 TABLE OF CONTENTS

**Read this later, in your own time. Everything is here.**

| # | Section | What it answers |
|---|---|---|
| 1 | [What this site includes](#1-what-this-site-includes) | Feature list |
| 2 | [File structure](#2-file-structure) | Which file does what |
| 3 | [**HOW TO DEPLOY**](#3-how-to-deploy--full-walkthrough) | Getting it online, step by step |
| 4 | [**HOW TO EDIT THE PRICE**](#4-how-to-edit-the-price) | Changing lesson cost |
| 5 | [**HOW TO EDIT THE PHOTO**](#5-how-to-edit-the-photo) | Changing tutor pictures |
| 5b | [**Photo vs Banner**](#5b-the-two-images-each-tutor-can-have) | The two images per tutor |
| 6 | [**HOW TO EDIT TUTOR DATA**](#6-how-to-edit-tutor-data) | Name, bio, subjects, schedule |
| 7 | [**HOW TO EDIT REVIEWS**](#7-how-to-edit-reviews) | Adding and removing reviews |
| 8 | [**HOW TO ADD A NEW TUTOR**](#8-how-to-add-a-new-tutor) | Full copy-paste template |
| 9 | [How to change the video](#9-how-to-change-the-intro-video) | YouTube setup |
| 10 | [How to change contact details](#10-how-to-change-contact-details) | Email and WhatsApp |
| 11 | [How tutors apply to join](#11-how-tutors-apply-to-join-you) | The join.html workflow |
| 11b | [**Connecting a Google Form**](#11b-connecting-a-google-form) | Using a form instead of email |
| 12 | [Languages](#12-languages--7-markets) | The 7-language system |
| 13 | [SEO explained](#13-seo--what-is-implemented-and-why) | Google ranking features |
| 14 | [After deploying: Google setup](#14-after-deploying--google-setup) | Search Console steps |
| 15 | [Troubleshooting](#15-troubleshooting) | If something breaks |
| 16 | [Testing locally](#16-testing-locally) | Preview before uploading |
| 17 | [Rules for AI agents](#17-rules-for-any-ai-agent) | Give this to any AI helper |

---

# 1. What this site includes

| Feature | Status |
|---|---|
| Branding — EkGuru + tagline | ✅ |
| **Whole tutor card clickable** — click anywhere to open the profile | ✅ |
| Home page with tutor listing | ✅ |
| Search page with level / price / sort filters | ✅ |
| Full profile page — about, experience, method, schedule, reviews | ✅ |
| **Become a Tutor** application page | ✅ |
| **Real intro video** — click-to-play YouTube | ✅ |
| **7 languages** with 🌐 globe switcher, including Arabic RTL | ✅ |
| Advanced SEO — 9 schema types, hreflang, sitemap | ✅ |
| Real contact — pre-filled email, optional WhatsApp | ✅ |
| Live Preply booking link | ✅ |
| Smooth animations, fully responsive, mobile menu | ✅ |
| White-page protection | ✅ |
| 404 page, favicon, PWA manifest, social share image | ✅ |
| Total size | 384 KB |

---

# 2. File structure

```
Preply/                            ← this becomes your repository root
│
├── index.html                     ← Home page
├── find-tutors.html               ← Search + filters
├── tutor.html                     ← Profile page (?id=sushila-g)
├── join.html                      ← Become a Tutor page
├── 404.html                       ← Shown for broken links
│
├── css/
│   └── style.css                  ← All styling, animations and RTL support
│
├── js/
│   ├── site-config.js             ← ★ EDIT: brand, email, WhatsApp, site URL
│   ├── tutors-data.js             ← ★ EDIT: everything about your tutors
│   ├── i18n.js                    ← The 7 language packs
│   ├── seo.js                     ← SEO + Google structured data engine
│   └── main.js                    ← Page rendering (you rarely touch this)
│
├── images/
│   ├── sushila.jpg                ← Sushila's photo (square)
│   ├── hemlata.jpg                ← Hemlata's photo (square)
│   ├── hemlata-banner.jpg         ← Hemlata's wide cover banner
│   ├── hemlata-banner-2.jpg       ← Alternative banner ("Read, Write & Speak")
│   ├── placeholder-banner.jpg     ← Fallback banner
│   ├── og-cover.jpg               ← Image shown when the link is shared
│   ├── placeholder-tutor.jpg      ← Automatic fallback if a photo is missing
│   ├── icon-192.png
│   └── icon-512.png
│
├── sitemap.xml                    ← Tells Google every page and language
├── robots.txt                     ← Allows Google + AI crawlers
├── manifest.webmanifest           ← Makes the site installable
├── .github/workflows/deploy.yml   ← Optional auto-deploy
├── .nojekyll                      ← ⚠️ NEVER DELETE — prevents the white page
├── README.md                      ← This file
└── EkGuru-Google-Form.md          ← Copy-paste script for the tutor application form
```

**In practice you only ever open two files:**
* `js/tutors-data.js` — tutor details, prices, photos, reviews
* `js/site-config.js` — your email, WhatsApp, site URL

---

# 3. HOW TO DEPLOY — full walkthrough

There are two ways. **Option A needs no software at all** — just a browser.

## Option A — Upload through the GitHub website (recommended)

### Step 1 — Create the repository

1. Go to **https://github.com** and sign in as `ek-guru`
2. Click the **`+`** icon in the top-right corner → **New repository**
3. Fill in exactly:
   * **Repository name:** `Preply`
   * **Description:** *(optional)* `EkGuru — Learn Hindi online`
   * **Public** ← must be Public. GitHub Pages is only free for public repos.
   * **Do NOT tick** "Add a README file"
   * **Do NOT** add a .gitignore or licence
4. Click **Create repository**

You now see an empty repository page with setup instructions.

### Step 2 — Upload the files

1. On that page, find the link **"uploading an existing file"** and click it
   *(or go to `https://github.com/ek-guru/Preply/upload/main`)*

2. Open the `EkGuru` folder on your computer.

   ⚠️ **The single most common mistake:** do not drag the `EkGuru` folder itself.
   Open it, select **everything inside it**, and drag that.

   You should be dragging:
   ```
   index.html          find-tutors.html    tutor.html
   join.html           404.html            README.md
   sitemap.xml         robots.txt          manifest.webmanifest
   css      (folder)   js      (folder)    images   (folder)
   ```

3. Wait for all files to finish uploading (you will see them listed).

4. Scroll down, type a message like `EkGuru website`, click **Commit changes**.

### Step 3 — Add the hidden `.nojekyll` file ⚠️ IMPORTANT

Files starting with a dot are **hidden** on Windows and Mac, so drag-and-drop
almost always skips `.nojekyll`. **Without it, GitHub may serve a white page.**

Check first: on your repo page, do you see `.nojekyll` in the file list?

**If it is missing, create it manually — it takes 15 seconds:**

1. On the repository page click **Add file** → **Create new file**
2. In the filename box type exactly: `.nojekyll`
3. Leave the file content **completely empty**
4. Scroll down → **Commit new file**

Also check that `.github/workflows/deploy.yml` uploaded. If it did not, that is fine —
it is optional and Option A does not need it.

### Step 4 — Turn on GitHub Pages

1. In your repository click the **Settings** tab (top-right, gear icon)
2. In the left sidebar scroll down and click **Pages**
3. Under **Build and deployment → Source**, choose **Deploy from a branch**
4. Two dropdowns appear:
   * Branch: **`main`**
   * Folder: **`/ (root)`**
5. Click **Save**

### Step 5 — Wait, then visit

* Wait **1 to 2 minutes**. Refresh the Settings → Pages screen.
* A green box appears: *"Your site is live at …"*
* Open 👉 **https://ek-guru.github.io/Preply/**

**Test this checklist on the live site:**
- [ ] Home page loads with the purple hero section
- [ ] Sushila's card appears — **click anywhere on the card**, profile opens
- [ ] Profile shows the video thumbnail — click it, the video plays
- [ ] Click the 🌐 globe in the header, switch to Español — the site translates
- [ ] Switch to العربية — the whole layout flips right-to-left
- [ ] "Send an email" opens your mail app with a pre-written message
- [ ] "Book on Preply" opens the real Preply profile
- [ ] Open the site on your phone — the menu becomes a hamburger

## Option B — Command line (if you have Git installed)

```bash
cd EkGuru

git init
git add -A                 # -A is essential: it includes the hidden .nojekyll
git commit -m "EkGuru — multilingual Hindi tutoring site"
git branch -M main
git remote add origin https://github.com/ek-guru/Preply.git
git push -u origin main
```

Then follow **Step 4** above to switch Pages on.

Verify `.nojekyll` made it:
```bash
git ls-files | grep nojekyll     # should print: .nojekyll
```

## How to update the site later

Once it is live, updating is easy:

**Small edit (changing a price, adding a review):**
1. Go to `https://github.com/ek-guru/Preply`
2. Click into `js` → `tutors-data.js`
3. Click the **pencil ✏️ icon** (top-right of the file)
4. Edit the text right in the browser
5. Scroll down → **Commit changes**
6. Wait 1 minute, hard-refresh the live site with **Ctrl+F5**

**Adding a photo:**
1. Click into the `images` folder → **Add file** → **Upload files**
2. Drag your image in → Commit
3. Then edit `js/tutors-data.js` to point at it

## If you rename the repository

Say you rename `Preply` to `ekguru-site`. Change two things:

1. `js/site-config.js` — one line:
   ```js
   baseUrl: "https://ek-guru.github.io/ekguru-site/",
   ```
2. `404.html` — three places where `/Preply/` appears

Everything else uses relative paths and keeps working automatically.

## Using your own domain (optional, better for SEO)

1. Buy a domain, e.g. `ekguru.com`
2. In your repo: **Settings → Pages → Custom domain** → type `ekguru.com` → Save
3. At your domain registrar, add these DNS records:
   ```
   A     @    185.199.108.153
   A     @    185.199.109.153
   A     @    185.199.110.153
   A     @    185.199.111.153
   CNAME www  ek-guru.github.io
   ```
4. Tick **Enforce HTTPS** once it becomes available
5. Update `baseUrl` in `js/site-config.js` to `https://ekguru.com/`

---

# 4. HOW TO EDIT THE PRICE

**File:** `js/tutors-data.js`

Find the tutor block and change this one number:

```js
priceUSD: 3,               // ← just the number. No "$", no quotes.
lessonLength: "50 min",    // ← how long one lesson is
```

**Example — raising the price to $8:**
```js
priceUSD: 8,
```

That is the entire change. The new price appears **automatically** in **six places**:

| Where | What updates |
|---|---|
| Tutor card on Home | The `$8` in the bottom-left corner |
| Profile header | The price stat block |
| Profile sidebar | The big price at the top of the booking box |
| Home page stats | The "Lessons from" figure (shows your cheapest tutor) |
| Search page filter | The price filter matches correctly |
| **Google search results** | The `Offer` price in the structured data |

### Changing the currency symbol

**File:** `js/site-config.js`

```js
currency: "$",             // the symbol shown on the page
currencyCode: "USD",       // the ISO code Google reads
```

For euros:
```js
currency: "€",
currencyCode: "EUR",
```

> ⚠️ Note: this changes the **symbol only**, not the numbers. If you switch to euros,
> also change each `priceUSD` value to the euro amount you want to charge.

---

# 5. HOW TO EDIT THE PHOTO

## Step 1 — Prepare the image
* **Shape:** square (equal width and height) — otherwise it gets cropped
* **Size:** 500×500 pixels or larger
* **Format:** `.jpg` (smaller) or `.png`
* **Filename:** lowercase, no spaces. Use `priya.jpg`, never `Priya Photo.JPG`
  *(GitHub's servers are case-sensitive — `Photo.jpg` and `photo.jpg` are different files)*

## Step 2 — Put it in the images folder

**On GitHub:** repository → `images` folder → **Add file** → **Upload files** → drag → Commit

**On your computer:** copy it into `EkGuru/images/`

## Step 3 — Point the tutor at it

**File:** `js/tutors-data.js`

```js
photo: "images/sushila.jpg",   // the big photo on the profile page
thumb: "images/sushila.jpg",   // the small photo on the cards
```

Change both to your new filename:
```js
photo: "images/priya.jpg",
thumb: "images/priya.jpg",
```

**Tip:** you can use two different files. Use a tightly cropped face for `thumb`
(it displays small) and a fuller photo for `photo`.

**Safety net:** if the file is missing or misspelled, the site shows
`placeholder-tutor.jpg` instead. The layout never breaks and you never get a white page.

---

# 5b. THE TWO IMAGES EACH TUTOR CAN HAVE

Every tutor supports **two different images**, and they do different jobs.

| Field | Shape | Size | Where it appears |
|---|---|---|---|
| `photo` / `thumb` | **Square** | 500×500 or larger | The round picture on the profile, and the small picture on every card |
| `banner` | **Wide 16:9** | 1280×720 | The large cover strip across the top of the profile page |

```js
photo:  "images/hemlata.jpg",          // square portrait
thumb:  "images/hemlata.jpg",          // same file is fine
banner: "images/hemlata-banner.jpg",   // wide cover strip
```

### How the banner behaves
* It sits across the very top of the profile, above the name.
* The round profile photo **overlaps the bottom edge** of it, which is the familiar
  social-profile look.
* A soft gradient fades the banner into the page so there is no hard line.
* It fades in gently as the page loads.
* On mobile it shortens automatically so it never dominates the screen.

### Banner is optional
Leave `banner: ""` and the profile simply starts without a cover strip — clean and
perfectly normal. Sushila and Tara are set up this way right now.

If you point `banner` at a file that does not exist, the site falls back to
`placeholder-banner.jpg`, and if that is missing too the banner quietly removes itself.
**The layout never breaks.**

### Hemlata has two banners to choose from
Both are already in the `images/` folder:

| File | The ribbon says |
|---|---|
| `hemlata-banner.jpg` *(currently in use)* | "for Kids, Adults & Beginners" |
| `hemlata-banner-2.jpg` | "READ, WRITE & SPEAK" |

To switch, change one line in `js/tutors-data.js`:
```js
banner: "images/hemlata-banner-2.jpg",
```

---

# 6. HOW TO EDIT TUTOR DATA

**File:** `js/tutors-data.js` — everything about a tutor lives in one block.

### Identity
```js
id: "sushila-g",           // unique. This becomes the URL: tutor.html?id=sushila-g
                           // Only lowercase letters and dashes. Changing it breaks old links.
name: "Sushila G.",
nickname: "Sashi",
headline: "Friendly Hindi Tutor — Speak, Read & Write with Confidence",
city: "Rajasthan, India",
timezone: "IST (GMT+5:30)",
countryFlag: "🇮🇳",
```

### Numbers and badges
```js
rating: 5.0,               // 0 to 5, one decimal
reviewsCount: 3,           // ⚠️ must match how many entries are in reviews[]
lessonsCount: 40,
experienceYears: 3,
verified: true,            // true = blue ✓ badge on the photo
superTutor: true,          // true = ⭐ Super Tutor chip next to the name
trialAvailable: true,      // true = "Trial lesson available" in the sidebar
```

### Tags and subjects
```js
tags: ["Patient", "Engaging", "Approachable", "Adaptable"],
// short personality words. The first 3 show on the card, all show on the profile.

teaches: [
  "Hindi for beginners",
  "Conversational Hindi",
  "Devanagari reading & writing"
],
// what you teach. These are also fed to Google as your areas of expertise.

levels: ["Beginner", "Intermediate", "Advanced"],
// ⚠️ must be spelled exactly like this — the search page filter depends on it.

speaks: [
  { lang: "Hindi", level: "Native" },
  { lang: "English", level: "Upper-Intermediate B2" }
],
```

### The About section
```js
about: [
  "First paragraph goes here.",
  "Second paragraph goes here.",
  "Third paragraph goes here."
],
```
**Each string in the list becomes one paragraph.** To add a paragraph, add another
string with a comma before it. To remove one, delete that line.

### Experience (the ✓ tick list)
```js
experience: [
  "Helped complete beginners build a strong Hindi foundation.",
  "Guided intermediate learners to improve speaking and writing."
],
```
Each string becomes one bullet with a green tick.

### Teaching method (the four boxes)
```js
methodology: [
  { title: "Speak from day one", desc: "You start speaking in your first lesson." },
  { title: "Step-by-step grammar", desc: "Grammar broken into small pieces." }
],
```
Add or remove `{ title, desc }` pairs freely — the grid re-flows automatically.

### Weekly schedule
```js
availability: {
  Mon: ["09:00", "10:00", "16:00", "18:00", "20:00"],
  Tue: ["09:00", "11:00", "17:00"],
  Wed: ["09:00", "16:00"],
  Thu: ["10:00", "17:00"],
  Fri: ["09:00", "16:00"],
  Sat: ["10:00", "12:00"],
  Sun: []                    // empty = day off, shows a grey dash
}
```
**Rules:** 24-hour format, always two digits (`09:00` not `9:00`), always in quotes,
separated by commas. Use the tutor's own local time — the page states the timezone
underneath so students can convert.

---

# 7. HOW TO EDIT REVIEWS

Yes — reviews are fully editable. **File:** `js/tutors-data.js`

```js
reviews: [
  {
    name: "Tomasz",
    date: "2026-07-12",        // YYYY-MM-DD format — required by Google
    stars: 5,                  // a whole number, 1 to 5
    text: "Sushila is a very patient teacher..."
  },
  {
    name: "Jon",
    date: "2026-06-19",
    stars: 5,
    text: "Shashi is very patient and maintains a good pace..."
  }
]
```

### To ADD a review
Copy an entire `{ ... }` block, paste it inside the square brackets, and put a
**comma after the previous block**:

```js
reviews: [
  { name: "Tomasz", date: "2026-07-12", stars: 5, text: "..." },   ← comma here
  { name: "Sarah",  date: "2026-08-01", stars: 5, text: "Excellent teacher!" }
]
```
> The **last** block must NOT have a comma after it. That single misplaced comma is the
> most common cause of a page failing to load.

### To DELETE a review
Delete the whole `{ ... }` block including its comma.

### To EDIT a review
Just change the text between the quotes.

### ⚠️ Always update these two numbers to match

```js
rating: 5.0,          // the average of all your stars
reviewsCount: 3,      // how many reviews are in the array
```

**Why this matters:** these two numbers are what Google reads to display the ⭐ star
rating next to your site in search results. If they do not match your actual review
list, Google can flag it as misleading markup and remove your stars entirely.

**How to calculate:** if you have four reviews with 5, 5, 4 and 5 stars:
`(5+5+4+5) ÷ 4 = 4.75` → set `rating: 4.8` and `reviewsCount: 4`.

### If a text contains an apostrophe or quotation mark
```js
text: "She's a great teacher.",              // ✅ apostrophe is fine inside double quotes
text: "He said \"excellent\" every time.",   // ✅ escape inner double quotes with \
```

---

# 8. HOW TO ADD A NEW TUTOR

At the bottom of `js/tutors-data.js` there is a ready template inside a comment block.
Here it is, ready to paste. Add it **after** the last tutor's closing `}`, with a comma
separating them:

```js
  ,{
    id: "priya-s",                    // MUST be unique — becomes tutor.html?id=priya-s
    name: "Priya S.",
    nickname: "Priya",
    headline: "Hindi Tutor for Kids & Beginners",
    subject: "Hindi",
    country: "India",
    countryFlag: "🇮🇳",
    city: "Jaipur, India",
    timezone: "IST (GMT+5:30)",

    photo: "images/priya.jpg",
    thumb: "images/priya.jpg",
    youtubeId: "",                    // paste the YouTube ID, or leave empty
    videoTitle: "",

    rating: 5.0,
    reviewsCount: 0,
    lessonsCount: 0,
    priceUSD: 5,
    lessonLength: "50 min",
    experienceYears: 2,
    trialAvailable: true,
    verified: true,
    superTutor: false,

    preplyUrl: "",                    // their Preply link, or leave empty
    email: "EkGuruLearning@gmail.com",
    whatsapp: "",

    tags: ["Friendly", "Patient", "Kid-friendly"],
    teaches: ["Hindi for kids", "Hindi for beginners", "Conversational Hindi"],
    levels: ["Beginner", "Intermediate"],
    speaks: [
      { lang: "Hindi", level: "Native" },
      { lang: "English", level: "Intermediate B1" }
    ],

    about: [
      "First paragraph about this tutor.",
      "Second paragraph."
    ],
    experience: [
      "First experience point.",
      "Second experience point."
    ],
    methodology: [
      { title: "Play and learn", desc: "Games and stories build vocabulary." },
      { title: "Small steps",    desc: "Every lesson has one clear goal." }
    ],

    availability: {
      Mon: ["15:00", "17:00"],
      Tue: ["15:00", "17:00"],
      Wed: ["15:00"],
      Thu: ["15:00", "19:00"],
      Fri: ["15:00"],
      Sat: ["09:00", "11:00"],
      Sun: []
    },

    reviews: []
  }
```

**That is all you do.** The new tutor appears automatically on the home page, in the
search results, in the filters, in the sitemap and in Google's structured data. You
never touch a single HTML file.

**Checklist when adding someone:**
- [ ] `id` is unique and uses only lowercase letters and dashes
- [ ] Their photo is uploaded to `images/` and both `photo` and `thumb` point at it
- [ ] There is a comma between the previous `}` and the new `{`
- [ ] The very last tutor has **no** comma after its closing `}`
- [ ] `reviewsCount` matches the number of entries in `reviews`

---

# 9. HOW TO CHANGE THE INTRO VIDEO

Sushila's real video is already working:
**https://youtu.be/Ykic7gkyHjg** — *"HINDI TUTOR INTRO" by Sashi*

### Getting the ID from any YouTube URL

You need only the **ID**, never the full link:

| URL format | The ID |
|---|---|
| `https://youtu.be/`**`Ykic7gkyHjg`** | `Ykic7gkyHjg` |
| `https://www.youtube.com/watch?v=`**`Ykic7gkyHjg`** | `Ykic7gkyHjg` |
| `https://youtube.com/shorts/`**`Ykic7gkyHjg`** | `Ykic7gkyHjg` |

### Setting it
```js
youtubeId: "Ykic7gkyHjg",
videoTitle: "Hindi Tutor Intro",
```

Leave `youtubeId: ""` and a tidy "Intro video coming soon" card appears instead.

### How it works, and why it is done this way

The page does **not** embed YouTube on load. It shows only the video's thumbnail image
with a large play button drawn over it. The real YouTube player is inserted the instant
someone clicks.

* **Speed:** saves roughly 1.5 MB and 2–3 seconds of loading on every profile view.
  Page speed is a direct Google ranking factor.
* **Privacy:** no YouTube cookies are set until the visitor actively chooses to watch,
  which keeps you clear of most cookie-consent obligations.
* **Reliability:** even if YouTube is slow, your page is not.

### If the video does not play

* Open the video on YouTube → **Edit** → **Visibility**. It must be **Public** or
  **Unlisted**. *Private* videos cannot be embedded anywhere.
* Scroll to **Show more** → check that **"Allow embedding"** is ticked.
* Make sure you pasted only the ID, not the whole URL.

---

# 10. HOW TO CHANGE CONTACT DETAILS

**File:** `js/site-config.js`

```js
email: "EkGuruLearning@gmail.com",   // already set — used across the whole site
whatsapp: "",                        // empty for now
```

### Turning WhatsApp on

Add a real number **with the country code and no spaces**:

```js
whatsapp: "+919876543210",
```

| Value | What happens |
|---|---|
| `""` *(current)* | WhatsApp buttons are hidden completely. The floating round button becomes an email button. **No broken links anywhere.** |
| `"+919876543210"` | Green WhatsApp buttons appear on every profile, and the floating button becomes WhatsApp — all opening a chat with a ready-written message already typed. |

### Per-tutor contact

A tutor can have their own details, which override the site defaults:

```js
email: "priya@gmail.com",
whatsapp: "+919812345678",
```

### What the buttons actually do

**Email button** opens the visitor's mail app with everything pre-written:
> **Subject:** Hindi lesson enquiry — Sushila G. (EkGuru)
> **Body:** Hello Sushila G., I found your profile on EkGuru and I would like to learn
> Hindi. My current level: ___ My goal: ___ Preferred days and times: ___

The student only fills in the blanks — which means you receive complete, useful enquiries
instead of a bare "hi".

**WhatsApp button** opens a chat with the message already typed and ready to send.

---

# 11. HOW TUTORS APPLY TO JOIN YOU

There is a dedicated page — **`join.html`** — linked in the header menu and the footer as
**"Become a Tutor"**.

### What the applicant sees
A numbered checklist of what to send, then a big button. Clicking it opens their email
app with a message **already written** to `EkGuruLearning@gmail.com`, containing a
numbered form:

```
1. Full name and city:
2. Short bio (150-250 words):
3. Profile photo: (attached)
4. Intro video link (YouTube):
5. Price per 50-minute lesson (USD):
6. Weekly availability and timezone:
7. Contact email:
8. WhatsApp number (optional):
9. Preply profile link (optional):
10. Years of teaching experience:
```

The page also answers the four questions every tutor asks: there is no joining fee,
EkGuru is Hindi-only, tutors handle their own payments (you take no commission), and
profiles can be updated any time.

### What YOU do when an application arrives

**Your 5-minute workflow:**

1. **Save their photo** — rename it to something simple like `priya.jpg`
2. **Upload it** — repository → `images` → Add file → Upload files → Commit
3. **Open** `js/tutors-data.js` → click the pencil ✏️
4. **Copy the template** from [Section 8](#8-how-to-add-a-new-tutor), paste it after the
   last tutor, and fill in the details from their email
5. **Commit changes**
6. Wait one minute — their profile is live

### Before you approve someone
- [ ] Do they actually teach Hindi? *(this site is Hindi-only — that focus is why students trust it)*
- [ ] Is the photo clear and professional?
- [ ] Does the intro video play, and is it set to Public or Unlisted?
- [ ] Is the bio written in reasonable English? *(you can tidy it up yourself)*
- [ ] Is the price sensible next to your existing tutors?

---

# 11b. CONNECTING A GOOGLE FORM

By default the "Become a Tutor" buttons open a pre-filled email. If you would rather
collect applications through a **Google Form** — which gives you photo uploads and a tidy
spreadsheet — the site supports that with a single line of configuration.

### Building the form
A complete, copy-paste-ready script for the form lives in a separate file:
**`EkGuru-Google-Form.md`**

It contains the exact form title, description, confirmation message, all 6 sections and
all 31 questions, plus which question type to choose and which validation rules to set.
Just paste each block into Google Forms in order.

### Connecting it to the site

Open **`js/site-config.js`** and find:

```js
applyFormUrl: "",
```

Paste your form link between the quotes:

```js
applyFormUrl: "https://forms.gle/AbCdEfGhIjKlMnOp",
```

Commit. That is the whole change.

### What happens automatically

| | `applyFormUrl: ""` *(current)* | `applyFormUrl: "https://forms.gle/…"` |
|---|---|---|
| Main button | "Email your application" → opens email | **"Apply with the form" → opens the form in a new tab** |
| Sidebar button | opens email | **opens the form** |
| Line underneath | just your email address | **"Prefer email? Write to EkGuruLearning@gmail.com"** |
| Button text | translated in all 7 languages | translated in all 7 languages |

The email route always remains available as a fallback, so nobody is ever blocked from
applying — and switching back is as simple as emptying the quotes again.

### Where the applications land

* **Responses tab** in your form, or click the green Sheets icon to get a spreadsheet
* **Uploaded photos** go to a Google Drive folder named after the form
* Turn on email alerts: Responses tab → **⋮** → *Get email notifications for new responses*

`EkGuru-Google-Form.md` also includes a mapping table showing which form question feeds
which field in `js/tutors-data.js`, so adding an approved tutor becomes pure copy-paste.

---

# 12. LANGUAGES — 7 markets

| Language | Market | Code | Notes |
|---|---|---|---|
| English | 🇺🇸 United States | `en` | default |
| Español | 🇪🇸 Spain | `es` | |
| Français | 🇫🇷 France | `fr` | |
| Deutsch | 🇩🇪 Germany | `de` | |
| Português | 🇧🇷 Brazil | `pt` | |
| 日本語 | 🇯🇵 Japan | `ja` | |
| العربية | 🇦🇪 UAE | `ar` | **full right-to-left layout** |

### How visitors use it
* A **🌐 globe icon** sits in the header next to the current flag and language name.
  Clicking it opens a labelled dropdown of all 7, with a ✓ on the active one.
* On mobile the switcher becomes a full-width row inside the hamburger menu.
* The choice is saved in the browser and reflected in the URL as `?lang=fr`, so a French
  visitor can bookmark or share a French link.
* First-time visitors are matched to their **browser language** automatically.
* All **146 text strings exist in all 7 languages** — verified, zero gaps.

### What does and does not translate

| Translates automatically | Stays as you wrote it |
|---|---|
| All buttons, menus, labels | Tutor names |
| Section headings | Tutor bios and experience text |
| Day names, FAQ, form text | Review text |
| Page titles and SEO descriptions | Subject tags |

This is deliberate — a bio written in the tutor's own voice reads better than a machine
translation. If you want translated bios later, you can add them per language.

### Adding an 8th language

1. **`js/site-config.js`** — add to `EKGURU_MARKETS`:
   ```js
   { code: "it", locale: "it-IT", country: "Italy", flag: "🇮🇹", label: "Italiano", dir: "ltr" }
   ```
2. **`js/i18n.js`** — copy the whole `en: { ... }` block, rename it to `it:`, translate
   the values (keep the keys on the left exactly as they are).

Any key you miss silently falls back to English rather than showing a blank.

---

# 13. SEO — what is implemented and why

This is the part that decides whether Google shows your site. Everything below is
generated from your data, so it stays accurate the moment you change a price or add a
review.

### Structured data — 9 schema types

Structured data is a hidden block of information that tells Google exactly what your page
is about. It is what earns those enhanced search results.

| Schema | Page | What you get in Google |
|---|---|---|
| `EducationalOrganization` | all | Brand recognition, knowledge-panel eligibility |
| `WebSite` + `SearchAction` | all | A search box directly inside your Google result |
| `BreadcrumbList` | all | `ekguru.com › Tutors › Sushila G.` trail |
| `Course` + `CourseInstance` | home, search | **Course rich result** showing your price |
| `ItemList` | home, search | Carousel eligibility for the tutor list |
| `Person` + `AggregateRating` | profiles | **⭐⭐⭐⭐⭐ 5.0 stars in search results** |
| `Service` + `Offer` | profiles | Price and availability shown in the result |
| `Review` ×3 | profiles | Quoted review snippets |
| `VideoObject` | profiles | **Video thumbnail in Google and the Video tab** |
| `FAQPage` | home, join | **Expandable questions under your result** |

### International SEO
* `hreflang` tags for all 7 locales **plus `x-default`** — 8 per page. This is what stops
  Google treating your Spanish page as a duplicate of your English page.
* `og:locale` and alternates so social previews are correct per market.
* `<html lang>` and `dir` set correctly, including RTL for Arabic.
* `sitemap.xml` lists every page with all 8 language alternates.

### Rankings and crawling
* **35 unique title/description combinations** — 5 pages × 7 languages, each written for
  the keywords that market actually searches for.
* Profile titles auto-include the rating and lesson count:
  *"Sushila G. — Online Hindi Tutor (5.0★, 40 lessons)"*. Numbers in a title measurably
  increase click-through rate, which itself feeds back into ranking.
* `robots.txt` explicitly welcomes **GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot and
  Google-Extended** — so your tutors can be recommended by AI assistants, not just Google.
* `max-image-preview:large` and `max-snippet:-1` for the largest possible result display.
* Canonical URLs prevent duplicate-content penalties from the `?lang=` parameters.

### Core Web Vitals — Google's speed ranking signal
* Zero external CSS or JavaScript. Nothing blocks rendering.
* The video facade saves ~1.5 MB on every profile view.
* Every image has explicit `width` and `height`, so nothing jumps as the page loads
  (CLS ≈ 0 — one of Google's three core metrics).
* `loading="lazy"` below the fold, `preconnect` hints for the video CDN.
* **Whole site: 384 KB.** Most tutoring sites load 3–5 MB.

### Accessibility — an indirect ranking factor
Skip-to-content link, semantic landmarks, visible focus rings, ARIA labels on the menu
and language switcher, full keyboard navigation, and a reduced-motion mode for users who
prefer less animation.

### Realistic expectations

SEO is not instant. A rough timeline for a brand-new site:

| Timeframe | What to expect |
|---|---|
| Week 1 | Google discovers and indexes the pages |
| Weeks 2–4 | You appear for your brand name ("EkGuru") |
| Months 2–3 | Long-tail phrases start ranking ("hindi tutor for beginners online") |
| Months 4–6 | Competitive terms, if you keep adding tutors and reviews |

**What speeds this up most:** more tutors, more genuine reviews, and links from other
sites. Put your site link in your Preply profile, your YouTube channel description, and
any social media you use.

---

# 14. AFTER DEPLOYING — Google setup

Do this once, right after the site goes live. It takes about ten minutes.

### 1. Google Search Console (essential)
1. Go to **https://search.google.com/search-console**
2. **Add property** → choose **URL prefix**
3. Enter `https://ek-guru.github.io/Preply/`
4. Verify using the **HTML tag** method — copy the meta tag Google gives you and paste it
   into the `<head>` of `index.html`, just under the `<title>` line
5. Once verified: **Sitemaps** in the left menu → enter `sitemap.xml` → **Submit**
6. **URL Inspection** → paste your home page URL → **Request indexing**

### 2. Rich Results Test (confirm your stars work)
1. Go to **https://search.google.com/test/rich-results**
2. Paste `https://ek-guru.github.io/Preply/tutor.html?id=sushila-g`
3. It should report **Person, Review, Video, Breadcrumb** as valid
4. Paste your home page too — it should report **Course, FAQ, Breadcrumb**

### 3. PageSpeed Insights (check your speed score)
1. Go to **https://pagespeed.web.dev**
2. Paste your home page URL
3. You should score in the 90s on both mobile and desktop

### 4. Bing (takes two minutes, worth doing)
**https://www.bing.com/webmasters** — you can import directly from Google Search Console
in one click. Bing also feeds DuckDuckGo and several AI assistants.

### 5. Spread your links
Google trusts a site more when other sites link to it. Add your URL to:
* Your Preply profile description
* Your YouTube channel "About" section and video descriptions
* Any Facebook, Instagram or LinkedIn profile
* Your email signature

---

# 15. TROUBLESHOOTING

### The page is completely white
1. **Check `.nojekyll` exists** in your repository root. This causes 90% of white pages.
   Missing? See [Step 3 of the deploy guide](#step-3--add-the-hidden-nojekyll-file--important).
2. **Hard refresh:** `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac)
3. **Check the folder structure.** In your repo you should see `index.html` at the top
   level. If you see an `EkGuru` folder instead, you uploaded the folder rather than its
   contents — delete everything and re-upload correctly.
4. **Open the browser console:** press `F12` → **Console** tab. Any red error message
   tells you exactly which file failed.

> This site is built so a white page should be nearly impossible — if the JavaScript
> fails, you get a **red error box naming the broken section** instead of a blank screen.
> If you see that red box, it will tell you what to fix.

### The site loads but has no styling
The CSS did not upload. Check that `css/style.css` exists in your repository, spelled
exactly like that in lowercase.

### A photo shows a grey silhouette
That is the automatic fallback. Either the file is missing, or the filename does not
match exactly. Remember: `Priya.jpg` and `priya.jpg` are **different files** on GitHub.

### A tutor disappeared after I edited the data
You have a syntax error in `js/tutors-data.js`. The usual culprits:
* A missing comma between two `{ }` blocks
* An **extra** comma after the **last** block
* A missing closing `"` on a text string
* A `"` inside a string that was not escaped as `\"`

**How to find it:** open the live site, press `F12` → **Console**. The error message
names the line number.

### The video will not play
See [Section 9](#if-the-video-does-not-play). Usually the video is set to Private, or
embedding is disabled in the YouTube settings.

### My changes are not showing up
1. Did you click **Commit changes** at the bottom of the GitHub edit page?
2. Deployment takes 1–2 minutes. Check the **Actions** tab for a green tick.
3. Hard refresh with `Ctrl + F5` — browsers cache aggressively.

### Google is not showing my site
1. Search `site:ek-guru.github.io/Preply` — if results appear, you are indexed
2. If not, use Search Console → **URL Inspection** → **Request indexing**
3. New sites genuinely take 1–4 weeks. This is normal and unavoidable.

---

# 16. TESTING LOCALLY

Always preview before you upload.

**Quickest way** — double-click `index.html`. Most things work, but the language
switcher and profile links behave slightly differently than on a real server.

**Proper way** — run a tiny local server:

```bash
cd EkGuru
python3 -m http.server 8080
```
Then open **http://localhost:8080**

Press `Ctrl + C` to stop it. This behaves exactly like GitHub Pages, so what you see is
what you will get.

---

# 17. RULES FOR ANY AI AGENT

Copy this section verbatim if you ask another AI to modify the site.

1. **Never hard-code tutor data into HTML.** Only `js/tutors-data.js`.
2. **Never use absolute paths** (`/css/...`). Always relative (`css/...`).
3. **Never delete `.nojekyll`.**
4. Wrap every new render function in `try/catch` calling `showError()`.
5. **Never add a build tool, framework or npm dependency.** This site stays pure static.
6. Always escape user-supplied text with `esc()` before inserting it into the DOM.
7. Add every new UI string to **all 7 language packs** in `js/i18n.js`.
8. If you add a page, add it to `sitemap.xml` and to the `COPY` table in `js/seo.js`.
9. Keep the whole tutor card clickable via the stretched `.tcard-link` anchor.
10. Test all 5 pages in all 7 languages before declaring the work finished.

---

# ✅ TEST RESULTS

Every item below was run and verified before delivery.

| Test | Result |
|---|---|
| JavaScript syntax — all 5 files | ✅ pass |
| Headless browser render — 5 pages | ✅ 0 errors, 0 white pages |
| Language sweep — 7 languages × 2 pages | ✅ 14/14 pass |
| Translation coverage | ✅ 146/146 keys in all 7 packs |
| Arabic RTL layout | ✅ `dir="rtl"` applied correctly |
| **Whole-card click — 8 different areas** | ✅ **8/8 open the profile** |
| Stretched link supports Ctrl+click / new tab | ✅ real `<a href>` |
| **🌐 Globe icon in all 7 languages** | ✅ 7/7 |
| Language menu — options, tick, ARIA label | ✅ 7 options, correct active state |
| Invalid `?id=` in the URL | ✅ graceful fallback, no crash |
| Video embed — real click test | ✅ real YouTube player loads |
| JSON-LD parse and field validation | ✅ 9 types, rating/price/reviews correct |
| hreflang tags | ✅ 8 per page (7 locales + x-default) |
| `sitemap.xml` XML validity | ✅ valid |
| All 17 resources over HTTP | ✅ all 200 OK |
| Absolute-path scan | ✅ none found |
| Total page weight | ✅ 384 KB |

---

# 📌 QUICK REFERENCE CARD

Keep this handy.

| I want to… | Open this file | Change this |
|---|---|---|
| Change the price | `js/tutors-data.js` | `priceUSD: 3,` |
| Change a photo | `js/tutors-data.js` | `photo:` and `thumb:` |
| Change the bio | `js/tutors-data.js` | `about: [ ... ]` |
| Add or edit a review | `js/tutors-data.js` | `reviews: [ ... ]` + `reviewsCount` |
| Change the schedule | `js/tutors-data.js` | `availability: { ... }` |
| Change the video | `js/tutors-data.js` | `youtubeId: "..."` |
| Add a new tutor | `js/tutors-data.js` | Paste the template block |
| Change the email | `js/site-config.js` | `email: "..."` |
| Turn WhatsApp on | `js/site-config.js` | `whatsapp: "+91..."` |
| Change the site URL | `js/site-config.js` | `baseUrl: "..."` |
| Add a language | `js/site-config.js` + `js/i18n.js` | `EKGURU_MARKETS` + a new pack |

---

© EkGuru — One Student. One Guru. One Goal.
