#!/usr/bin/env python3
"""EkGuru — wire the Apps Script mail token into the client (v99).

WHY THIS EXISTS
---------------
The owner's Apps Script relay is fail-closed: doPost() refuses mail
until the client's `mail.appsScript.token` matches the server-side
Script Property MAILER_SHARED_TOKEN. That token is a shared value the
owner mints ONCE (run mintToken() in the Apps Script editor), and it
must land in js/site-config.js at deploy time.

The problem this tool solves: after every `git pull` / site update,
site-config.js ships with `token: ""` again, and the owner would have
to re-paste the token by hand every single time — and forget once, and
the student's booking receipt silently loses its verified route.

The durable pattern:
  · the token lives in ONE file the owner controls: deploy-secrets.local.json
    (gitignored — never committed, never uploaded)
  · this script re-injects it into js/site-config.js, idempotently,
    after any update
  · tools/release-decision.js flags STUDENT_EMAIL: BLOCKED_ON_TOKEN
    until the token is wired, so it can never be forgotten silently

USAGE
-----
  1. One time:  echo '{"mailerToken": "PASTE_VALUE_HERE"}' > deploy-secrets.local.json
     (Get the value from the Apps Script editor → Project Settings →
      Script Properties → MAILER_SHARED_TOKEN.)
  2. After every update / before every deploy:
       python3 tools/wire-token.py
  3. Verify:  python3 tools/wire-token.py --check

The token is a deploy-time credential. A static browser bundle cannot keep
it confidential after deployment, but it must never be committed to source
control, copied into reports, or printed by diagnostics. The relay must also
enforce server-side authorization, origin checks, validation, and rate limits.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS = os.path.join(ROOT, "deploy-secrets.local.json")
CONFIG = os.path.join(ROOT, "js", "site-config.js")


def read_token():
    if not os.path.exists(SECRETS):
        return None
    try:
        with open(SECRETS, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("deploy-secrets.local.json is not valid JSON:", e)
        return None
    tok = (data or {}).get("mailerToken") or (data or {}).get("MAILER_SHARED_TOKEN")
    return str(tok).strip() if tok else None


def current_token():
    with open(CONFIG, "r", encoding="utf-8") as f:
        src = f.read()
    m = re.search(r"token:\s*\"([^\"]*)\"", src)
    return m.group(1) if m else None


def main():
    # --help / -h is informational only: no file reads, no writes, no secrets.
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python3 tools/wire-token.py [--check | --help]")
        print("Default: copy mailerToken from gitignored deploy-secrets.local.json")
        print("into js/site-config.js for deploy. Do NOT commit the wired file.")
        print("  --check   report EMPTY or WIRED; does not print the token; does not write")
        print("  --help    this message (does not read or write anything)")
        return 0

    if "--check" in sys.argv:
        # This is deliberately machine-readable and reveals no credential
        # metadata. Do not add paths, lengths, prefixes, or hints here.
        print("WIRED" if current_token() else "EMPTY")
        return 0

    tok = read_token()
    if not tok:
        print("No token found. Create deploy-secrets.local.json with")
        print('  {"mailerToken": "PASTE_VALUE_HERE"}')
        print("(value from Apps Script editor → Project Settings → Script Properties → MAILER_SHARED_TOKEN)")
        return 1

    with open(CONFIG, "r", encoding="utf-8") as f:
        src = f.read()

    if not re.search(r"token:\s*\"", src):
        print("Could not find the token field in js/site-config.js — aborting.")
        return 1

    new_src, n = re.subn(r"(token:\s*)\"[^\"]*\"", lambda m: m.group(1) + json.dumps(tok), src)
    if n == 0:
        print("No token assignment matched — aborting (no change made).")
        return 1

    with open(CONFIG, "w", encoding="utf-8") as f:
        f.write(new_src)

    print("Wired the token into js/site-config.js (%d assignment%s)." % (n, "" if n == 1 else "s"))
    print("REMINDER: the token now sits in a tracked file. Do NOT commit it.")
    print("Before deploying, run: python3 tools/release-decision.js  (STUDENT_EMAIL must not say BLOCKED_ON_TOKEN)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
