# EkGuru — Google AdSense APPROVAL Master Plan
### (Audit Report + Phase-wise Agent Commands — GitHub connected agent ke liye)

**Site:** https://ekguru.shop · **Repo:** `EkGuruLearning/EkGuru` · **AdSense Publisher ID:** `ca-pub-8175326569491671` / `pub-8175326569491671` · **Audit date:** 2026-09-28

---

# 📋 PART A — AUDIT REPORT (maine kya-kya check kiya)

## ✅ Jo SAHI hai (inhe touch mat karna)

| # | Cheez | Status | Detail |
|---|-------|--------|--------|
| 1 | `ads.txt` | ✅ PASS | Root pe hai: `google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0` — live 200 OK |
| 2 | Custom domain | ✅ PASS | `CNAME` = `ekguru.shop`; purana `ekgurulearning.github.io` 301 redirect karta hai |
| 3 | Canonical tags | ✅ PASS | 2635/2638 pages `https://ekguru.shop` pe point karte hain. Sirf 3 utility pages (admin, GSC-verify, email-preview) bina canonical — ye theek hai |
| 4 | Sitemaps | ✅ PASS | 15 child sitemaps + index, sab URLs ekguru.shop pe, **0 dead URLs** (sitemap ka har URL disk pe exist karta hai) |
| 5 | robots.txt | ✅ PASS | Crawling allowed; sirf `/admin.html`, `/tools/`, `/search/` blocked |
| 6 | Policy pages | ✅ PASS | `about`(768 words), `contact`(577), `privacy`(967), `terms`, `disclaimer`, `cookie-policy`, `copyright`, `monetization-disclosure`, `faq`, `support` — **sab exist karte hain** (AdSense ke liye zaroori) |
| 7 | Internal link wiring | ✅ PASS | Maine **1,52,153 internal links** crawl kiye — sirf 2 issues: (a) `admin.html` me `href=".."`, (b) `daily-hindi/index.html` line 216 me JS-template link `"../daily-hindi/day-"+nextDay+"/"` — ye runtime-generated hai, static bug NAHI |
| 8 | GSC verification | ✅ PASS | `googleb3b0e3defc1daa17.html` file live hai |
| 9 | Publisher ID consistency | ✅ PASS | Sab jagah ek hi ID: `ca-pub-8175326569491671` |
| 10 | CI/CD | ✅ PASS | GitHub Actions (`ci.yml`) me readiness gates hain: `build-all.py check` → `inject-ads.py --check`, `adsready.js --local`, `audit-adsense-readiness.py` |
| 11 | Page classes | ✅ PASS | Har page `<html data-ad-class="...">` pe class declare karta hai (inject-ads ne likha) |
| 12 | Ad-infrastructure code | ✅ PASS | `tools/inject-ads.py` (policy engine), `js/monetization.js`, `js/cookie-consent.js` — sab bane hue hain, sirf OFF hain |

## ❌ Jo GALAT / BAND hai (yahi approval nahi dene dega)

| # | Problem | Kahan | Kya hai abhi | Kya hona chahiye |
|---|---------|-------|--------------|------------------|
| **1** | **🚨 AdSense loader KISI page pe nahi hai** | `data/monetization/google-monetization.json` | `"loader_allowed": []` ← **KHAALI array** | `["HIGH_CONTENT", "MEDIUM_CONTENT"]` |
| **2** | **🚨 `google-adsense-account` meta tag 0 pages pe** | pura repo | 0 / 2638 pages | inject-ads.py chalane pe ~800 pages pe aa jayega |
| **3** | Runtime kill-switch OFF | `js/monetization.js` line 15 | `ADS_RUNTIME_ENABLED = false` | Approval ke BAAD hi true karna (Phase 5) |
| **4 | Advertising consent OFF | `js/cookie-consent.js` | `ADVERTISING_AVAILABLE = false` | Phase 5 me decide hoga (certified CMP) |
| 5 | `approval_status` | `google-monetization.json` | `"NOT_READY_DO_NOT_APPLY"` | `"APPLIED_AWAITING_GOOGLE_REVIEW"` |
| 6 | adsready.js ka regex bug | `tools/adsready.js` line 134 | `rel="canonical"\s+href=` order maangta hai, lekin HTML me `href` pehle hai → **false fail** (asal me canonical SAHI hai) | order-agnostic regex |
| 7 | ⚠️ Duplicate content risk | 965 pages | 304 repeated-paragraph groups, 5 template-intro groups — **"low value content" rejection ka #1 risk** | Phase 3 me unique karana |
| 8 | ⚠️ 1601 pages noindex | pura repo | Sitemap me sirf 1008 URLs | Ye INTENTIONAL hai — touch nahi karna, sirf verify |

