# EKGURU — ULTRA MODERN MOTION + MICRO-INTERACTION SYSTEM

PRODUCTION:
https://ekguru.shop/

GOAL:
Upgrade the entire EkGuru UI with polished, modern, consistent animation and micro-interactions — especially the 3-line mobile menu, header, tools, learning flows, modals, cards, forms, booking, admin, and feedback states.

IMPORTANT:
Animation must improve usability, hierarchy and perceived quality.
Do NOT add motion everywhere just for decoration.
Do NOT make the site slow.
Do NOT cause layout shift.
Do NOT break accessibility.
Do NOT trap focus or scroll.
Every animation must have:
- intentional purpose
- consistent timing
- graceful interruption
- reduced-motion alternative
- mobile-safe behavior

============================================================
1. CREATE ONE MOTION SYSTEM
============================================================

Do not hand-code unrelated animations across random files.

Create shared motion tokens:

--motion-fast
--motion-normal
--motion-slow

--ease-standard
--ease-emphasized
--ease-enter
--ease-exit

--radius-sm
--radius-md
--radius-lg

--shadow-rest
--shadow-hover
--shadow-focus

Use one shared motion utility/component layer.

Suggested timing ranges:
- micro interaction: 120–180ms
- normal transition: 180–280ms
- larger panel/modal: 280–420ms

Do not use long animations for routine interactions.

============================================================
2. REDUCED MOTION — NON-NEGOTIABLE
============================================================

Respect:

prefers-reduced-motion: reduce

When enabled:
- remove unnecessary movement
- reduce transform distances
- remove decorative loops
- keep opacity transitions short
- preserve functionality

Do not make accessibility depend on animation.

============================================================
3. MOBILE 3-LINE HAMBURGER — ULTRA ANIMATION
============================================================

The three-line menu button must animate smoothly between:

CLOSED:
☰

OPEN:
X

Behavior:
- top line rotates
- middle line fades/scales appropriately
- bottom line rotates
- transforms originate from center
- no jitter
- no size shift
- button remains exactly 44x44 or larger
- icon stays centered

Timing:
fast but smooth.

Requirements:
- tap opens menu
- tap closes menu
- Escape closes
- outside click closes where appropriate
- browser Back handles state correctly if menu state is URL/history-based
- focus moves appropriately
- background scroll locks safely
- closing restores scroll position
- header does not jump

============================================================
4. MOBILE DRAWER ANIMATION
============================================================

Use a polished drawer/panel transition.

Preferred behavior:
- backdrop fades in
- drawer slides/fades from intended edge
- slight opacity transition
- subtle elevation
- no overshoot that feels cartoonish
- no layout reflow behind drawer

Do NOT animate from far outside the screen with a large distance.

Drawer states:
CLOSED
OPENING
OPEN
CLOSING

Prevent:
double-open
double-close
race conditions
click-through
scroll leak

Animation must remain smooth on low-end mobile devices.

============================================================
5. BACKDROP
============================================================

Backdrop:
- fade in
- fade out
- optional subtle blur only if performance permits

Do not apply expensive backdrop-filter to huge areas on low-end devices unless tested.

Backdrop must:
- block unintended clicks
- preserve drawer focus
- disappear completely after closing

============================================================
6. HEADER ENTRANCE / SCROLL STATE
============================================================

Header should feel polished on load and scroll.

Use:
- subtle opacity/translate only when useful
- stable height
- no cumulative layout shift

On scroll:
- compact/sticky state may transition smoothly
- search can resize gently where appropriate
- do not hide critical navigation unexpectedly
- no sudden jump
- no content covered by header

Avoid dramatic sticky-header animations.

============================================================
7. HEADER HOVER / FOCUS MICRO-INTERACTIONS
============================================================

For:
Find Tutors
How it works
Book a trial
Language
Currency
Search
Logo

Use subtle:
- color/opacity change
- underline/indicator
- background highlight
- small elevation
- icon shift

Do not:
- move text significantly
- change layout width
- cause neighboring controls to shift

Keyboard focus must be visually stronger than hover.

============================================================
8. PRIMARY CTA — BOOK A TRIAL
============================================================

Use a premium but restrained interaction:

idle
→ hover
→ pressed
→ success

Hover:
small elevation / highlight

