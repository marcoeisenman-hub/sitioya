// Reel "A la medida" de @sitioya.pty (1080x1920, 30 fps, 25 s).
// Negocio de ejemplo genérico ("Tu negocio"): sin marcas, reseñas ni cifras inventadas.
// Precios y lo que trae cada plan: los mismos de https://sitioya.vercel.app
import React from "react";
import {
  AbsoluteFill, Audio, Img, Sequence, interpolate, random, spring,
  staticFile, useCurrentFrame, useVideoConfig, Easing,
} from "remotion";
import { loadFont } from "@remotion/fonts";
import linea from "./linea.json";

loadFont({ family: "DM Sans", url: staticFile("DMSans.ttf"), weight: "100 1000" });

const C = {
  bg: "#FFF6EC", ink: "#1B2A4A", soft: "#5B6680", coral: "#FF6B5B", coralD: "#E2503F",
  mint: "#7ED6C1", blush: "#FFE3DC", line: "#F0DFCC", sun: "#FFC94A", white: "#FFFFFF",
};
const FONT = "'DM Sans', sans-serif";
const E = linea.escenas;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const useSpring = (delay = 0, cfg: { damping?: number; stiffness?: number; mass?: number } = {}) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  return spring({ frame: f - delay, fps, config: { damping: 12, stiffness: 160, ...cfg } });
};

// --- fondo con 2 círculos que flotan (igual que los posts) ---
const Fondo: React.FC = () => {
  const f = useCurrentFrame();
  const a = Math.sin(f / 40) * 40, b = Math.cos(f / 50) * 50;
  return (
    <AbsoluteFill style={{ background: C.bg, overflow: "hidden" }}>
      <div style={{ position: "absolute", width: 1100, height: 1100, borderRadius: "50%", background: C.blush, left: -520 + a, top: 900 + b }} />
      <div style={{ position: "absolute", width: 1000, height: 1000, borderRadius: "50%", background: "#DDF4EC", right: -560 - b, top: -260 + a }} />
    </AbsoluteFill>
  );
};

const Pill: React.FC<{ children: React.ReactNode; bg?: string; color?: string; size?: number; style?: React.CSSProperties }> = ({ children, bg = C.coral, color = C.ink, size = 40, style }) => (
  <div style={{ display: "inline-block", background: bg, color, fontWeight: 800, fontSize: size, padding: `${size * 0.35}px ${size * 0.8}px`, borderRadius: 999, letterSpacing: 1, ...style }}>{children}</div>
);

const Logo: React.FC<{ size?: number }> = ({ size = 90 }) => (
  <div style={{ display: "flex", alignItems: "center", gap: size * 0.2 }}>
    <Img src={staticFile("favicon.svg")} style={{ width: size, height: size }} />
    <div style={{ fontSize: size * 0.62, fontWeight: 800, color: C.ink }}>Sitio<span style={{ color: C.coral }}>Ya</span></div>
  </div>
);

// --- franja coral que barre la pantalla en cada cambio de escena ---
const Barrido: React.FC<{ at: number }> = ({ at }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [at - 10, at + 10], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  if (p <= 0 || p >= 1) return null;
  const x = interpolate(p, [0, 1], [-2600, 1400]);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", top: -400, left: x, width: 1300, height: 2800, background: C.coral, transform: "rotate(14deg)" }} />
      <div style={{ position: "absolute", top: -400, left: x + 1300, width: 160, height: 2800, background: C.ink, transform: "rotate(14deg)" }} />
    </AbsoluteFill>
  );
};

// ===== 1) Gancho =====
const Gancho: React.FC = () => {
  const f = useCurrentFrame();
  const palabras = [["¿Tu", C.ink], ["negocio", C.ink], ["todavía", C.ink], ["no", C.ink], ["tiene", C.ink]] as const;
  const golpe = useSpring(31, { damping: 8, stiffness: 220 });
  const pill = useSpring(36);
  const temblor = f >= 31 && f < 40 ? Math.sin(f * 3) * (40 - f) * 1.2 : 0;
  return (
    <AbsoluteFill style={{ justifyContent: "center", padding: "0 80px", transform: `translateX(${temblor}px)` }}>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "0 28px", fontSize: 150, fontWeight: 900, lineHeight: 1.02, letterSpacing: -4 }}>
        {palabras.map(([w, col], i) => {
          const s = spring({ frame: f - 4 - i * 5, fps: 30, config: { damping: 10, stiffness: 200 } });
          return <span key={i} style={{ color: col, transform: `translateY(${(1 - s) * 120}px) scale(${0.4 + s * 0.6})`, opacity: s, display: "inline-block" }}>{w}</span>;
        })}
      </div>
      <div style={{ fontSize: 190, fontWeight: 900, color: C.coral, letterSpacing: -6, lineHeight: 1, transform: `scale(${0.2 + golpe * 0.8}) rotate(${(1 - golpe) * -10}deg)`, transformOrigin: "left center", opacity: golpe > 0.01 ? 1 : 0 }}>
        página web?
      </div>
      <div style={{ marginTop: 70, transform: `scale(${pill})`, transformOrigin: "left center" }}>
        <Pill bg={C.ink} color={C.white} size={44}>Para negocios en Panamá</Pill>
      </div>
    </AbsoluteFill>
  );
};

