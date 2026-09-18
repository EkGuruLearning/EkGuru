#!/usr/bin/env node
/* ==========================================================================
   test-question-api.mjs — a flag one learner throws reaches the next learner

   Prakash: "practice questions mai API use karo — jo ek user ne flag ya like
   kiya, wo doosre user ko bhi dikhna chahiye."

   The API is a Google Apps Script Web App (tools/apps-script-questions.gs).
   This test does not need it to be deployed: it stubs fetch, then proves the
   three things that have to be true for the feature to mean anything.

     1. OFFLINE — a vote is recorded on the device, queued, and the badge
        shows immediately with no network at all.
     2. SYNC — when the endpoint is configured, the queue is posted with the
        exact contract the .gs file answers, and the counts come back.
     3. COMMUNITY — a second learner's cached counts (what the API returned)
        are what a fresh device sees: a question flagged by somebody else
        appears in "Flagged by other learners" before that learner votes.

   Run:  node tools/test-question-api.mjs
   ========================================================================== */
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { JSDOM } = require("jsdom");
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
process.chdir(ROOT);

let pass = 0, fail = 0;
const ok = (name, cond, detail = "") => {
  if (cond) { pass++; console.log("  PASS  " + name); }
  else { fail++; console.log("  FAIL  " + name + (detail ? " — " + detail : "")); }
};
const read = (p) => readFileSync(p, "utf8");
const ENDPOINT = "https://script.google.com/macros/s/AKfyTEST/exec";

function page(endpoint, storage = {}) {
  const dom = new JSDOM("<!doctype html><html><body></body></html>", {
    url: "https://ekguru.shop/learn/bengali/practice/quiz/",
    runScripts: "outside-only"
  });
  const w = dom.window;
  for (const [k, v] of Object.entries(storage)) w.localStorage.setItem(k, v);
  w.EKGURU_SITE = { api: { questions: endpoint } };
  const calls = [];
  w.fetch = (url, init) => {
    calls.push({ url, init });
    if (!init || init.method === "GET") {
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true, bank: "bengali-quiz", counts: { "bq-01": { flags: 3, likes: 9 } } }) });
    }
    return Promise.resolve({ ok: true, json: () => Promise.resolve({ ok: true, bank: "bengali-quiz", id: "bq-02", flags: 1, likes: 0 }) });
  };
  w.eval(read("js/question-api.js"));
  return { w, calls };
}

console.log("\n1. the contract the .gs file answers\n");

