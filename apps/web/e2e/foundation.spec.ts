import { expect, test } from '@playwright/test';
test('control center calls the real API and navigates', async ({ page }) => {
  const health = page.waitForResponse(response => response.url().endsWith('/api/v1/health'));
  await page.goto('/');
  expect((await health).status()).toBe(200);
  await expect(page.getByRole('status')).toHaveText('Backend: connected');
  await expect(page.getByRole('heading', { name: 'Your delivery workspace' })).toBeVisible();
  await page.getByRole('link', { name: 'AI Chat', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'AI Chat', exact: true })).toBeVisible();
  await expect(page.getByText('No integration or execution', { exact: false })).toBeVisible();
  await page.reload();
  await expect(page.getByRole('heading', { name: 'AI Chat', exact: true })).toBeVisible();
  await page.screenshot({ path: '../../artifacts/m0-control-center.png', fullPage: true });
});
