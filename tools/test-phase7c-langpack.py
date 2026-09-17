#!/usr/bin/env python3
"""Phase 7C §53 Stage 2 — language-pack reuse proof, real Chromium (Gate I).

Verifies:
  · registry: es = BETA with starterPack, hi = PRODUCTION (only production)
  · /languages/ renders the Spanish starter pack through the SAME engines:
        36 items (24 words + 12 phrases), 4 grammar concepts
  · "hola"/"gracias" visible; "BETA" + "not a course" honesty strings present
  · Available-now grid has exactly ONE cell (Hindi) — es not labelled available
  · SRS add-button creates a card with language = "es" (shared card model)
  · 0 page errors
Output: reports/phase7c-langpack-test.json
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
es = by_id.get("es")
hi = by_id.get("hi")
note("registry_production", reg.get("production"))
note("es_status", es["productionStatus"] if es else None)
note("es_starterPack", es.get("starterPack") if es else None)
if not es or es["productionStatus"] != "BETA":
    fails.append("registry: es should be BETA, got %s" % (es and es["productionStatus"]))
if not es or not es.get("starterPack"):
    fails.append("registry: es should carry starterPack=true")
if reg.get("production") != ["hi"]:
    fails.append("registry: only hi may be PRODUCTION, got %s" % reg.get("production"))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

    pg.goto(BASE + "/languages/", wait_until="networkidle")
    for _ in range(50):
        if pg.evaluate("() => document.querySelectorAll('#langpack-app .v-item').length > 0 && document.querySelectorAll('#langpack-app .g-concept').length > 0"):
            break
        pg.wait_for_timeout(250)
    pg.wait_for_timeout(700)

    items = pg.evaluate("() => document.querySelectorAll('#langpack-app .v-item').length")
    note("pack_items", items)
    if items != 36:
        fails.append("expected 36 pack items (24 words + 12 phrases), got %d" % items)

    gram = pg.evaluate("() => document.querySelectorAll('#langpack-app .g-concept').length")
    note("pack_grammar", gram)
    if gram != 4:
        fails.append("expected 4 grammar concepts, got %d" % gram)

    body = pg.evaluate("() => document.body.innerText")
    note("has_hola", "hola" in body and "gracias" in body)
    if "hola" not in body or "gracias" not in body:
        fails.append("Spanish starter items not rendered")
    if "BETA" not in body:
        fails.append("BETA labelling missing")
    if "not a course" not in body:
        fails.append("'not a course' honesty string missing")

    # Available-now grid must contain exactly one cell (Hindi)
    prod_cells = pg.evaluate("""() => {
        var grids = document.querySelectorAll('.lang-grid');
        var first = grids[0];
        var cells = first ? first.querySelectorAll('.lang-cell') : [];
        var texts = Array.from(cells).map(function(c){ return c.innerText; });
        return {count: cells.length, texts: texts};
    }""")
    note("prod_grid", prod_cells)
    if prod_cells["count"] != 1 or "Hindi" not in "".join(prod_cells["texts"]):
        fails.append("Available-now grid should have exactly 1 Hindi cell, got %r" % prod_cells)

    # Spanish must carry the beta tag, not "Available"
    es_tag = pg.evaluate("() => { var c = Array.from(document.querySelectorAll('.lang-cell')).filter(function(x){return x.innerText.indexOf('Spanish')>=0;})[0]; return c ? c.innerText : 'NONE'; }")
    note("es_cell", es_tag[:120])
    if "Starter" not in es_tag or "Available" in es_tag:
        fails.append("Spanish cell mislabelled: %r" % es_tag)

    # SRS add-button → card language = es (shared language-agnostic card model)
    pg.evaluate("() => { try { localStorage.removeItem('ekguru:hindi:v1:review'); } catch(e){} }")
    pg.click("#langpack-app .hi-review-add >> nth=0")
    pg.wait_for_timeout(300)
    lang = pg.evaluate("() => { var c = window.EkGuruSRS.all(); return c[0] ? c[0].language : null; }")
    note("srs_card_language", lang)
    if lang != "es":
        fails.append("SRS card language should be 'es', got %r" % lang)

    note("page_errors", errs)
    b.close()

ok = not fails and not errs
res = {"generated": NOW, "pass": ok, "fails": fails, "facts": facts}
with open("reports/phase7c-langpack-test.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
print("language-pack reuse proof:", "PASS" if ok else "FAIL")
for k, v in facts.items():
    print("  %-22s %s" % (k, json.dumps(v, ensure_ascii=False)[:130]))
for x in fails:
    print("  FAIL", x)
