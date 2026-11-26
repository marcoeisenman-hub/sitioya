"""Arma el audio de un reel: música suave + efectos, todo sintetizado aquí (sin archivos de afuera), y la voz.

Uso: python3 audio.py <carpeta-trabajo>/<video>
Lee tiempos.json y sonidos.json, escribe audio.wav (48 kHz, estéreo).
"""
import json, subprocess, sys, wave
from pathlib import Path

import numpy as np

SR = 48000
rng = np.random.default_rng(7)  # fijo: el mismo audio cada vez


def env(n, a=0.005, r=0.1):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)


def lp(x, k):  # pasa bajos simple de un polo
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += k * (v - acc); y[i] = acc
    return y


def nota(f, dur, vol=1.0, tipo="pad"):
    n = int(dur * SR); t = np.arange(n) / SR
    if tipo == "pad":
        s = sum(np.sin(2 * np.pi * f * m * t + d) / m ** 1.6 for m, d in [(1, 0), (2, 1), (3, 2), (1.003, .5), (0.997, 1.5)])
        a = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)
    elif tipo == "pluck":
        s = np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) + .12 * np.sin(6 * np.pi * f * t)
        a = env(n, .003, .22)
    else:  # bajo
        s = np.sin(2 * np.pi * f * t) + .2 * np.sin(4 * np.pi * f * t)
        a = np.minimum(1, t / .01) * np.exp(-t / .5)
    return s * a * vol


def musica(total):
    bpm = 104; beat = 60 / bpm; bar = beat * 4
    n = int((total + 1) * SR); m = np.zeros(n)
    hz = lambda midi: 440 * 2 ** ((midi - 69) / 12)
    acordes = [[65, 69, 72, 76], [57, 60, 64, 67], [62, 65, 69, 72], [58, 62, 65, 69]]  # Fmaj7 Am7 Dm7 Bbmaj7
    bajos = [41, 45, 38, 46]
    arpe = [0, 2, 1, 3, 2, 1, 3, 2]
    t, i = 0.0, 0
    while t < total + 1:
        ac = acordes[i % 4]
        def suma(x, at):
            a = int(at * SR); b = min(n, a + len(x))
            if a < n: m[a:b] += x[: b - a]
        for nn in ac: suma(nota(hz(nn), bar + .3, .05, "pad"), t)
        suma(nota(hz(bajos[i % 4]), beat * 1.8, .16, "bajo"), t); suma(nota(hz(bajos[i % 4]), beat * 1.8, .12, "bajo"), t + beat * 2)
        for k in range(8):
            suma(nota(hz(ac[arpe[k]] + 12), .5, .055, "pluck"), t + k * beat / 2)
        for k in range(4):  # golpe suave y shaker
            kk = int(.18 * SR); tt = np.arange(kk) / SR
            suma(np.sin(2 * np.pi * (55 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 18) * .2, t + k * beat)
            h = rng.standard_normal(int(.05 * SR)); h = np.diff(h, prepend=0) * env(len(h), .001, .015) * .035
            suma(h, t + k * beat + beat / 2)
        t += bar; i += 1
    m = m[: int(total * SR)]
    f = np.minimum(1, np.arange(len(m)) / SR / 1.0) * np.minimum(1, (total - np.arange(len(m)) / SR) / 1.5)
    return m * f


def efecto(nombre):
    if nombre == "whoosh":
        n = int(.45 * SR); t = np.arange(n) / SR; x = rng.standard_normal(n)
        k = 0.02 + 0.25 * np.sin(np.pi * t / t[-1]) ** 2
        y = np.empty(n); acc = 0.0
        for i in range(n): acc += k[i] * (x[i] - acc); y[i] = acc
        return y * np.sin(np.pi * t / t[-1]) ** 1.5 * 1.1
    if nombre == "pop":
        n = int(.12 * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(900 * np.exp(-t * 28) + 380) / SR) * env(n, .001, .035) * .55
    if nombre == "tap":
        n = int(.06 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1800 * t) * .4 + rng.standard_normal(n) * .3) * env(n, .0005, .008)
    if nombre == "key":
        n = int(.04 * SR)
        return lp(rng.standard_normal(n), .5) * env(n, .0003, .006) * .7
    if nombre in ("notif", "ding"):
        tonos = [(1318.5, 0), (1760, .09)] if nombre == "notif" else [(1046.5, 0), (1568, .11), (2093, .22)]
        n = int(.9 * SR); y = np.zeros(n)
        for f, d in tonos:
            a = int(d * SR); t = np.arange(n - a) / SR
            y[a:] += (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 2.01 * t)) * env(n - a, .002, .22 if nombre == "ding" else .12)
        return y * .3
    if nombre == "send":
        n = int(.22 * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * np.cumsum(500 + 1400 * t / t[-1]) / SR) * np.sin(np.pi * t / t[-1]) * .3
    if nombre == "sparkle":
        n = int(.8 * SR); y = np.zeros(n)
        for j, f in enumerate([2093, 2637, 3136, 3951, 4186]):
            a = int(j * .07 * SR); t = np.arange(n - a) / SR
            y[a:] += np.sin(2 * np.pi * f * t) * env(n - a, .001, .15) * .12
        return y
    if nombre == "thud":
        n = int(.35 * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * (48 + 110 * np.exp(-t * 25)) * t) * env(n, .001, .12) * .9
    raise ValueError("efecto desconocido: " + nombre)


def leer_mp3(mp3):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp3), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def main(d: Path):
    tl = json.loads((d / "tiempos.json").read_text())
    ev = json.loads((d / "sonidos.json").read_text())
    total = tl["total"]; n = int(total * SR)
    voz = np.zeros(n); fx = np.zeros(n)
    def poner(buf, x, t, v=1.0):
        a = int(t * SR); b = min(n, a + len(x))
        if 0 <= a < n: buf[a:b] += x[: b - a] * v
    for e in tl["escenas"]:
        for l in e["lineas"]:
            poner(voz, leer_mp3(d / l["mp3"]), l["t"])
    cache = {}
    for e in ev:
        cache.setdefault(e["s"], efecto(e["s"]))
        poner(fx, cache[e["s"]], e["t"], e["v"])
    mus = musica(total)
    # la música baja cuando hay voz (suave, con 0.25 s de ataque y 0.5 s de salida)
    hay = np.abs(voz) > 0.02
    k = int(.05 * SR); w = np.convolve(hay.astype(float), np.ones(k) / k, "same") > 0
    g = np.where(w, .45, 1.0); sm = np.empty_like(g); acc = 1.0
    for i in range(0, n, 240):
        acc += (g[i] - acc) * (.25 if g[i] < acc else .1); sm[i:i + 240] = acc
    voz = voz / (np.max(np.abs(voz)) + 1e-9) * .9
    mezcla = voz + mus * sm * .36 + fx * .5
    L = mezcla + np.roll(fx, 240) * .05; R = mezcla + np.roll(mus * sm, 360) * .05
    st = np.stack([L, R], 1)
    pk = np.max(np.abs(st)); st = st / max(pk, 1.0) * .95 if pk > .95 else st
    with wave.open(str(d / "audio.wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())
    print("audio listo", d / "audio.wav")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: audio.py <carpeta-trabajo>/<video>")
    main(Path(sys.argv[1]).resolve())
