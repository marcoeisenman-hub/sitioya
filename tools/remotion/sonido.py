"""Música y efectos del reel "A la medida", todo sintetizado aquí (sin archivos de afuera ni música con derechos).

Uso: python3 sonido.py   -> escribe public/audio.wav (48 kHz, estéreo)
Lee los tiempos de src/linea.json (los mismos que usa el video) y reutiliza
los efectos de tools/reels/audio.py (whoosh, pop, tap, key, notif, ding, sparkle, thud).
"""
import json, sys, wave
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "reels"))
from audio import SR, env, nota, efecto as efecto_base  # noqa: E402

rng = np.random.default_rng(11)  # fijo: el mismo audio cada vez


def efecto(nombre):
    if nombre == "tape":  # cinta métrica que se estira: clics cada vez más rápidos
        n = int(.6 * SR); y = np.zeros(n); t = 0.0; paso = .045
        while t < .55:
            a = int(t * SR); k = int(.012 * SR)
            y[a:a + k] += rng.standard_normal(k)[: n - a] * env(k, .0003, .003)[: n - a] * .5
            t += paso; paso = max(.012, paso * .86)
        return y
    if nombre == "ticks":  # el precio que sube contando
        n = int(.55 * SR); y = np.zeros(n)
        for j in range(12):
            a = int(j * .045 * SR); k = int(.02 * SR); tt = np.arange(k) / SR
            y[a:a + k] += np.sin(2 * np.pi * (1400 + j * 60) * tt) * env(k, .0005, .006) * .35
        return y
    if nombre == "riser":  # sube antes del sello GRATIS
        n = int(.7 * SR); t = np.arange(n) / SR
        tono = np.sin(2 * np.pi * np.cumsum(220 + 900 * (t / t[-1]) ** 2) / SR)
        ruido = rng.standard_normal(n) * .25
        return (tono * .25 + ruido * (t / t[-1])) * (t / t[-1]) ** 1.5 * .6
    return efecto_base(nombre)


def musica(total, silencio):
    bpm = 120; beat = 60 / bpm; bar = beat * 4
    n = int((total + 1) * SR); m = np.zeros(n); bat = np.zeros(n)
    hz = lambda midi: 440 * 2 ** ((midi - 69) / 12)
    acordes = [[60, 64, 67, 71], [55, 59, 62, 67], [57, 60, 64, 67], [53, 57, 60, 64]]  # Cmaj7 G Am7 Fmaj7
    bajos = [36, 43, 45, 41]
    arpe = [0, 2, 1, 3, 2, 1, 3, 2]

    def suma(buf, x, at):
        a = int(at * SR); b = min(n, a + len(x))
        if 0 <= a < n: buf[a:b] += x[: b - a]

    t, i = 0.0, 0
    while t < total + 1:
        ac = acordes[i % 4]
        for nn in ac: suma(m, nota(hz(nn), bar + .3, .045, "pad"), t)
        for k in (0, 1.5, 2, 3.5):
            suma(m, nota(hz(bajos[i % 4]), beat * .9, .15, "bajo"), t + k * beat)
        for k in range(8):
            suma(m, nota(hz(ac[arpe[k]] + 12), .35, .05, "pluck"), t + k * beat / 2)
        for k in range(4):
            kk = int(.2 * SR); tt = np.arange(kk) / SR  # bombo
            suma(bat, np.sin(2 * np.pi * (50 + 110 * np.exp(-tt * 35)) * tt) * np.exp(-tt * 16) * .3, t + k * beat)
            for h in (0, .5):  # hi-hat
                hh = rng.standard_normal(int(.04 * SR)); hh = np.diff(hh, prepend=0) * env(len(hh), .0005, .01) * .04
                suma(bat, hh, t + k * beat + h * beat)
            if k in (1, 3):  # palmada
                cl = rng.standard_normal(int(.12 * SR)) * env(int(.12 * SR), .001, .03) * .12
                suma(bat, cl, t + k * beat)
        t += bar; i += 1
    m, bat = m[: int(total * SR)], bat[: int(total * SR)]
    s = np.arange(len(m)) / SR
    a, b = silencio  # la batería se calla justo antes del sello y vuelve con el golpe
    bat[(s >= a) & (s < b)] = 0
    fade = np.minimum(1, s / .4) * np.minimum(1, (total - s) / 1.2)
    return (m + bat) * fade


def main():
    linea = json.loads((AQUI / "src" / "linea.json").read_text())
    fps = linea["fps"]; total = linea["total"] / fps; n = int(total * SR)
    fx = np.zeros(n); cache = {}
    for e in linea["sonidos"]:
        x = cache.setdefault(e["s"], efecto(e["s"]))
        a = int(e["f"] / fps * SR); b = min(n, a + len(x))
        if 0 <= a < n: fx[a:b] += x[: b - a] * e["v"]
    mus = musica(total, (495 / fps, 516 / fps))
    mezcla = mus * .55 + fx * .6
    L = mezcla + np.roll(fx, 200) * .06; R = mezcla + np.roll(mus, 300) * .06
    st = np.stack([L, R], 1)
    pk = np.max(np.abs(st)); st = st / pk * .9 if pk > .9 else st
    salida = AQUI / "public" / "audio.wav"; salida.parent.mkdir(exist_ok=True)
    with wave.open(str(salida), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())
    print("audio listo", salida, f"{total:.1f} s")


if __name__ == "__main__":
    main()
