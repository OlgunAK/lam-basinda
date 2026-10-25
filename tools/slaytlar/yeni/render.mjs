// Renders slide HTML pages to 1920x1080 JPGs and warns about overflowing content.
// Usage: node render.mjs jobs.json   (jobs: [[htmlPath, jpgPath], ...])
import { readFileSync } from "fs";
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const jobs = JSON.parse(readFileSync(process.argv[2], "utf8"));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
let warn = 0;
for (const [src, out] of jobs) {
  await page.goto("file://" + src);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => [...document.images].every((i) => i.complete));
  const issues = await page.evaluate(() => {
    const r = [];
    const body = document.querySelector(".body");
    const t = document.querySelector("h1.t");
    if (t && t.getBoundingClientRect().bottom > 186) r.push("title too tall");
    if (body) {
      const b = body.getBoundingClientRect();
      for (const el of body.querySelectorAll("*")) {
        const e = el.getBoundingClientRect();
        if (e.width === 0) continue;
        if (e.bottom > b.bottom + 3 || e.right > b.right + 3) { r.push("outside body: " + el.className + " " + (el.textContent || "").slice(0, 40)); break; }
      }
    }
    for (const el of document.querySelectorAll(".box,.pato,.cap,.opt span,.live")) {
      if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2) r.push("clipped: " + el.className + " " + el.textContent.slice(0, 40));
    }
    const f = document.querySelector(".foot"), c = document.querySelector(".cred");
    if (f && c && f.getBoundingClientRect().right > c.getBoundingClientRect().left + (c.getBoundingClientRect().width - c.scrollWidth)) {
      // footer strip running under the credit line
      const fr = f.getBoundingClientRect().right;
      const range = document.createRange(); range.selectNodeContents(c);
      const cl = range.getBoundingClientRect().left;
      if (fr > cl - 10) r.push("footer overlaps credits");
    }
    return r;
  });
  if (issues.length) { warn++; console.log("UYARI " + src.split("/").slice(-2).join("/") + ": " + issues.join(" | ")); }
  await page.screenshot({ path: out, type: "jpeg", quality: 90 });
}
await browser.close();
console.log(`render: ${jobs.length} slayt${warn ? `, ${warn} uyarı` : ""}`);
