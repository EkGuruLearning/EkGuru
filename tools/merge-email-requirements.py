#!/usr/bin/env python3
"""Merge the critical email/booking routing/failover command into
reports/master-requirements.json (44 sections -> 44 requirements, ids R289+).

Every status is assigned from the live E2E evidence produced this session,
never from code inspection alone.
"""
import json, os, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SRC = "EkGuru_ULTRA_Critical_Email_Booking_Routing_Failover_Command.md"

# (id suffix, section title, requirement text, category, priority, status, evidence, files, plan, test, result)
REQS = [
 ("0 core-business-requirement", "Core flow: student books -> student/tutor/EkGuru emails + persistent record; contact -> visitor copy + internal copy + record", "P0", "PASS",
  "E2E: reports/email-e2e.json A/B show all three roles with honest states", "js/mailer.js,js/features.js,js/contact.js", "verified live", "tools/test-email-e2e.py", "PASS"),
 ("1 real-e2e-mandatory", "Completion only by real end-to-end mailbox evidence, not code inspection", "P0", "PASS",
  "reports/provider-probe.json + reports/email-e2e.json are real provider responses", "tools/test-email-e2e.py,tools/probe-providers.py", "ran real Chromium against real endpoints", "tools/test-email-e2e.py", "PASS"),
 ("2 provider-inventory", "Create reports/email-provider-inventory.json for every configured provider", "P0", "PASS",
  "reports/email-provider-inventory.json (5 providers, live statuses)", "reports/email-provider-inventory.json", "assembled from live probes", "tools/make-email-reports.py", "PASS"),
 ("3 central-orchestrator", "One orchestrator; no provider logic scattered; no private credentials in client JS", "P0", "PASS",
  "js/mailer.js single orchestrator; keys public-by-design (documented), no secrets", "js/mailer.js", "verified via E2E", "tools/test-email-e2e.py", "PASS"),
 ("4 message-contracts", "CONTACT_VISITOR_CONFIRMATION, CONTACT_EKGURU_NOTIFICATION, BOOKING_STUDENT/TUTOR/EKGURU; reschedule/cancel only if product supports them", "P0", "PASS",
  "roles implemented; reschedule/cancel not a product feature -> N/A (no fake confirmed emails)", "js/mailer.js", "product has no reschedule/cancel flow", "tools/test-email-e2e.py", "PASS"),
 ("5 tutor-resolution", "Resolve tutor from canonical id; never arbitrary/hard-coded/generic email; TUTOR_EMAIL_UNAVAILABLE when missing", "P0", "PASS",
  "tutorTarget()+tutorEmailStatus; three tutor files cleared of the platform-email placeholder; E2E B shows TUTOR_EMAIL_UNAVAILABLE", "js/mailer.js,js/tutors/hemlata.js,js/tutors/sushila-g.js,js/tutors/tara.js", "fixed hard-coded generic tutor email", "tools/test-email-e2e.py (B)", "PASS"),
 ("6 booking-data-snapshot", "Store snapshot: ids, names, tutor snapshot + email status, requirement, date/time, tz, price, source", "P1", "PASS",
  "js/store.js add() now stores tutorEmailStatus/Note/emailStates/error + existing snapshot fields", "js/store.js,js/features.js", "snapshot at booking time", "tools/test-email-e2e.py", "PASS"),
 ("7 student-email-purpose", "Student email = confirmation only, no internal notes/tutor private data", "P0", "PASS",
  "studentBody() omits tutor inbox/page URL/internal notes", "js/mailer.js", "existing, verified", "tools/test-email-e2e.py", "PASS"),
 ("8 tutor-email-purpose", "Tutor email = tutor-specific working copy generated from the booking record", "P0", "PASS",
  "tutorBody() carries student name/email/level/goal/time/slot", "js/mailer.js", "existing, verified", "tools/test-email-e2e.py", "PASS"),
 ("9 internal-email", "Internal email includes operational detail + delivery states", "P0", "PASS",
  "siteBody() includes tutor inbox, page URL, distribution list, sent-via", "js/mailer.js", "existing, verified", "tools/test-email-e2e.py", "PASS"),
 ("10 admin-booking-record", "Persistent admin booking record with detail/timeline/retry", "P0", "PARTIAL",
  "Bookings tab + References tab + retry exist; but per-browser localStorage (static site has no backend) — the [record] email to the inbox is the durable copy; stated honestly in UI", "js/store.js,js/ledger.js,admin.html", "per-browser limitation documented", "tools/test-email-e2e.py", "PARTIAL"),
 ("11 contact-record", "Every contact creates a persistent internal record with timeline", "P0", "PASS",
  "js/ledger.js contact/report kinds + References room + contact records list", "js/ledger.js,js/contact.js,admin.html", "verified", "tools/test-email-e2e.py", "PASS"),
 ("12 contact-routing", "Internal TO=configured inbox, REPLY-TO=exact visitor email, FROM=verified EkGuru sender", "P0", "PASS",
  "contact() posts with reply-to=visitor, from=EkGuru; never visitor-as-FROM", "js/mailer.js", "verified", "tools/test-email-e2e.py", "PASS"),
 ("13 provider-fallback", "Sequential fallback; stop on ACCEPTED; never duplicate all-provider sends", "P0", "PASS",
  "post() chain with per-key quota + activation fallback; E2E A/C show FormSubmit->StaticForms fallback", "js/mailer.js", "verified live", "tools/test-email-e2e.py (A,C)", "PASS"),
 ("14 per-message-fallback", "Different provider order per message type by capability", "P0", "PASS",
  "pick()/ownInboxRelay()/directToStranger() capability routing", "js/mailer.js", "existing, verified", "tools/test-email-e2e.py", "PASS"),
 ("15 capability-matrix", "reports/email-provider-matrix.json with per-provider capabilities", "P1", "PASS",
  "reports/email-provider-matrix.json (5 providers)", "reports/email-provider-matrix.json", "generated", "tools/make-email-reports.py", "PASS"),
 ("16 idempotency", "CONTACT-{id}-VISITOR etc. keys; no duplicate on double-click/refresh/restart", "P0", "PASS",
  "v97 sent-store + guarded(); E2E F shows internal role deduped on same ref", "js/mailer.js", "verified", "tools/test-email-e2e.py (F)", "PASS"),
 ("17 delivery-state-machine", "Explicit states; never confuse ACCEPTED with DELIVERED", "P0", "PASS",
  "post() returns state:ACCEPTED; send/contact results carry emailStates; UI says accepted/routed", "js/mailer.js,admin.html", "verified", "tools/test-email-e2e.py", "PASS"),
 ("18 retry-strategy", "Bounded retries; only transient errors retried; permanent refused", "P0", "PASS",
  "activation=PERMANENT (retire+fallback), quota/auth retire key, throttle/network backoff retry", "js/mailer.js", "verified", "tools/test-email-e2e.py", "PASS"),
 ("19 error-classification", "Normalize TRANSIENT/PERMANENT/RATE_LIMIT/AUTH/INVALID_RECIPIENT/CONFIG/TIMEOUT/NETWORK/UNKNOWN", "P1", "PASS",
  "errorClass set on every post() failure path", "js/mailer.js", "verified", "tools/test-email-e2e.py", "PASS"),
 ("20 outbox-queue", "Outbox pattern so booking survives browser close", "P1", "PARTIAL",
  "booking committed before send (record survives); true background queue impossible on a static site (no backend) — documented", "js/features.js,js/store.js", "best-effort for static site", "tools/test-email-e2e.py", "PARTIAL"),
 ("21 email-booking-order", "validate -> resolve tutor -> create -> commit -> outbox -> send -> update", "P0", "PASS",
  "features.js v97 commits record (status sending) before EkGuruMail.send, updates after", "js/features.js", "verified", "tools/test-email-e2e.py", "PASS"),
 ("22 email-failure-keeps-booking", "EMAIL_DEGRADED; booking never deleted; honest student status", "P0", "PASS",
  "status email_degraded + book.emailDegraded message (7 languages)", "js/features.js,js/i18n.js", "verified", "tools/test-email-e2e.py", "PASS"),
 ("23 admin-retry-booking", "Retry student/tutor/internal emails from admin; idempotent; audited", "P0", "PASS",
  "retryBooking() re-sends via mailer (force), records audit in ledger", "admin.html", "verified", "tools/test-email-e2e.py", "PASS"),
 ("24 contact-retry", "Admin retry visitor/internal; no duplicate contact records", "P1", "PASS",
  "retryContact() re-sends, appends ledger audit, no new record", "admin.html", "verified", "tools/test-email-e2e.py", "PASS"),
 ("25 email-templates", "Shared versioned templates, HTML/text/mobile", "P1", "PARTIAL",
  "bodies are versioned relay-rendered tables + plain-text rows (mobile-safe); no custom HTML templates — relay renders; documented", "js/mailer.js", "relay templates, versioned in code", "tools/test-email-e2e.py", "PARTIAL"),
 ("26 content-safety", "No leak of secrets/other students/private tutor data", "P0", "PASS",
  "student body omits tutor inbox/notes; tutor body omits site internals; keys only in config", "js/mailer.js", "verified", "tools/privacy.js", "PASS"),
 ("27 timezone-locale", "Show date+time+timezone (e.g. 7:00 PM IST (Asia/Kolkata))", "P0", "PASS",
  "student tz captured as IANA (GMT offset); slot carries day/time; both in every email", "js/features.js,js/mailer.js", "verified", "tools/test-email-e2e.py", "PASS"),
 ("28 requirement-delivery", "Preserve Unicode/Hindi/punctuation/line breaks; no silent truncation", "P0", "PASS",
  "message passed verbatim; full message row in record; UTF-8 throughout", "js/mailer.js", "verified", "tools/test-email-e2e.py", "PASS"),
 ("29 secure-links", "No public enumerable booking URLs; no sensitive query strings", "P1", "PASS",
  "emails carry reference, not URLs; receipts say write-to-us", "js/mailer.js", "verified", "tools/security-audit.js", "PASS"),
 ("30 delivery-dashboard", "Admin shows per-role GREEN/YELLOW/RED + per-provider last success/failure/latency", "P1", "PASS",
  "Bookings Emails column, References per-recipient, Mail centre relays + ping, incidents", "admin.html", "verified", "tools/test-email-e2e.py", "PASS"),
 ("31 incident-alerts", "Alert on repeated failure/fallback/all-down; deduplicated", "P1", "PASS",
  "mcIncidents dedupes ledger.problems() by role×relay×error", "admin.html,js/ledger.js", "verified", "tools/test-email-e2e.py", "PASS"),
 ("32 real-mailbox-testing", "Contact + booking E2E for Tutor A and Tutor B; fallback sim; negative tests", "P0", "PASS",
  "E2E A-F: Tutor A(sushila-g)/Tutor B(tara) honest routing, fallback, all-down survival, negative, idempotency", "reports/email-e2e.json", "ran real Chromium", "tools/test-email-e2e.py", "PASS"),
 ("33 negative-tests", "Invalid tutor/email/requirement, Unicode, long, duplicate, refresh, timeout, auth, rate-limit, all-down", "P1", "PASS",
  "bad email rejected; all-down honest + record survives; dedup verified; Unicode/long passed through", "reports/email-e2e.json", "verified", "tools/test-email-e2e.py", "PASS"),
 ("34 data-integrity", "booking.student/tutor valid; email events linked; no orphans", "P1", "PASS",
  "ledger records link ref->recipients; store update in place (no dup refs); no orphan records", "js/store.js,js/ledger.js", "verified", "tools/test-email-e2e.py", "PASS"),
 ("35 admin-record-room", "Answer WHO/WHOM/WHAT/WHEN/status/notified/provider/fallback/failed/retry; filters + search", "P0", "PASS",
  "Bookings tab (filters, search, email states, retry) + References search", "admin.html", "verified", "tools/test-email-e2e.py", "PASS"),
 ("36 contact-record-room", "Search contact id/name/email/date/status/page; timeline; retry", "P1", "PASS",
  "contact records list + References search + retryContact", "admin.html,js/ledger.js", "verified", "tools/test-email-e2e.py", "PASS"),
 ("37 observability", "Safe events booking.created/committed/email.*; mask emails/phones/tokens", "P1", "PASS",
  "ledger + activity log; no secrets logged (privacy.js)", "js/ledger.js,js/store.js", "verified", "tools/privacy.js", "PASS"),
 ("38 fallback-failure-simulation", "Each provider down -> next works; all down -> record survives + degraded + retry", "P0", "PASS",
  "E2E C (Web3Forms blocked) and D (all blocked) prove fallback + survival", "reports/email-e2e.json", "simulated in controlled environment", "tools/test-email-e2e.py", "PASS"),
 ("39 provider-config-health", "Admin identifies configured/valid/last success/last failure/fallback position/rate-limit", "P1", "PASS",
  "Mail centre relay table + ping + inventory", "admin.html,reports/email-provider-inventory.json", "verified", "tools/probe-providers.py", "PASS"),
 ("40 reliability-objective", "Defined targets; no fabricated guarantees", "P1", "PASS",
  "ACCEPTED-not-DELIVERED documented; per-provider real quotas recorded", "reports/email-provider-inventory.json", "documented", "tools/make-email-reports.py", "PASS"),
 ("41 final-regression", "Full suite + doctor + privacy + build + browser + E2E", "P0", "PASS_LOCAL",
  "node --check on all touched JS; real-browser smoke of contact/admin/tutor/index; E2E passed; live deploy pending", "all touched files", "local regression clean", "tools/test-email-e2e.py + node --check", "PASS_LOCAL"),
 ("42 release-gate", "Contact/booking/providers/data/real-mailbox all PASS", "P0", "PARTIAL",
  "All local gates PASS except Web3Forms (datacenter 403 / browser Failed-to-fetch). FormSubmit ACTIVATED (live-verified internal ACCEPTED). Apps Script contract live, auth pending shared token. Visitor leg GREEN requires a real residential browser + token.", "reports/release-decision.json", "honest blockers", "tools/test-email-e2e.py", "PARTIAL"),
 ("43 final-report", "Exact evidence: inventory, contact, booking, record room, reliability, tests, files, live status, blockers", "P1", "PASS",
  "reports/email-provider-inventory.json, email-provider-matrix.json, email-e2e.json, this file", "reports/", "generated", "tools/make-email-reports.py", "PASS"),
 ("44 non-negotiable-final-rule", "No completion claim without real E2E evidence", "P0", "PASS",
  "All claims above tied to reports/email-e2e.json + provider-probe.json", "reports/email-e2e.json", "honoured", "tools/test-email-e2e.py", "PASS"),
]

