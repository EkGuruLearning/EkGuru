# 🚀 PUSH TO GITHUB — VS Code terminal

Repository: **`github.com/EkGuruLearning/EkGuru`**
Live URL after deploy: **https://ekgurulearning.github.io/EkGuru/**

---

# ⚡ THE SHORT VERSION

Open the `EkGuru` folder in VS Code, then in the terminal:

```bash
git init
git add -A
git commit -m "EkGuru v20 — Hindi tutoring platform"
git branch -M main
git remote add origin https://github.com/EkGuruLearning/EkGuru.git
git push -u origin main
```

Then **Settings → Pages → Deploy from a branch → `main` / `/ (root)` → Save.**

That is it. Everything below is detail, troubleshooting and the update workflow.

---

# 📋 STEP BY STEP

## Step 0 · Create the repository first

The push will fail if the repository does not exist yet.

1. Go to **https://github.com/new**
2. Owner: **`EkGuruLearning`**
3. Repository name: **`EkGuru`** — exactly this capitalisation
4. Visibility: **Public** *(GitHub Pages is only free on public repos)*
5. **Do not** tick "Add a README", .gitignore or licence — you already have files
6. **Create repository**

> ⚠️ **Capitalisation matters.** `EkGuru` and `ekguru` produce different URLs, and every
> canonical tag, hreflang link and sitemap entry in this project is built for
> `https://ekgurulearning.github.io/EkGuru/`. Use `EkGuru`.

## Step 1 · Open the right folder

In VS Code: **File → Open Folder** → select the **`EkGuru`** folder itself.

Confirm you are in the right place — the terminal should list `index.html` at the top
level, not another folder called `EkGuru`:

```bash
ls
```

You should see: `index.html  find-tutors.html  tutor.html  join.html  css  js  images  …`

If instead you see a single `EkGuru` folder, run `cd EkGuru` first.

## Step 2 · Tell git who you are

Only needed once per machine. Skip if you have used git before.

```bash
git config --global user.name "Prakash"
git config --global user.email "EkGuruLearning@gmail.com"
```

## Step 3 · Initialise and commit

```bash
git init
git add -A
git commit -m "EkGuru v20 — Hindi tutoring platform"
git branch -M main
```

**Why `git add -A` and not `git add .`** — `-A` includes dotfiles, which matters because
**`.nojekyll` is the single most important file in this project.** Without it GitHub runs
Jekyll over your site and can serve a blank page.

Verify it made it in:

```bash
git ls-files | grep nojekyll
```

That must print `.nojekyll`. If it prints nothing, stop and run `git add -f .nojekyll`.

Check the whole file count while you are there — it should be around 82:

```bash
git ls-files | wc -l
```

## Step 4 · Connect and push

```bash
git remote add origin https://github.com/EkGuruLearning/EkGuru.git
git push -u origin main
```