// ===== 2) A la medida: cinta métrica + celular que se arma solo =====
const Cinta: React.FC<{ start: number }> = ({ start }) => {
  const f = useCurrentFrame();
  const w = interpolate(f, [start, start + 18], [0, 920], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <div style={{ position: "absolute", left: 80, top: 470, width: w, height: 90, background: C.sun, borderRadius: 14, overflow: "hidden", boxShadow: "0 10px 0 rgba(27,42,74,.12)" }}>
      {Array.from({ length: 47 }).map((_, i) => (
        <div key={i} style={{ position: "absolute", left: 14 + i * 19.5, top: 0, width: 4, height: i % 5 === 0 ? 46 : 24, background: C.ink, borderRadius: 2 }}>
          {i % 10 === 0 && <div style={{ position: "absolute", top: 48, left: -8, fontSize: 26, fontWeight: 800, color: C.ink }}>{i / 10}</div>}
        </div>
      ))}
    </div>
  );
};

const Bloque: React.FC<{ d: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ d, children, style }) => {
  const s = useSpring(d, { damping: 11, stiffness: 190 });
  return <div style={{ transform: `translateY(${(1 - s) * 60}px) scale(${0.6 + s * 0.4})`, opacity: Math.min(1, s * 1.4), ...style }}>{children}</div>;
};

const Etiqueta: React.FC<{ d: number; lado: "izq" | "der"; top: number; texto: string; color?: string }> = ({ d, lado, top, texto, color = C.coral }) => {
  const s = useSpring(d, { damping: 9, stiffness: 180 });
  const x = (1 - s) * (lado === "izq" ? -700 : 700);
  return (
    <div style={{ position: "absolute", top, [lado === "izq" ? "left" : "right"]: 40, transform: `translateX(${x}px) rotate(${lado === "izq" ? -4 : 4}deg)` }}>
      <Pill bg={color} color={color === C.ink ? C.white : C.ink} size={38} style={{ boxShadow: "0 8px 0 rgba(27,42,74,.18)" }}>{texto}</Pill>
    </div>
  );
};

