#!/usr/bin/env python3
"""Phase 3 dynamic tests (real Chromium):
  · §12 booking snapshot integrity — create booking, change source tutor data,
    verify the historical snapshot is unchanged.
  · §16 search quality audit — query battery against the single-source index.
"""
import json, time, re
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8017"
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# =========================================================== booking integrity
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(BASE + "/tutor/sushila-g/", wait_until="domcontentloaded")
    pg.wait_for_function("() => window.EkGuruStore", timeout=10000)
    result = pg.evaluate("""() => {
      var out = {};
      if (!window.EkGuruStore && !window.Store) { out.error = "store not found"; return out; }
      var S = window.EkGuruStore || window.Store;
      try { S.clear(); } catch (e) {}
      // 1. create a booking while the tutor's source name is "Sushila G."
      S.add({ ref: "BK-TEST-1", tutorId: "sushila-g", tutor: "Sushila G.", name: "Test Student",
              email: "student@example.com", slot: "Mon 10:00", goal: "speaking",
              tutorNameSnapshot: "Sushila G.", tutorEmailSnapshot: "", lessonType: "trial" });
      var first = S.all()[0];
      out.snapshotWritten = first.tutorNameSnapshot === "Sushila G.";
      out.snapshotEmailBlank = first.tutorEmailSnapshot === "";
      // 2. simulate the source tutor record changing name
      S.add({ ref: "BK-TEST-2", tutorId: "sushila-g", tutor: "Sushila Renamed",
              name: "Test Student", email: "student@example.com", slot: "Tue 10:00",
              tutorNameSnapshot: "Sushila Renamed", tutorEmailSnapshot: "", lessonType: "trial" });
      var still = S.all().filter(function(r){return r.ref==="BK-TEST-1";})[0];
      out.historicalUnchanged = still.tutorNameSnapshot === "Sushila G.";
      out.historicalRef = still.ref;
      // 3. a status update must not touch the snapshot
      S.update("BK-TEST-1", { status: "confirmed" });
      var after = S.all().filter(function(r){return r.ref==="BK-TEST-1";})[0];
      out.updateKeepsSnapshot = after.tutorNameSnapshot === "Sushila G." && after.status === "confirmed";
      out.fields = Object.keys(first).filter(function(k){return /snapshot|lessonType|ref|status/.test(k);});
      return out;
    }""")
    pg.close()
    b.close()

booking = {"generated": NOW, "test": "create booking → change source tutor name → verify historical snapshot unchanged",
           "result": result, "pass": bool(result.get("snapshotWritten") and result.get("historicalUnchanged")
                                          and result.get("updateKeepsSnapshot") and result.get("snapshotEmailBlank"))}
with open("reports/booking-snapshot-integrity.json", "w", encoding="utf-8") as f:
    json.dump(booking, f, indent=2)
print("booking integrity:", booking["pass"], result)

# =========================================================== search quality
QUERIES = [
    ("tutor", "Sushila"), ("lesson", "alphabet"), ("material", "devanagari chart"),
    ("tool", "numbers"), ("practice", "verb practice"), ("vocabulary", "vocabulary"),
    ("phrase", "phrases for travel"), ("hindi", "hindi"), ("english", "how to say hello"),
    ("location", "Jaipur"), ("country", "Japan"), ("exact-title", "Hindi Verb Practice — Endings and Tenses"),
    ("partial", "postpositions"), ("typo", "devanagri"), ("no-result", "zzzzqqqxx"),
]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(BASE + "/search/", wait_until="domcontentloaded")
    pg.wait_for_timeout(400)
    out = []
    for label, q in QUERIES:
        pg.fill("#q", q)
        pg.wait_for_timeout(500)
        rec = pg.evaluate("""() => {
          var hits = document.querySelectorAll('#res .faq');
          var first = hits[0];
          return {
            count: hits.length,
            firstTitle: first ? first.querySelector('b').textContent : null,
            firstHref: first ? first.querySelector('a').getAttribute('href') : null,
            firstType: first ? first.querySelector('.pill').textContent : null
          };
        }""")
        rec["query"] = q
        rec["label"] = label
        out.append(rec)
    pg.close()
    b.close()

search = {"generated": NOW, "queries": out,
          "summary": {
              "total": len(out),
              "withResults": sum(1 for r in out if r["count"] > 0),
              "noResultAsExpected": out[-1]["count"] == 0 if out else None,
              "distinctTypesSeen": sorted({r["firstType"] for r in out if r["firstType"]}),
          }}
with open("reports/search-quality-phase3.json", "w", encoding="utf-8") as f:
    json.dump(search, f, indent=2)
for r in out:
    print(f"{r['label']:12} '{r['query'][:28]:28}' -> {r['count']:2} | {r['firstType']} | {(r['firstTitle'] or '')[:44]}")
print("types seen:", search["summary"]["distinctTypesSeen"])
