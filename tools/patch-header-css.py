#!/usr/bin/env python3
"""Apply the measured header-layout fix to css/style.min.css.

Every replacement is exact-match; each must occur exactly once (or be
verified absent) so the patch is deterministic and auditable.
"""
import sys

PATH = "css/style.min.css"
css = open(PATH).read()

REPL = [
    # 1. Drop the random-margin hack on the "Book a trial" button; the nav
    #    gap now provides the spacing (spec: "Use CSS gap, not random margins").
    (".nav .btn{margin-left:6px}", ".nav .btn{}"),

    # 2. Tagline truncates gracefully with ellipsis instead of forcing width.
    (".logo small{display:block;font-size:0.8rem;font-weight:600;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;line-height:1}",
     ".logo small{display:block;max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:0.8rem;font-weight:600;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;line-height:1}"),

    # 3. Logo never shrinks; inner text column may shrink for the ellipsis.
    (".logo{display:flex;align-items:center;gap:10px;font-weight:900;font-size:1.3rem;letter-spacing:-.03em}",
     ".logo{display:flex;align-items:center;gap:10px;font-weight:900;font-size:1.3rem;letter-spacing:-.03em}.hdr .logo{flex:none}.hdr .logo>span{min-width:0}"),

    # 4. Consistent nav gap.
    (".nav{margin-left:auto;display:flex;align-items:center;gap:6px}",
     ".nav{margin-left:auto;display:flex;align-items:center;gap:10px}"),

    # 5. Never wrap (a wrapped row overflows the 70px header height).
    (".nav{min-width:0;flex-wrap:wrap;justify-content:flex-end;row-gap:6px;max-width:100%}",
     ".nav{min-width:0;flex-wrap:nowrap;justify-content:flex-end;row-gap:10px;max-width:100%}"),

    # 6. Items must not shrink (shrinking + white-space:nowrap paints text
    #    over neighbours — the root cause of the collision).
    (".nav>*{min-width:0}", ".nav>*{min-width:0;flex:0 0 auto}"),

    # 7-8. Search: no margin hack, fixed size (responsive bands below).
    (".hdr-search{position:relative;display:flex;align-items:center;margin-right:4px}",
     ".hdr-search{position:relative;display:flex;align-items:center;flex:0 0 auto}"),
    (".hdr-search input{width:190px;padding:9px 14px 9px 34px;border:1px solid var(--line);border-radius:999px;background:var(--bg-soft);font-size:0.88rem;color:var(--ink);font-family:inherit;transition:width .3s var(--ease),border-color .2s,box-shadow .2s,background .2s}",
     ".hdr-search input{width:220px;padding:9px 14px 9px 34px;border:1px solid var(--line);border-radius:999px;background:var(--bg-soft);font-size:0.88rem;color:var(--ink);font-family:inherit;transition:border-color .2s,box-shadow .2s,background .2s}"),

    # 9. Focus no longer widens the input (the old +60px expansion was a
    #    collision trigger). Focus restyles in place instead.
    (".hdr-search input:focus{outline:none;width:250px;background:#fff;border-color:var(--brand);box-shadow:0 0 0 3px rgba(91,61,245,.12)}",
     ".hdr-search input:focus{outline:none;background:#fff;border-color:var(--brand);box-shadow:0 0 0 3px rgba(91,61,245,.12)}"),

    # 10-11. Language control: drop margin, compact padding; keep globe, flag,
    #        "English", arrow and 40px touch height.
    (".lang-wrap{position:relative;margin-left:6px;flex:0 0 auto}",
     ".lang-wrap{position:relative;flex:0 0 auto}"),
    (".lang-btn{display:flex;align-items:center;gap:7px;padding:8px 13px;border-radius:999px;border:1px solid var(--line);background:#fff;cursor:pointer;font-weight:700;font-size:0.88rem;color:var(--ink-2);box-shadow:var(--sh-1);transition:border-color .2s,color .2s,transform .2s var(--ease);flex:0 0 auto;white-space:nowrap;min-height:40px}",
     ".lang-btn{display:flex;align-items:center;gap:6px;padding:7px 11px;border-radius:999px;border:1px solid var(--line);background:#fff;cursor:pointer;font-weight:700;font-size:0.85rem;color:var(--ink-2);box-shadow:var(--sh-1);transition:border-color .2s,color .2s,transform .2s var(--ease);flex:0 0 auto;white-space:nowrap;min-height:40px}"),

    # 12-13. Currency control: drop margin, compact padding; keep "₹ INR",
    #        coin icon, arrow and 40px touch height. Never shrink.
    (".cur-wrap{position:relative;margin-left:4px}",
     ".cur-wrap{position:relative;flex:0 0 auto}"),
    (".cur-btn{display:flex;align-items:center;gap:6px;padding:8px 12px;border-radius:999px;border:1px solid var(--line);background:#fff;cursor:pointer;font-weight:700;font-size:0.85rem;color:var(--ink-2);box-shadow:var(--sh-1);white-space:nowrap;transition:border-color .2s,color .2s,transform .2s var(--ease)}",
     ".cur-btn{display:flex;align-items:center;gap:6px;padding:7px 10px;border-radius:999px;border:1px solid var(--line);background:#fff;cursor:pointer;font-weight:700;font-size:0.85rem;color:var(--ink-2);box-shadow:var(--sh-1);white-space:nowrap;min-height:40px;flex:0 0 auto;transition:border-color .2s,color .2s,transform .2s var(--ease)}"),

    # 14. Stop hiding "How it works" (spec forbids hiding nav items).
    ('@media (max-width:1180px){.nav a[data-navlink="index.html"][data-hash]{display:none}}',
     ""),

    # 15. Drop the old squeeze block; keep only the unrelated .pf-layout rule.
    ("@media (min-width:981px) and (max-width:1180px){.hdr-in{gap:10px}.nav a{padding:8px 11px;font-size:0.9rem}.hdr-search input{width:150px}.hdr-search input:focus{width:210px}.pf-layout{grid-template-columns:1fr 300px;gap:26px}}",
     "@media (min-width:981px) and (max-width:1180px){.pf-layout{grid-template-columns:1fr 300px;gap:26px}}"),

    # 16. Responsive search-width bands (spec ranges: >=1440 -> 210-240;
    #     1280-1439 -> 175-205; 1100-1279 -> 145-180; below desktop threshold
    #     the search moves into the mobile panel).
    ("@media (max-width:1240px){.hdr-in{gap:10px}.nav{gap:2px}.nav a{padding:8px 9px;font-size:0.87rem}.hdr-search input{width:132px}.hdr-search input:focus{width:190px}.lang-btn{padding:7px 10px;font-size:0.83rem}.lang-btn .lbl{max-width:74px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}",
     "@media (min-width:1280px) and (max-width:1439px){.hdr-search input{width:190px}}@media (min-width:1081px) and (max-width:1279px){.hdr-search input{width:150px}}"),

    # 17. Tagline truncates (never fully hides) on narrower desktops.
    ("@media (max-width:1180px){.hdr .logo small{display:none}.hdr .logo{font-size:1.16rem}}",
     "@media (max-width:1180px){.hdr .logo{font-size:1.16rem}.hdr .logo small{max-width:120px}}"),

    # 18. Keep the language flag visible (it is part of the control identity).
    ("@media (max-width:1140px){.lang-btn .flag{display:none}}", ""),
]

fails = []
for old, new in REPL:
    n = css.count(old)
    if n == 0:
        fails.append(("MISSING", old[:60]))
        continue
    if n > 1:
        fails.append(("AMBIGUOUS x%d" % n, old[:60]))
        continue
    css = css.replace(old, new, 1)

if fails:
    print("PATCH ABORTED - no changes written:")
    for kind, s in fails:
        print("  ", kind, s)
    sys.exit(1)

open(PATH, "w").write(css)
print(f"OK: applied {len(REPL)} replacements to {PATH}")
print(f"final bytes: {len(css)}")
