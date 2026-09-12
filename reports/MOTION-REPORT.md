# EkGuru — Motion & Micro-Interaction System Report

Command: `EkGuru_ULTRA_Modern_Animation_Motion_System_Command.md` (48 sections)
Date: 2026-09-11 · Basis: current workspace code, real-browser verification (Chromium via Playwright)
Live check: `https://ekguru.shop/` still serves the previous build — deployment is blocked (no git remote/credentials in this environment), see "Remaining".

---

## 1. ANIMATION SYSTEM — files/components

The site already had a centralized token system; this turn completed the gaps.

| Layer | Where | State |
|---|---|---|
| Motion tokens `--motion-fast/normal/slow` (130/220/360ms), `--ease-*`, `--radius-*`, `--shadow-*` | `css/style.min.css` | Present before; reused by all new motion |
| Reduced-motion kill-switch (`prefers-reduced-motion: reduce`) | `css/style.min.css` (multiple blocks) | Present before; verified |
| Shared toast/skeleton primitive `EkGuruToast` | `js/toast.js` | Present before (complete, role=status/alert, click-to-dismiss, reduced-motion path) |
| Shared reveal/stagger + countUp | `js/main.js` | Present before (IntersectionObserver, no-JS fallback) |
| **New: consolidated motion-upgrade block** | `css/style.min.css` (appended) | §9/§12/§13/§14/§15/§16/§28/§30 |
| **New: quiz feedback micro-edits** | `toolbox/hindi-quiz/index.html` | `.q-bad` shake class + `#qtext.q-in` retrigger |
| **New: offline/network banner** | `js/site-config.js` (appended §35) | universal fixed banner, lazy-created |

Design rules honored throughout: transform/opacity only (compositor-friendly), no width/height/top/left animation, no layout shift (dimensions reserved, fixed-position banner), no fake states.

## 2. HEADER — before / after

- Hamburger (3-line) morphs to ✕: top/bottom lines rotate ±45° from center, middle line fades to transparent. Button stays 44×44, no size shift. *(Present before; verified in browser.)*
- Drawer: slides down from the header edge (`translateY(-135%) → 0`, `--ease` 340ms), backdrop fades in/out, scroll locks and restores exactly, focus moves in and Tab is trapped, Escape/outside-click/backdrop close, resize past breakpoint unlocks. *(Present before; verified.)*
- Header hover/focus micro-interactions: nav pill background + color, language/currency menu fade+slide, stronger keyboard focus ring (`:focus-visible`). *(Present before.)*

No header jumps, no overflow, no CLS — verified at 390px and 1440px.

## 3. COMPONENTS UPGRADED (this turn)

1. Tutor card photo — gentle `scale(1.05)` on hover, content stable (§12)
2. Toolbox tool links (chips) — 2px lift + shadow on hover (§13)
3. Search results (`.ac-item`) — staggered entrance, first 5 delayed 0–120ms, rest 150ms (§9)
4. Quiz feedback — correct/incorrect pop-in (`fbPop`), wrong-answer shake only when motion allowed (`shakeX`), question text fade (`qIn`), progress bar width transition (§15)
5. Flashcards — back/romanisation reveal on each flip (`faceIn`) (§16)
6. Level test — newly revealed question slides in (`qIn`) (§14)
7. Footer links — underline grows on hover/focus (§30)
8. Hero chips — bob amplitude reduced 12px→6px (remove "constant floating") (§45)
9. Offline/network banner — fixed, token-driven, Retry button, screen-reader announced (§35)

Not added (deliberately, per the command's own "do not add motion everywhere"): no fake search spinner (search is synchronous in-memory), no fake toasts (inline statuses already exist), no continuous card animation, no dramatic modals.

## 4. PAGES TESTED (real Chromium)

`index.html` (mobile 390×844 + desktop 1440×900), `tutor.html?id=sushila-g` (booking modal), `toolbox/index.html`, `toolbox/hindi-quiz/`, `toolbox/hindi-flashcards/`, `toolbox/hindi-level-test/`, `admin.html` (click-through), plus the two timezone regression tests on `tutor.html`.

## 5. REAL BROWSER TESTS

`motion-test.py` (Playwright, Chromium): **31/31 PASS**, including:
- burger ≥44×44, morphs to ✕, aria-expanded toggles
- drawer translate off/on, backdrop visible, scroll locked, Escape + backdrop + outside close, focus/aria attributes
- reduced-motion emulation: hero `::before` animation = none
- tutor photo scale on hover; tool chip lift
- quiz feedback pop present; wrong-answer shake class; progress-bar transition; question fade class
- flashcards back reveal + `faceIn`; level-test `qIn`
- booking modal opens (opacity 1, transform settled)
- no horizontal overflow; **zero page/console errors** on every page

Offline banner test: appears on real `offline` event (role=status, "Retry" button), hides on `online`.

Regression: timezone tests `tz-test.py` + `tz-test2.py` both PASS (select renders 32 zones, IST slot labels intact). Admin click-through PASS (incidents, clear-sent, bookings table with honest `tutor email unavailable · fallback: EkGuru inbox`, tabs, zero errors).

## 6. ACCESSIBILITY

- Reduced motion: global kill-switch removes animation/transition; all functionality preserved (verified).
- Keyboard: focus trap in drawer, Escape closes, `:focus-visible` ring stronger than hover.
- Screen reader: burger has `aria-controls`/`aria-expanded`; backdrop `aria-hidden` toggles; offline banner `role=status` + `aria-live=polite`; toast primitive `role=status/alert`.
- No information hidden in animation (flashcards show text immediately; quiz states are text).

## 7. PERFORMANCE

- All new motion is transform/opacity (compositor-only).
- No layout-triggering property animated; banner is `position:fixed`; dimensions reserved.
- No CLS measured: no horizontal overflow, header height stable, no content jump in tests.
- Search stagger is capped and self-limiting (nodes replaced per keystroke).

## 8. REGRESSION

Existing features re-verified: timezone selector (32 zones), booking modal + schedule render, admin dashboard, contact/booking email pipeline statuses unchanged (mailer.js untouched this turn). `node --check` PASS for `js/site-config.js`, `js/features.js`, `js/schedule.js`, and the quiz inline script.

## 9. LIVE

`https://ekguru.shop/` = **NO** (still previous build). This environment has no git remote URL in `.git/config` and no GitHub credentials (no `gh`, no token env, no `~/.netrc`/`~/.git-credentials`/SSH keys), so an authenticated push to `github.com/ekgurulearning/EkGuru` is not possible from here. All changes are committed locally (see FINAL-REPORT / git log for the exact hash).

## 10. REMAINING

- **Deployment**: push + GitHub Pages publish of the local `main` branch (needs credentialed machine). Until then the live site lags.
- R012 (dedicated mobile search screen) and R016-adjacent exhaustive z-index matrix remain documented as partial in `master-requirements.json`; R016 layering itself was re-verified and marked PASS this turn.
- External blockers unrelated to motion (Apps Script shared token, Web3Forms residential verification, per-tutor verified addresses) remain as already logged in the email reports.
