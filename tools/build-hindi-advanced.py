#!/usr/bin/env python3
"""EkGuru — Hindi Advanced level builder (additive; never touches the 15 lessons).

Reads the 6 hand-authored modules in tools/lang-data/modules/hi-*.json and:
  1. validates schema + quiz contract + quiz-ID uniqueness (hi-25..84),
  2. emits learn/hindi/advanced/index.html + 6 module pages (Hindi article
     shell, <div class="rel"> + <h2>Keep going</h2> so build-hindi-quizzes.py
     can inject the self-checks),
  3. appends the 60 quiz questions to js/hindi-quiz-bank.js (dedup by id,
     version bumped 1 -> 2, JSON contract preserved).

Run AFTER this builder (order matters):
  python3 tools/build-hindi-quizzes.py     # inject self-checks into new pages
  python3 tools/build-hindi-structure.py   # hub picks up the Advanced level

Idempotent: reruns rewrite the same 7 pages and replace (not duplicate)
the hi-* questions in the bank.
"""
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))


def load_mod(name):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(ROOT, "tools", name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


struct = load_mod("build-hindi-structure")
quizzes = load_mod("build-hindi-quizzes")

MOD_DIR = os.path.join(ROOT, "tools", "lang-data", "modules")
ORDER = ["health", "office", "education", "weather", "home", "festivals"]
OUT = os.path.join(ROOT, "learn", "hindi", "advanced")

PREV_NEXT_CSS = (
    ".prevnext{display:flex;justify-content:space-between;gap:12px;margin:34px 0 8px}"
    ".prevnext a{flex:1;border:1px solid var(--line);border-radius:12px;padding:12px 14px;"
    "text-decoration:none;color:var(--ink);background:var(--card,#fff)}"
    ".prevnext a:hover{border-color:var(--brand-2)}"
    ".prevnext .k{display:block;font-size:.78rem;color:var(--muted)}"
    ".prevnext .t{font-weight:600}"
)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def prevnext(prev_pair, next_pair):
    """prev_pair/next_pair: (href, label) or None. Self-contained nav."""
    if not prev_pair and not next_pair:
        return ""
    cells = []
    if prev_pair:
        cells.append(
            '<a href="%s"><span class="k">← Previous</span>'
            '<span class="t">%s</span></a>' % (prev_pair[0], esc(prev_pair[1])))
    else:
        cells.append("<span></span>")
    if next_pair:
        cells.append(
            '<a href="%s" style="text-align:right"><span class="k">Next →</span>'
            '<span class="t">%s</span></a>' % (next_pair[0], esc(next_pair[1])))
    return ('<nav class="prevnext" aria-label="More Hindi lessons">'
            + "".join(cells) + "</nav>")


def module_page(d, prev_pair, next_pair):
    title = "Hindi: " + d["title"]
    canon = struct.BASE + "/learn/hindi/advanced/" + d["slug"] + "/"
    b = []
    b.append('  <p class="crumb"><a href="../../../../">EkGuru</a> › '
             '<a href="../../../../learn/">Learn Hindi</a> › '
             '<a href="../../">Hindi</a> › '
             '<a href="../">Advanced</a> › %s</p>' % esc(d["title"].split(" &")[0]))
    b.append("  <h1>%s</h1>" % esc(title))
    b.append('  <p class="lede">%s</p>' % esc(d["lede"]))
    b.append("  <h2>Words (%d)</h2>" % len(d["words"]))
    b.append('  <table class="tbl"><thead><tr><th>English</th><th>Hindi</th>'
             "<th>Say it</th></tr></thead><tbody>")
    for w in d["words"]:
        b.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                 % (esc(w["en"]), esc(w["t"]), esc(w["r"])))
    b.append("  </tbody></table>")
    b.append("  <h2>Phrases</h2>")
    b.append('  <table class="tbl"><thead><tr><th>English</th><th>Hindi</th>'
             "<th>Say it</th></tr></thead><tbody>")
    for p in d["phrases"]:
        b.append("<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                 % (esc(p["en"]), esc(p["t"]), esc(p["r"])))
    b.append("  </tbody></table>")
    dg = d["dialogue"]
    b.append("  <h2>Dialogue — %s</h2>" % esc(dg["title"]))
    b.append('  <div class="dlg">')
    for ln in dg["lines"]:
        b.append('  <p><b>%s:</b> %s <span class="muted">(%s)</span><br>'
                 '<span class="muted">%s</span></p>'
                 % (esc(ln["sp"]), esc(ln["t"]), esc(ln["r"]), esc(ln["en"])))
    b.append("  </div>")
    b.append(prevnext(prev_pair, next_pair))
    b.append('  <div class="rel">')
    b.append("    <h2>Keep going</h2>")
    b.append('    <a href="../">Advanced Hindi — all six topics</a>')
    b.append('    <a href="../../practice/quiz/">Hindi topic quiz</a>')
    b.append('    <a href="../../">All of Learn Hindi</a>')
    b.append("  </div>")
    j = struct.jsonld("CollectionPage", title, d["lede"], canon)
    html = struct.shell(4, title, d["lede"], canon, title, d["lede"],
                        "\n".join(b), j)
    # prev/next styles: scoped <style> so the shared shell is untouched
    html = html.replace("</head>",
                        "<style>\n" + PREV_NEXT_CSS + "\n</style>\n</head>", 1)
    return html


def hub_page(mods):
    title = "Advanced Hindi — six real topics"
    lede = ("Past conversation into real life: the clinic, the office, school, "
            "the weather, home and festivals. Six word lists with phrases, "
            "dialogues and self-checks.")
    canon = struct.BASE + "/learn/hindi/advanced/"
    b = []
    b.append('  <p class="crumb"><a href="../../../">EkGuru</a> › '
             '<a href="../../../learn/">Learn Hindi</a> › '
             '<a href="../">Hindi</a> › Advanced</p>')
    b.append("  <h1>Advanced Hindi</h1>")
    b.append('  <p class="lede">%s</p>' % esc(lede))
    b.append("  <h2>Who this is for</h2>")
    b.append("  <p>You hold conversations, read paragraphs and handle tenses — "
             "now you want the vocabulary of real adult life: symptoms at the "
             "clinic, files at the office, the playground, the monsoon, the "
             "family table and the festival calendar.</p>")
    b.append("  <h2>What you will be able to do</h2>")
    b.append("  <p>Use 800+ words across six everyday domains, say the phrases "
             "that actually get used, follow short dialogues, and test "
             "yourself with ten quick questions per topic.</p>")
    b.append("  <h2>The six topics</h2>")
    b.append('  <div class="hs-grid">')
    for m in mods:
        b.append('<a class="hs-card" href="%s/"><b>%s</b><span>%s</span></a>'
                 % (m["slug"], esc(m["title"]), esc(m["lede"])))
    b.append("  </div>")
    b.append("  <h2>Practice</h2>")
    b.append('  <ul class="linklist">')
    b.append('    <li><a href="../practice/quiz/">Hindi topic quiz</a> — the '
             "new topics appear here automatically.</li>")
    b.append('    <li><a href="../practice/typing/">Typing trainer</a> — type '
             "the new words in Devanagari.</li>")
    b.append("  </ul>")
    b.append('  <p><a href="../">Back to All of Learn Hindi</a></p>')
    j = struct.jsonld("CollectionPage", title, lede, canon)
    return struct.shell(3, title, lede, canon, title, lede, "\n".join(b), j)


def validate(mods):
    errs = []
    seen_t = {}
    for d in mods:
        for k in ("slug", "title", "lede", "words", "phrases", "dialogue", "quiz"):
            if k not in d:
                errs.append(d.get("slug", "?") + ": missing " + k)
        for w in d.get("words", []):
            for k in ("en", "t", "r"):
                if k not in w or not w[k]:
                    errs.append(d["slug"] + ": bad word " + json.dumps(w, ensure_ascii=False))
            if w.get("t") in seen_t:
                errs.append("dup t %s (%s vs %s)" % (w["t"], seen_t[w["t"]], d["slug"]))
            seen_t[w.get("t", "")] = d["slug"]
        for p in d.get("phrases", []):
            for k in ("en", "t", "r"):
                if k not in p or not p[k]:
                    errs.append(d["slug"] + ": bad phrase")
        for ln in d.get("dialogue", {}).get("lines", []):
            for k in ("sp", "t", "r", "en"):
                if k not in ln or not ln[k]:
                    errs.append(d["slug"] + ": bad dialogue line")
        if len(d.get("quiz", [])) != 10:
            errs.append(d["slug"] + ": quiz != 10")
    ids = [q["id"] for d in mods for q in d["quiz"]]
    if len(set(ids)) != len(ids):
        errs.append("dup quiz ids within modules")
    expect = {"hi-%d" % i for i in range(25, 85)}
    if set(ids) != expect:
        errs.append("quiz ids != hi-25..84: missing=%s extra=%s"
                    % (sorted(expect - set(ids)), sorted(set(ids) - expect)))
    bank_ids = {q["id"] for q in quizzes.load_bank()["questions"]}
    clash = set(ids) & bank_ids
    if clash:
        errs.append("quiz id clash with bank: %s" % sorted(clash))
    for d in mods:
        for q in d["quiz"]:
            if q["a"] not in q["opts"] or len(q["opts"]) != 4:
                errs.append(q["id"] + ": bad answer/opts")
            if q.get("lesson") != "hindi/advanced/" + d["slug"]:
                errs.append(q["id"] + ": bad lesson pointer")
    # q-text uniqueness (injector rule: normalised-lowercase across whole bank)
    norm = lambda s: re.sub(r"\s+", " ", s).strip().lower()  # noqa: E731
    seen_q = {}
    for q in quizzes.load_bank()["questions"]:
        seen_q[norm(q["q"])] = q["id"]
    for d in mods:
        for q in d["quiz"]:
            k = norm(q["q"])
            if k in seen_q:
                errs.append("dup q-text %s vs %s" % (q["id"], seen_q[k]))
            seen_q[k] = q["id"]
    return errs


def write_bank(mods):
    bank = quizzes.load_bank()
    keep = [q for q in bank["questions"] if not q["id"].startswith("hi-")]
    new = [q for d in mods for q in d["quiz"]]
    bank["questions"] = keep + new
    bank["version"] = 2
    path = quizzes.BANK
    src = open(path, encoding="utf-8").read()
    marker = "window.EKGURU_HINDI_QUIZ ="
    head = src[:src.index(marker)]
    body = marker + "\n" + json.dumps(bank, ensure_ascii=False, indent=2) + ";\n"
    open(path, "w", encoding="utf-8").write(head + body)
    return len(keep), len(new)


def main():
    mods = []
    for s in ORDER:
        with open(os.path.join(MOD_DIR, "hi-%s.json" % s), encoding="utf-8") as f:
            mods.append(json.load(f))
    errs = validate(mods)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print("  -", e)
        raise SystemExit(1)
    os.makedirs(OUT, exist_ok=True)
    titles = {m["slug"]: m["title"] for m in mods}
    # hub
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(hub_page(mods))
    # modules with prev/next chain
    for i, m in enumerate(mods):
        prev_pair = None
        next_pair = None
        if i > 0:
            prev_pair = ("../%s/" % ORDER[i - 1], titles[ORDER[i - 1]])
        else:
            prev_pair = ("../", "Advanced Hindi")
        if i < len(mods) - 1:
            next_pair = ("../%s/" % ORDER[i + 1], titles[ORDER[i + 1]])
        d = os.path.join(OUT, m["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(module_page(m, prev_pair, next_pair))
    kept, added = write_bank(mods)
    total = sum(len(m["words"]) for m in mods)
    print("hindi-advanced: wrote 7 pages (%d words), bank %d kept + %d added (v2)"
          % (total, kept, added))


if __name__ == "__main__":
    main()
