/**
 * Five public journeys, run in CI with Playwright when Chromium is installed.
 * This file does not pretend a pass if the browser is missing.
 *
 *   npx playwright test tools/test-journeys.mjs
 */
import { test, expect } from "@playwright/test";
import { readFileSync } from "node:fs";

const base = process.env.EKGURU_BASE || "http://127.0.0.1:4173";

test("J1 home to learn to a guide", async ({ page }) => {
  await page.goto(base + "/");
  await expect(page.locator("h1")).toHaveCount(1);
  /* The stat is honest in BOTH states (U0): with public tutors it equals the
     number of cards; with zero it shows 0 and the hero carries the empty
     state with the free course — never a stale face or a fake count. */
  const stat = (await page.locator("#stat-tutors").textContent()).trim();
  if (stat === "0") {
    await expect(page.locator("#hero-tutor[data-eg-empty='1']")).toHaveCount(1);
    await expect(page.locator("#hero-tutor").getByRole("link", { name: /free course/i })).toBeVisible();
  } else {
    await expect(page.locator(".tcard").first()).toBeVisible();
  }
  await page.locator("header nav").getByRole("link", { name: "Learn", exact: true }).click();
  await expect(page).toHaveURL(/\/learn\/$/);
  await page.locator('a[href="hindi-alphabet-for-beginners/"]').click();
  await expect(page).toHaveURL(/hindi-alphabet-for-beginners/);
  await expect(page.locator("h1")).toHaveCount(1);
});

test("J2 home to tutors", async ({ page }) => {
  await page.goto(base + "/find-tutors.html");
  await expect(page.locator("h1")).toHaveCount(1);
  /* The live Sheet can approve and activate sheet-only tutors without a
     deploy. Do not hard-code names as unpublished: active approved rows may
     appear here and must link to the working dynamic profile route. A
     placeholder-photo row (Tara in the current Sheet) must still stay out. */
  const hemlataCard = page.locator('.tcard[data-id="hemlata"]');
  if (await hemlataCard.count()) {
    const profileLink = hemlataCard.first().getByRole("link").first();
    await expect(profileLink).toHaveAttribute("href", /tutor\.html\?id=hemlata/);
    await profileLink.click();
    await expect(page).toHaveURL(/tutor\.html\?id=hemlata/);
    await expect(page.locator('meta[name="robots"]'))
      .toHaveAttribute("content", /noindex/);
    await page.goto(base + "/find-tutors.html");
  }
  await expect(page.locator('.tcard[data-id="tara"]')).toHaveCount(0);
  /* The directory shows either a live roster or its honest empty state; both
     paths keep the journey usable. */
  const sushila = page.getByRole("link", { name: /Sushila/i });
  if (await sushila.count()) {
    await sushila.first().click();
    await expect(page).toHaveURL(/sushila-g/);
  } else {
    await expect(page.locator("[data-eg-empty='1']").first()).toBeVisible();
    await page.locator("main, #main").getByRole("link", { name: /free course|Learn Hindi|courses/i }).first().click();
    await expect(page).toHaveURL(/learn\/|courses\//);
  }
});

test("J3 countries directory", async ({ page }) => {
  await page.goto(base + "/learn/countries/");
  await expect(page.locator("h1")).toContainText("Published country guides");
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute("content", /index/);
});

test("J4 about privacy terms contact", async ({ page }) => {
  await page.goto(base + "/about/");
  await expect(page.getByText("24 hours")).toHaveCount(0);
  await page.goto(base + "/privacy/");
  await expect(page.getByText(/Advertising is disabled/i).first()).toBeVisible();
  await page.goto(base + "/terms/");
  await expect(page.locator("h1")).toHaveCount(1);
  await page.goto(base + "/contact/");
  await expect(page.getByRole("link", { name: "support@ekguru.shop" }).first()).toBeVisible();
  await expect(page.locator("#cf-name")).toBeVisible();
});

test("J5 mobile menu to learn", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(base + "/");
  await page.getByRole("button", { name: "Menu" }).click();
  await page.locator("header nav").getByRole("link", { name: "Learn", exact: true }).click();
  await expect(page).toHaveURL(/\/learn\/$/);
});

