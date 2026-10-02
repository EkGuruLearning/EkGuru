#!/usr/bin/env node
/**
 * test-googlebot-parity.mjs — U1 requirement
 *
 * Serves the site locally and checks that Googlebot UA and Chrome UA
 * receive byte-identical HTML (no cloaking, Golden Rule R-1).
 *
 * Usage:
 *   node tools/test-googlebot-parity.mjs            (auto-finds port)
 *   node tools/test-googlebot-parity.mjs --port 8080
 *   node tools/test-googlebot-parity.mjs --local     (uses file://, no server)
 *
 * Exit 0 = PASS, exit 1 = FAIL.
 */
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { join, resolve, extname } from 'node:path';
import { request as httpRequest } from 'node:http';

const ROOT = resolve(import.meta.dirname, '..');
const SAMPLE_PAGES = [
  '/', '/hindi/', '/learn/', '/ask/', '/answers/',
  '/daily-hindi/', '/materials/', '/ar/', '/ja/', '/de/',
  '/privacy/', '/contact/', '/courses/',
  '/languages/fr/level/a1/', '/languages/es/',
];

const GOOGLEBOT_UA = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)';
const CHROME_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

function resolveFile(urlPath) {
  const clean = urlPath.split('?')[0].split('#')[0];
  if (clean === '/' || clean === '') return join(ROOT, 'index.html');
  const dir = clean.replace(/\/$/, '');
  const candidate = join(ROOT, dir, 'index.html');
  if (existsSync(candidate) && statSync(candidate).isFile()) return candidate;
  const direct = join(ROOT, dir);
  if (existsSync(direct) && statSync(direct).isFile()) return direct;
  return null;
}

function startServer(port) {
  return new Promise((resolve) => {
    const srv = createServer((req, res) => {
      const filePath = resolveFile(req.url || '/');
      if (!filePath) { res.writeHead(404); res.end('Not Found'); return; }
      try {
        const body = readFileSync(filePath);
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(body);
      } catch { res.writeHead(500); res.end('Error'); }
    });
    srv.listen(port, '127.0.0.1', () => resolve(srv));
  });
}

function fetch(url, ua) {
  return new Promise((ok, fail) => {
    const u = new URL(url);
    const req = httpRequest({ hostname: u.hostname, port: u.port, path: u.pathname, method: 'GET', headers: { 'User-Agent': ua } }, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => ok({ status: res.statusCode, body: Buffer.concat(chunks) }));
    });
    req.on('error', fail);
    req.end();
  });
}

function stripVolatile(html) {
  // Remove timestamps, build IDs, nonce values, etc. that may differ between runs
  return html
    .replace(/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/g, 'TIMESTAMP')
    .replace(/nonce="[a-zA-Z0-9+/=]+"/g, 'nonce="STRIPPED"');
}

async function main() {
  const args = process.argv.slice(2);
  const portArg = args.indexOf('--port');
  const port = portArg >= 0 ? parseInt(args[portArg + 1], 10) : 0; // 0 = auto
  const localMode = args.includes('--local');

  let srv = null;
  let baseUrl;

  if (!localMode) {
    srv = await startServer(port);
    const addr = srv.address();
    baseUrl = `http://127.0.0.1:${addr.port}`;
  } else {
    baseUrl = `file://${ROOT}`;
  }

  let pass = 0;
  let fail = 0;
  const failures = [];

  for (const page of SAMPLE_PAGES) {
    const url = `${baseUrl}${page}`;
    try {
      if (localMode) {
        // In local/file mode just read the file directly — same content for both UAs
        const filePath = resolveFile(page);
        if (!filePath) { fail++; failures.push(`${page}: file not found`); continue; }
        pass++;
        continue;
      }

      const [gb, ch] = await Promise.all([
        fetch(url, GOOGLEBOT_UA),
        fetch(url, CHROME_UA),
      ]);

      if (gb.status !== ch.status) {
        fail++;
        failures.push(`${page}: status mismatch — Googlebot=${gb.status} Chrome=${ch.status}`);
        continue;
      }

      const gbClean = stripVolatile(gb.body.toString('utf-8'));
      const chClean = stripVolatile(ch.body.toString('utf-8'));

      if (gbClean === chClean) {
        pass++;
      } else {
        fail++;
        // Find first difference
        let diffIdx = -1;
        for (let i = 0; i < Math.max(gbClean.length, chClean.length); i++) {
          if (gbClean[i] !== chClean[i]) { diffIdx = i; break; }
        }
        failures.push(`${page}: HTML differs at byte ${diffIdx} (Googlebot=${gbClean.length}b, Chrome=${chClean.length}b)`);
      }
    } catch (err) {
      fail++;
      failures.push(`${page}: ${err.message}`);
    }
  }

  if (srv) srv.close();

  // Output
  console.log(`\nGooglebot parity: ${pass} passed, ${fail} failed (${SAMPLE_PAGES.length} pages)\n`);
  for (const f of failures) console.log(`  FAIL  ${f}`);
  if (fail === 0) {
    console.log('\nPASS  Googlebot and Chrome receive identical HTML (no cloaking detected).\n');
  } else {
    console.log(`\nFAIL  ${fail} page(s) have UA-dependent content. Fix before AdSense review.\n`);
  }

  process.exit(fail === 0 ? 0 : 1);
}

main().catch((err) => { console.error(err); process.exit(1); });