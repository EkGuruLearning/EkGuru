#!/usr/bin/env python3
"""Phase 7B §19 — country-page de-templating audit.

Computes word-5-gram Jaccard similarity across all 158 learn-hindi-from-*
pages (visible text only), finds the worst near-duplicate clusters and the
shared "template filler" phrases, so the worst clusters can be improved in
place (never auto-delete, never create more).

Output: reports/country-detemplating-phase7b.json
"""
import json, os, re, time
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def visible_text(path):
    h = open(path, encoding="utf-8").read()
    h = re.sub(r"<script[\s\S]*?</script>", " ", h)
    h = re.sub(r"<style[\s\S]*?</style>", " ", h)
    # body content between <h1> and <footer class="pw-ftr">
    m = re.search(r"<h1[^>]*>[\s\S]*?</h1>([\s\S]*?)<footer", h)
    seg = m.group(1) if m else h
    text = re.sub(r"<[^>]+>", " ", seg)
    text = re.sub(r"&\w+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

def ngrams(words, n=5):
    return set(tuple(words[i:i+n]) for i in range(len(words) - n + 1))

pages = {}
for d in sorted(os.listdir(".")):
    if d.startswith("learn-hindi-from-") and os.path.isdir(d):
        p = os.path.join(d, "index.html")
        if os.path.exists(p):
            pages[d] = visible_text(p)

texts = {d: re.findall(r"[a-z']+", t) for d, t in pages.items()}
grams = {d: ngrams(t) for d, t in texts.items()}

def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

# similarity for all pairs -> worst pairs
pairs = []
keys = sorted(pages)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        s = jaccard(grams[keys[i]], grams[keys[j]])
        pairs.append((s, keys[i], keys[j]))
pairs.sort(reverse=True)

# shared template phrases: 5-grams appearing in >= 60% of pages
gram_freq = Counter()
for d in keys:
    gram_freq.update(grams[d])
shared = [(g, c) for g, c in gram_freq.items() if c >= int(len(keys) * 0.6)]
shared.sort(key=lambda x: -x[1])

# per-page uniqueness: fraction of its 5-grams that are rare (appear in <= 3 pages)
rare_count = Counter()
for d in keys:
    rare_count.update(grams[d])
rare_grams = {g for g, c in rare_count.items() if c <= 3}
uniq_ratio = {}
for d in keys:
    g = grams[d]
    uniq_ratio[d] = round(len(g & rare_grams) / len(g), 3) if g else 0.0

worst = [{"sim": round(s, 3), "a": a, "b": b} for s, a, b in pairs[:30]]
report = {
    "generated": NOW,
    "pages": len(keys),
    "max_similarity": round(pairs[0][0], 3) if pairs else None,
    "avg_similarity": round(sum(s for s, _, _ in pairs) / len(pairs), 3) if pairs else None,
    "top_similar_pairs": worst,
    "template_5grams": [{"phrase": " ".join(g), "pages_with": c} for g, c in shared[:25]],
    "least_unique_pages": sorted(uniq_ratio.items(), key=lambda x: x[1])[:20],
    "avg_unique_ratio": round(sum(uniq_ratio.values()) / len(keys), 3) if keys else 0,
    "note": "Visible-text 5-gram Jaccard over the body between <h1> and <footer>.",
}
with open("reports/country-detemplating-phase7b.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("pages:", report["pages"], "| max sim:", report["max_similarity"],
      "| avg sim:", report["avg_similarity"], "| avg unique ratio:", report["avg_unique_ratio"])
print("\ntop similar pairs:")
for w in worst[:12]:
    print("  %.3f  %s <-> %s" % (w["sim"], w["a"], w["b"]))
print("\nmost shared 5-grams:")
for p in report["template_5grams"][:12]:
    print("  %3d pages | %s" % (p["pages_with"], p["phrase"]))
