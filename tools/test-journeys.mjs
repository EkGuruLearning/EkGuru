/**
 * Five public journeys, run in CI with Playwright when Chromium is installed.
 * This file does not pretend a pass if the browser is missing.
 *
 *   npx playwright test tools/test-journeys.mjs
 */
import { test, expect } from "@playwright/test";

const base = process.env.EKGURU_BASE || "http://127.0.0.1:4173";

async function noDead(page) {
  const hrefs = await page.$$eval("a[href]", (as) => as.map((a) => a.getAttribute("href")).filter(Boolean));
  const bad = hrefs.filter((h) => h === "#" || h.startsWith("javascript:"));
  expect(bad, "placeholder links").toEqual([]);
}

test("J1 home to learn to a guide", async ({ page }) => {
  await page.goto(base + "/");
  await expect(page.locator("h1")).toHaveCount(1);
  await expect(page.locator("#stat-tutors")).not.toHaveText("0");
  await page.locator("header nav").getByRole("link", { name: "Learn", exact: true }).click();
  await expect(page).toHaveURL(/\/learn\/$/);
  await page.getByRole("link", { name: /Hindi Alphabet/i }).first().click();
  await expect(page.locator("h1")).toHaveCount(1);
  await noDead(page);
});

test("J2 home to tutors", async ({ page }) => {
  await page.goto(base + "/find-tutors.html");
  await expect(page.locator("h1")).toHaveCount(1);
  await expect(page.getByText("Hemlata")).toHaveCount(0);
  await expect(page.getByText("Tara")).toHaveCount(0);
  await page.getByRole("link", { name: /Sushila/i }).first().click();
  await expect(page).toHaveURL(/sushila-g/);
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
  await expect(page.getByText(/Advertising is disabled/i)).toBeVisible();
  await page.goto(base + "/terms/");
  await expect(page.locator("h1")).toHaveCount(1);
  await page.goto(base + "/contact/");
  await expect(page.getByRole("link", { name: "support@ekguru.shop" })).toBeVisible();
  await expect(page.locator("#cf-name")).toBeVisible();
});

test("J5 mobile menu to learn", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(base + "/");
  await page.getByRole("button", { name: "Menu" }).click();
  await page.locator("header nav").getByRole("link", { name: "Learn", exact: true }).click();
  await expect(page).toHaveURL(/\/learn\/$/);
});
