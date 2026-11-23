import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './e2e',
  use: { baseURL: 'http://127.0.0.1:4200', browserName: 'chromium' },
  webServer: [
    { command: 'uv run --frozen uvicorn services.api.app.main:app --host 127.0.0.1 --port 8000', cwd: '../..', url: 'http://127.0.0.1:8000/api/v1/health', reuseExistingServer: false },
    { command: 'npm start', url: 'http://127.0.0.1:4200', reuseExistingServer: false },
  ],
});