## 🔍 Page-class counts (inject-ads.py --report se)

```
HIGH_CONTENT           455 pages  ← loader yahan jayega
MEDIUM_CONTENT         356 pages  ← loader yahan jayega
INTERACTIVE_LEARNING   186 pages  ← kabhi ads nahi (quiz/courses)
RESEARCH_REQUIRED     1628 pages  ← kabhi ads nahi (noindex/draft)
TRANSACTIONAL            3 pages  ← kabhi ads nahi (contact/join/support)
UTILITY                  8 pages  ← kabhi ads nahi (404/search/cookie-policy)
ADMIN                    1 page   ← kabhi ads nahi
```

## 🎯 Verdict (ek line me)
> **Site ka AdSense infrastructure 100% bana hua hai lekin policy `loader_allowed: []` ki wajah se Google ka code KISI page pe load nahi hota. AdSense ko "code not found" milega. Isko ON karna + duplicate content kam karna = approval ke 2 asli kaam.**

---

# 🚀 PART B — PHASE-WISE AGENT COMMANDS

## Ise kaise use karna hai:
1. Nayi chat kholo jisme agent ke paas **GitHub access** ho (write access to `EkGuruLearning/EkGuru`).
2. **Ek baar me EK PHASE** ka command box copy-paste karo.
3. Har phase ke end me agent ko report mangwayo (command me likha hai kya report chahiye).
4. Agla phase TABHI shuru karo jab pichla phase "acceptance criteria PASS" bole.

---

## 🟦 PHASE 0 — Connect + Baseline Audit (kuch bhi change NAHI karna)

```
Tum EkGuruLearning/EkGuru GitHub repo se kaam kar rahe ho. Is task me SIRF audit karna hai — KOI FILE CHANGE NAHI, KOI PUSH NAHI.

STEP 1: Repo clone/pull karo:
  git clone https://github.com/EkGuruLearning/EkGuru.git
  cd EkGuru

STEP 2: Ye 6 checks chalao aur exact output mujhe dikhao:

  CHECK A — AdSense loader kitne pages pe hai:
    grep -rl "adsbygoogle.js" . --include="*.html" | wc -l
    (Expected abhi: 0)

  CHECK B — google-adsense-account meta kitne pages pe hai:
    grep -rl "google-adsense-account" . --include="*.html" | wc -l
    (Expected abhi: 0)

  CHECK C — Policy gate ki current value:
    python3 -c "import json; d=json.load(open('data/monetization/google-monetization.json')); print('loader_allowed:', d['ad_policy']['loader_allowed']); print('approval_status:', d.get('approval_status'))"
    (Expected abhi: loader_allowed: [] aur NOT_READY_DO_NOT_APPLY)

  CHECK D — ads.txt sahi hai:
    cat ads.txt
    (Expected: google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0)

  CHECK E — Kitne pages ad-eligible class me hain:
    python3 tools/inject-ads.py --report
    (Expected: HIGH_CONTENT ~455, MEDIUM_CONTENT ~356)

  CHECK F — Live site pe code hai ya nahi:
    curl -s https://ekguru.shop/ | grep -c "adsbygoogle"
    curl -s https://ekguru.shop/ads.txt
    (Expected pehla: 0, dusra: ads.txt line)

STEP 3: Mujhe ye summary do (is format me):
  - Har check ka number + result
  - "BASELINE CONFIRMED: loader_allowed khaali hai, site pe AdSense code nahi hai" — ya agar koi cheez alag mili to wo batao.

Is phase me koi bhi file edit nahi karni, koi commit nahi karna.
```

**✔ Acceptance:** Agent ne 6 checks ke numbers diye aur baseline confirm kiya.

---

## 🟩 PHASE 1 — AdSense Code ON karo (MAIN FIX — sabse important)

