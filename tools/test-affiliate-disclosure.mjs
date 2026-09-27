/* Node/jsdom contract test for the affiliate skeleton (js/affiliate/affiliate.js).
   Run: node tools/test-affiliate-disclosure.mjs
   Proves: inactive registry neutralises affiliate anchors, an approved
   program activates with sponsored rel + disclosure, excluded page
   classes block activation entirely. */
import { readFileSync } from "node:fs";
import { JSDOM } from "jsdom";

const engineSrc = readFileSync("js/affiliate/affiliate.js", "utf8");
const fails = [];
const ok = (m, extra) => console.log("ok   ", m, extra ? " — " + extra : "");
const bad = (m) => { fails.push(m); console.log("FAIL ", m); };

function makeDom(cls, anchorsHtml, registryResponse) {
  const dom = new JSDOM(
    `<!DOCTYPE html><html data-ad-class="${cls}"><body><p id="slot">${anchorsHtml}</p></body></html>`,
    { url: "https://ekguru.shop/some/page/", runScripts: "outside-only" }
  );
  dom.window.fetch = () =>
    Promise.resolve({ ok: true, json: () => Promise.resolve(registryResponse) });
  dom.window.eval(engineSrc);
  return dom;
}

const EMPTY_REGISTRY = {
  global_rules: { activation_master_switch: false },
  programs: []
};

const APPROVED_REGISTRY = {
  global_rules: { activation_master_switch: true },
  programs: [{
    slug: "demo", enabled: true, owner_status: "APPROVED",
    approval_status: "APPROVED", tracking_id: "T-123",
    tracking_params: [{ name: "aff", value: "T-123" }],
    disclosure_text: "Demo disclosure sentence.",
    allowed_placements: ["/some/page/"]
  }]
};

/* 1 — inactive registry: anchor neutralised */
{
  const dom = makeDom("HIGH_CONTENT", `<a data-affiliate="demo" href="https://merchant.example/x">buy</a>`, EMPTY_REGISTRY);
  await dom.window.EkGuruAffiliate.scan(dom.window.document);
  const a = dom.window.document.querySelector("a");
  if (a.getAttribute("data-affiliate")) bad("inactive registry must neutralise the anchor");
  else ok("inactive registry neutralises the anchor");
  if ((a.getAttribute("rel") || "").includes("sponsored")) bad("no sponsored rel without approval");
  else ok("no sponsored rel is added without approval");
  if (dom.window.document.querySelector(".affiliate-disclosure")) bad("no disclosure may render for an inactive program");
  else ok("no disclosure rendered for an inactive program");
}

/* 2 — approved program: sponsored rel + disclosure + tracking param */
{
  const dom = makeDom("HIGH_CONTENT", `<a data-affiliate="demo" href="https://merchant.example/x">buy</a>`, APPROVED_REGISTRY);
  await dom.window.EkGuruAffiliate.scan(dom.window.document);
  const a = dom.window.document.querySelector("a");
  const rel = a.getAttribute("rel") || "";
  for (const token of ["sponsored", "nofollow", "noopener"]) {
    if (!rel.includes(token)) bad("activated link missing rel=" + token);
  }
  if (!rel.includes("sponsored")) {} else ok("activated link carries rel=sponsored nofollow noopener");
  const d = dom.window.document.querySelector(".affiliate-disclosure");
  if (!d || !d.textContent.includes("Demo disclosure sentence.")) bad("approved link must render its disclosure text");
  else ok("disclosure renders beside the approved link");
  if (!a.href.includes("aff=T-123")) bad("tracking parameter from the registry entry must be appended");
  else ok("tracking parameter appended from the registry entry");
}

/* 3 — excluded page class: never activate, even when approved */
{
  const dom = makeDom("INTERACTIVE_LEARNING", `<a data-affiliate="demo" href="https://merchant.example/x">buy</a>`, APPROVED_REGISTRY);
  await dom.window.EkGuruAffiliate.scan(dom.window.document);
  const a = dom.window.document.querySelector("a");
  if ((a.getAttribute("rel") || "").includes("sponsored")) bad("excluded page class must never activate affiliate links");
  else ok("excluded page class (INTERACTIVE_LEARNING) blocks activation");
}

/* 4 — wrong placement: neutral */
{
  const dom = makeDom("HIGH_CONTENT", `<a data-affiliate="demo" href="https://merchant.example/x">buy</a>`,
    { global_rules: { activation_master_switch: true },
      programs: [{ ...APPROVED_REGISTRY.programs[0], allowed_placements: ["/other/"] }] });
  await dom.window.EkGuruAffiliate.scan(dom.window.document);
  if ((dom.window.document.querySelector("a").getAttribute("rel") || "").includes("sponsored"))
    bad("placement outside allowed_placements must not activate");
  else ok("placement outside allowed_placements stays neutral");
}

/* 5 — registry data itself: zero active programs on disk */
{
  const reg = JSON.parse(readFileSync("data/affiliate-programs.json", "utf8"));
  const active = (reg.programs || []).filter((p) => p.enabled === true);
  if (active.length) bad("data/affiliate-programs.json must contain zero enabled programs, found " + active.length);
  else ok("on-disk registry has zero enabled programs");
  if (reg.global_rules?.activation_master_switch !== false) bad("global master switch must be false");
  else ok("global activation master switch is false");
}

if (fails.length) { console.error("\n" + fails.length + " affiliate contract failure(s)"); process.exit(1); }
console.log("\nall affiliate contract checks passed");
