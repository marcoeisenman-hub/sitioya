#!/bin/bash
# Hace los reels de @sitioya.pty: voz -> cuadros -> audio -> mp4 + portada en redes/videos/
# Uso: tools/reels/hacer_reels.sh [video ...]   (sin nombres los hace todos)
# Una sola vez: cd tools/reels && npm i && npx playwright install chromium-headless-shell
# Necesita también: python3 con numpy, ffmpeg y ffprobe en el PATH, y uv (para la voz con edge-tts).
set -euo pipefail
cd "$(dirname "$0")"
PROPIO=""; CANDADO=""; tmpv=""; tmpj=""
# al salir: borra temporales, suelta el candado (solo si es nuestro) y la carpeta de trabajo si la creó este script
limpiar() {
  rm -f "$tmpv" "$tmpj"
  if [ -n "$CANDADO" ]; then rmdir "$CANDADO" 2>/dev/null || true; fi
  if [ -n "$PROPIO" ]; then rm -rf "$PROPIO"; fi
}
trap limpiar EXIT
SALIDA="../../redes/videos"
mkdir -p "$SALIDA"
# una sola corrida a la vez (dos a la vez mezclarían videos y portadas)
mkdir "$SALIDA/.hacer_reels.lock" 2>/dev/null || { echo "Ya hay otra corrida (si no, borra $SALIDA/.hacer_reels.lock)" >&2; exit 1; }
CANDADO="$SALIDA/.hacer_reels.lock"
if [ -z "${TRABAJO:-}" ]; then PROPIO=$(mktemp -d -t reels-sitioya); TRABAJO="$PROPIO"; fi
VIDEOS=("$@"); [ ${#VIDEOS[@]} -eq 0 ] && VIDEOS=(antes-despues como-funciona tu-negocio-en-internet planes)
for v in "${VIDEOS[@]}"; do
  case "$v" in antes-despues|como-funciona|tu-negocio-en-internet|planes) ;; *) echo "Video desconocido: $v" >&2; exit 1;; esac
done
uv run --quiet --with edge-tts python3 voz.py "$TRABAJO" "${VIDEOS[@]}"
for v in "${VIDEOS[@]}"; do
  node render.mjs "$v" "$TRABAJO"
  python3 audio.py "$TRABAJO/$v"
  node render.mjs "$v" "$TRABAJO" --cuadros 2.4   # portada: el gancho ya armado
  tmpv=$(mktemp "$SALIDA/.$v.XXXXXX")
  tmpj=$(mktemp "$SALIDA/.$v.XXXXXX")
  ffmpeg -nostdin -y -hide_banner -loglevel error -i "$TRABAJO/$v/video-mudo.mp4" -i "$TRABAJO/$v/audio.wav" \
    -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo" \
    -c:a aac -b:a 160k -ar 48000 -movflags +faststart -shortest -f mp4 "$tmpv"
  ffmpeg -nostdin -y -hide_banner -loglevel error -i "$TRABAJO/$v/cuadro-2.40.png" -q:v 3 -f image2 -c:v mjpeg "$tmpj"
  chmod 644 "$tmpv" "$tmpj"
  # primero la portada y luego el video: si algo falla en medio, el video viejo sigue con su portada casi igual
  mv -f "$tmpj" "$SALIDA/$v.jpg"; mv -f "$tmpv" "$SALIDA/$v.mp4"; tmpv=""; tmpj=""
  echo "$v: $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$SALIDA/$v.mp4")"
done
[ -z "$PROPIO" ] && echo "Trabajo en $TRABAJO"
true
