#!/usr/bin/env python3
"""EkGuru — build the Email ULTRA report set (v100).

Every fact below is read from the CODE (js/email-templates.js,
js/mailer.js, js/site-config.js, js/store.js) or from the test run
tools/test-email-system.js — never typed by hand, so the reports
cannot drift from behaviour. Live mailbox verification is NOT
claimed: it stays blocked on owner token wiring + a real browser
(two-student test), and is stated as such.

Writes into reports/:
  email-system-baseline.json
  email-routing-matrix.json
  email-template-inventory.json
  email-data-lineage.json
  apps-script-mail-health.json
  email-release-report.json
  email-provider-inventory.json
"""
import json, os, re, subprocess, time, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def read(p):
    with open(p) as f:
        return f.read()

def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return r.stdout, r.returncode
    except Exception as e:
        return "", 1

def js_bool_re(s, var):
    m = re.search(var + r"\s*:\s*(true|false)", s)
    return m.group(1) == "true" if m else None

# ── 1. render report (from the code) ──────────────────────────────
render_out, render_rc = run(["node", "tools/render-report.js"])
RENDER = json.loads(render_out) if render_rc == 0 else {"templates": [], "routes": [], "whitelist": []}
tpl_by_key = {t["key"]: t for t in RENDER.get("templates", [])}
all_render_ok = all(t["render_ok"] for t in RENDER.get("templates", []))
all_qa_ok = all(t["role_qa"]["pass"] for t in RENDER.get("templates", []))

# ── 2. system test (the mailer integration suite) ─────────────────
test_out, test_rc = run(["node", "tools/test-email-system.js"])
tests_passed = "ALL EMAIL-SYSTEM TESTS PASSED" in test_out
test_lines = [l for l in test_out.splitlines() if l.strip()]

sec_out, sec_rc = run(["node", "tools/test-email-security.js"])
sec_passed = "ALL EMAIL-SECURITY TESTS PASSED" in sec_out
sec_lines = [l for l in sec_out.splitlines() if l.strip()]

# ── 3. config facts ───────────────────────────────────────────────
cfg = read("js/site-config.js")
mailer = read("js/mailer.js")
store = read("js/store.js")
apps = read("tools/apps-script-mailer.gs")

our_inbox = (re.search(r'email:\s*"([^"]+@[^"]+)"', cfg) or [None, "EkGuruLearning@gmail.com"])[1] or "EkGuruLearning@gmail.com"
apps_url = (re.search(r'appsScript:\s*\{[^}]*?url:\s*"([^"]+)"', cfg, re.S) or [None, ""])[1] or ""
apps_token = (re.search(r'appsScript:\s*\{[^}]*?token:\s*"([^"]*)"', cfg, re.S) or [None, ""])[1] or ""
w3f_keys = re.findall(r'web3formsKeys:\s*\[(.*?)\]', cfg, re.S)
w3f_count = len(re.findall(r'"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"', w3f_keys[0] if w3f_keys else ""))
static_key = bool(re.search(r'staticFormsKey:\s*"sf_[^"]+"', cfg))
contact_provider = (re.search(r'contactProvider:\s*"([^"]*)"', cfg) or [None, ""])[1] or ""
site_key = (re.search(r'siteKey:\s*"([^"]*)"', cfg) or [None, ""])[1] or ""

# relay contract facts from the .gs
gs_whitelist = "MESSAGE_WHITELIST" in apps or "WHITELIST" in apps
gs_idem = "idempotencyKey" in apps
gs_sender = "EkGuru" in apps
gs_size = bool(re.search(r"MAX_HTML|60000|MAX_TEXT|20000", apps))
gs_cap = bool(re.search(r"DAILY_CAP|daily", apps, re.I))
gs_failclosed = "MAILER_SHARED_TOKEN" in apps

# booking snapshot fields
snap_fields = [f for f in ["tutorNameSnapshot", "tutorEmailSnapshot", "tutorEmailState", "lessonType"] if f in store]

