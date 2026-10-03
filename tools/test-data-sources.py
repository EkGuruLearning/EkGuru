#!/usr/bin/env python3
"""Data-source regression test (run: python3 tools/test-data-sources.py).

Two live modes, detected from js/site-config.js:

  LIVE   — the four csvUrl fields hold published Google Sheet URLs.
           Each is fetched with the FIXED fallback order (U0, 30 Sep 2026):
               1. the URL with output=csv
               2. on non-200 / non-CSV / no id column — the same URL with
                  output=tsv  (Google's published-CSV endpoint for this
                  workbook answers HTTP 500 while output=tsv answers 200)
           When every sheet is only reachable via TSV the run reports
           "PASS (tsv fallback)" — the data path is alive, the CSV endpoint
           is not. When BOTH formats fail for any tab, it is a FAIL.

           Schema checks (required header columns, unique ids, settings
           key/value shape) run on whichever format answered — CSV and TSV
           are parsed with one parser (csv module, delimiter-aware) so the
           checks cannot drift between the two.

  PAUSED — the four csvUrl fields are empty + pausedForReupload flags set
           (DATA_SOURCE_STATUS = PAUSED_FOR_REUPLOAD, v101, 11 Sep 2026).
           The site then serves baked-in local data, so the SAME schema
           checks run against csv/*.csv instead of failing on missing URLs.

Offline verification (no network — used in the audit sandbox):
  EKGURU_TEST_FIXTURE_DIR=tests/fixtures python3 tools/test-data-sources.py
           runs the SAME schema checks against local exports
           (tutors.tsv, reviews.tsv, settings.tsv, content fixture or
           csv/ekguru_content.csv) and skips the network + Apps Script
           health check. This is how the check code itself is tested.

In both live modes the Google Apps Script endpoint answers its health JSON.
That one probe is retried up to three times, 5s apart, and the attempt it
answered on is printed: the endpoint has timed out transiently in CI (the
same commit green on one run, red on the next, 3 Oct 2026). A genuinely
unreachable endpoint still fails the run — it just takes ~10s more to say so.

Exit code 0 = all pass, 1 = any failure.
"""
import csv, io, json, re, sys, time, urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_raw = __import__("os").environ.get("EKGURU_TEST_FIXTURE_DIR") or ""
# Path("") is PosixPath('.') — ALWAYS truthy and always a dir. The env var
# must decide, or LIVE mode is unreachable (that bug is exactly what sent CI
# hunting for ./tutors.tsv instead of the published sheet).
FIXTURE_DIR = Path(_raw) if _raw else None

def get_config_csvurls():
    """All csvUrl values in js/site-config.js, INCLUDING empty ones."""
    cfg = (ROOT / "js" / "site-config.js").read_text(encoding="utf-8")
    return re.findall(r'csvUrl:\s*"([^"]*)"', cfg)

def is_paused():
    cfg = (ROOT / "js" / "site-config.js").read_text(encoding="utf-8")
    return "pausedForReupload: true" in cfg or "PAUSED_FOR_REUPLOAD" in cfg

def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "EkGuru-test/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read().decode("utf-8-sig")

def fetch_retry(url, timeout=30, attempts=3, backoff=5, label="probe", fetcher=None):
    """A live endpoint that times out once is not a failing endpoint.

    The Apps Script health probe answered on one CI run and timed out on the next
    with no code change (3 Oct 2026), and the same probe has done it before.
    scripts.google.com answers this JSON in well under a second when it is up, so
    a timeout is the network, not the endpoint. Retry it a BOUNDED number of
    times and report how many attempts it took: a genuinely dead endpoint still
    fails the run, it just takes ~10s longer to say so. Returns the same triple
    as fetch() plus the attempt number.
    """
    fetcher = fetcher or fetch
    last = None
    for attempt in range(1, attempts + 1):
        try:
            status, ctype, text = fetcher(url, timeout=timeout)
            return status, ctype, text, attempt
        except Exception as e:                       # noqa: BLE001 — reported below
            last = e
            if attempt < attempts:
                print(f"  [{label}] attempt {attempt}/{attempts} -> {type(e).__name__}: {e}"
                      f" — retrying in {backoff}s")
                time.sleep(backoff)
    raise last

def parse(text, delim=","):
    """One parser for BOTH formats: RFC-4180 quoting with a variable
    delimiter (Google's TSV export quotes exactly like its CSV export,
    so multi-line about/bio/experience cells survive either way)."""
    return [row for row in csv.reader(io.StringIO(text), delimiter=delim)
            if any(c.strip() for c in row)]

