/**
 *   node render.mjs icons <job.json>   # build.py 가 부른다 — 아이콘 PNG 굽기
 *   node render.mjs images <job.json>  # build.py 가 부른다 — 삽화 PNG 굽기
 *   node render.mjs preview [3 7 ...]  # preview/png/slide-NN.png 로 장마다 찍기
 */
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { mkdir, readFile } from "node:fs/promises";

const here = path.dirname(fileURLToPath(import.meta.url));
const [mode, ...rest] = process.argv.slice(2);
const browser = await chromium.launch({ channel: "chrome" });

if (mode === "icons") {
  const jobs = JSON.parse(await readFile(rest[0], "utf8"));
  await mkdir(path.join(here, "assets", "icons"), { recursive: true });
  const page = await browser.newPage({ deviceScaleFactor: 4 });
  for (const j of jobs) {
    await page.setContent(`<html><body style="margin:0;background:transparent"><div id="i" style="width:24px;height:24px;color:${j.color}">${j.svg}</div></body></html>`);
    await page.locator("#i").screenshot({ path: j.out, omitBackground: true });
  }
  console.log(`icons: ${jobs.length} rendered`);
} else if (mode === "images") {
  // 삽화: 2배 해상도로 굽는다 (슬라이드에서 선명하게)
  const jobs = JSON.parse(await readFile(rest[0], "utf8"));
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  for (const j of jobs) {
    await page.setViewportSize({ width: j.w, height: j.h });
    await page.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet"><style>body{margin:0;background:transparent;font-family:'Noto Sans KR',sans-serif}</style></head><body><div id="i" style="width:${j.w}px;height:${j.h}px;position:relative;overflow:hidden">${j.html}</div></body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);
    await page.locator("#i").screenshot({ path: j.out, omitBackground: !!j.transparent });
    console.log(`image: ${path.basename(j.out)}`);
  }
} else {
  const outDir = path.join(here, "preview", "png");
  await mkdir(outDir, { recursive: true });
  const only = rest.map(Number).filter(Boolean);
  const page = await browser.newPage({ deviceScaleFactor: 1, viewport: { width: 1320, height: 800 } });
  await page.goto("file://" + path.join(here, "preview", "index.html"));
  await page.waitForTimeout(1200); // 웹폰트
  const n = await page.locator("section.slide").count();
  for (let i = 1; i <= n; i++) {
    if (only.length && !only.includes(i)) continue;
    await page.locator(`#s${i}`).screenshot({ path: path.join(outDir, `slide-${String(i).padStart(2, "0")}.png`) });
  }
  console.log(`preview: ${only.length || n} slides → ${outDir}`);
}
await browser.close();
