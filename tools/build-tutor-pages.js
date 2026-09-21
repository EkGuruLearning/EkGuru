#!/usr/bin/env node
/* ==========================================================================
   EkGuru — TUTOR PROFILE PAGES
   --------------------------------------------------------------------------
   Rebuilds the pre-rendered profile of every tutor in the registry:

       tutor/sushila-g/index.html   tutor/hemlata/index.html
       tutor/shikha-dutta/index.html   tutor/tara/index.html
       tutor/<new-tutor>/index.html

   WHY THIS TOOL EXISTS
   --------------------
   Adding a tutor used to mean hand-copying a 500-line page, then hand-editing
   the title, the meta description, the seven Open Graph tags, the JSON-LD
   graph, the availability table, the price, the "other tutors" list and the
   footer. Every one of those is a place to forget something — and the pages
   that were already here had drifted: Tara's page advertised $6 in its meta
   description while her own data said $8 (the same stale-fallback bug that
   put $3 on six home pages, see js/sheet.js v72).

   So the profiles are generated from the SAME sources the browser reads —
   js/tutors/*.js plus js/tutors/_overrides.js, through the shared loader —
   and a new tutor needs nothing but their own file and one line in the
   registry. The generator then writes their page for them.

   WHAT IS REWRITTEN, AND WHAT IS NOT
   ----------------------------------
   For a tutor who already has a page, that page is used as its own shell:
   every byte of hand-built head boilerplate (icons, AdSense, the inline
   profile styles, the header, the footer, the scroll-restore and consent
   script tags) is preserved untouched. Only these are replaced:

     · <title>, meta description, canonical, og:*, twitter:*
     · the JSON-LD <script type="application/ld+json"> graph
     · <main>                     — the whole profile
     · the header "Book a trial" link      (it carries the tutor id)
     · the footer's tutor column           (it lists every tutor)
     · the <link rel="preload"> of the portrait

   A tutor with no page yet gets tutor/tara/index.html as its shell — the
   lightest page of the set — and is then treated identically. Because the
   shell is only ever used for the parts above, the shells cannot drift into
   each other: nothing tutor-specific survives a rebuild.

   ⚠️ Prices on the page are never typed as text. Every figure is a
   `data-usd` element that js/pricing.js fills from the live rate table, so a
   visitor in Jaipur sees rupees and a visitor in Berlin sees euros, from the
   same file. The plain `$n` in the meta description is the USD list price,
   for crawlers, and is written from priceUSD — never from a literal.

   Run:  node tools/build-tutor-pages.js [--check] [--id <tutor-id>]
         --check exits 1 if a page on disk is out of date (CI/gate use)
   ========================================================================== */

"use strict";

const fs = require("fs");
const path = require("path");

const { loadSite } = require("./lib/site-data");

const ROOT = path.resolve(__dirname, "..");
process.chdir(ROOT);

const SITE = "https://ekguru.shop";
const SHELL_FALLBACK = "tutor/tara/index.html";     // lightest page of the set
const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const DAY_LONG = {
  Mon: "Monday", Tue: "Tuesday", Wed: "Wednesday", Thu: "Thursday",
  Fri: "Friday", Sat: "Saturday", Sun: "Sunday"
};

/* --------------------------------------------------------------------------
   helpers
   -------------------------------------------------------------------------- */

/* Text for HTML. Everything a tutor types goes through this: Shikha's
   headline contains an ampersand, and a tutor with "&" in their name used to
   break the page they were on. */
const esc = (s) =>
  String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

/* Text for a meta="..." attribute — the same, minus the tags that would end
   the attribute early. */
const attr = (s) => esc(s).replace(/\n+/g, " ").trim();

function truncate(s, n) {
  s = String(s || "").trim();
  if (s.length <= n) return s;
  return s.slice(0, n - 1).replace(/[,;.\s]+\S*$/, "") + "…";
}

function toArray(v) {
  if (Array.isArray(v)) return v.filter(Boolean);
  if (!v) return [];
  return String(v).split(",").map((x) => x.trim()).filter(Boolean);
}

/* A repo-relative image path as the profile page needs it (pages live two
   levels deep). Anything already absolute or a full URL is left alone. */
