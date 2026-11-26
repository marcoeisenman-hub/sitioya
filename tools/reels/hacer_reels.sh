#!/bin/bash
# Hace los 3 reels de @sitioya.pty: voz -> cuadros -> audio -> mp4 + portada en redes/videos/
# Uso: tools/reels/hacer_reels.sh [video ...]   (sin nombres hace los 3)
# Una sola vez: cd tools/reels && npm i && npx playwright install chromium-headless-shell
# Necesita también: python3 con numpy, ffmpeg y ffprobe en el PATH, y uv (para la voz con edge-tts).
set -euo pipefail
cd "$(dirname "$0")"
TRABAJO="${TRABAJO:-$(mktemp -d -t reels-sitioya)}"
SALIDA="../../redes/videos"
mkdir -p "$SALIDA"
VIDEOS=("$@"); [ ${#VIDEOS[@]} -eq 0 ] && VIDEOS=(antes-despues como-funciona tu-negocio-en-internet)
for v in "${VIDEOS[@]}"; do
  case "$v" in antes-despues|como-funciona|tu-negocio-en-internet) ;; *) echo "Video desconocido: $v" >&2; exit 1;; esac
done
uv run --quiet --with edge-tts python3 voz.py "$TRABAJO" "${VIDEOS[@]}"
for v in "${VIDEOS[@]}"; do
  node render.mjs "$v" "$TRABAJO"
  python3 audio.py "$TRABAJO/$v"
  node render.mjs "$v" "$TRABAJO" --cuadros 2.4   # portada: el gancho ya armado
  tmpv=$(mktemp "$SALIDA/.$v.XXXXXX"); tmpj=$(mktemp "$SALIDA/.$v.XXXXXX")
  trap 'rm -f "$tmpv" "$tmpj"' EXIT
  ffmpeg -nostdin -y -hide_banner -loglevel error -i "$TRABAJO/$v/video-mudo.mp4" -i "$TRABAJO/$v/audio.wav" \
    -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo" \
    -c:a aac -b:a 160k -ar 48000 -movflags +faststart -shortest -f mp4 "$tmpv"
  ffmpeg -nostdin -y -hide_banner -loglevel error -i "$TRABAJO/$v/cuadro-2.40.png" -q:v 3 -f image2 -c:v mjpeg "$tmpj"
  chmod 644 "$tmpv" "$tmpj"
  mv -f "$tmpv" "$SALIDA/$v.mp4"; mv -f "$tmpj" "$SALIDA/$v.jpg"
  trap - EXIT
  echo "$v: $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$SALIDA/$v.mp4")"
done
echo "Trabajo en $TRABAJO"
