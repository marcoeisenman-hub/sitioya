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

## Estado de los videos ya hechos (2026-11-26)
En `redes/videos/` hay 4 reels hechos con `tools/reels/hacer_reels.sh`, todos de menos de 30 s: `antes-despues.mp4`, `como-funciona.mp4`, `tu-negocio-en-internet.mp4` y `planes.mp4` (cada uno con su portada `.jpg`). Los videos que pase Cam se revisan con el script y a los que pasen de 30 s se les arma la versión corta con los tiempos de abajo.

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
| 0-3 | Gancho: "Tu negocio en internet, ya" |
| 3-19 | 4 páginas de ejemplo en el celular, unos 4 s cada una: panadería, heladería, restaurante ("con tu menú en línea", la página baja hasta su menú) y salón |
| 19-25 | "Y no solo estos: hacemos páginas para cualquier negocio en Panamá" (barbería, cafetería, florería, gimnasio, taller, veterinaria, tienda, spa, fotografía, ¡y más!) |
| 25-29 | Cierre: Escríbenos por DM @sitioya.pty |

El que está en `redes/videos/tu-negocio-en-internet.mp4` (2026-11-26) dura 29.4 s y sigue estos tiempos. Se rehace con `tools/reels/hacer_reels.sh tu-negocio-en-internet`.

### 4) 3 cosas que pierde tu negocio sin página
| Segundos | Qué va |
|---|---|
| 0-2 | Gancho: "3 cosas que pierde tu negocio sin página" |
| 2-8 | Lo 1.º que pierde (el mismo texto del post "3 cosas que pierde tu negocio sin página") |
| 8-14 | Lo 2.º |
| 14-20 | Lo 3.º |
| 20-25 | Cierre: Escríbenos por DM @sitioya.pty |

### 5) Planes: Básica $99 y Completa $199
| Segundos | Qué va |
|---|---|
| 0-3 | Gancho: "¿Cuánto cuesta tu página web?" (salen $99 y $199) |
| 3-9 | Básica $99: tu logo, fotos, precios, horario, mapa y botón de WhatsApp (página de la panadería en el celular) |
| 9-16 | Completa $199: todo lo de la Básica + catálogo o menú, formas de pago, reservas, galería y tu propio dominio (el restaurante baja a su menú; nota chica: el dominio se paga aparte) |
| 16-19 | "Las dos, a tu medida": las 2 tarjetas y el sello "Hechas a la medida de tu negocio" |
| 19-25 | Cierre: Escríbenos por DM @sitioya.pty o al 6919-7559 |

`redes/videos/planes.mp4` (2026-11-26) dura 25.0 s. Se rehace con `tools/reels/hacer_reels.sh planes`. Sin "plantilla" ni "desde cero": las 2 son a la medida.

### 6) A la medida (Síguenos), hecho con Remotion
`redes/videos/a-la-medida.mp4` (+ portada `.jpg`, 2026-11-26, 25 s). Sin voz: todo con texto grande animado, música y efectos sintetizados en `tools/remotion/sonido.py` (sin música con derechos).
| Segundos | Qué va |
|---|---|
| 0-3 | Gancho: "¿Tu negocio todavía no tiene página web?" (palabra por palabra) |
| 3-8.5 | "Te la hacemos a la medida": cinta métrica + celular que se arma solo con "Tu negocio" (tus colores, fotos, precios, horario y mapa, botón de WhatsApp) |
| 8.5-15 | "Dos planes, a tu medida": Básica $99 y Completa $199 (el dominio se paga aparte) |
| 15-19.5 | "Antes de decidir, te armamos un ejemplo de tu página" + sello GRATIS |
| 19.5-25 | Escríbenos al WhatsApp 6919-7559, tarjeta @sitioya.pty que pasa a "Siguiendo" y "¡Síguenos para más ejemplos!" |

Se rehace con `bash tools/remotion/hacer.sh` (una vez: `cd tools/remotion && npm i`). Para verlo y editarlo en vivo: `cd tools/remotion && npm run studio` (primero arma el audio, así que necesita python3 con numpy, igual que `hacer.sh`). Los tiempos de escenas y sonidos están en `tools/remotion/src/linea.json`.

Caption:
> ¿Tu negocio todavía no tiene página web? Te la hacemos a la medida: Básica $99 o Completa $199. Antes de decidir, te armamos un ejemplo gratis para que veas cómo quedaría tu negocio. Escríbenos al WhatsApp 6919-7559 y síguenos para ver más ejemplos
>
> #Panamá #EmprendedoresPanamá #NegociosPanamá #PáginaWeb #SitioYa

## Paquete de la semana para Drive
`python3 tools/armar_contenido.py` arma `contenido/<fecha>/` (los días que ya existen no se tocan; `--rehacer` los arma de nuevo y guarda el anterior en `contenido/_anterior/`) (del 2026-11-27 al 2026-12-03, según el plan semanal) con cada imagen o video final y su caption en un `.txt` al lado. `contenido/` no va a Git ni a Vercel: es para subirlo a la carpeta de Drive. El post giveaway de los viernes queda pendiente hasta definir premio y reglas.

Recordatorio: negocios ficticios, sin marcas ni logos de terceros y sin reseñas ni cifras inventadas.
