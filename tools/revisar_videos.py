#!/usr/bin/env python3
"""Revisa que los videos/reels de SitioYa duren 15-30 segundos.

Uso:
    python3 tools/revisar_videos.py video1.mp4 video2.mov ...
    python3 tools/revisar_videos.py carpeta/          (revisa todos los videos de la carpeta)
    python3 tools/revisar_videos.py --recortar video.mp4
    python3 tools/revisar_videos.py --recortar --hasta 25 video.mp4

Sin --recortar solo dice cuánto dura cada video y si está bien.
Con --recortar, a los que pasan de 30 s les hace una copia corta
(<nombre>-corto.mp4, al lado del original) con los primeros segundos y un
fundido de 0.5 s al final (imagen y sonido). El original no se toca.

Necesita ffmpeg (en el PATH o el de `pip install imageio-ffmpeg`).
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

MINIMO = 15.0
MAXIMO = 30.0
FUNDIDO = 0.5
EXTENSIONES = {".mp4", ".mov", ".m4v", ".webm"}


def buscar_ffmpeg():
    ruta = shutil.which("ffmpeg")
    if ruta:
        return ruta
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit("No encontré ffmpeg. Instala con: pip install imageio-ffmpeg")


def duracion(ffmpeg, video):
    salida = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(video)],
        capture_output=True,
        text=True,
    ).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", salida)
    if not m:
        return None
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)


def tiene_audio(ffmpeg, video):
    salida = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(video)],
        capture_output=True,
        text=True,
    ).stderr
    return "Audio:" in salida


def recortar(ffmpeg, video, hasta):
    destino = video.with_name(f"{video.stem}-corto.mp4")
    inicio_fundido = max(hasta - FUNDIDO, 0)
    cmd = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(video), "-t", f"{hasta}",
        "-vf", f"fade=t=out:st={inicio_fundido}:d={FUNDIDO}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
    ]
    if tiene_audio(ffmpeg, video):
        cmd += ["-af", f"afade=t=out:st={inicio_fundido}:d={FUNDIDO}", "-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-an"]
    cmd.append(str(destino))
    subprocess.run(cmd, check=True)
    return destino


def juntar_videos(rutas):
    videos = []
    for r in rutas:
        p = Path(r)
        if p.is_dir():
            videos += sorted(
                x for x in p.iterdir()
                if x.suffix.lower() in EXTENSIONES and not x.stem.endswith("-corto")
            )
        elif p.is_file():
            videos.append(p)
        else:
            print(f"No existe: {r}")
    return videos


def main():
    ap = argparse.ArgumentParser(description="Revisa que los reels duren 15-30 s.")
    ap.add_argument("videos", nargs="+", help="videos o carpetas")
    ap.add_argument("--recortar", action="store_true", help="hace copia corta de los que pasan de 30 s")
    ap.add_argument("--hasta", type=float, default=MAXIMO, help="segundos de la copia corta (15-30, por defecto 30)")
    args = ap.parse_args()

    if not MINIMO <= args.hasta <= MAXIMO:
        sys.exit(f"--hasta tiene que estar entre {MINIMO:g} y {MAXIMO:g} segundos")

    ffmpeg = buscar_ffmpeg()
    videos = juntar_videos(args.videos)
    if not videos:
        sys.exit("No encontré videos para revisar.")

    largos = 0
    for v in videos:
        d = duracion(ffmpeg, v)
        if d is None:
            print(f"?  {v.name}: no pude leer la duración")
            continue
        if d > MAXIMO:
            largos += 1
            print(f"LARGO  {v.name}: {d:.1f} s (máximo {MAXIMO:g} s)")
            if args.recortar:
                destino = recortar(ffmpeg, v, args.hasta)
                print(f"       copia corta: {destino.name} ({duracion(ffmpeg, destino):.1f} s)")
        elif d < MINIMO:
            print(f"CORTO  {v.name}: {d:.1f} s (mínimo {MINIMO:g} s, se puede dejar si se entiende)")
        else:
            print(f"OK     {v.name}: {d:.1f} s")

    if largos and not args.recortar:
        print(f"\n{largos} video(s) pasan de 30 s. Para la copia corta: agrega --recortar (y --hasta 25 si quieres).")


if __name__ == "__main__":
    main()