{
  const gs = read("tools/apps-script-questions.gs");
  const api = read("js/question-api.js");
  ok("the server has both verbs", /function doGet\s*\(/.test(gs) && /function doPost\s*\(/.test(gs));
  ok("the server only accepts the five reasons", /"wrong answer": 1/.test(gs) && /"not in the lesson": 1/.test(gs));
  ok("the server hashes the client id instead of storing it",
    /computeDigest/.test(gs) && !/appendRow\(\[[^\]]*body\.client/.test(gs));
  ok("the server counts one vote per device per question",
    gs.indexOf('latest[String(r[5] || "") + "|" + String(r[2])]') > 0 && /clientHash/.test(gs));
  ok("the client sends text/plain, so there is no preflight",
    /"Content-Type": "text\/plain;charset=utf-8"/.test(api));
  ok("both sides agree on the actions", ["flag", "unflag", "like", "unlike"]
    .every((a) => gs.includes(a) && api.includes(`"${a}"`)));
}

console.log("\n2. offline: a vote is kept and shown with no network\n");

{
  const { w, calls } = page("");           /* endpoint deliberately not set */
  const q = w.EKGURU_QUESTIONS;
  ok("an unset endpoint means sync is off, not broken", q.enabled() === false);
  q.flag("bengali-quiz", "bq-02", "wrong answer");
  ok("the vote is remembered on the device", q.myVote("bengali-quiz", "bq-02") === "flag");
  ok("the badge shows it immediately", q.counts("bengali-quiz")["bq-02"].flags === 1);
  ok("the vote is queued for when there is a network", q.pending() === 1);
  ok("nothing was sent", calls.length === 0);
  q.like("bengali-quiz", "bq-02");
  ok("a like replaces the flag for this device", q.myVote("bengali-quiz", "bq-02") === "like");
  ok("the flag badge is not double counted", q.counts("bengali-quiz")["bq-02"].flags === 0 &&
    q.counts("bengali-quiz")["bq-02"].likes === 1);
}

console.log("\n3. sync: the queue goes out, the counts come back\n");

{
  const { w, calls } = page(ENDPOINT);
  const q = w.EKGURU_QUESTIONS;
  ok("a configured endpoint enables sync", q.enabled() === true);
  q.flag("bengali-quiz", "bq-02", "typo or spelling");
  await q.flush();
  ok("the vote posted exactly one entry", calls.filter((c) => c.init && c.init.method === "POST").length === 1,
    String(calls.length) + " calls seen");
  const posted = calls.find((c) => c.init && c.init.method === "POST");
  ok("the post lands on the configured endpoint", posted && posted.url === ENDPOINT);
  const body = JSON.parse(posted.init.body);
  ok("the payload matches the server contract",
    body.action === "flag" && body.bank === "bengali-quiz" && body.id === "bq-02" &&
    body.reason === "typo or spelling" && typeof body.client === "string" && body.client.length > 4,
    JSON.stringify(body));
  ok("no personal data rides along", !/email|name|user|@/i.test(JSON.stringify(body)));
  await q.flush();
  ok("the queue drains after a successful send", q.pending() === 0);
  ok("the counts refresh from the API", calls.some((c) => !c.init || c.init.method === "GET"));
  ok("a flush with an empty queue does nothing", (await q.flush()) === 0);
}

console.log("\n4. community: another learner's flag is visible here\n");

{
  /* A second device: it has never voted, but it has the API's counts. */
  const { w } = page(ENDPOINT);
  const q = w.EKGURU_QUESTIONS;
  await q.refresh("bengali-quiz");
  const top = q.topFlagged("bengali-quiz", 5);
  ok("the question another learner flagged is listed for this one",
    top.length === 1 && top[0].id === "bq-01" && top[0].flags === 3, JSON.stringify(top));
  ok("and its likes are carried too", top[0].likes === 9);
  ok("this device has not voted on it", q.myVote("bengali-quiz", "bq-01") === null);
  q.flag("bengali-quiz", "bq-01", "confusing wording");
  ok("once it does, the count includes both learners", q.counts("bengali-quiz")["bq-01"].flags === 4);
}

console.log("\n5. it all works with the site's own pages\n");

{
  const quiz = read("learn/bengali/practice/quiz/index.html");
  const hindi = read("learn/hindi/practice/quiz/index.html");
  const world = read("languages/ar/quiz/index.html");
  const landing = read("learn/bengali/practice/worksheets/index.html");
  ok("the quiz pages load the API", /js\/question-api\.js/.test(quiz) && /js\/question-api\.js/.test(hindi));
  ok("so do the world-course quiz and the worksheet builder",
    /js\/question-api\.js/.test(world) && /js\/question-api\.js/.test(landing));
  ok("the API script sits next to the tool it feeds",
    quiz.indexOf("question-api.js") < quiz.indexOf("hindi-tools.js"));
  ok("the quiz UI has flag, like and a community block",
    /data-flag=/.test(read("js/hindi-tools.js")) && /data-like=/.test(read("js/hindi-tools.js")) &&
    /Flagged by other/.test(read("js/hindi-tools.js")));
  ok("vote buttons never print", /class="q-vote no-print"/.test(read("js/hindi-tools.js")));
  ok("the offline cache carries the API", /question-api\.js/.test(read("sw.js")));
  ok("the endpoint is configured, not invented",
    /api:\s*\{\s*\n\s*questions:\s*""/.test(read("js/site-config.js")));
}

console.log(`\n${fail ? "FAIL" : "PASS"}  ${pass} passed, ${fail} failed\n`);
process.exit(fail ? 1 : 0);
