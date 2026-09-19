#!/usr/bin/env python3
"""EkGuru — build the LOCAL, paste-ready tutors CSV for the Google Sheet.

    python3 tools/make-tutor-row.py sarshtee-baliyan --email her@example.com
    python3 tools/make-tutor-row.py sarshtee-baliyan --email her@example.com --full

Why this exists
---------------
`csv/ekguru_tutors.csv` is the committed, schema-exact upload pack. It is
published in the repository — so a tutor's personal inbox must never be in it.
The booking inbox lives in the sheet's `notification_email` column, which is
the canonical one: `js/sheet.js` keeps it separate from the legacy `email`
column precisely because `email` is the value that used to be printed on a
public page.

So this tool writes the file you actually hand to Google Sheets, and it is not
committed (`*.local.csv` is in `.gitignore`; `tools/privacy.js` treats a
personal address in a tracked file as a leak — the two agree).

Two shapes, one per way of importing:

  default     csv/<id>-row.local.csv
                header + the sheet's own #help row + the tutor's row
                → File ▸ Import ▸ Upload ▸ *Insert new sheet(s)*: it lands as
                  its own tab, columns already split, ready to copy across

  --full      csv/ekguru_tutors.local.csv
                the whole tutors tab, every row, in sheet order
                → select A1 in the tutors tab, then File ▸ Import ▸ Upload ▸
                  *Replace data at selected cell*: no other tab is touched

The base for `--full` is `live-sheets/tutors.csv` — the copy of the owner's
current tab, which is what the site validates against. Building from the live
tab rather than the pack is deliberate: the pack is a fresh-workbook file, and
two of its cells disagree with the live tab on purpose or by accident
(`hemlata`/`tara` are `active=no` live, and tara's production `videoTitle` has
a pasted methodology block the loader refuses). Replacing a live tab with the
pack would silently un-hide two tutors. With `--full` only the new row appears.
"""

import argparse
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PACK = os.path.join("csv", "ekguru_tutors.csv")
LIVE = os.path.join("live-sheets", "tutors.csv")
FULL_OUT = os.path.join("csv", "ekguru_tutors.local.csv")
PRIVATE_COLUMNS = ("notification_email", "email")


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))


def write_csv(path, rows, cols):
    for r in rows:
        if len(r) != cols:
            sys.exit(f"refusing to write {path}: a row has {len(r)} columns, expected {cols}")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        csv.writer(fh, quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n").writerows(rows)


def main():
    ap = argparse.ArgumentParser(description="build a local, uncommitted tutors CSV")
    ap.add_argument("tutor_id", help="the id in the first column, e.g. sarshtee-baliyan")
    ap.add_argument("--email", help="the tutor's booking inbox (notification_email)")
    ap.add_argument("--full", action="store_true",
                    help="write the whole tutors tab (csv/ekguru_tutors.local.csv) "
                         "instead of just the one row")
    ap.add_argument("--base", help=f"row source other than {PACK}")
    ap.add_argument("--out", help="output file")
    args = ap.parse_args()

    pack = read_csv(PACK)
    if not pack:
        sys.exit(f"{PACK} is empty")
    header = pack[0]
    try:
        col = header.index("notification_email")
    except ValueError:
        sys.exit("no notification_email column — is this the 48-column tutors pack?")

    mine = [r for r in pack[1:] if r and r[0].strip() == args.tutor_id.strip()]
    if not mine:
        ids = [r[0] for r in pack[1:] if r and not r[0].startswith("#")]
        sys.exit(f"no row for {args.tutor_id!r} in {PACK} — ids there: {', '.join(ids)}")
    row = list(mine[0])

    if args.email:
        row[col] = args.email.strip()
    elif not row[col]:
        print(f"note: {args.tutor_id} has no notification_email yet — booking mail falls back "
              "to the site inbox (the honest TUTOR_EMAIL_UNAVAILABLE path in js/sheet.js). "
              "Pass --email to fill it.", file=sys.stderr)

    if args.full:
        base_path = args.base or (LIVE if os.path.exists(LIVE) else PACK)
        base = read_csv(base_path)
        if base[0] != header:
            sys.exit(f"{base_path} has a different header from {PACK} — not safe to merge")
        body = base[1:]
        if any(r and r[0].strip() == row[0] for r in body):
            print(f"note: {row[0]} is already in {base_path} — replacing that row, not duplicating it.")
            body = [r for r in body if not (r and r[0].strip() == row[0])]
        help_row = next((r for r in body if r and r[0].startswith("#help")), None)
        rest = [r for r in body if not (r and r[0].startswith("#help"))]
        out_rows = [header] + ([help_row] if help_row else []) + rest + [row]
        out = args.out or FULL_OUT
        write_csv(out, out_rows, len(header))
        print(f"wrote {out}  ({len(out_rows)} rows × {len(header)} columns, base: {base_path})")
        print(f"  tutors: {', '.join(r[0] for r in out_rows[2:])}")
        print("  Import: in the tutors tab select A1, then File ▸ Import ▸ Upload ▸ "
              "*Replace data at selected cell*.")
        print("          Other tabs are untouched; this tab's 7 rows land in A1 on top of the old ones.")
        missing = [r[0] for r in out_rows[2:] if not r[col]]
        if missing:
            print(f"  no booking inbox for: {', '.join(missing)} — their requests go to the "
                  "EkGuru inbox until a cell is filled.", file=sys.stderr)
    else:
        # the sheet's own #help row travels with the header so the pasted block
        # lines up with the live tab exactly as it is
        help_row = next((r for r in pack[1:] if r and r[0].startswith("#help")), None)
        out_rows = [header] + ([help_row] if help_row else []) + [row]
        out = args.out or os.path.join("csv", f"{args.tutor_id}-row.local.csv")
        write_csv(out, out_rows, len(header))
        print(f"wrote {out}  ({len(out_rows)} rows × {len(header)} columns)")
        print("  Import: File ▸ Import ▸ Upload ▸ *Insert new sheet(s)* — it arrives as its own tab")
        print("          with the columns already split; copy the last row into the tutors tab.")
        print("          (Do not paste the raw line: Sheets splits on tabs, not commas.)")

    filled = ", ".join(f"{c}={row[header.index(c)] or '(blank)'}"
                       for c in PRIVATE_COLUMNS if c in header)
    print(f"  {args.tutor_id}: {filled}")
    print("  not committed — `*.local.csv` is git-ignored on purpose (see the docstring).")


if __name__ == "__main__":
    main()
