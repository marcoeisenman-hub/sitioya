#!/bin/bash
# Hace los 3 reels de @sitioya.pty: voz -> cuadros -> audio -> mp4 + portada en redes/videos/
# Uso: tools/reels/hacer_reels.sh [video ...]   (sin nombres hace los 3)
# Necesita: node + npm i (aquí), python3 con numpy, ffmpeg y ffprobe, uv (para edge-tts).
set -euo pipefail
cd "$(dirname "$0")"
TRABAJO="${TRABAJO:-$(mktemp -d -t reels-sitioya)}"
SALIDA="../../redes/videos"
mkdir -p "$SALIDA"
VIDEOS=("$@"); [ ${#VIDEOS[@]} -eq 0 ] && VIDEOS=(antes-despues como-funciona tu-negocio-en-internet)
for v in "${VIDEOS[@]}"; do
  case "$v" in antes-despues|como-funciona|tu-negocio-en-internet) ;; *) echo "Video desconocido: $v" >&2; exit 1;; esac
done
uv run --quiet --with edge-tts python3 voz.py "$TRABAJO"
for v in "${VIDEOS[@]}"; do
  node render.mjs "$v" "$TRABAJO"
  python3 audio.py "$TRABAJO/$v"
  tmp="$SALIDA/.$v.tmp.mp4"
  ffmpeg -nostdin -y -hide_banner -loglevel error -i "$TRABAJO/$v/video-mudo.mp4" -i "$TRABAJO/$v/audio.wav" \
    -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo" -c:a aac -b:a 160k -ar 48000 \
    -movflags +faststart -shortest "$tmp"
  mv -f "$tmp" "$SALIDA/$v.mp4"
  # portada: el cuadro del gancho ya armado
  node render.mjs "$v" "$TRABAJO" --cuadros 2.4
  ffmpeg -nostdin -y -hide_banner -loglevel error -i "$TRABAJO/$v/cuadro-2.40.png" -q:v 3 "$SALIDA/$v.jpg"
  echo "$v: $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$SALIDA/$v.mp4")"
done
echo "Trabajo en $TRABAJO"
