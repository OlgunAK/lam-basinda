// Kaynak dosyadan (canli/dersler/kaynak/<ID>.json) slayt JPG'lerini ve canlı ders dosyasını üretir.
// Kullanım: node tools/slaytlar/ciz.mjs M3 [M4 ...]   (yalnız bazı kareler: M3:05,06)
import { createServer } from "http";
import { readFileSync, writeFileSync, readdirSync, unlinkSync, mkdirSync, existsSync } from "fs";
import { join, extname, dirname } from "path";
import { fileURLToPath } from "url";
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const REPO = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const TUR = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".jpg": "image/jpeg", ".png": "image/png", ".woff2": "font/woff2", ".svg": "image/svg+xml", ".css": "text/css" };
const srv = createServer((q, r) => {
  const p = join(REPO, decodeURIComponent(q.url.split("?")[0]));
  let veri;
  try { veri = readFileSync(p); } catch { console.log("EKSİK", q.url); r.writeHead(404); r.end(); return; }
  r.writeHead(200, { "content-type": TUR[extname(p)] || "application/octet-stream" }); r.end(veri);
}).listen(0);
const port = srv.address().port;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on("pageerror", e => console.log("HATA", e.message));
await p.goto(`http://127.0.0.1:${port}/duzenle/cizim.html`);
for (const arg of process.argv.slice(2)) {
  const [id, only] = arg.split(":");
  const sec = only ? new Set(only.split(",")) : null;
  const kareler = await p.evaluate(id => window.yukle(id), id);
  const dir = join(REPO, "canli", "slaytlar", id); mkdirSync(dir, { recursive: true });
  let n = 0, uyari = 0;
  for (let i = 0; i < kareler.length; i++) {
    const k = kareler[i];
    if (!k.gorsel) continue;
    if (sec && ![...sec].some(s => k.ad.startsWith(s))) continue;
    const u = await p.evaluate(i => window.goster(i), i);
    if (u.length) { uyari++; console.log("UYARI", id, k.ad, u.join(" | ")); }
    await p.screenshot({ path: join(dir, k.ad), type: "jpeg", quality: 88, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    n++;
  }
  if (!sec) {
    const keep = new Set(kareler.filter(k => k.gorsel).map(k => k.ad));
    for (const f of readdirSync(dir)) if (!keep.has(f)) unlinkSync(join(dir, f));
  }
  const L = await p.evaluate(() => window.canliJSON());
  writeFileSync(join(REPO, "canli", "dersler", id + ".json"), JSON.stringify(L, null, 1));
  const idxP = join(REPO, "canli", "dersler", "index.json");
  const idx = JSON.parse(readFileSync(idxP, "utf8"));
  const e = idx.find(x => x.id === id);
  const rec = { id, title: L.title, date: L.date, n: L.questions.length };
  if (e) Object.assign(e, rec); else idx.push(rec);
  writeFileSync(idxP, JSON.stringify(idx, null, 1));
  console.log(`${id}: ${n} kare çizildi${uyari ? `, ${uyari} uyarı` : ""}; süre ${L.duration}`);
}
await b.close(); srv.close();