GitHub will ask you to sign in. See [authentication](#-authentication) below if it does
not open a browser window.

## Step 5 · Turn on Pages

1. Your repo → **Settings** tab
2. Left sidebar → **Pages**
3. **Source**: `Deploy from a branch`
4. **Branch**: `main`  ·  **Folder**: `/ (root)`
5. **Save**

Wait 1–2 minutes, refresh, and the green box appears:

### 🎉 https://ekgurulearning.github.io/EkGuru/

---

# 🔐 AUTHENTICATION

GitHub stopped accepting account passwords over HTTPS in 2021. Pick one of these.

## Option A — GitHub CLI (easiest)

```bash
# install once
winget install GitHub.cli        # Windows
brew install gh                  # macOS

gh auth login
```
Choose **GitHub.com → HTTPS → Login with a web browser**, press Enter, paste the code.
After that `git push` just works, forever.

## Option B — Personal Access Token

1. **https://github.com/settings/tokens** → *Generate new token (classic)*
2. Note: `EkGuru deploy` · Expiration: 90 days or No expiration
3. Tick the **`repo`** scope
4. Generate, and **copy the token** — it is shown only once
5. When `git push` asks:
   * Username: `EkGuruLearning`
   * Password: **paste the token** *(not your GitHub password)*

Save it so you are not asked again:
```bash
git config --global credential.helper store     # Linux
git config --global credential.helper manager   # Windows
git config --global credential.helper osxkeychain  # macOS
```

## Option C — SSH

Use the SSH remote instead:

```bash
ssh-keygen -t ed25519 -C "EkGuruLearning@gmail.com"
cat ~/.ssh/id_ed25519.pub
```

Copy that key into **https://github.com/settings/keys** → *New SSH key*, then:

```bash
git remote set-url origin git@github.com:EkGuruLearning/EkGuru.git
ssh -T git@github.com          # should greet you by name
git push -u origin main
```

---

# 🔄 UPDATING LATER

Once it is live, every change is three commands:

```bash
git add -A
git commit -m "Updated Hemlata's bio"
git push
```

The site refreshes in about a minute. Hard-refresh with `Ctrl+F5` to see it.

## After editing any tutor file

The sitemap, feeds and generated pages need regenerating first:

```bash
node build/sitemap.js
node build/feeds.js
node build/manifest.js
node build/patch.js        # always last

git add -A
git commit -m "Updated tutor details"
git push
```

`patch.js` re-applies the Google verification tag, the static hreflang and the canonical
tutor links, all of which live in generated files and would otherwise be lost.

**One-liner for convenience:**

```bash
node build/sitemap.js && node build/feeds.js && node build/manifest.js && node build/patch.js && git add -A && git commit -m "Update" && git push
```

---

# 🆘 IF SOMETHING GOES WRONG

### `remote origin already exists`
```bash
git remote set-url origin https://github.com/EkGuruLearning/EkGuru.git
```

### `failed to push some refs` / `rejected`
The remote has something yours does not — usually a README created by accident.
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```
If you are certain your local copy is the correct one:
```bash
git push -u origin main --force
```

### `Support for password authentication was removed`
You typed your GitHub password. Use a token or the CLI — see [authentication](#-authentication).

### `src refspec main does not match any`
The commit did not happen. Run `git add -A` then `git commit -m "first"` and push again.

### The site loads but has no styling
`.nojekyll` is missing. Check on GitHub, and if it is not there:
```bash
git add -f .nojekyll
git commit -m "Add .nojekyll"
git push
```

### White page
Same cause, 90% of the time — `.nojekyll`. Otherwise open the browser console with `F12`
and read the first red line; this project prints a clear message rather than failing
silently.

### Pages says "Your site is live" but you get a 404
* Wait another two minutes, the first build is the slowest
* Confirm `index.html` is at the **top level** of the repo, not inside a subfolder
* Check the URL capitalisation: `/EkGuru/`, not `/ekguru/`

---

# ✅ AFTER IT IS LIVE

Open the site and check:

- [ ] Logo shows in the header, three tutor cards on the home page
- [ ] Clicking a card opens `/tutor/<id>/` with the full profile
- [ ] The 🪙 currency dropdown appears in the header
- [ ] `/es/` and `/ar/` load, with Arabic right-to-left
- [ ] Sharing the link on WhatsApp shows the purple preview image
- [ ] On a phone: reviews swipe sideways, the booking bar sticks to the bottom

Then, the same day:

1. **Search Console** → https://search.google.com/search-console → add
   `https://ekgurulearning.github.io/EkGuru/` → **Verify**
   *(both methods are already in place — the meta tag on 28 pages and
   `googleb3b0e3defc1daa17.html` at the root, either will pass)*
2. **Submit `sitemap.xml`**
3. **Request indexing** for the home page and each `/tutor/<id>/`
4. **Bing Webmaster Tools** → import from Search Console in one click
5. **Add the site link to your Preply profile** — five minutes, and worth more for
   ranking than anything else on this list

---

**Built by Prakash — MNIT Jaipur, CSE 2022–2026 batch pass out.**

© EkGuru — One Student. One Guru. One Goal.
