#!/bin/bash
# Reel "A la medida" (Síguenos) de @sitioya.pty hecho con Remotion.
# Uso: tools/remotion/hacer.sh            -> redes/videos/a-la-medida.mp4 + a-la-medida.jpg
#      tools/remotion/hacer.sh --cuadros 45 230 ...  -> solo PNG de esos cuadros en /tmp/sy-stills (para revisar)
# Una sola vez: cd tools/remotion && npm i   (Remotion baja su Chrome solo la primera vez)
# Necesita python3 con numpy (para la música y los efectos, que se sintetizan en sonido.py).
set -euo pipefail
cd "$(dirname "$0")"
REMOTION=node_modules/.bin/remotion
if [ "${1:-}" = "--cuadros" ]; then
  shift; mkdir -p /tmp/sy-stills
  for fr in "$@"; do "$REMOTION" still src/index.ts a-la-medida "/tmp/sy-stills/f$fr.png" --frame="$fr" --log=error; done
  exit 0
fi
python3 sonido.py
SALIDA="../../redes/videos"
mkdir -p "$SALIDA"
tmpd=$(mktemp -d -t a-la-medida); trap 'rm -rf "$tmpd"' EXIT
"$REMOTION" render src/index.ts a-la-medida "$tmpd/crudo.mp4" --codec=h264 --crf=20 --audio-codec=aac --audio-bitrate=192k --log=error
ffmpeg -nostdin -y -hide_banner -loglevel error -i "$tmpd/crudo.mp4" -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000" -c:a aac -b:a 160k -movflags +faststart "$tmpd/final.mp4"
# portada: el gancho ya armado
"$REMOTION" still src/index.ts a-la-medida "$tmpd/portada.png" --frame=60 --log=error
ffmpeg -nostdin -y -hide_banner -loglevel error -i "$tmpd/portada.png" -q:v 3 "$tmpd/portada.jpg"
mv -f "$tmpd/portada.jpg" "$SALIDA/a-la-medida.jpg"; mv -f "$tmpd/final.mp4" "$SALIDA/a-la-medida.mp4"
chmod 644 "$SALIDA/a-la-medida.mp4" "$SALIDA/a-la-medida.jpg"
echo "a-la-medida: $(ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$SALIDA/a-la-medida.mp4")"
