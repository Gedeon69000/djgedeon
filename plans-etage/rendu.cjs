// Rendu PNG + PDF (A3 paysage) des plans SVG via Chromium/Playwright.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = __dirname;
  const svgs = ['plan_cote.svg', 'plan_amenagement.svg'];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 990 }, deviceScaleFactor: 2 });
  for (const f of svgs) {
    await page.setContent(`<html><body style="margin:0">${fs.readFileSync(path.join(dir, f), 'utf8')}</body></html>`);
    await page.screenshot({ path: path.join(dir, f.replace('.svg', '.png')), clip: { x: 0, y: 0, width: 1400, height: 990 } });
  }
  const pages = svgs.map(f => `<div class="p">${fs.readFileSync(path.join(dir, f), 'utf8')}</div>`).join('');
  await page.setContent(`<html><head><style>@page{size:420mm 297mm;margin:0}body{margin:0}
    .p{width:420mm;height:297mm;page-break-after:always;overflow:hidden}.p svg{width:420mm;height:297mm}</style></head>
    <body>${pages}</body></html>`);
  await page.pdf({ path: path.join(dir, 'plans_etage_A3.pdf'), width: '420mm', height: '297mm', printBackground: true });
  await browser.close();
  console.log('rendu ok');
})();
