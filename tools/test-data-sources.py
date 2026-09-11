#!/usr/bin/env python3
"""Live data-source regression test (run: python3 tools/test-data-sources.py).

Checks the production Google-Sheets data layer end to end:
  - every csvUrl in js/site-config.js returns HTTP 200 as text/csv
  - each sheet has its required header columns
  - ids are unique and non-empty (tutors, reviews, content)
  - settings is key/value shaped and keys are unique
  - the Google Apps Script endpoint answers its health JSON

Exit code 0 = all pass, 1 = any failure.
"""
import csv, io, json, re, sys, urllib.request
from collections import Counter

ROOT = __import__("pathlib").Path(__file__).resolve().parent.parent

def get_config_urls():
    cfg = (ROOT / "js" / "site-config.js").read_text(encoding="utf-8")
    return re.findall(r'csvUrl:\s*"([^"]+)"', cfg)

def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "EkGuru-test/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read().decode("utf-8-sig")

def parse(text):
    return [row for row in csv.reader(io.StringIO(text)) if any(c.strip() for c in row)]

def data_rows(rows):
    return [r for r in rows[1:] if r and r[0] and not r[0].startswith("#")]

failures = []
checks = 0

def check(name, cond, detail=""):
    global checks
    checks += 1
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        failures.append(name)

print("== 1. Configured CSV endpoints ==")
urls = get_config_urls()
print(f"  csvUrl count in js/site-config.js: {len(urls)}")
if len(urls) != 4:
    failures.append("expected exactly 4 csvUrls")

BASE = "2PACX-1vRGCkYfn_JfKPGaUy7tGWRFoPvo7x6-cB4SLTbi-kzKY1f0k1hwXYCwYob-qHG5EKZeVrwcBeBD64fc"
for u in urls:
    check(f"consolidated workbook: {u.split('/d/e/')[1].split('/')[0][:20]}…", BASE in u)

# identify sheets by gid
gid = {re.search(r"gid=(\d+)", u).group(1): u for u in urls}
print("  gids configured:", sorted(gid.keys()))

sheets = {}
for g, u in gid.items():
    status, ctype, text = fetch(u)
    rows = parse(text)
    head = [h.strip().lower() for h in rows[0]] if rows else []
    label = {"1290168568": "reviews", "764031473": "settings",
             "2135319947": "content", "834026040": "tutors"}.get(g, g)
    sheets[label] = (rows, head)
    check(f"{label}: HTTP {status} text/csv", status == 200 and "csv" in ctype, f"{status} {ctype}")
    check(f"{label}: has header row", len(rows) >= 2 and len(head) > 0)

print("\n== 2. Schema checks ==")
t_rows, t_head = sheets.get("tutors", ([], []))
check("tutors: has 'id' column", "id" in t_head, str(t_head[:8]))
check("tutors: has 'formKey' column", "formkey" in t_head)
check("tutors: has 'holiday' column", "holiday" in t_head)
check("tutors: has 'exams' column", "exams" in t_head)
check("tutors: has 'email' column", "email" in t_head)
t_ids = [r[t_head.index("id")] for r in data_rows(t_rows) if t_head]
check("tutors: data rows == 4", len(t_ids) == 4, f"got {len(t_ids)}")
check("tutors: unique ids", len(set(t_ids)) == len(t_ids), f"dup? {[k for k,v in Counter(t_ids).items() if v>1]}")

r_rows, r_head = sheets.get("reviews", ([], []))
check("reviews: has required cols", all(c in r_head for c in ["tutor", "name", "stars", "text"]), str(r_head))
if "tutor" in r_head:
    rr = data_rows(r_rows)
    check("reviews: non-empty data rows", len(rr) >= 1, f"got {len(rr)}")

s_rows, s_head = sheets.get("settings", ([], []))
check("settings: key/value shaped", "key" in s_head and "value" in s_head, str(s_head))
if "key" in s_head:
    ki, vi = s_head.index("key"), s_head.index("value")
    pairs = [(r[ki], r[vi]) for r in s_rows[1:] if len(r) > vi and r[ki] and not r[ki].startswith("#") and r[vi]]
    keys = [k for k, _ in pairs]
    check("settings: unique keys", len(set(keys)) == len(keys), f"dup? {[k for k,v in Counter(keys).items() if v>1]}")
    print("  settings keys:", keys)

c_rows, c_head = sheets.get("content", ([], []))
check("content: has required cols", all(c in c_head for c in ["slug", "question", "answer", "status"]), str(c_head))
if "slug" in c_head:
    ci = c_head.index("slug")
    cr = data_rows(c_rows)
    cids = [r[ci] for r in cr]
    check("content: unique slugs", len(set(cids)) == len(cids), f"dup? {[k for k,v in Counter(cids).items() if v>1]}")
    print(f"  content live rows: {len(cr)}")

print("\n== 3. Apps Script endpoint ==")
APPS = "https://script.google.com/macros/s/AKfycbwG978gM3Vspo0r8JmNxRojiUwA5h0tWoFd8p9vQf5x-NX9QGDB8VCr0j1LnTPoOjqtdA/exec"
try:
    status, ctype, text = fetch(APPS)
    body = json.loads(text)
    check("Apps Script: HTTP 200 JSON health", status == 200 and "json" in ctype and body.get("success") == "true", f"{status} {text[:80]}")
except Exception as e:
    check("Apps Script: reachable", False, str(e))

print(f"\n{checks} checks, {len(failures)} failures")
sys.exit(1 if failures else 0)
