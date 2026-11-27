# Post del GIVEAWAY de @sitioya.pty: premio = una página web Básica gratis.
# Mismo estilo que redes_posts.py y redes_promo.py (colores, fuente, logo y el celular
# con la Heladería de ejemplo).
# Uso: python3 tools/redes_giveaway.py
#   -> redes/posts/giveaway-1080x1350.png (feed) y redes/posts/giveaway-story-1080x1920.png
import os
import sys

from PIL import ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redes_heladeria import (  # noqa: E402
    BLANCO, BLUSH, CORAL, CORAL_D, CREMA, NAVY, SOFT,
    base, envolver, fuente, logo_sitioya, pantalla_portada, pastilla, sombra, texto_ancho,
)
from redes_posts import MENTA_CLARO, SALIDA, celular_chico  # noqa: E402
from redes_promo import NOMBRE, USUARIO, frase, lineas  # noqa: E402

PREMIO = 'Premio: página Básica gratis'
INCLUYE = ('Una sección con tu nombre, logo, colores, fotos, servicios con precios, '
           'horario, mapa, botón de WhatsApp y redes.')
REGLAS = (
    (('Sigue a ', NAVY), (USUARIO, CORAL_D)),
    (('Dale like a este post', NAVY),),
    (('Etiqueta a 2 amigos que tengan negocio', NAVY),),
)
FECHA = 'viernes 4 de diciembre'
ETIQUETA_TEL = 'Página de ejemplo'


def reglas(im, caja, tam, hueco):
    """Tarjeta blanca con las 3 reglas numeradas (círculo coral con el número)."""
    x0, y0, x1, y1 = caja
    sombra(im, caja, 34, desp=(0, 12), difuso=22, alfa=28)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(caja, 34, fill=BLANCO)
    f = fuente(tam, 800)
    fn = fuente(int(tam * 1.15), 900)
    r = int(tam * 0.85)
    paso = 2 * r + hueco
    y = y0 + ((y1 - y0) - (3 * 2 * r + 2 * hueco)) / 2
    cx = x0 + 34 + r
    for n, partes in enumerate(REGLAS, 1):
        d.ellipse((cx - r, y, cx + r, y + 2 * r), fill=CORAL)
        s = str(n)
        d.text((cx - texto_ancho(d, s, fn) / 2, y + r - fn.size * 0.62), s, font=fn, fill=NAVY)
        w = frase(d, (cx + r + 26, y + r - f.size * 0.62), partes, f)
        assert cx + r + 26 + w <= x1 - 24, (partes, w)
        y += paso
    return d


def caja_fecha(d, caja, tam):
    """Caja azul: 'Anunciamos al ganador el' + fecha grande en coral."""
    x0, y0, x1, y1 = caja
    d.rounded_rectangle(caja, 34, fill=NAVY)
    f1, f2 = fuente(tam, 800), fuente(int(tam * 1.5), 900)
    cx = (x0 + x1) / 2
    alto = f1.size * 1.3 + f2.size
    y = y0 + ((y1 - y0) - alto) / 2 - tam * 0.12
    for t, f, c in (('Anunciamos al ganador el', f1, CREMA), (FECHA, f2, CORAL)):
        w = texto_ancho(d, t, f)
        assert w < (x1 - x0) - 50, t
        d.text((cx - w / 2, y), t, font=f, fill=c)
        y += f.size * 1.3


def feed():
    W, H = 1080, 1350
    im = base(W, H)
    d = ImageDraw.Draw(im)
    d.ellipse((520, -120, 1320, 680), fill=MENTA_CLARO)
    d.ellipse((-320, 380, 300, 1000), fill=BLUSH)
    logo_sitioya(im, (66, 56), 58)
    d = ImageDraw.Draw(im)
    pastilla(d, (66, 150), 'GIVEAWAY', fuente(40, 900), CORAL, NAVY, pad=(32, 16))
    izq, ancho_txt = 66, 560
    f = fuente(104, 900)
    y = lineas(d, (izq - 4, 240), ('Gana tu',), f, NAVY, ancho_max=ancho_txt)
    y = lineas(d, (izq - 4, y), ('página', 'web'), f, CORAL_D, ancho_max=ancho_txt)
    # premio
    y += 16
    d.text((izq, y), PREMIO, font=fuente(34, 900), fill=NAVY)
    y += 48
    fi = fuente(26, 500)
    inc = envolver(d, INCLUYE, fi, 545)
    y = lineas(d, (izq, y), inc, fi, SOFT, interlineado=1.32)
    assert y < 780, y
    # celular a la derecha
    ancho = 360
    x_tel, y_tel = W - ancho - 50, 96
    w, h = celular_chico(im, (x_tel, y_tel), pantalla_portada(600, 1170), ancho, girar=3)
    d = ImageDraw.Draw(im)
    pastilla(d, (x_tel + w / 2, y_tel + h - 40), ETIQUETA_TEL, fuente(26, 900), NAVY, CREMA,
             pad=(22, 12), centro=True)
    fin_tel = y_tel + h
    # reglas
    top = max(y, fin_tel) + 26
    caja_r = (66, top, W - 66, top + 250)
    d = reglas(im, caja_r, 34, 14)
    # fecha
    caja_f = (66, caja_r[3] + 20, W - 66, caja_r[3] + 20 + 150)
    caja_fecha(d, caja_f, 32)
    # firma
    fy = caja_f[3] + 26
    fn = fuente(30, 900)
    d.text((66, fy), NOMBRE, font=fn, fill=NAVY)
    fu = fuente(28, 700)
    d.text((W - 66 - texto_ancho(d, USUARIO, fu), fy + 2), USUARIO, font=fu, fill=SOFT)
    assert fy + 40 < H - 30, fy
    return im