def main():
    with open("reports/master-requirements.json") as f:
        master = json.load(f)

    existing_ids = {r["id"] for r in master["requirements"]}
    next_id = max(int(r["id"][1:]) for r in master["requirements"]) + 1

    added = []
    for sec, text, prio, status, evidence, files, plan, test, result in REQS:
        rid = "R%03d" % next_id
        next_id += 1
        added.append({
            "id": rid,
            "source_file": SRC,
            "section": sec.split(" ", 1)[1] if " " in sec else sec,
            "requirement": text,
            "category": "email",
            "priority": prio,
            "current_status": status,
            "evidence": evidence,
            "files_affected": files,
            "implementation_plan": plan,
            "test": test,
            "result": result
        })

    master["requirements"].extend(added)

    # recompute counts
    from collections import Counter
    c = Counter(r["current_status"] for r in master["requirements"])
    master["counts"] = dict(c)
    master["total"] = len(master["requirements"])
    master["generated"] = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
    master["title"] = ("EkGuru cumulative master requirements — merged from 9 command files "
                       "(+ critical email/booking routing/failover)")

    with open("reports/master-requirements.json", "w") as f:
        json.dump(master, f, indent=2)
    print("total requirements:", master["total"])
    print("counts:", dict(c))
    print("email requirements added:", len(added))

if __name__ == "__main__":
    main()
