# EkGuru: visitors kaise aayenge. Diagnosis, mera decision, 30 din ka plan

24 Nov 2026. PRIVATE (sirf owner ke liye). Repo mein kuch change nahi kiya.

## 1. Seedha jawab

Problem site ke andar nahi hai. Problem **discovery** hai: site naya hai, kisi ne link nahi diya, aur Google ko shayad site dikh hi nahi rahi. Isliye "aur pages bana do" se visitor nahi aayenge. Maine decide kiya:

| # | Kya karna hai | Kaun karega | Kitna time |
|---|---|---|---|
| 1 | **Naapna aur index karwana**: GoatCounter ke asli numbers, Search Console mein index status, Cloudflare check | Owner | 30 min, ek baar |
| 2 | **Share cover badalna**: abhi "Verified native tutors" likha hai, jo site ke apne disclaimer se takrata hai | Owner (file ready hai) | 5 min |
| 3 | **Naye auto-generated pages band** (30 din): jo pages hain unhi ko dikhao | Sab (arena sessions bhi) | 0 |
| 4 | **Visitors ko bulana**: 2 logon ko, 4 jagah se (neeche) | Owner + 17 tutors | roz 30-40 min |

Main khud Reddit, Instagram, WhatsApp par post nahi kar sakta (mere paas un accounts ka access nahi hai). Isliye har post ka text taiyar hai, copy-paste mein 2 minute lagte hain: `DISTRIBUTION-KIT-2026-11-24.md`.

## 2. Kya pata chala (evidence aur kitna bharosa)

| Baat | Source | Bharosa |
|---|---|---|
| 18 Nov se pehle GoatCounter par 1 se 3 visit/din tha, jabki Cloudflare par ~2,000 requests/din (zyadatar bots). Counter hi sahi load nahi ho raha tha | Repo ka commit `aebda1330` | Pakka. 18 Nov se counter default-on hai, to ab asli numbers GoatCounter mein dekho |
| `ekguru.shop` apne exact title ("Learn Hindi Online — Free Course \| EkGuru") aur domain naam search par bhi nahi aata | Meri web search | **Kamzor sabut**: ye Google nahi hai. Search Console se confirm karo |
| Hindi ke head keywords par Udemy, HindiPod101, Multibhashi, Ling, Memrise, Preply, Superprof pehle se hain | Search results | Pakka |
| Marathi, Gujarati, Kannada ke "free beginners" search mein zyada Udemy listing, 50languages aur Ling hain, koi bada free structured course nahi dikha | Search results (sirf titles dekhe) | Medium. Ye "kam competition" ka sanket hai, saboot nahi |
| Site par ~2,761 pages hain, 1,029 indexable, zyadatar templates se bane | `data/quality/full-page-inventory.json` | Pakka. Naye domain par itne template pages ka asar Search Console se hi pata chalega |
| Live-guard aur course-health weekly workflows lagatar fail ho rahe hain; `main` par CI 23 Nov ko red hai (4 "days-and-months-in-*" pages stale) | GitHub Actions | Pakka |
| Share cover par "Verified native tutors", "7 languages", ek tutor ki photo hai | `images/og-cover.jpg` | Pakka |

**Jo mujhe nahi pata** (aur isliye plan mein pehle check hai): Search Console mein kitne pages indexed hain, Googlebot ko Cloudflare rok raha hai ya nahi, aur ab GoatCounter mein kitne visit hain. GoatCounter dashboard mere liye robots se band hai.

## 3. Maine kya decide kiya

### Kise bulana hai (priority order)

