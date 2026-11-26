// Graba un reel cuadro a cuadro: escenas.html + Playwright (headless) -> ffmpeg.
// Uso: node render.mjs <video> <carpeta-trabajo> [--cuadros 1.2,5,9.8]   (con --cuadros solo saca esas imágenes)
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const raiz = path.resolve(aqui, "../..");
const [video, trabajoArg, flag, lista] = process.argv.slice(2);
if (!video || !trabajoArg) { console.error("Uso: node render.mjs <video> <trabajo> [--cuadros t1,t2]"); process.exit(1); }
const trabajo = path.resolve(trabajoArg, video);
const FPS = 30;
const FFMPEG = process.env.FFMPEG || "ffmpeg";
const tiempos = JSON.parse(fs.readFileSync(path.join(trabajo, "tiempos.json"), "utf8"));

// servidor local de solo lectura, solo con lo que usa el render: escenas, letra, páginas de ejemplo y fotos
const PERMITIDO = /^\/(tools\/reels\/(escenas\.html|DMSans\.ttf)|plantillas\/[a-z-]+\.html|img\/[\w\/.-]+\.(jpe?g|png|webp|svg))$/;
const TIPOS = { ".html": "text/html; charset=utf-8", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".svg": "image/svg+xml", ".ttf": "font/ttf" };
const raizReal = fs.realpathSync(raiz);
const srv = http.createServer((req, res) => {
  let u;
  try { u = decodeURIComponent(new URL(req.url, "http://x").pathname); } catch { res.writeHead(400); return res.end(); }
  if (!PERMITIDO.test(u) || u.includes("..")) { res.writeHead(404); return res.end(); }
  let f;
  try { f = fs.realpathSync(path.join(raizReal, u)); } catch { res.writeHead(404); return res.end(); }
  if (!f.startsWith(raizReal + path.sep) || !fs.statSync(f).isFile()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "content-type": TIPOS[path.extname(f).toLowerCase()] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});
await new Promise(r => srv.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${srv.address().port}`;

let b, ff;
try {
  b = await chromium.launch({ headless: true });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  // sin internet: las letras de Google de las páginas de ejemplo no deben trabar la carga
  await p.route(/^https?:\/\/(?!127\.0\.0\.1)/, r => r.request().url().includes("fonts.g") ? r.continue() : r.abort());
  p.on("pageerror", e => { console.error("Error en la página:", e.message); process.exitCode = 1; });
  await p.goto(`${base}/tools/reels/escenas.html`, { waitUntil: "load" });
  const eventos = await p.evaluate(([n, t]) => window.preparar(n, t), [video, tiempos]);
  fs.writeFileSync(path.join(trabajo, "sonidos.json"), JSON.stringify(eventos));
  const total = Math.round(tiempos.total * FPS);
  if (flag === "--cuadros") {
    for (const s of lista.split(",").map(Number)) {
      await p.evaluate(t => window.render(t), s);
      await p.screenshot({ path: path.join(trabajo, `cuadro-${s.toFixed(2)}.png`) });
    }
  } else {
    const salida = path.join(trabajo, "video-mudo.mp4");
    ff = spawn(FFMPEG, ["-y", "-hide_banner", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
      "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-pix_fmt", "yuv420p", "-r", String(FPS), salida], { stdio: ["pipe", "inherit", "inherit"] });
    const fin = new Promise((ok, mal) => {
      ff.on("error", e => mal(new Error(`no se pudo abrir ffmpeg (${FFMPEG}): ${e.message}`)));
      ff.on("close", c => c === 0 ? ok() : mal(new Error("ffmpeg salió con " + c)));
    });
    let roto = null;
    fin.catch(e => { roto = e; });
    ff.stdin.on("error", e => { roto = roto || new Error("ffmpeg cerró la entrada: " + e.message); });
    const escribir = buf => new Promise((ok, mal) => {
      if (roto) return mal(roto);
      const listo = () => { limpiar(); ok(); };
      const falla = e => { limpiar(); mal(roto || e); };
      const limpiar = () => { ff.stdin.off("drain", listo); ff.stdin.off("error", falla); ff.off("close", cerro); };
      const cerro = () => falla(new Error("ffmpeg se cerró antes de tiempo"));
      if (ff.stdin.write(buf)) return ok();
      ff.stdin.once("drain", listo); ff.stdin.once("error", falla); ff.once("close", cerro);
    });
    for (let i = 0; i < total; i++) {
      await p.evaluate(t => window.render(t), i / FPS);
      const buf = await p.screenshot({ type: "jpeg", quality: 93 });
      await escribir(buf);
      if (i % 150 === 0) console.log(`${video}: ${i}/${total}`);
    }
    if (roto) throw roto;
    ff.stdin.end();
    await fin;
    console.log("listo", salida);
  }
} finally {
  if (ff && ff.exitCode === null && !ff.stdin.writableEnded) ff.kill();
  if (b) await b.close().catch(() => {});
  srv.close();
}