```
Repo: EkGuruLearning/EkGuru. AdSense publisher ID: ca-pub-8175326569491671.
Is phase me AdSense loader code ko site pe ON karna hai. Repo ka apna build-system use karna hai — manually kisi HTML me script paste NAHI karni.

TASK 1 — Policy gate ON karo:
  File: data/monetization/google-monetization.json
  Change 1: "loader_allowed": []  ko  "loader_allowed": ["HIGH_CONTENT", "MEDIUM_CONTENT"]  se replace karo.
  Change 2: "approval_status": "NOT_READY_DO_NOT_APPLY"  ko  "approval_status": "APPLIED_AWAITING_GOOGLE_REVIEW"  se replace karo.
  Change 3: "reviewed_at" value ko aaj ki date (2026-09-28) karo.
  Dhyan rahe: json valid rehna chahiye (python3 -m json.tool data/monetization/google-monetization.json > /dev/null se verify karo).

TASK 2 — Inject chalao (repo ka apna tool, ye hi sahi tarika hai):
  python3 tools/inject-ads.py
  (Ye har HIGH_CONTENT aur MEDIUM_CONTENT page ke <head> me exactly ek marked block
   <!-- ekguru:adsense:start --> ... <!-- ekguru:adsense:end --> daalega jisme:
   preconnect links + <meta name="google-adsense-account" content="ca-pub-8175326569491671">
   + <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8175326569491671" crossorigin="anonymous"></script>)

TASK 3 — Ye checks PASS hone chahiye (sab dikhao):
  python3 tools/inject-ads.py --check          → exit 0, "ok" bolna chahiye
  grep -rl "google-adsense-account" . --include="*.html" | wc -l    → 800+ hona chahiye
  grep -rl "adsbygoogle.js" . --include="*.html" | wc -l            → 800+ hona chahiye
  grep -c "adsbygoogle" index.html                                  → homepage me block dikhe
  Ye EXCLUDED pages clean rehne chahiye (0 dikhna chahiye):
    grep -c "adsbygoogle" contact/index.html privacy/index.html cookie-policy/index.html courses/by-country/index.html 404.html
  Full build gate:
    python3 tools/build-all.py check
  Repo ka apna ad-policy test:
    node tools/test-ad-policy.mjs

TASK 4 — adsready.js ka canonical-check regex fix karo (ye tool ka bug hai — attribute order):
  File: tools/adsready.js, line ~134. Abhi ye hai:
    /rel="canonical"\s+href="https:\/\/ekguru\.shop\/"/.test(home.body)
  Ise order-agnostic banao:
    /<link[^>]*(rel="canonical"[^>]*href="https:\/\/ekguru\.shop\/"|href="https:\/\/ekguru\.shop\/"[^>]*rel="canonical")[^>]*>/.test(home.body)

TASK 5 — js/monetization.js aur js/cookie-consent.js me KOI CHANGE NAHI:
  ADS_RUNTIME_ENABLED aur ADVERTISING_AVAILABLE dono false hi rahenge. Ye approval ke baad (Phase 5) ka kaam hai. Agar tumne inhe true kiya to task FAIL.

TASK 6 — Commit + Push:
  NAYI BRANCH banao: git checkout -b adsense-enable-2026-09-28
  Sirf in files commit karo jo inject-ads.py ne badli + google-monetization.json + tools/adsready.js:
    git add -A
    git status   (dikhao kya-kya staged hai — data/ HTML files, json, adsready.js se zyada kuch ajeeb na ho)
  Commit message: "adsense: enable loader on HIGH/MEDIUM_CONTENT pages via inject-ads (policy gate ON)"
  Push: git push origin adsense-enable-2026-09-28
  PR kholo base=main, title: "Enable AdSense loader for Google review", aur PR description me TASK 3 ke saath check outputs paste karo.

TASK 7 — CI watch karo:
  gh run watch   (ya Actions tab se)
  CI green honi chahiye. Agar koi gate red ho to uska naam + error mujhe dikhao, fix karke push karo. Merge TABHI karna jab CI green ho.

REPORT FORMAT:
  - loader kitne pages pe laga (exact number)
  - TASK 3 ke sab check outputs
  - PR link + CI status
  - Merge hua ya nahi
```

