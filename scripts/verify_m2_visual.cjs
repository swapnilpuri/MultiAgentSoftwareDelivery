// Requires masd-web's pinned Playwright install and the explicitly configured M2 stack.
const fs = require('node:fs');
const path = require('node:path');
const workspace = path.resolve(process.argv[2] || path.join(__dirname, '../..'));
const { chromium } = require(path.join(workspace, 'masd-web/node_modules/playwright'));
const output = path.resolve(__dirname, '../artifacts/m2-implementation');

(async () => {
  const login = JSON.parse(fs.readFileSync(path.join(workspace, 'masd-infrastructure/artifacts/m2-human-login.json'), 'utf8'));
  const record = JSON.parse(fs.readFileSync(path.join(output, 'browser-baseline.json'), 'utf8'));
  const uuid = '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}';
  const match = new RegExp(`^/api/v1/projects/(${uuid})/requirements/sessions/(${uuid})$`).exec(record.path);
  if (!match) throw new Error('Acceptance record must identify a local requirements session');
  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 950 } });
    const response = await context.request.post('http://127.0.0.1:4400/api/v1/auth/session', {
      headers: { 'X-MASD-Request': 'requirements-studio' }, data: login,
    });
    if (response.status() !== 200) throw new Error('Configured test-human login failed');
    const page = await context.newPage();
    await page.goto(`http://127.0.0.1:4400/projects/${match[1]}/requirements/${match[2]}`);
    await page.getByLabel('Product overview', { exact: true }).waitFor();
    fs.mkdirSync(output, { recursive: true });
    await page.screenshot({ path: path.join(output, 'studio-desktop.png') });
    await page.setViewportSize({ width: 390, height: 844 });
    if (await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)) {
      throw new Error('Requirements Studio has horizontal overflow at 390px');
    }
    await page.screenshot({ path: path.join(output, 'studio-mobile.png') });
    console.log('PASS: desktop/390px mobile rendering; no horizontal overflow; screenshots retained');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