const Medida: React.FC = () => {
  const f = useCurrentFrame();
  const t1 = useSpring(2), t2 = useSpring(8, { damping: 9 });
  const cel = useSpring(30, { damping: 14, stiffness: 120 });
  const boton = useSpring(120, { damping: 6, stiffness: 260 });
  const late = f > 130 ? 1 + Math.sin((f - 130) / 4) * 0.03 : 1;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", top: 150, left: 80, right: 80 }}>
        <div style={{ fontSize: 110, fontWeight: 900, color: C.ink, letterSpacing: -3, transform: `translateX(${(1 - t1) * -900}px)` }}>Te la hacemos</div>
        <div style={{ fontSize: 150, fontWeight: 900, color: C.coral, letterSpacing: -5, lineHeight: 1, transform: `scale(${t2})`, transformOrigin: "left center" }}>a la medida</div>
      </div>
      <Cinta start={10} />
      {/* celular */}
      <div style={{ position: "absolute", left: 250, top: 620, width: 580, height: 1130, borderRadius: 80, background: C.ink, padding: 22, transform: `translateY(${(1 - cel) * 1400}px) rotate(${(1 - cel) * 12}deg)` }}>
        <div style={{ width: "100%", height: "100%", borderRadius: 60, background: C.bg, overflow: "hidden", padding: "70px 34px 0", display: "flex", flexDirection: "column", gap: 22 }}>
          <Bloque d={45}>
            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <div style={{ width: 64, height: 64, borderRadius: 20, background: C.coral }} />
              <div style={{ fontSize: 40, fontWeight: 900, color: C.ink }}>Tu negocio</div>
            </div>
          </Bloque>
          <Bloque d={60}>
            <div style={{ height: 270, borderRadius: 30, background: `linear-gradient(135deg, ${C.blush}, ${C.coral})`, position: "relative", overflow: "hidden" }}>
              <div style={{ position: "absolute", width: 150, height: 150, borderRadius: "50%", background: C.sun, right: 40, top: 40 }} />
              <div style={{ position: "absolute", width: 600, height: 300, borderRadius: "50%", background: C.mint, left: -120, top: 170 }} />
            </div>
          </Bloque>
          {[75, 82, 89].map((d, i) => (
            <Bloque key={i} d={d}>
              <div style={{ display: "flex", alignItems: "center", gap: 18, background: C.white, borderRadius: 22, padding: "16px 18px" }}>
                <div style={{ width: 70, height: 70, borderRadius: 16, background: [C.sun, C.mint, C.blush][i] }} />
                <div style={{ flex: 1 }}>
                  <div style={{ height: 18, width: "80%", background: C.ink, borderRadius: 9, opacity: 0.85 }} />
                  <div style={{ height: 14, width: "50%", background: C.soft, borderRadius: 7, opacity: 0.4, marginTop: 10 }} />
                </div>
                <div style={{ fontSize: 34, fontWeight: 900, color: C.coral }}>$</div>
              </div>
            </Bloque>
          ))}
          <Bloque d={105}>
            <div style={{ display: "flex", gap: 16 }}>
              <div style={{ flex: 1, background: C.white, borderRadius: 22, padding: 18, fontSize: 26, fontWeight: 800, color: C.ink }}>Horario<div style={{ height: 12, width: "70%", background: C.soft, opacity: .35, borderRadius: 6, marginTop: 10 }} /></div>
              <div style={{ width: 140, borderRadius: 22, background: "#DDF4EC", position: "relative" }}>
                <div style={{ position: "absolute", left: 50, top: 18, width: 40, height: 40, borderRadius: "50% 50% 50% 0", transform: "rotate(-45deg)", background: C.coral }} />
              </div>
            </div>
          </Bloque>
          <div style={{ transform: `scale(${boton * late})`, background: C.coral, borderRadius: 999, padding: "22px 0", textAlign: "center", fontSize: 32, fontWeight: 900, color: C.ink }}>
            Escríbenos por WhatsApp
          </div>
        </div>
      </div>
      <Etiqueta d={58} lado="izq" top={760} texto="Tus colores" color={C.sun} />
      <Etiqueta d={70} lado="der" top={930} texto="Tus fotos" color={C.mint} />
      <Etiqueta d={85} lado="izq" top={1180} texto="Tus precios" />
      <Etiqueta d={100} lado="der" top={1500} texto="Horario y mapa" color={C.sun} />
      <Etiqueta d={122} lado="izq" top={1775} texto="Botón de WhatsApp" color={C.ink} />
    </AbsoluteFill>
  );
};

// ===== 3) Planes =====
const Contador: React.FC<{ hasta: number; d: number }> = ({ hasta, d }) => {
  const f = useCurrentFrame();
  const v = Math.round(interpolate(f, [d, d + 16], [0, hasta], { ...clamp, easing: Easing.out(Easing.quad) }));
  return <>${v}</>;
};

