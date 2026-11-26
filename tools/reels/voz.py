"""Genera la voz de cada línea (edge-tts, voz panameña) y arma la línea de tiempo.

Uso: uv run --with edge-tts python3 voz.py <carpeta-trabajo>
Escribe <trabajo>/<video>/linea-N.mp3 y <trabajo>/<video>/tiempos.json
"""
import asyncio, difflib, hashlib, json, re, subprocess, sys
from pathlib import Path

import edge_tts

AQUI = Path(__file__).resolve().parent
COLA = 0.4  # segundos de aire después de cada línea antes de cambiar de escena


def dur(mp3: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


async def tts(texto, voz, vel, mp3: Path, js: Path):
    if mp3.exists() and js.exists():
        return json.loads(js.read_text())
    com = edge_tts.Communicate(texto, voz, rate=vel, boundary="WordBoundary")
    palabras, audio = [], bytearray()
    async for c in com.stream():
        if c["type"] == "audio":
            audio += c["data"]
        elif c["type"] == "WordBoundary":
            palabras.append({"w": c["text"], "t": c["offset"] / 1e7, "d": c["duration"] / 1e7})
    if not audio:
        raise RuntimeError("edge-tts no devolvió audio para: " + texto)
    tmp = mp3.with_suffix(".tmp")
    tmp.write_bytes(audio)
    tmp.replace(mp3)
    js.write_text(json.dumps(palabras, ensure_ascii=False))
    return palabras


NUM = {"1": "uno", "2": "dos", "3": "tres", "dm": "di"}


def _norm(s: str) -> str:
    s = re.sub(r"[^\wáéíóúñü]", "", s.lower())
    return NUM.get(s, s)


def subtitulos(sub: str, palabras, inicio: float, largo: float):
    """Pone a cada palabra del subtítulo el tiempo en que la voz la dice.

    Alinea por texto (difflib); las palabras que no se dicen igual ($99, DM, @sitioya.pty)
    toman el tiempo interpolado entre sus vecinas.
    """
    ws = sub.split()
    if not palabras:
        return [{"w": w, "t": round(inicio + largo * i / len(ws), 3)} for i, w in enumerate(ws)]
    sm = difflib.SequenceMatcher(None, [_norm(w) for w in ws], [_norm(p["w"]) for p in palabras], autojunk=False)
    t = [None] * len(ws)
    for i, j, n in sm.get_matching_blocks():
        for k in range(n):
            t[i + k] = palabras[j + k]["t"]
    if t[0] is None:
        t[0] = palabras[0]["t"]
    if t[-1] is None:
        t[-1] = max(t[0], min(largo - 0.3, palabras[-1]["t"] + palabras[-1]["d"]))
    for i in range(len(ws)):
        if t[i] is None:
            j = next(k for k in range(i + 1, len(ws)) if t[k] is not None)
            a, b = t[i - 1], t[j]
            t[i] = a + (b - a) * 1 / (j - i + 1)
    return [{"w": w, "t": round(inicio + x, 3)} for w, x in zip(ws, t)]


async def main(trabajo: Path):
    g = json.loads((AQUI / "guiones.json").read_text())
    for nombre, escenas in g["videos"].items():
        d = trabajo / nombre
        d.mkdir(parents=True, exist_ok=True)
        t, n, salida = 0.0, 0, []
        for e in escenas:
            fin_voz = 0.0
            lineas = []
            for l in e["lineas"]:
                h = hashlib.sha1(f'{g["voz"]}|{g["velocidad"]}|{l["say"]}'.encode()).hexdigest()[:10]
                mp3, js = d / f"voz-{h}.mp3", d / f"voz-{h}.json"
                pal = await tts(l["say"], g["voz"], g["velocidad"], mp3, js)
                ld = dur(mp3)
                ini = t + l["at"]
                lineas.append({"mp3": mp3.name, "t": round(ini, 3), "d": round(ld, 3),
                               "subs": subtitulos(l["sub"], pal, ini, ld)})
                fin_voz = max(fin_voz, l["at"] + ld)
                n += 1
            largo = round(max(e["min"], fin_voz + COLA), 3)
            esc = {k: v for k, v in e.items() if k != "lineas"}
            esc.update({"t": round(t, 3), "d": largo, "lineas": lineas})
            salida.append(esc)
            t += largo
        (d / "tiempos.json").write_text(json.dumps({"total": round(t, 3), "escenas": salida}, ensure_ascii=False, indent=1))
        print(f"{nombre}: {t:.2f} s")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: voz.py <carpeta-trabajo>")
    asyncio.run(main(Path(sys.argv[1]).resolve()))
