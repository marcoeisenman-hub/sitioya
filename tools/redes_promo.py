# Arte promocional de SitioYa para compartir por WhatsApp o Instagram:
# story 1080x1920 y cuadrado 1080x1080, con el celular de la Heladería de ejemplo
# (Nieve & Co, la misma del carrusel "Ejemplo de la semana").
# Uso: python3 tools/redes_promo.py  -> redes/promo/*.png
import os
import sys

from PIL import ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redes_heladeria import (  # noqa: E402
    BLUSH, CORAL, CORAL_D, CREMA, NAVY, SOFT, RAIZ,
    base, envolver, fuente, logo_sitioya, pantalla_portada, pastilla, texto_ancho,
)
from redes_posts import MENTA_CLARO, celular_chico  # noqa: E402

SALIDA = os.path.join(RAIZ, 'redes', 'promo')
os.makedirs(SALIDA, exist_ok=True)

TITULO = ('¿Tu negocio necesita', 'página web?')
SUBTITULO = 'Hacemos páginas para negocios en Panamá, hechas para tu negocio'
TELEFONO = '6919-7559'
USUARIO = '@sitioya.pty'
NOTA = 'Negocio y datos de ejemplo'


def lineas(d, xy, textos, f, color, interlineado=1.08, centrado=False, ancho_max=None):
    """Dibuja líneas ya cortadas; avisa si alguna se sale del ancho."""
    x, y = xy
    for t in textos:
        w = texto_ancho(d, t, f)
        if ancho_max:
            assert w <= ancho_max, (t, w, ancho_max)
        d.text((x - w / 2 if centrado else x, y), t, font=f, fill=color)
        y += int(f.size * interlineado)
    return y


def frase(d, xy, partes, f, centrado=False):
    """Una línea con partes de distinto color: [(texto, color), ...]."""
    x, y = xy
    total = sum(texto_ancho(d, t, f) for t, _ in partes)
    if centrado:
        x -= total / 2
    for t, c in partes:
        d.text((x, y), t, font=f, fill=c)
        x += texto_ancho(d, t, f)
    return total


def caja_contacto(d, caja, tam):
    """Caja azul oscuro con 'Escríbenos por WhatsApp 6919-7559 o en @sitioya.pty'."""
    x0, y0, x1, y1 = caja
    d.rounded_rectangle(caja, int(tam * 1.1), fill=NAVY)
    cx = (x0 + x1) / 2
    f1, f2, f3 = fuente(tam, 800), fuente(int(tam * 1.9), 900), fuente(tam, 800)
    alto = f1.size * 1.3 + f2.size * 1.15 + f3.size
    y = y0 + ((y1 - y0) - alto) / 2 - tam * 0.1
    for t, f, c in (('Escríbenos por WhatsApp', f1, CREMA), (TELEFONO, f2, CORAL)):
        w = texto_ancho(d, t, f)
        assert w < (x1 - x0) - 40, t
        d.text((cx - w / 2, y), t, font=f, fill=c)
        y += f.size * (1.3 if f is f1 else 1.15)
    w = frase(d, (cx, y), (('o en ', CREMA), (USUARIO, CORAL)), f3, centrado=True)
    assert w < (x1 - x0) - 40