Pressed:
tiny scale-down

Do not create:
- continuous pulsing
- fake urgency
- aggressive glow

For successful action:
short confirmation animation.

============================================================
9. SEARCH BOX
============================================================

Add interaction states:

idle
focus
typing
loading
results
no-result
error

On focus:
- subtle border/focus ring
- optional background elevation

On search:
- spinner or progress indicator
- do not shift surrounding layout

Result appearance:
- stagger only a few items
- stop animation if content updates rapidly

Keyboard navigation:
- selected result highlight
- smooth but subtle

============================================================
10. DROPDOWNS
============================================================

For language/currency/dropdowns:

open:
fade + small vertical/scale entrance

close:
fast fade/slide

Requirements:
- anchor to trigger
- remain within viewport
- no clipping
- Escape closes
- keyboard navigation
- focus handling
- outside click where appropriate

No bouncing menus.

============================================================
11. CARDS
============================================================

For tutor/content/tool cards:

Hover:
- subtle shadow/elevation
- very small translate
- border/highlight

Pressed:
- tiny scale or visual response

Do NOT animate every card continuously.

On mobile:
prefer press/focus states instead of hover-only effects.

============================================================
12. TUTOR CARD ANIMATION
============================================================

Tutor cards should feel trustworthy, not like advertisements.

Use:
- image subtle scale on hover
- content stays stable
- CTA emphasis
- availability/status transition

Never animate price or important information excessively.

============================================================
13. TOOL CARDS / TOOLBOX
============================================================

Tool cards:
- icon reveal
- small lift
- progress/active state
- clean hover

Opening a tool:
- transition into tool page/panel where appropriate
- preserve context
- no heavy page animation

============================================================
14. LEARN PAGE
============================================================

Learning pages should have purposeful motion:

Lesson loading:
- skeleton shimmer only while genuinely waiting

Lesson start:
- subtle content entrance

Practice:
- correct answer:
  short positive feedback animation

Incorrect:
  clear correction state
  no shaming animation

Progress:
- smooth but short progress update

Completion:
- tasteful completion animation
- never block next action

============================================================
15. QUIZ
============================================================

Quiz transitions:
- question change
- answer state
- progress
- result

Use directional transition only if it helps orientation.

Do NOT animate the entire page unnecessarily.

Correct:
- subtle confirmation
- optional check icon draw

Incorrect:
- subtle shake only if reduced motion is disabled

Score:
- animate numeric change briefly

============================================================
16. FLASHCARDS
============================================================

If existing flashcards use flip:

- use accessible flip
- preserve keyboard functionality
- provide text alternative where needed
- reduce motion when preferred

Do not hide important information solely in animation.

============================================================
17. TOOL RESULTS
============================================================

When a tool generates output:

input
→ processing
→ output

Use:
- subtle loading
- output fade/slide
- copy confirmation
- error state

Do not animate huge result blocks in ways that move the page unexpectedly.

============================================================
18. COPY BUTTON
============================================================

States:

Copy
→ Copying if needed
→ Copied
→ idle

Animate icon/text subtly.

Do not rely only on color.

Provide accessible status text.

============================================================
19. FORMS
============================================================

Forms should have:

idle
focus
valid
invalid
submitting
success
error

Focus:
- clear focus ring

Validation:
- short highlight
- useful message
- no aggressive shake

Submitting:
- disable only what is necessary
- spinner
- prevent duplicate submission

Success:
- clear confirmation
- optional check animation

Failure:
- clear explanation
- retry

============================================================
20. CONTACT FORM
============================================================

Animate:

focus
validation
submission
success/partial-success/failure

Do NOT show a fake success animation before server confirmation.

If email delivery is degraded:
show honest status according to actual backend state.

============================================================
21. BOOKING FLOW
============================================================

Booking steps can use subtle progress transitions.

Example:

Tutor
→ Time
→ Requirement
→ Review
→ Submit
→ Result

Use:
- step indicator
- smooth content transition
- selected-state animation
- loading state
- success/failure state

Do not reset form state during transitions.

Do not animate away user-entered data.

============================================================
22. MODALS
============================================================

All modals:
- backdrop
- panel entrance
- focus trap
- Escape
- close button
- outside click where appropriate

