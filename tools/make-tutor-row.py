#!/usr/bin/env python3
"""EkGuru — build the LOCAL paste-ready CSV row for one tutor.

    python3 tools/make-tutor-row.py sarshtee-baliyan --email her@example.com

Why this exists
---------------
`csv/ekguru_tutors.csv` is the committed, schema-exact upload pack. It is the
file that gets imported into the tutors tab, and it is published in the
repository — so a tutor's personal inbox must never be in it.

The booking inbox lives in the sheet's `notification_email` column, which is
the canonical one: `js/sheet.js` keeps it separate from the legacy `email`
column precisely because `email` is the value that used to be printed on a
public page. So the pack ships with `notification_email` blank and this tool
writes the row you actually paste, into a file that is not committed:

    csv/<id>-row.local.csv        header row
                                  the sheet's own #help row
                                  the tutor's row, with the address filled in

`.gitignore` covers `*.local.csv`, and `tools/privacy.js` treats a personal
address in a tracked file as a leak, so the two agree: the address belongs in
the spreadsheet and on the owner's disk, never in Git. The file is ignored on
purpose — if it is gone, run this command again with the same address.
"""

import argparse
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PACK = os.path.join("csv", "ekguru_tutors.csv")
PRIVATE_COLUMNS = ("notification_email", "email")


def main():
    ap = argparse.ArgumentParser(description="build a local, uncommitted tutor row")
    ap.add_argument("tutor_id", help="the id in the pack's first column, e.g. sarshtee-baliyan")
    ap.add_argument("--email", help="the tutor's booking inbox (notification_email)")
    ap.add_argument("--out", help="output file (default csv/<id>-row.local.csv)")
    args = ap.parse_args()

    with open(PACK, encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        sys.exit(f"{PACK} is empty")

    header, body = rows[0], rows[1:]
    try:
        col = header.index("notification_email")
    except ValueError:
        sys.exit("the pack has no notification_email column — is it the 48-column sheet pack?")

    mine = [r for r in body if r and r[0].strip() == args.tutor_id.strip()]
    if not mine:
        ids = [r[0] for r in body if r and not r[0].startswith("#")]
        sys.exit(f"no row for {args.tutor_id!r} in {PACK} — ids there: {', '.join(ids)}")
    row = list(mine[0])

    if args.email:
        row[col] = args.email.strip()
    elif not row[col]:
        print(f"note: {args.tutor_id} has no notification_email yet — bookings fall back to "
              "the site inbox (TUTOR_EMAIL_UNAVAILABLE in js/sheet.js). Pass --email to fill it.",
              file=sys.stderr)

    # the sheet's own #help row travels with the header so the pasted block
    # lines up with the live tab exactly as it is
    help_row = next((r for r in body if r and r[0].startswith("#help")), None)
    out_rows = [header] + ([help_row] if help_row else []) + [row]

    out = args.out or os.path.join("csv", f"{args.tutor_id}-row.local.csv")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        csv.writer(fh, quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n").writerows(out_rows)

    filled = ", ".join(f"{c}={row[header.index(c)] or '(blank)'}"
                       for c in PRIVATE_COLUMNS if c in header)
    print(f"wrote {out}  ({len(out_rows)} rows × {len(header)} columns)")
    print(f"  {args.tutor_id}: {filled}")
    print("  not committed — `*.local.csv` is git-ignored on purpose (see the docstring).")


if __name__ == "__main__":
    main()
