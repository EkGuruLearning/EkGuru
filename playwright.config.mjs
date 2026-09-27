import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "tools",
  testMatch: "test-journeys.mjs",
  timeout: 60000,
  use: { baseURL: process.env.EKGURU_BASE || "http://127.0.0.1:4173" },
  webServer: {
    command: "python3 -m http.server 4173 --bind 0.0.0.0",
    port: 4173,
    reuseExistingServer: true,
  },
});
