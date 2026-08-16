#!/usr/bin/env node
/* =========================================================
   EkGuru — POST-BUILD PATCHER
   ---------------------------------------------------------
   The pre-rendered and language pages are generated files. A few
   corrections have to be applied to them every time they are rebuilt,
   or they silently regress:

     1. Google site-verification meta on every page
     2. Static hreflang on the three English shell pages, so a crawler
        sees the language set on its first pass rather than only after
        JavaScript runs. Without this the hreflang is one-way and
        Google discards it.
     3. Tutor links point at the canonical /tutor/<id>/ page rather
        than tutor.html?id=, which is nearly empty without JavaScript.
     4. A language strip on the pre-rendered pages so they are not
        English-only islands with no route into the translations.

   Run it last:
       node build/patch.js
   ========================================================= */
const fs = require("fs");
const path = require("path");
const { load, ROOT } = require("./load.js");

const W = load();
const S = W.EKGURU_SITE;
const M = W.EKGURU_MARKETS;
const BASE = S.baseUrl.replace(/\/?$/, "/");
const VERIFY = '<meta name="google-site-verification" content="hFaqyp-9LdUXSKPA9RF011TkO2m_-7AUMasXqm_0dGI" />';

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith(".") || e.name === "node_modules") continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith(".html")) out.push(p);
  }
  return out;
}

function hreflangBlock(file) {
  const out = ["<!-- hreflang written statically: a crawler must see the language",
               "     set on its first pass, otherwise the mapping is one-way and",
               "     Google ignores it. seo.js refreshes these at runtime. -->"];
  M.forEach(m => {
    const pre = m.code === "en" ? "" : m.code + "/";
    const href = BASE + pre + (file === "index.html" ? "" : file);
    out.push(`<link rel="alternate" hreflang="${m.locale}" href="${href}">`);
    out.push(`<link rel="alternate" hreflang="${m.code}" href="${href}">`);
  });
  out.push(`<link rel="alternate" hreflang="x-default" href="${BASE + (file === "index.html" ? "" : file)}">`);
  return out.join("\n");
}

const LANGSTRIP = depth => {
  const up = "../".repeat(depth);
  return '\n  <nav class="pr-langs" aria-label="Languages">\n' +
    '    <strong>Also available in:</strong>\n    ' +
    M.filter(m => m.code !== "en")
     .map(m => `<a href="${up}${m.code}/find-tutors.html">${m.flag} ${m.label}</a>`)
     .join("\n    ") + "\n  </nav>\n";
};

let stats = { verify: 0, hreflang: 0, links: 0, strip: 0 };

for (const file of walk(ROOT)) {
  const rel = path.relative(ROOT, file).split(path.sep).join("/");
  let s = fs.readFileSync(file, "utf8");
  const before = s;

  /* 1. verification meta */
  if (!s.includes("google-site-verification") && s.includes("<head>")) {
    s = s.replace('<meta name="viewport"', VERIFY + '\n<meta name="viewport"');
    stats.verify++;
  }

  /* 2. static hreflang on the English shell pages */
  if (["index.html", "find-tutors.html", "join.html"].includes(rel) &&
      !s.includes('rel="alternate" hreflang')) {
    s = s.replace('<link rel="manifest"', hreflangBlock(rel) + '\n<link rel="manifest"');
    stats.hreflang++;
  }

  /* 3. canonical tutor links */
  const n1 = (s.match(/tutor\.html\?id=/g) || []).length;
  if (rel.match(/^[a-z]{2}\/(index|find-tutors)\.html$/)) {
    s = s.replace(/href="\.\.\/tutor\.html\?id=([a-z0-9-]+)(&amp;lang=[a-z]{2})?"/g, 'href="../tutor/$1/"');
  }
  if ((s.match(/tutor\.html\?id=/g) || []).length !== n1) stats.links++;

  /* 4. theme-color, which several browsers use for the address bar */
  if (!s.includes('name="theme-color"') && s.includes("<head>")) {
    s = s.replace('<link rel="manifest"', '<meta name="theme-color" content="#5b3df5">\n<link rel="manifest"');
  }

  /* 5. language strip on pre-rendered tutor pages */
  if (rel.startsWith("tutor/") && rel.endsWith("/index.html") &&
      rel !== "tutor/index.html" && !s.includes("pr-langs")) {
    s = s.replace("</article>", LANGSTRIP(2) + "</article>");
    stats.strip++;
  }


  /* 6. The hero statistics are hard-coded in index.html as a placeholder
        for the moment before JavaScript runs. A crawler reads exactly
        those numbers, so they must be true. */
  if (rel === "index.html") {
    const n = (W.EKGURU_TUTORS || []).length;
    const lessons = (W.EKGURU_TUTORS || []).reduce((a, t) => a + (t.lessonsCount || 0), 0);
    const min = (W.EKGURU_TUTORS || []).length
      ? Math.min(...W.EKGURU_TUTORS.map(t => t.priceUSD || 0)) : 0;
    s = s.replace(/(<b id="stat-tutors">)\d+(<\/b>)/, `$1${n}$2`);
    s = s.replace(/(<b id="stat-lessons">)[^<]*(<\/b>)/, `$1${lessons}+$2`);
    s = s.replace(/(<b id="stat-price">)[^<]*(<\/b>)/, `$1$${min}$2`);
  }


  /* 7. Footer column titles must be h3, not h4. Jumping from h2 to h4
        breaks the heading order, which assistive technology relies on
        and Lighthouse flags. */
  s = s.replace(/<h4( data-i18n="ftr\.(?:site|contact)")>/g, '<h3$1>');
  s = s.replace(/(<h3 data-i18n="ftr\.(?:site|contact)">[^<]*)<\/h4>/g, '$1</h3>');

  if (s !== before) fs.writeFileSync(file, s);
}

console.log(`patch: verification+${stats.verify}  hreflang+${stats.hreflang}  links+${stats.links}  langstrip+${stats.strip}`);
