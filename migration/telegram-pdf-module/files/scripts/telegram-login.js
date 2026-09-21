#!/usr/bin/env node
/**
 * One-time Telegram login helper.
 *
 * Usage:
 *   TELEGRAM_API_ID=... TELEGRAM_API_HASH=... node scripts/telegram-login.js
 *
 * The script:
 *  1. asks for phone number (on stdin, locally)
 *  2. sends Telegram code request
 *  3. asks for OTP locally
 *  4. asks for 2FA password locally if required
 *  5. prints the StringSession to stdout AND writes it to .telegram-session
 *     (which is gitignored).
 *
 * The operator then copies that session string into TELEGRAM_SESSION on the
 * production environment (or stores it in the secret manager).
 */

"use strict";

const readline = require("readline");
const fs = require("fs");
const path = require("path");
const { TelegramClient, sessions, Api } = require("teleproto");

const API_ID = parseInt(process.env.TELEGRAM_API_ID || "0", 10);
const API_HASH = process.env.TELEGRAM_API_HASH || "";

if (!API_ID || !API_HASH) {
  console.error("Set TELEGRAM_API_ID and TELEGRAM_API_HASH before running.");
  console.error("You can also put non-SECRET values (apiId/apiHash) in the Apps Script Config tab;");
  console.error("then run the server once and it will be read automatically. For login, pass them on env:");
  console.error("  TELEGRAM_API_ID=12345 TELEGRAM_API_HASH=abcdef... node scripts/telegram-login.js");
  process.exit(2);
}

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
function ask(q) {
  return new Promise((resolve) => rl.question(q, (a) => resolve(String(a || "").trim())));
}

(async () => {
  const client = new TelegramClient(new sessions.StringSession(""), API_ID, API_HASH, {
    connectionRetries: 2,
    useWSS: true,
  });
  await client.connect();

  const phone = await ask("Phone number (with country code, e.g. +91...): ");
  await client.sendCode({ apiId: API_ID, apiHash: API_HASH }, phone);

  const code = await ask("Telegram login code (as received in app): ");
  let signInResult;
  try {
    signInResult = await client.invoke(new Api.auth.SignIn({
      phoneNumber: phone,
      phoneCodeHash: client._phoneCodeHash ? client._phoneCodeHash[phone] : undefined,
      phoneCode: code,
    }));
  } catch (err) {
    if (err && err.message && /PASSWORD/i.test(err.message)) {
      const pwd = await ask("Two-factor password is enabled. Enter your 2FA password: ");
      const password = await client.invoke(new Api.account.GetPassword());
      const inputPwd = await client.computePasswordCheck(password, pwd);
      signInResult = await client.invoke(new Api.auth.CheckPassword({ password: inputPwd }));
    } else {
      throw err;
    }
  }

  const sessionStr = client.session.save();
  console.log("\n=== TELEGRAM SESSION STRING (save this securely) ===");
  console.log(sessionStr);
  console.log("====================================================\n");

  const outPath = path.join(__dirname, "..", ".telegram-session");
  fs.writeFileSync(outPath, sessionStr, { mode: 0o600 });
  console.log(`Saved to ${outPath} (chmod 600). Copy this value into the TELEGRAM_SESSION secret.`);
  console.log("NEVER commit .telegram-session. The file is listed in .gitignore.");

  await client.disconnect();
  rl.close();
})().catch((err) => {
  console.error("Login failed:", err && err.message ? err.message : err);
  process.exit(1);
});