function relImage(p) {
  if (!p) return "";
  if (/^https?:\/\//i.test(p) || p.startsWith("//")) return p;
  return "../../" + String(p).replace(/^\//, "");
}

const exists = (p) => p && !/^https?:/i.test(p) && fs.existsSync(p);

/* "images/sushila.jpg" -> "images/sushila.webp" when the webp sibling exists */
function webpSibling(p) {
  if (!p || !/\.(jpe?g|png)$/i.test(p)) return "";
  const w = p.replace(/\.(jpe?g|png)$/i, ".webp");
  return exists(w) ? w : "";
}

function availabilityDays(t) {
  const a = t.availability || {};
  return DAYS.filter((d) => Array.isArray(a[d]) && a[d].length);
}

function prettyPrice(n) {
  const v = Number(n);
  if (!isFinite(v) || v <= 0) return "";
  return "$" + (Number.isInteger(v) ? v : v.toFixed(2));
}

/* --------------------------------------------------------------------------
   the pieces of the page
   -------------------------------------------------------------------------- */

function metaDescription(t, price) {
  return truncate(
    "Tutor-provided profile for " + t.name +
      ": stated subjects, languages and lesson details. Confirm current pricing and availability before booking.",
    158
  );
}

function title(t) {
  return t.name + " — Online Hindi Tutor Profile | EkGuru";
}

/* Profiles are descriptive pages, not inventory. Do not emit Offer,
   availability, CourseInstance or employment relationships: prices and
   schedules are imported profile fields that visitors must reconfirm. */
function jsonLd(t) {
  const url = SITE + "/tutor/" + t.id + "/";
  const photo = /^https?:/i.test(t.photo || "")
    ? t.photo
    : SITE + "/" + String(t.photo || "").replace(/^\//, "");
  const excerpt = (t.about && t.about[0]) || t.headline || "";

  const graph = [
    {
      "@type": "Person",
      "@id": url + "#person",
      name: t.name,
      jobTitle: "Hindi Tutor",
      description: "Tutor-provided profile excerpt: " + excerpt,
      image: photo,
      url,
      knowsLanguage: (t.speaks || []).map((s) => (typeof s === "string" ? s : s.lang)).filter(Boolean),
      knowsAbout: t.teaches || [],
      sameAs: [t.preplyUrl].filter(Boolean)
    },
    {
      "@type": "BreadcrumbList",
      "@id": url + "#breadcrumb",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Home", item: SITE + "/" },
        { "@type": "ListItem", position: 2, name: "Hindi Tutors", item: SITE + "/find-tutors.html" },
        { "@type": "ListItem", position: 3, name: t.name, item: url }
      ]
    }
  ];

  return JSON.stringify({ "@context": "https://schema.org", "@graph": graph });
}

function head(t, price) {
  const url = SITE + "/tutor/" + t.id + "/";
  const desc = metaDescription(t, price);
  const image = /^https?:/i.test(t.photo || "")
    ? t.photo
    : SITE + "/" + String(t.photo || "images/placeholder-tutor.jpg").replace(/^\//, "");

  return {
    title: title(t),
    desc,
    url,
    image,
    jsonLd: jsonLd(t)
  };
}

/* -- the profile itself ---------------------------------------------------- */

function headBlock(t, price) {
  const photo = relImage(t.photo || "images/placeholder-tutor.jpg");
  const webp = webpSibling(t.photo || "");
  const stats = [];

  if (price) {
    stats.push(
      'Profile lists <strong data-usd="' + t.priceUSD + '" data-t="' + t.id + '" data-f="priceUSD" data-fmt="money">' +
        price + "</strong> per <span data-t=\"" + t.id + '" data-f="lessonLength">' +
        esc(t.lessonLength || "50 min") + "</span> lesson"
    );
  }
  if (t.rating && t.reviewsCount) {
    stats.push(
      "Source profile: " + "★".repeat(Math.max(1, Math.min(5, Math.round(Number(t.rating))))) +
        ' <span data-t="' + t.id + '" data-f="rating" data-fmt="rating">' +
        Number(t.rating).toFixed(1) + '</span> from <span data-t="' + t.id +
        '" data-f="reviewsCount">' + t.reviewsCount + "</span> reviews"
    );
  }
  if (t.lessonsCount) {
    stats.push('Source profile lists <span data-t="' + t.id + '" data-f="lessonsCount">' + t.lessonsCount + "</span> lessons");
  }
  if (t.experienceYears) {
    stats.push(
      'Tutor states <span data-t="' + t.id + '" data-f="experienceYears">' + t.experienceYears + "</span>+ years' experience"
    );
  }

  const cta = [
    '<a class="btn btn-primary" href="../../tutor.html?id=' + t.id + '">Request a lesson with ' + esc(t.name) + "</a>",
    '<a class="btn btn-ghost" href="mailto:' + (t.formKey || t.email || "") +
      "?subject=" + encodeURIComponent("Hindi lesson enquiry — " + t.name) + '">Send an enquiry</a>'
  ];
  if (t.preplyUrl) {
    cta.push('<a class="btn btn-ghost" href="' + esc(t.preplyUrl) + '" rel="noopener nofollow">View current Preply profile</a>');
  }

  return `  <header class="pr-head">
    <picture>
      ${webp ? '<source srcset="' + relImage(webp) + '" type="image/webp">\n      ' : ""}<img class="pr-photo" src="${esc(photo)}" alt="${attr(t.name + ", online Hindi tutor from " + (t.city || t.country || "India"))}" width="200" height="200" itemprop="image" decoding="async">
    </picture>
    <div>
      <h1 itemprop="name" data-t="${t.id}" data-f="name">${esc(t.name)}</h1>
      <p class="pr-role"><span itemprop="jobTitle">Online Hindi Tutor</span> · <span itemprop="homeLocation" data-t="${t.id}" data-f="city">${esc(t.city || t.country || "India")}</span></p>
      <p class="pr-headline" data-t="${t.id}" data-f="headline">${esc(t.headline || "")}</p>
      <p class="pr-stats">
        ${stats.join("\n         · ")}
      </p>
      <p class="pr-cta">
        ${cta.join("\n        ")}
      </p>
    </div>
  </header>`;
}

function aboutBlock(t) {
  const paras = (t.about || []).map((p) => "      <p>" + esc(p) + "</p>").join("\n");
  if (!paras) return "";
  return `  <section class="pr-sec">
    <h2>About ${esc(t.name)}</h2>
    <div itemprop="description">
${paras}
    </div>
  </section>`;
}

function teachesBlock(t) {
  const teaches = toArray(t.teaches);
  const items = teaches.map((x) => '      <li itemprop="knowsAbout">' + esc(x) + "</li>").join("\n");
  const exams = toArray(t.exams);
  const specialities = toArray(t.specialities);

  const speaks = (t.speaks || []).map((s) =>
    typeof s === "string" ? s : s.lang + (s.level ? " (" + s.level + ")" : "")
  );

  return `  <section class="pr-sec">
    <h2>What ${esc(t.name)}'s profile lists</h2>
    <ul>
${items}
    </ul>
    <p>The tutor-provided profile lists <strong>${esc((t.levels || []).join(", "))}</strong> learner levels
       and these languages: ${esc(speaks.join(" and "))}.</p>
${exams.length ? "    <p>Profile-listed exam preparation: <strong>" + esc(exams.join(", ")) + "</strong>.</p>\n" : ""}${specialities.length ? "    <p>Profile-listed specialities: " + esc(specialities.join(" · ")) + ".</p>\n" : ""}  </section>`;
}

function experienceBlock(t) {
  const ex = toArray(t.experience);
  if (!ex.length) return "";
  return `  <section class="pr-sec">
    <h2>Teaching experience</h2>
    <ul>
${ex.map((x) => "      <li>" + esc(x) + "</li>").join("\n")}
    </ul>
  </section>`;
}

function methodologyBlock(t) {
  const m = t.methodology || [];
  if (!m.length) return "";
  const rows = m
    .map((x) => {
      if (typeof x === "string") {
        const [title, ...rest] = x.split("|");
        return "      <dt>" + esc(title.trim()) + "</dt><dd>" + esc(rest.join("|").trim()) + "</dd>";
      }
      return "      <dt>" + esc(x.title || "") + "</dt><dd>" + esc(x.desc || "") + "</dd>";
    })
    .join("\n");
  return `  <section class="pr-sec">
    <h2>How ${esc(t.name)} teaches</h2>
    <dl>
${rows}
    </dl>
  </section>`;
}

function availabilityBlock(t) {
  const days = availabilityDays(t);
  if (!days.length) return "";
  const on = days.map((d) => DAY_LONG[d]);

  const sentence =
    on.length
      ? "The imported profile lists times on " +
        (on.length > 1 ? on.slice(0, -1).join(", ") + ", and " + on[on.length - 1] : on[0]) + "."
      : "The imported profile has no weekly times listed.";

  const rows = DAYS.map((d) => {
    const slots = (t.availability || {})[d] || [];
    const cell = slots.length ? slots.join(", ") : "Not available";
    return "        <tr><th scope=\"row\">" + DAY_LONG[d] + "</th><td>" + esc(cell) + "</td></tr>";
  }).join("\n");

  return `  <section class="pr-sec">
    <h2>Profile-listed times (confirmation required)</h2>
    <p>${sentence} Times are shown in ${esc(t.timezone || "IST (GMT+5:30)")}. This is not a live availability calendar; request confirmation before making plans.</p>
    <table class="pr-table">
      <caption>Imported weekly times for ${esc(t.name)}; availability is not guaranteed</caption>
      <thead><tr><th scope="col">Day</th><th scope="col">Available times</th></tr></thead>
      <tbody>
${rows}
      </tbody>
    </table>
  </section>`;
}

function videoBlock(t) {
  if (!t.youtubeId) return "";
  return `  <section class="pr-sec">
    <h2>Intro video</h2>
    <p><a href="https://www.youtube.com/watch?v=${encodeURIComponent(t.youtubeId)}" rel="noopener">Watch ${esc(t.name)}'s ${esc(
    (t.videoTitle || "introduction video").toLowerCase()
  )} on YouTube</a></p>
  </section>`;
}

function reviewsBlock(t) {
  const reviews = t.reviews || [];
  if (!reviews.length) return "";
  const quote = (r) => {
    const value = r.stars || r.rating;
    const stars = value ? "★".repeat(Math.round(Number(value))) : "";
    const who = [r.name || r.student || r.author || "Reviewer", r.date].filter(Boolean).join(", ");
    const source = r.source === "preply" && t.preplyUrl
      ? ' · excerpt attributed to <a href="' + esc(t.preplyUrl) + '" rel="nofollow noopener">Preply</a>'
      : " · source not independently verified";
    return `    <blockquote class="pr-quote">
      <p>${esc(r.text || r.body || "")}</p>
      <footer>— <cite>${esc(who)}</cite>${stars ? " · " + stars : ""}${source}</footer>
    </blockquote>`;
  };
  return `  <section class="pr-sec">
    <h2>Attributed review excerpts for ${esc(t.name)}</h2>
${reviews.map(quote).join("\n")}
  </section>`;
}

function bookingBlock(t, price) {
  const contact = t.formKey || t.email || "EkGuruLearning@gmail.com";

  return `  <section class="pr-sec">
    <h2>Request current lesson details from ${esc(t.name)}</h2>
    <p>The imported profile lists <span data-usd="${t.priceUSD}" data-t="${t.id}" data-f="priceUSD" data-fmt="money">${price}</span> for <span data-t="${t.id}" data-f="lessonLength">${esc(
    t.lessonLength || "50 min"
  )}</span>. Price, format and availability can change and are not confirmed by this static page.
       Send an enquiry to
       <a data-s="email" href="mailto:${esc(contact)}?subject=${encodeURIComponent(
    "Hindi lesson enquiry for " + t.name
  )}">${esc(contact)}</a>. EkGuru forwards it when no direct tutor contact is on file.</p>
    <p><a class="btn btn-primary" href="../../tutor.html?id=${t.id}">Open the interactive profile and send an availability request</a></p>
  </section>`;
}

function othersBlock(t, roster) {
  const others = roster.filter((x) => x.id !== t.id);
  if (!others.length) return "";
  const rows = others
    .map((x) => {
      const p = prettyPrice(x.priceUSD);
      return (
        '      <li data-t-row="' + x.id + '"><a href="../' + x.id + '/"><span data-t="' + x.id +
        '" data-f="name">' + esc(x.name) + '</span></a> — <span data-t="' + x.id + '" data-f="headline">' +
        esc(x.headline || "") + "</span> (" +
        '<span data-usd="' + x.priceUSD + '" data-t="' + x.id + '" data-f="priceUSD" data-fmt="money">' +
        p + "</span> per lesson in the imported profile)</li>"
      );
    })
    .join("\n");
  return `  <nav class="pr-sec pr-others">
    <h2>Other Hindi tutors on EkGuru</h2>
    <ul>
${rows}
    </ul>
  </nav>`;
}

const LANGS = [
  ["es", "🇪🇸 Español"],
  ["fr", "🇫🇷 Français"],
  ["de", "🇩🇪 Deutsch"],
  ["pt", "🇧🇷 Português"],
  ["ja", "🇯🇵 日本語"],
  ["ar", "🇦🇪 العربية"]
];

function langsNav() {
  const links = LANGS.map(([code, label]) => '    <a href="../../' + code + '/find-tutors.html">' + label + "</a>").join("\n");
  return `  <nav class="pr-langs" aria-label="Languages">
    <strong>Also available in:</strong>
${links}
  </nav>`;
}

function main(t, roster) {
  const price = prettyPrice(t.priceUSD);
  const banner = t.banner
    ? '  <img class="pr-banner" src="' + esc(relImage(t.banner)) + '" alt="' + attr(t.name + " — " + (t.headline || "Hindi tutor")) +
      '" width="1280" height="720" fetchpriority="high" decoding="async">\n'
    : "";

  return `<main id="main" class="pr-wrap">
  <p class="pr-note">
    This page contains tutor-provided or source-profile information imported on 14 September 2026. EkGuru has not independently verified every statement, price or time. Confirm current details before booking.
    <a href="../../tutor.html?id=${t.id}"><strong>Open the interactive profile and send an availability request</strong></a>
  </p>
  <article class="pr-article" itemscope itemtype="https://schema.org/Person">
  <nav class="crumbs" aria-label="Breadcrumb">
    <a href="../../index.html">Home</a> ›
    <a href="../../find-tutors.html">Find Tutors</a> ›
    <span>${esc(t.name)}</span>
  </nav>

${banner}
${headBlock(t, price)}

${aboutBlock(t)}

${teachesBlock(t)}

${experienceBlock(t)}

${methodologyBlock(t)}

${availabilityBlock(t)}

${videoBlock(t)}

${reviewsBlock(t)}

${bookingBlock(t, price)}

${othersBlock(t, roster)}

${langsNav()}
</article>
</main>`;
}

function footerTutors(roster) {
  const links = roster.map((x) => '      <a href="../' + x.id + '/">' + esc(x.name) + "</a>").join("\n");
  return `<h3>Tutors</h3>\n${links}</div>`;
}

/* --------------------------------------------------------------------------
   build one page
   -------------------------------------------------------------------------- */

function build(t, roster) {
  const file = path.join("tutor", t.id, "index.html");
  const shell = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : fs.readFileSync(SHELL_FALLBACK, "utf8");

  const h = head(t, prettyPrice(t.priceUSD));
  let out = shell;

  /* Always replaced through a function, never a `$&`-style pattern string: the
     profile contains prices ("$8") and a tutor may write "$" in their bio, and
     a plain replacement string would treat those as capture references. */
  const once = (re, value, what) => {
    if (!re.test(out)) throw new Error(file + ": could not find " + what + " in the shell");
    out = out.replace(re, () => value);
  };

  once(/<title>[\s\S]*?<\/title>/, "<title>" + esc(h.title) + "</title>", "<title>");
  once(/<meta(?=[^>]*\bname="description")[^>]*>/, '<meta name="description" content="' + attr(h.desc) + '">', "meta description");
  once(/<link(?=[^>]*\brel="canonical")[^>]*>/, '<link rel="canonical" href="' + h.url + '">', "canonical");
  once(/<meta(?=[^>]*\bproperty="og:title")[^>]*>/, '<meta property="og:title" content="' + attr(h.title) + '">', "og:title");
  once(/<meta(?=[^>]*\bproperty="og:description")[^>]*>/, '<meta property="og:description" content="' + attr(h.desc) + '">', "og:description");
  once(/<meta(?=[^>]*\bproperty="og:url")[^>]*>/, '<meta property="og:url" content="' + h.url + '">', "og:url");
  once(/<meta(?=[^>]*\bproperty="og:image")[^>]*>/, '<meta property="og:image" content="' + attr(h.image) + '">', "og:image");
  once(/<meta(?=[^>]*\bname="twitter:title")[^>]*>/, '<meta name="twitter:title" content="' + attr(h.title) + '">', "twitter:title");
  once(/<meta(?=[^>]*\bname="twitter:description")[^>]*>/, '<meta name="twitter:description" content="' + attr(h.desc) + '">', "twitter:description");
  once(/<meta(?=[^>]*\bname="twitter:image")[^>]*>/, '<meta name="twitter:image" content="' + attr(h.image) + '">', "twitter:image");
  once(/<script type="application\/ld\+json">[\s\S]*?<\/script>/, '<script type="application/ld+json">' + h.jsonLd + "</script>", "JSON-LD");
  once(/<main(?=[^>]*\bid="main")[^>]*>[\s\S]*?<\/main>/, main(t, roster), "<main>");

  /* the portrait preload must point at the portrait this tutor actually has */
  const pre = webpSibling(t.photo || "") || (t.photo || "images/placeholder-tutor.webp");
  if (/<link(?=[^>]*\brel="preload")(?=[^>]*\bas="image")[^>]*>/.test(out)) {
    out = out.replace(
      /<link(?=[^>]*\brel="preload")(?=[^>]*\bas="image")[^>]*>/,
      '<link rel="preload" as="image" href="' + esc(relImage(pre)) + '"' +
        (/\.webp$/i.test(pre) ? ' type="image/webp"' : "") + " fetchpriority=\"high\">"
    );
  }

  /* the header's booking button carries the tutor id */
  out = out.replace(
    /(<a class="btn btn-primary btn-sm" href="\.\.\/\.\.\/tutor\.html\?id=)[a-z0-9-]+(">)/,
    "$1" + t.id + "$2"
  );

  /* the footer lists every tutor — keep it in registry order */
  out = out.replace(/<h3>Tutors<\/h3>[\s\S]*?<\/div>/, footerTutors(roster));

  return out;
}

/* --------------------------------------------------------------------------
   the three files that list tutor URLs
   --------------------------------------------------------------------------
   A tutor exists in four places, and three of them are easy to forget:

       tutor/<id>/index.html      the profile          (above)
       sitemap-tutors.xml         the tutor sitemap
       sitemap.xml                the master sitemap, with image entries
       feed.xml                   the RSS feed

   All three were hand-maintained, which is how a new tutor ends up with a
   page that Google is never told about. They are written here, from the same
   roster, so a tutor is discoverable the moment their file exists.

   Existing entries keep their own pubDate/lastmod history where it matters
   (the feed); a tutor being added today is dated today. */

const today = () => new Date().toISOString().slice(0, 10);
const rfc822 = (d) => new Date(d).toUTCString();

function sitemapEntry(t, stamp) {
  const photo = /^https?:/i.test(t.photo || "")
    ? t.photo
    : SITE + "/" + String(t.photo || "images/placeholder-tutor.jpg").replace(/^\//, "");
  const images =
    `    <image:image>\n      <image:loc>${photo}</image:loc>\n` +
    `      <image:caption>${esc(t.name)} — online Hindi tutor</image:caption>\n` +
    `      <image:title>${esc(t.name)}</image:title>\n    </image:image>` +
    (t.banner
      ? `\n    <image:image>\n      <image:loc>${
          /^https?:/i.test(t.banner) ? t.banner : SITE + "/" + String(t.banner).replace(/^\//, "")
        }</image:loc>\n      <image:caption>${esc(t.name + " — " + (t.headline || "Hindi tutor"))}</image:caption>\n` +
        `      <image:title>${esc(t.name)} banner</image:title>\n    </image:image>`
      : "");
  return `  <url>\n    <loc>${SITE}/tutor/${t.id}/</loc>\n${images}\n    <lastmod>${stamp}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>`;
}

function feedItem(t, pubDate) {
  const first = (t.about && t.about[0]) || t.headline || "";
  const price = prettyPrice(t.priceUSD);
  return `  <item>\n    <title>${esc(t.name + " — " + (t.headline || "Hindi tutor"))}</title>\n` +
    `    <link>${SITE}/tutor/${t.id}/</link>\n` +
    `    <guid isPermaLink="true">${SITE}/tutor/${t.id}/</guid>\n` +
    `    <description>${esc("Tutor-provided profile excerpt: " + first)}${price ? " Imported profile price: " + price + " per " + (t.lessonLength || "50 min") + "; confirm current details." : ""}</description>\n` +
    `    <category>Hindi tutor</category>\n    <pubDate>${rfc822(pubDate)}</pubDate>\n  </item>`;
}

/* Replace a tutor's existing entry, or insert one after the last tutor entry
   when they are new. Nothing else in these files is touched — the sitemaps
   carry thousands of URLs written by other generators. */
function upsertUrlBlock(xml, id, block) {
  const re = new RegExp(
    "  <url>\\s*<loc>" + SITE.replace(/\./g, "\\.") + "/tutor/" + id + "/</loc>[\\s\\S]*?</url>"
  );
  if (re.test(xml)) return xml.replace(re, () => block);

  const all = /  <url>\s*<loc>[^<]*\/tutor\/[a-z0-9-]+\/<\/loc>[\s\S]*?<\/url>/g;
  let last = null;
  for (let m = all.exec(xml); m; m = all.exec(xml)) last = m;
  if (!last) throw new Error("no tutor <url> block to anchor a new tutor to");
  const at = last.index + last[0].length;
  return xml.slice(0, at) + "\n" + block + xml.slice(at);
}

function pruneTutorImageEntries(text, roster) {
  const keep = new Set(roster.map((t) => t.name));
  return text.replace(/\s*<image:image>[\s\S]*?<\/image:image>/g, (block) => {
    const caption = block.match(/<image:caption>(.*?) — online Hindi tutor<\/image:caption>/);
    return caption && !keep.has(caption[1]) ? "" : block;
  });
}

function pruneTutorEntries(text, roster, kind) {
  const keep = new Set(roster.map((t) => t.id));
  const block = kind === "feed"
    ? /  <item>[\s\S]*?<\/item>\n?/g
    : /  <url>[\s\S]*?<\/url>\n?/g;
  return text.replace(block, (whole) => {
    const match = whole.match(new RegExp(SITE.replace(/\./g, "\\.") + "/tutor/([a-z0-9-]+)/"));
    return match && !keep.has(match[1]) ? "" : whole;
  });
}

function upsertFeedItem(feed, t, stamp) {
  /* Work on whole <item> blocks, one at a time. A regex that hunts for
     "<title>…</title><link>…</link>" across the file will happily swallow a
     dozen items on its way to the one it wants — that is how the first
     version of this function deleted the feed's other entries. */
  const items = [...feed.matchAll(/  <item>[\s\S]*?<\/item>/g)];
  const mine = items.find((m) => m[0].indexOf(`${SITE}/tutor/${t.id}/`) > -1);

  if (mine) {
    /* keep the tutor's original publication date — an entry that has been in
       the feed since July must not claim to be new today */
    const old = /<pubDate>([^<]+)<\/pubDate>/.exec(mine[0]);
    const block = feedItem(t, old ? old[1] : stamp);
    return feed.slice(0, mine.index) + block + feed.slice(mine.index + mine[0].length);
  }

  /* a new tutor: after the last tutor item, so the tutor entries stay
     together at the top of the channel and the guides keep their order */
  const tutorItems = items.filter((m) => /<link>[^<]*\/tutor\/[a-z0-9-]+\/<\/link>/.test(m[0]));
  const anchor = (tutorItems.length ? tutorItems[tutorItems.length - 1] : items[items.length - 1]);
  if (!anchor) throw new Error("the feed has no <item> to anchor a new tutor to");
  const at = anchor.index + anchor[0].length;
  return feed.slice(0, at) + "\n" + feedItem(t, stamp) + feed.slice(at);
}

function updateIndexFiles(roster, stamp, check) {
  const tutors = roster;
  const results = [];

  let stale = 0;
  const write = (file, next, what) => {
    const before = fs.readFileSync(file, "utf8");
    if (before === next) {
      results.push("ok    " + file + " already up to date");
      return;
    }
    if (check) {
      results.push("STALE " + file + " (" + what + ")");
      stale++;
      return;
    }
    fs.writeFileSync(file, next);
    results.push("wrote " + file + " (" + what + ")");
  };

  /* sitemap-tutors.xml — the tutor set only */
  let st = pruneTutorEntries(fs.readFileSync("sitemap-tutors.xml", "utf8"), tutors, "sitemap");
  for (const t of tutors) {
    st = upsertUrlBlock(
      st,
      t.id,
      `  <url>\n    <loc>${SITE}/tutor/${t.id}/</loc>\n    <lastmod>${stamp}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>`
    );
  }
  write("sitemap-tutors.xml", st, tutors.length + " tutor URLs");

  /* sitemap.xml — the same entries, with the image markup Google uses */
  let sm = pruneTutorImageEntries(fs.readFileSync("sitemap.xml", "utf8"), tutors);
  sm = pruneTutorEntries(sm, tutors, "sitemap");
  for (const t of tutors) sm = upsertUrlBlock(sm, t.id, sitemapEntry(t, stamp));
  write("sitemap.xml", sm, tutors.length + " tutor URLs");

  /* feed.xml — items, with the channel's build date */
  let feed = pruneTutorEntries(fs.readFileSync("feed.xml", "utf8"), tutors, "feed");
  for (const t of tutors) feed = upsertFeedItem(feed, t, stamp);
  feed = feed.replace(/<lastBuildDate>[^<]*<\/lastBuildDate>/, () => `<lastBuildDate>${rfc822(stamp)}</lastBuildDate>`);
  write("feed.xml", feed, tutors.length + " items");

  return { lines: results, stale };
}

/* --------------------------------------------------------------------------
   main
   -------------------------------------------------------------------------- */

function main0() {
  const argv = process.argv.slice(2);
  const check = argv.includes("--check");
  const idFlag = argv.indexOf("--id");
  const only = idFlag > -1 ? argv[idFlag + 1] : null;

  const site = loadSite();
  const roster = site.tutors;
  if (!roster.length) throw new Error("the tutor registry is empty");

  for (const id of site.unlisted) {
    console.log("warn  \"" + id + "\" has a tutor file but is not listed in js/tutors/_registry.js");
  }

  const targets = only ? roster.filter((t) => t.id === only) : roster;
  if (only && !targets.length) {
    console.error("no tutor with id \"" + only + "\" in the registry");
    return 1;
  }

  let stale = 0;
  let wrote = 0;

  for (const t of targets) {
    const file = path.join("tutor", t.id, "index.html");
    const before = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "";
    const after = build(t, roster);

    if (before === after) {
      console.log("ok    " + file + " already up to date");
      continue;
    }
    if (check) {
      console.log("STALE " + file + (before ? "" : " (missing)"));
      stale++;
      continue;
    }
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, after);
    wrote++;
    console.log(
      (before ? "wrote " : "new   ") + file + " (" + before.length + " → " + after.length + " bytes, " +
        roster.length + " tutors)"
    );
  }

  if (!wrote && !stale) console.log("all " + targets.length + " tutor page(s) already up to date");

  /* The sitemaps and the feed always follow the whole roster, even when only
     one page was rebuilt — a tutor added with --id still has to be findable. */
  if (!only) {
    const idx = updateIndexFiles(roster, today(), check);
    idx.lines.forEach((l) => console.log(l));
    stale += idx.stale;
  }

  if (check && stale) {
    console.log("STALE: " + stale + " tutor page(s) — run tools/build-tutor-pages.js");
    return 1;
  }
  return 0;
}

process.exit(main0());
