// Saca capturas de celular (390 px, x2) de las páginas de ejemplo para los reels.
// Uso: node capturar_paginas.mjs <carpeta-salida> panaderia barberia ...
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const [out, ...nombres] = process.argv.slice(2);
if (!out || !nombres.length) { console.error("Uso: node capturar_paginas.mjs <salida> <pagina...>"); process.exit(1); }
const ALTO = 3400; // px css que se capturan de cada página

const b = await chromium.launch({ headless: true, executablePath: process.env.PW_CHROME || undefined });
try {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  for (const n of nombres) {
    if (!/^[a-z-]+$/.test(n)) throw new Error("nombre raro: " + n);
    const p = await ctx.newPage();
    await p.goto(pathToFileURL(path.join(aqui, "../../plantillas", n + ".html")).href, { waitUntil: "load", timeout: 30000 });
    await p.addStyleTag({ content: "*,*::before,*::after{animation:none!important;transition:none!important}.fade,.rv{opacity:1!important;transform:none!important}#sy-cotiza{display:none!important}" });
    await p.evaluate(async () => { for (let y = 0; y < 5000; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); });
    await p.evaluate(() => Promise.race([
      Promise.all([...document.images].map(i => { i.loading = "eager"; return i.complete ? 0 : new Promise(r => { i.addEventListener("load", r); i.addEventListener("error", r); }); })),
      new Promise(r => setTimeout(r, 8000)),
    ]));
    await p.waitForTimeout(400);
    const h = await p.evaluate(() => document.documentElement.scrollHeight);
    await p.screenshot({ path: path.join(out, n + ".jpg"), type: "jpeg", quality: 88, fullPage: true, clip: { x: 0, y: 0, width: 390, height: Math.min(h, ALTO) } });
    console.log(n, Math.min(h, ALTO));
    await p.close();
  }
} finally { await b.close(); }
