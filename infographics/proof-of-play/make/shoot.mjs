import { chromium } from 'playwright-core';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
await p.goto('file://' + process.cwd() + '/proof-of-play.html');
await p.waitForTimeout(900);
const m = await p.evaluate(() => {
  const c = document.querySelector('.card');
  const f = document.querySelector('.foot').getBoundingClientRect();
  const field = document.querySelector('.field').getBoundingClientRect();
  return { scrollH: c.scrollHeight, footBottom: Math.round(f.bottom), dots: document.querySelectorAll('.field i').length, fieldW: Math.round(field.width), fieldH: Math.round(field.height) };
});
console.log(JSON.stringify(m));
await p.screenshot({ path: 'proof-of-play.png', clip: { x: 0, y: 0, width: 1080, height: 1350 } });
await b.close();
