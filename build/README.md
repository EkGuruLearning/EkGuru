# build/ — generators

Run these after editing anything in `js/tutors/` or `js/site-config.js`.

```bash
cd EkGuru
node build/sitemap.js     # sitemap.xml — 28 URLs, hreflang, 96 image entries
node build/feeds.js       # llms.txt + feed.xml
node build/manifest.js    # manifest.webmanifest
```

`load.js` is a helper the others use; you never run it directly.

## Note on the pre-rendered pages

`tutor/*/index.html` and the language folders (`es/`, `fr/`, `de/`, `pt/`, `ja/`, `ar/`)
are committed to the repository as finished files. They only need regenerating if you
change a tutor's details, and the generators for those live alongside these scripts in
the project history. For a normal edit — a price, a bio, a review — run the three
commands above and the site is consistent again.

## Full rebuild order

```bash
node build/minify.js     # css/style.css -> css/style.min.css
node build/sitemap.js
node build/feeds.js
node build/manifest.js
node build/patch.js      # always last
```

`minify.js` refuses to write if the rule count or brace balance does not match the
source, so a broken stylesheet cannot ship.

`patch.js` re-applies the Google verification tag, static hreflang, canonical tutor
links, the language strips, the hero statistics and the footer heading levels — all of
which live in generated files and would otherwise be lost on a rebuild.

## When you change the stylesheet

Edit `css/style.css`, never `css/style.min.css`. Run `node build/minify.js` afterwards.

If you change anything above the fold — the header, hero or buttons — also refresh the
inlined critical CSS in the four HTML files. It is the block marked
`<style id="critical">`.

## Service worker

`sw.js` caches the shell and images so repeat visits are near-instant, working around
the 10-minute cache lifetime GitHub Pages enforces. **Bump `CACHE` in `sw.js` on every
deploy**, otherwise returning visitors keep the previous version.
