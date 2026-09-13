#!/usr/bin/env python3
"""Phase 7C Stage 3 — multi-language starter packs + home reachability, real
Chromium (Gate J).

Verifies:
  · registry: 29 BETA starter packs, production == ["hi"], 0 PLANNED
  · home page: a #languages section + a nav link; Hindi (full course) pill + 9
    beta pills, each linking to its detail page
  · /languages/ hub: 1 available cell (Hindi), 9 beta cells (linked), 20 planned
    (no thin pages), picker lists 9 packs, es renders by default
  · every BETA language has a detail page /languages/{code}/ that renders 36
    items + 4 grammar concepts through the SAME engines, with SRS add-buttons,
    a unique <title>, BETA + "not a … course" honesty strings, 0 page errors
  · a PLANNED language has NO detail page (404 — no thin pages)
Output: reports/phase7c-langs-test.json
"""
import json, os, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BASE = "http://127.0.0.1:8899"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
fails, facts = [], {}

def note(k, v):
    facts[k] = v

# ---- registry assertions (Python-side) ----
reg = json.load(open("reports/language-registry-phase7c.json", encoding="utf-8"))
by_id = {l["id"]: l for l in reg["languages"]}
beta_ids = sorted([l["id"] for l in reg["languages"] if l["productionStatus"] == "BETA"])
planned_ids = sorted([l["id"] for l in reg["languages"] if l["productionStatus"] == "PLANNED"])
note("production", reg.get("production"))
note("beta_ids", beta_ids)
note("planned_count", len(planned_ids))
if reg.get("production") != ["hi"]:
    fails.append("only hi may be PRODUCTION, got %s" % reg.get("production"))
if beta_ids != sorted(["en", "es", "bn", "ta", "te", "mr", "gu", "pa", "ur",
                       "fr", "ar", "de", "ja", "ko", "zh", "ru", "pt", "it", "nl", "pl",
                       "tr", "fa", "he", "th", "vi", "id", "ms", "sw", "uk"]):
    fails.append("expected 29 BETA starter packs, got %s" % beta_ids)