| Rank | Audience | Kyun | Kahan milte hain | Site par kahan bhejna |
|---|---|---|---|---|
| 1 | **India mein shift hue log jo local language seekhna chahte hain** (Pune, Mumbai, Hyderabad, Chennai, Ahmedabad, Kolkata, Chandigarh). Bengaluru abhi nahi, kyunki Kannada course ready nahi hai | Competition kam, aapki Indian-language courses sabse alag cheez hain, tutors bhi India mein hain | r/pune, r/mumbai, r/hyderabad, r/chennai, r/gujarat, r/kolkata, r/punjab (har subreddit ke rules pehle padho); Quora; WhatsApp/Facebook "relocation" groups; YouTube Shorts | `/learn/marathi/`, `/learn/gujarati/`, `/learn/tamil/`, `/learn/telugu/`, `/learn/bengali/`, `/learn/punjabi/`, `/learn/urdu/` |
| 2 | **Videsh mein bachchon ko Hindi sikhane wale NRI parents** | Paise dene ko taiyar, tutors ki zaroorat, Preply par bhi yahi log hain | Hindi schools, mandir ke Hindi classes, Facebook parent groups, r/hindi, r/ABCDesis | `/hindi-tutor/`, `/learn/hindi/` (free pehle), `/find-tutors.html` |
| 3 | Hindi seekhne wale videshi (partner, travel, kaam) | Bada hai par sabse zyada competition | r/hindi, r/languagelearning | Baad mein. 30 din mein sirf comment/reply, naye pages nahi |

Ek honest baat: **Kannada** shayad sabse zyada maangi jaane wali relocation language hai (Bengaluru), par `/learn/kannada/` aur `/learn/malayalam/` abhi noindex aur adhure hain. Inhe promote mat karo. Kannada A1 aur A2 ko native reviewer ke saath poora karna sabse achhi content investment hai.

### Kya band karna hai
- **30 din tak koi naya auto-generated page nahi** (country, daily phrases, speaker pages). Pichle hafte 196 aur country pages bane. Naye domain par yeh "bahut saare pages, koi link nahi" wala pattern hai. Jo pages hain unhe link, share aur index karwao.
- Paid ads ya backlink kharidna nahi.

### Sabse tez channel: aapke 17 tutors
Har tutor ke paas apna WhatsApp status, Instagram, aur jaan-pehchaan wale hain. Ek tutor se 10 asli visit bhi aaye to 17 tutors = 170. Tutor share kit kit file mein hai. Aap bol chuke ho ki student milne mein time lagega; ye wahi kaam hai jo time bachata hai.

## 4. Pehle 30 minute (sirf owner kar sakta hai)

1. **GoatCounter**: `ekguru.goatcounter.com` kholo. Settings → "Allow viewing without login" on karo. Last 7 din ka screenshot bhejo (Pages, Referrers, Countries). Isse asli number pata chalega.
2. **Search Console** → URL Inspection → `https://ekguru.shop/` → **Test live URL**. Agar "Page fetch: Failed" ya "Blocked" aaye, to Cloudflare Googlebot ko rok raha hai: Cloudflare → Security → Bots → "Bot Fight Mode" off karke dobara test karo. Ye sabse bada ek hi kaaran ho sakta hai.
3. **Search Console → Pages (Indexing)**: Indexed, "Discovered – currently not indexed", "Crawled – currently not indexed" ki sankhya note karo. Agar zyadatar "not indexed" mein hain, to pehle trim karna hai (section 6).
4. **Sitemaps**: sirf `https://ekguru.shop/sitemap-index.xml` submit karo. (Mera pehle wala `sitemap.xml` + `sitemap-places.xml` wala salah purana hai; robots.txt ab index batata hai.)
5. **URL Inspection → Request indexing** (roz ~10 limit) in pages ke liye, roz 2 se 3:
   `/`, `/learn/`, `/learn/hindi/`, `/learn/marathi/`, `/learn/gujarati/`, `/learn/tamil/`, `/learn/telugu/`, `/learn/bengali/`, `/name-in-hindi/`, `/toolbox/`
6. **Bing Webmaster Tools**: Search Console se import karo. 2 minute, aur Bing/DuckDuckGo/ChatGPT search ka rasta khulta hai.
7. **Social profiles**: `@ekguru_india` (YouTube, X), `ekguru.in` (Instagram), Facebook page, LinkedIn: kya inpar ek bhi post hai? Khaali profile par jaane wale ko trust nahi hota. Kam se kam 3 post daalo (kit mein).
8. **Cover badlo**: `og-cover-new.jpg` ko `images/og-cover.jpg` ki jagah rakho (aur `og-cover.webp` ki bhi). Facebook Sharing Debugger se "Scrape again" karo.

