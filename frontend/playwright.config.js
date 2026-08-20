import { defineConfig, devices } from "@playwright/test";

const FRONTEND_URL = "http://127.0.0.1:5173";
const BACKEND_URL = "http://127.0.0.1:8000";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  workers: 1,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : [["list"]],
  timeout: 30_000,
  expect: { timeout: 7_000 },
  use: {
    baseURL: FRONTEND_URL,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: [
    {
      command:
        "uv run --project ../backend uvicorn studio.api.app:app --host 127.0.0.1 --port 8000",
      url: `${BACKEND_URL}/api/health`,
      reuseExistingServer: !process.env.CI,
      timeout: 60_000,
      env: { STUDIO_STORAGE: "memory" },
    },
    {
      command: "npm run dev -- --host 127.0.0.1 --port 5173",
      url: FRONTEND_URL,
      reuseExistingServer: !process.env.CI,
      timeout: 60_000,
      env: { STUDIO_NO_BROWSER: "true", STUDIO_API_URL: BACKEND_URL },
    },
  ],
});