**✔ Acceptance:** 800+ pages pe loader + meta; sab gates PASS; PR merged; CI green.

---

## 🟨 PHASE 2 — Live Deployment Verify (Google ko dikhna chahiye)

```
Repo: EkGuruLearning/EkGuru. Phase 1 merge ho chuka hai. Ab LIVE site verify karni hai (GitHub Pages deploy hone me 2-10 min lagte hain).

STEP 1 — Deploy hone do, phir ye LIVE checks chalao (sab paste karo):

  A) Homepage pe AdSense meta:
     curl -s https://ekguru.shop/ | grep -o 'google-adsense-account[^>]*'
     (Expected: <meta name="google-adsense-account" content="ca-pub-8175326569491671">)

  B) Homepage pe loader script:
     curl -s https://ekguru.shop/ | grep -o 'adsbygoogle.js?client=[^"]*'
     (Expected: ca-pub-8175326569491671)

  C) Deep page pe bhi (hindi section):
     curl -s https://ekguru.shop/hindi/ | grep -c "adsbygoogle"
     (Expected: 1 ya usse zyada)

  D) ads.txt live:
     curl -s https://ekguru.shop/ads.txt
     (Expected: google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0)

  E) Excluded page clean hai live pe:
     curl -s https://ekguru.shop/contact/ | grep -c "adsbygoogle"
     (Expected: 0)

  F) Repo ka live readiness:
     node tools/adsready.js
     (Expected: 12/12 PASS — regex fix ke baad)

STEP 2 — Agar koi live check fail ho:
  5 minute wait karke dubara try karo (Pages deploy late hota hai). 15 min ke baad bhi fail ho to purane SHA se compare karo:
    curl -s https://ekguru.shop/ | head -50   → aur batao kya dikh raha hai. Push skip na karo.

STEP 3 — Sitemap Google ko ping karo:
  curl -s "https://www.google.com/ping?sitemap=https://ekguru.shop/sitemap-index.xml"

REPORT: A se F tak har check ka output + "LIVE VERIFIED" ya problem ka detail.
```

**✔ Acceptance:** Live site pe har content page pe AdSense code dikh raha hai; ads.txt 200 OK; adsready 12/12.

---

## 🟧 PHASE 3 — Content Quality Fix (approval ka #1 rejection risk)

> ⚠️ **Ye phase review submit karne se PEHLE karna zaroori hai.** Repo ke apne audit (`data/quality/adsense-readiness.json`) me **965 pages duplicate-risk** par hain (304 repeated-paragraph groups). AdSense ka sabse common rejection "low value content" hai — programmatic template pages ka.

```
Repo: EkGuruLearning/EkGuru. Goal: duplicate/low-value content kam karna taaki AdSense review pass ho.

TASK 1 — Fresh audit generate karo:
  python3 tools/audit-adsense-readiness.py
  cat data/quality/adsense-readiness.json | python3 -m json.tool | head -80
  Isme se "duplicate_risk" aur "originality" sections ke exact numbers nikalo, aur "groups" me jo page lists hain unhe ek working list me daalo (sirf INDEXABLE pages — jinpe noindex meta NAHI hai).

TASK 2 — Worst groups pehle theek karo (priority order):
  (a) languages/<code>/level/a1..c5 tree ke pages jinke intro/beginning ke paragraphs same template se copy hue hain — unke opening 2-3 paragraphs per level UNIQUE banao. Har page ka content us language+level ke learner ke hisaab se likho (kya-alag-hoga is level me, kya सीखoge, ek real example, ek common mistake). Kam se kam: koi bhi 2 pages ka pehla paragraph word-to-word same na ho.
  (b) jo 5 "template_intro_groups" hain (ja/find-tutors.html, ja/index.html etc.) — unke intros unique karo.
  (c) Bilingual mirror pages (hindi/, urdu/, bengali/ etc. ke same-topic pages) — check karo ki translated pages me translated unique content hai, sirf machine-clone nahi.

TASK 3 — Rules (IMPORTANT):
  - Content HINDI/ENGLISH me natural likho, keyword-stuffing bilkul nahi.
  - noindex wale 1601 pages ko indexable MAT banao — unhe waise hi chhodna.
  - Kisi page ko delete nahi karna, sirf content improve karna. Sitemap/URL structure change nahi karna.
  - Har batch ke baad: python3 tools/build-all.py check  (green hona chahiye)

TASK 4 — Batch me commit karo:
  Har 30-50 pages ke batch pe ek commit: "content: unique intros for languages/xx level pages (batch N)"
  Ek PR: "AdSense content quality: de-duplicate template paragraphs"
  CI green → merge.

TASK 5 — Final audit dubara chalao aur mujhe BEFORE/AFTER do:
  BEFORE: repeated_paragraph_groups: 304, affected: 965
  AFTER: (naya number — target: affected indexable pages < 200, ho sake to < 100)

REPORT: before/after numbers + batch list + PR link + CI status.
```

