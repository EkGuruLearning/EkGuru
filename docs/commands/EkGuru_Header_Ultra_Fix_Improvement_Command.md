# EkGuru — Header Fix + Advanced UX Improvement Command

PRODUCTION:
https://ekguru.shop/

TASK:
Fix the EkGuru header completely and improve it to a polished, production-grade responsive header.

IMPORTANT:
The current screenshot shows the desktop header becoming visually crowded around:
- logo/tagline
- COMING SOON/status pill
- tutor search
- Find Tutor
- How it works
- Book a trial
- language selector
- currency selector

Do NOT just hide the overflow.
Measure the real browser geometry and redesign the responsive behavior.

==================================================
1. REMOVE UNNECESSARY HEADER ITEMS
==================================================

The header MUST NOT contain:

- Learn
- Become a Tutor

on:
- desktop
- tablet
- mobile
- sticky header
- hamburger drawer
- responsive duplicate navigation

Do not delete the actual Learn or Become a Tutor pages/features.
They can remain reachable through footer/contextual links where useful.

==================================================
2. REMOVE / FIX "COMING SOON"
==================================================

The current screenshot shows a "COMING SOON" pill.

If EkGuru is now live, remove it from the public header.

Do not show:
- Coming Soon
- Under Construction
- Launch Soon

on a fully launched production site unless the statement is factually required.

If a badge is genuinely useful, replace it with a truthful non-blocking status/value badge.

Do not invent a status.

==================================================
3. DESKTOP HEADER ARCHITECTURE
==================================================

Build a deliberate desktop layout instead of one oversized flex row.

Preferred structure:

LEFT:
Logo + brand

CENTER:
Tutor search

RIGHT:
Find Tutors
How it works
Book a trial
Language
Currency

Use CSS Grid or carefully constrained flex sections.

Requirements:
- no overlap
- no clipping
- no negative positioning
- no hidden off-screen controls
- no horizontal page scroll
- no tiny unreadable text

The header must remain visually balanced.

==================================================
4. REAL BROWSER WIDTH MATRIX
==================================================

Test the LIVE/production build in Chromium at:

1024x768
1100x700
1200x800
1280x720
1366x768
1440x900
1536x864
1600x900
1680x900
1920x1080

Use actual getBoundingClientRect() values.

For every header element verify:
left >= 0
right <= viewportWidth
top >= 0
bottom <= header height
no overlap with adjacent controls
visible
clickable

Create an automated assertion for this.

==================================================
5. BREAKPOINT STRATEGY
==================================================

Do not force the desktop header into narrow widths.

Suggested behavior:

>= 1280:
full header

1100–1279:
reduce search width/spacing while keeping all important controls usable

900–1099:
simplified desktop/tablet header

< 900:
mobile/tablet menu

Do not blindly use these exact breakpoints if real measured content needs different values.

Choose breakpoints from actual component width.

==================================================
6. SEARCH BOX
==================================================

Make the tutor search field:

- visually distinct
- aligned vertically
- keyboard accessible
- clickable
- easy to type into
- never covering nav
- never pushing CTA off-screen

Desktop:
responsive max width

Tablet:
smaller width or move to second row if necessary

Mobile:
search should have a dedicated full-width or near-full-width area.

Never let the search input overlap:
- logo
- nav
- CTA
- language
- currency

==================================================
7. BOOK A TRIAL CTA
==================================================

Book a trial is a primary CTA.

It must:
- remain fully visible at supported widths
- have sufficient touch area
- have clear text
- never be clipped
- never overlap language/currency
- have strong keyboard focus
- work on mobile

At narrow widths, move it into the menu or a dedicated CTA row rather than clipping it.

==================================================
8. LANGUAGE SELECTOR
==================================================

Improve:
- clear label/current language
- keyboard access
- mobile usability
- dropdown positioning
- no off-screen menu
- no viewport clipping

Test at:
320
360
390
430
768
1024
1280
1920

If dropdown would overflow, reposition intelligently.

Do not allow:
positioned dropdown outside viewport
horizontal clipping
click-through overlay

==================================================
9. CURRENCY SELECTOR
==================================================

Same requirements:

- visible
- readable
- accessible
- dropdown stays inside viewport
- no overlap
- mobile-friendly

Currency display should remain compact.

==================================================
10. LOGO / BRAND
==================================================

Logo:
- never disappears
- never overlaps search
- tagline should not force overflow
- truncate tagline gracefully if required
- maintain readable brand name
- retain accessible alt/label

Do NOT allow the logo block to consume the entire mobile width.

==================================================
11. MOBILE HEADER
==================================================

Test:

320x568
360x800
375x812
390x844
412x915
430x932

Required mobile layout:

Top:
logo + hamburger

Optional:
search as second row

Menu:
Find Tutors
How it works
Book a trial
Language
Currency

