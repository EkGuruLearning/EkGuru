// Isolated fixtures: failure must exit nonzero, counts cannot claim approval.
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, copyFileSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
const root = mkdtempSync(join(tmpdir(), 'ekguru-adsready-'));
try {
  mkdirSync(join(root, 'tools')); mkdirSync(join(root, 'reports'));
  copyFileSync(new URL('../../tools/adsready.js', import.meta.url), join(root, 'tools/adsready.js'));
  const local = spawnSync(process.execPath, [join(root, 'tools/adsready.js'), '--local'], { encoding: 'utf8' });
  assert.equal(local.status, 1);
  const report = JSON.parse(readFileSync(join(root, 'reports/adsready-local.json'), 'utf8'));
  assert.equal(report.ready, false);
  assert.ok(report.failed.some(c => c.id === 'ads-txt'));
  assert.match(report.checks.find(c => c.id === 'content-volume').label, /not quality or eligibility/);
  assert.doesNotMatch(local.stdout, /Substantial unique content|All preconditions verified/);
  writeFileSync(join(root, 'offline.mjs'), `globalThis.fetch = async (url, options) => {
    if (!options.signal || !options.redirect) throw Error('missing bounded request');
    throw Error('fixture: network unavailable');
  };`);
  const offline = spawnSync(process.execPath, ['--import', join(root, 'offline.mjs'), join(root, 'tools/adsready.js'), '--live'], { encoding: 'utf8' });
  assert.equal(offline.status, 1);
  const live = JSON.parse(readFileSync(join(root, 'reports/adsready.json'), 'utf8'));
  assert.equal(live.ready, false);
  assert.ok(live.failed.some(c => c.id === 'home-200'));
  assert.doesNotMatch(offline.stdout, /All preconditions verified/);
  console.log('PASS diagnostics fail on missing files/network and never equate page count with approval');
} finally { rmSync(root, { recursive: true, force: true }); }