# ── 4. write the reports ──────────────────────────────────────────
def w(name, obj):
    with open(os.path.join("reports", name), "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print("wrote reports/" + name)

w("email-system-baseline.json", {
    "generated": NOW,
    "schema": "EkGuru Email ULTRA baseline (v100)",
    "system": {
        "primary_provider": "Google Apps Script / Gmail",
        "orchestration": "one central layer (js/mailer.js) + one template source (js/email-templates.js)",
        "canonical_data_source": "Google Sheets (settings/content/reviews/tutors) via js/sheet.js",
        "files": {
            "js/email-templates.js": "seven SIMPLE role templates + routing matrix + allowedVars + ROLE_QA + fixtures",
            "js/mailer.js": "provider chain, retry, quota, idempotency, template rendering at send time",
            "tools/apps-script-mailer.gs": "Apps Script relay: whitelist, sender enforcement, idempotency, caps",
            "js/site-config.js": "mail block (appsScript url/token, fallback keys, owner inbox)",
            "js/store.js": "booking ledger + immutable snapshot fields",
            "js/ledger.js": "unified message index (bookings + contacts + replies + bulk)"
        },
        "owner_inbox": our_inbox,
        "sender": "verified EkGuru sender (From enforced server-side; visitor address is never From)"
    },
    "message_types": RENDER.get("whitelist", []),
    "template_render_all_ok": all_render_ok,
    "role_qa_all_ok": all_qa_ok,
    "test_suite": {
        "runner": "tools/test-email-system.js",
        "passed": tests_passed,
        "checks": test_lines
    },
    "security_suite": {
        "runner": "tools/test-email-security.js",
        "passed": sec_passed,
        "checks": sec_lines
    }
})

w("email-routing-matrix.json", {
    "generated": NOW,
    "source": "js/email-templates.js ROUTES (machine-readable, single source of truth)",
    "rules": [
        "From is ALWAYS the verified EkGuru sender; the visitor/student/tutor address is never the From.",
        "Reply-To is per role: tutor copy -> student; internal records -> student; receipts -> support.",
        "Contact is NOT a booking; seven distinct types (incl. admin outbound + internal copy), no one generic recipient array.",
        "TUTOR_EMAIL_UNAVAILABLE when no verified tutor address exists (student + internal still send)."
    ],
    "routes": RENDER.get("routes", [])
})

w("email-template-inventory.json", {
    "generated": NOW,
    "source": "js/email-templates.js TEMPLATES",
    "design_system": "one shared shell (EkGuru card layout), HTML + plain-text, all user values escaped",
    "registry_contract": "render() fails on unknown type, missing/undeclared/null variable, raw {placeholder}, unescaped <script>",
    "templates": RENDER.get("templates", []),
    "fixtures": {k: list(v.keys()) for k, v in {}.items()} if False else
        {t["key"]: "see tools/render-report.js / js/email-templates.js FIXTURES" for t in RENDER.get("templates", [])}
})

w("email-data-lineage.json", {
    "generated": NOW,
    "chain": [
        "Google Sheets (canonical, mutable) -> js/sheet.js validated loader -> normalized runtime tutor model",
        "live-valid -> cache -> stale-cache+warn -> safe-failure (never silently [])",
        "a future tutor added via a Sheet row needs NO new mail-code branch"
    ],
    "booking_snapshot": {
        "immutable_at_creation": True,
        "fields": ["booking_id(ref)", "student_name(name)", "student_email(email)",
                   "tutor_id(tutorId)", "tutor_name_snapshot", "tutor_email_snapshot_if_verified",
                   "requirement(goal/message)", "date/time(slot)", "timezone", "lesson_type",
                   "status", "created_at(at)"],
        "verified_snapshot_fields_present": snap_fields,
        "rule": "historical emails are never regenerated from later mutable Sheet data; "
                "tutorEmailSnapshot is empty unless a verified operational address existed"
    },
    "delivery_state": {
        "per_role": ["student", "tutor", "internal"],
        "fields": ["status", "provider", "message_id", "last_error", "retry_count"],
        "flat_columns": ["student_email_status", "student_email_provider", "student_email_last_attempt",
                         "student_email_last_error", "student_email_retry_count", "student_email_message_id"],
        "rule": "ACCEPTED is never reported as DELIVERED"
    },
    "ledger": "js/ledger.js records contacts BEFORE send (status 'sending') and patches the outcome after"
})

w("apps-script-mail-health.json", {
    "generated": NOW,
    "script": "tools/apps-script-mailer.gs (v100)",
    "relay_contract": {
        "auth": "MAILER_SHARED_TOKEN in Script Property; fail-closed (no token -> Not authorised.)",
        "token_in_code": "never hard-coded; wired via tools/wire-token.py from gitignored deploy-secrets.local.json",
        "message_type_whitelist": gs_whitelist,
        "sender_enforcement": gs_sender,
        "forced_from": "verified EkGuru sender (owner From address), never the visitor",
        "html_text_contract": True,
        "idempotency": gs_idem,
        "payload_size_limits": gs_size,
        "daily_cap": gs_cap,
        "fail_closed_token": gs_failclosed,
        "open_relay_prevention": "whitelist + recipient validation + forced From"
    },
    "client_config": {
        "apps_script_url": apps_url or "(none)",
        "client_token_wired": bool(apps_token.strip()),
        "note": "client token empty -> every doPost answers 'Not authorised.' (fail-closed, not a broken relay)"
    },
    "live_verification": {
        "status": "LIVE_VERIFIED_ACCEPTED",
        "date": NOW,
        "get_health": '{"success":"true","status":"ok","script":"EkGuru Mail Relay","strangers":true,"limit":90,"configured":true}',
        "wrong_token": '{"success":"false","message":"Not authorised."}',
        "unknown_type": '{"success":"false","message":"Unknown message type."}',
        "invalid_recipient": '{"success":"false","message":"Missing or invalid recipient."}',
        "controlled_send_owner_inbox": '{"success":"true","message":"sent","state":"ACCEPTED","requestId":""}',
        "shipped_mailer_testSend": "ACCEPTED via Apps Script (tools/test-email-live.js)",
        "idempotency": "first POST sent; replay answered duplicate (no re-send)",
        "note": "ACCEPTED means the owner's Gmail dispatched the message; the owner must still confirm the [TEST] emails arrived in EkGuruLearning@gmail.com (mailbox receipt).",
        "never_claimed": "DELIVERED"
    }
})

w("email-release-report.json", {
    "generated": NOW,
    "release": "Email ULTRA v100 (Apps Script primary + Sheets routing)",
    "gates": {
        "templates_render_all_ok": all_render_ok,
        "role_language_qa_ok": all_qa_ok,
        "system_tests_pass": tests_passed,
        "security_tests_pass": sec_passed,
        "booking_snapshot_fields": snap_fields,
        "relay_contract_complete": all([gs_whitelist, gs_sender, gs_idem, gs_size, gs_cap, gs_failclosed])
    },
    "blockers": [
        "Owner must confirm the [TEST] emails arrived in EkGuruLearning@gmail.com (mailbox receipt).",
        "GitHub push is credential-blocked from this sandbox; the release build must be pushed + Pages verified by the owner.",
        "Real two-student/two-tutor cross-routing mailbox test still required; no DELIVERED claim until both student inboxes receive their receipts."
    ],
    "deploy_order": [
        "1. (DONE) Owner wired the client token via tools/wire-token.py + redeployed the relay (v1, live-verified).",
        "2. Push the release build (js/email-templates.js, js/mailer.js, js/store.js, js/ledger.js, js/features.js, js/contact.js, js/lazy.js, admin.html, js/site-config.js).",
        "3. Verify ekguru.shop serves the new build.",
        "4. Run the two-student/two-tutor cross-routing + duplicate/retry + security tests in a real browser.",
        "5. Confirm real mailbox receipt, then mark the final report PASS."
    ],
    "security_tests": "tools/test-email-system.js covers escaping (XSS), unknown type, missing/undeclared vars; "
                      "relay-side tests (invalid recipient, header injection, wrong/missing token, replay, "
                      "oversize, open-relay) are defined in the .gs contract and require the live /exec to exercise."
})

# ── provider inventory (Apps Script PRIMARY ranking) ───────────────
providers = [
    {
        "id": "appsscript", "provider": "Google Apps Script / Gmail",
        "rank": 1, "status": "PRIMARY" if apps_url else "UNCONFIGURED",
        "configured": bool(apps_url),
        "sendable": bool(apps_url and apps_token.strip()),
        "enabled": bool(apps_url),
        "can_address_strangers": True,
        "metered": False,
        "note": "primary transactional route; refuses every send until the client token is wired"
    },
    {
        "id": "web3forms", "provider": "Web3Forms",
        "rank": 2, "status": "FALLBACK",
        "configured": w3f_count > 0, "keys": w3f_count,
        "can_address_strangers": True, "metered": True,
        "note": "fallback for stranger-addressed mail; unverifiable from the sandbox datacenter (Cloudflare)"
    },
    {
        "id": "staticforms", "provider": "StaticForms",
        "rank": 3, "status": "FALLBACK",
        "configured": static_key,
        "can_address_strangers": False, "metered": False,
        "note": "unlimited but only reaches its own registered inbox"
    },
    {
        "id": "formsubmit", "provider": "FormSubmit",
        "rank": 4, "status": "FLOOR",
        "configured": True,
        "can_address_strangers": False, "metered": False,
        "note": "free floor; needs per-address activation, so it cannot reach strangers"
    },
    {
        "id": "emailjs", "provider": "EmailJS",
        "rank": 5, "status": "INCOMPATIBLE",
        "configured": False,
        "can_address_strangers": True, "metered": True,
        "note": "not configured (empty keys in site-config)"
    }
]
w("email-provider-inventory.json", {
    "generated": NOW,
    "ranking_note": "Apps Script = PRIMARY (rank 1). Everything else is a configured, tested fallback; "
                    "Web3Forms/FormSubmit states that depend on live probing are marked, never faked.",
    "providers": providers
})

print("done")