/* J6 — the lesson reader lays out as a page, on a phone and on a laptop.
   17 Nov 2026: the booking modal's `.bk-step{display:flex}` collided with
   the reader's step class, so every level/lesson step rendered as a flex
   ROW and the text was pinched into letter-wide columns. jsdom cannot see
   layout; only a real browser can — hence this journey. */
for (const vp of [{ name: "phone", width: 390, height: 844 }, { name: "laptop", width: 1366, height: 900 }]) {
  test("J6 level reader is readable on a " + vp.name, async ({ page }) => {
    await page.setViewportSize({ width: vp.width, height: vp.height });
    await page.goto(base + "/languages/hi/level/a1/");
    const art = page.locator(".lv-main.bk-on");
    await expect(art).toBeVisible();
    const m = await page.evaluate(() => {
      const art = document.querySelector(".lv-main.bk-on");
      const step = art.querySelector(".bk-leaf:not([hidden])");
      const cs = getComputedStyle(step);
      const aw = art.getBoundingClientRect().width;
      const kids = [...step.children].filter((k) => k.getBoundingClientRect().height > 0);
      const narrow = kids.filter((k) => k.getBoundingClientRect().width < aw * 0.6).map((k) => k.tagName + "." + k.className);
      const rail = document.querySelector(".bk-rail"), hdr = document.querySelector(".hdr");
      window.scrollTo(0, 1200);
      return new Promise((r) => setTimeout(() => r({
        display: cs.display, aw, narrow,
        railTop: rail.getBoundingClientRect().top, hdrBottom: hdr.getBoundingClientRect().bottom,
        railH: rail.getBoundingClientRect().height,
        docWider: document.documentElement.scrollWidth > window.innerWidth + 1
      }), 300));
    });
    expect(m.display).toBe("block");
    expect(m.narrow, "pinched children: " + m.narrow.join(", ")).toEqual([]);
    expect(m.railTop, "rail slid behind the sticky header").toBeGreaterThanOrEqual(m.hdrBottom - 1);
    expect(m.railH, "sticky rail too tall").toBeLessThan(vp.height * 0.3);
    expect(m.docWider, "page scrolls sideways").toBe(false);
    /* Next turns the page; Whole lesson shows everything and drops the nav */
    await page.getByRole("button", { name: "Next →" }).click();
    await expect(page.locator(".bk-label")).toContainText("Step 2 of");
    await page.getByRole("button", { name: "Whole lesson" }).click();
    await expect(page.locator(".bk-nav")).toBeHidden();
    await expect(page.locator(".bk-leaf[hidden]")).toHaveCount(0);
  });
}

/* Old shared bookmarks must reach the real conversation content without JS.
   The second case simulates a client that suppresses automatic refresh. */
test("J7 retired country phrase bookmark redirects without JavaScript", async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto(base + "/learn-hindi-from-ghana/daily-phrases/", { waitUntil: "domcontentloaded" });
  await expect(page).toHaveURL(base + "/learn/hindi/conversation/");
  await expect(page.locator("h1")).toContainText("Conversation");
  await context.close();
});

test("J8 redirect fallback is keyboard usable when refresh is unavailable", async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.route("**/learn-hindi-from-philippines/daily-phrases/", async route => {
    const response = await route.fetch();
    const body = (await response.text()).replace(/<meta http-equiv="refresh"[^>]*>/, "");
    await route.fulfill({ response, body });
  });
  await page.goto(base + "/learn-hindi-from-philippines/daily-phrases/");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Hindi daily phrases have moved");
  const link = page.getByRole("link", { name: "Open Hindi greetings and conversation" });
  await expect(link).toBeVisible();
  await link.focus();
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(base + "/learn/hindi/conversation/");
  await context.close();
});

test("J9 home Hindi practice validates the displayed phrase", async ({ page }) => {
  await page.goto(base + "/");
  const card = page.locator('[data-hf-practice]');
  const input = card.getByLabel('Type the phrase above (Hindi or Roman letters)');
  const feedback = card.locator('[data-hf-type-msg]');
  await input.fill('this is wrong');
  await card.getByRole('button', { name: 'Check answer' }).click();
  await expect(input).toHaveAttribute('aria-invalid', 'true');
  await expect(feedback).toContainText('Not quite');
  const phrase = await card.locator('[data-hf-word]').textContent();
  await input.fill(phrase);
  await expect(feedback).toBeEmpty();
  await input.press('Enter');
  await expect(feedback).toContainText('Correct!');
  await expect(card.locator('[data-hf-word]')).toHaveText(phrase);
  await card.getByRole('button', { name: 'Next word' }).click();
  await expect(input).toHaveValue('');
  await expect(feedback).toBeEmpty();
  await input.fill(phrase);
  await input.press('Enter');
  await expect(input).toHaveAttribute('aria-invalid', 'true');
});

