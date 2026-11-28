"use strict";

// This gate intentionally excludes the editorial comparison areas and other
// non-page directories. Upload packs are private *at the repository root*;
// do not exclude a same-named directory elsewhere in the public site.
const fs = require("fs");
const path = require("path");
const EXCL_DIRS = new Set([".git", "node_modules", "ask", "answers", "reports", "docs",
  "research", "data", "tools", "csv", "live-sheets", "server", "images", "css",
  "audio", "fonts", "unselected", "Unselected files"]);
const PRIVATE_ROOTS = new Set(["A-Manually", ".artifacts"]);

function walk(root, dir = root, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (!EXCL_DIRS.has(entry.name) && !(dir === root && PRIVATE_ROOTS.has(entry.name))) {
        walk(root, path.join(dir, entry.name), out);
      }
    } else if (entry.isFile()) {
      out.push(path.join(dir, entry.name));
    }
  }
  return out;
}

module.exports = { walk };
