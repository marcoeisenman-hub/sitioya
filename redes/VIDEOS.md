# Videos y reels de @sitioya.pty

## Regla: cortos, de 15 a 30 segundos (nunca más de 30)
- Lo ideal: 20-25 s. Si se pasa de 30 s, se recorta.
- Gancho en los primeros 2 segundos, una sola idea por video y cierre con: **Escríbenos por DM @sitioya.pty**.
- Vertical 1080x1920, subtítulos grandes (mucha gente lo ve sin sonido).

## Cómo revisar y recortar
```
python3 tools/revisar_videos.py carpeta-con-los-videos/
python3 tools/revisar_videos.py --recortar --hasta 25 video-largo.mp4
```
- Sin `--recortar` solo dice cuánto dura cada uno (OK, LARGO o CORTO).
- Con `--recortar` hace `<nombre>-corto.mp4` al lado del original, con los primeros segundos y un fundido de 0.5 s al final. El original no se toca y nunca pisa un archivo que ya exista (si ya hay uno, sale `-corto-2.mp4`).
- Ese recorte corta el final del video. Si el cierre con el DM queda afuera, mejor quitar escenas del medio en el editor siguiendo los tiempos de abajo.

## Estado de los videos ya hechos (2026-11-25)
En esta carpeta no hay ningún video guardado todavía (los de antes/después y los animados los hace Cam). Cuando los pase, se revisan con el script y a los que pasen de 30 s se les arma la versión corta con los tiempos de abajo.

## Tiempos para que cada reel quede en unos 25 s
Si un video ya hecho es más largo, se recorta siguiendo estos bloques: se acortan o se quitan las escenas del medio y se dejan siempre el gancho y el cierre.

### 1) Antes y después (vender solo por DM vs con página)
| Segundos | Qué va |
|---|---|
| 0-2 | Gancho: "¿Sigues vendiendo solo por DM?" |
| 2-9 | Antes: los mismos mensajes de siempre (precio, horario, dónde están) |
| 9-19 | Después: la página con todo eso a la vista (scroll en el celular) |
| 19-25 | Cierre: Escríbenos por DM @sitioya.pty |

### 2) Cómo funciona
| Segundos | Qué va |
|---|---|
| 0-2 | Gancho: "Tu página en 3 pasos" |
| 2-7 | 1. Escríbenos |
| 7-13 | 2. Te armamos un ejemplo de tu página |
| 13-19 | 3. Lista en pocos días y compartes tu link |
| 19-25 | Cierre: Escríbenos por DM @sitioya.pty |

### 3) Tu negocio en internet, ya
| Segundos | Qué va |
|---|---|
| 0-2 | Gancho: "Tu negocio en internet, ya" |
| 2-18 | Páginas de ejemplo de sitioya.vercel.app en laptop y celular (3 o 4, unos 4 s cada una) |
| 18-25 | Cierre: Escríbenos por DM @sitioya.pty |

### 4) 3 cosas que pierde tu negocio sin página
| Segundos | Qué va |
|---|---|
| 0-2 | Gancho: "3 cosas que pierde tu negocio sin página" |
| 2-8 | Lo 1.º que pierde (el mismo texto del post "3 cosas que pierde tu negocio sin página") |
| 8-14 | Lo 2.º |
| 14-20 | Lo 3.º |
| 20-25 | Cierre: Escríbenos por DM @sitioya.pty |

Recordatorio: negocios ficticios, sin marcas ni logos de terceros y sin reseñas ni cifras inventadas.
