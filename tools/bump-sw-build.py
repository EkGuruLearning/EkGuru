#!/usr/bin/env python3
"""
EkGuru — build-aware service-worker generation (tools/bump-sw-build.py)

The P0 rule: a reload must show the deployed build, never yesterday's
stylesheet, and a visitor must never need a hard refresh to get new work.

sw.js names its cache "ekguru-<BUILD_ID>". This tool rebuilds that ID from
the repository itself:

    <short-commit-sha>-v<generation>

so the cache name is unique per commit AND per build. The generation is a
monotonic counter in data/sw-generation.json; it moves on every run that
changes the ID, and it never moves twice for the same commit. sw.js's
activate handler already deletes every cache that is not the current
generation, so when the ID moves, the old copy is gone on the next launch —
online build wins over stale cache, and a normal reload is enough.

    python3 tools/bump-sw-build.py            # bump if needed
    python3 tools/bump-sw-build.py --check    # exit 1 if sw.js is stale

Idempotent: running it twice on the same commit changes nothing the second
time.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
os.chdir(ROOT)
SW = ROOT / "sw.js"
GEN = ROOT / "data" / "sw-generation.json"
# an old "/* BUILD: ... */" comment may sit directly on the line above —
# absorb it, or every bump would stack another comment
LINE_RE = re.compile(r"(?:^/\* BUILD: .* \*/\n)?^const BUILD_ID = \".*\";$", re.MULTILINE)


def short_sha():
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=10, cwd=ROOT)
        sha = out.stdout.strip()
        if sha and re.fullmatch(r"[0-9a-f]{4,40}", sha):
            return sha
    except Exception:
        pass
    return "nosha"


def load_gen():
    if GEN.exists():
        try:
            data = json.loads(GEN.read_text(encoding="utf-8"))
            if isinstance(data.get("generation"), int):
                return data
        except Exception:
            pass
    return {"generation": 0, "note": "monotonic SW cache generation — moved by tools/bump-sw-build.py"}


def main():
    check_only = "--check" in sys.argv[1:]
    sw = SW.read_text(encoding="utf-8")
    m = LINE_RE.search(sw)
    if not m:
        raise SystemExit("ERROR: sw.js: no const BUILD_ID line found")
    # the match may include the absorbed BUILD comment — compare the
    # const line itself, or the tool bumps on every run forever
    current = m.group(0).strip().splitlines()[-1].strip()

    sha = short_sha()
    data = load_gen()
    gen = data["generation"]

    # already on this commit at the current generation — nothing to do
    if current == 'const BUILD_ID = "%s-v%d";' % (sha, gen):
        if check_only:
            print("sw build id is current (%s)" % current)
        else:
            print("sw build id unchanged: %s" % current)
        return

    gen += 1
    new_line = 'const BUILD_ID = "%s-v%d";' % (sha, gen)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # the comment above the line records why the generation moved
    new_line = "/* BUILD: %s %s */\n%s" % (stamp, new_line.split('"')[1], new_line)
    sw = sw[:m.start()] + new_line + sw[m.end():]
    data["generation"] = gen
    data["last_bump"] = stamp
    if not check_only:
        SW.write_text(sw, encoding="utf-8")
        GEN.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("sw build id %s -> %s" % (current.split('"')[1], new_line.split('"')[1]))
    if check_only:
        print("STALE: sw.js build id does not match the working tree generation")
        sys.exit(1)


if __name__ == "__main__":
    main()
