╔══════════════════════════════════════════════════════════════════════════════╗
║   EKGURU — GOOGLE ADSENSE APPROVAL: FINAL MASTER COMMAND DOCUMENT            ║
║   v2 ADVANCED · 2026-09-28 · Full-depth audit + scenario matrix + phases     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  REPO    : github.com/EkGuruLearning/EkGuru  (site: https://ekguru.shop)     ║
║  PUB-ID  : ca-pub-8175326569491671  /  ads.txt: pub-8175326569491671         ║
║  SCALE   : 2638 HTML pages · 1008 indexable · 811 ad-eligible · 1.5L links   ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─ TABLE OF CONTENTS ─────────────────────────────────────────────────────────┐
│ PART A  — ADVANCED AUDIT REPORT v2 (sab numbers, evidence ke saath)         │
│           A-1 inventory · A-2 CONTENT LANGUAGE AUDIT · A-3 depth            │
│           A-4 adsense wiring · A-5 duplicate risk · A-6 findings · A-7 gates│
│ PART B  — SCENARIO MATRIX (S-01..S-60 har bigadne-wali possibility +        │
│           R-1..R-8 rejection index) — detect/fix/prevent har ek ka          │
│ PART C  — MASTER PHASE COMMANDS P0→P10 (word-to-word agent paste)           │
│           P0 baseline · P1 CODE ON · P2 live verify · P3 content quality    │
│           P4 tech SEO · P5 review submit (manual) · P6 wait guards          │
│           P7 rejection recovery · P8 ads live · P9 CMP · P10 monitoring     │
│ PART D  — PER-SECTION CONTENT COMMANDS (D-01..D-24; har section ka likhna)  │
│ PART E  — APPENDICES (811 eligible pages FULL LIST + counts + scripts)      │
│ PART F  — 100-CHECK VERIFICATION BATTERY (review se pehle ka final test)    │
│ PART G  — GOLDEN RULES + ROLLBACK BIBLE + PASTE INDEX + time budget         │
└──────────────────────────────────────────────────────────────────────────────┘

⚡ SABSE PEHLE YE 3 CHEEZEIN SAMAJH LO:
1. Tumhari site ka AdSense infrastructure 100% bana hua hai — loader sirf ISLIYE
   band hai kyunki policy file me "loader_allowed": [] khaali hai. Phase 1 ise
   ON karta hai (811 pages pe code). Ye pura plan ka core hai.
2. Content language PROBLEM NAHI hai — translated pages real hain (Arabic/Japanese/
   German verified), lang attributes sahi hain. Duplicate TEMPLATED paragraphs
   (965 pages) hi asli risk hai — Phase 3 + PART D wahi fix karte hain.
3. Approval GOOGLE ka decision hai. Ye plan rejection ke top-8 reasons pehle se
   khatam karta hai — 100-check battery (PART F) green = tum best possible
   position me review doge.

⚠ PADHNE WALI BAAT: Ye document ~3.5k DENSE lines ka hai — har line actionable
  hai (command/expected-value/rule). Jaan-boojh kar filler se 20k lines NAHI
  banaya — lamba filler agent ko confuse karta, kaam kharab karta.

════════════════════════════════════════════════════════════════════════════════
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  EKGURU — ADSENSE APPROVAL FINAL MASTER COMMAND DOCUMENT (v2 ADVANCED)      ║
# ║  Repo: EkGuruLearning/EkGuru · Site: https://ekguru.shop                     ║
# ║  Publisher: ca-pub-8175326569491671 · Audit: 2026-09-28 · Audit depth: FULL  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
#
# Ise kaise use kare:
#  1. Nayi chat kholo jisme agent ke paas GitHub (write) access ho.
#  2. PART C ke phase commands EK-EK karke paste karo (Phase 0 se).
#  3. Har phase ke end me agent se ACCEPTANCE REPORT mangwa lo (har command me likha hai).
#  4. Koi phase fail ho to PART B (Scenario Matrix) me us scenario ka number dhundo.
#  5. PART D section-commands Phase 3 ke andar use hote hain.
#
# ⚠ HONESTY NOTE: Google AdSense approval Google ka decision hai. Ye document
#   har TECHNICAL + POLICY blocker remove karta hai jo repo me detect hua.
#   Jhooti guarantee koi nahi de sakta — lekin ye plan rejection ke sabse
#   common 8 reasons ko pehle hi fix kar deta hai (PART B: R-1..R-8).

════════════════════════════════════════════════════════════════════════════════
# PART A — ADVANCED AUDIT REPORT v2 (FULL DEPTH, HAR NUMBER EVIDENCE KE SAATH)
════════════════════════════════════════════════════════════════════════════════

## A-1. SITE INVENTORY (scan-complete: 2638/2638 files)

| Metric | Value | Verdict |
|---|---|---|
| Total HTML files | 2638 | — |
| Indexable pages (no noindex) | 1008 | ✅ sitemap se 100% match |
| noindex pages (by design) | 1630 | ✅ 0 noindex pages sitemap me — koi conflict nahi |
| Sitemap URLs | 1008 (15 child sitemaps + index) | ✅ 0 dead URLs — har URL disk pe exist karta hai |
| Internal links scanned | 1,52,153 | ✅ sirf 2 trivial issues (A-6) |
| Canonical host | ekguru.shop × 2635 | ✅ 0 github.io canonical bache |
| hreflang annotations | 1698 pages pe | ✅ |
| Mixed content (http:// links) | 0 | ✅ |
| Duplicate <title> | 0 | ✅ |
| Indexable pages <120 words | 0 | ✅ (thin sab noindex me hain) |
| og:title missing | sirf 2 (admin, 1 report preview) | ✅ negligible |
| Images missing alt (>3 per page) | 0 pages | ✅ |
| Empty directories | 0 | ✅ |
| PWA manifest icons | 5/5 exist on disk | ✅ |
| Razorpay/secret keys exposed | 0 | ✅ security clean |
| lang attribute mismatches | 0 | ✅ A-2 me detail |

## A-2. CONTENT LANGUAGE AUDIT (jo tumne poocha tha — "pages language me hone chahiye")

Google AdSense ka rule: page ka content ek RECOGNIZABLE language me hona chahiye
aur <html lang> usse match karna chahiye. Maine har section ka lang attribute
uske actual content ke against check kiya:

| Section | lang= | Content actually in that language? | Words (sample) |
|---|---|---|---|
| / (root, 2604 pages) | en | ✅ English content | — |
| /ar/ | ar | ✅ REAL Arabic translation (578 words) | ✅ |
| /de/ | de | ✅ REAL German (556 words) | ✅ |
| /es/ | es | ✅ | ✅ |
| /fr/ | fr | ✅ | ✅ |
| /ja/ | ja | ✅ REAL Japanese (309 words) | ✅ |
| /pt/ | pt | ✅ | ✅ |
| /tr/, /ru/, /ko/, /zh/, /id/, /vi/, /pl/, /bn/, /ur/ | same | ✅ sab sahi | ✅ |
| /hindi/, /urdu/, /tamil/, /telugu/, /bengali/, /malayalam/, /kannada/, /marathi/, /gujarati/, /punjabi/ | en | ✅ ye ENGLISH-medium sections hain (Hindi sikhane ke liye English me) — lang="en" SAHI hai | ✅ |

VERDICT: **Language wiring pe koi kaam NAHI chahiye.** Translated pages machine-placeholder
nahi hain — real translated copy hai. Ye AdSense ke liye sabse badi relief hai.

## A-3. CONTENT DEPTH DISTRIBUTION (2638 pages ka word-count)

| Bucket | Pages | % |
|---|---|---|
| <100 words | 1 (404 page — theek hai) | 0.04% |
| 100–250 words | 422 (sab noindex ya JS-shell) | 16% |
| 250–500 words | 808 | 31% |
| 500–1000 words | 898 | 34% |
| >1000 words | 509 | 19% |

Sample depths: about=768w, contact=577w, privacy=967w, hindi/=1417w,
learn-hindi-from-india=1356w, languages/fr/level/a1=8199w.
**Depth problem nahi hai. DUPLICATION problem hai (A-5).**

## A-4. ADSENSE WIRING STATUS (asli blocker)

```
Simulated run (policy gate flip karke, temp copy pe):
  loader inject hoga → 811 pages pe (exact list: eligible-pages.txt / PART E)
  clean rahenge      → 1826 pages (excluded classes)
  stripped           → 1 (admin.html)

811 pages ka section breakdown:
  learn/            218     hindi/             35
  languages/         81     urdu/              33
  ask/               44     telugu/            33
  answers/           28     punjabi/           33
  daily-hindi/       31     marathi/           33
  materials/         16     hindi-tutor/       33
  bengali/           32     gujarati/          33
  tamil/             32     ar,de,es,fr,ja,pt  24 (4 each)
  kannada/ (etc.)           zh,tr,ru,...       8 (1 each)
  root: index.html + find-tutors.html      2
```

Abhi ke 3 blockers:
1. `data/monetization/google-monetization.json` → `"loader_allowed": []` ← **KHAALI** (Phase 1 fix)
2. `google-adsense-account` meta → 0/2638 pages (inject-ads.py khud laga dega)
3. `approval_status: NOT_READY_DO_NOT_APPLY` (Phase 1 me flip hoga)

Approval ke BAAD wale 2 switches (ABHI TOUCH NAHI KARNA):
- `js/monetization.js` → `ADS_RUNTIME_ENABLED = false` (Phase 8 me true)
- `js/cookie-consent.js` → `ADVERTISING_AVAILABLE = false` (Phase 8 me decide)

## A-5. DUPLICATE CONTENT RISK (rejection ka #1 candidate)

Repo ka apna audit (`data/quality/adsense-readiness.json`, 2026-09-27):
- exact duplicate title groups: **0** ✅
- exact duplicate meta groups: **0** ✅
- template intro groups: **5** (ja/find-tutors.html + ja/index.html etc.)
- repeated paragraph groups: **304** → **965 pages affected** ⚠️
- Sabse bada group: `languages/<code>/level/a1..c5` tree — 12+ languages × 6 levels
  ke pages ka opening paragraph same template se hai.

Ye indexable pages hain (sitemap me hain), isliye Google inhe "cookie-cutter /
low value content" pattern ki tarah dekh sakta hai. **Phase 3 + PART D isko fix karta hai.**

## A-6. BAAKI CHHOTE FINDINGS (Phase-wise handle honge)

| ID | Finding | Severity | Kahan |
|---|---|---|---|
| F-1 | `tools/adsready.js` line ~134 ka canonical regex attribute-order maangta hai → false FAIL (canonical asal me sahi hai) | Medium (CI noise) | tools/adsready.js |
| F-2 | `admin.html` me `href=".."` link | Trivial (noindex page) | admin.html |
| F-3 | `daily-hindi/index.html:216` JS template link `"../daily-hindi/day-"+nextDay+"/"` — runtime-generated, static bug nahi | Info | daily-hindi/ |
| F-4 | `feed.xml` + `llms.txt` me abhi bhi "Verified native Hindi tutors" claim hai, jabki git history me contact se ye claim HATAYA gaya tha — inconsistency | Low (trust/consistency) | feed.xml, llms.txt |
| F-5 | `contact/` form sirf `mailto:` action hai — kaam chalau; real form (apps-script endpoint) better trust signal | Low | contact/ |
| F-6 | `bengali/index.html` me 1 "coming soon" string — context verify karna (languages/index.html wala match marketing-copy hai, harmless) | Info | bengali/ |
| F-7 | Service Worker HTML ke liye **network-first** hai ✅ — isliye deploy ke baad stale-cache risk nahi; phir bhi Phase 2 me CACHE/BUILD_ID bump verify karenge | Info | sw.js |

## A-7. REPO KE APNE GATES (jo hum use karenge — ye already bane hue hain)

- `tools/inject-ads.py` — policy engine: loader inject/strip, `--check`, `--report`
- `tools/adsready.js` — live readiness (12 checks)
- `tools/audit-adsense-readiness.py` — content/duplicate audit
- `tools/test-ad-policy.mjs` — policy test (excluded pages pe ad KABHI nahi)
- `tools/test-consent-release.mjs` — consent fail-closed test
- `tools/build-all.py check` — master gate (CI me chalta hai)
- `.github/workflows/ci.yml` — sab gates push pe auto-run

Inhe REINVENT nahi karna — sirf chalana hai.
════════════════════════════════════════════════════════════════════════════════
# PART B — SCENARIO MATRIX (har possibility jo bigad sakti hai: S-01..S-60 + R-1..R-8)
════════════════════════════════════════════════════════════════════════════════
Format har scenario ka:
  TRIGGER  → kab/kahan ho sakta hai
  DETECT   → detect karne ki exact command (expected output)
  FIX      → fix ka exact command/instruction
  PREVENT  → dobara na ho iske liye

────────────────────────────────────────────────────────────────
## B-1. ADSENSE CODE / POLICY SCENARIOS
────────────────────────────────────────────────────────────────

S-01 · Loader kisi page pe DOUBLE inject ho gaya (do baar script)
  TRIGGER: inject-ads.py manually do baar chalaya + regex fail
  DETECT: for f in $(grep -rl "ekguru:adsense:start" . --include="*.html"); do n=$(grep -c "ekguru:adsense:start" "$f"); [ "$n" -gt 1 ] && echo "DOUBLE: $f"; done   → (empty hona chahiye)
  FIX: python3 tools/inject-ads.py   (idempotent hai — khud theek kar dega)
  PREVENT: haath se HTML edit kabhi nahi; sirf inject-ads.py se

S-02 · Loader EXCLUDED page pe leak ho gaya (privacy/contact/courses...)
  TRIGGER: kisi ne manually script paste kar di, ya purana template
  DETECT: node tools/test-ad-policy.mjs   → "no excluded page carries the ad loader" PASS hona chahiye
  FIX: python3 tools/inject-ads.py   (scrubber sab ad-tags hata deta hai)
  PREVENT: build-all.py check CI me hai — red hua to merge block

S-03 · Galat publisher ID kahin snapshot ho gayi (purani/ca-pub-XXXX)
  TRIGGER: template copy-paste kisi aur site se
  DETECT: grep -rho "ca-pub-[0-9]*" . --include="*.html" | sort -u   → sirf ca-pub-8175326569491671 hona chahiye
  FIX: sed -i 's/ca-pub-[0-9]*/ca-pub-8175326569491671/g' <file>  phir inject-ads.py --check
  PREVENT: PART F check #4 har push pe

S-04 · ads.txt repo se hat gaya / rename ho gaya
  TRIGGER: cleanup me delete, ya .nojekyll ke saath conflict
  DETECT: test -f ads.txt && curl -s https://ekguru.shop/ads.txt | grep pub-8175326569491671
  FIX: git checkout -- ads.txt  (ya git se restore)
  PREVENT: adsready.js check #1 isko live test karta hai

S-05 · ads.txt live purani cached value dikhaye
  TRIGGER: GitHub Pages CDN cache (10 min)
  DETECT: curl -sH "Cache-Control: no-cache" https://ekguru.shop/ads.txt
  FIX: 10 min wait; phir bhi purana ho to Pages deploy status dekho (repo Settings→Pages / Actions)
  PREVENT: push ke turant baad judge mat karo, 10 min do

S-06 · google-adsense-account meta sirf kuch pages pe gaya (partial inject)
  TRIGGER: inject beech me crash hua
  DETECT: grep -rl "google-adsense-account" . --include="*.html" | wc -l   → 811 (ya current eligible count)
  FIX: python3 tools/inject-ads.py && python3 tools/inject-ads.py --check
  PREVENT: hamesha --check ke saath end karo

S-07 · <html data-ad-class> attribute kisi page pe missing/galat
  TRIGGER: naya page template haath se banaya
  DETECT: node tools/test-ad-policy.mjs   → "every page states its own class" PASS
  FIX: python3 tools/inject-ads.py   (class khud likh deta hai)
  PREVENT: naye templates inject-ads ke baad hi commit karo

S-08 · Policy JSON kharab ho gayi (invalid JSON → poora build red)
  TRIGGER: haath se edit, trailing comma
  DETECT: python3 -m json.tool data/monetization/google-monetization.json > /dev/null && echo OK
  FIX: git checkout -- data/monetization/google-monetization.json  aur dobara saaf edit
  PREVENT: JSON edit ke baad hamesha json.tool se validate

S-09 · loader_allowed me galat class aa gayi (e.g. UTILITY)
  TRIGGER: typo
  DETECT: python3 -c "import json;print(json.load(open('data/monetization/google-monetization.json'))['ad_policy']['loader_allowed'])"   → ["HIGH_CONTENT","MEDIUM_CONTENT"] hi
  FIX: sirf ye 2 values rakho; koi aur class mat jodo
  PREVENT: PART C Phase 1 ka command as-is paste karo

S-10 · Auto ads QUIZ/learner UI me ghus gaye (UX policy risk)
  TRIGGER: ADS_RUNTIME_ENABLED true kiya without guards
  DETECT: grep -n "google-anno-skip" js/monetization.js | head -3  (guards list hai) + manual browser check /courses/ pe koi ad nahi
  FIX: guards list touch nahi karni; runtime sirf Phase 8 me enable
  PREVENT: js/monetization.js ka isAdEligiblePage() logic immutable samjho

S-11 · AdSense review bole "code not found" (jabki code hai)
  TRIGGER: Google ne cached/purana version dekha, ya www/apex mismatch
  DETECT: curl -s https://ekguru.shop/ | grep -c adsbygoogle   (≥1) + curl -s https://www.ekguru.shop/ -I (301 → apex hona chahiye ya same content)
  FIX: www→apex redirect confirm karo (GitHub Pages CNAME khud karta hai); review dobara submit
  PREVENT: Phase 2 ke live checks review se pehle

S-12 · Do properties (github.io + ekguru.shop) AdSense me ho
  TRIGGER: purani property ka data
  DETECT: AdSense → Sites list me sirf ekguru.shop active hona chahiye
  FIX: AdSense dashboard se github.io property remove karo
  PREVENT: canonical sab ekguru.shop pe hain (audit ✅) — naya kuch mat banao

S-13 · Site pe dono Analytics + AdSense scripts conflict
  TRIGGER: gtag/consent defaults ad_storage galat set karein
  DETECT: grep -n "ad_storage" js/cookie-consent.js | head -3
  FIX: consent mode defaults "denied" se start — repo me already aisa hi hai; change nahi karna jab tak Phase 8 na ho
  PREVENT: cookie-consent.js ko sirf Phase 8 me chhedna

S-14 · Inject ne HEAD ke bahar block daal diya (body me)
  TRIGGER: kisi page ka <head> malformed
  DETECT: python3 tools/inject-ads.py --report   → "0 with no head" hona chahiye
  FIX: us page ka <head> theek karo, phir inject
  PREVENT: build-all.py check

S-15 · SW (service worker) purana HTML serve kare jisme loader nahi
  TRIGGER: returning visitor + pura cache
  DETECT: sw.js me HTML network-first hai (audit ✅) — sw.js line ~265
  FIX: kuch nahi karna; bas Phase 2 me CACHE/BUILD_ID bump hota hai kya, verify karo (git log sw.js)
  PREVENT: sw.js ka design network-first hi rakho

────────────────────────────────────────────────────────────────
## B-2. SEO / WIRING SCENARIOS
────────────────────────────────────────────────────────────────

S-16 · Canonical kahin github.io pe wapas chala jaye
  DETECT: grep -rl 'canonical"[^>]*github.io' . --include="*.html" | wc -l   → 0
  FIX: sed se ekguru.shop karo; root cause (build template) dhoondo
  PREVENT: PART F check #2

S-17 · Sitemap me aisa URL jo 404 de
  DETECT: python3 (sitemap-vs-disk script — PART F check #6)   → 0
  FIX: us URL ka page banao YA sitemap se hatao (build tool se, haath se nahi)
  PREVENT: sitemap build-generated hai — pages delete karte waqt sitemap rebuild karo

S-18 · noindex page sitemap me ghus gaya
  DETECT: audit script (audit me 0 tha)
  FIX: sitemap builder me noindex filter already hai — page ka noindex hatao ya sitemap rebuild
  PREVENT: build-full-page-inventory.py CI me hai

S-19 · Redirect loop (github.io ⇄ ekguru.shop)
  DETECT: curl -sIL https://ekgurulearning.github.io/EkGuru/ | grep -i "^HTTP\|location"
  FIX: CNAME file + Pages custom domain config verify (abhi sahi hai ✅)
  PREVENT: CNAME file delete kabhi mat karna

S-20 · www.ekguru.shop na khule ya cert error de
  DETECT: curl -sI https://www.ekguru.shop/   → 301/200, valid TLS
  FIX: DNS me www CNAME → ekguru.shop; Pages me dono domains listed
  PREVENT: DNS change ke baad 24h dheeraj

S-21 · Naya page banaya par kahin se link nahi (orphan)
  DETECT: naye page ka <a> inbound grep uske parent section hub me
  FIX: section hub page (e.g. learn/index.html) me link add karo
  PREVENT: naya page = hub link + sitemap entry, dono

S-22 · hreflang galat pairing (x-default missing etc.)
  DETECT: grep -o 'hreflang="[^"]*"' <page> | sort | uniq -c
  FIX: translated homepages ke set me x-default → en add karo agar missing ho
  PREVENT: ek hi template se translate pages banao

S-23 · robots.txt me galti se /hindi/ block ho gaya
  DETECT: curl -s https://ekguru.shop/robots.txt | grep -A2 "Disallow"
  FIX: repo ka robots.txt restore (audit me Allow rules already hain ✅)
  PREVENT: robots.txt edit = CI adsready check + manual dekho

S-24 · 404 page khud index ho gaya
  DETECT: grep -o 'noindex' 404.html | head -1  (hona chahiye)
  FIX: meta robots noindex add
  PREVENT: 404 template me already hai

S-25 · Sitemap lastmod sab aaj ki ho gayi (mass-touch)
  DETECT: grep -o "<lastmod>[^<]*" sitemap-learn.xml | sort -u | head
  FIX: lastmod sirf materially-changed pages ki — build tool iska dhyan rakhta hai; haath se mass-edit nahi
  PREVENT: content batches me commit karo (Phase 3 plan)

────────────────────────────────────────────────────────────────
## B-3. CONTENT / POLICY-CONTENT SCENARIOS
────────────────────────────────────────────────────────────────

S-26 · "Low value content" rejection (R-1 ka root)
  DETECT: data/quality/adsense-readiness.json → duplicate_risk.affected_page_count
  FIX: Phase 3 + PART D (per-section unique content commands)
  PREVENT: naya programmatic section banaye to unique-intro rule pehle se follow karo

S-27 · Translated page me aadha English chhoot gaya (mixed language)
  DETECT: for p in ar/*/*.html; do English-word ratio check (sample manual review)
  FIX: missing strings translate karo
  PREVENT: translation i18n dictionary se aati hai — dictionary me key add karo, haath se page nahi

S-28 · "coming soon" jaisi under-construction string indexable page pe
  DETECT: grep -rio "coming soon" . --include="*.html" | grep -v admin
  FIX: ya to page complete karo ya us section ko noindex rakho
  PREVENT: under-construction pages default noindex template se banao

S-29 · "native tutors" jaisa unverified claim kahin bach gaya (F-4)
  DETECT: grep -rl "native Hindi" . --include="*.html" | head  (+ feed.xml, llms.txt)
  FIX: OWNER DECISION: ya claim substantiate karo (tutor profiles me credential do) ya wording "verified tutors" me unify karo
  PREVENT: ek claims-page (about) pe single source of truth

S-30 · Copyright: kisi aur site ka paragraph copy ho gaya
  DETECT: 3-4 random sentences Google me quoted search karke
  FIX: apne words me rewrite
  PREVENT: sab content repo ke own writers se; copywatch.js already hai — use karo

S-31 · Content me adult/violence-adjacent material
  DETECT: n/a — course content hai, audit me kuch nahi mila
  FIX: n/a
  PREVENT: naya topic likhte waqt AdSense content policy yaad rakho

S-32 · Affiliate links disclosure ke bina
  DETECT: node tools/test-affiliate-disclosure.mjs (repo me hai)
  FIX: disclosure widget add (repo ka component use karo)
  PREVENT: monetization-disclosure page already hai ✅ — naye affiliate me link karo

S-33 · Broken anchor (#section) jisse user experience kharab
  DETECT: (low priority) anchors sample check
  FIX: id add karo
  PREVENT: headings me auto-id already hoga (template)

────────────────────────────────────────────────────────────────
## B-4. INFRA / CI / DEPLOY SCENARIOS
────────────────────────────────────────────────────────────────

S-34 · CI red ho gayi merge ke baad
  DETECT: gh run list --limit 1
  FIX: failing step ka log padho; PART B me uska scenario dhundo; fix commit; merge dobara
  PREVENT: local pe build-all.py check chala ke hi push karo

S-35 · GitHub Pages deploy fail (build error)
  DETECT: repo → Actions → "pages build and deployment" status
  FIX: usually HTML syntax ya bada file; error file dekho
  PREVENT: bade binary files images/ ke bahar na daalo

S-36 · Node version mismatch local vs CI
  DETECT: node --version (local 20.x hai; CI 22 use karta hai)
  FIX: repo tools Node 20+ pe chalte hain ✅; agar 22-specific feature aaye to package.json engines note karo
  PREVENT: CI green = source of truth

S-37 · npm install fail (jsdom network issue)
  DETECT: npm install ka error log
  FIX: npm cache clean --force && npm install --no-audit --no-fund
  PREVENT: package-lock.json commit hai ✅

S-38 · Python tools fail (3.11 vs 3.12 difference)
  DETECT: python3 tools/<tool>.py ka traceback
  FIX: repo tools stdlib use karte hain — traceback padho, usually path/cwd issue; hamesha repo ROOT se chalao
  PREVENT: commands PART C me cwd ke saath likhi hain

S-39 · DNS expire / CNAME records hat gaye (domain renewal!)
  DETECT: curl -sI https://ekguru.shop/   → NXDOMAIN/TLS fail
  FIX: DNS provider me A records (GitHub Pages ke 4 IPs) + CNAME www → restore; domain RENEW karo
  PREVENT: domain auto-renew ON rakho — ye sabse bada single-point-of-failure hai

S-40 · GitHub Pages HTTPS certificate provision nahi hua
  DETECT: browser me cert warning
  FIX: repo Settings→Pages → "Enforce HTTPS" checkbox (provision hone me 24h lag sakta hai)
  PREVENT: custom domain set karte hi Enforce HTTPS ON

S-41 · Repo size limit / push reject (100MB file)
  DETECT: git push ka error
  FIX: bade CSV/JSON data ko compress ya split karo
  PREVENT: media files LFS ya external (images abhi theek hain)

S-42 · Do log ek hi file edit karein (merge conflict)
  DETECT: git push rejected / conflict markers
  FIX: git pull --rebase, resolve, push
  PREVENT: ek waqt pe ek phase, ek branch

────────────────────────────────────────────────────────────────
## B-5. ADSENSE ACCOUNT-SIDE SCENARIOS
────────────────────────────────────────────────────────────────

S-43 · AdSense me site "Getting ready" atka rahe hai hafte bhar
  DETECT: AdSense → Sites → status
  FIX: code live verify (Phase 2 checks) + GSC me URL inspection se Googlebot ka dekha hua HTML confirm; phir bhi atka ho to ek naya article publish karke crawl invite karo
  PREVENT: sitemap ping (Phase 2 STEP 3)

S-44 · "ads.txt status: not found" warning AdSense me
  DETECT: AdSense → Sites → ads.txt status
  FIX: curl live ads.txt (S-04/S-05); 2-7 din me status update hota hai
  PREVENT: ads.txt root pe hi hai ✅ — haath mat lagao

S-45 · Payment address verification ka PIN nahi aya
  DETECT: AdSense → Payments → red banner
  FIX: 3 hafte baad PIN re-request; ya identity verification online
  PREVENT: address billing ke saath EXACT same rakho

S-46 · Identity/tax info mangwaya
  DETECT: AdSense → Payments → Verification check
  FIX: PAN + tax form (W-8BEN India ke liye) submit — India me ye normal hai
  PREVENT: pehle hi complete kar do taaki payment na atke

S-47 · EEA/UK traffic aana shuru ho aur consent CMP na ho
  DETECT: Analytics me EEA traffic %
  FIX: Phase 9 (certified CMP) tabhi jab EEA traffic meaningful ho
  PREVENT: abhi ke liye ad personalization EEA me hi denied rahega — theek hai

S-48 · Account pe invalid traffic warning
  DETECT: AdSense email/alert
  FIX: apne clicks band (kabhi click mat karo), traffic sources audit, Google ko form bharo
  PREVENT: PART G Golden Rules

S-49 · Review me "Site down / unavailable" bole
  DETECT: uptime check (Phase 6 me guard script)
  FIX: hosting status dekho (GitHub Pages status.twitter/dashboard), DNS (S-39)
  PREVENT: review week me koi hosting experiment NAHI

S-50 · Review me "Policy violation: scraped content"
  DETECT: rejection email
  FIX: R-5 playbook (PART C Phase 7)
  PREVENT: S-30

────────────────────────────────────────────────────────────────
## B-6. POST-APPROVAL SCENARIOS
────────────────────────────────────────────────────────────────

S-51 · Ads approved par kuch pages pe hi dikhe
  DETECT: pagead requests network tab (allowed vs excluded pages)
  FIX: expected behaviour hai — policy classes intentionally kuch pages exclude karti hain
  PREVENT: n/a (by design)

S-52 · Revenue zero par impressions hain
  DETECT: AdSense reports
  FIX: 2-4 din do; placements dekho (Auto ads); CPC niche ka hai
  PREVENT: n/a

S-53 · Kisi ne ads pe click-farm kiya (competition/sabotage)
  DETECT: CTR spike dashboard me
  FIX: Google ko turant report karo (Invalid traffic form)
  PREVENT: kuch nahi — Google filters karta hai; transparency hi bachav hai

S-54 · Naya page add kiya par loader nahi gaya
  DETECT: inject-ads.py --check red
  FIX: python3 tools/inject-ads.py chalao, commit
  PREVENT: page add karne ka SOP = build-all.py run karke commit

S-55 · Theme/CSS change ne ad-slot area todi
  DETECT: visual check HIGH_CONTENT page pe
  FIX: CSS me .ad-slot area restore
  PREVENT: layout change ke baad PART F visual checks

S-56 · Ads page speed ko dhire kare
  DETECT: PageSpeed mobile score approval se pehle vs baad
  FIX: loader already async hai; aur zyada issue ho to Auto ads format exclusions account me tune karo
  PREVENT: preconnect links inject karte hain ✅

S-57 · Policy center me naya alert
  DETECT: monthly PART F check #100
  FIX: alert text mujhe bhejo, main fix-phase likhunga
  PREVENT: monthly review

S-58 · Consent banner UI mobile pe content dhaba de (CLS)
  DETECT: mobile visual + CLS score
  FIX: banner CSS tweak (experience.css)
  PREVENT: banner non-blocking layout me hai — change karte waqt CLS test

S-59 · Custom domain change karna pade (future)
  DETECT: n/a
  FIX: KABHI mat karo bina plan ke — canonical/ads.txt/GSC sab tootenge; mujhse poochho, naya phase likhunga
  PREVENT: domain mat badlo 🙂

S-60 · Agent ne galti se bade area rewrite kar diye
  DETECT: git diff --stat abnormal bada
  FIX: git revert <merge-sha> — phase ka rollback
  PREVENT: har phase apni branch + PR me (PART C aisa hi mande karta hai)

────────────────────────────────────────────────────────────────
## B-7. REJECTION PLAYBOOK INDEX (detail Phase 7 me)
────────────────────────────────────────────────────────────────
R-1 Low value content          → Phase 7.1 (Phase 3 ko deeper chalao)
R-2 Site down/unavailable      → Phase 7.2 (S-39/S-40/S-49)
R-3 Policy violation: content  → Phase 7.3 (S-31/S-32)
R-4 Code not found / copied    → Phase 7.4 (S-11/S-12)
R-5 Scraped/spun content       → Phase 7.5 (S-30)
R-6 Navigation broken          → Phase 7.6 (link audit)
R-7 Under construction         → Phase 7.7 (S-28)
R-8 Unsupported language       → Phase 7.8 (A-2 recheck — unlikely, sab verified)
════════════════════════════════════════════════════════════════════════════════
# PART C — MASTER PHASE COMMANDS (word-to-word; ek phase = ek paste)
════════════════════════════════════════════════════════════════════════════════
ORDER STRICT HAI: P0 → P1 → P2 → P3 → P4 → P5 → P6(manual) → wait approval → P7 sirf reject pe → P8 approve ke baad → P9 optional → P10 hamesha.

────────────────────────────────────────────────────────────────
## 🟦 PHASE 0 — CONNECT + BASELINE (kuch change NAHI)
────────────────────────────────────────────────────────────────

```
Tum EkGuruLearning/EkGuru GitHub repo par kaam kar rahe ho. Ye task SIRF AUDIT hai — koi file edit nahi, koi commit nahi, koi push nahi.

STEP 1 — Clone (ya existing me pull):
  git clone https://github.com/EkGuruLearning/EkGuru.git
  cd EkGuru
  git log --oneline -3

STEP 2 — Ye 10 checks chalao aur EXACT output numbers mujhe do:

  C-01 loader kitne pages pe hai:
    grep -rl "adsbygoogle.js" . --include="*.html" | wc -l
    (expected: 0)

  C-02 adsense meta kitne pages pe hai:
    grep -rl "google-adsense-account" . --include="*.html" | wc -l
    (expected: 0)

  C-03 policy gate ki value:
    python3 -c "import json; d=json.load(open('data/monetization/google-monetization.json')); print(d['ad_policy']['loader_allowed'], d.get('approval_status'))"
    (expected: [] NOT_READY_DO_NOT_APPLY)

  C-04 ads.txt:
    cat ads.txt
    (expected: google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0)

  C-05 eligible class report:
    python3 tools/inject-ads.py --report
    (expected: HIGH_CONTENT 455, MEDIUM_CONTENT 356, admin stripped 1)

  C-06 runtime kill-switches:
    grep -n "ADS_RUNTIME_ENABLED = " js/monetization.js
    grep -n "ADVERTISING_AVAILABLE = " js/cookie-consent.js
    (expected: dono false)

  C-07 live homepage pe code:
    curl -s https://ekguru.shop/ | grep -c adsbygoogle
    (expected: 0)

  C-08 live ads.txt:
    curl -s https://ekguru.shop/ads.txt

  C-09 canonical hosts:
    grep -rho 'rel="canonical" href="[^"]*"' . --include="*.html" | sed 's/.*href="//;s/"$//' | sed 's|https://||;s|/.*||' | sort | uniq -c
    (expected: sirf ekguru.shop, ~2635)

  C-10 repo apne gates green hain:
    python3 tools/inject-ads.py --check && echo GATE-OK
    node tools/adsready.js --local 2>/dev/null | tail -3
    (adsready me canonical wala check false-fail ho sakta hai — ye KNOWN BUG hai (F-1), Phase 1 me fix hoga; baaki checks green dikhne chahiye)

STEP 3 — Mujhe ye FORMAT me report do:
  C-01: <number>
  C-02: <number>
  ... (C-10 tak)
  BASELINE CONFIRMED: <haan/nahi> — agar koi number expected se alag hai to batao kya alag hai.
Koi bhi file change mat karo. Koi commit nahi.
```

✔ ACCEPTANCE: 10 numbers + BASELINE CONFIRMED.

────────────────────────────────────────────────────────────────
## 🟩 PHASE 1 — ADSENSE CODE ON (MASTER FIX)
────────────────────────────────────────────────────────────────

```
Repo: EkGuruLearning/EkGuru (repo root me ho). Publisher ID: ca-pub-8175326569491671.
Phase 0 ka baseline confirm ho chuka hai. Ab AdSense loader ko repo ke APNE build-tool se enable karna hai. MANUALLY kisi HTML me script paste NAHI karni — sirf policy JSON badlegi aur tools/inject-ads.py chalega.

TASK 1 — NAYI BRANCH:
  git checkout main && git pull
  git checkout -b adsense-enable-<aaj-ki-date>

TASK 2 — Policy gate flip (data file, sirf ye 3 values):
  File: data/monetization/google-monetization.json
  2.1) "loader_allowed" ki value [] se badal kar ["HIGH_CONTENT", "MEDIUM_CONTENT"]
  2.2) "approval_status" ki value "NOT_READY_DO_NOT_APPLY" se badal kar "APPLIED_AWAITING_GOOGLE_REVIEW"
  2.3) "reviewed_at" ko aaj ki date karo
  Validate: python3 -m json.tool data/monetization/google-monetization.json > /dev/null && echo JSON-OK
  Inke alawa us file me KUCH AUR NAHI badalna (publisher block, ad_policy.classes, excluded_paths sab waise hi).

TASK 3 — Inject chalao (repo ka tool, yahi official tarika hai):
  python3 tools/inject-ads.py
  Expected console: "811 tagged" ke aas-paas ka number (HIGH+MEDIUM = 811)
  Ye tool har eligible page ke <head> me ye MARKED block daalega:
    <!-- ekguru:adsense:start --> ... preconnect links ...
    <meta name="google-adsense-account" content="ca-pub-8175326569491671">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8175326569491671" crossorigin="anonymous"></script>
    <!-- ekguru:adsense:end -->

TASK 4 — VERIFICATION BATTERY (sabke outputs paste karo):
  V-1 python3 tools/inject-ads.py --check
      (expected: "ok ad policy..." + exit 0)
  V-2 grep -rl "adsbygoogle.js" . --include="*.html" | wc -l
      (expected: 811)
  V-3 grep -rl "google-adsense-account" . --include="*.html" | wc -l
      (expected: 811)
  V-4 double-inject scan:
      for f in $(grep -rl "ekguru:adsense:start" . --include="*.html"); do n=$(grep -c "ekguru:adsense:start" "$f"); [ "$n" -ne 1 ] && echo "PROBLEM: $f = $n"; done
      (expected: koi output nahi)
  V-5 excluded pages CLEAN hain:
      grep -l "adsbygoogle.js" contact/index.html privacy/index.html terms/index.html cookie-policy/index.html disclaimer/index.html copyright/index.html search/index.html 404.html admin.html tutor.html join.html 2>/dev/null; echo "excluded-scan-done"
      (expected: sirf "excluded-scan-done", koi file naam nahi)
  V-6 courses clean:
      grep -rl "adsbygoogle.js" courses/ | wc -l
      (expected: 0)
  V-7 repo ka policy test:
      node tools/test-ad-policy.mjs
      (expected: PASS sab, 0 failed)
  V-8 master gate:
      python3 tools/build-all.py check
      (expected: sab steps ok)
  V-9 publisher ID ek hi hai:
      grep -rho "ca-pub-[0-9]*" . --include="*.html" | sort -u
      (expected: sirf ca-pub-8175326569491671)
  V-10 homepage me block:
      grep -c "adsbygoogle" index.html
      (expected: 2 — ek meta/JS-comment na ho to 1-2, zero NAHI)

TASK 5 — adsready.js ka KNOWN BUG fix (F-1):
  File: tools/adsready.js, canonical wali line (line ~134):
    Abhi: /rel="canonical"\s+href="https:\/\/ekguru\.shop\/"/.test(home.body)
    Naya (order-agnostic):
      /<link[^>]*(?:rel="canonical"[^>]*href="https:\/\/ekguru\.shop\/"|href="https:\/\/ekguru\.shop\/"[^>]*rel="canonical")[^>]*>/.test(home.body)
  Phir: node tools/adsready.js --local  → 12/12 PASS dikhna chahiye

TASK 6 — TOUCH NAHI KARNA (agar kiya to phase FAIL):
  js/monetization.js  (ADS_RUNTIME_ENABLED false hi rahega)
  js/cookie-consent.js (ADVERTISING_AVAILABLE false hi rahega)
  robots.txt, ads.txt, CNAME, sitemaps, koi bhi content page ka text.

TASK 7 — COMMIT + PR:
  git add -A
  git status   → mujhe dikhao: changed files ~815 (811 HTML + json + adsready.js) ke aas-paas hi honi chahiye; koi ajeeb bada folder na dikhe
  git commit -m "adsense: enable account loader on HIGH_CONTENT+MEDIUM_CONTENT via policy gate (inject-ads)"
  git push origin adsense-enable-<aaj-ki-date>
  PR kholo: base=main, title "AdSense loader enable — Google review ke liye"
  PR body me TASK 4 ke saare outputs paste karo.

TASK 8 — CI:
  gh run watch  (ya Actions tab)
  CI GREEN hone tak wait karo. Red ho to failing step ka log mujhe dikhao, PART B scenario follow karke fix karo, push karo.
  CI green → merge karo (merge commit, squash nahi).

REPORT FORMAT:
  injected: <number> pages
  V-1..V-10 outputs
  adsready: <x>/12
  PR link + CI status + merge status
  changed-files count: <number>
```

✔ ACCEPTANCE: V-1..V-10 sab expected; CI green; merged.

ROLLBACK (agar kuch bhi galat ho):
  git revert -m 1 <merge-sha> && git push   (loader poora hatega, site waisi ki waisi)

────────────────────────────────────────────────────────────────
## 🟨 PHASE 2 — LIVE DEPLOY VERIFY (Google ko code DIKHNA chahiye)
────────────────────────────────────────────────────────────────

```
Phase 1 merge ho gaya. GitHub Pages deploy me 2-10 min lagte hain. Ab LIVE verification.

STEP 1 — Deploy ka wait/confirm:
  gh run list --limit 3   (pages build and deployment → completed)
  (ya 10 min wait)

STEP 2 — LIVE CHECKS (L-1..L-14, saare outputs paste karo):
  L-01 curl -s https://ekguru.shop/ | grep -o 'google-adsense-account[^>]*'
      (expected: meta ca-pub-8175326569491671)
  L-02 curl -s https://ekguru.shop/ | grep -o 'adsbygoogle.js?client=[^"]*'
      (expected: ca-pub-8175326569491671)
  L-03 curl -s https://ekguru.shop/hindi/ | grep -c adsbygoogle        (expected ≥1)
  L-04 curl -s https://ekguru.shop/learn/ | grep -c adsbygoogle        (expected ≥1)
  L-05 curl -s https://ekguru.shop/ask/ | grep -c adsbygoogle          (expected ≥1)
  L-06 curl -s https://ekguru.shop/answers/ | grep -c adsbygoogle      (expected ≥1)
  L-07 curl -s https://ekguru.shop/daily-hindi/ | grep -c adsbygoogle  (expected ≥1)
  L-08 curl -s https://ekguru.shop/materials/ | grep -c adsbygoogle    (expected ≥1)
  L-09 curl -s https://ekguru.shop/ar/ | grep -c adsbygoogle           (expected ≥1)
  L-10 curl -s https://ekguru.shop/ja/ | grep -c adsbygoogle           (expected ≥1)
  L-11 curl -s https://ekguru.shop/de/ | grep -c adsbygoogle           (expected ≥1)
  L-12 EXCLUDED live clean:
       curl -s https://ekguru.shop/contact/ | grep -c adsbygoogle   (expected 0)
       curl -s https://ekguru.shop/privacy/ | grep -c adsbygoogle   (expected 0)
       curl -s https://ekguru.shop/courses/ | grep -c adsbygoogle   (expected 0 — courses/ root)
  L-13 curl -s https://ekguru.shop/ads.txt
      (expected: google.com, pub-8175326569491671, DIRECT, f08c47fec0942fa0)
  L-14 node tools/adsready.js
      (expected: 12/12 PASS)

STEP 3 — Deep sample (random 10 eligible URLs ke liye L-03 jaisa check; PART E ki list se
  10 URLs khud utha lo, har ek pe curl grep adsbygoogle ≥1).

STEP 4 — Google ko crawl invite:
  curl -s "https://www.google.com/ping?sitemap=https://ekguru.shop/sitemap-index.xml"
  (expected: yaa XML acknowledgement)

STEP 5 — GSC cross-check (agar Search Console access hai):
  GSC → URL Inspection → https://ekguru.shop/ → "Test Live URL" → rendered HTML me script dikhna chahiye.
  Report me screenshot/likhit confirmation do.

REPORT: L-01..L-14 numbers + 10-sample results + ping result.
Koi check fail ho: 10 min wait → dobara; phir bhi fail → S-05/S-35 scenario.
```

✔ ACCEPTANCE: 14/14 live green + sample 10/10.

────────────────────────────────────────────────────────────────
## 🟧 PHASE 3 — CONTENT QUALITY (REJECTION SE BACHAV — sabse lamba phase)
────────────────────────────────────────────────────────────────

> Is phase me PART D ke per-section commands use honge (Section D-01..D-40).
> Pehle master batch-plan, phir sections ek-ek karke.

```
Repo: EkGuruLearning/EkGuru. Goal: duplicate/templated content ko unique banakar
"low value content" rejection ka risk khatam karna.

RULES (har batch pe laagu):
  R1. Sirf INDEXABLE pages chhedne hain. noindex pages ko indexable MAT banao;
      noindex pages ko chhod do.
  R2. Har page ka OPENING 2-3 paragraph + koi ek midd le-section us page ke
      topic/language/level ke hisaab se UNIQUE likhna hai. Baaki structure same
      reh sakta hai (layout template theek hai).
  R3. Content ka language = page ki existing language (en pages me English,
      ar me Arabic, ja me Japanese...). Machine-translation ka pata na chale.
  R4. Keyword-stuffing nahi. Natural teaching tone. Ek real example + ek common
      mistake har page me.
  R5. Koi page delete nahi, koi URL change nahi, koi sitemap haath-se edit nahi.
  R6. Batch = 30-50 pages → ek commit → batch-end pe:
      python3 tools/build-all.py check  (green) 
      python3 tools/audit-adsense-readiness.py  (numbers note karo)

STEP 1 — Fresh audit numbers:
  python3 tools/audit-adsense-readiness.py
  python3 - <<'EOF'
  import json
  d=json.load(open('data/quality/adsense-readiness.json'))
  print('BEFORE affected:', d['duplicate_risk']['affected_page_count'])
  print('BEFORE groups:', len(d['duplicate_risk']['groups'].get('introductions',{})))
  EOF
  (numbers note karo — AFTER se compare honge)

STEP 2 — Batch order (is sequence me, har batch ek PR):
  B-01 languages/<code>/level/a1 (sab codes, ~81 pages)  ← sabse bada template group
  B-02 languages/<code>/level/a2 (agla wave)
  B-03 languages/<code>/level/b1, b2
  B-04 languages/<code>/level/c1..c5
  B-05 learn/ repeated-paragraph pages (218 eligible me jo audit me aaye)
  B-06 ask/ + answers/ repeated pages
  B-07 daily-hindi/ + materials/
  B-08 hindi/ urdu/ tamil/ telugu/ bengali/ malayalam/ kannada/ marathi/ gujarati/ punjabi/ hindi-tutor/ (in me jo audit flag kare)
  B-09 ja/find-tutors.html + ja/index.html + baaki 5 template-intro groups
  B-10 feed.xml + llms.txt me "native Hindi tutors" wording unify (S-29 — owner se poochho: claim rakna hai ya "verified tutors"?)

  Har section ke LIKHONE ke liye PART D ke section-commands use karo
  (D-01..D-40) — unme har section ke liye EXACT directory list, unique-angle
  instructions aur likhne ka pattern diya gaya hai.

STEP 3 — Commit discipline:
  branch: content-quality-<batch-id>
  commit: "content: unique intros <section> (batch B-0X, N pages)"
  PR: "AdSense content quality — batch B-0X"
  CI green → merge → agla batch.

STEP 4 — AFTER audit (sab batches ke baad):
  python3 tools/audit-adsense-readiness.py
  affected_page_count report karo.
  TARGET: indexable affected < 200 (ideal < 100)

REPORT: BEFORE vs AFTER numbers + batch list (B-01..B-10, pages-per-batch) + PR links + final audit json ke numbers.
```

✔ ACCEPTANCE: affected indexable pages < 200; sab batches merged; CI green.

────────────────────────────────────────────────────────────────
## 🟦 PHASE 4 — TECHNICAL SEO + RICH RESULTS (approval week se pehle)
────────────────────────────────────────────────────────────────

```
Repo: EkGuruLearning/EkGuru. Goal: technical polish jo review ke waqt Google dekhta hai.

T-1 Structured data validate (sample 10 pages):
  Homepage, hindi/, learn/, ask/ koi ek, answers/ koi ek, daily-hindi/, languages/fr/level/a1/, learn-hindi-from-usa/, index per translated set.
  Har page pe JSON-LD <script type="application/ld+json"> nikalo:
    python3 - <<'EOF'
    import re,sys
    t=open(sys.argv[1],encoding='utf-8').read()
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>',t):
        import json
        try: json.loads(m.group(1)); print(sys.argv[1],'LD-OK')
        except Exception as e: print(sys.argv[1],'LD-BROKEN:',e)
    EOF
  Broken mile to json fix karo (comma/quote).

T-2 Rich results test (manual, browser):
  https://search.google.com/test/rich-results pe homepage + 1 course page + 1 article daalo.
  Errors → fix; warnings acceptable.

T-3 Mobile-friendliness:
  PageSpeed: https://pagespeed.web.dev/ → ekguru.shop
  Mobile Performance ≥ 70, Accessibility ≥ 90 hona chahiye. Jo bhi red flag aaye report karo.

T-4 404 page behaviour:
  curl -s -o /dev/null -w "%{http_code}" https://ekguru.shop/ye-page-exist-nahi-karta/
  (expected: 404 + 404.html ka branded page)

T-5 Trailing slash consistency (sample):
  curl -sI https://ekguru.shop/hindi  | head -1   (301 → /hindi/ hona chahiye — GitHub Pages standard)

T-6 XML sitemap lint:
  python3 - <<'EOF'
  import glob,re
  for s in sorted(glob.glob('sitemap*.xml')):
      if 'index' in s: continue
      t=open(s,encoding='utf-8',errors='ignore').read()
      n=len(re.findall(r'<loc>',t))
      assert t.startswith('<?xml'), s
      print(s, n, 'OK')
  EOF

T-7 Favicon + PWA:
  curl -s -o /dev/null -w "%{http_code}\n" https://ekguru.shop/images/icon-192.png
  curl -s -o /dev/null -w "%{http_code}\n" https://ekguru.shop/manifest.webmanifest
  (dono 200)

T-8 contact form upgrade (OPTIONAL, owner confirm kare):
  contact/ abhi mailto: use karta hai. Agar owner chaahe to repo ke apps-script/
  endpoint se real form wiring — ye bada change hai, alag PR, mere confirmation ke bina nahi.

REPORT: T-1..T-7 ke results. Koi error fix karke tabhi agle phase pe jao.
```

────────────────────────────────────────────────────────────────
## 🟥 PHASE 5 — OWNER MANUAL: ADSENSE ACCOUNT + REVIEW SUBMIT
────────────────────────────────────────────────────────────────
(Ye agent nahi karega — TUM karoge, 15-20 minute. Word-to-word clicks:)

```
1. Browser me https://adsense.google.com → login Google account se
   (wahi account jisse pub-8175326569491671 bana hai).
2. Home → "Sites" → "+ Add site" → ekguru.shop → Save.
3. Site status "Getting ready" ya "Ready" dikhega. Code already live hai (Phase 2)
   isliye "Review request" ka option aayega → "Request review" click karo.
4. Review ke liye ye FINAL pre-flight (10 min):
   [ ] Mobile phone se site kholo — khulta hai, ads nahi dikhe (abhi runtime off — theek hai)
   [ ] view-source:https://ekguru.shop/ me adsbygoogle dikh raha hai
   [ ] adsense.google.com → Sites → ads.txt status "Authorized" (2-7 din lag sakte hain)
   [ ] About/Contact/Privacy/Terms pages khul rahe hain
   [ ] PageSpeed mobile ≥ 70 (Phase 4 T-3)
   [ ] Search Console me sitemap-index.xml submitted hai
5. Review submit → Google 2 din–2 hafte le sakta hai.
6. IS DAURAAN: koi bada deploy/experiment nahi (S-49), koi apna ad-click nahi (S-48).
7. Decision email + AdSense → Sites me status aayega:
   APPROVED  → Phase 8
   REJECTED  → Phase 7 (reason ke saath mujhe batao)
```

────────────────────────────────────────────────────────────────
## 🟫 PHASE 6 — WAIT-PERIOD GUARDS (review ke dinon me, agent se har 2-3 din)
────────────────────────────────────────────────────────────────

```
Guard run (review week me har 2-3 din me ek baar):
  G-1 curl -s -o /dev/null -w "%{http_code}\n" https://ekguru.shop/            (200)
  G-2 curl -s https://ekguru.shop/ads.txt | grep -c pub-8175326569491671        (1)
  G-3 curl -s https://ekguru.shop/ | grep -c adsbygoogle                        (≥1)
  G-4 curl -s -o /dev/null -w "%{http_code}\n" https://ekguru.shop/hindi/       (200)
  G-5 curl -s -o /dev/null -w "%{http_code}\n" https://ekguru.shop/contact/     (200)
  G-6 gh run list --limit 1                                                     (green)
  G-7 git status                                                                (clean)
Koi bhi guard red → turant mujhe batana.
Is week me repo me KOI BADA PUSH NAHI (chhota typo-fix theek hai).
```

────────────────────────────────────────────────────────────────
## 🟪 PHASE 7 — REJECTION RECOVERY (sirf tab jab Google REJECT kare)
────────────────────────────────────────────────────────────────

```
Rejection email ka EXACT reason text mujhe do. Neeche har reason ka fix-path hai:

7.1 "Low value content":
  Phase 3 ko DEEP mode me chalao:
    - duplicate audit se INDEXABLE groups ki poori list nikaalo (sirf flag nahi — har group ke pages)
    - har page ka opening 2-3 para + 1 midd le-section + 1 conclusion unique
    - jis section me sabse zyada pages hain wahan per-page 150+ unique words add karo
    - thin-noindex walo ko WAISE HI chhodna
    - AFTER target: affected < 50
    - 15-20 NAYE deep articles bhi publish karo (learn/ me 1500+ words wale) — fresh value signal
  Phir 2 hafte content me aur improve karke dobara review.

7.2 "Site down/unavailable":
  S-39 (DNS/renewal), S-40 (HTTPS), S-49 (uptime) follow karo; sab green hone ke
  baad 3 din stable rehne do, phir review.

7.3 "Policy violation (content)":
  Rejection email me jo page-URLs listed hain unko kholo; offending content
  remove/rewrite; affiliate disclosure check (S-32); phir review.

7.4 "Code not found / copied code":
  S-11 (www/canonical), S-12 (do properties), S-05 (cache) follow karo;
  view-source verify; review dobara.

7.5 "Scraped content":
  S-30: quoted-search se overlap dhoondo; rewrite; apne examples/screenshots/data add karo; phir review.

7.6 "Navigation issues":
  PART F link-audit full run karo; sab hubs (learn/, hindi/, toolbox/) se main
  areas reachable hon; header/footer links test; phir review.

7.7 "Under construction":
  S-28: sab "coming soon"/empty section pages ya complete karo ya noindex+sitemap-se-out;
  phir review.

7.8 "Unsupported language":
  A-2 audit dobara chalao (lang attr + sample content); galat mila to translate
  fix; sab sahi tha to appeal me clarify karo ki sections language-declared hain.

HAR CASE ME: fix ke baad KAM SE KAM 5-7 din wait karke review dobara — Google
recrawl ke liye time leta hai. Baar-baar turant review dena counter-productive hai.
```

────────────────────────────────────────────────────────────────
## 🟩 PHASE 8 — APPROVAL KE BAAD: ADS LIVE (tabhi jab "Approved" mile)
────────────────────────────────────────────────────────────────

```
AdSense → Sites → ekguru.shop status "Ready" / ads serving ON. Ab runtime enable.

TASK 1 — Branch: ads-live-<date>

TASK 2 — js/monetization.js:
  var ADS_RUNTIME_ENABLED = false;  →  true
  Is file ka BAaki KUCH bhi change nahi (isAdEligiblePage, selectors, google-anno-skip sab jagah ke jagah).

TASK 3 — Consent (MUJHE/OWNER se confirm karke):
  Mode A (default, EEA traffic negligible): js/cookie-consent.js
    ADVERTISING_AVAILABLE = false → true
    aur uske upar ka comment update: decision date + "non-EEA deployment" note.
  Mode B (EEA/UK traffic meaningful): pehle Phase 9 (CMP) — Mode A ABHI NAHI.
  Confirm aane tak TASK 3 skip, baaki mat karo.

TASK 4 — Tests:
  node tools/test-consent-release.mjs   (expected PASS — fail hua to test ka message padho, expected-state flip miss hua hoga)
  node tools/test-ad-policy.mjs         (PASS)
  python3 tools/build-all.py check      (green)

TASK 5 — Browser/playwright verify (5 page matrix):
  /hindi/            → pagead request JAANI chahiye   (network tab)
  /courses/<koi>/    → NAHI jaani chahiye
  /privacy/          → NAHI
  /search/?q=test    → NAHI
  /contact/          → NAHI
  Evidence (screenshots) PR me paste karo.

TASK 6 — AdSense dashboard:
  Ads → By site → ekguru.shop → Auto ads ON (start: "max revenue" nahi —
  "Non-UI recommended/optimized" default rakho; formats me "in-page" ON,
  "anchors" ON, "vignettes" OFF start ke liye — learning-site me vignette
  interruptive lagta hai, 2 hafte baad tune karna).

TASK 7 — PR: "ads: runtime enable post-approval (consent-gated)" → CI green → merge.
REPORT: 3 test outputs + 5-page matrix evidence + PR link.
```

────────────────────────────────────────────────────────────────
## 🟨 PHASE 9 — EEA/UK CERTIFIED CMP (OPTIONAL — EEA traffic hone par)
────────────────────────────────────────────────────────────────

```
Trigger: Analytics/GSC me EEA+UK sessions > 5% ho jayein.
Kaam: Google-certified CMP list (Google Ads Help → "certified CMP") se ek CMP
  choose karo (CookieYes/Consentmode wala koi bhi TCF-certified), uska script
  cookie-consent.js ke saath integrate karo, TCF v2.2 string wire karo,
  test-consent-release.mjs me EEA case add karo.
Ye naya integration hai — merge se pehle mujhse plan confirm karna.
Jab tak ye nahi hua: EEA users ko ads load mat karwana (consent unavailable).
```

────────────────────────────────────────────────────────────────
## 🟪 PHASE 10 — ONGOING MONITORING (hamesha)
────────────────────────────────────────────────────────────────

```
1. Repo me tools/weekly-guard.sh banao:

#!/usr/bin/env bash
# EkGuru weekly AdSense+SEO guard
set -u
FAIL=0
ck(){ printf "%-58s" "$1"; shift; if eval "$*" >/dev/null 2>&1; then echo "OK"; else echo "FAIL"; FAIL=1; fi; }
ck "site 200"            '[ "$(curl -s -o /dev/null -w %{http_code} https://ekguru.shop/)" = 200 ]'
ck "hindi/ 200"          '[ "$(curl -s -o /dev/null -w %{http_code} https://ekguru.shop/hindi/)" = 200 ]'
ck "contact/ 200"        '[ "$(curl -s -o /dev/null -w %{http_code} https://ekguru.shop/contact/)" = 200 ]'
ck "ads.txt publisher"   'curl -s https://ekguru.shop/ads.txt | grep -q pub-8175326569491671'
ck "loader on homepage"  'curl -s https://ekguru.shop/ | grep -q adsbygoogle'
ck "loader on hindi"     'curl -s https://ekguru.shop/hindi/ | grep -q adsbygoogle'
ck "no ads on privacy"   '! curl -s https://ekguru.shop/privacy/ | grep -q adsbygoogle.js'
ck "no ads on courses"   '! curl -s https://ekguru.shop/courses/ | grep -q adsbygoogle.js'
ck "robots allows"       'curl -s https://ekguru.shop/robots.txt | grep -q "Allow: /"'
ck "sitemap ping-able"   'curl -s -o /dev/null https://ekguru.shop/sitemap-index.xml'
ck "policy gate correct" 'python3 -c "import json,sys; d=json.load(open(\"data/monetization/google-monetization.json\")); sys.exit(0 if d[\"ad_policy\"][\"loader_allowed\"]==[\"HIGH_CONTENT\",\"MEDIUM_CONTENT\"] else 1)"'
ck "inject idempotent"   'python3 tools/inject-ads.py --check'
ck "ad policy tests"     'node tools/test-ad-policy.mjs'
ck "CI green"            'gh run list --limit 1 | grep -qi "success"'
echo; [ $FAIL -eq 0 ] && echo "GUARD: ALL GREEN" || echo "GUARD: FAILURES HAIN — mujhe batao"
exit $FAIL

  chmod +x tools/weekly-guard.sh
  (CI me bhi add kar sakte ho: ci.yml me ek step: bash tools/weekly-guard.sh — network checks CI me flaky ho sakte hain, isliye local/cron recommended.)

2. Har mahine (calendar reminder lagao):
  - AdSense → Policy center: koi alert? (mujhe text bhejo)
  - PART F ka full 100-check run
  - audit-adsense-readiness.py fresh numbers
  - PageSpeed mobile score

3. Golden rules (PART G) kabhi na tootey.
```
════════════════════════════════════════════════════════════════════════════════
# PART D — PER-SECTION CONTENT COMMANDS (Phase 3 ke andar use hone wale)
════════════════════════════════════════════════════════════════════════════════
Har D-XX block ko Phase 3 ke batch ke waqt agent ko paste karo. Sab blocks ke upar
D-24 (UNIQUE-7 pattern) common hai — pehle wo padho.

────────────────────────────────────────
## D-24 · UNIQUE-7 WRITING PATTERN (sab sections ke liye COMMON — pehle ye)
────────────────────────────────────────
```
Har page me jo templated/duplicate mila hai, uski jagah ye 7-element pattern likhna
(sirf OPENING 2-3 paragraph + ek mid-section badalna hai; page ka layout nahi):

  U1. PAGE-SPECIFIC HOOK: pehli line us page ke EXACT topic pe — generic "learning
      Hindi is rewarding" jaisi line KABHI nahi.
  U2. READER-CONTEXT: ye page kaun padhega (beginner/heritage learner/traveller/kid's parent)
      aur usko is topic me sabse pehli dikkat kya lagegi.
  U3. REAL EXAMPLE: is page ke topic ka 1 genuine example — Devanagari (ya us bhasha
      ki script) + transliteration + meaning. Copy-paste dusre page se nahi.
  U4. COMMON MISTAKE: is topic pe learners jo galti karte hain + uska fix.
  U5. PAGE-KA-MAKSAD: is page ke end tak reader kya-kya kar payega (2-3 bullets).
  U6. CROSS-LINK SUGGESTION (text me, natural): 1 related page ka mention
      jo WAHI section me ho (internal linking deep hone chahiye).
  U7. LENGTH GUARD: opening 150-220 words, total page existing se chhota nahi hona
      chahiye. Kam pad gaya to U3/U4 ko detail me badhao, filler nahi.

RULES:
  - Language = page ki existing language (en me English; ar/ja/de... me wahi bhasha).
  - Devanagari words sahi spelling me (अम्मा vs अम्मी — source page se verify karo).
  - Kisi aur site ka sentence copy NAHI — quoted-search test khud pe karo.
  - Har 10 page ke baad khud se 2 page ka diff padho — kahin apna hi template to nahi ban gaya?

VERIFICATION (har batch ke end me):
  python3 tools/audit-adsense-readiness.py
  grep -c "noindex" <changed-page>  (noindex pe touch nahi hua)
  python3 tools/build-all.py check
```

────────────────────────────────────────
## D-01 · languages/<code>/ TREE (81 pages — sabse BADA template group)
────────────────────────────────────────
```
DIRECTORIES: languages/ar languages/de languages/es languages/fr languages/it
             languages/ja languages/ko languages/pt languages/ru languages/zh
             (har ek me ~8 pages + languages/index.html)

AUDIT KA CLAIM: inke level/index pages ka intro paragraph same template se hai.

STEP 1 — Duplicates pinpoint karo:
  python3 - <<'EOF'
  import json
  d=json.load(open('data/quality/adsense-readiness.json'))
  g=d['duplicate_risk']['groups'].get('introductions',{})
  for h,ps in g.items():
      if any(p.startswith('languages/') for p in ps): print(h, ps)
  EOF

STEP 2 — Har language-tree ke liye D-24 pattern se opening rewrite:
  - languages/<code>/index.html: "<code> bhashi learners ke liye Hindi" ka SPECIFIC angle:
    (ar→script difference + right-to-left habit, ja→particles vs postpositions,
     zh→tones vs Hindi tones-less but gender, ko→honorifics parallel, es/it/pt→
     gender-friendly but verb-aspect new, de→case system parallel, ru→Cyrillic to
     Devanagari switch, fr→nasal vowels advantage)
  - languages/<code>/level/a1..cN (jo bhi files hain): HAR LEVEL ka angle us level
    ke learner ke liye (a1: pehle 50 words ki strategy us mother-tongue se;
    b1: aspect/gender errors jo specifically us bhashi karta hai; c1: register/
    formality). Same sentence 2 levels me repeat NAHI.
  - Example words U3 me us language ke learners ke known pain-point wale lo
    (e.g. ja me "वह vs यह", de me "ने construction").

STEP 3 — Verify:
  python3 tools/audit-adsense-readiness.py  → languages/ groups kam hone chahiye
  2 random pages ka diff khud padho.

BATCH SPLIT: 2 batches (B-01: ar de es fr it; B-02: ja ko pt ru zh)
```

────────────────────────────────────────
## D-02 · learn/<lang>/ TOPIC PAGES (176 pages — 8 languages × 22 topics)
────────────────────────────────────────
```
DIRECTORIES: learn/hindi learn/urdu learn/tamil learn/telugu learn/punjabi
             learn/marathi learn/gujarati learn/bengali  (har ek me ~22 topics)

DUPLICATE SHAPE: audit me repeated_paragraph_groups in sections ke across hain.

STEP 1 — Kaunse pages/groups flag hue:
  python3 - <<'EOF'
  import json
  d=json.load(open('data/quality/adsense-readiness.json'))
  g=d['duplicate_risk']['groups']
  for kind,groups in g.items():
      for h,ps in groups.items() if isinstance(groups,dict) else []:
          hits=[p for p in ps if p.startswith('learn/')]
          if hits: print(kind, h[:8], len(hits), hits[:3])
  EOF

STEP 2 — D-24 pattern per page. SPECIAL RULES:
  - learn/<X>/grammar type pages: X-language-specific comparison table already
    hogi — uske AROUND ka text unique banao (table ko chhedna nahi).
  - learn/<X>/bollywood|kollywood|tollywood|pollywood type pages: har bhasha ke
    apne 2-3 REAL film/music examples — cross-language copy nahi.
  - learn/<X>/alphabet: us bhashi ko Devanagari me sabse confusing 2 letters
    (e.g. tamil speaker ke liye र/ड़) — bhasha-specific hi likhna.
  - learn/<X>/vs-hindi pages: comparison ke 3 REAL examples.

STEP 3 — Verify (D-24 ka verification block). BATCH SPLIT: 4 batches (2-3 languages per batch).
```

────────────────────────────────────────
## D-03 · learn/practice · learn/paths · learn/contexts (22 pages)
────────────────────────────────────────
```
STEP 1: ls learn/practice/ learn/paths/ learn/contexts/
STEP 2: Ye structured pages hain — inka intro + "how to use this" section D-24
  se unique karo. practice pages pe: ye practice kis lesson ke baad karni chahiye
  (specific path reference). paths pages pe: is path me kitne din/weeks lagenge
  real numbers ke saath. contexts pages pe: ye context kin kin learners ke liye hai.
STEP 3: 1 batch (B-05 ke saath).
```

────────────────────────────────────────
## D-04 · learn/ SINGLE-TOPIC GUIDES (~11 pages)
────────────────────────────────────────
```
FILES: learn/write-your-name-in-hindi/, learn/learn-hindi-online-guide/,
  learn/learn-hindi-from-bollywood/, learn/how-to-say-hello-in-hindi/,
  learn/hindi-verbs-present-past-future/, learn/hindi-sentence-structure/,
  learn/hindi-phrases-for-travel/, learn/hindi-or-urdu-difference/,
  learn/hindi-numbers-1-to-100/, learn/hindi-how-to-write-vowels/,
  learn/hindi-how-to-write-consonants/, learn/hindi-gender-masculine-feminine/,
  learn/hindi-family-words/, learn/hindi-days-months-time/, learn/hindi-barakhadi/,
  learn/hindi-alphabet-for-beginners/, learn/common-hindi-mistakes/,
  learn/aap-tum-tu-hindi/
Ye HIGH-value organic pages hain (ye bhi in sitemap). Ye PRIORITY pages hain:
  - Inka opening sabse shararat se unique hona chahiye (ye Google me rank
    karti hain — inka content sabse deep ho).
  - Har page me U3 example page-ke-numbers se (1-to-100 page me numbers hi, etc.)
    aur ek unique insider tip (jo kisi aur page me na ho).
1 batch, sabse dhyan se.
```

────────────────────────────────────────
## D-05..D-12 · SECTION TREES (hindi/ urdu/ tamil/ telugu/ bengali/ marathi/ gujarati/ punjabi/)
────────────────────────────────────────
```
DIRECTORIES (eligible pages):
  hindi/ (35)  urdu/ (33)  tamil/ (32)  telugu/ (33)
  bengali/ (32) marathi/ (33) gujarati/ (33) punjabi/ (33)

COMMON SHAPE: har section me same 30+ topics (alphabet, greetings, numbers,
family, emergency, business, slang, cinema page, vs-hindi page...).
DUPLICATE RISK: same topic 8 sections me lagbhag same English paragraph.

STEP 1 — Audit groups me in sections ke hits dekho (D-02 STEP 1 wali script me
  startswith list badal kar: hindi/ urdu/ tamil/ telugu/ bengali/ marathi/ gujarati/ punjabi/).

STEP 2 — CROSS-SECTION UNIQUENESS RULE (ye sabse important):
  Same topic (e.g. "greetings") ke 8 pages ka opening EK-DUSRE SE BHI alag hona
  chahiye, sirf apne section me unique kaafi nahi:
  - hindi/greetings: general Hindi learner angle
  - urdu/greetings: Urdu script/nastaliq + adaab vs namaste cultural angle
  - tamil/greetings: tamil speaker ke liye vanakkam vs namaste angle
  - telugu/greetings: namaskaram parallel angle
  - bengali/greetings: nomoshkar angle + bollywood exposure
  - marathi/greetings: namaskar in marathi vs hindi difference
  - gujarati/greetings: kem chho angle
  - punjabi/greetings: sat sri akal angle
  Har page me us bhashi ke REAL transferable advantage/confusion likho.

STEP 3 — Cinema pages: har bhasha ke apne 2-3 real films (tamil→Kollywood,
  telugu→Tollywood, bengali→Satyajit Ray reference, marathi, gujarati, punjabi→Pollywood).
STEP 4 — BATCH SPLIT: 8 chhote batches (1 language = 1 batch) — review asaan rahega.
```

────────────────────────────────────────
## D-13 · hindi-tutor/ (33 pages — city/country tutor pages)
────────────────────────────────────────
```
DIRECTORIES: hindi-tutor/<city> (delhi, mumbai, jaipur, london, new-york, dubai...)

DUPLICATE RISK: city pages ka template paragraph.
STEP 1 — Audit se hindi-tutor/ hits.
STEP 2 — Har CITY page me LOCAL SPECIFICS:
  - us city/country me Hindi kyun useful (community size, business, heritage families)
  - timezone note (lessons kiske liye kab convenient)
  - 1 real local context (e.g. london→Brent community, dubai→Indian expat workforce)
  Placeholder city-facts NAHI — verifiable general facts.
STEP 3 — verify + 2 batches.
```

────────────────────────────────────────
## D-14 · daily-hindi/ (31 pages — day-1..day-30 + hub)
────────────────────────────────────────
```
STEP 1 — audit hits.
STEP 2 — Days already structured hain (ek idea, ek task). Duplicate intro ho to:
  har day ka opening US DAY ke concept pe (day-16 gender, day-22 ne...).
  Day-to-day ka continuity line rakho ("kal tumne X dekha, aaj uska use Y me").
  Day-30 me next-steps already hoga.
STEP 3 — 1 batch.
```

────────────────────────────────────────
## D-15 · ask/ (44 pages — question pages)
────────────────────────────────────────
```
STEP 1 — audit hits.
STEP 2 — Ye Q&A pages: opening me DIRECT ANSWER pehle 2 lines me (Google
  featured-snippet style), uske baad D-24 ka U2-U5. Do ask-pages ka answer
  section EK-JAISA nahi (e.g. how-to-say-sorry ke 2 variants pages hain —
  unme alag-alag focus: ek formal ek casual).
  NOTE: ask/is-italki-or-preply-better-for-hindi — competitor names wala page:
  neutral, factual, FINGERS-off claims (repo ka no-competitor-attribution gate
  hai — us test ko green rakhna): node tools/test-no-competitor-attribution.js
STEP 3 — 2 batches (22+22).
```

────────────────────────────────────────
## D-16 · answers/ (28 pages)
────────────────────────────────────────
```
ask/ jaisa hi: direct-answer-first + D-24. Vocabulary-list pages (colours,
body-parts, days, months) me lists already hain — unke AROUND ka prose unique.
1-2 batches.
```

────────────────────────────────────────
## D-17 · materials/ (16 pages)
────────────────────────────────────────
```
materials/grammar materials/writing materials/work materials/vocabulary ... hub
STEP: har material page pe — ye material KIS learner ke liye, kaise use kare
(5-minute drill plan), print/download instruction already hogi (usse relevant).
1 batch.
```

────────────────────────────────────────
## D-18 · TRANSLATED HOMEPAGES (ar de es fr ja pt — 24 pages)
────────────────────────────────────────
```
FILES: <code>/index.html + <code>/find-tutors.html + <code>/<1-2 more> per code
YE ALREADY REAL TRANSLATIONS HAIN (audit A-2 ✅). Kaam sirf tab jab audit inme
template-intro flag kare (ja/find-tutors + ja/index group known hai):
  - ja ke 2 pages ke intros alag karo (find-tutors vs index ka purpose hi alag hai)
  - baaki codes me agar group mile to same treatment
LANGUAGE: pure <code> me likhna — English mix na ho. Native-level quality na ho
  paye to mujhe batana (hindi sikhane walon ke liye English rakhna better hai
  galat translation se).
1 batch.
```

────────────────────────────────────────
## D-19 · TRANSLATED SINGLES (<code>/hindi — 16 pages)
────────────────────────────────────────
```
FILES: ar/hindi de/hindi es/hindi fr/hindi ja/hindi pt/hindi ko/hindi zh/hindi
       vi/hindi ur/hindi tr/hindi ru/hindi it/hindi id/hindi pl/hindi bn/hindi
STEP: audit inme se kisi ko flag kare to D-18 jaisa treatment (pure language).
  Ye 1-page mini-hubs hain — unka CTA (find tutors link) intact rakhna.
1 batch (agar groups mile to).
```

────────────────────────────────────────
## D-20 · learn-hindi-from-* INDEXABLE COUNTRY PAGES (54 pages)
────────────────────────────────────────
```
NOTE: 200+ country folders hain par sirf 54 eligible/indexable hain (baaki
noindex — unhe chhedna NAHI).

STEP 1 — 54 ki list:
  sed 's|^|https://ekguru.shop/|' eligible-pages.txt me jo learn-hindi-from-* hain
  (ya: grep "learn-hindi-from" eligible-pages.txt)

STEP 2 — Har COUNTRY page me (D-24 + country specifics):
  - us desh me Hindi kahan kaam aati hai (diaspora hubs real names ke saath)
  - time-zone + lesson scheduling angle
  - 1 cultural bridge point (e.g. fiji→Fiji Hindi fact, uk→Leicester,
    canada→Brampton, usa→Edison NJ, kenya nahi eligible to skip...)
  Template country-facts (capital/population) sirf tab jab page-specific angle ke
  saath — plain Wikipedia-copy strictly nahi (S-50 risk).
4 batches (14+14+13+13).
```

────────────────────────────────────────
## D-21 · ROOT HUB PAGES (about, faq, how-levels-work, start, name-in-hindi, monetization-disclosure, hubs)
────────────────────────────────────────
```
FILES: about/index.html faq/index.html how-levels-work/index.html start/index.html
       name-in-hindi/index.html + section hubs (learn/ hindi/ toolbox waghera jo
       eligible hain)
STEP: inke openings already solid hain (about=768w). Sirf audit-flag wale touch karo.
SPECIAL: monetization-disclosure page pe loader bhi ja raha hai (eligible list me
  hai) — OWNER DECISION: ads disclosure page pe weird lagta hai. RECOMMENDED:
  data/monetization/google-monetization.json ke UTILITY class ke match array me
  "/monetization-disclosure/**" ADD karo (Phase 1 ke TASK 2 ke saath, mujhse confirm
  karke), phir inject dobara chalao — loader us page se hat jayega.
```

────────────────────────────────────────
## D-22 · CLAIMS UNIFY (feed.xml + llms.txt — S-29)
────────────────────────────────────────
```
ISSUE: feed.xml aur llms.txt me "Verified native Hindi tutors" phrase hai;
git history me contact se native-claim hataya gaya tha. Inconsistent.

STEP 1: grep -rn "native" feed.xml llms.txt
STEP 2: OWNER se poochho (mujhe/owner ko message): claim RAKHNA hai ya hataana?
  - RAKHNA hai → about/ me tutor credentials page ke link se substantiate
  - HATAANA hai → feed.xml + llms.txt + answers pages me "native Hindi" ko
    "Hindi" ya "verified tutors" karo (grep -rl "native Hindi" se poori list)
STEP 3: node tools/test-no-competitor-attribution.js green rehna chahiye.
```

────────────────────────────────────────
## D-23 · VERIFY-ONLY SECTIONS (inme eligible page 0 hai — TOUCH NAHI KARNA)
────────────────────────────────────────
```
toolbox/ (13 pages)      → UTILITY class — ads nahi, noindex nahi par eligible nahi.
  Sirf check: wo sahi se classify hue hain? node tools/test-ad-policy.mjs PASS = done.
world-languages/ (195)   → RESEARCH/noindex — chhedna nahi. Verify: sitemap me nahi hain.
courses/ (186)           → INTERACTIVE_LEARNING — ads kabhi nahi. Aise hi sahi.
learn-hindi-for-*-speakers (30+ roots) → noindex set — chhedna nahi.
malayalam/ kannada/      → eligible list me nahi (class differ karti hai) — mat chhedo.
languages/<code>/level/  me jo noindex hain → waise hi.
Rule: AGAR TUMNE INME KUCH BADLA TO PHASE 3 FAIL.
```
════════════════════════════════════════════════════════════════════════════════
# PART E — APPENDICES (auto-generated exact lists)
════════════════════════════════════════════════════════════════════════════════

## E-1 · LOADER-ELIGIBLE PAGES (811) — Phase 1 me INHI pe code jayega
Simulated policy-flip se nikali gayi EXACT list (repo ke inject-ads.py se).
Agent Phase 1 chalane ke baad in pages pe 'ekguru:adsense:start' mark milna chahiye.

```
# eligible pages (811) — full list:
about/index.html
answers/best-hindi-movies-to-learn-hindi/index.html
answers/best-way-to-learn-hindi-as-a-beginner/index.html
answers/can-i-learn-hindi-without-learning-the-script/index.html
answers/difference-between-hindi-and-urdu/index.html
answers/hindi-body-parts-vocabulary/index.html
answers/hindi-colours-list/index.html
answers/hindi-days-of-the-week/index.html
answers/hindi-family-words/index.html
answers/hindi-greetings-namaste-and-others/index.html
answers/hindi-months-and-seasons/index.html
answers/hindi-numbers-1-to-100/index.html
answers/hindi-phrases-for-travelling-in-india/index.html
answers/hindi-postpositions-ka-ki-ke/index.html
answers/hindi-pronouns-explained/index.html
answers/hindi-verb-hona-to-be/index.html
answers/hindi-vs-punjabi-vs-bengali/index.html
answers/hindi-word-order-explained/index.html
answers/how-to-ask-for-directions-in-hindi/index.html
answers/how-to-order-food-in-hindi/index.html
answers/how-to-practice-hindi-speaking-alone/index.html
answers/how-to-say-goodbye-in-hindi/index.html
answers/how-to-say-i-am-hungry-in-hindi/index.html
answers/how-to-say-i-am-learning-hindi/index.html
answers/how-to-say-please-and-thank-you-in-hindi/index.html
answers/how-to-tell-the-time-in-hindi/index.html
answers/how-to-type-hindi-on-phone/index.html
answers/index.html
answers/what-does-ji-mean-in-hindi/index.html
ar/find-tutors.html
ar/hindi/index.html
ar/index.html
ar/join.html
ask/best-way-to-learn-hindi-for-beginners/index.html
ask/can-i-learn-hindi-by-myself/index.html
ask/can-i-learn-hindi-from-bollywood-alone/index.html
ask/can-i-learn-hindi-in-3-months/index.html
ask/cheapest-way-to-learn-hindi/index.html
ask/do-hindi-speakers-mind-mistakes/index.html
ask/do-i-need-to-learn-devanagari/index.html
ask/hindi-alphabet-question/index.html
ask/hindi-family-question/index.html
ask/hindi-for-kids-how-to-start/index.html
ask/hindi-or-urdu-question/index.html
ask/hindi-or-urdu-which-to-learn/index.html
ask/hindi-words-every-beginner-should-know/index.html
ask/how-long-to-learn-hindi/index.html
ask/how-long-to-read-hindi-script/index.html
ask/how-many-words-do-i-need-in-hindi/index.html
ask/how-much-does-a-hindi-tutor-cost/index.html
ask/how-to-count-1-to-10-in-hindi/index.html
ask/how-to-introduce-yourself-in-hindi/index.html
ask/how-to-practice-hindi-without-a-partner/index.html
ask/how-to-remember-hindi-genders/index.html
ask/how-to-say-good-morning-in-hindi/index.html
ask/how-to-say-hello-in-hindi-question/index.html
ask/how-to-say-how-are-you-in-hindi/index.html
ask/how-to-say-i-dont-understand-in-hindi/index.html
ask/how-to-say-i-love-you-in-hindi/index.html
ask/how-to-say-please-in-hindi/index.html
ask/how-to-say-sorry-in-hindi-properly/index.html
ask/how-to-say-sorry-in-hindi/index.html
ask/how-to-say-thank-you-in-hindi/index.html
ask/how-to-say-what-is-your-name-in-hindi/index.html
ask/how-to-say-yes-and-no-in-hindi/index.html
ask/how-to-write-name-hindi-question/index.html
ask/index.html
ask/is-duolingo-good-for-hindi/index.html
ask/is-hindi-hard-to-learn/index.html
ask/is-hindi-or-spanish-easier-to-learn/index.html
ask/is-hindi-useful-to-learn/index.html
ask/is-italki-or-preply-better-for-hindi/index.html
ask/what-does-acha-mean-in-hindi/index.html
ask/what-does-namaste-really-mean/index.html
ask/what-does-yaar-mean-in-hindi/index.html
ask/what-is-the-best-age-to-learn-hindi/index.html
ask/what-is-the-hardest-part-of-hindi/index.html
bengali/alphabet/index.html
bengali/beginners/index.html
bengali/bollywood/index.html
bengali/business/index.html
bengali/conversation/index.html
bengali/emergency/index.html
bengali/family/index.html
bengali/flashcards-topic/index.html
bengali/for-kids/index.html
bengali/formal-informal/index.html
bengali/grammar/index.html
bengali/greetings/index.html
bengali/heritage/index.html
bengali/how-long/index.html
bengali/indian-languages/index.html
bengali/listening/index.html
bengali/mistakes/index.html
bengali/name-topic/index.html
bengali/numbers/index.html
bengali/phrases-food/index.html
bengali/phrases-travel/index.html
bengali/pronunciation/index.html
bengali/reading/index.html
bengali/relationships/index.html
bengali/sentence-structure/index.html
bengali/shopping/index.html
bengali/slang/index.html
bengali/speaking/index.html
bengali/time-date/index.html
bengali/verbs/index.html
bengali/vocabulary/index.html
bengali/writing/index.html
bn/hindi/index.html
daily-hindi/day-1/index.html
daily-hindi/day-10/index.html
daily-hindi/day-11/index.html
daily-hindi/day-12/index.html
daily-hindi/day-13/index.html
daily-hindi/day-14/index.html
daily-hindi/day-15/index.html
daily-hindi/day-16/index.html
daily-hindi/day-17/index.html
daily-hindi/day-18/index.html
daily-hindi/day-19/index.html
daily-hindi/day-2/index.html
daily-hindi/day-20/index.html
daily-hindi/day-21/index.html
daily-hindi/day-22/index.html
daily-hindi/day-23/index.html
daily-hindi/day-24/index.html
daily-hindi/day-25/index.html
daily-hindi/day-26/index.html
daily-hindi/day-27/index.html
daily-hindi/day-28/index.html
daily-hindi/day-29/index.html
daily-hindi/day-3/index.html
daily-hindi/day-30/index.html
daily-hindi/day-4/index.html
daily-hindi/day-5/index.html
daily-hindi/day-6/index.html
daily-hindi/day-7/index.html
daily-hindi/day-8/index.html
daily-hindi/day-9/index.html
daily-hindi/index.html
de/find-tutors.html
de/hindi/index.html
de/index.html
de/join.html
es/find-tutors.html
es/hindi/index.html
es/index.html
es/join.html
faq/index.html
find-tutors.html
fr/find-tutors.html
fr/hindi/index.html
fr/index.html
fr/join.html
gujarati/alphabet/index.html
gujarati/beginners/index.html
gujarati/business/index.html
gujarati/conversation/index.html
gujarati/emergency/index.html
gujarati/family/index.html
gujarati/flashcards-topic/index.html
gujarati/for-kids/index.html
gujarati/formal-informal/index.html
gujarati/grammar/index.html
gujarati/greetings/index.html
gujarati/gujarati-cinema/index.html
gujarati/gujarati-vs-hindi/index.html
gujarati/heritage/index.html
gujarati/how-long/index.html
gujarati/indian-languages/index.html
gujarati/listening/index.html
gujarati/mistakes/index.html
gujarati/name-topic/index.html
gujarati/numbers/index.html
gujarati/phrases-food/index.html
gujarati/phrases-travel/index.html
gujarati/pronunciation/index.html
gujarati/reading/index.html
gujarati/relationships/index.html
gujarati/sentence-structure/index.html
gujarati/shopping/index.html
gujarati/slang/index.html
gujarati/speaking/index.html
gujarati/time-date/index.html
gujarati/verbs/index.html
gujarati/vocabulary/index.html
gujarati/writing/index.html
hindi-tutor/ahmedabad/index.html
hindi-tutor/australia/index.html
hindi-tutor/bangalore/index.html
hindi-tutor/canada/index.html
hindi-tutor/chandigarh/index.html
hindi-tutor/chennai/index.html
hindi-tutor/delhi/index.html
hindi-tutor/dubai/index.html
hindi-tutor/germany/index.html
hindi-tutor/houston/index.html
hindi-tutor/hyderabad/index.html
hindi-tutor/index.html
hindi-tutor/jaipur/index.html
hindi-tutor/japan/index.html
hindi-tutor/kolkata/index.html
hindi-tutor/london/index.html
hindi-tutor/lucknow/index.html
hindi-tutor/melbourne/index.html
hindi-tutor/mumbai/index.html
hindi-tutor/nepal/index.html
hindi-tutor/new-york/index.html
hindi-tutor/patna/index.html
hindi-tutor/pune/index.html
hindi-tutor/san-francisco/index.html
hindi-tutor/singapore/index.html
hindi-tutor/south-africa/index.html
hindi-tutor/spain/index.html
hindi-tutor/sydney/index.html
hindi-tutor/toronto/index.html
hindi-tutor/united-arab-emirates/index.html
hindi-tutor/united-kingdom/index.html
hindi-tutor/united-states/index.html
hindi-tutor/worldwide/index.html
hindi/alphabet/index.html
hindi/beginners/index.html
hindi/bollywood/index.html
hindi/business/index.html
hindi/conversation/index.html
hindi/emergency/index.html
hindi/family/index.html
hindi/flashcards-topic/index.html
hindi/for-kids/index.html
hindi/formal-informal/index.html
hindi/grammar/index.html
hindi/greetings/index.html
hindi/heritage/index.html
hindi/hindi-vs-urdu/index.html
hindi/hinglish/index.html
hindi/how-long/index.html
hindi/index.html
hindi/indian-languages/index.html
hindi/listening/index.html
hindi/mistakes/index.html
hindi/name-topic/index.html
hindi/numbers/index.html
hindi/phrases-food/index.html
hindi/phrases-travel/index.html
hindi/pronunciation/index.html
hindi/reading/index.html
hindi/relationships/index.html
hindi/sentence-structure/index.html
hindi/shopping/index.html
hindi/slang/index.html
hindi/speaking/index.html
hindi/time-date/index.html
hindi/verbs/index.html
hindi/vocabulary/index.html
hindi/writing/index.html
how-levels-work/index.html
id/hindi/index.html
index.html
it/hindi/index.html
ja/find-tutors.html
ja/hindi/index.html
ja/index.html
ja/join.html
ko/hindi/index.html
languages/ar/course/index.html
languages/ar/index.html
languages/ar/lessons/alphabet-and-sounds/index.html
languages/ar/lessons/food-and-ordering/index.html
languages/ar/lessons/greetings-and-introductions/index.html
languages/ar/lessons/numbers-1-to-20/index.html
languages/ar/lessons/present-tense-verbs/index.html
languages/ar/lessons/pronouns-and-to-be/index.html
languages/de/course/index.html
languages/de/index.html
languages/de/lessons/food-and-ordering/index.html
languages/de/lessons/greetings-and-introductions/index.html
languages/de/lessons/nouns-gender-and-articles/index.html
languages/de/lessons/numbers-1-to-20/index.html
languages/de/lessons/present-tense-regular-verbs/index.html
languages/de/lessons/sein-and-haben/index.html
languages/es/course/index.html
languages/es/index.html
languages/es/lessons/food-and-ordering/index.html
languages/es/lessons/gender-and-articles/index.html
languages/es/lessons/greetings-and-introductions/index.html
languages/es/lessons/numbers-1-to-20/index.html
languages/es/lessons/present-tense-regular-verbs/index.html
languages/es/lessons/ser-and-estar/index.html
languages/fr/course/index.html
languages/fr/index.html
languages/fr/lessons/etre-and-avoir/index.html
languages/fr/lessons/food-and-ordering/index.html
languages/fr/lessons/gender-and-articles/index.html
languages/fr/lessons/greetings-and-introductions/index.html
languages/fr/lessons/numbers-1-to-20/index.html
languages/fr/lessons/present-tense-regular-verbs/index.html
languages/index.html
languages/it/course/index.html
languages/it/index.html
languages/it/lessons/essere-and-avere/index.html
languages/it/lessons/food-and-ordering/index.html
languages/it/lessons/greetings-and-introductions/index.html
languages/it/lessons/nouns-gender-and-articles/index.html
languages/it/lessons/numbers-1-to-20/index.html
languages/it/lessons/present-tense-regular-verbs/index.html
languages/ja/course/index.html
languages/ja/index.html
languages/ja/lessons/desu-aru-iru/index.html
languages/ja/lessons/food-and-ordering/index.html
languages/ja/lessons/greetings-and-introductions/index.html
languages/ja/lessons/masu-verbs/index.html
languages/ja/lessons/numbers-and-counters/index.html
languages/ja/lessons/scripts-and-particles/index.html
languages/ko/course/index.html
languages/ko/index.html
languages/ko/lessons/food-and-ordering/index.html
languages/ko/lessons/greetings-and-introductions/index.html
languages/ko/lessons/hangul-and-particles/index.html
languages/ko/lessons/ida-and-isseoyo/index.html
languages/ko/lessons/present-tense-verbs/index.html
languages/ko/lessons/two-number-systems/index.html
languages/pt/course/index.html
languages/pt/index.html
languages/pt/lessons/food-and-ordering/index.html
languages/pt/lessons/greetings-and-introductions/index.html
languages/pt/lessons/nouns-gender-and-articles/index.html
languages/pt/lessons/numbers-1-to-20/index.html
languages/pt/lessons/present-tense-regular-verbs/index.html
languages/pt/lessons/ser-and-estar/index.html
languages/ru/course/index.html
languages/ru/index.html
languages/ru/lessons/byt-and-imet/index.html
languages/ru/lessons/food-and-ordering/index.html
languages/ru/lessons/greetings-and-introductions/index.html
languages/ru/lessons/nouns-gender-and-cases/index.html
languages/ru/lessons/numbers-1-to-20/index.html
languages/ru/lessons/present-tense-verbs/index.html
languages/zh/course/index.html
languages/zh/index.html
languages/zh/lessons/basic-sentences/index.html
languages/zh/lessons/food-and-ordering/index.html
languages/zh/lessons/greetings-and-introductions/index.html
languages/zh/lessons/numbers-and-measure-words/index.html
languages/zh/lessons/pinyin-and-tones/index.html
languages/zh/lessons/shi-you-and-zai/index.html
learn-hindi-from-afghanistan/index.html
learn-hindi-from-armenia/index.html
learn-hindi-from-azerbaijan/index.html
learn-hindi-from-bahrain/index.html
learn-hindi-from-bangladesh/index.html
learn-hindi-from-bhutan/index.html
learn-hindi-from-brunei/index.html
learn-hindi-from-cambodia/index.html
learn-hindi-from-canada/index.html
learn-hindi-from-ethiopia/index.html
learn-hindi-from-georgia/index.html
learn-hindi-from-haiti/index.html
learn-hindi-from-india/index.html
learn-hindi-from-indonesia/index.html
learn-hindi-from-iran/index.html
learn-hindi-from-iraq/index.html
learn-hindi-from-israel/index.html
learn-hindi-from-jordan/index.html
learn-hindi-from-kazakhstan/index.html
learn-hindi-from-kosovo/index.html
learn-hindi-from-kuwait/index.html
learn-hindi-from-kyrgyzstan/index.html
learn-hindi-from-laos/index.html
learn-hindi-from-lebanon/index.html
learn-hindi-from-malaysia/index.html
learn-hindi-from-maldives/index.html
learn-hindi-from-moldova/index.html
learn-hindi-from-myanmar/index.html
learn-hindi-from-nepal/index.html
learn-hindi-from-new-zealand/index.html
learn-hindi-from-oman/index.html
learn-hindi-from-pakistan/index.html
learn-hindi-from-palestine/index.html
learn-hindi-from-peru/index.html
learn-hindi-from-philippines/index.html
learn-hindi-from-poland/index.html
learn-hindi-from-qatar/index.html
learn-hindi-from-romania/index.html
learn-hindi-from-saudi-arabia/index.html
learn-hindi-from-singapore/index.html
learn-hindi-from-south-africa/index.html
learn-hindi-from-sri-lanka/index.html
learn-hindi-from-syria/index.html
learn-hindi-from-tajikistan/index.html
learn-hindi-from-thailand/index.html
learn-hindi-from-timor-leste/index.html
learn-hindi-from-turkiye/index.html
learn-hindi-from-turkmenistan/index.html
learn-hindi-from-uae/index.html
learn-hindi-from-uk/index.html
learn-hindi-from-usa/index.html
learn-hindi-from-uzbekistan/index.html
learn-hindi-from-vietnam/index.html
learn-hindi-from-yemen/index.html
learn/aap-tum-tu-hindi/index.html
learn/bengali/advanced/education/index.html
learn/bengali/advanced/festivals/index.html
learn/bengali/advanced/health/index.html
learn/bengali/advanced/home/index.html
learn/bengali/advanced/index.html
learn/bengali/advanced/office/index.html
learn/bengali/advanced/weather/index.html
learn/bengali/basics/index.html
learn/bengali/beginner/index.html
learn/bengali/conversation/index.html
learn/bengali/daily-life/index.html
learn/bengali/elementary/index.html
learn/bengali/food/index.html
learn/bengali/grammar/index.html
learn/bengali/index.html
learn/bengali/intermediate/index.html
learn/bengali/numbers/index.html
learn/bengali/pronunciation/index.html
learn/bengali/shopping/index.html
learn/bengali/time-dates/index.html
learn/bengali/travel/index.html
learn/bengali/vocabulary/index.html
learn/common-hindi-mistakes/index.html
learn/contexts/heritage/index.html
learn/contexts/index.html
learn/contexts/india-visitor/index.html
learn/countries/index.html
learn/gujarati/advanced/education/index.html
learn/gujarati/advanced/festivals/index.html
learn/gujarati/advanced/health/index.html
learn/gujarati/advanced/home/index.html
learn/gujarati/advanced/index.html
learn/gujarati/advanced/office/index.html
learn/gujarati/advanced/weather/index.html
learn/gujarati/basics/index.html
learn/gujarati/beginner/index.html
learn/gujarati/conversation/index.html
learn/gujarati/daily-life/index.html
learn/gujarati/elementary/index.html
learn/gujarati/food/index.html
learn/gujarati/grammar/index.html
learn/gujarati/index.html
learn/gujarati/intermediate/index.html
learn/gujarati/numbers/index.html
learn/gujarati/pronunciation/index.html
learn/gujarati/shopping/index.html
learn/gujarati/time-dates/index.html
learn/gujarati/travel/index.html
learn/gujarati/vocabulary/index.html
learn/hindi-alphabet-for-beginners/index.html
learn/hindi-barakhadi/index.html
learn/hindi-days-months-time/index.html
learn/hindi-family-words/index.html
learn/hindi-gender-masculine-feminine/index.html
learn/hindi-how-to-write-consonants/index.html
learn/hindi-how-to-write-vowels/index.html
learn/hindi-numbers-1-to-100/index.html
learn/hindi-or-urdu-difference/index.html
learn/hindi-phrases-for-travel/index.html
learn/hindi-sentence-structure/index.html
learn/hindi-verbs-present-past-future/index.html
learn/hindi/advanced/education/index.html
learn/hindi/advanced/festivals/index.html
learn/hindi/advanced/health/index.html
learn/hindi/advanced/home/index.html
learn/hindi/advanced/index.html
learn/hindi/advanced/office/index.html
learn/hindi/advanced/weather/index.html
learn/hindi/basics/index.html
learn/hindi/beginner/index.html
learn/hindi/conversation/index.html
learn/hindi/daily-life/index.html
learn/hindi/elementary/index.html
learn/hindi/food/index.html
learn/hindi/grammar/index.html
learn/hindi/index.html
learn/hindi/intermediate/index.html
learn/hindi/numbers/index.html
learn/hindi/pronunciation/index.html
learn/hindi/shopping/index.html
learn/hindi/time-dates/index.html
learn/hindi/travel/index.html
learn/hindi/vocabulary/index.html
learn/how-to-say-hello-in-hindi/index.html
learn/index.html
learn/learn-hindi-from-bollywood/index.html
learn/learn-hindi-online-guide/index.html
learn/marathi/advanced/education/index.html
learn/marathi/advanced/festivals/index.html
learn/marathi/advanced/health/index.html
learn/marathi/advanced/home/index.html
learn/marathi/advanced/index.html
learn/marathi/advanced/office/index.html
learn/marathi/advanced/weather/index.html
learn/marathi/basics/index.html
learn/marathi/beginner/index.html
learn/marathi/conversation/index.html
learn/marathi/daily-life/index.html
learn/marathi/elementary/index.html
learn/marathi/food/index.html
learn/marathi/grammar/index.html
learn/marathi/index.html
learn/marathi/intermediate/index.html
learn/marathi/numbers/index.html
learn/marathi/pronunciation/index.html
learn/marathi/shopping/index.html
learn/marathi/time-dates/index.html
learn/marathi/travel/index.html
learn/marathi/vocabulary/index.html
learn/paths/everyday-hindi/index.html
learn/paths/grammar-foundations/index.html
learn/paths/hindi-from-zero/index.html
learn/paths/index.html
learn/paths/reading-hindi/index.html
learn/paths/speaking-starter/index.html
learn/paths/travel-hindi/index.html
learn/practice/daily/index.html
learn/practice/grammar/index.html
learn/practice/index.html
learn/practice/listening/index.html
learn/practice/placement/index.html
learn/practice/pronunciation/index.html
learn/practice/reading/index.html
learn/practice/sentence-builder/index.html
learn/practice/speaking/index.html
learn/practice/verbs/index.html
learn/practice/vocabulary/index.html
learn/practice/writing/index.html
learn/punjabi/advanced/education/index.html
learn/punjabi/advanced/festivals/index.html
learn/punjabi/advanced/health/index.html
learn/punjabi/advanced/home/index.html
learn/punjabi/advanced/index.html
learn/punjabi/advanced/office/index.html
learn/punjabi/advanced/weather/index.html
learn/punjabi/basics/index.html
learn/punjabi/beginner/index.html
learn/punjabi/conversation/index.html
learn/punjabi/daily-life/index.html
learn/punjabi/elementary/index.html
learn/punjabi/food/index.html
learn/punjabi/grammar/index.html
learn/punjabi/index.html
learn/punjabi/intermediate/index.html
learn/punjabi/numbers/index.html
learn/punjabi/pronunciation/index.html
learn/punjabi/shopping/index.html
learn/punjabi/time-dates/index.html
learn/punjabi/travel/index.html
learn/punjabi/vocabulary/index.html
learn/tamil/advanced/education/index.html
learn/tamil/advanced/festivals/index.html
learn/tamil/advanced/health/index.html
learn/tamil/advanced/home/index.html
learn/tamil/advanced/index.html
learn/tamil/advanced/office/index.html
learn/tamil/advanced/weather/index.html
learn/tamil/basics/index.html
learn/tamil/beginner/index.html
learn/tamil/conversation/index.html
learn/tamil/daily-life/index.html
learn/tamil/elementary/index.html
learn/tamil/food/index.html
learn/tamil/grammar/index.html
learn/tamil/index.html
learn/tamil/intermediate/index.html
learn/tamil/numbers/index.html
learn/tamil/pronunciation/index.html
learn/tamil/shopping/index.html
learn/tamil/time-dates/index.html
learn/tamil/travel/index.html
learn/tamil/vocabulary/index.html
learn/telugu/advanced/education/index.html
learn/telugu/advanced/festivals/index.html
learn/telugu/advanced/health/index.html
learn/telugu/advanced/home/index.html
learn/telugu/advanced/index.html
learn/telugu/advanced/office/index.html
learn/telugu/advanced/weather/index.html
learn/telugu/basics/index.html
learn/telugu/beginner/index.html
learn/telugu/conversation/index.html
learn/telugu/daily-life/index.html
learn/telugu/elementary/index.html
learn/telugu/food/index.html
learn/telugu/grammar/index.html
learn/telugu/index.html
learn/telugu/intermediate/index.html
learn/telugu/numbers/index.html
learn/telugu/pronunciation/index.html
learn/telugu/shopping/index.html
learn/telugu/time-dates/index.html
learn/telugu/travel/index.html
learn/telugu/vocabulary/index.html
learn/urdu/advanced/education/index.html
learn/urdu/advanced/festivals/index.html
learn/urdu/advanced/health/index.html
learn/urdu/advanced/home/index.html
learn/urdu/advanced/index.html
learn/urdu/advanced/office/index.html
learn/urdu/advanced/weather/index.html
learn/urdu/basics/index.html
learn/urdu/beginner/index.html
learn/urdu/conversation/index.html
learn/urdu/daily-life/index.html
learn/urdu/elementary/index.html
learn/urdu/food/index.html
learn/urdu/grammar/index.html
learn/urdu/index.html
learn/urdu/intermediate/index.html
learn/urdu/numbers/index.html
learn/urdu/pronunciation/index.html
learn/urdu/shopping/index.html
learn/urdu/time-dates/index.html
learn/urdu/travel/index.html
learn/urdu/vocabulary/index.html
learn/write-your-name-in-hindi/index.html
marathi/alphabet/index.html
marathi/beginners/index.html
marathi/business/index.html
marathi/conversation/index.html
marathi/emergency/index.html
marathi/family/index.html
marathi/flashcards-topic/index.html
marathi/for-kids/index.html
marathi/formal-informal/index.html
marathi/grammar/index.html
marathi/greetings/index.html
marathi/heritage/index.html
marathi/how-long/index.html
marathi/indian-languages/index.html
marathi/listening/index.html
marathi/marathi-cinema/index.html
marathi/marathi-vs-hindi/index.html
marathi/mistakes/index.html
marathi/name-topic/index.html
marathi/numbers/index.html
marathi/phrases-food/index.html
marathi/phrases-travel/index.html
marathi/pronunciation/index.html
marathi/reading/index.html
marathi/relationships/index.html
marathi/sentence-structure/index.html
marathi/shopping/index.html
marathi/slang/index.html
marathi/speaking/index.html
marathi/time-date/index.html
marathi/verbs/index.html
marathi/vocabulary/index.html
marathi/writing/index.html
materials/alphabet/devanagari-chart/index.html
materials/beginner/reading-guide/index.html
materials/conversation/polite-vs-casual/index.html
materials/family/family-words-quick-ref/index.html
materials/grammar/beginner-grammar-reference/index.html
materials/grammar/postpositions/index.html
materials/grammar/sentence-patterns/index.html
materials/index.html
materials/pronunciation/pronunciation-guide/index.html
materials/reading/reading-practice/index.html
materials/revision/mistakes-checklist/index.html
materials/travel/restaurant-shopping-transport/index.html
materials/verbs/essential-verbs/index.html
materials/vocabulary/100-essential-words/index.html
materials/work/work-phrases/index.html
materials/writing/writing-practice/index.html
monetization-disclosure/index.html
name-in-hindi/index.html
pl/hindi/index.html
pt/find-tutors.html
pt/hindi/index.html
pt/index.html
pt/join.html
punjabi/alphabet/index.html
punjabi/beginners/index.html
punjabi/business/index.html
punjabi/conversation/index.html
punjabi/emergency/index.html
punjabi/family/index.html
punjabi/flashcards-topic/index.html
punjabi/for-kids/index.html
punjabi/formal-informal/index.html
punjabi/grammar/index.html
punjabi/greetings/index.html
punjabi/heritage/index.html
punjabi/how-long/index.html
punjabi/indian-languages/index.html
punjabi/listening/index.html
punjabi/mistakes/index.html
punjabi/name-topic/index.html
punjabi/numbers/index.html
punjabi/phrases-food/index.html
punjabi/phrases-travel/index.html
punjabi/pollywood/index.html
punjabi/pronunciation/index.html
punjabi/punjabi-vs-hindi/index.html
punjabi/reading/index.html
punjabi/relationships/index.html
punjabi/sentence-structure/index.html
punjabi/shopping/index.html
punjabi/slang/index.html
punjabi/speaking/index.html
punjabi/time-date/index.html
punjabi/verbs/index.html
punjabi/vocabulary/index.html
punjabi/writing/index.html
ru/hindi/index.html
start/index.html
tamil/alphabet/index.html
tamil/beginners/index.html
tamil/business/index.html
tamil/conversation/index.html
tamil/emergency/index.html
tamil/family/index.html
tamil/flashcards-topic/index.html
tamil/for-kids/index.html
tamil/formal-informal/index.html
tamil/grammar/index.html
tamil/greetings/index.html
tamil/heritage/index.html
tamil/how-long/index.html
tamil/indian-languages/index.html
tamil/kollywood/index.html
tamil/listening/index.html
tamil/mistakes/index.html
tamil/name-topic/index.html
tamil/numbers/index.html
tamil/phrases-food/index.html
tamil/phrases-travel/index.html
tamil/pronunciation/index.html
tamil/reading/index.html
tamil/relationships/index.html
tamil/sentence-structure/index.html
tamil/shopping/index.html
tamil/slang/index.html
tamil/speaking/index.html
tamil/time-date/index.html
tamil/verbs/index.html
tamil/vocabulary/index.html
tamil/writing/index.html
telugu/alphabet/index.html
telugu/beginners/index.html
telugu/business/index.html
telugu/conversation/index.html
telugu/emergency/index.html
telugu/family/index.html
telugu/flashcards-topic/index.html
telugu/for-kids/index.html
telugu/formal-informal/index.html
telugu/grammar/index.html
telugu/greetings/index.html
telugu/heritage/index.html
telugu/how-long/index.html
telugu/indian-languages/index.html
telugu/listening/index.html
telugu/mistakes/index.html
telugu/name-topic/index.html
telugu/numbers/index.html
telugu/phrases-food/index.html
telugu/phrases-travel/index.html
telugu/pronunciation/index.html
telugu/reading/index.html
telugu/relationships/index.html
telugu/sentence-structure/index.html
telugu/shopping/index.html
telugu/slang/index.html
telugu/speaking/index.html
telugu/telugu-vs-tamil/index.html
telugu/time-date/index.html
telugu/tollywood/index.html
telugu/verbs/index.html
telugu/vocabulary/index.html
telugu/writing/index.html
tr/hindi/index.html
ur/hindi/index.html
urdu/alphabet/index.html
urdu/beginners/index.html
urdu/business/index.html
urdu/conversation/index.html
urdu/emergency/index.html
urdu/family/index.html
urdu/flashcards-topic/index.html
urdu/for-kids/index.html
urdu/formal-informal/index.html
urdu/grammar/index.html
urdu/greetings/index.html
urdu/heritage/index.html
urdu/how-long/index.html
urdu/indian-languages/index.html
urdu/listening/index.html
urdu/lollywood/index.html
urdu/mistakes/index.html
urdu/name-topic/index.html
urdu/numbers/index.html
urdu/phrases-food/index.html
urdu/phrases-travel/index.html
urdu/pronunciation/index.html
urdu/reading/index.html
urdu/relationships/index.html
urdu/sentence-structure/index.html
urdu/shopping/index.html
urdu/slang/index.html
urdu/speaking/index.html
urdu/time-date/index.html
urdu/urdu-vs-hindi/index.html
urdu/verbs/index.html
urdu/vocabulary/index.html
urdu/writing/index.html
vi/hindi/index.html
zh/hindi/index.html
```

## E-2 · SECTION COUNTS (eligible)
```
      3 ROOT/pt
      3 ROOT/ja
      3 ROOT/fr
      3 ROOT/es
      3 ROOT/de
      3 ROOT/ar
      1 zh/hindi
      1 vi/hindi
      1 urdu/writing
      1 urdu/vocabulary
      1 urdu/verbs
      1 urdu/urdu-vs-hindi
      1 urdu/time-date
      1 urdu/speaking
      1 urdu/slang
      1 urdu/shopping
      1 urdu/sentence-structure
      1 urdu/relationships
      1 urdu/reading
      1 urdu/pronunciation
      1 urdu/phrases-travel
      1 urdu/phrases-food
      1 urdu/numbers
      1 urdu/name-topic
      1 urdu/mistakes
      1 urdu/lollywood
      1 urdu/listening
      1 urdu/indian-languages
      1 urdu/how-long
      1 urdu/heritage
      1 urdu/greetings
      1 urdu/grammar
      1 urdu/formal-informal
      1 urdu/for-kids
      1 urdu/flashcards-topic
      1 urdu/family
      1 urdu/emergency
      1 urdu/conversation
      1 urdu/business
      1 urdu/beginners
      1 urdu/alphabet
      1 ur/hindi
      1 tr/hindi
      1 telugu/writing
      1 telugu/vocabulary
      1 telugu/verbs
      1 telugu/tollywood
      1 telugu/time-date
      1 telugu/telugu-vs-tamil
      1 telugu/speaking
      1 telugu/slang
      1 telugu/shopping
      1 telugu/sentence-structure
      1 telugu/relationships
      1 telugu/reading
      1 telugu/pronunciation
      1 telugu/phrases-travel
      1 telugu/phrases-food
      1 telugu/numbers
      1 telugu/name-topic
      1 telugu/mistakes
      1 telugu/listening
      1 telugu/indian-languages
      1 telugu/how-long
      1 telugu/heritage
      1 telugu/greetings
      1 telugu/grammar
      1 telugu/formal-informal
      1 telugu/for-kids
      1 telugu/flashcards-topic
      1 telugu/family
      1 telugu/emergency
      1 telugu/conversation
      1 telugu/business
      1 telugu/beginners
      1 telugu/alphabet
      1 tamil/writing
      1 tamil/vocabulary
      1 tamil/verbs
      1 tamil/time-date
      1 tamil/speaking
      1 tamil/slang
      1 tamil/shopping
      1 tamil/sentence-structure
      1 tamil/relationships
      1 tamil/reading
      1 tamil/pronunciation
      1 tamil/phrases-travel
      1 tamil/phrases-food
      1 tamil/numbers
      1 tamil/name-topic
      1 tamil/mistakes
      1 tamil/listening
      1 tamil/kollywood
      1 tamil/indian-languages
      1 tamil/how-long
      1 tamil/heritage
      1 tamil/greetings
      1 tamil/grammar
      1 tamil/formal-informal
      1 tamil/for-kids
      1 tamil/flashcards-topic
      1 tamil/family
      1 tamil/emergency
      1 tamil/conversation
      1 tamil/business
      1 tamil/beginners
      1 tamil/alphabet
      1 ru/hindi
      1 punjabi/writing
      1 punjabi/vocabulary
      1 punjabi/verbs
      1 punjabi/time-date
      1 punjabi/speaking
      1 punjabi/slang
      1 punjabi/shopping
      1 punjabi/sentence-structure
      1 punjabi/relationships
      1 punjabi/reading
      1 punjabi/punjabi-vs-hindi
      1 punjabi/pronunciation
      1 punjabi/pollywood
      1 punjabi/phrases-travel
      1 punjabi/phrases-food
      1 punjabi/numbers
      1 punjabi/name-topic
      1 punjabi/mistakes
      1 punjabi/listening
      1 punjabi/indian-languages
      1 punjabi/how-long
      1 punjabi/heritage
      1 punjabi/greetings
      1 punjabi/grammar
      1 punjabi/formal-informal
      1 punjabi/for-kids
      1 punjabi/flashcards-topic
      1 punjabi/family
      1 punjabi/emergency
      1 punjabi/conversation
      1 punjabi/business
      1 punjabi/beginners
      1 punjabi/alphabet
      1 pt/hindi
      1 pl/hindi
      1 materials/writing/writing-practice
      1 materials/work/work-phrases
      1 materials/vocabulary/100-essential-words
      1 materials/verbs/essential-verbs
      1 materials/travel/restaurant-shopping-transport
      1 materials/revision/mistakes-checklist
      1 materials/reading/reading-practice
      1 materials/pronunciation/pronunciation-guide
      1 materials/grammar/sentence-patterns
      1 materials/grammar/postpositions
      1 materials/grammar/beginner-grammar-reference
      1 materials/family/family-words-quick-ref
      1 materials/conversation/polite-vs-casual
      1 materials/beginner/reading-guide
      1 materials/alphabet/devanagari-chart
      1 marathi/writing
      1 marathi/vocabulary
      1 marathi/verbs
      1 marathi/time-date
      1 marathi/speaking
      1 marathi/slang
      1 marathi/shopping
      1 marathi/sentence-structure
      1 marathi/relationships
      1 marathi/reading
      1 marathi/pronunciation
      1 marathi/phrases-travel
      1 marathi/phrases-food
      1 marathi/numbers
      1 marathi/name-topic
      1 marathi/mistakes
      1 marathi/marathi-vs-hindi
      1 marathi/marathi-cinema
      1 marathi/listening
      1 marathi/indian-languages
      1 marathi/how-long
      1 marathi/heritage
      1 marathi/greetings
      1 marathi/grammar
      1 marathi/formal-informal
      1 marathi/for-kids
      1 marathi/flashcards-topic
      1 marathi/family
      1 marathi/emergency
      1 marathi/conversation
      1 marathi/business
      1 marathi/beginners
      1 marathi/alphabet
      1 learn/write-your-name-in-hindi
      1 learn/urdu/vocabulary
      1 learn/urdu/travel
      1 learn/urdu/time-dates
      1 learn/urdu/shopping
      1 learn/urdu/pronunciation
      1 learn/urdu/numbers
      1 learn/urdu/intermediate
      1 learn/urdu/grammar
      1 learn/urdu/food
      1 learn/urdu/elementary
      1 learn/urdu/daily-life
      1 learn/urdu/conversation
      1 learn/urdu/beginner
      1 learn/urdu/basics
      1 learn/urdu/advanced/weather
      1 learn/urdu/advanced/office
      1 learn/urdu/advanced/home
      1 learn/urdu/advanced/health
      1 learn/urdu/advanced/festivals
      1 learn/urdu/advanced/education
      1 learn/urdu/advanced
      1 learn/urdu
      1 learn/telugu/vocabulary
      1 learn/telugu/travel
      1 learn/telugu/time-dates
      1 learn/telugu/shopping
      1 learn/telugu/pronunciation
      1 learn/telugu/numbers
      1 learn/telugu/intermediate
      1 learn/telugu/grammar
      1 learn/telugu/food
      1 learn/telugu/elementary
      1 learn/telugu/daily-life
      1 learn/telugu/conversation
      1 learn/telugu/beginner
      1 learn/telugu/basics
      1 learn/telugu/advanced/weather
      1 learn/telugu/advanced/office
      1 learn/telugu/advanced/home
      1 learn/telugu/advanced/health
      1 learn/telugu/advanced/festivals
      1 learn/telugu/advanced/education
      1 learn/telugu/advanced
      1 learn/telugu
      1 learn/tamil/vocabulary
      1 learn/tamil/travel
      1 learn/tamil/time-dates
      1 learn/tamil/shopping
      1 learn/tamil/pronunciation
      1 learn/tamil/numbers
      1 learn/tamil/intermediate
      1 learn/tamil/grammar
      1 learn/tamil/food
      1 learn/tamil/elementary
      1 learn/tamil/daily-life
      1 learn/tamil/conversation
      1 learn/tamil/beginner
      1 learn/tamil/basics
      1 learn/tamil/advanced/weather
      1 learn/tamil/advanced/office
      1 learn/tamil/advanced/home
      1 learn/tamil/advanced/health
      1 learn/tamil/advanced/festivals
      1 learn/tamil/advanced/education
      1 learn/tamil/advanced
      1 learn/tamil
      1 learn/punjabi/vocabulary
      1 learn/punjabi/travel
      1 learn/punjabi/time-dates
      1 learn/punjabi/shopping
      1 learn/punjabi/pronunciation
      1 learn/punjabi/numbers
      1 learn/punjabi/intermediate
      1 learn/punjabi/grammar
      1 learn/punjabi/food
      1 learn/punjabi/elementary
      1 learn/punjabi/daily-life
      1 learn/punjabi/conversation
      1 learn/punjabi/beginner
      1 learn/punjabi/basics
      1 learn/punjabi/advanced/weather
      1 learn/punjabi/advanced/office
      1 learn/punjabi/advanced/home
      1 learn/punjabi/advanced/health
      1 learn/punjabi/advanced/festivals
      1 learn/punjabi/advanced/education
      1 learn/punjabi/advanced
      1 learn/punjabi
      1 learn/practice/writing
      1 learn/practice/vocabulary
      1 learn/practice/verbs
      1 learn/practice/speaking
      1 learn/practice/sentence-builder
      1 learn/practice/reading
      1 learn/practice/pronunciation
      1 learn/practice/placement
      1 learn/practice/listening
      1 learn/practice/grammar
      1 learn/practice/daily
      1 learn/practice
      1 learn/paths/travel-hindi
      1 learn/paths/speaking-starter
      1 learn/paths/reading-hindi
      1 learn/paths/hindi-from-zero
      1 learn/paths/grammar-foundations
      1 learn/paths/everyday-hindi
      1 learn/paths
      1 learn/marathi/vocabulary
      1 learn/marathi/travel
      1 learn/marathi/time-dates
      1 learn/marathi/shopping
      1 learn/marathi/pronunciation
      1 learn/marathi/numbers
      1 learn/marathi/intermediate
      1 learn/marathi/grammar
      1 learn/marathi/food
      1 learn/marathi/elementary
      1 learn/marathi/daily-life
      1 learn/marathi/conversation
      1 learn/marathi/beginner
      1 learn/marathi/basics
      1 learn/marathi/advanced/weather
      1 learn/marathi/advanced/office
      1 learn/marathi/advanced/home
      1 learn/marathi/advanced/health
      1 learn/marathi/advanced/festivals
      1 learn/marathi/advanced/education
      1 learn/marathi/advanced
      1 learn/marathi
      1 learn/learn-hindi-online-guide
      1 learn/learn-hindi-from-bollywood
      1 learn/how-to-say-hello-in-hindi
      1 learn/hindi/vocabulary
      1 learn/hindi/travel
      1 learn/hindi/time-dates
      1 learn/hindi/shopping
      1 learn/hindi/pronunciation
      1 learn/hindi/numbers
      1 learn/hindi/intermediate
      1 learn/hindi/grammar
      1 learn/hindi/food
      1 learn/hindi/elementary
      1 learn/hindi/daily-life
      1 learn/hindi/conversation
      1 learn/hindi/beginner
      1 learn/hindi/basics
      1 learn/hindi/advanced/weather
      1 learn/hindi/advanced/office
      1 learn/hindi/advanced/home
      1 learn/hindi/advanced/health
      1 learn/hindi/advanced/festivals
      1 learn/hindi/advanced/education
      1 learn/hindi/advanced
      1 learn/hindi-verbs-present-past-future
      1 learn/hindi-sentence-structure
      1 learn/hindi-phrases-for-travel
      1 learn/hindi-or-urdu-difference
      1 learn/hindi-numbers-1-to-100
      1 learn/hindi-how-to-write-vowels
      1 learn/hindi-how-to-write-consonants
      1 learn/hindi-gender-masculine-feminine
      1 learn/hindi-family-words
      1 learn/hindi-days-months-time
      1 learn/hindi-barakhadi
      1 learn/hindi-alphabet-for-beginners
      1 learn/hindi
      1 learn/gujarati/vocabulary
      1 learn/gujarati/travel
      1 learn/gujarati/time-dates
      1 learn/gujarati/shopping
      1 learn/gujarati/pronunciation
      1 learn/gujarati/numbers
      1 learn/gujarati/intermediate
      1 learn/gujarati/grammar
      1 learn/gujarati/food
      1 learn/gujarati/elementary
      1 learn/gujarati/daily-life
      1 learn/gujarati/conversation
      1 learn/gujarati/beginner
      1 learn/gujarati/basics
      1 learn/gujarati/advanced/weather
      1 learn/gujarati/advanced/office
      1 learn/gujarati/advanced/home
      1 learn/gujarati/advanced/health
      1 learn/gujarati/advanced/festivals
      1 learn/gujarati/advanced/education
      1 learn/gujarati/advanced
      1 learn/gujarati
      1 learn/countries
      1 learn/contexts/india-visitor
      1 learn/contexts/heritage
      1 learn/contexts
      1 learn/common-hindi-mistakes
      1 learn/bengali/vocabulary
      1 learn/bengali/travel
      1 learn/bengali/time-dates
      1 learn/bengali/shopping
      1 learn/bengali/pronunciation
      1 learn/bengali/numbers
      1 learn/bengali/intermediate
      1 learn/bengali/grammar
      1 learn/bengali/food
      1 learn/bengali/elementary
      1 learn/bengali/daily-life
      1 learn/bengali/conversation
      1 learn/bengali/beginner
      1 learn/bengali/basics
      1 learn/bengali/advanced/weather
      1 learn/bengali/advanced/office
      1 learn/bengali/advanced/home
      1 learn/bengali/advanced/health
      1 learn/bengali/advanced/festivals
      1 learn/bengali/advanced/education
      1 learn/bengali/advanced
      1 learn/bengali
      1 learn/aap-tum-tu-hindi
      1 languages/zh/lessons/shi-you-and-zai
      1 languages/zh/lessons/pinyin-and-tones
      1 languages/zh/lessons/numbers-and-measure-words
      1 languages/zh/lessons/greetings-and-introductions
      1 languages/zh/lessons/food-and-ordering
      1 languages/zh/lessons/basic-sentences
      1 languages/zh/course
      1 languages/zh
      1 languages/ru/lessons/present-tense-verbs
      1 languages/ru/lessons/numbers-1-to-20
      1 languages/ru/lessons/nouns-gender-and-cases
      1 languages/ru/lessons/greetings-and-introductions
      1 languages/ru/lessons/food-and-ordering
      1 languages/ru/lessons/byt-and-imet
      1 languages/ru/course
      1 languages/ru
      1 languages/pt/lessons/ser-and-estar
      1 languages/pt/lessons/present-tense-regular-verbs
      1 languages/pt/lessons/numbers-1-to-20
      1 languages/pt/lessons/nouns-gender-and-articles
      1 languages/pt/lessons/greetings-and-introductions
      1 languages/pt/lessons/food-and-ordering
      1 languages/pt/course
      1 languages/pt
      1 languages/ko/lessons/two-number-systems
      1 languages/ko/lessons/present-tense-verbs
      1 languages/ko/lessons/ida-and-isseoyo
      1 languages/ko/lessons/hangul-and-particles
      1 languages/ko/lessons/greetings-and-introductions
      1 languages/ko/lessons/food-and-ordering
      1 languages/ko/course
      1 languages/ko
      1 languages/ja/lessons/scripts-and-particles
      1 languages/ja/lessons/numbers-and-counters
      1 languages/ja/lessons/masu-verbs
      1 languages/ja/lessons/greetings-and-introductions
      1 languages/ja/lessons/food-and-ordering
      1 languages/ja/lessons/desu-aru-iru
      1 languages/ja/course
      1 languages/ja
      1 languages/it/lessons/present-tense-regular-verbs
      1 languages/it/lessons/numbers-1-to-20
      1 languages/it/lessons/nouns-gender-and-articles
      1 languages/it/lessons/greetings-and-introductions
      1 languages/it/lessons/food-and-ordering
      1 languages/it/lessons/essere-and-avere
      1 languages/it/course
      1 languages/it
      1 languages/fr/lessons/present-tense-regular-verbs
      1 languages/fr/lessons/numbers-1-to-20
      1 languages/fr/lessons/greetings-and-introductions
      1 languages/fr/lessons/gender-and-articles
      1 languages/fr/lessons/food-and-ordering
      1 languages/fr/lessons/etre-and-avoir
      1 languages/fr/course
      1 languages/fr
      1 languages/es/lessons/ser-and-estar
      1 languages/es/lessons/present-tense-regular-verbs
      1 languages/es/lessons/numbers-1-to-20
      1 languages/es/lessons/greetings-and-introductions
      1 languages/es/lessons/gender-and-articles
      1 languages/es/lessons/food-and-ordering
      1 languages/es/course
      1 languages/es
      1 languages/de/lessons/sein-and-haben
      1 languages/de/lessons/present-tense-regular-verbs
      1 languages/de/lessons/numbers-1-to-20
      1 languages/de/lessons/nouns-gender-and-articles
      1 languages/de/lessons/greetings-and-introductions
      1 languages/de/lessons/food-and-ordering
      1 languages/de/course
      1 languages/de
      1 languages/ar/lessons/pronouns-and-to-be
      1 languages/ar/lessons/present-tense-verbs
      1 languages/ar/lessons/numbers-1-to-20
      1 languages/ar/lessons/greetings-and-introductions
      1 languages/ar/lessons/food-and-ordering
      1 languages/ar/lessons/alphabet-and-sounds
      1 languages/ar/course
      1 languages/ar
      1 ko/hindi
      1 ja/hindi
      1 it/hindi
      1 id/hindi
      1 hindi/writing
      1 hindi/vocabulary
      1 hindi/verbs
      1 hindi/time-date
      1 hindi/speaking
      1 hindi/slang
      1 hindi/shopping
      1 hindi/sentence-structure
      1 hindi/relationships
      1 hindi/reading
      1 hindi/pronunciation
      1 hindi/phrases-travel
      1 hindi/phrases-food
      1 hindi/numbers
      1 hindi/name-topic
      1 hindi/mistakes
      1 hindi/listening
      1 hindi/indian-languages
      1 hindi/how-long
      1 hindi/hinglish
      1 hindi/hindi-vs-urdu
      1 hindi/heritage
      1 hindi/greetings
      1 hindi/grammar
      1 hindi/formal-informal
      1 hindi/for-kids
      1 hindi/flashcards-topic
      1 hindi/family
      1 hindi/emergency
      1 hindi/conversation
      1 hindi/business
      1 hindi/bollywood
      1 hindi/beginners
      1 hindi/alphabet
      1 hindi-tutor/worldwide
      1 hindi-tutor/united-states
      1 hindi-tutor/united-kingdom
      1 hindi-tutor/united-arab-emirates
      1 hindi-tutor/toronto
      1 hindi-tutor/sydney
      1 hindi-tutor/spain
      1 hindi-tutor/south-africa
      1 hindi-tutor/singapore
      1 hindi-tutor/san-francisco
      1 hindi-tutor/pune
      1 hindi-tutor/patna
      1 hindi-tutor/new-york
      1 hindi-tutor/nepal
      1 hindi-tutor/mumbai
      1 hindi-tutor/melbourne
      1 hindi-tutor/lucknow
      1 hindi-tutor/london
      1 hindi-tutor/kolkata
      1 hindi-tutor/japan
      1 hindi-tutor/jaipur
      1 hindi-tutor/hyderabad
      1 hindi-tutor/houston
      1 hindi-tutor/germany
      1 hindi-tutor/dubai
      1 hindi-tutor/delhi
      1 hindi-tutor/chennai
      1 hindi-tutor/chandigarh
      1 hindi-tutor/canada
      1 hindi-tutor/bangalore
      1 hindi-tutor/australia
      1 hindi-tutor/ahmedabad
      1 gujarati/writing
      1 gujarati/vocabulary
      1 gujarati/verbs
      1 gujarati/time-date
      1 gujarati/speaking
      1 gujarati/slang
      1 gujarati/shopping
      1 gujarati/sentence-structure
      1 gujarati/relationships
      1 gujarati/reading
      1 gujarati/pronunciation
      1 gujarati/phrases-travel
      1 gujarati/phrases-food
      1 gujarati/numbers
      1 gujarati/name-topic
      1 gujarati/mistakes
      1 gujarati/listening
      1 gujarati/indian-languages
      1 gujarati/how-long
      1 gujarati/heritage
      1 gujarati/gujarati-vs-hindi
      1 gujarati/gujarati-cinema
      1 gujarati/greetings
      1 gujarati/grammar
      1 gujarati/formal-informal
      1 gujarati/for-kids
      1 gujarati/flashcards-topic
      1 gujarati/family
      1 gujarati/emergency
      1 gujarati/conversation
      1 gujarati/business
      1 gujarati/beginners
      1 gujarati/alphabet
      1 fr/hindi
      1 es/hindi
      1 de/hindi
      1 daily-hindi/day-9
      1 daily-hindi/day-8
      1 daily-hindi/day-7
      1 daily-hindi/day-6
      1 daily-hindi/day-5
      1 daily-hindi/day-4
      1 daily-hindi/day-30
      1 daily-hindi/day-3
      1 daily-hindi/day-29
      1 daily-hindi/day-28
      1 daily-hindi/day-27
      1 daily-hindi/day-26
      1 daily-hindi/day-25
      1 daily-hindi/day-24
      1 daily-hindi/day-23
      1 daily-hindi/day-22
      1 daily-hindi/day-21
      1 daily-hindi/day-20
      1 daily-hindi/day-2
      1 daily-hindi/day-19
      1 daily-hindi/day-18
      1 daily-hindi/day-17
      1 daily-hindi/day-16
      1 daily-hindi/day-15
      1 daily-hindi/day-14
      1 daily-hindi/day-13
      1 daily-hindi/day-12
      1 daily-hindi/day-11
      1 daily-hindi/day-10
      1 daily-hindi/day-1
      1 bn/hindi
      1 bengali/writing
      1 bengali/vocabulary
      1 bengali/verbs
      1 bengali/time-date
      1 bengali/speaking
      1 bengali/slang
      1 bengali/shopping
      1 bengali/sentence-structure
      1 bengali/relationships
      1 bengali/reading
      1 bengali/pronunciation
      1 bengali/phrases-travel
      1 bengali/phrases-food
      1 bengali/numbers
      1 bengali/name-topic
      1 bengali/mistakes
      1 bengali/listening
      1 bengali/indian-languages
      1 bengali/how-long
      1 bengali/heritage
      1 bengali/greetings
      1 bengali/grammar
      1 bengali/formal-informal
      1 bengali/for-kids
      1 bengali/flashcards-topic
      1 bengali/family
      1 bengali/emergency
      1 bengali/conversation
      1 bengali/business
      1 bengali/bollywood
      1 bengali/beginners
      1 bengali/alphabet
      1 ask/what-is-the-hardest-part-of-hindi
      1 ask/what-is-the-best-age-to-learn-hindi
      1 ask/what-does-yaar-mean-in-hindi
      1 ask/what-does-namaste-really-mean
      1 ask/what-does-acha-mean-in-hindi
      1 ask/is-italki-or-preply-better-for-hindi
      1 ask/is-hindi-useful-to-learn
      1 ask/is-hindi-or-spanish-easier-to-learn
      1 ask/is-hindi-hard-to-learn
      1 ask/is-duolingo-good-for-hindi
      1 ask/how-to-write-name-hindi-question
      1 ask/how-to-say-yes-and-no-in-hindi
      1 ask/how-to-say-what-is-your-name-in-hindi
      1 ask/how-to-say-thank-you-in-hindi
      1 ask/how-to-say-sorry-in-hindi-properly
      1 ask/how-to-say-sorry-in-hindi
      1 ask/how-to-say-please-in-hindi
      1 ask/how-to-say-i-love-you-in-hindi
      1 ask/how-to-say-i-dont-understand-in-hindi
      1 ask/how-to-say-how-are-you-in-hindi
      1 ask/how-to-say-hello-in-hindi-question
      1 ask/how-to-say-good-morning-in-hindi
      1 ask/how-to-remember-hindi-genders
      1 ask/how-to-practice-hindi-without-a-partner
      1 ask/how-to-introduce-yourself-in-hindi
      1 ask/how-to-count-1-to-10-in-hindi
      1 ask/how-much-does-a-hindi-tutor-cost
      1 ask/how-many-words-do-i-need-in-hindi
      1 ask/how-long-to-read-hindi-script
      1 ask/how-long-to-learn-hindi
      1 ask/hindi-words-every-beginner-should-know
      1 ask/hindi-or-urdu-which-to-learn
      1 ask/hindi-or-urdu-question
      1 ask/hindi-for-kids-how-to-start
      1 ask/hindi-family-question
      1 ask/hindi-alphabet-question
      1 ask/do-i-need-to-learn-devanagari
      1 ask/do-hindi-speakers-mind-mistakes
      1 ask/cheapest-way-to-learn-hindi
      1 ask/can-i-learn-hindi-in-3-months
      1 ask/can-i-learn-hindi-from-bollywood-alone
      1 ask/can-i-learn-hindi-by-myself
      1 ask/best-way-to-learn-hindi-for-beginners
      1 ar/hindi
      1 answers/what-does-ji-mean-in-hindi
      1 answers/how-to-type-hindi-on-phone
      1 answers/how-to-tell-the-time-in-hindi
      1 answers/how-to-say-please-and-thank-you-in-hindi
      1 answers/how-to-say-i-am-learning-hindi
      1 answers/how-to-say-i-am-hungry-in-hindi
      1 answers/how-to-say-goodbye-in-hindi
      1 answers/how-to-practice-hindi-speaking-alone
      1 answers/how-to-order-food-in-hindi
      1 answers/how-to-ask-for-directions-in-hindi
      1 answers/hindi-word-order-explained
      1 answers/hindi-vs-punjabi-vs-bengali
      1 answers/hindi-verb-hona-to-be
      1 answers/hindi-pronouns-explained
      1 answers/hindi-postpositions-ka-ki-ke
      1 answers/hindi-phrases-for-travelling-in-india
      1 answers/hindi-numbers-1-to-100
      1 answers/hindi-months-and-seasons
      1 answers/hindi-greetings-namaste-and-others
      1 answers/hindi-family-words
      1 answers/hindi-days-of-the-week
      1 answers/hindi-colours-list
      1 answers/hindi-body-parts-vocabulary
      1 answers/difference-between-hindi-and-urdu
      1 answers/can-i-learn-hindi-without-learning-the-script
      1 answers/best-way-to-learn-hindi-as-a-beginner
      1 answers/best-hindi-movies-to-learn-hindi
      1 ROOT/start
      1 ROOT/name-in-hindi
      1 ROOT/monetization-disclosure
      1 ROOT/materials
      1 ROOT/learn-hindi-from-yemen
      1 ROOT/learn-hindi-from-vietnam
      1 ROOT/learn-hindi-from-uzbekistan
      1 ROOT/learn-hindi-from-usa
      1 ROOT/learn-hindi-from-uk
      1 ROOT/learn-hindi-from-uae
      1 ROOT/learn-hindi-from-turkmenistan
      1 ROOT/learn-hindi-from-turkiye
      1 ROOT/learn-hindi-from-timor-leste
      1 ROOT/learn-hindi-from-thailand
      1 ROOT/learn-hindi-from-tajikistan
      1 ROOT/learn-hindi-from-syria
      1 ROOT/learn-hindi-from-sri-lanka
      1 ROOT/learn-hindi-from-south-africa
      1 ROOT/learn-hindi-from-singapore
      1 ROOT/learn-hindi-from-saudi-arabia
      1 ROOT/learn-hindi-from-romania
      1 ROOT/learn-hindi-from-qatar
      1 ROOT/learn-hindi-from-poland
      1 ROOT/learn-hindi-from-philippines
      1 ROOT/learn-hindi-from-peru
      1 ROOT/learn-hindi-from-palestine
      1 ROOT/learn-hindi-from-pakistan
      1 ROOT/learn-hindi-from-oman
      1 ROOT/learn-hindi-from-new-zealand
      1 ROOT/learn-hindi-from-nepal
      1 ROOT/learn-hindi-from-myanmar
      1 ROOT/learn-hindi-from-moldova
      1 ROOT/learn-hindi-from-maldives
      1 ROOT/learn-hindi-from-malaysia
      1 ROOT/learn-hindi-from-lebanon
      1 ROOT/learn-hindi-from-laos
      1 ROOT/learn-hindi-from-kyrgyzstan
      1 ROOT/learn-hindi-from-kuwait
      1 ROOT/learn-hindi-from-kosovo
      1 ROOT/learn-hindi-from-kazakhstan
      1 ROOT/learn-hindi-from-jordan
      1 ROOT/learn-hindi-from-israel
      1 ROOT/learn-hindi-from-iraq
      1 ROOT/learn-hindi-from-iran
      1 ROOT/learn-hindi-from-indonesia
      1 ROOT/learn-hindi-from-india
      1 ROOT/learn-hindi-from-haiti
      1 ROOT/learn-hindi-from-georgia
      1 ROOT/learn-hindi-from-ethiopia
      1 ROOT/learn-hindi-from-canada
      1 ROOT/learn-hindi-from-cambodia
      1 ROOT/learn-hindi-from-brunei
      1 ROOT/learn-hindi-from-bhutan
      1 ROOT/learn-hindi-from-bangladesh
      1 ROOT/learn-hindi-from-bahrain
      1 ROOT/learn-hindi-from-azerbaijan
      1 ROOT/learn-hindi-from-armenia
      1 ROOT/learn-hindi-from-afghanistan
      1 ROOT/learn
      1 ROOT/languages
      1 ROOT/index.html
      1 ROOT/how-levels-work
      1 ROOT/hindi-tutor
      1 ROOT/hindi
      1 ROOT/find-tutors.html
      1 ROOT/faq
      1 ROOT/daily-hindi
      1 ROOT/ask
      1 ROOT/answers
      1 ROOT/about
```

## E-3 · learn-hindi-from-* (indexable country pages)
```
learn-hindi-from-afghanistan/index.html
learn-hindi-from-armenia/index.html
learn-hindi-from-azerbaijan/index.html
learn-hindi-from-bahrain/index.html
learn-hindi-from-bangladesh/index.html
learn-hindi-from-bhutan/index.html
learn-hindi-from-brunei/index.html
learn-hindi-from-cambodia/index.html
learn-hindi-from-canada/index.html
learn-hindi-from-ethiopia/index.html
learn-hindi-from-georgia/index.html
learn-hindi-from-haiti/index.html
learn-hindi-from-india/index.html
learn-hindi-from-indonesia/index.html
learn-hindi-from-iran/index.html
learn-hindi-from-iraq/index.html
learn-hindi-from-israel/index.html
learn-hindi-from-jordan/index.html
learn-hindi-from-kazakhstan/index.html
learn-hindi-from-kosovo/index.html
learn-hindi-from-kuwait/index.html
learn-hindi-from-kyrgyzstan/index.html
learn-hindi-from-laos/index.html
learn-hindi-from-lebanon/index.html
learn-hindi-from-malaysia/index.html
learn-hindi-from-maldives/index.html
learn-hindi-from-moldova/index.html
learn-hindi-from-myanmar/index.html
learn-hindi-from-nepal/index.html
learn-hindi-from-new-zealand/index.html
learn-hindi-from-oman/index.html
learn-hindi-from-pakistan/index.html
learn-hindi-from-palestine/index.html
learn-hindi-from-peru/index.html
learn-hindi-from-philippines/index.html
learn-hindi-from-poland/index.html
learn-hindi-from-qatar/index.html
learn-hindi-from-romania/index.html
learn-hindi-from-saudi-arabia/index.html
learn-hindi-from-singapore/index.html
learn-hindi-from-south-africa/index.html
learn-hindi-from-sri-lanka/index.html
learn-hindi-from-syria/index.html
learn-hindi-from-tajikistan/index.html
learn-hindi-from-thailand/index.html
learn-hindi-from-timor-leste/index.html
learn-hindi-from-turkiye/index.html
learn-hindi-from-turkmenistan/index.html
learn-hindi-from-uae/index.html
learn-hindi-from-uk/index.html
learn-hindi-from-usa/index.html
learn-hindi-from-uzbekistan/index.html
learn-hindi-from-vietnam/index.html
learn-hindi-from-yemen/index.html
```

## E-4 · NO-ADS CLASSES (1826+ pages — kabhi ads nahi)
```
ADMIN                  stripped       1  e.g. admin.html
HIGH_CONTENT           kept-clean   455  e.g. about/index.html
INTERACTIVE_LEARNING   kept-clean   186  e.g. courses/by-country/index.html
MEDIUM_CONTENT         kept-clean   356  e.g. ar/find-tutors.html
RESEARCH_REQUIRED      kept-clean  1628  e.g. 404.html
TRANSACTIONAL          kept-clean     3  e.g. contact/index.html
UTILITY                kept-clean     8  e.g. cookie-policy/index.html
ok    ad policy: 2637 page(s) match the matrix (kept-clean 2636, stripped 1)
```

## E-5 · LINK-AUDIT SCRIPT (jo audit me chala tha — agent dobara chala sakta hai)
```
python3 - <<'PY'
# poore repo ka internal-link audit — repo root se chalao
import os, re
from urllib.parse import unquote
htmls=set(); other=set(); dirs=set()
for root,d,files in os.walk('.'):
    d[:] = [x for x in d if x not in ('.git','node_modules')]
    rr = os.path.relpath(root)
    if rr != '.': dirs.add(rr.lstrip('./'))
    for f in files:
        p = os.path.relpath(os.path.join(root,f))
        (htmls if f.endswith('.html') else other).add(p)
def resolves(l):
    l = l.split('#')[0].split('?')[0]
    if l in ('','.'): return True
    if l.endswith('/'): return (l+'index.html') in htmls or l in dirs
    return l in htmls or l in other or l in dirs
broken={}
for root,d,files in os.walk('.'):
    d[:] = [x for x in d if x not in ('.git','node_modules')]
    for f in files:
        if not f.endswith('.html'): continue
        rel = os.path.relpath(os.path.join(root,f)); base=os.path.dirname(rel)
        t = open(rel,encoding='utf-8',errors='ignore').read()
        for m in re.finditer(r'href=["\']([^"\']+)["\']', t):
            u=m.group(1)
            if u.startswith(('mailto:','tel:','http','javascript:','data:')): continue
            tgt = u.lstrip('/') if u.startswith('/') else os.path.normpath(os.path.join(base,u))
            tgt = unquote(tgt).replace('\\','/')
            if not resolves(tgt): broken.setdefault(tgt,set()).add(rel)
print('BROKEN targets:', len(broken))
for t,s in sorted(broken.items(), key=lambda x:-len(x[1]))[:20]:
    print(t, '<-', len(s), 'pages, e.g.', sorted(s)[0])
PY
```
════════════════════════════════════════════════════════════════════════════════
# PART F — FINAL 100-CHECK VERIFICATION BATTERY
════════════════════════════════════════════════════════════════════════════════
Ise agent se review-submit se PEHLE poora chalwao (Phase 4 ke end me). Har check
ke saath expected value diya hai. Format: [check-id] command → expected.
Agent se report maango: "PASS n" / "FAIL <list>". Ek bhi FAIL = submit mat karo.

── A. CODE PRESENCE (repo) ──
F-01 grep -rl "adsbygoogle.js" . --include="*.html" | wc -l → 811
F-02 grep -rl "google-adsense-account" . --include="*.html" | wc -l → 811
F-03 for f in $(grep -rl "ekguru:adsense:start" . --include="*.html"); do n=$(grep -c "ekguru:adsense:start" "$f"); [ "$n" -ne 1 ] && echo "$f"; done → (empty)
F-04 grep -rho "ca-pub-[0-9]*" . --include="*.html" | sort -u → sirf ca-pub-8175326569491671
F-05 python3 tools/inject-ads.py --check → ok, exit 0
F-06 node tools/test-ad-policy.mjs → 0 failed
F-07 python3 tools/build-all.py check → all ok
F-08 grep -n "ADS_RUNTIME_ENABLED = " js/monetization.js → false (approval tak)
F-09 grep -n "ADVERTISING_AVAILABLE = " js/cookie-consent.js → false (Phase 8 tak)
F-10 python3 -c "import json;d=json.load(open('data/monetization/google-monetization.json'));print(d['ad_policy']['loader_allowed'])" → ['HIGH_CONTENT','MEDIUM_CONTENT']

── B. EXCLUDED PAGES CLEAN (repo) ──
F-11 grep -c adsbygoogle contact/index.html → 0
F-12 grep -c adsbygoogle privacy/index.html → 0
F-13 grep -c adsbygoogle terms/index.html → 0
F-14 grep -c adsbygoogle disclaimer/index.html → 0
F-15 grep -c adsbygoogle cookie-policy/index.html → 0
F-16 grep -c adsbygoogle copyright/index.html → 0
F-17 grep -c adsbygoogle 404.html → 0
F-18 grep -c adsbygoogle admin.html → 0
F-19 grep -rc adsbygoogle courses/ | grep -v ":0" | wc -l → 0
F-20 grep -c adsbygoogle search/index.html → 0

── C. LIVE SITE ──
F-21 curl -s -o /dev/null -w "%{http_code}" https://ekguru.shop/ → 200
F-22 curl -s https://ekguru.shop/ | grep -c adsbygoogle → ≥1
F-23 curl -s https://ekguru.shop/ads.txt | grep pub-8175326569491671 → 1 line
F-24 curl -s https://ekguru.shop/hindi/ | grep -c adsbygoogle → ≥1
F-25 curl -s https://ekguru.shop/learn/ | grep -c adsbygoogle → ≥1
F-26 curl -s https://ekguru.shop/ask/ | grep -c adsbygoogle → ≥1
F-27 curl -s https://ekguru.shop/answers/ | grep -c adsbygoogle → ≥1
F-28 curl -s https://ekguru.shop/daily-hindi/ | grep -c adsbygoogle → ≥1
F-29 curl -s https://ekguru.shop/materials/ | grep -c adsbygoogle → ≥1
F-30 curl -s https://ekguru.shop/ar/ | grep -c adsbygoogle → ≥1
F-31 curl -s https://ekguru.shop/ja/ | grep -c adsbygoogle → ≥1
F-32 curl -s https://ekguru.shop/contact/ | grep -c adsbygoogle.js → 0
F-33 curl -s https://ekguru.shop/privacy/ | grep -c adsbygoogle.js → 0
F-34 curl -sI https://ekgurulearning.github.io/EkGuru/ | tail -1 → 200/301 chain ka final https://ekguru.shop/
F-35 curl -sI https://www.ekguru.shop/ → 301/200 (broken nahi)
F-36 curl -s -o /dev/null -w "%{http_code}" https://ekguru.shop/404-check-nahi-hai/ → 404
F-37 curl -s https://ekguru.shop/robots.txt | grep -c "Disallow: /admin" → 1
F-38 curl -s -o /dev/null -w "%{http_code}" https://ekguru.shop/sitemap-index.xml → 200
F-39 curl -s -o /dev/null -w "%{http_code}" https://ekguru.shop/images/icon-512.png → 200
F-40 curl -s "https://www.google.com/ping?sitemap=https://ekguru.shop/sitemap-index.xml" → non-empty

── D. SEO WIRING (repo) ──
F-41 canonical github.io count → 0
F-42 canonical non-ekguru host count → 0 (3 utility pages bina canonical — allowed)
F-43 sitemap URLs without disk file → 0
F-44 noindex pages in sitemap → 0
F-45 dup titles → 0
F-46 mixed http:// links → 0
F-47 hreflang pages count → 1698 (kam hua to investigate)
F-48 og:title missing count → ≤2
F-49 img alt audit pages count → 0
F-50 RSS feed valid head (<?xml) → yes

── E. CONTENT QUALITY ──
F-51 audit: duplicate_risk.affected_page_count → <200 (target <100)
F-52 audit: exact duplicate title groups → 0
F-53 audit: exact duplicate meta groups → 0
F-54 audit: thin INDEXABLE pages → 0
F-55 "coming soon" on indexable pages → 0 (sirf marketing-copy wala allowed)
F-56 "Lorem ipsum" anywhere → 0
F-57 random 5 changed pages ka opening ek-dusre se distinct (manual diff) → yes
F-58 random 3 pages quoted-search test (2 lines Google me) → koi exact match nahi

── F. LANGUAGE WIRING ──
F-59 ar/ me lang="ar" → yes
F-60 ja/ me lang="ja" → yes
F-61 de es fr pt me respective lang → yes
F-62 hindi/ sections lang="en" (English-medium — SAHI) → yes
F-63 ar/index.html content Arabic-only opening → yes
F-64 ja/index.html content Japanese-only opening → yes
F-65 (sample) kisi translated page me aadha-adhura English block → nahi

── G. STRUCTURED DATA ──
F-66 homepage JSON-LD parses → yes
F-67 hindi/ JSON-LD parses → yes
F-68 1 course page JSON-LD → yes
F-69 1 ask page JSON-LD → yes
F-70 daily-hindi/ JSON-LD (Course+ItemList) → yes
F-71 kisi bhi page pe LD-BROKEN nahi (sample 10) → 0 broken

── H. CI / REPO HEALTH ──
F-72 gh run list --limit 1 → success
F-73 git status → clean
F-74 git log -1 --format=%ci → recent (deploy hua tha)
F-75 changed-file count Phase-1 PR me ~815 ke aas-paas tha (abnormal nahi) → confirmed
F-76 CNAME file exist + ekguru.shop → yes
F-77 ads.txt tracked in git → yes
F-78 robots.txt me Allow: / → yes
F-79 .github/workflows/ci.yml present → yes
F-80 repo me koi credential/secret string nahi (rzp_live_/sk_live/secret=) → 0

── I. UX / POLICY GUARDS ──
F-81 google-anno-skip guards list js/monetization.js me intact → yes
F-82 courses page pe runtime pe bhi ad nahi (Phase 8 ke baad check) → yes
F-83 consent banner bina CSP error ke load → yes (console clean)
F-84 PWA manifest + SW valid → yes
F-85 mobile pe banner content overlay nahi karta (manual) → yes

── J. ACCOUNT-SIDE (owner, manual) ──
F-86 AdSense Sites me ekguru.shop added → yes
F-87 ads.txt status "Authorized" ya "Checking" (not "Not found" stuck) → yes
F-88 Payment profile address complete → yes
F-89 Identity verification done → yes
F-90 GSC property + sitemap submitted → yes

── K. FINAL REVIEW WEEK GUARDS ──
F-91..F-96 → PART C Phase 6 ke G-1..G-6 roz/2-din me
F-97 PageSpeed mobile ≥ 70 → yes
F-98 PageSpeed accessibility ≥ 90 → yes
F-99 weekly-guard.sh ALL GREEN → yes
F-100 AdSense Policy center me 0 alerts → yes

REPORT FORMAT (agent se):
  TOTAL: <n>/100 PASS
  FAIL list: F-xx, F-yy (reasons)
  "READY FOR REVIEW" ya "NOT READY — pehle FAIL fix"
════════════════════════════════════════════════════════════════════════════════

# PART G — GOLDEN RULES + ROLLBACK BIBLE + PASTE INDEX
════════════════════════════════════════════════════════════════════════════════

## G-1. GOLDEN RULES (kabhi na tootey)
1. AdSense script hamesha policy-JSON + tools/inject-ads.py se; HTML me haath se kabhi nahi.
2. ADS_RUNTIME_ENABLED / ADVERTISING_AVAILABLE approval se pehle true kabhi nahi.
3. Apni ads pe click kabhi nahi; kisi se karwana bhi nahi. Click-karo type CTA kabhi nahi.
4. Legal/transactional/interactive pages (privacy, terms, cookie-policy, contact,
   search, admin, courses, 404, tutor, join, booking, checkout, payment) pe ads
   kabhi nahi — policy engine ka kaam hai, bypass nahi.
5. Koi bhi deploy CI green ke bina merge nahi.
6. noindex pages ko indexable mat banao; indexable ko noindex mat karo (bina plan ke).
7. Domain (ekguru.shop) kabhi change nahi — ads.txt/canonical/GSC sab ispe bethe hain.
   Domain renewal auto-ON rakho (S-39).
8. Review week me koi bada deploy nahi.
9. Har phase apni branch me; rollback aasaan rahe.
10. Kuch bhi samajh na aaye → phase roko, mujhse (owner) poochho, guess nahi.

## G-2. ROLLBACK BIBLE
| Kya bigda | Rollback |
|---|---|
| Phase 1 ka loader sab pages se hatana | git revert -m 1 <merge-sha>; push; (ya loader_allowed → [] karke inject) |
| Phase 3 content batch kharab | git revert <batch-merge-sha> — batch-wise commits isliye |
| Phase 8 runtime pe ads har page pe | ADS_RUNTIME_ENABLED → false; push (2-min rollback) |
| Sitemap kharab | git checkout origin/main -- sitemap*.xml; rebuild tool se |
| inject-ads ne galat pages tag kiye | loader_allowed/classes JSON restore → python3 tools/inject-ads.py (idempotent) |
| Poora phase hi galat direction me | gh pr close + git branch -D <branch> — main untouched rahega (agar merge nahi hua) |

## G-3. PASTE INDEX (kya kabhi paste karna hai)
| Situation | Kya paste karna |
|---|---|
| Nayi agent chat shuru | PART C → PHASE 0 |
| Baseline mil gaya | PART C → PHASE 1 |
| Phase 1 merged | PART C → PHASE 2 |
| Live verified | PART C → PHASE 3 (+ PART D ke section blocks batch-order me) |
| Content done | PART C → PHASE 4 |
| Tech checks green | PART C → PHASE 5 (khud karo — manual) |
| Review chal raha | PART C → PHASE 6 (har 2-3 din) |
| REJECT aaya | rejection-reason ke hisaab se PART C → PHASE 7.x |
| APPROVED aaya | PART C → PHASE 8 |
| EEA traffic aaya | PART C → PHASE 9 |
| Har hafte | PART C → PHASE 10 (weekly-guard) |
| Kuch bigda | PART B me scenario number dhundo |
| Review se pehle | PART F 100-check run |

## G-4. TIME BUDGET (realistic)
Phase 0: 20 min · Phase 1: 1-2 ghante · Phase 2: 30 min · Phase 3: 2-5 din (batches)
Phase 4: 2-3 ghante · Phase 5: 20 min (manual) · Review wait: 2 din-2 hafte
Phase 8: 1 ghanta · Phase 10: hafte me 15 min
