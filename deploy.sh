#!/usr/bin/env bash
# =========================================================
# EkGuru — one-command deploy
#   ./deploy.sh              rebuild, commit, push
#   ./deploy.sh "message"    with your own commit message
#
# Safe to run repeatedly. On the first run it initialises the
# repository and connects the remote for you.
# =========================================================
set -e

REPO="https://github.com/EkGuruLearning/EkGuru.git"
MSG="${1:-EkGuru update $(date '+%Y-%m-%d %H:%M')}"

cd "$(dirname "$0")"

echo "▸ regenerating sitemap, feeds, manifest"
node build/sitemap.js
node build/feeds.js
node build/manifest.js
node build/patch.js          # must run last — restores verification, hreflang, canonicals

if [ ! -d .git ]; then
  echo "▸ first run: initialising the repository"
  git init -q
  git branch -M main
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "▸ connecting remote"
  git remote add origin "$REPO"
fi

echo "▸ staging (-A so .nojekyll is included)"
git add -A

if git diff --cached --quiet; then
  echo "▸ nothing changed, nothing to push"
  exit 0
fi

# .nojekyll is the single most important file here: without it GitHub runs
# Jekyll over the site and can serve a blank page.
if ! git ls-files --cached | grep -qx ".nojekyll"; then
  echo "▸ .nojekyll was missing from the index — forcing it in"
  git add -f .nojekyll
fi

echo "▸ committing: $MSG"
git commit -q -m "$MSG"

echo "▸ pushing to $REPO"
git push -u origin main

echo
echo "✓ pushed $(git ls-files | wc -l | tr -d ' ') files"
echo "  https://ekgurulearning.github.io/EkGuru/"
echo
echo "  If this is your first push, finish in the browser:"
echo "  Settings → Pages → Deploy from a branch → main → / (root) → Save"
