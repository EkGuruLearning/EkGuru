#!/usr/bin/env node
/*
 * Keep the 196 country-learning pages honest when the public tutor roster is
 * empty. These pages were written when the site advertised a $6 tutor offer,
 * live lesson windows and available tutors. The current public roster is the
 * sheet-approved registry intersection, not every tutor file in the repo.
 *
 * This transform deliberately preserves each page's robots and canonical
 * tags. Changing either requires owner approval (repo rule R-7).
 *
 * Run: node tools/apply-country-tutor-availability.js [--check]
 */
"use strict";

const fs = require("fs");
const path = require("path");
const { loadSite } = require("./lib/site-data");

const ROOT = path.resolve(__dirname, "..");
const MARK = "<!-- ekguru:country-tutor-availability:v1 -->";
const SOURCE = "No public tutor profiles are currently available for booking.";

function decodeHtml(value) {
  return String(value || "")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">");
}

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function attrs(tag) {
  const out = {};
  const re = /([\w:-]+)\s*=\s*(["'])(.*?)\2/g;
  let match;
  while ((match = re.exec(tag))) out[match[1].toLowerCase()] = match[3];
  return out;
}

function preservationState(html) {
  const canonicalTag = (html.match(/<link\b[^>]*\brel=["']canonical["'][^>]*>/i) || [""])[0];
  const robotsTag = (html.match(/<meta\b[^>]*\bname=["']robots["'][^>]*>/i) || [""])[0];
  return {
    canonical: attrs(canonicalTag).href || "",
    robots: attrs(robotsTag).content || "",
  };
}

function countryName(html, rel) {
  const title = (html.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i) || ["", ""])[1];
  const decoded = decodeHtml(title.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim());
  const match = decoded.match(/^Learn Hindi from\s+(.+?)(?:\s*\|\s*EkGuru)?$/i);
  if (!match) throw new Error(`${rel}: cannot identify the country from <title>`);
  return match[1].trim();
}

function metaDescription(country) {
  return `Country-specific context for learning Hindi from ${country}, with starter phrases and free self-study resources. No tutor schedule or price is advertised.`;
}

function replaceDescriptionMeta(html, description) {
  return html.replace(/<meta\b[^>]*>/gi, (tag) => {
    const a = attrs(tag);
    const key = (a.name || a.property || "").toLowerCase();
    if (!["description", "og:description", "twitter:description"].includes(key)) return tag;
    if (/\bcontent\s*=\s*["']/i.test(tag)) {
      return tag.replace(/(\bcontent\s*=\s*)(["'])([\s\S]*?)\2/i,
        (_all, prefix, quote) => prefix + quote + escapeHtml(description) + quote);
    }
    return tag.replace(/\s*\/?\s*>$/, ` content="${escapeHtml(description)}"/>`);
  });
}

function updateVisibleFaq(html, country) {
  let count = 0;
  const answerFor = (question) => {
    const q = decodeHtml(question.replace(/<[^>]*>/g, " ")).replace(/\s+/g, " ").trim();
    if (/^Can I learn Hindi from\b/i.test(q)) {
      return `Yes. EkGuru's free Hindi self-study course is available online in ${country}. ${SOURCE} This page does not promise live lessons.`;
    }
    if (/^(What time|When)\b/i.test(q) && /lesson/i.test(q)) {
      return `EkGuru does not have a public tutor schedule to quote at the moment. The Hindi course is self-paced, so you can study at a time that works for you.`;
    }
    if (/how much|cost/i.test(q) && /lesson/i.test(q)) {
      return `The self-study Hindi course and linked learning guides are free to use. ${SOURCE} There is no current tutor price quoted on this page.`;
    }
    return null;
  };
  const out = html.replace(/<div\b(?=[^>]*\bclass=["'][^"']*\bfaq\b[^"']*["'])[^>]*>[\s\S]*?<\/div>/gi, (block) => {
    const q = (block.match(/<b\b[^>]*>([\s\S]*?)<\/b>/i) || ["", ""])[1];
    const answer = answerFor(q);
    if (!answer) return block;
    const p = /(<p\b[^>]*>)[\s\S]*?(<\/p>)/i;
    if (!p.test(block)) throw new Error(`FAQ answer paragraph missing for ${decodeHtml(q)}`);
    count += 1;
    return block.replace(p, `$1${escapeHtml(answer)}$2`);
  });
  if (count !== 3) throw new Error(`expected to update 3 country FAQs, updated ${count}`);
  return { html: out, answerFor };
}

function updateJsonLd(html, country, description, answerFor) {
  let scripts = 0;
  const out = html.replace(/<script\b(?=[^>]*\btype=["']application\/ld\+json["'])[^>]*>([\s\S]*?)<\/script>/gi,
    (tag, body) => {
      let data;
      try { data = JSON.parse(body); } catch (err) {
        throw new Error(`invalid JSON-LD: ${err.message}`);
      }
      const graph = Array.isArray(data["@graph"]) ? data["@graph"] : null;
      if (!graph) return tag;
      data["@graph"] = graph.filter((node) => node && node["@type"] !== "Service");
      for (const node of data["@graph"]) {
        if (!node || typeof node !== "object") continue;
        if (node["@type"] === "WebPage") node.description = description;
        if (node["@type"] === "FAQPage" && Array.isArray(node.mainEntity)) {
          for (const question of node.mainEntity) {
            const answer = answerFor(question && question.name || "");
            if (answer && question.acceptedAnswer) question.acceptedAnswer.text = answer;
          }
        }
      }
      scripts += 1;
      return tag.replace(body, JSON.stringify(data));
    });
  return { html: out, scripts };
}

function transform(html, rel) {
  const country = countryName(html, rel);
  const before = preservationState(html);
  let updated = html;

  updated = replaceDescriptionMeta(updated, metaDescription(country));

  const lede = /<p\b(?=[^>]*\bclass=["'][^"']*\blede\b[^"']*["'])[^>]*>[\s\S]*?<\/p>/i;
  if (!lede.test(updated)) throw new Error(`${rel}: missing country-page lede`);
  updated = updated.replace(lede,
    `<p class="lede">This country-specific guide explores how local language background and context can shape learning Hindi from ${escapeHtml(country)}. ${SOURCE} Its free Hindi course and self-study guides remain open.</p>`);

  const facts = /<div\b(?=[^>]*\bclass=["'][^"']*\bfacts\b[^"']*["'])[^>]*>\s*<div\b(?=[^>]*\bclass=["'][^"']*\bfact\b[^"']*["'])[^>]*>[\s\S]*?<\/div>\s*<div\b(?=[^>]*\bclass=["'][^"']*\bfact\b[^"']*["'])[^>]*>[\s\S]*?<\/div>\s*<div\b(?=[^>]*\bclass=["'][^"']*\bfact\b[^"']*["'])[^>]*>[\s\S]*?<\/div>\s*<\/div>/i;
  if (!facts.test(updated)) throw new Error(`${rel}: expected three country facts`);
  updated = updated.replace(facts,
    '<div class="facts" data-eg-country-tutor-state="none">' +
      '<div class="fact"><b>Free</b><span>self-paced Hindi course</span></div>' +
      '<div class="fact"><b>Any time</b><span>study on your schedule</span></div>' +
      '<div class="fact"><b>0 public</b><span>tutor profiles available for booking</span></div>' +
    '</div>');

  const time = /<h2>When your lessons would be<\/h2>[\s\S]*?(?=<h2>What it costs(?:\s+from)?\b)/i;
  if (!time.test(updated)) throw new Error(`${rel}: missing tutor-time section boundary`);
  updated = updated.replace(time,
    '<h2>Study Hindi on your own schedule</h2>\n' +
    `<p>${SOURCE} This page does not list a live lesson schedule. The self-paced Hindi course is available whenever it suits your day; you do not need to match Indian Standard Time. <a href="../learn/hindi/">Open the free Hindi course</a>.</p>\n`);

  const cost = /<h2>What it costs[^<]*<\/h2>[\s\S]*?(?=<h2>Five phrases to start with today<\/h2>)/i;
  if (!cost.test(updated)) throw new Error(`${rel}: missing tutor-price section boundary`);
  updated = updated.replace(cost,
    '<h2>Free Hindi self-study options</h2>\n' +
    `<p>The Hindi course, starter guides and practice tools on EkGuru are free to use. ${SOURCE} This page does not quote a current private-lesson price. If tutor listings return in future, confirm the current price and terms on the profile before booking.</p>\n`);

  const faq = updateVisibleFaq(updated, country);
  updated = faq.html;

  const cta = /<aside\b(?=[^>]*\bclass=["'][^"']*\bcta\b[^"']*["'])(?=[^>]*\baria-label=["']Next step["'])[^>]*>[\s\S]*?<\/aside>/i;
  if (!cta.test(updated)) throw new Error(`${rel}: missing country next-step CTA`);
  updated = updated.replace(cta,
    '<aside class="cta" aria-label="Next step" data-eg-country-tutor-state="none">\n' +
    '<b>Start with free, self-paced Hindi practice</b>\n' +
    `<p>${SOURCE} You can begin with the free Hindi course and guided lessons at your own pace.</p>\n` +
    '<a class="btn btn-primary" href="../learn/hindi/">Start the free course</a>\n' +
    '<a class="btn btn-ghost" href="../learn/">Free Hindi guides</a>\n' +
    '</aside>');

  const oldTutorList = /If you want a tutor now,\s*the\s*<a\b(?=[^>]*\bhref=["']\.\.\/find-tutors\.html["'])[^>]*>tutor list<\/a>\s*shows everyone available\./i;
  if (!oldTutorList.test(updated)) throw new Error(`${rel}: missing outdated tutor-list claim`);
  updated = updated.replace(oldTutorList,
    `${SOURCE} Start with the free course and guides while the directory is empty.`);

  const ld = updateJsonLd(updated, country, metaDescription(country), faq.answerFor);
  updated = ld.html;
  if (ld.scripts !== 1 && before.robots.toLowerCase().indexOf("noindex") === -1) {
    throw new Error(`${rel}: expected one JSON-LD graph on an indexable country page, found ${ld.scripts}`);
  }

  if (!updated.includes(MARK)) {
    const mainOpen = /<main\b[^>]*>/i;
    if (!mainOpen.test(updated)) throw new Error(`${rel}: missing <main> for country policy marker`);
    updated = updated.replace(mainOpen, (open) => open + "\n" + MARK);
  }

  const after = preservationState(updated);
  if (before.canonical !== after.canonical || before.robots !== after.robots) {
    throw new Error(`${rel}: transform changed canonical/robots (owner approval required)`);
  }
  return updated;
}

function files() {
  return fs.readdirSync(ROOT)
    .filter((name) => /^learn-hindi-from-[a-z0-9-]+$/.test(name))
    .map((name) => path.join(ROOT, name, "index.html"))
    .filter((file) => fs.existsSync(file))
    .sort();
}

function main() {
  const check = process.argv.includes("--check");
  const site = loadSite();
  const pages = files();
  const alreadyTransformed = pages.filter((file) => fs.readFileSync(file, "utf8").includes(MARK));
  if (site.publicTutors.length) {
    const legacy = pages.filter((file) => !fs.readFileSync(file, "utf8").includes(MARK));
    throw new Error(
      `public roster contains ${site.publicTutors.length} tutor(s). Country pages need a reviewed, roster-specific service rebuild before this change can be reversed; ${legacy.length} legacy page(s) remain.`
    );
  }
  if (!pages.length) throw new Error("no learn-hindi-from country pages found");

  let changed = 0;
  for (const file of pages) {
    const oldHtml = fs.readFileSync(file, "utf8");
    const rel = path.relative(ROOT, file).split(path.sep).join("/");
    const newHtml = oldHtml.includes(MARK) ? oldHtml : transform(oldHtml, rel);
    if (newHtml === oldHtml) continue;
    changed += 1;
    if (check) continue;
    fs.writeFileSync(file, newHtml);
  }

  if (check && changed) {
    console.error(`STALE ${changed} country page(s) — run node tools/apply-country-tutor-availability.js`);
    process.exitCode = 1;
    return;
  }
  console.log(`country tutor availability: ${pages.length} pages, ${changed} changed, ${alreadyTransformed.length} already current; robots/canonicals preserved`);
}

try {
  main();
} catch (error) {
  console.error(`FAIL country tutor availability: ${error.message}`);
  process.exitCode = 1;
}
