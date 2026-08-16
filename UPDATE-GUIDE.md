# 🚀 EkGuru v20 — DEPLOY READY

Seven releases since v13. **8 more bugs found and fixed. 47 checks passing, 0 failures.**

---

# 🐛 WHAT WAS STILL BROKEN

I went hunting again rather than assuming v13 was clean. These are what turned up.

| # | Bug | Why it mattered | Fixed |
|---|---|---|---|
| 1 | **hreflang was one-way** | Language pages listed all 7 languages; the English pages listed none in their raw HTML. Google requires the mapping to point *both* ways — a one-way set is silently discarded, so all six translations were wasted | v14 |
| 2 | **Pre-rendered pages were language islands** | `/tutor/hemlata/` had no route to any translation. A Spanish visitor arriving from Google was stuck on an English page | v15 |
| 3 | **Language pages linked to `?id=`** | Every translated page sent crawl equity to the near-empty shell instead of the canonical page | v16 |
| 4 | **Fixes were not repeatable** | Regenerating any page silently undid the verification tag, hreflang and canonical links | v17 |
| 5 | **`llms.txt` and `feed.xml` undiscoverable** | Neither was announced in `robots.txt` or linked from any page | v18 |
| 6 | **287 KB of render-blocking JavaScript** | Twelve scripts in `<head>` with no `defer`, each one pausing the parser | v19 |
| 7 | **No static Open Graph tags** | Share the link on WhatsApp or LinkedIn and the preview was blank, because the tags only appeared after JavaScript ran | v20 |
| 8 | **No `theme-color`** | Mobile browsers showed a grey address bar instead of the brand purple | v20 |

---

# 📦 v14 — BIDIRECTIONAL HREFLANG

The most damaging of the eight.

`es/index.html` declared all seven languages. `index.html` declared none until JavaScript
ran — and Googlebot reads the raw HTML first. Google's rule is explicit: if page A claims
page B as its Spanish version, page B must claim page A back. Without the return link the
whole cluster is thrown away.

**Now:** 15 static hreflang links in the raw HTML of `index.html`, `find-tutors.html` and
`join.html` — both the locale form (`es-ES`) and the bare code (`es`), plus `x-default`.
Verified: `es/` points back to English, and English points to all six.

---

# 🌍 v15 — PRE-RENDERED PAGES ARE NO LONGER ISLANDS

Each `/tutor/<id>/` page now ends with a language strip:

> **Also available in:** 🇪🇸 Español · 🇫🇷 Français · 🇩🇪 Deutsch · 🇧🇷 Português · 🇯🇵 日本語 · 🇦🇪 العربية

Six real links per page, eighteen new internal routes into the translated section.

---

# 🔗 v16 — EVERY LINK POINTS AT THE CANONICAL PAGE

Twelve language pages were sending visitors and crawlers to `tutor.html?id=X`, which holds
48 words without JavaScript. All 36 of those links now go to `/tutor/<id>/`, the version
with 500–800 words and its own schema.

---

# 🔧 v17 — THE FIXES ARE NOW PERMANENT

Every correction above lived in generated files. Running `node build/langpages.js` would
have quietly wiped them.

**New: `build/patch.js`** re-applies all of them after any rebuild:

1. Google verification meta on every page
2. Static hreflang on the English shell pages
3. Canonical tutor links
4. Language strips on pre-rendered pages
5. `theme-color`

It is **idempotent** — verified by running it twice, second run reports zero changes.

**Rebuild order:**
```bash
node build/sitemap.js
node build/feeds.js
node build/manifest.js
node build/patch.js      # ← always last
```

---

# 🤖 v18 — ROBOTS AND AI DISCOVERY

`robots.txt` rewritten with **18 named crawlers**: GPTBot, OAI-SearchBot, ChatGPT-User,
PerplexityBot, ClaudeBot, Claude-Web, anthropic-ai, Google-Extended, Applebot,
Applebot-Extended, Amazonbot, FacebookBot, Bytespider, CCBot, cohere-ai, YouBot,
DuckAssistBot — all explicitly allowed.

Language directories are called out individually, the sitemap is declared, and `llms.txt`
now has a discovery `<link>` in every page head.

---

# ⚡ v19 — RENDER-BLOCKING SCRIPTS

Twelve scripts, 287 KB, all blocking the parser in `<head>`.

All twelve now carry `defer`. This is the right tool rather than `async`: `defer`
preserves execution order — which matters, because `site-config` must run before
`tutors-data`, which must run before `seo.js` — while letting the parser continue.