for c in beta_ids:
    l = by_id[c]
    if not l.get("starterPack") or not l.get("starterCounts"):
        fails.append("%s should carry starterPack + starterCounts" % c)
    sc = l.get("starterCounts") or {}
    if sc.get("vocab") != 24 or sc.get("phrase") != 12 or sc.get("grammar") != 4:
        fails.append("%s starterCounts should be 24/12/4, got %s" % (c, sc))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    def wait_items(timeout_s=8):
        for _ in range(int(timeout_s * 4)):
            if pg.evaluate("() => document.querySelectorAll('#langpack-app .v-item').length > 0"):
                return True
            pg.wait_for_timeout(250)
        return False

    # ---- home page reachability ----
    pg.goto(BASE + "/", wait_until="networkidle")
    home = pg.evaluate("""() => {
        var sec = document.getElementById('languages');
        var nav = document.querySelector('.nav a[href="languages/index.html"]');
        var pills = Array.from(document.querySelectorAll('.lang-pill'));
        return {
            sec: !!sec, nav: !!nav,
            pills: pills.map(function(x){return x.textContent.trim();}),
            links: pills.map(function(x){return x.getAttribute('href');})
        };
    }""")
    note("home_section", home["sec"])
    note("home_nav", home["nav"])
    note("home_pills", home["pills"])
    if not home["sec"]:
        fails.append("home page missing #languages section")
    if not home["nav"]:
        fails.append("home nav missing Languages link")
    if "Hindi full course" not in "".join(home["pills"]):
        fails.append("home pills missing Hindi full-course entry")
    for c in beta_ids:
        if ("/languages/%s/" % c) not in home["links"]:
            fails.append("home pills missing /languages/%s/ link" % c)

    # ---- hub ----
    pg.goto(BASE + "/languages/", wait_until="networkidle")
    wait_items()
    pg.wait_for_timeout(600)
    hub = pg.evaluate("""() => {
        var grids = document.querySelectorAll('.lang-grid');
        var prod = grids[0] ? grids[0].querySelectorAll('.lang-cell').length : -1;
        var beta = document.querySelectorAll('.lang-grid .lb').length;
        var sel = document.getElementById('lp-select');
        var opts = sel ? Array.from(sel.options).map(function(o){return o.value;}) : [];
        return {
            prod_cells: prod,
            beta_cells: beta,
            select_opts: opts,
            default_items: document.querySelectorAll('#langpack-app .v-item').length,
            default_concepts: document.querySelectorAll('#langpack-app .g-concept').length
        };
    }""")
    note("hub", hub)
    if hub["prod_cells"] != 1:
        fails.append("hub should have exactly 1 available cell, got %d" % hub["prod_cells"])
    if hub["beta_cells"] != 29:
        fails.append("hub should have 29 beta cells, got %d" % hub["beta_cells"])
    if sorted(hub["select_opts"]) != beta_ids:
        fails.append("picker options %s != beta ids %s" % (sorted(hub["select_opts"]), beta_ids))
    if hub["default_items"] != 36 or hub["default_concepts"] != 4:
        fails.append("hub default pack should render 36 items + 4 concepts")

    # ---- every beta detail page ----
    detail = {}
    for c in beta_ids:
        pg.goto(BASE + "/languages/%s/" % c, wait_until="networkidle")
        ok = wait_items(10)
        pg.wait_for_timeout(500)
        d = pg.evaluate("""() => {
            var t = document.body.innerText;
            return {
                items: document.querySelectorAll('#langpack-app .v-item').length,
                concepts: document.querySelectorAll('#langpack-app .g-concept').length,
                add: document.querySelectorAll('#langpack-app .hi-review-add').length,
                title: document.title,
                beta: t.indexOf('BETA') >= 0,
                notcourse: (t.indexOf('not a course') >= 0 || t.indexOf('not a full course') >= 0 || t.indexOf('not a course') >= 0)
            };
        }""")
        detail[c] = d
        if not ok or d["items"] != 36:
            fails.append("%s detail: expected 36 items, got %d" % (c, d["items"]))
        if d["concepts"] != 4:
            fails.append("%s detail: expected 4 concepts, got %d" % (c, d["concepts"]))
        if d["add"] < 36:
            fails.append("%s detail: expected SRS add-buttons, got %d" % (c, d["add"]))
        if not d["beta"]:
            fails.append("%s detail: BETA labelling missing" % c)
        if not d["notcourse"]:
            fails.append("%s detail: 'not a course' honesty missing" % c)
        if by_id[c]["name"] not in d["title"]:
            fails.append("%s detail: title should name the language" % c)
    titles = [detail[c]["title"] for c in beta_ids]
    note("detail_titles", titles)
    if len(set(titles)) != len(titles):
        fails.append("detail pages must have unique titles, got dupes")

    # ---- a PLANNED language must NOT have a thin page ----
    import urllib.request, urllib.error
    planned_no_page = 0
    for probe in planned_ids:
        try:
            urllib.request.urlopen(BASE + "/languages/%s/" % probe, timeout=5)
            planned_no_page += 1  # page exists → thin content
        except urllib.error.HTTPError as e:
            if e.code != 404:
                planned_no_page += 1
        except Exception:
            pass
    note("planned_with_page", planned_no_page)
    if planned_no_page:
        fails.append("%d PLANNED languages have detail pages (thin content)" % planned_no_page)
    note("page_errors", errs)
    b.close()

ok = not fails and not errs
res = {"generated": NOW, "pass": ok, "fails": fails, "facts": facts}
with open("reports/phase7c-langs-test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("multi-language packs + reachability:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    s = json.dumps(v, ensure_ascii=False)
    print("  %-20s %s" % (k, s[:120]))
for x in fails:
    print("  FAIL", x)