**✔ Acceptance:** Duplicate-affected indexable pages drastically kam; CI green; audit file updated.

---

## 🟥 PHASE 4 — AdSense Account + Review Submit (ye tumhe KHUD karna hai — agent nahi kar sakta)

**Google AdSense approval ke liye ye manual steps hain (agent ke saath beth kar, 15 minute):**

1. **https://adsense.google.com** kholo → `pub-8175326569491671` account me login.
2. **Home → Sites → Add site** → `ekguru.shop` daalo → Save.
3. Site status "Ready" / "Review me bhejne ke liye ready" dikhna chahiye (kyunki Phase 1-2 me code live hai).
4. **"Request review"** dabao. Review me 2 din se 2 hafte lag sakte hain.
5. Review ke waqt ye confirm karo (agent se chhatwa lo):
   - [ ] Homepage + koi bhi content page pe code `view-source:` me dikh raha hai
   - [ ] ads.txt live hai
   - [ ] About / Contact / Privacy / Terms pages khul rahe hain
   - [ ] Site mobile pe theek khulta hai (PageSpeed: https://pagespeed.web.dev/ → ekguru.shop, score 80+ hona accha hai)
   - [ ] Search Console me site verified hai aur sitemap submit hai (https://search.google.com/search-console)
6. **Decision aane tak Phase 5 shuru MAT karna.**

Agar **REJECT** ho jaye to rejection reason AdSense dashboard ke "Issues" section me milega — wo reason muje bhejo, main agla fix-phase likh dunga. Common reasons: "low value content" (→ Phase 3 dubara deep), "site down/unavailable" (→ hosting check).

---

## 🟪 PHASE 5 — Approval ke BAAD: Ads Enable (TABHI karna jab Google "Approved" bole)

```
Repo: EkGuruLearning/EkGuru. AdSense approval mil gaya hai (site status "Ready"/ads serving). Ab ads ko RUNTIME pe enable karna hai — dhyan se, repo ke fail-closed design ko respect karte hue.

CONTEXT: Repo ka design fail-closed hai:
  - js/monetization.js me ADS_RUNTIME_ENABLED = false
  - js/cookie-consent.js me ADVERTISING_AVAILABLE = false
  - Ye isliye false the kyunki approval nahi tha aur certified CMP nahi tha.

TASK 1 — Runtime flag ON:
  js/monetization.js:  var ADS_RUNTIME_ENABLED = false;  →  true
  (is file ka isAdEligiblePage() logic waise hi rehne do — wo pages pe ads rokne ka kaam karta hai: quizzes, forms, legal pages, search, courses. YE PROTECTION APPROVED HAI, touch nahi karni.)

TASK 2 — Consent decision (mujhse pooch kar):
  Agar EEA/UK traffic target NAHI hai aur tum chahoge ki sirf India/US jaise markets me non-personalized ads chale: js/cookie-consent.js me ADVERTISING_AVAILABLE ko true karo AUR uske upar wale comment ko update karo ki decision kab liya gaya.
  Agar EEA/UK traffic chahiye: pehle Google ke certified CMP list se ek CMP integrate karna hoga — ye alag task hoga, mujhse confirm karo.
  Default: ADVERTISING_AVAILABLE = true with non-personalized fallback — lekin mera confirmation lo.

TASK 3 — Consent test update:
  node tools/test-consent-release.mjs
  node tools/test-ad-policy.mjs
  python3 tools/build-all.py check
  Teeno green hone chahiye. Jo test fail ho usko padho — wo bata raha hoga ki kaunsa expected-state flip karna bhool gaye.

TASK 4 — Verify karo ki ads sirf allowed pages pe hi request ho rahe hain:
  Browser me kholo (ya playwright se): /hindi/ (ad request jana chahiye), /courses/ (NAHI jana chahiye), /privacy/ (NAHI), /search/ (NAHI), /contact/ (NAHI)
  Network tab me pagead request sirf first type ke pages pe ho. Screenshot/evidence do.

TASK 5 — Commit: branch ads-live-<date>, message: "ads: enable runtime after approval (consent-gated, policy exclusions intact)", PR, CI green, merge.

REPORT: teeno test outputs + page-type matrix (kaunse page pe ad request gaya/na gaya) + PR link.
```

---

## 🟫 PHASE 6 — Monitoring & Protection (har mahine / hamesha)

```
Repo: EkGuruLearning/EkGuru. Ye ongoing-guard commands hain — inhe kabhi bhi chala sakte ho:

DAILY/WEEKLY GUARDS (agent se chalwao):
  1. node tools/adsready.js                    → 12/12 PASS hona chahiye
  2. python3 tools/inject-ads.py --check       → exit 0
  3. node tools/test-ad-policy.mjs             → PASS (excluded pages pe ads kabhi nahi)
  4. curl -s https://ekguru.shop/ads.txt       → publisher line intact
  5. curl -sI https://ekguru.shop/             → HTTP 200 (site up)
  6. CI green hai? → gh run list --limit 3

HAMESHA YAAD RAKHNE WALE RULES (meri taraf se, AdSense policy):
  1. Apni ads pe KABHI click mat karo, kisi se karwao mat (invalid traffic = account ban).
  2. Ads ke upar "Click karo" type koi text/button/image KABHI nahi.
  3. Legal pages (privacy, terms, cookie-policy, contact, search, admin, courses) pe ads hamesha OFF rahenge — repo ka policy engine ye karta hai, isko bypass mat karna.
  4. naya page template banate waqt data-ad-class sahi set karo (content → HIGH/MEDIUM_CONTENT).
  5. Traffic sources: paid-bot traffic, exchange traffic KABHI nahi — AdSense detect kar leta hai.
  6. Har mahine ek baar AdSense → Policy center kholo aur koi alert ho to muje bhejo.
```

---

# 🛡️ PART C — GOLDEN RULES (sab phases pe apply)

1. **Kabhi manually HTML me `<script adsbygoogle>` paste mat karwana** — hamesha `data/monetization/google-monetization.json` + `python3 tools/inject-ads.py` se. (Repo ka design yahi hai; manual paste agle build me corrupt ho jayega.)
2. **Order matter karta hai:** Phase 1 (code ON) → Phase 2 (verify) → Phase 3 (content) → Phase 4 (review submit) → approval → Phase 5 (ads live). Content fix (P3) review se pehle hona chahiye.
3. `ADS_RUNTIME_ENABLED` / `ADVERTISING_AVAILABLE` **approval se pehle true NAHI** karne.
4. Har phase me CI green = green signal agle phase ke liye.
5. Kuch bhi galat lage to agent se bolo: `git revert <sha>` — phir mujhse poochho.

---

## 📌 Ek line ka quick-paste (agar sirf ek hi message bhejna ho)

```
EkGuruLearning/EkGuru repo me AdSense enable karna hai: (1) data/monetization/google-monetization.json me "loader_allowed": [] → ["HIGH_CONTENT","MEDIUM_CONTENT"] aur approval_status → "APPLIED_AWAITING_GOOGLE_REVIEW"; (2) python3 tools/inject-ads.py chala kar loader ~800+ pages pe inject karo; (3) python3 tools/inject-ads.py --check, node tools/test-ad-policy.mjs, python3 tools/build-all.py check sab green karo; (4) tools/adsready.js line 134 ka canonical regex order-agnostic fix karo; (5) js/monetization.js ka ADS_RUNTIME_ENABLED aur cookie-consent.js ka ADVERTISING_AVAILABLE false hi rehne do; (6) branch adsense-enable-2026-09-28 se PR + CI green + merge; (7) live verify: curl -s https://ekguru.shop/ | grep google-adsense-account aur curl -s https://ekguru.shop/ads.txt. Report me saare numbers do.
```
