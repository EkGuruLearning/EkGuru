#!/usr/bin/env python3
"""EkGuru — direct live probe of every mail provider, from a REAL browser context.

This is the ground-truth half of the provider inventory: it POSTs real requests
to each provider endpoint exactly as js/mailer.js would, and records the raw
response. It does NOT route through the site's own code, so it shows what the
providers themselves actually do today (11 Sep 2026).

For FormSubmit we use fetch() from inside a served page so the request carries
a real http(s) Origin — the same thing the real site does. curl cannot do this
and FormSubmit rejects curl with its "web server" message.

Output: reports/provider-probe.json
"""
import json, time, os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
OUR_INBOX = "EkGuruLearning@gmail.com"
STRANGER = "never-a-real-person-20260911@example.com"
STUDENT = "EkGuruLearning+student-test@gmail.com"

W3F_KEYS = {
    "legacy web3formsKey": "5ad4a9a6-fcb2-445c-9764-cab8c99fadfa",
    "key1 abc520f5": "abc520f5-f682-4225-9810-266bac004cd6",
    "key2 50855e6f": "50855e6f-ffcd-4956-b6b1-8802eb8840e1",
    "key3 8d80b297": "8d80b297-9f6d-42d3-8865-d4883e264021",
    "key4 83fd80d7": "83fd80d7-9ab4-4116-9082-685433861376",
}
STATIC_KEY = "sf_cfb12602e030b67320c6f99e"

out = {"generated": None, "probes": {}}

def run():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context()
        pg = ctx.new_page()
        pg.goto(BASE + "/contact/", wait_until="domcontentloaded", timeout=30000)
        pg.wait_for_timeout(1200)

        def fetch_post(url, body, extra_headers=None):
            """fetch POST from inside the page context; returns {status, body}."""
            js = """
            async (arg) => {
              try {
                const res = await fetch(arg.u, {
                  method: "POST",
                  headers: Object.assign({"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}, arg.hd||{}),
                  body: arg.bd
                });
                const txt = await res.text();
                return { status: res.status, body: txt.slice(0, 500) };
              } catch (e) {
                return { status: -1, body: "FETCH ERROR: " + e.message };
              }
            }
            """
            return pg.evaluate(js, {"u": url, "bd": body, "hd": extra_headers or {}})

        def qs(d):
            from urllib.parse import urlencode
            return urlencode(d)

        # 1. FormSubmit — our inbox
        out["probes"]["formsubmit_our_inbox"] = fetch_post(
            "https://formsubmit.co/ajax/" + OUR_INBOX,
            qs({"name": "Provider Probe", "message": "probe", "_captcha": "false",
                "_subject": "E2E provider probe: formsubmit our inbox"}))
        # 2. FormSubmit — stranger
        out["probes"]["formsubmit_stranger"] = fetch_post(
            "https://formsubmit.co/ajax/" + STRANGER,
            qs({"name": "Provider Probe", "message": "probe", "_captcha": "false"}))
        # 3. FormSubmit — student alias (gmail +alias)
        out["probes"]["formsubmit_student_alias"] = fetch_post(
            "https://formsubmit.co/ajax/" + STUDENT,
            qs({"name": "Provider Probe", "message": "probe", "_captcha": "false",
                "_subject": "E2E provider probe: formsubmit student alias"}))

        # 4. StaticForms — our inbox (registered address)
        out["probes"]["staticforms"] = fetch_post(
            "https://api.staticforms.dev/submit",
            qs({"accessKey": STATIC_KEY, "subject": "E2E provider probe: staticforms",
                "name": "EkGuru", "email": OUR_INBOX, "message": "probe", "honeypot": ""}))

        # 5. Web3Forms — each key, real submit (delivers to the account's
        #    registered inbox; a distinctive subject marks each one)
        for label, key in W3F_KEYS.items():
            out["probes"]["web3forms_" + label] = fetch_post(
                "https://api.web3forms.com/submit",
                qs({"access_key": key, "name": "EkGuru E2E", "email": OUR_INBOX,
                    "subject": "E2E provider probe: " + label,
                    "message": "Provider inventory probe."}))

        b.close()

    out["generated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    os.makedirs("reports", exist_ok=True)
    with open("reports/provider-probe.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))

if __name__ == "__main__":
    run()
