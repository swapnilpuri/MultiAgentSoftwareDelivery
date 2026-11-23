import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';
import { API_BASE_URL, RuntimeConfig } from './app/api-config';

async function main(): Promise<void> {
  const response = await fetch('/config.json');
  if (!response.ok) throw new Error('Runtime configuration unavailable');
  const config: RuntimeConfig = await response.json();
  if (typeof config.apiBaseUrl !== 'string' || !config.apiBaseUrl)
    throw new Error('Invalid API URL');
  await bootstrapApplication(App, {
    providers: [
      ...appConfig.providers,
      { provide: API_BASE_URL, useValue: config.apiBaseUrl.replace(/\/$/, '') },
    ],
  });
}
main().catch(() => {
  const root = document.querySelector('app-root');
  if (root)
    root.textContent = 'Application configuration unavailable. Check config.json and reload.';
});