Animation:
- opacity
- subtle scale/translate

Avoid:
large zooms
spins
dramatic bouncing

On mobile:
modal should remain usable with keyboard and viewport changes.

============================================================
23. TOASTS / NOTIFICATIONS
============================================================

Toasts:
- enter
- remain
- exit

Use short motion.

Do not rely on animation alone to communicate success/error.

Allow screen-reader announcement.

============================================================
24. SKELETONS
============================================================

Use skeleton loading only when a real wait exists.

Skeleton:
- stable dimensions
- no layout shift
- subtle shimmer
- reduced-motion alternative

Do not show fake skeletons after content is already available.

============================================================
25. PAGE TRANSITIONS
============================================================

If SPA-like navigation is used, use very subtle transitions.

Do not:
- delay navigation
- animate on every link for no reason
- harm browser Back/Forward
- interfere with deep links
- hurt SEO rendering

Content should remain immediately usable.

============================================================
26. SCROLL-REVEAL
============================================================

Use intersection-based reveal only for:
- non-critical decorative sections
- supporting content
- large visual sections

Do NOT hide critical text/navigation until animation runs.

No reveal animation should block indexing or accessibility.

============================================================
27. HERO ANIMATION
============================================================

Hero can use:
- very subtle entrance
- soft background movement
- one-time decorative animation

Do NOT use:
continuous distracting motion
parallax-heavy effects
large moving objects behind text

Keep text immediately visible.

============================================================
28. NUMBER / PROGRESS ANIMATION
============================================================

For:
progress
quiz score
stats
completion

Use short eased count transitions.

Never delay important information for animation.

============================================================
29. ICON MICRO-INTERACTIONS
============================================================

Where useful:
- chevron rotates
- check draws
- copy icon changes
- play button responds
- search icon responds
- bookmark toggles

Keep animations consistent across components.

============================================================
30. FOOTER
============================================================

Footer links can have:
- subtle hover/focus
- underline transition
- icon movement

Do not make the entire footer bounce or animate on entry unnecessarily.

============================================================
31. ADMIN DASHBOARD MOTION
============================================================

Admin UI should be more functional than decorative.

Use:
- table row state
- drawer transitions
- modal transitions
- filter panel
- toast
- loading/skeleton
- health status change

Health state transition:
UNKNOWN
→ CHECKING
→ GREEN/YELLOW/RED

Use clear status indicators, not flashy animations.

============================================================
32. HEALTH DASHBOARD
============================================================

Live health updates:
- subtle number/status transition
- timestamp update
- last-check pulse only when status changes

Do not use constant blinking.

Critical RED:
- clear visible status
- optional single attention animation
- no infinite flashing

============================================================
33. EMAIL/BOOKING ADMIN
============================================================

Delivery status animation:

QUEUED
→ SENDING
→ ACCEPTED
→ DELIVERED

Failure:
FAILED
→ RETRYING

Use status icon + text.

Do not animate fake delivery.

============================================================
34. ERROR PAGES
============================================================

404/500/network/offline states:

- friendly entrance
- clear next action
- subtle illustration
- retry button

Do not over-animate errors.

============================================================
35. OFFLINE / NETWORK STATE
============================================================

If network disconnects:
- subtle connectivity status
- retry
- preserve user input where safe

When connection returns:
- concise transition
- refresh only what is necessary

============================================================
36. PAGE-SPECIFIC MOTION
============================================================

Audit every page type:

Home
Learn
Toolbox
Tool
Topic
Guide
Question
Tutor listing
Tutor profile
Booking
Contact
About
Privacy
Terms
Disclaimer
Search
Daily Hindi
Course
Quiz
Flashcards
Admin
Health

For each:
inventory existing animation
remove broken/redundant motion
add consistent interactions
test performance

============================================================
37. ANIMATION PERFORMANCE
============================================================

Prefer compositor-friendly properties:
transform
opacity

Avoid unnecessary:
layout-triggering width/height/top/left animations

Do not animate:
huge DOM trees
large shadows continuously
expensive blur everywhere
entire page height changes repeatedly

Use CSS transitions/animations where possible.

Use JavaScript only when state/interaction requires it.

============================================================
38. NO LAYOUT SHIFT
============================================================