def read_local(name):
    p = ROOT / "csv" / name
    with open(p, encoding="utf-8-sig") as f:
        return parse(f.read())

def data_rows(rows):
    return [r for r in rows[1:] if r and r[0] and not r[0].startswith("#")]

failures = []
checks = 0
fallback_used = []

def check(name, cond, detail=""):
    global checks
    checks += 1
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        failures.append(name)

def fetch_sheet(url, label):
    """CSV first, TSV second (the U0 contract). Returns rows or None."""
    for fmt in ("csv", "tsv"):
        u = re.sub(r"([?&])output=[^&]*", r"\1output=" + fmt, url) if "output=" in url \
            else url + ("&" if "?" in url else "?") + "output=" + fmt
        try:
            status, ctype, text = fetch(u)
        except Exception as e:
            print(f"  [{label}] output={fmt} -> {type(e).__name__}: {e}")
            continue
        if status != 200:
            print(f"  [{label}] output={fmt} -> HTTP {status}")
            continue
        if text.lstrip().startswith("<"):
            print(f"  [{label}] output={fmt} -> HTML page, not {fmt}")
            continue
        rows = parse(text, "\t" if fmt == "tsv" else ",")
        head = [h.strip().lower() for h in rows[0]] if rows else []
        if not head or not any(c in head for c in ("id", "tutor", "key", "slug")):
            print(f"  [{label}] output={fmt} -> header has no id/tutor/key column")
            continue
        if fmt == "tsv":
            fallback_used.append(label)
            check(f"{label}: reachable via tsv fallback (csv endpoint down)", True)
        else:
            check(f"{label}: reachable via csv", True)
        return rows, head
    return None, []

print("== 0. Mode detection ==")
all_urls = get_config_csvurls()
live_urls = [u for u in all_urls if u.strip()]
print(f"  csvUrl fields in js/site-config.js: {len(all_urls)} ({len(live_urls)} non-empty)")
if len(all_urls) != 4:
    failures.append("expected exactly 4 csvUrl fields")

OFFLINE = bool(FIXTURE_DIR) and FIXTURE_DIR.is_dir()
if OFFLINE:
    MODE = "OFFLINE"
    print(f"  MODE = OFFLINE — schema checks against {FIXTURE_DIR} (network skipped)")
elif len(live_urls) == 0 and is_paused():
    MODE = "PAUSED"
    print("  MODE = PAUSED_FOR_REUPLOAD (by design, v101) — validating local csv/*.csv")
elif len(live_urls) == 4:
    MODE = "LIVE"
    print("  MODE = LIVE — fetching published Google Sheets (csv first, tsv fallback)")
else:
    MODE = "MIXED"
    print("  MODE = MIXED — some csvUrl empty, some set (misconfiguration)")
    failures.append("mixed csvUrl state: all four must be set (LIVE) or all empty + paused (PAUSED)")

sheets = {}

if MODE == "LIVE":
    print("\n== 1. Configured CSV/TSV endpoints ==")
    urls = live_urls
    BASE = "2PACX-1vQIman_Um2wQrj_3mXqqgq4k69zzmJHkhZ1TRoAnh2jcamhzoo-0VeTd55UieGMi6mEaTl3Zy84G44h"
    for u in urls:
        check(f"consolidated workbook: {u.split('/d/e/')[1].split('/')[0][:20]}…", BASE in u)

    gid = {re.search(r"gid=(\d+)", u).group(1): u for u in urls}
    print("  gids configured:", sorted(gid.keys()))
    LABELS = {"298809212": "reviews", "1658518385": "settings",
              "1654125803": "content", "1631273256": "tutors"}

    for g, u in gid.items():
        label = LABELS.get(g, g)
        rows, head = fetch_sheet(u, label)
        if rows is None:
            check(f"{label}: reachable in ANY format (csv AND tsv failed)", False)
            sheets[label] = ([], [])
            continue
        check(f"{label}: has header row", len(rows) >= 2 and len(head) > 0)
        sheets[label] = (rows, head)