def story():
    W, H = 1080, 1920
    im = base(W, H)
    d = ImageDraw.Draw(im)
    d.ellipse((-320, 760, 560, 1640), fill=BLUSH)
    d.ellipse((560, 640, 1440, 1520), fill=MENTA_CLARO)
    # logo arriba, centrado (Instagram tapa los primeros ~120 px con la barra de la story)
    f_logo = fuente(int(70 * 0.62), 900)
    ancho_logo = 70 + 70 * 0.22 + texto_ancho(d, 'SitioYa', f_logo)
    logo_sitioya(im, ((W - ancho_logo) / 2, 150), 70)
    d = ImageDraw.Draw(im)
    f = fuente(94, 900)
    y = lineas(d, (W / 2, 262), TITULO[:1], f, NAVY, centrado=True, ancho_max=990)
    y = lineas(d, (W / 2, y), TITULO[1:], f, CORAL, centrado=True, ancho_max=990)
    fs = fuente(42, 700)
    sub = envolver(d, SUBTITULO, fs, 900)
    assert len(sub) <= 2, sub
    y = lineas(d, (W / 2, y + 26), sub, fs, SOFT, interlineado=1.3, centrado=True)
    # celular con la heladería
    ancho = 410
    y_tel = y + 46
    w, h = celular_chico(im, ((W - ancho) / 2, y_tel), pantalla_portada(600, 1170), ancho)
    d = ImageDraw.Draw(im)
    pastilla(d, (W / 2, y_tel + h - 40), 'Página de ejemplo: Heladería', fuente(32, 900), NAVY, CREMA,
             pad=(28, 14), centro=True)
    fin_tel = y_tel + h + 6
    # contacto
    caja = (90, fin_tel + 40, W - 90, fin_tel + 40 + 250)
    caja_contacto(d, caja, 40)
    nota_y = caja[3] + 22
    d.text(((W - texto_ancho(d, NOTA, fuente(24, 500))) / 2, nota_y), NOTA, font=fuente(24, 500), fill=SOFT)
    # todo tiene que quedar arriba de la barra de "responder" de la story (~200 px de abajo)
    assert nota_y + 30 < H - 150, nota_y
    return im


def cuadrado():
    W = H = 1080
    im = base(W, H)
    d = ImageDraw.Draw(im)
    d.ellipse((560, 120, 1360, 920), fill=MENTA_CLARO)
    d.ellipse((-300, 760, 380, 1440), fill=BLUSH)
    logo_sitioya(im, (66, 60), 62)
    d = ImageDraw.Draw(im)
    izq = 66
    ancho_txt = 560
    f = fuente(80, 900)
    y = lineas(d, (izq, 168), ('¿Tu negocio', 'necesita'), f, NAVY, ancho_max=ancho_txt)
    y = lineas(d, (izq, y), ('página web?',), f, CORAL, ancho_max=ancho_txt)
    fs = fuente(34, 700)
    y = lineas(d, (izq, y + 22), envolver(d, SUBTITULO, fs, 520), fs, SOFT, interlineado=1.3)
    assert y < 640, y
    # celular a la derecha
    ancho = 372
    x_tel, y_tel = W - ancho - 56, 70
    w, h = celular_chico(im, (x_tel, y_tel), pantalla_portada(600, 1170), ancho, girar=3)
    d = ImageDraw.Draw(im)
    pastilla(d, (x_tel + w / 2, y_tel + h - 34), 'Heladería de ejemplo', fuente(26, 900), NAVY, CREMA,
             pad=(22, 12), centro=True)
    assert y_tel + h < 820, y_tel + h
    # contacto abajo, de lado a lado
    caja = (66, 832, W - 66, 1010)
    d.rounded_rectangle(caja, 44, fill=NAVY)
    fc = fuente(46, 900)
    cy = caja[1] + 30
    for partes in ((('Escríbenos por WhatsApp ', CREMA), (TELEFONO, CORAL)),
                   (('o en ', CREMA), (USUARIO, CORAL))):
        w = frase(d, (W / 2, cy), partes, fc, centrado=True)
        assert w < caja[2] - caja[0] - 60, w
        cy += 64
    f_nota = fuente(22, 500)
    d.text((W - 66 - texto_ancho(d, NOTA, f_nota), 1030), NOTA, font=f_nota, fill=SOFT)
    return im


def main():
    for nombre, hacer, tam in (('sitioya-promo-story.png', story, (1080, 1920)),
                               ('sitioya-promo-cuadrado.png', cuadrado, (1080, 1080))):
        im = hacer()
        assert im.size == tam, (nombre, im.size)
        im.convert('RGB').save(os.path.join(SALIDA, nombre), optimize=True)
        print(nombre, im.size)


if __name__ == '__main__':
    main()