Verified after the change: tutors load, SEO runs (1,622 phrases), cards render, zero
errors on all four page types.

---

# 📱 v20 — STATIC SOCIAL TAGS

Sharing a link on WhatsApp, LinkedIn or Slack produced a blank preview, because those
scrapers never run JavaScript.

Every shell page now carries, in raw HTML:

```
og:type, og:site_name, og:title, og:description, og:url,
og:image (1200×630), og:image:width, og:image:height, og:image:alt,
og:locale, twitter:card, twitter:title, twitter:description,
twitter:image, theme-color, apple-mobile-web-app-title, application-name
```

`seo.js` still refines them at runtime for the per-tutor and per-language cases.

---

# ✅ FINAL STATE

| | |
|---|---|
| Files | 82 |
| Size | 2.1 MB |
| Sitemap | 25 URLs, 92 image entries |
| Verification | 28 pages + HTML file method |
| Languages | 7, with 18 real translated files |
| Pre-rendered profiles | 3, 485–813 words each |
| Schema types | 12, 21 JSON-LD blocks, all valid |
| Keyword space | 11,65,684 crore |
| Keywords published per page | 1,622 across 26 channels |
| Currencies | 51, auto-detected |
| Crawlers welcomed | 18 |

## Test results

| Suite | Checks | Result |
|---|---|---|
| v14 bidirectional hreflang | 4 | ✅ |
| v15 language strips | 3 | ✅ |
| v16 canonical links | 6 | ✅ |
| v18 robots + discovery | 4 | ✅ |
| v19 defer, nothing broken | 4 | ✅ |
| v20 static social tags | 4 | ✅ |
| Full regression | 22 | ✅ |
| **Total** | **47** | **✅ 0 failures** |

Plus: all JS syntax valid · 21/21 JSON-LD blocks parse · sitemap, feed and manifest valid ·
29/29 live resources return 200 · `patch.js` idempotent.

---

# 🚀 DEPLOY

**Upload the entire `EkGuru` folder contents — 82 files.**

1. Repo `ekgurulearning/EkGuru`, **Public**
2. Upload everything **inside** the folder, not the folder itself
3. Confirm `.nojekyll` exists — if drag-and-drop skipped it,
   **Add file → Create new file → `.nojekyll` → empty → Commit**
4. **Settings → Pages → Deploy from a branch → `main` / `/ (root)` → Save**
5. Wait 2 minutes → **https://ekgurulearning.github.io/EkGuru/**

## Immediately after

1. **Search Console → Verify.** Both methods are in place — the meta tag on 28 pages and
   `googleb3b0e3defc1daa17.html` at the root. Either will pass.
2. **Submit `sitemap.xml`.**
3. **Request indexing** for: home, `find-tutors.html`, and each `/tutor/<id>/`.
4. **Bing Webmaster Tools** → import from Search Console, one click.
5. **Add your site link to your Preply profile.** Five minutes, and worth more than every
   other item on this list.

## Post-deploy checks

- [ ] Home loads, logo in header, 3 tutor cards
- [ ] Card click → `/tutor/<id>/` with the full profile
- [ ] 🪙 currency dropdown in the header
- [ ] `/es/` and `/ar/` load, Arabic right-to-left
- [ ] Share the link on WhatsApp — the OG image preview appears
- [ ] Phone: reviews swipe, sticky booking bar appears
- [ ] `sitemap.xml`, `llms.txt`, `feed.xml` all load

---

# 📁 VERSION HISTORY

| Version | Added |
|---|---|
| v1–v6 | Tutors, booking, search, responsive, country pricing, pre-rendering |
| v7–v10 | 11 bugs, header currency, 26 meta channels, language pages, 11 lakh crore keywords |
| v11–v13 | Logo, WebP, image sitemap, canonical conflict, Google verification, LinkedIn |
| **v14** | **Bidirectional hreflang in raw HTML** |
| **v15** | **Language strips on pre-rendered pages** |
| **v16** | **All links to canonical tutor pages** |
| **v17** | **`build/patch.js` — fixes survive rebuilds** |
| **v18** | **18 crawlers, llms.txt discovery** |
| **v19** | **All scripts deferred** |
| **v20** | **Static Open Graph, theme-color — DEPLOY READY** |

---

**Built by Prakash — MNIT Jaipur, CSE 2022–2026 batch pass out.**
[linkedin.com/in/itstheprakash](https://www.linkedin.com/in/itstheprakash/)

© EkGuru — One Student. One Guru. One Goal.
