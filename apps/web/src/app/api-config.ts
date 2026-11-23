import { InjectionToken } from '@angular/core';
// Same-origin /api uses the development proxy. Override via runtime config.json.
export const API_BASE_URL = new InjectionToken<string>('API_BASE_URL');
export interface RuntimeConfig {
  apiBaseUrl: string;
}