DO NOT put:
Learn
Become a Tutor

Menu must:
- open
- close
- close on Escape
- close on outside click where appropriate
- lock background scroll safely
- restore scroll on close
- preserve focus
- not jump the header
- fit entirely within viewport

==================================================
12. MOBILE SEARCH
==================================================

Search must not be squeezed into the same row as:
logo + hamburger + all controls.

Prefer:
logo/hamburger row
+
search row

Search input:
min-height >= 44px
easy to tap
no zoom/layout issues
no overflow

==================================================
13. HEADER STICKY / SCROLL STATE
==================================================

Test:
- page top
- scroll down
- scroll up
- open mobile menu after scrolling
- close menu after scrolling

Ensure:
- sticky header doesn't jump
- header doesn't change width unexpectedly
- no content becomes hidden under header
- menu state remains coherent
- body scroll lock is restored

==================================================
14. VISUAL DESIGN IMPROVEMENTS
==================================================

Keep EkGuru's existing visual identity.

Improve:
- spacing consistency
- vertical alignment
- typography hierarchy
- control heights
- border radius consistency
- shadows
- hover states
- focus states
- active state
- icon alignment
- separator usage
- visual grouping

Do not over-design.

Header should look:
clean
modern
calm
professional
learning-focused

Avoid:
too many pills
too many borders
excessive gradients
tiny text
crowding

==================================================
15. ACCESSIBILITY
==================================================

Header must support:

keyboard navigation
visible focus
semantic nav
aria-expanded for menu
aria-controls where relevant
accessible names for icon buttons
Escape to close dropdown/menu
logical tab order

Minimum interactive target:
44x44px where practical.

Do not rely on hover only.

==================================================
16. Z-INDEX / LAYERING
==================================================

Audit:
header
sticky header
mobile drawer
dropdowns
modal
cookie/consent UI
ad UI

No dropdown should appear behind:
- header
- hero
- modal
- other controls

No header should cover important page content unexpectedly.

==================================================
17. TOUCH / MOUSE QA
==================================================

Test each:

Find Tutors
How it works
Book a trial
Language
Currency
Search
Hamburger
Logo/home

with:
mouse
trackpad
touch simulation
keyboard

No dead areas.

==================================================
18. RESPONSIVE RESIZE
==================================================

Continuously resize:

320
360
390
430
768
820
900
1024
1100
1200
1280
1366
1440
1536
1680
1920

Find:
- sudden layout jumps
- overlap
- clipping
- menu state bugs
- search resizing problems
- CTA disappearance

==================================================
19. HEADER PERFORMANCE
==================================================

Do not add unnecessary libraries.

Header should:
- load quickly
- avoid layout shift
- have stable dimensions
- not depend on heavy JS for basic navigation
- remain usable before secondary JS finishes

Use CSS for layout behavior where possible.

==================================================
20. SEO / CRAWLABILITY
==================================================

Header links should use real crawlable:
<a href="...">

Do not replace important navigation with:
- JS-only click handlers
- divs
- buttons that navigate without href

Important public pages must remain crawlable.

Do not create duplicate links solely for SEO.

==================================================
21. HEADER CONTENT RULE
==================================================

Current desired primary header navigation:

Find Tutors
How it works
Book a trial
Language
Currency

Plus:
Logo/brand
Search

NOT:
Learn
Become a Tutor
Coming Soon

==================================================
22. AUTOMATED HEADER REGRESSION TESTS
==================================================

Add tests that fail if:

- Learn appears in header
- Become a Tutor appears in header
- Coming Soon appears on launched production header
- any header element extends outside viewport
- header elements overlap
- search overlaps nav
- CTA is clipped
- language dropdown exceeds viewport
- currency dropdown exceeds viewport
- mobile hamburger is unreachable
- menu cannot open/close
- sticky header shifts
- horizontal overflow is introduced
- interactive header target is below acceptable size

Run in Chromium.

Do not rely on jsdom alone for geometry.

==================================================
23. FINAL VISUAL ACCEPTANCE
==================================================

Take screenshots at:

1280x720
1366x768
1440x900
1920x1080
390x844
430x932
768x1024

Compare:
- no crowding
- no overlap
- no clipping
- clean spacing
- clear CTA
- readable logo
- useful search
- consistent controls

==================================================
24. FINAL REPORT
==================================================

Return:

BEFORE:
- header issues found
- screenshots/evidence

AFTER:
- exact CSS/HTML/JS files changed
- breakpoint strategy
- header layout strategy
- navigation changes
- mobile menu changes

TESTS:
- desktop widths passed
- mobile widths passed
- touch passed
- keyboard passed
- sticky scroll passed
- dropdown passed
- regression tests passed

LIVE:
- production header verified at https://ekguru.shop/

Do not call the header fixed until real Chromium screenshots and geometry checks pass.

Do not modify unrelated site features.