const Tarjeta: React.FC<{ d: number; nombre: string; precio: number; texto: string; nota?: string; oscura?: boolean }> = ({ d, nombre, precio, texto, nota, oscura }) => {
  const s = useSpring(d, { damping: 13, stiffness: 140 });
  const sello = useSpring(d + 63, { damping: 7, stiffness: 240 });
  const fg = oscura ? C.white : C.ink;
  return (
    <div style={{ position: "relative", background: oscura ? C.ink : C.white, borderRadius: 50, padding: "50px 56px", boxShadow: "0 16px 0 rgba(27,42,74,.12)", transform: `perspective(1400px) rotateY(${(1 - s) * 80}deg) translateX(${(1 - s) * 300}px)`, opacity: s > 0.02 ? 1 : 0 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <div style={{ fontSize: 70, fontWeight: 900, color: fg }}>{nombre}</div>
        <div style={{ fontSize: 130, fontWeight: 900, color: C.coral, letterSpacing: -4 }}><Contador hasta={precio} d={d + 15} /></div>
      </div>
      <div style={{ fontSize: 42, fontWeight: 600, color: oscura ? "#D9DEEA" : C.soft, lineHeight: 1.3, marginTop: 10 }}>{texto}</div>
      {nota && <div style={{ fontSize: 30, fontWeight: 600, color: oscura ? "#AEB6CB" : C.soft, marginTop: 18 }}>{nota}</div>}
      <div style={{ position: "absolute", right: 36, top: -34, transform: `scale(${sello}) rotate(6deg)` }}>
        <Pill bg={C.mint} size={30}>A tu medida</Pill>
      </div>
    </div>
  );
};

const Planes: React.FC = () => {
  const t = useSpring(2);
  return (
    <AbsoluteFill style={{ padding: "170px 70px 0" }}>
      <div style={{ transform: `translateY(${(1 - t) * -300}px)`, opacity: t }}>
        <div style={{ fontSize: 60, fontWeight: 800, color: C.soft }}>¿Cuánto cuesta?</div>
        <div style={{ fontSize: 120, fontWeight: 900, color: C.ink, letterSpacing: -4, lineHeight: 1.02 }}>Dos planes,<br /><span style={{ color: C.coral }}>a tu medida</span></div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 70, marginTop: 90 }}>
        <Tarjeta d={30} nombre="Básica" precio={99} texto="Una sección con lo esencial: tus fotos, precios, horario, mapa y botón de WhatsApp." />
        <Tarjeta d={90} nombre="Completa" precio={199} oscura texto="Varias secciones: catálogo o menú, formas de pago, reservas, galería y tu dominio propio." nota="El dominio se paga aparte." />
      </div>
    </AbsoluteFill>
  );
};

// ===== 4) Ejemplo gratis =====
const Confeti: React.FC<{ d: number }> = ({ d }) => {
  const f = useCurrentFrame();
  if (f < d) return null;
  const t = (f - d) / 30;
  const cols = [C.coral, C.mint, C.sun, C.ink];
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {Array.from({ length: 46 }).map((_, i) => {
        const ang = random(`a${i}`) * Math.PI * 2, vel = 700 + random(`v${i}`) * 900;
        const x = 540 + Math.cos(ang) * vel * t, y = 1120 + Math.sin(ang) * vel * t + 900 * t * t;
        return <div key={i} style={{ position: "absolute", left: x, top: y, width: 22, height: 34, background: cols[i % 4], borderRadius: 6, transform: `rotate(${(random(`r${i}`) * 720) * t}deg)`, opacity: interpolate(t, [0, 1.6, 2.2], [1, 1, 0], clamp) }} />;
      })}
    </AbsoluteFill>
  );
};

const Gratis: React.FC = () => {
  const f = useCurrentFrame();
  const a = useSpring(15), b = useSpring(30);
  const sello = useSpring(66, { damping: 7, stiffness: 300, mass: 0.8 });
  const sub = useSpring(80);
  const zoom = interpolate(f, [45, 66], [1, 1.05], clamp);
  return (
    <AbsoluteFill style={{ padding: "330px 80px 0", transform: `scale(${zoom})` }}>
      <div style={{ fontSize: 100, fontWeight: 900, color: C.ink, letterSpacing: -3, opacity: a, transform: `translateY(${(1 - a) * 80}px)` }}>Antes de decidir,</div>
      <div style={{ fontSize: 100, fontWeight: 900, color: C.ink, letterSpacing: -3, lineHeight: 1.05, opacity: b, transform: `translateY(${(1 - b) * 80}px)` }}>te armamos un ejemplo de tu página</div>
      <div style={{ marginTop: 90, display: "flex", justifyContent: "center" }}>
        <div style={{ transform: `scale(${f < 66 ? 0 : 3 - sello * 2}) rotate(-8deg)`, opacity: f < 66 ? 0 : 1, border: `14px solid ${C.coral}`, borderRadius: 40, padding: "20px 70px", fontSize: 210, fontWeight: 900, color: C.coral, letterSpacing: 6, background: "rgba(255,255,255,.7)" }}>
          GRATIS
        </div>
      </div>
      <div style={{ marginTop: 90, textAlign: "center", fontSize: 50, fontWeight: 700, color: C.soft, opacity: sub, transform: `translateY(${(1 - sub) * 40}px)` }}>
        Así ves cómo quedaría tu negocio
      </div>
      <Confeti d={68} />
    </AbsoluteFill>
  );
};

