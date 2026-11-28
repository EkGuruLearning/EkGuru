"use strict";
/* The Firebase web API key is a public project identifier, not an admin
 * credential. The owner explicitly approved this exact key at this exact path.
 * All other keys, including a different key in the same file, still fail. */
const FIREBASE_PATH = "js/student/config.js";
const FIREBASE_WEB_KEY = "AIzaSyBEPKUDm2eh6rPZxaWolAnOL5JaQKLPDa8";
const PATTERNS = [
  [/\bAKIA[0-9A-Z]{16}\b/g, "AWS access key"],
  [/\bAIza[0-9A-Za-z_-]{35}\b/g, "Google API key"],
  [/\bsk-[A-Za-z0-9_-]{24,}\b/g, "sk- style key"],
  [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/g, "private key block"],
  [/\brzp_live_[A-Za-z0-9]{10,}\b/g, "Razorpay LIVE key id"],
  [/\bghp_[A-Za-z0-9]{30,}\b/g, "GitHub token"],
  [/\bxox[baprs]-[A-Za-z0-9-]{10,}\b/g, "Slack token"],
  [/EK_ADMIN_TOKEN\s*[:=]\s*["'][^"'\s]{8,}["']/g, "admin token value"],
  [/MAILER_SHARED_TOKEN\s*[:=]\s*["'][^"'\s]{8,}["']/g, "mailer token value"],
];
function findSecrets(text, rel) {
  const findings=[];
  for (const [pattern, name] of PATTERNS) {
    for (const match of text.matchAll(pattern)) {
      if (name === 'Google API key' && rel === FIREBASE_PATH && match[0] === FIREBASE_WEB_KEY) continue;
      findings.push(name + ' in ' + rel);
    }
  }
  return findings;
}
module.exports = { findSecrets };
