#!/usr/bin/env python3
"""EkGuru — tutor card photo variants.

Tutor cards (js/main.js tutorCard, tools/build-home-tutors.js) serve
square 176px/264px variants (`<name>-176.jpg`, `<name>-264.jpg`,
plus WebP twins) so an 88px card does not download the full photo.
A tutor whose variants were never generated gets 404 srcset
candidates and a broken/placeholder card — that is how Pinky Kumari's
card shipped (only the 1104px original existed).

Run:  python3 tools/build-tutor-photo-variants.py [--check]
Needs: Pillow (pip install pillow). Square centre-top crop, matching
object-position 50% 32% in the card CSS.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIZES = (176, 264)


def variants_for(src: Path):
    base = src.with_suffix("")
    out = []
    for n in SIZES:
        out.append(Path(str(base) + f"-{n}.jpg"))
        out.append(Path(str(base) + f"-{n}.webp"))
    return out


def tutor_photos():
    photos = []
    for f in sorted((ROOT / "js" / "tutors").glob("*.js")):
        if f.name.startswith("_"):
            continue
        for line in f.read_text(encoding="utf8", errors="ignore").splitlines():
            line = line.strip()
            if line.startswith("photo:"):
                m = re.search(r'"([^"]+)"', line) or re.search(r"'([^']+)'", line)
                rel = m.group(1) if m else ""
                if rel and not rel.startswith("http"):
                    photos.append(ROOT / rel)
                break
    return photos


def make(src: Path):
    from PIL import Image
    im = Image.open(src).convert("RGB")
    w, h = im.size
    side = min(w, h)
    x = (w - side) // 2
    y = max(0, int(h * 0.32 - side / 2)) if h > w else (h - side) // 2
    y = min(y, h - side)
    crop = im.crop((x, y, x + side, y + side))
    for out in variants_for(src):
        n = int(out.stem.rsplit("-", 1)[1])
        crop.resize((n, n), Image.LANCZOS).save(out, quality=86)
        print("wrote", out.relative_to(ROOT))


def main():
    check = "--check" in sys.argv
    missing = []
    for photo in tutor_photos():
        if not photo.exists():
            print("MISSING ORIGINAL", photo.relative_to(ROOT))
            continue
        for v in variants_for(photo):
            if not v.exists():
                missing.append(v)
                if not check:
                    break
    if check:
        if missing:
            print("STALE tutor photo variants — run tools/build-tutor-photo-variants.py:")
            for v in missing:
                print("  ", v.relative_to(ROOT))
            return 1
        print("ok    every tutor photo has its 176/264 jpg+webp variants")
        return 0
    done = set()
    for photo in tutor_photos():
        if photo.exists() and any(not v.exists() for v in variants_for(photo)):
            make(photo)
            done.add(photo.name)
    print(f"variants built for {len(done)} photo(s)" if done else "all variants already present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