for (const width of [390, 1280]) {
  test(`J10 join wizard ships its real stylesheet at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    const cssResponse = page.waitForResponse((r) => new URL(r.url()).pathname === '/css/join-wizard.css');
    await page.goto(base + '/join.html');
    expect((await cssResponse).status()).toBe(200);
    await expect(page.locator('#jw')).toHaveClass(/jw-on/);
    await expect(page.locator('.jw-next')).toBeVisible();
    await expect(page.locator('.jw-fallback')).toBeHidden();
    const layout = await page.locator('#jw').evaluate((el) => ({
      maxWidth: getComputedStyle(el).maxWidth,
      overflow: document.documentElement.scrollWidth > innerWidth + 1,
      nextHeight: el.querySelector('.jw-next').getBoundingClientRect().height,
    }));
    expect(layout.maxWidth).toBe('1120px');
    expect(layout.overflow).toBe(false);
    expect(layout.nextHeight).toBeGreaterThanOrEqual(44);
    await page.locator('.jw-next').click();
    await expect(page.locator('#jw-step-1')).toBeVisible();
    await expect(page.locator('#jw-step-1 [data-jw-summary]')).toBeVisible();
  });
}

// Learners can distinguish free self-study from optional Hindi tutoring on
// both layouts, without any popup, login, payment or invented availability.
for (const width of [390, 1280]) {
  test(`Hindi learner next step stays optional at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 844 });
    for (const route of ['/learn/', '/learn/hindi/']) {
      await page.goto(base + route);
      const offer = page.locator('[data-eg-hindi-help]');
      await expect(offer.getByRole('heading', { name: 'Want help speaking Hindi?' })).toBeVisible();
      await expect(offer).toContainText('a request is not a confirmed booking');
      await expect(offer.getByRole('link', { name: 'continue learning Hindi for free' })).toBeVisible();
      const cta = offer.getByRole('link', { name: 'Compare Hindi tutor profiles' });
      await cta.scrollIntoViewIfNeeded();
      const box = await cta.boundingBox();
      expect(box.x).toBeGreaterThanOrEqual(0);
      expect(box.x + box.width).toBeLessThanOrEqual(width + 1);
      await cta.click();
      await expect(page).toHaveURL(/find-tutors\.html$/);
      await expect(page.locator('#f-q')).toBeVisible();
    }
  });
}

for (const width of [390, 1280]) {
  test(`Hindi name card is a real free PNG at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 844 });
    // Exercise deterministic offline spelling, not the availability of Google.
    await page.route('https://inputtools.google.com/**', route => route.abort());
    await page.goto(base + '/name-in-hindi/');
    await page.locator('#nameIn').fill('Sarah');
    await expect(page.locator('#out .big')).not.toHaveText('आपका नाम');
    const button = page.getByRole('button', { name: 'Download name card (PNG)' });
    await expect(button).toBeVisible();
    const pending = page.waitForEvent('download');
    await button.click();
    const download = await pending;
    expect(download.suggestedFilename()).toBe('ekguru-name-card.png');
    const png = readFileSync(await download.path());
    expect(png.subarray(0, 8).toString('hex')).toBe('89504e470d0a1a0a');
    expect(png.readUInt32BE(16)).toBe(1200);
    expect(png.readUInt32BE(20)).toBe(630);
    expect(png.length).toBeGreaterThan(10000);
    await expect(page.locator('#name-card-status')).toContainText('download started');
    await expect(button).toBeEnabled();
    const support = page.getByRole('link', { name: 'Support EkGuru — optional', exact: true });
    await expect(support).toHaveAttribute('href', '../support/');
    expect(await page.locator('script[src*="adsbygoogle"]').count()).toBe(0);
  });
}