## 5. 30 din ka sprint

Roz 30 se 40 minute. Har hafte ek channel dominant.

| Hafta | Focus | Roz ka kaam | Hafta ke ant mein check |
|---|---|---|---|
| 1 | Index + tutors | Section 4 ke kaam. 17 tutors ko share kit bhejo (WhatsApp). Roz 2 se 3 URL "Request indexing" | Search Console: indexed count. GoatCounter: referrers |
| 2 | Reddit + Quora (audience 1) | Roz 1 helpful comment ya answer (link sirf jahan madad kare). Hafte mein 2 post | Kaunsa post chala, kitne visit aaye |
| 3 | Short video (audience 1 aur 2) | 3 Shorts/Reels hafte mein, ek hi 30-second format, kit ki scripts | Views aur profile clicks |
| 4 | Backlinks (outreach) | Roz 3 email: university language centres, Hindi schools, blogger. Template kit mein | Kitne reply, kitne link mile |

### Decision rules (ye khud lagao)
- 14 din ke baad GoatCounter referrers dekho. **Jo channel sabse zyada visit de, usse double karo. Jo 0 de, 3 attempt ke baad chhod do.**
- 4 hafte baad agar Search Console mein "not indexed" pages 70% se zyada hain, to site ko ~150 sabse achhe pages tak trim karne ka plan banao (baaki noindex). Ye tabhi, data dekh kar.
- Agar section 4 step 2 mein fetch failed aaye, baaki sab rok do aur pehle wo thik karo.

### Realistic umeed (mera andaza, data nahi)
Agar indexing theek hai aur 17 tutors + 8 se 10 achhe community posts hote hain, to pehle hafte mein 20 se 200 visit aa sakte hain. Search se pehle clicks aksar indexing ke 4 se 12 hafte baad aate hain, aur tabhi jab doosri sites se kuch links mil chuke hon. Tutor bookings pehle mahine mein shayad 0 se 3. Isse zyada ka vaada koi nahi kar sakta.

## 6. Repo mein kaun se changes chahiye (aap karoge, ya jab bolo main PR bana dunga)

| # | Change | Kyun |
|---|---|---|
| a | `images/og-cover.jpg` aur `.webp` badlo (file taiyar) | "Verified native tutors" claim, site ke disclaimer se takrata hai |
| b | `python3 tools/build-time-pages-bodies.py` chalao, commit karo | `main` par CI red hai (days-and-months-in-gujarati, kannada, telugu, urdu stale) |
| c | `find-tutors.html` mein static tutor cards ya isko noindex karke `/tutor/` ko canonical banao | Abhi 0 static cards, 38 scripts; crawler ko khaali list dikhti hai |
| d | `.github/workflows/live-guard.yml` ko Cloudflare-safe banao ya GitHub runner IP allow karo | Har hafte fail hota hai, isliye asli problem chhup jaati hai |
| e | `og:image:alt` "free, self-paced Hindi learning" 31 pages par hai (`start/`, `languages/` aur 29 language hubs, jaise `languages/de/`). Ye meri PR #52 ki galti hai | Alt text page ke hisaab se hona chahiye. `tools/build-phase7-pages.py` ka template badlo |
| f | PR #63 (meri purani docs PR) band karo, ye 18 Nov se pehle ke data par hai aur conflict mein hai | Purana data |
| g | Site par kahin nahi likha ki EkGuru tutor lessons par commission nahi leta (about, terms, find-tutors mein dhoondha). Agar ye aapka asli USP hai (Preply/Superprof se alag), to About aur Find-tutors par likho, **phir** posts mein bolo | Bina likhe claim mat karo |

## 7. Aapke baar-baar poochhne wali baat

"Kise bulaoge": audience 1 (India mein local language seekhne wale) aur audience 2 (NRI parents), 17 tutors ke zariye aur 4 channels se. "Kise fix karoge": pehle measurement aur indexing, phir cover, phir naye pages band. Jab GoatCounter aur Search Console ke numbers mil jayenge, main isi plan ko un par tika kar dobara decide kar dunga.