// ===== 5) Cierre: WhatsApp + Síguenos =====
const Cierre: React.FC = () => {
  const f = useCurrentFrame();
  const logo = useSpring(8, { damping: 9 });
  const tel = useSpring(22);
  const escribe = Math.max(0, Math.min(9, Math.floor((f - 26) / 4.5) + 1));
  const numero = "6919-7559".slice(0, escribe);
  const perfil = useSpring(62, { damping: 12 });
  const toque = 87; // el dedo toca "Seguir"
  const apretado = f >= toque && f < toque + 5 ? 0.9 : 1;
  const siguiendo = f >= toque + 3;
  const dedo = interpolate(f, [70, toque, toque + 18], [500, 0, 420], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const ok = useSpring(toque + 3, { damping: 8, stiffness: 240 });
  return (
    <AbsoluteFill style={{ alignItems: "center", padding: "200px 70px 0" }}>
      <div style={{ transform: `scale(${logo})` }}><Logo size={120} /></div>
      <div style={{ marginTop: 90, textAlign: "center", opacity: tel, transform: `translateY(${(1 - tel) * 60}px)` }}>
        <div style={{ fontSize: 64, fontWeight: 800, color: C.ink }}>Escríbenos al WhatsApp</div>
        <div style={{ fontSize: 170, fontWeight: 900, color: C.coral, letterSpacing: -3, minHeight: 200 }}>{numero}<span style={{ opacity: f % 16 < 8 && escribe < 9 ? 1 : 0, color: C.ink }}>|</span></div>
      </div>
      {/* tarjeta de perfil genérica (sin logos de ninguna red) */}
      <div style={{ marginTop: 70, width: 900, background: C.white, borderRadius: 50, padding: "44px 50px", boxShadow: "0 16px 0 rgba(27,42,74,.12)", transform: `translateY(${(1 - perfil) * 900}px)`, display: "flex", alignItems: "center", gap: 34 }}>
        <Img src={staticFile("favicon.svg")} style={{ width: 150, height: 150 }} />
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 54, fontWeight: 900, color: C.ink }}>@sitioya.pty</div>
          <div style={{ fontSize: 34, fontWeight: 600, color: C.soft, marginTop: 6 }}>Páginas web para negocios en Panamá</div>
          <div style={{ marginTop: 24, transform: `scale(${apretado})`, transformOrigin: "left center", display: "inline-block" }}>
            <div style={{ background: siguiendo ? C.mint : C.coral, borderRadius: 999, padding: "16px 54px", fontSize: 40, fontWeight: 900, color: C.ink }}>
              {siguiendo ? <span style={{ display: "inline-block", transform: `scale(${0.7 + ok * 0.3})` }}>Siguiendo ✓</span> : "Seguir"}
            </div>
          </div>
        </div>
      </div>
      <div style={{ marginTop: 80, textAlign: "center", fontSize: 92, fontWeight: 900, color: C.ink, letterSpacing: -2, lineHeight: 1.1, opacity: ok, transform: `scale(${0.6 + ok * 0.4})` }}>
        ¡<span style={{ color: C.coral }}>Síguenos</span> para<br />más ejemplos!
      </div>
      <div style={{ marginTop: 60, opacity: ok }}>
        <Pill bg={C.ink} color={C.white} size={40}>Ejemplo gratis antes de decidir</Pill>
      </div>
      {/* dedo */}
      <div style={{ position: "absolute", left: 470, top: 1290 + dedo, width: 120, height: 120, borderRadius: "50%", background: "rgba(27,42,74,.25)", border: `8px solid ${C.ink}`, opacity: f > 70 && f < toque + 18 ? 1 : 0, transform: `scale(${f >= toque && f < toque + 6 ? 0.8 : 1})` }} />
    </AbsoluteFill>
  );
};

const Escena: React.FC<{ r: number[]; children: React.ReactNode }> = ({ r, children }) => (
  <Sequence from={r[0]} durationInFrames={r[1] - r[0]}>{children}</Sequence>
);

export const Reel: React.FC = () => (
  <AbsoluteFill style={{ fontFamily: FONT, color: C.ink }}>
    <Fondo />
    <Escena r={E.gancho}><Gancho /></Escena>
    <Escena r={E.medida}><Medida /></Escena>
    <Escena r={E.planes}><Planes /></Escena>
    <Escena r={E.gratis}><Gratis /></Escena>
    <Escena r={E.cierre}><Cierre /></Escena>
    {[E.medida[0], E.planes[0], E.gratis[0], E.cierre[0]].map((at) => <Barrido key={at} at={at} />)}
    <Audio src={staticFile("audio.wav")} />
  </AbsoluteFill>
);