Animations must not cause:
- CLS
- content jumping
- buttons moving
- header resizing unexpectedly
- modal position changing
- tool result pushing unexpected content

Reserve dimensions for:
images
icons
media
skeletons
dynamic result areas

============================================================
39. LOW-END DEVICE TEST
============================================================

Test on throttled CPU/network where possible.

Check:
- menu opens quickly
- drawer is responsive
- scroll remains smooth
- tools remain interactive
- animation does not consume excessive CPU
- no long main-thread tasks caused by motion

If animation harms interaction:
reduce/remove it.

============================================================
40. ACCESSIBILITY TEST
============================================================

Test:
- keyboard
- screen reader labels
- focus
- reduced motion
- high zoom
- text resizing
- touch

When motion is reduced, all functionality must remain.

============================================================
41. TOUCH TEST
============================================================

Mobile:
320
360
390
430

Test:
- hamburger
- drawer links
- search
- dropdown
- cards
- tool buttons
- copy
- quiz answers
- booking
- modals

No accidental taps.

============================================================
42. BROWSER TEST MATRIX
============================================================

Use real Chromium/browser automation.

Desktop:
1024x768
1280x720
1366x768
1440x900
1536x864
1920x1080

Mobile:
320x568
360x800
390x844
430x932

Test:
page load
scroll
hover
focus
click
keyboard
resize
menu
modal
dropdown
form
tool
booking

Take screenshots of actual failures.

============================================================
43. AUTOMATED MOTION REGRESSION TESTS
============================================================

Create tests that detect:

- menu cannot open
- menu cannot close
- menu animation leaves overlay
- scroll remains locked
- focus lost
- modal inaccessible
- dropdown off-screen
- animation creates overflow
- layout shifts unexpectedly
- header jumps
- reduced-motion regression
- duplicate transition events
- stale animation state
- double-submit during transition

============================================================
44. MOTION DESIGN SYSTEM
============================================================

Centralize all shared:
- durations
- easings
- distance
- scales
- opacity
- shadows

Do not allow random:
250ms here
600ms there
1s elsewhere

unless there is a deliberate reason.

============================================================
45. VISUAL QUALITY
============================================================

The final motion language should feel:

modern
premium
light
fast
trustworthy
learning-focused
professional

Avoid:
- gaming-style excessive effects
- neon/glow overload
- giant bounces
- constant floating
- excessive parallax
- distracting auto-play animations

============================================================
46. FINAL ACCEPTANCE
============================================================

The work is complete only when:

HEADER:
- hamburger animation smooth
- drawer smooth
- no jump
- no overflow
- correct focus
- correct scroll lock

DESKTOP:
- no overlap
- no clipping
- polished hover/focus
- stable layout

MOBILE:
- no overflow
- smooth interactions
- touch-friendly
- reduced-motion works

LEARN:
- transitions improve orientation
- practice feedback clear
- progress smooth
- no content hidden

TOOLS:
- inputs/results smooth
- copy feedback
- loading
- errors
- no layout shift

BOOKING:
- step transitions
- validation
- success/failure
- no data loss
- no duplicate submit

ADMIN:
- health/status transitions
- drawers/modals
- table states
- no distracting motion

ACCESSIBILITY:
- reduced motion
- keyboard
- focus
- screen reader

PERFORMANCE:
- no meaningful regression
- no significant CLS
- no unnecessary CPU-heavy animation

============================================================
47. FINAL REPORT
============================================================

Return:

ANIMATION SYSTEM:
files/components created

HEADER:
before/after
screenshots
mobile
desktop

COMPONENTS UPGRADED:
count + list

PAGES TESTED:
count

REAL BROWSER TESTS:
passed
failed

ACCESSIBILITY:
passed
failed

PERFORMANCE:
before/after
CLS impact
CPU/main-thread impact where measured

REGRESSION:
existing features still working
full test result

LIVE:
https://ekguru.shop/
verified = YES/NO

REMAINING:
exact issues

============================================================
48. NON-NEGOTIABLE
============================================================

Do not add animation just because it looks impressive.

Animation must:
- communicate state
- guide attention
- preserve context
- improve perceived responsiveness
- remain accessible
- remain performant

The 3-line mobile menu is a priority, but the same motion system must be applied consistently across the entire EkGuru product.

END.