elif MODE == "OFFLINE":
    print("\n== 1. Local fixture exports (offline verification) ==")
    names = {"tutors": "tutors.tsv", "reviews": "reviews.tsv",
             "settings": "settings.tsv", "content": None}
    for label, fname in names.items():
        if label == "content":
            # the content tab is large; fall back to the baked CSV snapshot
            rows = read_local("ekguru_content.csv")
            head = [h.strip().lower() for h in rows[0]] if rows else []
            sheets[label] = (rows, head)
            check("content: local file csv/ekguru_content.csv readable", True)
            continue
        p = FIXTURE_DIR / fname
        if not p.exists():
            check(f"{label}: fixture {p} exists", False, "missing")
            sheets[label] = ([], [])
            continue
        rows = parse(p.read_text(encoding="utf-8"), "\t")
        head = [h.strip().lower() for h in rows[0]] if rows else []
        sheets[label] = (rows, head)
        check(f"{label}: fixture {fname} readable", True)
        check(f"{label}: has header row", len(rows) >= 2 and len(head) > 0)

elif MODE == "PAUSED":
    print("\n== 1. Local CSV files (paused mode — these ARE the live data) ==")
    local_files = {"tutors": "ekguru_tutors.csv", "reviews": "ekguru_reviews.csv",
                   "settings": "ekguru_settings.csv", "content": "ekguru_content.csv"}
    for label, fname in local_files.items():
        try:
            rows = read_local(fname)
        except FileNotFoundError:
            check(f"{label}: local file csv/{fname} exists", False, "missing")
            sheets[label] = ([], [])
            continue
        head = [h.strip().lower() for h in rows[0]] if rows else []
        sheets[label] = (rows, head)
        check(f"{label}: local file csv/{fname} readable", True)
        check(f"{label}: has header row", len(rows) >= 2 and len(head) > 0)

print("\n== 2. Schema checks (identical for csv and tsv) ==")
t_rows, t_head = sheets.get("tutors", ([], []))
check("tutors: has 'id' column", "id" in t_head, str(t_head[:8]))
check("tutors: has 'formkey' column", "formkey" in t_head)
check("tutors: has 'holiday' column", "holiday" in t_head)
check("tutors: has 'exams' column", "exams" in t_head)
check("tutors: has 'email' column", "email" in t_head)
t_ids = [r[t_head.index("id")] for r in data_rows(t_rows) if t_head]
check("tutors: has data rows", len(t_ids) >= 1, f"got {len(t_ids)}")
check("tutors: unique ids", len(set(t_ids)) == len(t_ids), f"dup? {[k for k,v in Counter(t_ids).items() if v>1]}")
check("tutors: ids look like slugs", all(re.fullmatch(r"[a-z0-9-]+", i) for i in t_ids), str(t_ids))
if "active" in t_head:
    ai = t_head.index("active")
    actives = Counter((r[ai] if len(r) > ai else "").strip().lower() for r in data_rows(t_rows))
    print("  tutor active flags:", dict(actives))

r_rows, r_head = sheets.get("reviews", ([], []))
check("reviews: has required cols", all(c in r_head for c in ["tutor", "name", "stars", "text"]), str(r_head))
if "tutor" in r_head:
    rr = data_rows(r_rows)
    # 30 Sep 2026: the tab may hold 0 rows (site-native reviews only); the
    # shape is what matters. Rows, when present, must carry a tutor id.
    check("reviews: data rows (if any) carry a tutor id",
          all(len(r) > r_head.index("tutor") and r[r_head.index("tutor")] for r in rr), f"{len(rr)} rows")
    print(f"  reviews rows: {len(rr)}")

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
if MODE == "OFFLINE":
    print("  skipped (offline verification mode)")
else:
    APPS = "https://script.google.com/macros/s/AKfycbzdX02U8KQU0XZpqXp4ACuNDAShrOKcHPCrMW5R3UcWOtHuWqquyouppkNusnLIz5ri/exec"
    try:
        status, ctype, text, tries = fetch_retry(APPS, label="Apps Script")
        body = json.loads(text)
        check("Apps Script: HTTP 200 JSON health", status == 200 and "json" in ctype and str(body.get("success")).lower() == "true", f"{status} {text[:80]}")
        if tries > 1:
            print(f"  [Apps Script] answered on attempt {tries}/3 (the earlier timeout was transient)")
    except Exception as e:
        check("Apps Script: reachable", False, f"{type(e).__name__}: {e} (after 3 attempts)")

verdict = "PASS"
if failures:
    verdict = "FAIL"
elif fallback_used:
    verdict = "PASS (tsv fallback)"
print(f"\nMODE={MODE}: {checks} checks, {len(failures)} failures — {verdict}")
if fallback_used:
    print("  tsv fallback used for:", ", ".join(fallback_used))
sys.exit(1 if failures else 0)
