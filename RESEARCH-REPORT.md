# 🔬 DEEP RESEARCH REPORT
### Mobile fixes · SEO audit · Country pricing · Why search is not showing you

**Nothing has been changed. This is analysis only.**
Read it, tell me what you want, and I will build it.

---

# 📑 CONTENTS

| # | Question you asked | Section |
|---|---|---|
| 1 | Mobile kaise fix hoga, kaunsi file badlegi | [Part 1](#part-1--the-mobile-bug) |
| 2 | Reviews mobile par slide kaise honge | [Part 2](#part-2--mobile-review-slider) |
| 3 | Mobile ke liye special aur kya | [Part 3](#part-3--mobile-first-thinking) |
| 4 | SEO kahan hai, kaunsi file mein | [Part 4](#part-4--where-the-seo-lives) |
| 5 | Kaunse word, kis page par kitne | [Part 5](#part-5--exact-keyword-counts) |
| 6 | **Search mein abhi bhi kyun nahi dikhta** | [Part 6](#part-6--why-you-are-not-in-search-the-real-answer) ⚠️ |
| 7 | SEO ko next level kaise le jayein | [Part 7](#part-7--taking-seo-to-the-next-level) |
| 8 | Country-specific price bina login | [Part 8](#part-8--country-specific-pricing) |
| — | Sab files ka summary | [Part 9](#part-9--every-file-that-changes) |

---

# PART 1 — THE MOBILE BUG

## Aapke screenshot mein exactly kya galat hai

Screenshot 1 mein saaf dikh raha hai:
- Sidebar (`$12` wala box) **screen se bahar nikal raha hai** — "Book a lesson" button kata hua hai
- "About me" column patla ho gaya hai, text bahut jaldi wrap ho raha hai
- Right side ka content viewport se bahar hai

Screenshot 2 mein:
- Content column **screen ki aadhi width** le raha hai, dayen taraf khaali jagah

**Yeh design ki galti nahi hai — yeh ek CSS cascade bug hai.**

## Asli wajah — maine code mein dhoond li

`css/style.css` mein `.pf-layout` (profile ka do-column grid) **teen jagah** define hua hai:

| Line | Rule | Kab lagta hai |
|---|---|---|
| 217 | `grid-template-columns: 1fr 340px` | Default (desktop) |
| **338** | `grid-template-columns: 1fr` | `@media (max-width:980px)` ✅ sahi |
| **921** | `grid-template-columns: 1fr 300px` | `@media (max-width:1024px)` ❌ |

**Problem:** 390px (iPhone) par **dono** media queries match karti hain — 390 < 980 bhi hai aur 390 < 1024 bhi.

CSS ka niyam: jab do rules ki specificity barabar ho, **file mein jo baad mein likha ho wo jeetta hai**.

Line 921, line 338 ke **baad** hai. Isliye phone par bhi `1fr 300px` lag jata hai — yaani do column, jabki phone par sirf ek column chahiye. 300px ka sidebar 390px ki screen par thusa jata hai, aur bahar nikal jata hai.

Yeh v3 mein aaya tha jab maine "small laptops" ka breakpoint add kiya — maine `max-width:1024px` likha, jabki `min-width` bhi lagana chahiye tha.

## Fix — teen line ka kaam

**File:** `css/style.css` — **sirf yahi ek file**

```css
/* Line 921 — abhi yeh hai (galat) */
@media (max-width:1024px){
  .pf-layout{grid-template-columns:1fr 300px;gap:26px}
}

/* Yeh hona chahiye — dono taraf se bandha hua */
@media (min-width:981px) and (max-width:1024px){
  .pf-layout{grid-template-columns:1fr 300px;gap:26px}
}
```

Ab yeh rule sirf 981px se 1024px ke beech lagega. Phone par kabhi nahi.

## Isi tarah ke aur conflicts jo maine dhoonde

Poori file scan ki. Yeh saare same pattern ke hain:

| Line | Rule | Kya hota hai | Fix |
|---|---|---|---|
| 921 | `.pf-layout` @1024 | **Phone par sidebar bahar** | `min-width:981px` add karo |
| 335 vs 934 | `.filters` do baar | Filter grid confuse | Ranges alag karo |
| 335 vs 954 | `.ftr-in` do baar | Footer column mismatch | Ranges alag karo |
| 343 vs 954 | `.sched` teen baar | Schedule column count | Ranges alag karo |
| 671/676 vs 934/954 | `.pf-photo` margin | Photo overlap thoda off | Consolidate |

**Root cause ek hi hai:** breakpoints time ke saath add hote gaye (v1 mein 980/720, v3 mein 1180/1024/900/640/400, v5 mein 1240/1180/1140/1080). Ab 31 media queries hain jinme se kai overlap karti hain.

## Behtar hal — sirf patch nahi, poora system

Main sujhaav deta hoon ki **ek hi breakpoint ladder** bana dein:

```css
/* EkGuru breakpoint system — har rule sirf EK band mein */
/*  XS   0    – 479px   phone (chhota)        */
/*  SM   480  – 767px   phone (bada)          */
/*  MD   768  – 1023px  tablet                */
/*  LG   1024 – 1279px  laptop                */
/*  XL   1280px+        desktop               */
```

Har rule `min-width` **aur** `max-width` dono ke saath — taaki kabhi overlap na ho:

```css
@media (min-width:768px) and (max-width:1023px){ /* sirf tablet */ }
@media (min-width:1024px) and (max-width:1279px){ /* sirf laptop */ }
```

Isse aaj ka bug bhi theek hoga aur aage kabhi dobara nahi hoga.

**Kitna kaam:** `css/style.css` ka responsive section rewrite — 31 media queries se ghatkar ~12. Baaki koi file nahi chhuni padegi.

---

# PART 2 — MOBILE REVIEW SLIDER

## Abhi kya hai

`js/main.js` line 508 par reviews aise banti hain:

```js
'<div class="rev">…</div>'   // har review ek block
```

CSS (line 255): `margin-bottom:14px` — yaani ek ke neeche ek, vertically stacked.

Sushila ke 3 reviews hain, har ek 4–6 lines ka. Phone par yeh **poori screen** kha jate hain, aur user ko scroll karke neeche jaana padta hai — jahan booking button hai. Yeh conversion ke liye bura hai.

## Jo main banana chahta hoon

Phone par reviews **horizontal swipe carousel** ban jayein. Desktop par jaise hain waise hi rahein.

**Kaise kaam karega:**

```
┌──────────────────────────┐
│  ⭐⭐⭐⭐⭐  Tomasz         │  ← ek card poori width ka
│  "Sushila is a very      │
│   patient teacher…"      │
│                          │
└──────────────────────────┘
      ● ○ ○     ← dots
   ← swipe karo →
```

**Technical approach — CSS scroll-snap** (koi library nahi, 0 KB extra):

```css
@media (max-width:767px){
  .rev-wrap{
    display:flex;
    overflow-x:auto;
    scroll-snap-type:x mandatory;   /* har card par ruk jaye */
    gap:12px;
    scroll-behavior:smooth;
    -webkit-overflow-scrolling:touch;
    scrollbar-width:none;            /* scrollbar chhupa do */
  }
  .rev-wrap::-webkit-scrollbar{display:none}
  .rev{
    flex:0 0 88%;                    /* agla card thoda jhaanke */
    scroll-snap-align:center;
    margin-bottom:0;
  }
}
```

`flex:0 0 88%` khaas hai — agla card ka 12% dikhta rehta hai, isse user ko pata chalta hai ki aur reviews hain. Yeh Instagram/Amazon wala trick hai.

**Plus features jo main jodunga:**

1. **Dots indicator** — kitne reviews hain, abhi kaunsa dikh raha hai
2. **Swipe hint** — pehli baar par card halka sa hilta hai (nudge animation), taaki user ko pata chale swipe ho sakta hai
3. **Keyboard support** — arrow keys se bhi chale (accessibility)
4. **Auto-height** — sabse lambe review ke hisaab se sab cards barabar
5. **"Read more"** — 4 line se lamba review ho to fold ho jaye, tap par khule

**Files:**
- `css/style.css` — carousel styles (~60 lines)
- `js/main.js` — reviews ko `<div class="rev-wrap">` mein lapetna (2 lines ka change)
- `js/features.js` — dots + swipe detection (~50 lines)

**Yeh teeno tutors par apne aap lag jayega** — kyunki rendering ek hi jagah se hoti hai (`renderProfile()`). Naye tutor add karoge to usko bhi automatically milega.

---

# PART 3 — MOBILE-FIRST THINKING

Aapne kaha "mobile ke liye thodi special socho". Maine poori site phone ki nazar se dekhi. Yeh mila:

## 3.1 Sticky booking bar — sabse bada impact

**Problem:** phone par profile page bahut lamba hai (banner → about → video → experience → method → subjects → schedule → reviews). Booking button sirf sabse upar hai. User neeche padhte-padhte pahunchta hai, convince ho jata hai — par button dikhta hi nahi.

**Hal:** neeche fixed bar, jo scroll karne par aata hai:

```
┌─────────────────────────────────┐
│  $12 / 50 min    [📅 Book now]  │  ← screen ke neeche chipka
└─────────────────────────────────┘
```

Tutor ki photo + price + button. Yeh Preply, Airbnb, Booking.com — sab karte hain, kyunki mobile conversion **30-50% badhta hai**.

## 3.2 Bottom sheet booking modal

Abhi booking modal beech mein khulta hai. Phone par native pattern **bottom sheet** hai — neeche se upar slide hoke aana, aur neeche swipe karke band karna.

```
        ↓ swipe down to close
┌─────────────────────────────────┐
│         ────                    │  ← grab handle
│  📅 Book with Hemlata           │
│  [time slots…]                  │
```

## 3.3 Collapsible sections

Phone par 7 khule hue panels bahut lambe lagte hain. Pehle 2 khule rahein (About, Video), baaki accordion:

```
▸ Experience          (tap to open)
▸ Teaching method
▸ What I teach
▸ Availability
▸ Reviews (3)
```

Page ki lambai **60% kam** ho jayegi.

## 3.4 Baaki mobile improvements

| # | Kya | Kyun |
|---|---|---|
| 1 | **Thumb-zone buttons** — important buttons screen ke neeche-beech mein | Phone ek haath se pakadte hain, upar pahunchna mushkil |
| 2 | **Tutor cards horizontal scroll** home par | 3 cards vertically 3 screen lete hain |
| 3 | **Schedule 3-col grid** phone par | Abhi 7 columns squeeze hote hain |
| 4 | **Sticky filter bar** search page par | Filter upar chala jata hai scroll karte hi |
| 5 | **Skeleton loaders** | Blank screen se behtar lagta hai |
| 6 | **Pull-to-refresh disable** | Galti se page reload na ho |
| 7 | **`100dvh` use karna** | Phone browser bar ke saath height badalti hai |
| 8 | **Tap feedback** | Button dabane par turant visual response |
| 9 | **Image `srcset`** | Phone par 1280px banner ki zarurat nahi, 640px kaafi — 60% data bachega |
| 10 | **Font preload** | Text pehle flash na kare |

## 3.5 Screenshot se ek aur cheez

Screenshot 2 mein **back-to-top button** aur **email FAB** dono ek doosre ke bahut paas hain (bottom-right). Ungli se galat wala dab sakta hai. Inhe alag karna chahiye — ya to spacing badhao, ya back-to-top ko left side karo.

---

# PART 4 — WHERE THE SEO LIVES

## Do files, do kaam

```
js/seo-engine.js   478 lines   24 KB   ← KEYWORDS banata hai
js/seo.js          612 lines   33 KB   ← META TAGS + SCHEMA likhta hai
```

## `js/seo-engine.js` — keyword factory

Isme **11 vocabulary lists** hain. Yeh multiply hoke lakhon combination banate hain:

| Line (approx) | Variable | Kitne | Kya hai |
|---|---|---|---|
| 44 | `ACTION` | 20 | learn, study, master, speak, practise… |
| 49 | `QUALITY` | 28 | best, top, affordable, cheap, native… |
| 53 | `SUBJECT` | 36 | hindi, hindi lessons, devanagari, grammar… |
| 62 | `ROLE` | 16 | tutor, teacher, guru, instructor… |
| 66 | `AUDIENCE` | 34 | for kids, for adults, for beginners… |
| 75 | `MODE` | 24 | online, on zoom, private, with trial… |
| 80 | `PLACE` | 25+ | near me, in usa, in uk, from india… |
| 86 | `PRICE` | 13 | cheap, under 5 dollars, free trial… |
| 90 | `TIME` | 12 | 2026, in 30 days, from scratch… |
| 94 | `QUESTION` | 34 | "how much do hindi lessons cost"… |
| 131 | `FOUNDER` | **90** | Prakash, MNIT, CSE, Kolwa, Dausa… |
| 210 | `PLATFORMS` | 31 | preply, italki, verbling, cambly… |
| 216 | `COMPARE` | 222 | "preply alternative", "cheaper than italki"… |
| — | `BRAND` | 17 | ekguru, ek guru, ekguru hindi… |

**Founder keywords** (line ~131) — aapke diye hue exact facts se:
- `FOUNDER` ke andar 4 group hain: `name` (14), `college` (24), `place` (32), `story` (20) = **90**
- Place group mein: `kolwa dausa`, `gothwal ki dhani kolwa`, `dausa 303325`, `kolwa railway station`, `prakash dausa`

**Aapko edit karna ho to:** in arrays mein word add/remove kar dijiye. Baaki sab apne aap adjust ho jayega.

## `js/seo.js` — page par likhta hai

| Line (approx) | Kya karta hai |
|---|---|
| ~120 | `COPY` — har page ka title aur description, 7 languages mein |
| ~200 | `meta()` — keywords, description, robots, og:, twitter: tags |
| ~230 | `hreflang` — 7 languages + x-default |
| ~280 | JSON-LD `@graph` — saare schema types |
| ~350 | Founder ka `Person` schema (MNIT, birthPlace) |
| ~420 | `HowTo` schema |
| ~450 | `Speakable` schema |

---

# PART 5 — EXACT KEYWORD COUNTS

Maine abhi measure kiya, ye asli numbers hain:

| Page | Generate hue | Tag mein gaye | Characters |
|---|---|---|---|
| index.html | 398 | 108 | 2,389 |
| find-tutors.html | 397 | 108 | 2,389 |
| join.html | 212 | 108 | 2,389 |
| tutor: sushila-g | 300 | 108 | 2,389 |
| tutor: hemlata | 300 | 108 | 2,389 |
| tutor: tara | 282 | 108 | 2,389 |

**Combination space:** 12,668,831 (7 languages ke saath)
**Per language:** 1,809,833

## ⚠️ Ek bug jo mujhe abhi mila

Dekhiye — **har page ke tag mein wahi 108 keywords ja rahe hain.**

Maine test kiya: index, find-tutors, aur hemlata — teeno ka keyword tag **bilkul identical** hai, saare 108 positions same.

**Kyun:** v5 mein maine ordering ko "balanced core" banaya tha — brand + founder + head terms + comparison. Wo core **300+ phrases ka ho gaya**, aur 2400-character limit usi core mein khatam ho jati hai. Page-specific slice (`out`) kabhi likha hi nahi jata.

Pichli baar mera test pass ho gaya tha kyunki main `<meta>` ka content compare kar raha tha, jisme page-specific `c.k` bhi juda hua tha — wo alag tha, isliye "unique" dikha. Engine ka output actually same hai.

**Fix:** har page ke liye core ko chhota karke (30-40 phrases) baaki jagah page-specific keywords ko deni hogi. Ya limit badha kar 4000 characters kar dein.

Yeh `js/seo-engine.js` mein `forPage()` function ka ~15 line ka change hai.

---

# PART 6 — WHY YOU ARE NOT IN SEARCH (THE REAL ANSWER)

Aapne pucha "abhi bhi search mein nahi dikh raha". Maine deep jaanch ki. **Teen wajah hain, aur SEO keywords unme se ek bhi nahi hai.**

## ⚠️ Wajah 1 — Site abhi deploy hi nahi hui

Sabse pehli baat: `https://ek-guru.github.io/Preply/` **abhi live hai ya nahi?**

Agar aapne GitHub par upload nahi kiya, ya Pages on nahi kiya, to Google ke paas dhoondhne ke liye kuch hai hi nahi. Keywords, schema, sitemap — sab bekaar hai agar page internet par maujood hi nahi.

**Check kaise karein:** browser mein URL kholiye. Site dikhti hai? Nahi to `DEPLOY.md` follow kijiye.

## ⚠️ Wajah 2 — Naya domain = 2 se 12 hafte lagte hain

Yeh normal hai, koi galti nahi:

| Kab | Kya hota hai |
|---|---|
| Din 1–3 | Google ko pata bhi nahi ki aap exist karte ho |
| Hafta 1–2 | Crawler aata hai (agar sitemap submit kiya ho) |
| Hafta 2–4 | Brand name par dikhna shuru — "ekguru" |
| Mahina 2–3 | Long-tail phrases |
| Mahina 6+ | Competitive terms |

**Tezi lane ka ek hi tarika:** Google Search Console mein **manually "Request indexing"** dabana. Ye 2-4 hafte bacha deta hai. `DEPLOY.md` Part 4 mein steps hain.

## 🔴 Wajah 3 — YEH SABSE BADI HAI: JavaScript rendering

Maine test kiya ki **JavaScript ke bina** aapke page par kya dikhta hai. Google ka crawler pehle yahi dekhta hai:

| Page | JavaScript ke bina kitne words |
|---|---|
| index.html | 183 words |
| **tutor.html** | **48 words** 🔴 |
| find-tutors.html | ~90 words |

**48 words.** Aur wo bhi sirf header aur footer ka text. Tutor ka naam nahi, bio nahi, price nahi, reviews nahi — kuch bhi nahi.

**Aisa kyun:** aapki site ka saara content `js/main.js` banata hai, browser mein. HTML file mein sirf khaali `<div id="profile">` hai.

**Google kya karta hai:**
1. Pehla pass — HTML padhta hai. 48 words milte hain. "Yeh page khaali hai."
2. Doosra pass — JavaScript chalata hai. **Par ye kabhi kuch din baad hota hai, aur hamesha nahi hota.**
3. Bing, DuckDuckGo, aur zyadatar AI crawlers — **JavaScript chalate hi nahi.**

**Iska matlab:** aapke 12 million keywords, 12 schema types, 90 founder phrases — sab `<head>` mein hain aur wo Google padh lega. Lekin **asli content** (jo actually rank karata hai) crawler ko dikhta hi nahi.

### Hal — Static HTML pre-rendering

Har tutor ke liye ek **asli HTML file** banani hogi, jisme content pehle se likha ho:

```
Abhi:                          Hona chahiye:
tutor.html?id=hemlata     →    tutor/hemlata/index.html
tutor.html?id=sushila-g   →    tutor/sushila-g/index.html
tutor.html?id=tara        →    tutor/tara/index.html
```

Har file mein Hemlata ka naam, bio, price, schedule, reviews — **HTML mein likhe hue**, JavaScript ke bina bhi dikhne wale.

**Kaise banega:** ek chhota Node script (`build/prerender.js`) jo `tutors-data.js` padhkar HTML files generate kar de. Aap `node build/prerender.js` chalayenge, files ban jayengi, aur wahi GitHub par upload hongi.

**Ye single sabse bada SEO improvement hai.** 48 words se 800+ words per page.

**Bonus:** aapka `js/tutors-data.js` wala workflow bilkul same rahega. Script sirf usse padhta hai.

## Wajah 4 — Backlinks zero hain

Google ka sabse bada ranking signal: kitni doosri sites aapko link karti hain. Abhi **zero**.

**Aaj hi ye kar sakte hain (free, 30 minute):**

| Kahan | Kaise | Value |
|---|---|---|
| **Preply profile** | Description mein site ka link | ⭐⭐⭐⭐⭐ same topic |
| **YouTube** | Channel About + har video description | ⭐⭐⭐⭐⭐ |
| Instagram/Facebook bio | Link daaliye | ⭐⭐⭐ |
| LinkedIn | Aapki profile mein "Founder, EkGuru" + link | ⭐⭐⭐⭐ |
| Reddit r/Hindi, r/languagelearning | Helpful comment, spam nahi | ⭐⭐⭐ |
| Quora | "How to learn Hindi" wale sawaalon par jawab | ⭐⭐⭐ |
| Product Hunt | Launch kijiye | ⭐⭐⭐⭐ |
| BetaList / IndieHackers | Startup listing | ⭐⭐⭐ |

**Ek Preply backlink 10 lakh keywords se zyada karega.** Ye main seriously keh raha hoon.

## Sachai — priority order

| # | Kaam | Asar | Kaun karega |
|---|---|---|---|
| 1 | Site actually deploy karo | 🔴 bina iske kuch nahi | Aap |
| 2 | Search Console + Request indexing | 🔴 2-4 hafte bachate hain | Aap |
| 3 | **Static HTML pre-render** | 🔴 48 → 800 words | **Main** |
| 4 | Preply/YouTube backlink | 🔴 sabse bada signal | Aap |
| 5 | Hemlata/Tara ki asli bio + reviews | 🟠 asli content | Aap |
| 6 | Aur keywords | ⚪ **lagbhag zero** | — |

Google ne 2009 mein keywords meta tag ko ranking se hata diya tha. Wo aaj bhi Bing aur AI crawlers ke liye useful hai, isliye maine banaya — par **wo rank nahi karata**. Content, speed aur links karate hain.

---

# PART 7 — TAKING SEO TO THE NEXT LEVEL

Agar aap chahte hain to yeh sab bana sakta hoon. Impact ke hisaab se sorted:

## Tier 1 — Sabse zyada asar

### 7.1 Static pre-rendering (Part 6 wala)
Har tutor ka asli HTML page. **48 words → 800+ words.**

### 7.2 Language-specific HTML pages
Abhi `?lang=es` sirf ek URL parameter hai — Google ke liye wahi page hai.

```
es/index.html      ← asli Spanish page
fr/index.html      ← asli French page
ja/index.html      ← asli Japanese page
```

**5 pages × 7 languages = 35 asli pages** Google ko indexing ke liye. Abhi 5 hain.

### 7.3 Content pages — jahan asli traffic aata hai

Tutoring sites ka 70% traffic informational content se aata hai, tutor pages se nahi:

| Page | Kya keyword target karega |
|---|---|
| `/learn-hindi-for-beginners/` | "how to learn hindi for beginners" |
| `/devanagari-alphabet-guide/` | "hindi alphabet chart", "devanagari letters" |
| `/hindi-greetings/` | "how to say hello in hindi" |
| `/hindi-numbers-1-100/` | "hindi numbers" |
| `/hindi-vs-urdu/` | "difference between hindi and urdu" |
| `/how-long-to-learn-hindi/` | "how long does it take to learn hindi" |
| `/hindi-for-travel-india/` | "useful hindi phrases for travel" |
| `/best-way-to-learn-hindi/` | "best way to learn hindi" |

Har page 800-1500 words. Yeh **asli, useful content** hoga — aur har page ke end mein "Book a lesson with our tutors" CTA.

10 aise pages = 10 naye entry points Google mein.

## Tier 2 — Technical

### 7.4 RSS/Atom feed
Naye tutors aur content ke liye. AI crawlers aur aggregators isko pasand karte hain.

### 7.5 `llms.txt`
Naya standard — AI assistants ko batata hai aapki site kis baare mein hai:
```
# EkGuru
> Online Hindi tutoring with verified native tutors from India.
## Tutors
- Sushila G. — $3/50min — beginner to advanced
- Hemlata — $12/50min — kids, adults, beginners
```

### 7.6 Image SEO
- Har image ka descriptive filename
- `srcset` — phone ke liye chhoti image
- WebP/AVIF format — 40% chhoti files
- `ImageObject` schema

### 7.7 Aur schema types
Abhi 12 hain. Ye add kar sakte hain:
- `Event` — free webinar/demo class
- `Offer` with `priceValidUntil` — launch discount
- `AggregateOffer` — "lessons from $3 to $12"
- `SoftwareApplication` — agar app banayein
- `LocalBusiness` — Jaipur address ke saath

## Tier 3 — Content strategy

### 7.8 Har tutor ke liye unique long-form bio
Abhi Hemlata aur Tara ki bio placeholder hai (maine likhi hai). Google duplicate/thin content pakad leta hai.

**Har tutor ke liye 300+ words unique** — unke apne shabdon mein.

### 7.9 Review schema properly bharna
Jaise-jaise asli reviews aayein, `rating` aur `reviewsCount` update karte rahiye. Google ⭐ stars dikhayega — CTR **35% tak** badhta hai.

### 7.10 Video SEO
Har tutor ka intro video YouTube par, proper title/description ke saath, aur site par embed. YouTube khud duniya ka doosra sabse bada search engine hai.

---

# PART 8 — COUNTRY-SPECIFIC PRICING

Aapka sawaal: **bina login ke country-specific price kaise dikhayein?**

Achhi khabar — bilkul ho sakta hai, aur bina kisi server ke.

## Browser bina backend ke ye jaan sakta hai

Maine test kiya:

| Method | Kya milta hai | Accuracy | Cost |
|---|---|---|---|
| `Intl.DateTimeFormat().resolvedOptions().timeZone` | `Asia/Kolkata`, `America/New_York` | ~95% | free, instant |
| `navigator.language` | `en-IN`, `de-DE`, `pt-BR` | ~85% | free, instant |
| `Intl.NumberFormat` | Currency format karna | 100% | free, built-in |
| IP geolocation API | Exact country | ~99% | free tier, network call |

**Sabse achha:** timezone + language dono milakar. Ye **zero network call** hai, instant hai, aur private hai.

Maine verify kiya ki `Intl.NumberFormat` sahi format deta hai:
- `de-DE` + EUR → `11,50 €`
- `en-IN` + INR → `₹1,000`

## Design — 3 options

### Option A: Sirf currency convert karo (recommended)
Price wahi rahe, sirf local currency mein dikhe:

```
🇮🇳 India ke user ko:     ₹1,000  ($12)
🇺🇸 USA ke user ko:       $12
🇩🇪 Germany ke user ko:   €11  ($12)
🇯🇵 Japan ke user ko:     ¥1,800  ($12)
```

Chhote akshar mein USD bhi dikhega, taaki transparency rahe.

**Faayda:** user ko turant samajh aata hai. Studies mein local currency dikhane se conversion **20-30% badhta hai**.

**Rates kahan se:** `js/site-config.js` mein manually likhe hue (aap mahine mein ek baar update karein). Ya free API se live (network call lagega).

### Option B: Country ke hisaab se alag price
Purchasing power ke hisaab se:

```js
regionPricing: {
  IN: 0.35,   // India — 35% price (₹350 instead of ₹1000)
  US: 1.0,    // USA — full
  GB: 1.0,
  DE: 0.9,
  BR: 0.5,
  JP: 1.0,
  AE: 0.9,
  default: 1.0
}
```

Yeh Netflix/Spotify wala model hai. Ek Indian student ke liye $12 bahut hai, par $4 theek hai.

**Dhyan dein:** yeh tutor ki kamai badalta hai, isliye tutor se pooch lena chahiye.

### Option C: Dono — auto-detect + manual switcher
Auto-detect karo, aur header mein currency switcher bhi do (🌐 globe ke bagal mein), taaki user badal sake.

## Technical implementation

**Nayi file:** `js/pricing.js` (~150 lines)

```js
// 1. Country detect karo
function detectCountry() {
  // timezone se — sabse reliable
  var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
  // Asia/Kolkata -> IN, America/New_York -> US
  var fromTz = TZ_TO_COUNTRY[tz];
  if (fromTz) return fromTz;
  // fallback: browser language se
  var loc = navigator.language;         // "en-IN"
  var m = /-([A-Z]{2})$/.exec(loc);
  return m ? m[1] : "US";
}

// 2. Currency format karo
function formatPrice(usd, country) {
  var cur = COUNTRY_CURRENCY[country] || "USD";
  var rate = RATES[cur] || 1;
  return new Intl.NumberFormat(navigator.language, {
    style: "currency", currency: cur,
    maximumFractionDigits: cur === "INR" || cur === "JPY" ? 0 : 2
  }).format(usd * rate);
}
```

**`js/site-config.js` mein add hoga:**

```js
pricing: {
  mode: "currency",        // "currency" | "regional" | "off"
  showUsdAlso: true,       // "₹1,000 ($12)" dikhaye
  allowManualSwitch: true, // header mein switcher
  rates: {                 // 1 USD = kitna
    INR: 83, EUR: 0.92, GBP: 0.79, JPY: 150,
    AED: 3.67, BRL: 5.0, CAD: 1.36, AUD: 1.52
  },
  regional: {              // Option B ke liye
    IN: 0.35, BR: 0.5, default: 1.0
  }
}
```

**Files jo badlengi:**
| File | Kya |
|---|---|
| `js/pricing.js` | **nayi** — detection + formatting |
| `js/site-config.js` | pricing config block |
| `js/main.js` | 4 jagah `CUR + price` ki jagah `formatPrice()` |
| `js/features.js` | booking modal + search dropdown mein |
| `js/seo.js` | schema mein `priceCurrency` |
| `css/style.css` | currency switcher ke styles |
| `js/i18n.js` | switcher ke labels, 7 languages |

**Important:** schema (Google ke liye) hamesha **USD** mein rahega — kyunki wo canonical price hai. Sirf display badlega.

---

# PART 9 — EVERY FILE THAT CHANGES

Agar aap sab kuch karwana chahein:

| # | Kaam | Files | Naya kaam |
|---|---|---|---|
| 1 | **Mobile layout bug** | `css/style.css` | Breakpoint ladder rewrite |
| 2 | **Review slider** | `css/style.css`, `js/main.js`, `js/features.js` | ~110 lines |
| 3 | **Sticky booking bar** | `css/style.css`, `js/features.js` | ~80 lines |
| 4 | **Bottom sheet modal** | `css/style.css`, `js/features.js` | ~60 lines |
| 5 | **Collapsible sections** | `js/main.js`, `css/style.css` | ~50 lines |
| 6 | **Keyword bug fix** | `js/seo-engine.js` | ~15 lines |
| 7 | **Static pre-render** 🔴 | `build/prerender.js` **naya** + all HTML | ~300 lines |
| 8 | **Language pages** | `build/prerender.js` | 35 pages generate |
| 9 | **Content pages** | 8-10 nayi HTML files | Bada kaam |
| 10 | **Country pricing** | `js/pricing.js` **naya** + 6 files | ~200 lines |
| 11 | **llms.txt + RSS** | 2 nayi files | ~40 lines |
| 12 | **Image srcset/WebP** | `images/` + `js/main.js` | Rebuild images |

## Meri sifarish — is order mein

**Aaj (jaldi, bada asar):**
1. Mobile layout bug — screenshot wala, 10 minute
2. Keyword bug — 10 minute
3. Review slider — mobile UX
4. Sticky booking bar — conversion

**Phir (sabse bada SEO asar):**
5. Static pre-rendering — 48 words se 800+

**Uske baad:**
6. Country pricing
7. Language pages
8. Content pages

**Aap jo bhi kahein, main wo pehle karunga.** Ya sab ek saath — jo aap chahein.

---

# 📌 SUMMARY — 30 SECOND

| Aapka sawaal | Jawab |
|---|---|
| Mobile kaise fix hoga | `css/style.css` — line 921 par `min-width:981px` add karna. Ek line ka bug hai. |
| Reviews slide | CSS scroll-snap carousel, 0 KB library. 3 files, ~110 lines. Teeno tutors par apne aap. |
| SEO kahan hai | `js/seo-engine.js` (keywords banata hai) + `js/seo.js` (page par likhta hai) |
| Kitne keywords | 12,668,831 combinations · har page 108 tag mein · **par abhi sab pages par same ja rahe hain — bug hai** |
| Search mein kyun nahi | 1) Site deploy hui? 2) Naya domain = 2-12 hafte 3) **tutor.html mein JS ke bina sirf 48 words hain** 4) Zero backlinks |
| Next level | Static pre-rendering (sabse bada), language pages, content pages |
| Country pricing | Ho sakta hai, bina server. Timezone + `Intl.NumberFormat`. Nayi file `js/pricing.js`. |

**Sabse zaroori do baatein:**
1. **Site deploy kijiye** aur Search Console mein "Request indexing" dabaiye
2. **Preply profile mein link daaliye** — ek backlink 10 lakh keywords se zyada hai

---

© EkGuru — One Student. One Guru. One Goal.
Research by your agent · Nothing changed, analysis only
