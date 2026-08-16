/* Loads the EkGuru data layer in plain Node, the way a browser would,
   so the build scripts can read tutors, config and the SEO engine. */
const fs = require("fs");
const vm = require("vm");
const path = require("path");
const ROOT = path.join(__dirname, "..");

function load() {
  const sandbox = { console, Intl, Date, Math, JSON, URLSearchParams };
  sandbox.window = sandbox;
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  const run = f => {
    const p = path.join(ROOT, f);
    if (fs.existsSync(p)) vm.runInContext(fs.readFileSync(p, "utf8"), sandbox, { filename: f });
  };
  run("js/site-config.js");
  run("js/tutors/_registry.js");
  (sandbox.window.EKGURU_TUTOR_ORDER || []).forEach(id => run("js/tutors/" + id + ".js"));
  ["js/tutors-data.js", "js/i18n.js", "js/seo-engine.js"].forEach(run);
  return sandbox.window;
}
module.exports = { load, ROOT };
