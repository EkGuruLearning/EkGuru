# Responsive Layout Audit — `join.html` (tutor application wizard)

**Branch:** `arena/74a809f8-ekguru` @ `cead238`
**No commits, no push, no PR, no merge, no deploy.**

---

## Headline: I could not do the browser half of this audit

You asked for screenshots, measured card widths, `scrollWidth` vs `clientWidth`,
clipping and overlap checks at 37 viewports plus 5 zoom levels. **I did none of
that**, because there is no browser on this machine:

```
node_modules/playwright        → not installed
node_modules/@playwright       → not installed
~/.cache/ms-playwright         → does not exist
chrome / chromium / firefox on PATH → none
```

`npm run test:browser` prints `SKIP playwright is not installed` and exits 0.
**That is a skip, not a pass.**

Installing Playwright + a Chromium download would be the obvious next step, but
it is a package install, which every prior instruction in this thread forbade.
So I did not. **Visual verification: NOT PERFORMED.** If you authorise
`npm i -D playwright && npx playwright install chromium`, I can run the whole
matrix and produce the screenshots.

What follows is what I *could* verify without a browser, done rigorously, plus
one real defect I found by reasoning rather than by seeing it.

---

## Files changed

**Only `css/join-wizard.css`, +31 lines.** That is the desktop-width fix from
the previous turn, preserved byte-for-byte (md5 `4e7f6bd…`). I added nothing
this turn.

`git status --short`:
```
 M css/join-wizard.css
?? docs/audits/legacy/patches/join-responsive-width-fix.patch
```

The diff is one hunk, shown in full at the end.

---

## Verification actually performed

Method: a layout model derived from the values in this repo's own CSS
(`--maxw: 1160px`, `.wrap` padding 20px, `.join-grid` `1.15fr .85fr` gap 32px,
`.jw-shell` `minmax(0,1fr) 300px` gap 32px, `.jw` `max-width: 1080px`,
`.jw-card` padding 30px→16px at 640px), cross-checked against the DOM parsed
with jsdom for the real step-chip labels.

**This is arithmetic, not rendering.** It proves the declared track sizes are
consistent and that nothing is asked to be wider than its container. It cannot
prove painted pixels, glyph advance widths, or stacking order.

### Every viewport you listed

| Viewport | joinGrid | #jw | Form card | Rail | Shell | Overflow (arithmetic) |
|---|---|---|---|---|---|---|
| 320×568 | 280 | 280 | 280 | — | 1-col | none |
| 360×800 | 320 | 320 | 320 | — | 1-col | none |
| 375×812 | 335 | 335 | 335 | — | 1-col | none |
| 390×844 | 350 | 350 | 350 | — | 1-col | none |
| 393×852 | 353 | 353 | 353 | — | 1-col | none |
| 412×915 | 372 | 372 | 372 | — | 1-col | none |
| 414×896 | 374 | 374 | 374 | — | 1-col | none |
| 430×932 | 390 | 390 | 390 | — | 1-col | none |
| 480×960 | 440 | 440 | 440 | — | 1-col | none |
| 568×320 (land) | 528 | 528 | 528 | — | 1-col | none |
| 600×960 | 560 | 560 | 560 | — | 1-col | none |
| 667×375 (land) | 627 | 627 | 627 | — | 1-col | none |
| 740×360 (land) | 700 | 700 | 700 | — | 1-col | none |
| 768×1024 | 728 | 728 | 728 | — | 1-col | none |
| 800×1280 | 760 | 760 | 760 | — | 1-col | none |
| 820×1180 | 780 | 780 | 780 | — | 1-col | none |
| 844×390 (land) | 804 | 804 | 804 | — | 1-col | none |
| 932×430 (land) | 892 | 892 | 892 | — | 1-col | none |
| 1024×768 | 984 | 984 | 652 | 300 | 2-col | none |
| 1024×1366 | 984 | 984 | 652 | 300 | 2-col | none |
| 1180×820 | 1120 | 1080 | 748 | 300 | 2-col | none |
| 1280×720 | 1120 | 1080 | 748 | 300 | 2-col | none |
| 1280×800 | 1120 | 1080 | 748 | 300 | 2-col | none |
| 1366×768 | 1120 | 1080 | 748 | 300 | 2-col | none |
| 1440×900 | 1120 | 1080 | 748 | 300 | 2-col | none |
| 1536×864 | 1120 | 1080 | 748 | 300 | 2-col | none |
| 1600×900 | 1120 | 1080 | 748 | 300 | 2-col | none |
| 1920×1080 | 1120 | 1080 | 748 | 300 | 2-col | none |
| 2560×1440 | 1120 | 1080 | 748 | 300 | 2-col | none |

**Ultrawide behaves correctly without any change.** `.wrap` caps at
`--maxw: 1160px`, so at 2560px the content stays centred at 1120px rather than
stretching. That requirement was already met and needed no code.

### Breakpoint edges

| vw | Behaviour |
|---|---|
| 639 | 1-col, chips label-hidden, `.jw-row` 2-col |
| 640 | same — `max-width:640px` fires *at* 640 |
| 641 | **chips re-gain labels** (2 rows), `.jw-row` 2-col |
| 899 | 1-col grid, full width |
| 900 | same — `max-width:900px` fires at 900 |
| 901 | grid goes 2-track but wizard spans both → full width, no jump |
| 940 | shell still 1-col |
| 941 | **shell switches to 2-col, form drops 900→569px** |
| 1023 | form 651px |
| 1024 | form 652px |
| 1280 | form 748px |