def story():
    W, H = 1080, 1920
    im = base(W, H)
    d = ImageDraw.Draw(im)
    d.ellipse((-320, 560, 520, 1400), fill=BLUSH)
    d.ellipse((600, 440, 1440, 1280), fill=MENTA_CLARO)
    # logo arriba, centrado (Instagram tapa los primeros ~120 px con la barra de la story)
    f_logo = fuente(int(64 * 0.62), 900)
    ancho_logo = 64 + 64 * 0.22 + texto_ancho(d, 'SitioYa', f_logo)
    logo_sitioya(im, ((W - ancho_logo) / 2, 140), 64)
    d = ImageDraw.Draw(im)
    pastilla(d, (W / 2, 232), 'GIVEAWAY', fuente(44, 900), CORAL, NAVY, pad=(36, 18), centro=True)
    f = fuente(108, 900)
    y = lineas(d, (W / 2, 322), ('Gana tu',), f, NAVY, centrado=True, ancho_max=990)
    y = lineas(d, (W / 2, y), ('página web',), f, CORAL_D, centrado=True, ancho_max=990)
    # celular a la izquierda, premio a la derecha
    ancho = 284
    x_tel, y_tel = 90, y + 30
    w, h = celular_chico(im, (x_tel, y_tel), pantalla_portada(600, 1170), ancho, girar=-3)
    d = ImageDraw.Draw(im)
    pastilla(d, (x_tel + w / 2, y_tel + h - 40), ETIQUETA_TEL, fuente(26, 900), NAVY, CREMA,
             pad=(22, 12), centro=True)
    px = x_tel + w + 40
    py = y_tel + 40
    pastilla(d, (px, py), 'PREMIO', fuente(28, 900), NAVY, CREMA, pad=(22, 11))
    py += 76
    fp = fuente(56, 900)
    py = lineas(d, (px, py), ('Página Básica',), fp, NAVY, interlineado=1.1, ancho_max=W - 70 - px)
    py = lineas(d, (px, py), ('gratis',), fp, CORAL_D, interlineado=1.1, ancho_max=W - 70 - px)
    py += 18
    fi = fuente(30, 500)
    py = lineas(d, (px, py), envolver(d, INCLUYE, fi, W - 70 - px), fi, SOFT, interlineado=1.32,
                ancho_max=W - 70 - px)
    fin = max(py, y_tel + h)
    # reglas + fecha + firma
    caja_r = (70, fin + 30, W - 70, fin + 30 + 270)
    d = reglas(im, caja_r, 37, 14)
    caja_f = (70, caja_r[3] + 20, W - 70, caja_r[3] + 20 + 160)
    caja_fecha(d, caja_f, 36)
    fy = caja_f[3] + 26
    fn = fuente(34, 900)
    w = texto_ancho(d, NOMBRE, fn)
    d.text(((W - w) / 2, fy), NOMBRE, font=fn, fill=NAVY)
    fu = fuente(30, 700)
    w = texto_ancho(d, USUARIO, fu)
    d.text(((W - w) / 2, fy + 50), USUARIO, font=fu, fill=SOFT)
    # todo arriba de la barra de "responder" de la story (~200 px de abajo)
    assert fy + 90 < H - 190, fy
    return im


def main():
    for nombre, hacer, tam in (('giveaway-1080x1350.png', feed, (1080, 1350)),
                               ('giveaway-story-1080x1920.png', story, (1080, 1920))):
        im = hacer()
        assert im.size == tam, (nombre, im.size)
        im.convert('RGB').save(os.path.join(SALIDA, nombre), optimize=True)
        print(nombre, im.size)


if __name__ == '__main__':
    main()
