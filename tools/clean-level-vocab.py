#!/usr/bin/env python3
"""EkGuru — clean vocabulary entries in the level course data.

WHAT IS CLEANED AND WHY
-----------------------
A generator run left some C1/C2 (and a few B1/B2) vocabulary entries that are
not words at all: comma-split fragments of a running sentence
("وفقًا للتقرير،" — "according to the report,"), whose "translation" is
"discourse segment N in '...'". A learner who opens a C1 page sees those and
the level stops being trusted. This tool, run over every level JSON:

  · drops entries whose translation is "discourse segment N in ..." —
    generator filler, not a vocabulary item;
  · strips edge commas/semicolons/colons/quotes from the word and its
    romanisation (a comma at the edge of a "word" is a sentence fragment;
    terminal . ! ? are legitimate and are NEVER touched);
  · drops entries that come out empty;
  · removes exact duplicate entries inside a single lesson's list
    (the same word repeated across lessons is intentional review and is
    left alone);
  · drops srs_candidates that are those fragments (by exact text match with
    a dropped discourse entry, or by edge-comma) so review decks do not
    drill sentence pieces.

Everything else is untouched. Files are re-serialised with the exact format
the repo already uses (indent=2, ensure_ascii=False, trailing newline), so a
clean file comes out byte-identical.

Run:  python3 tools/clean-level-vocab.py [--check]
      --check reports what would change without writing anything.
Report:  data/audit/clean-level-vocab.json
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
REPORT = "data/audit/clean-level-vocab.json"

DISCOURSE = re.compile(r"discourse segment \d+ in")
# Edge characters that can never end a real word: commas, semicolons,
# colons, dashes between words, and quotation marks. Periods, ! and ? stay —
# they end complete example sentences, which are legitimate list entries.
EDGE = set(" ,،؛;:”“”‘’\"'")


def clean_text(t):
    s = t
    while s and s[0] in EDGE:
        s = s[1:]
    while s and s[-1] in EDGE:
        s = s[:-1]
    return s


def collect_discourse(d):
    """Pass 1: the text of every discourse-filler entry, raw and stripped.
    These exact strings also appear in srs_candidates and must go with it."""
    out = set()
    def walk(o):
        if isinstance(o, dict):
            if "t" in o and isinstance(o.get("t"), str) \
                    and isinstance(o.get("en"), str) and DISCOURSE.search(o["en"]):
                out.add(o["t"].strip())
                out.add(clean_text(o["t"]).strip())
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(d)
    return out


def process(d, discourse_words=None):
    """Clean the level data in place. Returns a stats dict."""
    stats = {"dropped_discourse": 0, "stripped": 0, "dropped_empty": 0,
             "deduped_in_list": 0, "dropped_srs": 0}
    stats["vocab_entries"] = 0
    discourse_words = discourse_words or set()

    def walk(o):
        if isinstance(o, dict):
            # A vocabulary entry: a dict with a text field "t".
            if "t" in o and isinstance(o.get("t"), str):
                stats["vocab_entries"] += 1
                if isinstance(o.get("en"), str) and DISCOURSE.search(o["en"]):
                    stats["dropped_discourse"] += 1
                    return "drop"
                t = o["t"]
                cleaned = clean_text(t)
                if cleaned != t:
                    o["t"] = cleaned
                    stats["stripped"] += 1
                r = o.get("r")
                if isinstance(r, str) and r:
                    rcleaned = clean_text(r)
                    if rcleaned != r:
                        o["r"] = rcleaned
                if not o.get("t", "").strip():
                    stats["dropped_empty"] += 1
                    return "drop"
                return "keep"
            for k, v in list(o.items()):
                if isinstance(v, list):
                    kept = []
                    seen = set()
                    for item in v:
                        if isinstance(item, dict) and "t" in item \
                                and isinstance(item.get("t"), str):
                            action = walk(item)
                            if action == "drop":
                                continue
                            key = (item.get("t", "").strip(),
                                   item.get("r", "").strip(),
                                   item.get("en", "").strip())
                            if key in seen:
                                stats["deduped_in_list"] += 1
                                continue
                            seen.add(key)
                        elif isinstance(item, str) and k == "srs_candidates":
                            s = item.strip()
                            if (not s or s in discourse_words
                                    or s[0] in EDGE or s[-1] in EDGE):
                                stats["dropped_srs"] += 1
                                continue
                            if s in seen:
                                stats["deduped_in_list"] += 1
                                continue
                            seen.add(s)
                        else:
                            walk(item)
                        kept.append(item)
                    v[:] = kept
                    continue
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        return None

    walk(d)
    return stats


def main():
    check = "--check" in sys.argv
    files = sorted(glob.glob("data/courses/phase-*/*_[A-Z][0-9].json"))
    total = {"files": len(files), "files_changed": 0, "lessons": 0,
             "vocab_entries": 0, "dropped_discourse": 0, "stripped": 0,
             "dropped_empty": 0, "deduped_in_list": 0, "dropped_srs": 0}
    detail = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            raw = fh.read()
        d = json.loads(raw)
        for u in (d.get("level") or {}).get("units", []):
            total["lessons"] += len(u.get("lessons", []))
        stats = process(d, collect_discourse(d))
        out = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
        changed = out != raw
        for k in ("vocab_entries", "dropped_discourse", "stripped",
                  "dropped_empty", "deduped_in_list", "dropped_srs"):
            total[k] += stats[k]
        if changed:
            total["files_changed"] += 1
            detail.append({"file": f, **{k: stats[k] for k in
                        ("dropped_discourse", "stripped", "dropped_empty",
                         "deduped_in_list", "dropped_srs")}})
            if not check:
                with open(f, "w", encoding="utf-8") as fh:
                    fh.write(out)

    print("files scanned: %d  changed: %d  lessons: %d  vocab entries: %d"
          % (total["files"], total["files_changed"], total["lessons"],
             total["vocab_entries"]))
    print("dropped discourse-filler: %d  stripped edge punctuation: %d  "
          "dropped empty: %d  deduped in-list: %d  dropped srs fragments: %d"
          % (total["dropped_discourse"], total["stripped"],
             total["dropped_empty"], total["deduped_in_list"],
             total["dropped_srs"]))

    report = {"tool": "tools/clean-level-vocab.py",
              "mode": "check" if check else "apply",
              "files_scanned": total["files"], "files_changed": total["files_changed"],
              "lessons": total["lessons"], "vocab_entries": total["vocab_entries"],
              "dropped_discourse": total["dropped_discourse"],
              "stripped_edge_punctuation": total["stripped"],
              "dropped_empty": total["dropped_empty"],
              "deduped_in_list": total["deduped_in_list"],
              "dropped_srs": total["dropped_srs"],
              "files": detail}
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("report: %s" % REPORT)
    return 1 if (total["files_changed"] and check) else 0


if __name__ == "__main__":
    sys.exit(main())