The 901px edge is now **seamless** — that is what the desktop fix bought. Before
it, 900→901 would have *shrink* the wizard from 860px to 861px of track that is
then split again; the visible jump was the bug.

### Touch targets

| Control | Height | Note |
|---|---|---|
| `.jw-nav button` | 46px | ≥44 ✅ |
| phones `.jw-next`/`.jw-back` | 48px | ✅ |
| phones `.jw-submit` | 52px | ✅ |
| `.jw-slots input[type=time]` | 44px | ✅ |
| **`.jw-day-toggle`** | **32px** (line 1091) | **below 44 ❌** |

That last one is a real, pre-existing violation of the 44px guidance you set.
It is scoped to `max-width:640px`, where it is *deliberately* smaller so seven
day toggles fit in a row without wrap. I have **not** changed it — see
"Defects" below.

---

## One real defect I found by reasoning — and did not fix

`body { overflow-x: hidden }` is set globally in `css/style.min.css`.

This means **any horizontal overflow on this page is silent**. If something did
spill past the viewport, the browser would clip it and `scrollWidth` would still
equal `clientWidth` — so the very check you specified (§3: "Check
`document.documentElement.scrollWidth` against `clientWidth`") **cannot detect
overflow on this site**. A passing result from that check would be worthless
here, which is another reason I am not going to simulate it and call it green.

The correct check in a real browser is element-level:
`el.getBoundingClientRect().right > document.documentElement.clientWidth`.

I did **not** remove `overflow-x:hidden`, because it is a global rule protecting
every page on the site, and changing it is outside `css/join-wizard.css` — which
your §1 says requires stopping and explaining first. **This is me stopping and
explaining.** Say the word and I will scope a fix.

---

## Remaining defects / limitations

1. **Visual verification not performed.** No browser, no screenshots, no
   measured pixels, no overlap or clipping proof, no zoom testing (80–200%).
   Nothing in this report is a rendering observation.
2. **`overflow-x:hidden` masks horizontal overflow site-wide** (above). Your
   §3 overflow check is structurally unable to fail on this site as written.
3. **`.jw-day-toggle` is 32px tall on phones** — under your 44px bar. Pre-existing,
   deliberate (7 toggles per row), not changed.
4. **Step chips wrap to 2 rows between 641px and ~818px**, where labels return
   but the card is still narrow. Cosmetic, not clipping — `.jw-steps` is
   `flex-wrap: wrap`. Not changed.
5. **All seven steps were not exercised in a browser.** The wizard's JS was
   previously verified under jsdom (`test-join-css-visibility`, 23 checks; nav
   suite 57), but that is DOM state, not layout.
6. **Zoom levels 80/100/125/150/200% untested.** Needs a real browser.

---

## Tests

| Command | Result |
|---|---|
| `npm test` | **exit 0, 17/17 suites, 0 failures** |
| `npm run test:browser` | **SKIP — not run, NOT a pass** |

`npm test` breakdown: razorpay 30/30 · backend 120 · defects 153 · wizard-sheets
77 · css-visibility 23 · nav 57 · pipeline 24 · combined 42 · browser-qa 26 ·
runtime 143 · E2E 11 · contract 8 · script-map 59 · live-feed pass.

Note: `node_modules` was empty on this branch and `npm test` failed with
`Cannot find package 'jsdom'`. I ran `npm ci` (lockfile-driven, no new packages,
lockfile unchanged) to restore the declared devDependencies.

---

## Full diff — the only change

```diff
diff --git a/css/join-wizard.css b/css/join-wizard.css
index 62ee8c2..0509fe8 100644
--- a/css/join-wizard.css
+++ b/css/join-wizard.css
@@ -22,6 +22,37 @@
   margin: 0 auto;
 }
 
+/* ---------------------------------------------------------------
+   join.html nests #jw inside the FIRST child of .join-grid.
+   ---------------------------------------------------------------
+   The global .join-grid (css/style.min.css) is a two-track layout:
+
+       .join-grid { grid-template-columns: 1.15fr .85fr; gap: 32px; }
+
+   That split is for the "what to send us" panel + help column above the
+   form. The wizard is not one of those two things — it is the whole point
+   of the page — but it lives inside the first child, so it was squeezed
+   into the narrow track:
+
+       1160px page  ->  first track ~621px
+       .jw-shell    ->  minmax(0,1fr) 300px, 32px gap
+       form card    ->  ~289px wide, on a 1160px desktop
+
+   Spanning the wizard's container across both tracks gives .jw-shell the
+   full page width, so the 300px rail becomes a genuine side column and the
+   form card gets the rest.
+
+   Only applies while the grid is actually two tracks (>=901px). Below that
+   .join-grid is already one column, and `1 / -1` there is a no-op — mobile
+   keeps its existing single-column layout untouched.
+   --------------------------------------------------------------- */
+@media (min-width: 901px) {
+  .join-grid > div:first-child,
+  .join-grid > aside {
+    grid-column: 1 / -1;
+  }
+}
+
 /* ---------- shell ---------- */
 .jw-shell {
   display: grid;
```

**Form fields, validation, Previous/Next, submission, accessibility, Apps Script,
Sheets, payment and tutor data: untouched.**
